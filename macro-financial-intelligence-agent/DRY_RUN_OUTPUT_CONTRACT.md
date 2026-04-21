# Dry-Run Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for the `daily_us_core` dry-run helper.

It exists to prevent silent output drift as the runtime later expands. It does not define live fetching, scheduler execution, report composition, CI, package migration, external service calls, or ai-meta-kernel runtime handoff.

## Scope

This contract applies only to:

- script: `workflows/daily_us_core_dry_run.py`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`

It covers the JSON object printed by the dry-run helper.

## Required Output Fields

| Field | Current value / type | Meaning | Fixed for current slice? | Future expansion rule |
| --- | --- | --- | --- | --- |
| `dry_run_status` | `"ok"` | Indicates the dry-run completed all local checks. | Yes | May later add failure/status variants only with explicit contract update. |
| `profile_id` | `"daily_us_core"` | Governed profile selected from `scheduler/run_profiles.yaml`. | Yes | Do not broaden beyond this profile in this helper without approval. |
| `run_mode` | `"daily_brief_run"` | Run mode from the selected profile. | Yes | Must remain aligned with `INGESTION_BUNDLE.schema.json`. |
| `report_target` | `"daily_brief"` | Report target from the selected profile. | Yes | Must remain mapped to `reporting/templates/DAILY_BRIEF_TEMPLATE.md`. |
| `regions` | `["US"]` | Regions declared by the selected profile. | Yes | Additional regions require explicit profile/config approval. |
| `selected_source_ids` | list of source IDs | Whitelisted source IDs resolved from `include_source_ids`. | Value comes from config | May change only through governed `source_registry.yaml` / `run_profiles.yaml` edits. |
| `selected_source_count` | integer | Count of resolved selected sources. | Derived | Must equal `len(selected_source_ids)`. |
| `bundle_id` | `"dry_run_daily_us_core_no_items"` | Identifier for the in-memory dry-run bundle artifact. | Yes for now | May change when governed bundle assembly exists. |
| `item_count_raw` | `0` | Raw item count before dedup. | Yes | May become positive only after approved live or fixture-based item ingestion. |
| `item_count_after_dedup` | `0` | Retained item count after dedup. | Yes | Must never exceed `item_count_raw`. |
| `schema_validation` | `"ok"` | The dry-run bundle passed `INGESTION_BUNDLE.schema.json`. | Yes | Additional states require explicit contract update. |
| `semantic_validation` | `"ok"` | The dry-run bundle passed current semantic validation helper checks. | Yes | Additional states require explicit contract update. |
| `deferred_runtime_behavior` | list of strings | Explicit marker of runtime behaviors not implemented in this helper. | Yes | May shrink only when a behavior is intentionally implemented and documented. |

## Optional Output Field

| Field | Trigger | Meaning | Constraints |
| --- | --- | --- | --- |
| `dry_run_bundle_artifact` | Present only with `--show-artifact` | In-memory no-new-items bundle-compatible artifact. | Must pass schema validation and semantic validation. It must not replace governed example files. |

## Current Fixed Values

The current dry-run slice fixes these values:

```json
{
  "dry_run_status": "ok",
  "profile_id": "daily_us_core",
  "run_mode": "daily_brief_run",
  "report_target": "daily_brief",
  "regions": ["US"],
  "bundle_id": "dry_run_daily_us_core_no_items",
  "item_count_raw": 0,
  "item_count_after_dedup": 0,
  "schema_validation": "ok",
  "semantic_validation": "ok"
}
```

## Validation Requirements

The dry-run output is valid only if:

1. selected sources are registered in `config/source_registry.yaml`;
2. selected sources are enabled;
3. selected source authority tiers match the profile authority tier filter;
4. selected source regions match the profile regions;
5. the in-memory artifact passes `INGESTION_BUNDLE.schema.json`;
6. the in-memory artifact passes `validate_single_bundle_semantics()`.

## Deferred Runtime Behaviors

The following behaviors must remain absent from this dry-run helper until explicitly implemented in a later governed task:

- `live_fetching`
- `scheduler_execution`
- `normalization_dedup_tagging_triage`
- `report_composition`
- `archive_export`
- `ai_meta_kernel_runtime_handoff`

These markers are intentionally present in `deferred_runtime_behavior` so future expansion cannot silently change the helper's scope.

## Drift Control Rules

- Do not rename required fields without updating this contract.
- Do not remove validation status fields without replacing them with an equivalent explicit status.
- Do not add runtime behavior while leaving it listed under `deferred_runtime_behavior`.
- Do not make `dry_run_bundle_artifact` always-on unless output size and artifact ownership are explicitly reviewed.
- Do not change this helper from `daily_us_core` to a generic profile runner without a new contract pass.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_dry_run.py'
```

To inspect the optional in-memory artifact:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_dry_run.py' --show-artifact
```
