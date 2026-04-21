"""Fixture-driven tagging scaffold for the daily_us_core v0.1 slice.

This helper converts retained deterministic fixture NormalizedItem objects into
deterministic TagSet outputs. It does not fetch sources, execute schedules,
triage, build bundles, compose reports, call external services, or call
ai-meta-kernel.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"
TAGGING_MODE = "fixture_rule_based_v0_1"
TAG_VOCABULARY_VERSION = "fixture_tags_v0_1"

CONTROLLED_VOCABULARY: dict[str, set[str]] = {
    "topic_tags": {
        "monetary_policy",
        "labor_market",
        "securities_regulation",
    },
    "market_tags": {
        "rates",
        "macro_data",
        "equities",
        "credit",
    },
    "risk_tags": {
        "policy_path",
        "inflation_growth",
        "regulatory",
        "market_structure",
    },
}

SOURCE_TAG_RULES: dict[str, dict[str, list[str]]] = {
    "fed_fomc": {
        "topic_tags": ["monetary_policy"],
        "market_tags": ["rates"],
        "risk_tags": ["policy_path"],
    },
    "bls": {
        "topic_tags": ["labor_market"],
        "market_tags": ["macro_data"],
        "risk_tags": ["inflation_growth"],
    },
    "sec_press": {
        "topic_tags": ["securities_regulation"],
        "market_tags": ["equities"],
        "risk_tags": ["regulatory"],
    },
}


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_retained_fixture_items() -> tuple[dict[str, Any], list[Any], list[Any]]:
    """Reuse the fixture deduper path and return retained/dropped items."""

    deduper_module = load_module(
        "daily_us_core_fixture_deduper",
        PROJECT_ROOT / "workflows" / "daily_us_core_fixture_deduper.py",
    )
    profile, normalized_items = deduper_module.load_fixture_normalized_items()
    dedup_result = deduper_module.build_dedup_result(normalized_items)
    return profile, dedup_result.retained_items, dedup_result.dropped_items


def tag_retained_item(retained_item: Any) -> Any:
    """Assign deterministic fixture tags to one retained item."""

    if retained_item.source_id not in SOURCE_TAG_RULES:
        raise ValueError(f"no fixture tag rule for source_id '{retained_item.source_id}'")

    tagger_module = load_module(
        "tagger",
        PROJECT_ROOT / "preprocessing" / "tagging" / "tagger.py",
    )
    rules = SOURCE_TAG_RULES[retained_item.source_id]
    return tagger_module.TagSet(
        topic_tags=list(rules["topic_tags"]),
        market_tags=list(rules["market_tags"]),
        risk_tags=list(rules["risk_tags"]),
    )


def validate_tagged_items(
    retained_items: list[Any],
    dropped_items: list[Any],
    tagged_items: dict[str, Any],
) -> None:
    """Validate deterministic fixture tagging invariants."""

    errors: list[str] = []
    retained_ids = {item.item_id for item in retained_items}
    dropped_ids = {item.item_id for item in dropped_items}
    tagged_ids = set(tagged_items)

    if tagged_ids != retained_ids:
        errors.append("every retained item must receive exactly one TagSet")
    if tagged_ids.intersection(dropped_ids):
        errors.append("dropped dedup items must not be tagged")

    for item_id, tag_set in tagged_items.items():
        tag_fields = {
            "topic_tags": tag_set.topic_tags,
            "market_tags": tag_set.market_tags,
            "risk_tags": tag_set.risk_tags,
        }
        for field_name, tags in tag_fields.items():
            if not tags:
                errors.append(f"{item_id}: {field_name} must be non-empty")
            for tag in tags:
                if tag not in CONTROLLED_VOCABULARY[field_name]:
                    errors.append(f"{item_id}: {field_name} contains unknown tag '{tag}'")

    if len(tagged_items) != len(retained_items):
        errors.append("tagged_item_count must equal retained_item_count")

    if errors:
        raise ValueError("tagging fixture validation failed:\n- " + "\n- ".join(errors))


def run_fixture_tagger(include_tags: bool) -> dict[str, Any]:
    profile, retained_items, dropped_items = load_retained_fixture_items()
    tagged_items = {
        item.item_id: tag_retained_item(item)
        for item in sorted(retained_items, key=lambda retained_item: retained_item.item_id)
    }
    validate_tagged_items(retained_items, dropped_items, tagged_items)

    result: dict[str, Any] = {
        "fixture_tagging_status": "ok",
        "profile_id": profile["profile_id"],
        "run_mode": profile["run_mode"],
        "report_target": profile["report_target"],
        "regions": profile["regions"],
        "retained_item_count": len(retained_items),
        "tagged_item_count": len(tagged_items),
        "tagging_mode": TAGGING_MODE,
        "tag_vocabulary_version": TAG_VOCABULARY_VERSION,
        "vocabulary_validation": "ok",
        "dropped_items_tagged": 0,
        "deferred_runtime_behavior": [
            "live_fetching",
            "production_tagging",
            "open_ended_tag_generation",
            "ai_assisted_classification",
            "priority_scoring",
            "triage",
            "bundle_assembly",
            "report_composition",
            "ai_meta_kernel_runtime_handoff",
        ],
    }
    if include_tags:
        retained_by_id = {item.item_id: item for item in retained_items}
        result["tagged_item_summaries"] = [
            {
                "item_id": item_id,
                "source_id": retained_by_id[item_id].source_id,
                "topic_tags": tagged_items[item_id].topic_tags,
                "market_tags": tagged_items[item_id].market_tags,
                "risk_tags": tagged_items[item_id].risk_tags,
            }
            for item_id in sorted(tagged_items)
        ]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tag retained deterministic daily_us_core fixture NormalizedItems."
    )
    parser.add_argument(
        "--show-tags",
        action="store_true",
        help="Print compact tagged item summaries.",
    )
    args = parser.parse_args()

    result = run_fixture_tagger(include_tags=args.show_tags)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
