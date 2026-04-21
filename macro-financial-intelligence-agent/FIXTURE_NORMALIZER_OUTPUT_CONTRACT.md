# Fixture Normalizer Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for the `daily_us_core` fixture normalizer.

It exists to prevent silent output drift as preprocessing expands. It does not define live fetching, scheduler execution, production normalization for live pages, deduplication, tagging, triage, bundle assembly, report composition, CI, package migration, external service calls, or ai-meta-kernel runtime handoff.

## Scope

This contract applies only to:

- script: `workflows/daily_us_core_fixture_normalizer.py`
- upstream fixture loader: `workflows/daily_us_core_fixture_loader.py`
- fixture file: `fixtures/daily_us_core_raw_items.fixture.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`

It covers the JSON object printed by the fixture normalizer.

## Required Output Fields

| Field | Current value / type | Meaning | Fixed for current slice? | Future expansion rule |
| --- | --- | --- | --- | --- |
| `fixture_normalizer_status` | `"ok"` | Indicates the fixture normalizer completed deterministic local normalization checks. | Yes | Additional status variants require explicit contract update. |
| `profile_id` | `"daily_us_core"` | Governed profile selected through the reused fixture loader context. | Yes | Do not broaden beyond this profile in this helper without approval. |
| `run_mode` | `"daily_brief_run"` | Run mode from the selected profile. | Yes | Must remain aligned with the selected profile. |
| `report_target` | `"daily_brief"` | Report target from the selected profile. | Yes | Must remain aligned with the selected profile and report templates. |
| `regions` | `["US"]` | Regions declared by the selected profile. | Yes | Additional regions require explicit profile/config approval. |
| `raw_item_count` | integer | Number of validated fixture `RawItem` inputs received from the fixture loader path. | Derived | Must equal the number of validated raw fixture items accepted for normalization. |
| `normalized_item_count` | integer | Number of deterministic `NormalizedItem` objects produced. | Derived | Must equal `raw_item_count` until filtering or deduplication is explicitly implemented later. |
| `normalization_mode` | `"fixture_deterministic_v0_1"` | Identifier for the current fixture-only deterministic normalization rule set. | Yes | Any rule-set change requires explicit contract update. |
| `raw_excerpt_max_length` | `240` | Maximum character length for deterministic `raw_excerpt` output. | Yes | Changes require explicit contract update and fixture review. |
| `required_field_validation` | `"ok"` | Every produced `NormalizedItem` has required fields populated and unique `item_id` values. | Yes | Additional states require explicit contract update. |
| `deferred_runtime_behavior` | list of strings | Explicit marker of runtime and preprocessing behaviors not implemented in this helper. | Yes | May shrink only when a behavior is intentionally implemented and documented. |

## Optional Output Field

| Field | Trigger | Meaning | Constraints |
| --- | --- | --- | --- |
| `normalized_item_summaries` | Present only with `--show-items` | Compact summaries of deterministic `NormalizedItem` objects. | Must not include full raw text, full excerpts beyond length metadata, tags, triage, market analysis, or report-ready conclusions. |

Current `normalized_item_summaries` entries contain:

| Field | Meaning |
| --- | --- |
| `item_id` | Deterministic fixture-safe item identifier. |
| `source_id` | Source ID copied from the validated `RawItem`. |
| `title` | Trimmed title copied from the validated `RawItem`. |
| `content_type` | Content type copied from the validated `RawItem`. |
| `published_at` | Source publication timestamp, or `retrieved_at` fallback when publication time is missing. |
| `canonical_url` | Canonical URL, or `source_url` fallback when canonical URL is missing. |
| `raw_excerpt_length` | Length of the deterministic excerpt, not the excerpt text itself. |

## Current Fixed Values

The current fixture normalizer slice fixes these values:

```json
{
  "fixture_normalizer_status": "ok",
  "profile_id": "daily_us_core",
  "run_mode": "daily_brief_run",
  "report_target": "daily_brief",
  "regions": ["US"],
  "raw_item_count": 3,
  "normalized_item_count": 3,
  "normalization_mode": "fixture_deterministic_v0_1",
  "raw_excerpt_max_length": 240,
  "required_field_validation": "ok"
}
```

## Deterministic Normalization Rules

The current normalizer applies only these deterministic fixture-safe rules:

1. Trim leading and trailing whitespace from `RawItem.title`.
2. Trim and collapse whitespace in `RawItem.raw_text` before excerpting.
3. Use `canonical_url = source_url` when `RawItem.canonical_url` is missing.
4. Use `published_at = retrieved_at` when `RawItem.published_at` is missing.
5. Generate `item_id` deterministically from `source_id`, publication/retrieval timestamp, and trimmed title.
6. Generate `raw_excerpt` by truncating normalized raw text to `raw_excerpt_max_length`.
7. Copy fixture metadata and add normalization markers only.

The normalizer does not summarize, infer market significance, assign tags, assign priority, or prepare report-ready conclusions.

## Validation Requirements

The fixture normalizer output is valid only if:

1. input `RawItem` objects come from the validated fixture loader path;
2. each accepted raw item produces exactly one `NormalizedItem`;
3. every required `NormalizedItem` field is populated;
4. every generated `item_id` is unique within the current fixture run;
5. `normalized_item_count` equals `raw_item_count`;
6. every excerpt length is less than or equal to `raw_excerpt_max_length`;
7. the output retains the explicit `deferred_runtime_behavior` markers.

## Deferred Runtime Behaviors

The following behaviors must remain absent from this fixture normalizer until explicitly implemented in a later governed task:

- `live_fetching`
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
- Do not change `normalization_mode` without documenting the rule-set change.
- Do not change `raw_excerpt_max_length` without reviewing fixture output stability.
- Do not add deduplication, tagging, triage, bundle assembly, report composition, live fetching, or kernel handoff while leaving those behaviors listed under `deferred_runtime_behavior`.
- Do not include full `raw_text` or analytical interpretation in `normalized_item_summaries`.
- Do not treat `NormalizedItem` output as an ingestion bundle item; bundle assembly remains deferred.
- Do not change this helper from `daily_us_core` to a generic fixture normalizer without a new contract pass.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_normalizer.py'
```

To inspect compact normalized item summaries:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_normalizer.py' --show-items
```
