# Fixture Loader Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for the `daily_us_core` raw fixture loader.

It exists to prevent silent output drift as fixture-driven preprocessing expands. It does not define live fetching, scheduler execution, production normalization, production deduplication, production tagging, production triage, report composition, CI, package migration, external service calls, or ai-meta-kernel runtime handoff.

## Scope

This contract applies only to:

- script: `workflows/daily_us_core_fixture_loader.py`
- fixture file: `fixtures/daily_us_core_raw_items.fixture.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`

It covers the JSON object printed by the fixture loader.

## Required Output Fields

| Field | Current value / type | Meaning | Fixed for current slice? | Future expansion rule |
| --- | --- | --- | --- | --- |
| `fixture_loader_status` | `"ok"` | Indicates the fixture loader completed all local raw-item checks. | Yes | Additional status variants require explicit contract update. |
| `fixture_set_id` | `"daily_us_core_raw_items_v0_1"` | Identifier of the local fixture set. | Yes for this fixture file | May change only with a governed fixture set revision. |
| `profile_id` | `"daily_us_core"` | Governed profile selected from `scheduler/run_profiles.yaml`. | Yes | Do not broaden beyond this profile in this helper without approval. |
| `run_mode` | `"daily_brief_run"` | Run mode from the selected profile. | Yes | Must remain aligned with the selected profile. |
| `report_target` | `"daily_brief"` | Report target from the selected profile. | Yes | Must remain aligned with the selected profile and report templates. |
| `regions` | `["US"]` | Regions declared by the selected profile. | Yes | Additional regions require explicit profile/config approval. |
| `fixture_item_count` | integer | Number of fixture records converted into valid `RawItem` objects. | Derived | Must equal the number of accepted fixture raw items. |
| `validated_source_ids` | list of source IDs | Fixture source IDs that passed selected-source validation. | Derived | Must remain a subset of `daily_us_core` selected sources. |
| `minimum_field_validation` | `"ok"` | Every accepted fixture passed `RawItem.validate_minimum_fields()`. | Yes | Additional states require explicit contract update. |
| `source_selection_validation` | `"ok"` | Every accepted fixture source is selected by `daily_us_core`. | Yes | Additional states require explicit contract update. |
| `region_validation` | `"ok"` | Every accepted fixture region matches selected profile regions. | Yes | Additional states require explicit contract update. |
| `deferred_runtime_behavior` | list of strings | Explicit marker of runtime behaviors not implemented in this helper. | Yes | May shrink only when a behavior is intentionally implemented and documented. |

## Optional Output Field

| Field | Trigger | Meaning | Constraints |
| --- | --- | --- | --- |
| `raw_item_summaries` | Present only with `--show-items` | Compact summaries of validated `RawItem` objects. | Must not include full raw text or analytical interpretation. |

## Current Fixed Values

The current fixture loader slice fixes these values:

```json
{
  "fixture_loader_status": "ok",
  "fixture_set_id": "daily_us_core_raw_items_v0_1",
  "profile_id": "daily_us_core",
  "run_mode": "daily_brief_run",
  "report_target": "daily_brief",
  "regions": ["US"],
  "minimum_field_validation": "ok",
  "source_selection_validation": "ok",
  "region_validation": "ok"
}
```

## Validation Requirements

The fixture loader output is valid only if:

1. the fixture JSON object has `profile_id = daily_us_core`;
2. `raw_items` is a non-empty list;
3. each fixture record maps to supported `RawItem` fields only;
4. each fixture record can be converted into a `RawItem`;
5. each `RawItem` passes `validate_minimum_fields()`;
6. each `RawItem.source_id` is selected by `daily_us_core`;
7. each `RawItem.region` is included in the selected profile regions.

## Deferred Runtime Behaviors

The following behaviors must remain absent from this fixture loader until explicitly implemented in a later governed task:

- `live_fetching`
- `normalization`
- `deduplication`
- `tagging`
- `triage`
- `bundle_assembly`
- `report_composition`
- `ai_meta_kernel_runtime_handoff`

These markers are intentionally present in `deferred_runtime_behavior` so future expansion cannot silently change the helper's scope.

## Drift Control Rules

- Do not rename required output fields without updating this contract.
- Do not remove validation status fields without replacing them with equivalent explicit status.
- Do not add production preprocessing behavior while leaving it listed under `deferred_runtime_behavior`.
- Do not include full `raw_text` in `raw_item_summaries`.
- Do not change this helper from `daily_us_core` to a generic fixture runner without a new contract pass.
- Do not treat fixture metadata as source evidence or market analysis.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_loader.py'
```

To inspect compact item summaries:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_loader.py' --show-items
```
