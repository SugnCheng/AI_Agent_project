"""Local dry-run orchestrator scaffold for the daily_us_core v0.1 slice.

This helper exercises the governed config and bundle contracts without live
fetching, scheduler execution, report composition, external services, package
migration, or ai-meta-kernel runtime handoff.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"

PROFILE_ID = "daily_us_core"
DRY_RUN_GENERATED_AT = "2026-04-23T07:05:00+08:00"
DRY_RUN_DATE_RANGE = {
    "start": "2026-04-22T07:00:00+08:00",
    "end": "2026-04-23T07:00:00+08:00",
}


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    """Load governed source registry and run profile config."""

    source_loader_module = load_module(
        "source_registry_loader",
        PROJECT_ROOT / "acquisition" / "source_registry_loader.py",
    )
    run_profiles_loader_module = load_module(
        "run_profiles_loader",
        PROJECT_ROOT / "scheduler" / "run_profiles_loader.py",
    )

    source_registry = source_loader_module.SourceRegistryLoader(
        PROJECT_ROOT / "config" / "source_registry.yaml"
    ).load_structured()
    run_profiles = run_profiles_loader_module.RunProfilesLoader(
        PROJECT_ROOT / "scheduler" / "run_profiles.yaml"
    ).load_structured()

    return source_registry.parsed, run_profiles.parsed


def select_profile(run_profiles: dict[str, Any]) -> dict[str, Any]:
    """Select the governed daily_us_core profile."""

    for profile in run_profiles["profiles"]:
        if profile["profile_id"] == PROFILE_ID:
            if profile.get("enabled") is not True:
                raise ValueError(f"profile '{PROFILE_ID}' must be enabled for this dry-run.")
            return profile
    raise ValueError(f"profile '{PROFILE_ID}' not found.")


def resolve_selected_sources(
    source_registry: dict[str, Any], profile: dict[str, Any]
) -> list[dict[str, Any]]:
    """Resolve and validate profile source references against the whitelist registry."""

    sources_by_id = {source["source_id"]: source for source in source_registry["sources"]}
    include_source_ids = profile.get("source_selection", {}).get("include_source_ids", [])
    allowed_tiers = set(profile.get("source_selection", {}).get("authority_tiers", []))
    profile_regions = set(profile.get("regions", []))

    if not include_source_ids:
        raise ValueError("daily_us_core dry-run requires explicit include_source_ids.")

    selected_sources = []
    errors: list[str] = []

    for source_id in include_source_ids:
        source = sources_by_id.get(source_id)
        if source is None:
            errors.append(f"unknown source_id '{source_id}'")
            continue
        if source.get("enabled") is not True:
            errors.append(f"source_id '{source_id}' is disabled")
        if source.get("authority_tier") not in allowed_tiers:
            errors.append(
                f"source_id '{source_id}' authority_tier '{source.get('authority_tier')}' "
                f"is outside profile tiers {sorted(allowed_tiers)}"
            )
        if source.get("region") not in profile_regions:
            errors.append(
                f"source_id '{source_id}' region '{source.get('region')}' "
                f"is outside profile regions {sorted(profile_regions)}"
            )
        selected_sources.append(source)

    if errors:
        raise ValueError("daily_us_core source resolution failed:\n- " + "\n- ".join(errors))

    return selected_sources


def build_dry_run_request(profile: dict[str, Any]) -> Any:
    """Construct a no-new-items BundleBuildRequest for enum validation only."""

    bundle_builder_module = load_module(
        "bundle_builder",
        PROJECT_ROOT / "bundles" / "bundle_builder.py",
    )

    return bundle_builder_module.BundleBuildRequest(
        bundle_id="dry_run_daily_us_core_no_items",
        run_mode=profile["run_mode"],
        generated_at=DRY_RUN_GENERATED_AT,
        date_range=DRY_RUN_DATE_RANGE,
        regions=profile["regions"],
        report_target=profile["report_target"],
        watchlist_topics=["monetary_policy", "labor_market"],
        operator_notes=(
            "Local dry-run artifact. TODO: replace with generated operator notes "
            "after live acquisition and review workflow exist."
        ),
        items=[],
        item_count_raw=0,
    )


def validate_request_enums(request: Any) -> None:
    """Validate run_mode and report_target through the existing builder scaffold."""

    bundle_builder_module = load_module(
        "bundle_builder",
        PROJECT_ROOT / "bundles" / "bundle_builder.py",
    )
    errors = bundle_builder_module.IngestionBundleBuilder().validate_request_enums(request)
    if errors:
        raise ValueError("dry-run request enum validation failed:\n- " + "\n- ".join(errors))


def build_no_items_bundle_artifact(request: Any) -> dict[str, Any]:
    """Build an in-memory no-new-items bundle-compatible artifact.

    TODO: replace this explicit scaffold with IngestionBundleBuilder.build once
    governed bundle assembly exists.
    """

    return {
        "bundle_metadata": {
            "bundle_id": request.bundle_id,
            "run_mode": request.run_mode,
            "generated_at": request.generated_at,
            "date_range": request.date_range,
            "regions": request.regions,
            "source_count": 0,
            "item_count_raw": request.item_count_raw,
            "item_count_after_dedup": 0,
        },
        "bundle_context": {
            "report_target": request.report_target,
            "watchlist_topics": request.watchlist_topics,
            "operator_notes": request.operator_notes,
        },
        "items": [],
    }


def validate_bundle_artifact(bundle: dict[str, Any]) -> None:
    """Validate the in-memory dry-run bundle against the governed JSON Schema."""

    validator_module = load_module(
        "bundle_schema_validator",
        PROJECT_ROOT / "bundles" / "bundle_schema_validator.py",
    )
    validator = validator_module.IngestionBundleSchemaValidator(
        PROJECT_ROOT / "bundles" / "schemas" / "INGESTION_BUNDLE.schema.json"
    )
    errors = validator.validate_bundle(bundle)
    if errors:
        raise ValueError("dry-run bundle schema validation failed:\n- " + "\n- ".join(errors))


def validate_bundle_semantics(bundle: dict[str, Any]) -> None:
    """Validate the dry-run bundle through the existing semantic validation layer."""

    semantic_module = load_module(
        "semantic_contract_checks",
        PROJECT_ROOT / "validation" / "semantic_contract_checks.py",
    )
    errors = semantic_module.validate_single_bundle_semantics(
        bundle,
        label="daily_us_core_dry_run_artifact",
    )
    if errors:
        raise ValueError("dry-run bundle semantic validation failed:\n- " + "\n- ".join(errors))


def run_unified_local_validation() -> None:
    """Run the existing local validation wrapper on operator request."""

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "validation" / "run_all_local_checks.py"),
        ],
        cwd=REPO_ROOT,
        env=env,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def run_dry_run(include_artifact: bool) -> dict[str, Any]:
    source_registry, run_profiles = load_inputs()
    profile = select_profile(run_profiles)
    selected_sources = resolve_selected_sources(source_registry, profile)
    request = build_dry_run_request(profile)
    validate_request_enums(request)
    bundle = build_no_items_bundle_artifact(request)
    validate_bundle_artifact(bundle)
    validate_bundle_semantics(bundle)

    result: dict[str, Any] = {
        "dry_run_status": "ok",
        "profile_id": profile["profile_id"],
        "run_mode": profile["run_mode"],
        "report_target": profile["report_target"],
        "regions": profile["regions"],
        "selected_source_ids": [source["source_id"] for source in selected_sources],
        "selected_source_count": len(selected_sources),
        "bundle_id": bundle["bundle_metadata"]["bundle_id"],
        "item_count_raw": bundle["bundle_metadata"]["item_count_raw"],
        "item_count_after_dedup": bundle["bundle_metadata"]["item_count_after_dedup"],
        "schema_validation": "ok",
        "semantic_validation": "ok",
        "deferred_runtime_behavior": [
            "live_fetching",
            "scheduler_execution",
            "normalization_dedup_tagging_triage",
            "report_composition",
            "archive_export",
            "ai_meta_kernel_runtime_handoff",
        ],
    }
    if include_artifact:
        result["dry_run_bundle_artifact"] = bundle
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the local daily_us_core dry-run orchestrator scaffold."
    )
    parser.add_argument(
        "--show-artifact",
        action="store_true",
        help="Print the in-memory no-new-items bundle-compatible artifact.",
    )
    parser.add_argument(
        "--run-local-checks",
        action="store_true",
        help="Run validation/run_all_local_checks.py after the dry-run.",
    )
    args = parser.parse_args()

    result = run_dry_run(include_artifact=args.show_artifact)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.run_local_checks:
        run_unified_local_validation()


if __name__ == "__main__":
    main()
