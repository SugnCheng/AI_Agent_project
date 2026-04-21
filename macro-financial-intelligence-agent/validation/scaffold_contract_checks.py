"""Minimal scaffold contract checks for v0.1.

This file intentionally uses only Python standard library modules. It does not
fetch sources, run schedules, build production bundles, compose reports, or
call ai-meta-kernel.
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module from a file path without requiring packaging."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_raw_item_minimum_fields() -> None:
    raw_item_module = load_module(
        "raw_item_scaffold",
        PROJECT_ROOT / "acquisition" / "raw_item.py",
    )

    valid_item = raw_item_module.RawItem(
        source_id="fed_fomc",
        retrieved_at="2026-04-22T07:01:00+08:00",
        source_url="https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm",
        title="Example Federal Reserve policy communication",
        raw_text="Example raw text.",
        content_type="statement",
        region="US",
        language="en",
    )
    assert valid_item.validate_minimum_fields() == []

    invalid_item = raw_item_module.RawItem(
        source_id="",
        retrieved_at="2026-04-22T07:01:00+08:00",
        source_url="",
        title="",
        raw_text="",
        content_type="statement",
        region="US",
        language="en",
    )
    assert invalid_item.validate_minimum_fields() == [
        "source_id",
        "source_url",
        "title",
        "raw_text",
    ]


def check_bundle_build_request_enum_validation() -> None:
    bundle_builder_module = load_module(
        "bundle_builder_scaffold",
        PROJECT_ROOT / "bundles" / "bundle_builder.py",
    )
    builder = bundle_builder_module.IngestionBundleBuilder()

    valid_request = bundle_builder_module.BundleBuildRequest(
        bundle_id="bundle_daily_us_core_2026_04_22_example",
        run_mode="daily_brief_run",
        generated_at="2026-04-22T07:05:00+08:00",
        date_range={
            "start": "2026-04-21T07:00:00+08:00",
            "end": "2026-04-22T07:00:00+08:00",
        },
        regions=["US"],
        report_target="daily_brief",
        watchlist_topics=["monetary_policy"],
        operator_notes="Contract check only.",
        items=[],
        item_count_raw=0,
    )
    assert builder.validate_request_enums(valid_request) == []

    invalid_request = bundle_builder_module.BundleBuildRequest(
        bundle_id="bundle_invalid_example",
        run_mode="invalid_run",
        generated_at="2026-04-22T07:05:00+08:00",
        date_range={
            "start": "2026-04-21T07:00:00+08:00",
            "end": "2026-04-22T07:00:00+08:00",
        },
        regions=["US"],
        report_target="invalid_report",
        watchlist_topics=[],
        operator_notes="Contract check only.",
        items=[],
        item_count_raw=0,
    )
    assert builder.validate_request_enums(invalid_request) == [
        "invalid run_mode: invalid_run",
        "invalid report_target: invalid_report",
    ]


def check_governed_example_bundles() -> None:
    schema = json.loads(
        (PROJECT_ROOT / "bundles" / "schemas" / "INGESTION_BUNDLE.schema.json").read_text(
            encoding="utf-8"
        )
    )
    source_registry_text = (
        PROJECT_ROOT / "config" / "source_registry.yaml"
    ).read_text(encoding="utf-8")

    source_ids = set(re.findall(r"source_id:\s+\"([^\"]+)\"", source_registry_text))

    run_modes = set(schema["properties"]["bundle_metadata"]["properties"]["run_mode"]["enum"])
    report_targets = set(
        schema["properties"]["bundle_context"]["properties"]["report_target"]["enum"]
    )
    item_schema = schema["properties"]["items"]["items"]
    required_item_fields = set(item_schema["required"])
    allowed_item_fields = set(item_schema["properties"])
    authority_tiers = set(item_schema["properties"]["authority_tier"]["enum"])
    priorities = set(item_schema["properties"]["preliminary_priority"]["enum"])

    example_paths = sorted((PROJECT_ROOT / "bundles" / "examples").glob("*.example.json"))
    assert example_paths, "expected governed example bundle files"

    for path in example_paths:
        bundle = json.loads(path.read_text(encoding="utf-8"))
        metadata = bundle["bundle_metadata"]
        context = bundle["bundle_context"]
        items = bundle["items"]

        assert metadata["run_mode"] in run_modes, path.name
        assert context["report_target"] in report_targets, path.name
        assert metadata["item_count_after_dedup"] == len(items), path.name
        assert metadata["item_count_after_dedup"] <= metadata["item_count_raw"], path.name

        for item in items:
            missing = required_item_fields - set(item)
            extra = set(item) - allowed_item_fields
            assert not missing, f"{path.name}:{item.get('item_id')} missing {sorted(missing)}"
            assert not extra, f"{path.name}:{item.get('item_id')} extra {sorted(extra)}"
            assert item["source_id"] in source_ids, path.name
            assert item["authority_tier"] in authority_tiers, path.name
            assert item["preliminary_priority"] in priorities, path.name


def main() -> None:
    check_raw_item_minimum_fields()
    check_bundle_build_request_enum_validation()
    check_governed_example_bundles()
    print("scaffold-contract-checks-ok")


if __name__ == "__main__":
    main()
