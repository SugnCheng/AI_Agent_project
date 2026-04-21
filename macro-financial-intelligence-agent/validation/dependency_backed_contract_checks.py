"""Dependency-backed contract checks for v0.1.

This validation entrypoint uses the approved dependencies PyYAML and jsonschema.
It validates governed config loading and example bundle schema compliance.

It does not fetch sources, execute schedules, compose reports, call external
services, or call ai-meta-kernel.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module from a file path without requiring package layout."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_structured_config_loading() -> None:
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

    assert isinstance(source_registry.parsed, dict)
    assert isinstance(run_profiles.parsed, dict)
    assert source_registry.parsed["sources"], "source registry must contain governed sources"
    assert run_profiles.parsed["profiles"], "run profiles must contain governed profiles"


def check_example_bundle_schema_validation() -> None:
    validator_module = load_module(
        "bundle_schema_validator",
        PROJECT_ROOT / "bundles" / "bundle_schema_validator.py",
    )
    validator = validator_module.IngestionBundleSchemaValidator(
        PROJECT_ROOT / "bundles" / "schemas" / "INGESTION_BUNDLE.schema.json"
    )

    example_paths = sorted((PROJECT_ROOT / "bundles" / "examples").glob("*.example.json"))
    assert example_paths, "expected governed example bundles"

    failures: list[str] = []
    for path in example_paths:
        errors = validator.validate_bundle_file(path)
        if errors:
            failures.append(f"{path.name}: {errors}")

    assert not failures, "\n".join(failures)


def main() -> None:
    check_structured_config_loading()
    check_example_bundle_schema_validation()
    print("dependency-backed-contract-checks-ok")


if __name__ == "__main__":
    main()
