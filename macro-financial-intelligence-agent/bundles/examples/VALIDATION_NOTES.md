# Governed Example Validation Notes

## Purpose

These notes explain how the governed example bundles relate to the minimal scaffolding layer.

The examples are static contract artifacts. They are not outputs from live fetchers, real schedulers, production triage, or report composers.

## Scaffold Relationship

| Example | Scaffold expectation demonstrated |
| --- | --- |
| `daily_us_core.example.json` | Shows how retained items should already contain the traceability fields required by `RawItem` and the ingestion bundle schema. |
| `weekly_us_core.example.json` | Shows how multiple retained items can share a governed weekly run mode and report target while preserving source-level traceability. |
| `daily_us_core_empty.example.json` | Shows that no-new-items runs can still produce a valid bundle envelope with `items: []`. |

## Local Check Coverage

`../../validation/scaffold_contract_checks.py` performs only contract-level checks:

- `RawItem.validate_minimum_fields()` accepts a complete raw item.
- `RawItem.validate_minimum_fields()` reports missing minimum fields.
- `IngestionBundleBuilder.validate_request_enums()` accepts governed `run_mode` and `report_target` values.
- `IngestionBundleBuilder.validate_request_enums()` reports invalid enum values.
- Governed example bundles use valid `run_mode`, `report_target`, `source_id`, `authority_tier`, and `preliminary_priority` values.
- Governed example bundles do not add item fields outside `INGESTION_BUNDLE.schema.json`.

## Explicit Non-Coverage

The check file does not validate:

- real YAML parsing,
- live source fetching,
- cron execution,
- dedup algorithm quality,
- tagging accuracy,
- triage scoring correctness,
- JSON Schema Draft 2020-12 compliance,
- report composition,
- kernel handoff execution.

Those behaviors remain intentionally deferred.
