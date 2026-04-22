"""Fixture-driven bundle assembly scaffold for the daily_us_core v0.1 slice.

This helper converts retained triaged deterministic fixture items into an
in-memory ingestion bundle artifact and validates it against the governed JSON
Schema. It does not fetch sources, execute schedules, compose reports, persist
artifacts, call external services, or call ai-meta-kernel.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"

BUNDLE_ID = "fixture_daily_us_core_bundle_2026_04_23_v0_1"
BUNDLE_GENERATED_AT = "2026-04-23T07:15:00+08:00"
BUNDLE_DATE_RANGE = {
    "start": "2026-04-22T07:00:00+08:00",
    "end": "2026-04-23T07:00:00+08:00",
}
WATCHLIST_TOPIC_ORDER = (
    "monetary_policy",
    "labor_market",
    "securities_regulation",
)
TRIAGE_PRIORITIES = ("P1", "P2", "P3", "DROP")


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_fixture_pipeline_outputs() -> tuple[
    dict[str, Any],
    list[Any],
    list[Any],
    Any,
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    """Reuse existing fixture helpers through deterministic triage."""

    deduper_module = load_module(
        "daily_us_core_fixture_deduper",
        PROJECT_ROOT / "workflows" / "daily_us_core_fixture_deduper.py",
    )
    tagger_module = load_module(
        "daily_us_core_fixture_tagger",
        PROJECT_ROOT / "workflows" / "daily_us_core_fixture_tagger.py",
    )
    triage_module = load_module(
        "daily_us_core_fixture_triage",
        PROJECT_ROOT / "workflows" / "daily_us_core_fixture_triage.py",
    )

    profile, normalized_items = deduper_module.load_fixture_normalized_items()
    dedup_result = deduper_module.build_dedup_result(normalized_items)

    tagged_items = {
        item.item_id: tagger_module.tag_retained_item(item)
        for item in sorted(dedup_result.retained_items, key=lambda retained: retained.item_id)
    }
    tagger_module.validate_tagged_items(
        dedup_result.retained_items,
        dedup_result.dropped_items,
        tagged_items,
    )

    source_registry_by_id = triage_module.load_source_registry_by_id()
    retained_by_id = {item.item_id: item for item in dedup_result.retained_items}
    triage_decisions = {
        item_id: triage_module.evaluate_fixture_item(
            retained_by_id[item_id],
            tag_set,
            source_registry_by_id,
        )
        for item_id, tag_set in sorted(tagged_items.items())
    }
    triage_module.validate_triage_decisions(
        dedup_result.retained_items,
        dedup_result.dropped_items,
        tagged_items,
        triage_decisions,
    )

    return (
        profile,
        normalized_items,
        dedup_result.retained_items,
        dedup_result,
        tagged_items,
        triage_decisions,
        source_registry_by_id,
    )


def dedup_group_by_item_id(dedup_result: Any) -> dict[str, str]:
    """Map each normalized item ID to its deterministic dedup group ID."""

    group_by_item_id: dict[str, str] = {}
    for group_id, item_ids in dedup_result.dedup_groups.items():
        for item_id in item_ids:
            if item_id in group_by_item_id:
                raise ValueError(f"item_id '{item_id}' appears in multiple dedup groups")
            group_by_item_id[item_id] = group_id
    return group_by_item_id


def build_summary_seed(source_id: str, priority: str, reason_codes: list[str]) -> str:
    """Build deterministic non-analytical seed text for later report drafting."""

    return (
        f"Fixture-only {source_id} item triaged as {priority}; "
        f"reason codes: {', '.join(reason_codes)}."
    )


def build_bundle_items(
    retained_items: list[Any],
    tagged_items: dict[str, Any],
    triage_decisions: dict[str, Any],
    source_registry_by_id: dict[str, dict[str, Any]],
    group_by_item_id: dict[str, str],
) -> list[dict[str, Any]]:
    """Map retained triaged fixture items into schema-compatible bundle items."""

    bundle_items: list[dict[str, Any]] = []
    for item in sorted(retained_items, key=lambda retained: retained.item_id):
        source = source_registry_by_id[item.source_id]
        tag_set = tagged_items[item.item_id]
        decision = triage_decisions[item.item_id]
        reason_codes = list(decision.reason_codes)
        bundle_items.append(
            {
                "item_id": item.item_id,
                "source_id": item.source_id,
                "authority_tier": source["authority_tier"],
                "region": item.region,
                "retrieved_at": item.retrieved_at,
                "published_at": item.published_at,
                "title": item.title,
                "source_url": item.source_url,
                "canonical_url": item.canonical_url,
                "content_type": item.content_type,
                "topic_tags": list(tag_set.topic_tags),
                "market_tags": list(tag_set.market_tags),
                "risk_tags": list(tag_set.risk_tags),
                "preliminary_priority": decision.preliminary_priority,
                "summary_seed": build_summary_seed(
                    item.source_id,
                    decision.preliminary_priority,
                    reason_codes,
                ),
                "raw_excerpt": item.raw_excerpt,
                "dedup_group_id": group_by_item_id[item.item_id],
                "language": item.language,
                "official_status": source["official_status"],
                "priority_weight": source["priority_weight"],
                "trust_score": source["trust_score"],
                "notes": (
                    "Fixture-only bundle item; not final analysis; "
                    f"triage_reason_codes={','.join(reason_codes)}"
                ),
            }
        )
    return bundle_items


def build_watchlist_topics(tagged_items: dict[str, Any]) -> list[str]:
    """Build deterministic fixture-safe watchlist topics from current tags."""

    observed_topics = {
        topic for tag_set in tagged_items.values() for topic in tag_set.topic_tags
    }
    return [topic for topic in WATCHLIST_TOPIC_ORDER if topic in observed_topics]


def build_bundle_artifact(
    profile: dict[str, Any],
    normalized_items: list[Any],
    retained_items: list[Any],
    tagged_items: dict[str, Any],
    bundle_items: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build the in-memory fixture bundle artifact."""

    return {
        "bundle_metadata": {
            "bundle_id": BUNDLE_ID,
            "run_mode": profile["run_mode"],
            "generated_at": BUNDLE_GENERATED_AT,
            "date_range": BUNDLE_DATE_RANGE,
            "regions": profile["regions"],
            "source_count": len({item["source_id"] for item in bundle_items}),
            "item_count_raw": len(normalized_items),
            "item_count_after_dedup": len(retained_items),
        },
        "bundle_context": {
            "report_target": profile["report_target"],
            "watchlist_topics": build_watchlist_topics(tagged_items),
            "operator_notes": (
                "Fixture-only local validation artifact. Not produced from live "
                "fetching, scheduler execution, report composition, archive/export "
                "automation, or ai-meta-kernel runtime handoff."
            ),
        },
        "items": bundle_items,
    }


def validate_bundle_schema(bundle: dict[str, Any]) -> None:
    """Validate the in-memory fixture bundle against the governed JSON Schema."""

    validator_module = load_module(
        "bundle_schema_validator",
        PROJECT_ROOT / "bundles" / "bundle_schema_validator.py",
    )
    validator = validator_module.IngestionBundleSchemaValidator(
        PROJECT_ROOT / "bundles" / "schemas" / "INGESTION_BUNDLE.schema.json"
    )
    errors = validator.validate_bundle(bundle)
    if errors:
        raise ValueError("fixture bundle schema validation failed:\n- " + "\n- ".join(errors))


def validate_bundle_invariants(
    bundle: dict[str, Any],
    normalized_items: list[Any],
    retained_items: list[Any],
    dropped_items: list[Any],
    triage_decisions: dict[str, Any],
) -> dict[str, int]:
    """Validate fixture bundle invariants from the assembly plan."""

    errors: list[str] = []
    item_ids = [item["item_id"] for item in bundle["items"]]
    retained_ids = {item.item_id for item in retained_items}
    dropped_ids = {item.item_id for item in dropped_items}
    triaged_ids = set(triage_decisions)

    if set(item_ids) != retained_ids:
        errors.append("every retained triaged item must appear exactly once in items")
    if len(item_ids) != len(set(item_ids)):
        errors.append("bundle items must not contain duplicate item_id values")
    if set(item_ids).intersection(dropped_ids):
        errors.append("dedup-dropped items must not appear in bundle items")
    if set(item_ids) != triaged_ids:
        errors.append("bundle item IDs must match triaged retained item IDs")

    metadata = bundle["bundle_metadata"]
    source_count = len({item["source_id"] for item in bundle["items"]})
    if metadata["source_count"] != source_count:
        errors.append("source_count must equal distinct item source_id count")
    if metadata["item_count_raw"] != len(normalized_items):
        errors.append("item_count_raw must equal raw fixture item count")
    if metadata["item_count_after_dedup"] != len(retained_items):
        errors.append("item_count_after_dedup must equal retained dedup item count")
    if len(bundle["items"]) != metadata["item_count_after_dedup"]:
        errors.append("len(items) must equal item_count_after_dedup")

    priority_counts = {priority: 0 for priority in TRIAGE_PRIORITIES}
    for item in bundle["items"]:
        decision = triage_decisions[item["item_id"]]
        if item["preliminary_priority"] != decision.preliminary_priority:
            errors.append(
                f"{item['item_id']}: preliminary_priority must copy TriageDecision"
            )
        priority_counts[item["preliminary_priority"]] += 1

    if errors:
        raise ValueError("fixture bundle invariant validation failed:\n- " + "\n- ".join(errors))
    return priority_counts


def run_fixture_bundle_assembler(include_bundle: bool) -> dict[str, Any]:
    (
        profile,
        normalized_items,
        retained_items,
        dedup_result,
        tagged_items,
        triage_decisions,
        source_registry_by_id,
    ) = load_fixture_pipeline_outputs()
    group_by_item_id = dedup_group_by_item_id(dedup_result)
    bundle_items = build_bundle_items(
        retained_items,
        tagged_items,
        triage_decisions,
        source_registry_by_id,
        group_by_item_id,
    )
    bundle = build_bundle_artifact(
        profile,
        normalized_items,
        retained_items,
        tagged_items,
        bundle_items,
    )
    validate_bundle_schema(bundle)
    priority_counts = validate_bundle_invariants(
        bundle,
        normalized_items,
        retained_items,
        dedup_result.dropped_items,
        triage_decisions,
    )

    result: dict[str, Any] = {
        "fixture_bundle_status": "ok",
        "profile_id": profile["profile_id"],
        "run_mode": profile["run_mode"],
        "report_target": profile["report_target"],
        "regions": profile["regions"],
        "bundle_id": bundle["bundle_metadata"]["bundle_id"],
        "schema_validation": "ok",
        "invariant_validation": "ok",
        "item_count_raw": bundle["bundle_metadata"]["item_count_raw"],
        "item_count_after_dedup": bundle["bundle_metadata"]["item_count_after_dedup"],
        "bundle_item_count": len(bundle["items"]),
        "source_count": bundle["bundle_metadata"]["source_count"],
        "priority_counts": priority_counts,
        "deferred_runtime_behavior": [
            "live_fetching",
            "scheduler_execution",
            "production_bundle_assembly",
            "report_composition",
            "archive_export",
            "event_clustering",
            "operator_override_persistence",
            "ai_meta_kernel_runtime_handoff",
        ],
    }
    if include_bundle:
        result["fixture_bundle_artifact"] = bundle
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assemble an in-memory daily_us_core fixture ingestion bundle."
    )
    parser.add_argument(
        "--show-bundle",
        action="store_true",
        help="Print the full in-memory fixture ingestion bundle artifact.",
    )
    args = parser.parse_args()

    result = run_fixture_bundle_assembler(include_bundle=args.show_bundle)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
