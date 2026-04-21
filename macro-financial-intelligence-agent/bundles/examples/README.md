# Ingestion Bundle Examples

## Purpose

This folder contains small governed examples for the v0.1 ingestion bundle contract.

These examples are not runtime outputs from real fetchers. They are static contract examples showing how `config/source_registry.yaml`, `scheduler/run_profiles.yaml`, and `bundles/schemas/INGESTION_BUNDLE.schema.json` are expected to align.

## Files

| File | Demonstrates |
| --- | --- |
| `daily_us_core.example.json` | A valid daily brief bundle using `daily_brief_run`, `daily_brief`, and enabled US Tier 1 source IDs. |
| `weekly_us_core.example.json` | A valid weekly intelligence bundle using `weekly_intelligence_run`, `weekly_intelligence_report`, and multiple retained items after deduplication. |
| `daily_us_core_empty.example.json` | A valid no-new-items daily bundle with `items: []`, `item_count_raw: 0`, and `item_count_after_dedup: 0`. |

## Validation Assumptions

- `source_id` values come from `config/source_registry.yaml`.
- `run_mode` values come from `scheduler/run_profiles.yaml` and the ingestion bundle schema.
- `report_target` values map to the reporting templates.
- `authority_tier` values use the registry/schema vocabulary.
- `preliminary_priority` values use the triage/schema vocabulary.
- Timestamps and URLs are illustrative, not evidence of actual retrieval.

## Non-Goals

These examples do not implement fetching, scheduling, preprocessing, triage, bundle building, report composition, or archive behavior.
