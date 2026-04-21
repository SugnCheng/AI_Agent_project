"""Semantic contract checks for macro-financial-intelligence-agent v0.1.

This script implements only the currently in-scope semantic rules documented in
SEMANTIC_VALIDATION_PLAN.md:

- SV-01 through SV-07
- the limited existing-region portion of SV-08

It does not fetch sources, execute schedules, compose reports, add CI, migrate
package layout, or call ai-meta-kernel.
"""

from __future__ import annotations

from datetime import datetime
import importlib.util
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"

REPORT_TARGET_TEMPLATES = {
    "daily_brief": PROJECT_ROOT / "reporting" / "templates" / "DAILY_BRIEF_TEMPLATE.md",
    "weekly_intelligence_report": PROJECT_ROOT
    / "reporting"
    / "templates"
    / "WEEKLY_INTELLIGENCE_REPORT_TEMPLATE.md",
    "special_event_memo": PROJECT_ROOT
    / "reporting"
    / "templates"
    / "SPECIAL_EVENT_MEMO_TEMPLATE.md",
}


def load_module(module_name: str, path: Path) -> Any:
    """Load a module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_datetime(value: str) -> datetime:
    """Parse an ISO-like datetime used by governed examples."""

    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[tuple[Path, dict[str, Any]]]]:
    """Load governed registry, run profiles, schema, and example bundles."""

    source_loader_module = load_module(
        "source_registry_loader",
        PROJECT_ROOT / "acquisition" / "source_registry_loader.py",
    )
    run_profiles_loader_module = load_module(
        "run_profiles_loader",
        PROJECT_ROOT / "scheduler" / "run_profiles_loader.py",
    )

    registry = source_loader_module.SourceRegistryLoader(
        PROJECT_ROOT / "config" / "source_registry.yaml"
    ).load_structured()
    profiles = run_profiles_loader_module.RunProfilesLoader(
        PROJECT_ROOT / "scheduler" / "run_profiles.yaml"
    ).load_structured()
    schema = json.loads(
        (PROJECT_ROOT / "bundles" / "schemas" / "INGESTION_BUNDLE.schema.json").read_text(
            encoding="utf-8"
        )
    )
    examples = [
        (path, json.loads(path.read_text(encoding="utf-8")))
        for path in sorted((PROJECT_ROOT / "bundles" / "examples").glob("*.example.json"))
    ]
    return registry.parsed, profiles.parsed, schema, examples


def validate_run_profile_sources(
    registry: dict[str, Any], profiles: dict[str, Any], errors: list[str]
) -> None:
    """SV-01 and SV-02: validate run profile source references."""

    sources_by_id = {source["source_id"]: source for source in registry["sources"]}

    for profile in profiles["profiles"]:
        profile_id = profile["profile_id"]
        source_selection = profile.get("source_selection", {})
        include_source_ids = source_selection.get("include_source_ids", [])

        for source_id in include_source_ids:
            if source_id not in sources_by_id:
                errors.append(
                    f"SV-01 {profile_id}: include_source_ids references unknown source_id '{source_id}'."
                )
                continue

            if profile.get("enabled") is True and sources_by_id[source_id].get("enabled") is False:
                errors.append(
                    f"SV-02 {profile_id}: active profile selects disabled source_id '{source_id}' "
                    "without an approved override."
                )


def validate_run_modes_and_report_targets(
    profiles: dict[str, Any],
    schema: dict[str, Any],
    examples: list[tuple[Path, dict[str, Any]]],
    errors: list[str],
) -> None:
    """SV-03 and SV-04: validate run modes and report targets."""

    schema_run_modes = set(schema["properties"]["bundle_metadata"]["properties"]["run_mode"]["enum"])
    schema_report_targets = set(
        schema["properties"]["bundle_context"]["properties"]["report_target"]["enum"]
    )
    profile_run_modes = {profile["run_mode"] for profile in profiles["profiles"]}

    for profile in profiles["profiles"]:
        profile_id = profile["profile_id"]
        run_mode = profile["run_mode"]
        report_target = profile["report_target"]

        if run_mode not in schema_run_modes:
            errors.append(
                f"SV-03 {profile_id}: run_mode '{run_mode}' is not present in bundle schema enum."
            )
        if report_target not in schema_report_targets:
            errors.append(
                f"SV-04 {profile_id}: report_target '{report_target}' is not present in bundle schema enum."
            )
        template = REPORT_TARGET_TEMPLATES.get(report_target)
        if template is None or not template.exists():
            errors.append(
                f"SV-04 {profile_id}: report_target '{report_target}' does not map to an existing template."
            )

    for path, bundle in examples:
        run_mode = bundle["bundle_metadata"]["run_mode"]
        report_target = bundle["bundle_context"]["report_target"]
        if run_mode not in schema_run_modes or run_mode not in profile_run_modes:
            errors.append(
                f"SV-03 {path.name}: run_mode '{run_mode}' must exist in schema and run profiles."
            )
        template = REPORT_TARGET_TEMPLATES.get(report_target)
        if report_target not in schema_report_targets or template is None or not template.exists():
            errors.append(
                f"SV-04 {path.name}: report_target '{report_target}' must exist in schema and templates."
            )


def validate_bundle_invariants(examples: list[tuple[Path, dict[str, Any]]], errors: list[str]) -> None:
    """SV-05: validate bundle date and count invariants."""

    for path, bundle in examples:
        metadata = bundle["bundle_metadata"]
        date_range = metadata["date_range"]
        items = bundle["items"]

        try:
            start = parse_datetime(date_range["start"])
            end = parse_datetime(date_range["end"])
        except ValueError as exc:
            errors.append(f"SV-05 {path.name}: invalid date_range datetime: {exc}.")
            continue

        if end < start:
            errors.append(f"SV-05 {path.name}: date_range.end is earlier than date_range.start.")

        item_count_after_dedup = metadata["item_count_after_dedup"]
        item_count_raw = metadata["item_count_raw"]
        source_count = metadata["source_count"]
        distinct_item_sources = {item["source_id"] for item in items}

        if item_count_after_dedup != len(items):
            errors.append(
                f"SV-05 {path.name}: item_count_after_dedup={item_count_after_dedup} "
                f"must equal len(items)={len(items)}."
            )
        if item_count_after_dedup > item_count_raw:
            errors.append(
                f"SV-05 {path.name}: item_count_after_dedup must not exceed item_count_raw."
            )
        if items and source_count > len(distinct_item_sources):
            errors.append(
                f"SV-05 {path.name}: source_count={source_count} must not exceed distinct item sources "
                f"{len(distinct_item_sources)}."
            )
        if not items and (item_count_raw != 0 or item_count_after_dedup != 0):
            errors.append(
                f"SV-05 {path.name}: empty bundle must have item_count_raw=0 and "
                "item_count_after_dedup=0."
            )


def validate_bundle_sources_and_regions(
    registry: dict[str, Any],
    profiles: dict[str, Any],
    examples: list[tuple[Path, dict[str, Any]]],
    errors: list[str],
) -> None:
    """SV-06, SV-07, and limited SV-08: validate source IDs, tiers, and regions."""

    sources_by_id = {source["source_id"]: source for source in registry["sources"]}
    registry_regions = {region["code"] for region in registry["regions"]}

    for profile in profiles["profiles"]:
        profile_id = profile["profile_id"]
        profile_regions = profile.get("regions", [])
        if profile.get("enabled") is True and not profile_regions:
            errors.append(f"SV-08 {profile_id}: active profile must declare at least one region.")
        for region in profile_regions:
            if region not in registry_regions:
                errors.append(
                    f"SV-08 {profile_id}: profile region '{region}' is not defined in source registry."
                )

    for path, bundle in examples:
        for region in bundle["bundle_metadata"]["regions"]:
            if region not in registry_regions:
                errors.append(
                    f"SV-08 {path.name}: bundle region '{region}' is not defined in source registry."
                )

        for item in bundle["items"]:
            item_ref = f"{path.name}:{item.get('item_id', '<missing item_id>')}"
            source_id = item["source_id"]
            source = sources_by_id.get(source_id)

            if source is None:
                errors.append(f"SV-06 {item_ref}: source_id '{source_id}' is not in source registry.")
                continue

            if item["authority_tier"] != source["authority_tier"]:
                errors.append(
                    f"SV-07 {item_ref}: authority_tier '{item['authority_tier']}' does not match "
                    f"registry tier '{source['authority_tier']}'."
                )
            if item["region"] != source["region"]:
                errors.append(
                    f"SV-08 {item_ref}: item region '{item['region']}' does not match registry "
                    f"source region '{source['region']}'."
                )


def run_semantic_checks() -> list[str]:
    """Run all currently in-scope v0.1 semantic checks."""

    registry, profiles, schema, examples = load_inputs()
    errors: list[str] = []

    validate_run_profile_sources(registry, profiles, errors)
    validate_run_modes_and_report_targets(profiles, schema, examples, errors)
    validate_bundle_invariants(examples, errors)
    validate_bundle_sources_and_regions(registry, profiles, examples, errors)

    return errors


def main() -> None:
    errors = run_semantic_checks()
    if errors:
        print("semantic-contract-checks-failed")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("semantic-contract-checks-ok")


if __name__ == "__main__":
    main()
