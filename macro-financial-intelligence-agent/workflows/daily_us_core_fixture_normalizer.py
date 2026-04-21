"""Fixture-driven normalization scaffold for the daily_us_core v0.1 slice.

This helper converts validated local fixture RawItem objects into deterministic
NormalizedItem objects. It does not fetch sources, execute schedules,
deduplicate, tag, triage, build bundles, compose reports, call external
services, or call ai-meta-kernel.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "macro-financial-intelligence-agent"
RAW_EXCERPT_MAX_LENGTH = 240


def load_module(module_name: str, path: Path) -> Any:
    """Load a scaffold module by path without requiring package migration."""

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_validated_fixture_raw_items() -> tuple[dict[str, Any], list[Any]]:
    """Reuse the fixture loader path to get validated RawItem objects."""

    fixture_loader_module = load_module(
        "daily_us_core_fixture_loader",
        PROJECT_ROOT / "workflows" / "daily_us_core_fixture_loader.py",
    )
    fixture = fixture_loader_module.load_fixture()
    profile, selected_sources = fixture_loader_module.load_daily_us_core_context()
    raw_items = fixture_loader_module.validate_raw_items(fixture, profile, selected_sources)
    return profile, raw_items


def stable_slug(value: str) -> str:
    """Create a deterministic compact slug for ID input, not user-facing copy."""

    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "untitled"


def build_item_id(raw_item: Any) -> str:
    """Generate a deterministic fixture-safe item ID."""

    timestamp = raw_item.published_at or raw_item.retrieved_at
    seed = f"{raw_item.source_id}|{timestamp}|{raw_item.title.strip()}"
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
    return f"fixture_{raw_item.source_id}_{stable_slug(raw_item.title)[:40]}_{digest}"


def build_raw_excerpt(raw_text: str) -> str:
    """Create a deterministic excerpt without summarization or analysis."""

    normalized_text = " ".join(raw_text.strip().split())
    return normalized_text[:RAW_EXCERPT_MAX_LENGTH]


def normalize_raw_item(raw_item: Any) -> Any:
    """Convert one validated RawItem to a deterministic NormalizedItem."""

    normalizer_module = load_module(
        "normalizer",
        PROJECT_ROOT / "preprocessing" / "normalize" / "normalizer.py",
    )
    title = raw_item.title.strip()
    published_at = raw_item.published_at or raw_item.retrieved_at
    canonical_url = raw_item.canonical_url or raw_item.source_url
    metadata = dict(raw_item.metadata)
    metadata["normalization_mode"] = "fixture_deterministic_v0_1"
    metadata["raw_excerpt_max_length"] = RAW_EXCERPT_MAX_LENGTH

    return normalizer_module.NormalizedItem(
        item_id=build_item_id(raw_item),
        source_id=raw_item.source_id,
        region=raw_item.region,
        retrieved_at=raw_item.retrieved_at,
        published_at=published_at,
        title=title,
        source_url=raw_item.source_url,
        canonical_url=canonical_url,
        content_type=raw_item.content_type,
        language=raw_item.language,
        raw_excerpt=build_raw_excerpt(raw_item.raw_text),
        metadata=metadata,
    )


def validate_normalized_items(normalized_items: list[Any]) -> None:
    """Validate required NormalizedItem fields are populated."""

    required_fields = (
        "item_id",
        "source_id",
        "region",
        "retrieved_at",
        "published_at",
        "title",
        "source_url",
        "canonical_url",
        "content_type",
        "language",
        "raw_excerpt",
    )
    errors: list[str] = []
    seen_item_ids: set[str] = set()

    for index, item in enumerate(normalized_items):
        item_label = f"normalized_items[{index}]"
        for field in required_fields:
            if not getattr(item, field):
                errors.append(f"{item_label}: missing required field '{field}'")
        if item.item_id in seen_item_ids:
            errors.append(f"{item_label}: duplicate item_id '{item.item_id}'")
        seen_item_ids.add(item.item_id)

    if errors:
        raise ValueError("normalized fixture validation failed:\n- " + "\n- ".join(errors))


def run_fixture_normalizer(include_items: bool) -> dict[str, Any]:
    profile, raw_items = load_validated_fixture_raw_items()
    normalized_items = [normalize_raw_item(raw_item) for raw_item in raw_items]
    validate_normalized_items(normalized_items)

    result: dict[str, Any] = {
        "fixture_normalizer_status": "ok",
        "profile_id": profile["profile_id"],
        "run_mode": profile["run_mode"],
        "report_target": profile["report_target"],
        "regions": profile["regions"],
        "raw_item_count": len(raw_items),
        "normalized_item_count": len(normalized_items),
        "normalization_mode": "fixture_deterministic_v0_1",
        "raw_excerpt_max_length": RAW_EXCERPT_MAX_LENGTH,
        "required_field_validation": "ok",
        "deferred_runtime_behavior": [
            "live_fetching",
            "deduplication",
            "tagging",
            "triage",
            "bundle_assembly",
            "report_composition",
            "ai_meta_kernel_runtime_handoff",
        ],
    }
    if include_items:
        result["normalized_item_summaries"] = [
            {
                "item_id": item.item_id,
                "source_id": item.source_id,
                "title": item.title,
                "content_type": item.content_type,
                "published_at": item.published_at,
                "canonical_url": item.canonical_url,
                "raw_excerpt_length": len(item.raw_excerpt),
            }
            for item in normalized_items
        ]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize validated daily_us_core fixture RawItem objects."
    )
    parser.add_argument(
        "--show-items",
        action="store_true",
        help="Print compact NormalizedItem summaries.",
    )
    args = parser.parse_args()

    result = run_fixture_normalizer(include_items=args.show_items)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
