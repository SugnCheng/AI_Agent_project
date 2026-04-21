"""Fixture-driven dedup scaffold for the daily_us_core v0.1 slice.

This helper converts deterministic fixture NormalizedItem objects into a
deterministic DedupResult. It does not fetch sources, execute schedules, tag,
triage, build bundles, compose reports, call external services, or call
ai-meta-kernel.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"
DEDUP_MODE = "fixture_exact_url_v0_1"
DEDUP_KEY_STRATEGY = "canonical_url_key"


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_fixture_normalized_items() -> tuple[dict[str, Any], list[Any]]:
    """Reuse the fixture normalizer path to get deterministic NormalizedItems."""

    normalizer_module = load_module(
        "daily_us_core_fixture_normalizer",
        PROJECT_ROOT / "workflows" / "daily_us_core_fixture_normalizer.py",
    )
    profile, raw_items = normalizer_module.load_validated_fixture_raw_items()
    normalized_items = [
        normalizer_module.normalize_raw_item(raw_item) for raw_item in raw_items
    ]
    normalizer_module.validate_normalized_items(normalized_items)
    return profile, normalized_items


def canonical_url_key(normalized_item: Any) -> str:
    """Build the first v0.1 exact dedup key from canonical_url."""

    return normalized_item.canonical_url.strip().lower().rstrip("/")


def dedup_group_id(dedup_key: str) -> str:
    """Create a deterministic non-semantic group ID from the exact key."""

    digest = hashlib.sha256(dedup_key.encode("utf-8")).hexdigest()[:12]
    return f"dedup_{digest}"


def build_dedup_result(normalized_items: list[Any]) -> Any:
    """Build a deterministic DedupResult using exact canonical URL grouping."""

    deduper_module = load_module(
        "deduper",
        PROJECT_ROOT / "preprocessing" / "dedup" / "deduper.py",
    )
    grouped_items: dict[str, list[Any]] = {}
    for item in normalized_items:
        if not item.item_id:
            raise ValueError("normalized item missing item_id")
        if not item.canonical_url:
            raise ValueError(f"normalized item {item.item_id} missing canonical_url")
        grouped_items.setdefault(canonical_url_key(item), []).append(item)

    retained_items: list[Any] = []
    dropped_items: list[Any] = []
    dedup_groups: dict[str, list[str]] = {}

    for dedup_key in sorted(grouped_items):
        group_items = sorted(grouped_items[dedup_key], key=lambda item: item.item_id)
        group_id = dedup_group_id(dedup_key)
        dedup_groups[group_id] = [item.item_id for item in group_items]
        retained_items.append(group_items[0])
        dropped_items.extend(group_items[1:])

    result = deduper_module.DedupResult(
        retained_items=retained_items,
        dropped_items=dropped_items,
        dedup_groups=dedup_groups,
    )
    validate_dedup_result(normalized_items, result)
    return result


def validate_dedup_result(normalized_items: list[Any], dedup_result: Any) -> None:
    """Validate deterministic fixture dedup invariants."""

    errors: list[str] = []
    input_item_ids = [item.item_id for item in normalized_items]
    grouped_item_ids = [
        item_id for group in dedup_result.dedup_groups.values() for item_id in group
    ]
    retained_ids = {item.item_id for item in dedup_result.retained_items}
    dropped_ids = {item.item_id for item in dedup_result.dropped_items}

    if sorted(grouped_item_ids) != sorted(input_item_ids):
        errors.append("every input item must appear in exactly one dedup group")
    if len(grouped_item_ids) != len(set(grouped_item_ids)):
        errors.append("dedup groups contain repeated item IDs")
    if len(dedup_result.retained_items) + len(dedup_result.dropped_items) != len(
        normalized_items
    ):
        errors.append("retained_items + dropped_items must equal input count")
    if retained_ids.intersection(dropped_ids):
        errors.append("retained and dropped item sets must not overlap")

    group_sizes_by_item_id: dict[str, int] = {}
    for group in dedup_result.dedup_groups.values():
        for item_id in group:
            group_sizes_by_item_id[item_id] = len(group)
    for dropped_item in dedup_result.dropped_items:
        if group_sizes_by_item_id.get(dropped_item.item_id, 0) <= 1:
            errors.append(
                f"dropped item {dropped_item.item_id} must come from a duplicate group"
            )

    if errors:
        raise ValueError("dedup fixture validation failed:\n- " + "\n- ".join(errors))


def run_fixture_deduper(include_groups: bool) -> dict[str, Any]:
    profile, normalized_items = load_fixture_normalized_items()
    dedup_result = build_dedup_result(normalized_items)

    result: dict[str, Any] = {
        "fixture_dedup_status": "ok",
        "profile_id": profile["profile_id"],
        "run_mode": profile["run_mode"],
        "report_target": profile["report_target"],
        "regions": profile["regions"],
        "normalized_item_count": len(normalized_items),
        "retained_item_count": len(dedup_result.retained_items),
        "dropped_item_count": len(dedup_result.dropped_items),
        "dedup_group_count": len(dedup_result.dedup_groups),
        "dedup_mode": DEDUP_MODE,
        "dedup_key_strategy": DEDUP_KEY_STRATEGY,
        "invariant_validation": "ok",
        "deferred_runtime_behavior": [
            "live_fetching",
            "production_deduplication",
            "fuzzy_matching",
            "source_precedence",
            "tagging",
            "triage",
            "bundle_assembly",
            "report_composition",
            "ai_meta_kernel_runtime_handoff",
        ],
    }
    if include_groups:
        retained_ids = {item.item_id for item in dedup_result.retained_items}
        result["dedup_group_summaries"] = [
            {
                "dedup_group_id": group_id,
                "item_ids": item_ids,
                "retained_item_id": next(
                    item_id for item_id in item_ids if item_id in retained_ids
                ),
                "dropped_item_ids": [
                    item_id for item_id in item_ids if item_id not in retained_ids
                ],
            }
            for group_id, item_ids in sorted(dedup_result.dedup_groups.items())
        ]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deduplicate deterministic daily_us_core fixture NormalizedItems."
    )
    parser.add_argument(
        "--show-groups",
        action="store_true",
        help="Print compact dedup group summaries.",
    )
    args = parser.parse_args()

    result = run_fixture_deduper(include_groups=args.show_groups)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
