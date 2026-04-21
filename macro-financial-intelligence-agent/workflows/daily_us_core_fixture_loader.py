"""Local raw fixture loader scaffold for the daily_us_core v0.1 slice.

This helper validates local fixture raw items as RawItem objects. It does not
fetch sources, execute schedules, normalize, deduplicate, tag, triage, compose
reports, call external services, or call ai-meta-kernel.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"
FIXTURE_PATH = PROJECT_ROOT / "fixtures" / "daily_us_core_raw_items.fixture.json"
PROFILE_ID = "daily_us_core"


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_fixture(path: Path = FIXTURE_PATH) -> dict[str, Any]:
    """Load the governed local raw item fixture file."""

    fixture = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(fixture, dict):
        raise ValueError("raw item fixture must be a JSON object.")
    if fixture.get("profile_id") != PROFILE_ID:
        raise ValueError(f"fixture profile_id must be '{PROFILE_ID}'.")
    raw_items = fixture.get("raw_items")
    if not isinstance(raw_items, list) or not raw_items:
        raise ValueError("fixture raw_items must be a non-empty list.")
    return fixture


def load_daily_us_core_context() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Reuse the dry-run profile/source resolution boundary."""

    dry_run_module = load_module(
        "daily_us_core_dry_run",
        PROJECT_ROOT / "workflows" / "daily_us_core_dry_run.py",
    )
    source_registry, run_profiles = dry_run_module.load_inputs()
    profile = dry_run_module.select_profile(run_profiles)
    selected_sources = dry_run_module.resolve_selected_sources(source_registry, profile)
    return profile, selected_sources


def raw_item_from_record(record: dict[str, Any]) -> Any:
    """Convert one fixture record into a RawItem object."""

    raw_item_module = load_module(
        "raw_item",
        PROJECT_ROOT / "acquisition" / "raw_item.py",
    )
    allowed_fields = {
        "source_id",
        "retrieved_at",
        "source_url",
        "title",
        "raw_text",
        "content_type",
        "region",
        "language",
        "published_at",
        "canonical_url",
        "metadata",
    }
    extra_fields = sorted(set(record) - allowed_fields)
    if extra_fields:
        raise ValueError(f"fixture record has unsupported RawItem fields: {extra_fields}")
    return raw_item_module.RawItem(**record)


def validate_raw_items(
    fixture: dict[str, Any],
    profile: dict[str, Any],
    selected_sources: list[dict[str, Any]],
) -> list[Any]:
    """Validate fixture records as RawItem objects and return converted items."""

    selected_source_ids = {source["source_id"] for source in selected_sources}
    profile_regions = set(profile.get("regions", []))

    raw_items = []
    errors: list[str] = []

    for index, record in enumerate(fixture["raw_items"]):
        item_label = f"raw_items[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{item_label}: must be a JSON object")
            continue

        try:
            raw_item = raw_item_from_record(record)
        except (TypeError, ValueError) as exc:
            errors.append(f"{item_label}: {exc}")
            continue

        missing_fields = raw_item.validate_minimum_fields()
        if missing_fields:
            errors.append(f"{item_label}: missing minimum fields {missing_fields}")
        if raw_item.source_id not in selected_source_ids:
            errors.append(
                f"{item_label}: source_id '{raw_item.source_id}' is not selected by {PROFILE_ID}"
            )
        if raw_item.region not in profile_regions:
            errors.append(
                f"{item_label}: region '{raw_item.region}' is outside profile regions "
                f"{sorted(profile_regions)}"
            )

        raw_items.append(raw_item)

    if errors:
        raise ValueError("raw fixture validation failed:\n- " + "\n- ".join(errors))
    return raw_items


def run_fixture_loader(include_items: bool) -> dict[str, Any]:
    fixture = load_fixture()
    profile, selected_sources = load_daily_us_core_context()
    raw_items = validate_raw_items(fixture, profile, selected_sources)

    result: dict[str, Any] = {
        "fixture_loader_status": "ok",
        "fixture_set_id": fixture["fixture_set_id"],
        "profile_id": profile["profile_id"],
        "run_mode": profile["run_mode"],
        "report_target": profile["report_target"],
        "regions": profile["regions"],
        "fixture_item_count": len(raw_items),
        "validated_source_ids": sorted({item.source_id for item in raw_items}),
        "minimum_field_validation": "ok",
        "source_selection_validation": "ok",
        "region_validation": "ok",
        "deferred_runtime_behavior": [
            "live_fetching",
            "normalization",
            "deduplication",
            "tagging",
            "triage",
            "bundle_assembly",
            "report_composition",
            "ai_meta_kernel_runtime_handoff",
        ],
    }
    if include_items:
        result["raw_item_summaries"] = [
            {
                "source_id": item.source_id,
                "title": item.title,
                "content_type": item.content_type,
                "region": item.region,
                "retrieved_at": item.retrieved_at,
            }
            for item in raw_items
        ]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate local daily_us_core raw item fixtures as RawItem objects."
    )
    parser.add_argument(
        "--show-items",
        action="store_true",
        help="Print compact validated RawItem summaries.",
    )
    args = parser.parse_args()

    result = run_fixture_loader(include_items=args.show_items)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
