"""Fixture-driven triage scaffold for the daily_us_core v0.1 slice.

This helper converts retained tagged deterministic fixture items into
deterministic TriageDecision outputs. It does not fetch sources, execute
schedules, build bundles, compose reports, call external services, or call
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
TRIAGE_MODE = "fixture_rule_based_v0_1"
TRIAGE_RULES_VERSION = "TRIAGE_RULES_v0_1"
TRIAGE_PRIORITIES = ("P1", "P2", "P3", "DROP")

APPROVED_REASON_CODES = {
    "TIER_1_OFFICIAL",
    "POLICY_RELEVANCE",
    "REGULATORY_RELEVANCE",
    "RATES_RELEVANCE",
    "MACRO_MARKET_RELEVANCE",
    "LABOR_RELEVANCE",
    "MARKET_STRUCTURE_RELEVANCE",
    "MANDATORY_CENTRAL_BANK_COMMUNICATION",
    "MANDATORY_OFFICIAL_MACRO_RELEASE",
    "MANDATORY_REGULATORY_ACTION_CANDIDATE",
}

MANDATORY_REASON_BY_SOURCE = {
    "fed_fomc": "MANDATORY_CENTRAL_BANK_COMMUNICATION",
    "bls": "MANDATORY_OFFICIAL_MACRO_RELEASE",
    "sec_press": "MANDATORY_REGULATORY_ACTION_CANDIDATE",
}


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_source_registry_by_id() -> dict[str, dict[str, Any]]:
    """Load source registry entries by source_id for authority lookup."""

    loader_module = load_module(
        "source_registry_loader",
        PROJECT_ROOT / "acquisition" / "source_registry_loader.py",
    )
    registry = loader_module.SourceRegistryLoader(
        PROJECT_ROOT / "config" / "source_registry.yaml"
    ).load_structured()
    assert registry.parsed is not None
    return {
        source["source_id"]: source
        for source in registry.parsed["sources"]
    }


def load_tagged_fixture_items() -> tuple[dict[str, Any], list[Any], list[Any], dict[str, Any]]:
    """Reuse the fixture tagger path and return retained items, dropped items, tags."""

    tagger_module = load_module(
        "daily_us_core_fixture_tagger",
        PROJECT_ROOT / "workflows" / "daily_us_core_fixture_tagger.py",
    )
    profile, retained_items, dropped_items = tagger_module.load_retained_fixture_items()
    tagged_items = {
        item.item_id: tagger_module.tag_retained_item(item)
        for item in sorted(retained_items, key=lambda retained_item: retained_item.item_id)
    }
    tagger_module.validate_tagged_items(retained_items, dropped_items, tagged_items)
    return profile, retained_items, dropped_items, tagged_items


def validate_required_metadata(retained_item: Any) -> None:
    """Validate TRIAGE_RULES.md required minimum metadata."""

    required_fields = (
        "item_id",
        "source_id",
        "region",
        "published_at",
        "title",
        "canonical_url",
        "content_type",
    )
    missing = [field for field in required_fields if not getattr(retained_item, field)]
    if missing:
        raise ValueError(f"{retained_item.item_id}: missing triage metadata {missing}")


def priority_from_score(score: int) -> str:
    """Map TRIAGE_RULES.md v0.1 score to preliminary priority."""

    if score >= 7:
        return "P1"
    if score >= 4:
        return "P2"
    if score >= 1:
        return "P3"
    return "DROP"


def evaluate_fixture_item(
    retained_item: Any,
    tag_set: Any,
    source_registry_by_id: dict[str, dict[str, Any]],
) -> Any:
    """Evaluate one retained tagged fixture item with deterministic rules."""

    validate_required_metadata(retained_item)
    source = source_registry_by_id.get(retained_item.source_id)
    if source is None:
        raise ValueError(f"{retained_item.item_id}: source_id not in source registry")

    triage_module = load_module(
        "triage_scaffold",
        PROJECT_ROOT / "preprocessing" / "triage" / "triage_scaffold.py",
    )

    score = 0
    reason_codes: list[str] = []

    if source.get("authority_tier") == "TIER_1" and source.get("official_status") == "official":
        score += 4
        reason_codes.append("TIER_1_OFFICIAL")

    topic_tags = set(tag_set.topic_tags)
    market_tags = set(tag_set.market_tags)
    risk_tags = set(tag_set.risk_tags)

    if "monetary_policy" in topic_tags or "policy_path" in risk_tags:
        score += 3
        reason_codes.append("POLICY_RELEVANCE")
    if "securities_regulation" in topic_tags or "regulatory" in risk_tags:
        score += 3
        reason_codes.append("REGULATORY_RELEVANCE")
    if "rates" in market_tags:
        score += 3
        reason_codes.append("RATES_RELEVANCE")
    if "macro_data" in market_tags:
        score += 3
        reason_codes.append("MACRO_MARKET_RELEVANCE")
    if "labor_market" in topic_tags:
        score += 3
        reason_codes.append("LABOR_RELEVANCE")
    if "equities" in market_tags and "regulatory" in risk_tags:
        score += 3
        reason_codes.append("MARKET_STRUCTURE_RELEVANCE")

    preliminary_priority = priority_from_score(score)
    mandatory_reason = MANDATORY_REASON_BY_SOURCE.get(retained_item.source_id)
    if mandatory_reason is not None:
        reason_codes.append(mandatory_reason)
        preliminary_priority = "P1"

    return triage_module.TriageDecision(
        preliminary_priority=preliminary_priority,
        reason_codes=reason_codes,
        notes="Fixture-only preliminary triage; not final analysis.",
    )


def validate_triage_decisions(
    retained_items: list[Any],
    dropped_items: list[Any],
    tagged_items: dict[str, Any],
    triage_decisions: dict[str, Any],
) -> dict[str, int]:
    """Validate deterministic fixture triage invariants."""

    errors: list[str] = []
    retained_ids = {item.item_id for item in retained_items}
    dropped_ids = {item.item_id for item in dropped_items}
    triaged_ids = set(triage_decisions)

    if triaged_ids != set(tagged_items):
        errors.append("every tagged retained item must receive exactly one TriageDecision")
    if triaged_ids != retained_ids:
        errors.append("triaged item IDs must match retained item IDs")
    if triaged_ids.intersection(dropped_ids):
        errors.append("dropped dedup items must not be triaged")

    priority_counts = {priority: 0 for priority in TRIAGE_PRIORITIES}
    for item_id, decision in triage_decisions.items():
        if not decision.validate_priority():
            errors.append(f"{item_id}: invalid preliminary_priority")
        else:
            priority_counts[decision.preliminary_priority] += 1
        for reason_code in decision.reason_codes:
            if reason_code not in APPROVED_REASON_CODES:
                errors.append(f"{item_id}: unapproved reason code '{reason_code}'")

    if sum(priority_counts.values()) != len(triage_decisions):
        errors.append("priority counts must sum to triaged item count")
    if len(triage_decisions) != len(tagged_items):
        errors.append("triaged_item_count must equal tagged_item_count")

    if errors:
        raise ValueError("triage fixture validation failed:\n- " + "\n- ".join(errors))
    return priority_counts


def run_fixture_triage(include_decisions: bool) -> dict[str, Any]:
    profile, retained_items, dropped_items, tagged_items = load_tagged_fixture_items()
    source_registry_by_id = load_source_registry_by_id()
    retained_by_id = {item.item_id: item for item in retained_items}
    triage_decisions = {
        item_id: evaluate_fixture_item(retained_by_id[item_id], tag_set, source_registry_by_id)
        for item_id, tag_set in sorted(tagged_items.items())
    }
    priority_counts = validate_triage_decisions(
        retained_items,
        dropped_items,
        tagged_items,
        triage_decisions,
    )

    result: dict[str, Any] = {
        "fixture_triage_status": "ok",
        "profile_id": profile["profile_id"],
        "run_mode": profile["run_mode"],
        "report_target": profile["report_target"],
        "regions": profile["regions"],
        "tagged_item_count": len(tagged_items),
        "triaged_item_count": len(triage_decisions),
        "triage_mode": TRIAGE_MODE,
        "triage_rules_version": TRIAGE_RULES_VERSION,
        "priority_counts": priority_counts,
        "reason_code_validation": "ok",
        "dropped_items_triaged": 0,
        "deferred_runtime_behavior": [
            "live_fetching",
            "production_triage",
            "advanced_negative_scoring",
            "watchlist_matching",
            "event_chain_continuity",
            "operator_override_persistence",
            "bundle_assembly",
            "report_composition",
            "ai_meta_kernel_runtime_handoff",
        ],
    }
    if include_decisions:
        result["triage_decision_summaries"] = [
            {
                "item_id": item_id,
                "source_id": retained_by_id[item_id].source_id,
                "preliminary_priority": triage_decisions[item_id].preliminary_priority,
                "reason_codes": triage_decisions[item_id].reason_codes,
                "topic_tags": tagged_items[item_id].topic_tags,
                "market_tags": tagged_items[item_id].market_tags,
                "risk_tags": tagged_items[item_id].risk_tags,
            }
            for item_id in sorted(triage_decisions)
        ]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Triage retained tagged daily_us_core fixture items."
    )
    parser.add_argument(
        "--show-decisions",
        action="store_true",
        help="Print compact triage decision summaries.",
    )
    args = parser.parse_args()

    result = run_fixture_triage(include_decisions=args.show_decisions)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
