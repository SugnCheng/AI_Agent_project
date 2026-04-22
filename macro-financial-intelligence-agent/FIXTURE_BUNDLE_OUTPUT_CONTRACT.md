# Fixture Bundle Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for the `daily_us_core` fixture bundle assembler.

It exists to prevent silent output drift as reporting and runtime behavior expand. It does not define live fetching, scheduler execution, production bundle assembly, report composition, archive/export automation, event clustering, operator override persistence, CI, package migration, external service calls, or ai-meta-kernel runtime handoff.

## Scope

This contract applies only to:

- script: `workflows/daily_us_core_fixture_bundle_assembler.py`
- upstream fixture triage helper: `workflows/daily_us_core_fixture_triage.py`
- upstream fixture tagger: `workflows/daily_us_core_fixture_tagger.py`
- upstream fixture deduper: `workflows/daily_us_core_fixture_deduper.py`
- upstream fixture normalizer: `workflows/daily_us_core_fixture_normalizer.py`
- upstream fixture file: `fixtures/daily_us_core_raw_items.fixture.json`
- schema authority: `bundles/schemas/INGESTION_BUNDLE.schema.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`

It covers the compact JSON object printed by the fixture bundle assembler and the optional full in-memory bundle artifact printed with `--show-bundle`.

## Required Output Fields

| Field | Current value / type | Meaning | Fixed for current slice? | Future expansion rule |
| --- | --- | --- | --- | --- |
| `fixture_bundle_status` | `"ok"` | Indicates fixture bundle assembly completed and validation checks passed. | Yes | Additional status variants require explicit contract update. |
| `profile_id` | `"daily_us_core"` | Governed profile inherited from the fixture pipeline. | Yes | Do not broaden beyond this profile in this helper without approval. |
| `run_mode` | `"daily_brief_run"` | Run mode from the selected profile and bundle metadata. | Yes | Must remain aligned with `scheduler/run_profiles.yaml` and bundle schema enums. |
| `report_target` | `"daily_brief"` | Report target from the selected profile and bundle context. | Yes | Must remain aligned with profile config, schema enums, and reporting templates. |
| `regions` | `["US"]` | Regions declared by the selected profile and bundle metadata. | Yes | Additional regions require explicit profile/config approval. |
| `bundle_id` | `"fixture_daily_us_core_bundle_2026_04_23_v0_1"` | Deterministic fixture bundle identifier. | Yes | Changing the ID pattern requires explicit contract update. |
| `schema_validation` | `"ok"` | The in-memory bundle validates against `INGESTION_BUNDLE.schema.json`. | Yes | Additional states require explicit contract update. |
| `invariant_validation` | `"ok"` | The helper's fixture-specific count, dedup, source, and priority invariants passed. | Yes | Additional states require explicit contract update. |
| `item_count_raw` | `3` | Count of fixture items before dedup, currently equal to normalized fixture item count. | Derived | Must match fixture raw item count for this slice. |
| `item_count_after_dedup` | `3` | Count of retained deterministic dedup items. | Derived | Must not exceed `item_count_raw`. |
| `bundle_item_count` | `3` | Number of items emitted in the in-memory bundle artifact. | Derived | Must equal `item_count_after_dedup` until a governed filtered-item rule exists. |
| `source_count` | `3` | Number of distinct item `source_id` values in the bundle. | Derived | Must equal distinct item source count. |
| `priority_counts` | object | Counts of `P1`, `P2`, `P3`, and `DROP` values across bundle items. | Derived | Must sum to `bundle_item_count`. |
| `deferred_runtime_behavior` | list of strings | Explicit marker of runtime behaviors not implemented in this helper. | Yes | May shrink only when a behavior is intentionally implemented and documented. |

## Optional Output Field

| Field | Trigger | Meaning | Constraints |
| --- | --- | --- | --- |
| `fixture_bundle_artifact` | Present only with `--show-bundle` | Full in-memory ingestion bundle object built from retained triaged fixture items. | Must conform to `INGESTION_BUNDLE.schema.json`; must not include report prose, final analysis, external service output, persistent archive metadata, or ai-meta-kernel handoff output. |

The optional `fixture_bundle_artifact` must contain only the schema-governed top-level fields:

- `bundle_metadata`
- `bundle_context`
- `items`

## Current Fixed Values

The current fixture bundle slice fixes these compact output values:

```json
{
  "fixture_bundle_status": "ok",
  "profile_id": "daily_us_core",
  "run_mode": "daily_brief_run",
  "report_target": "daily_brief",
  "regions": ["US"],
  "bundle_id": "fixture_daily_us_core_bundle_2026_04_23_v0_1",
  "schema_validation": "ok",
  "invariant_validation": "ok",
  "item_count_raw": 3,
  "item_count_after_dedup": 3,
  "bundle_item_count": 3,
  "source_count": 3,
  "priority_counts": {
    "P1": 3,
    "P2": 0,
    "P3": 0,
    "DROP": 0
  }
}
```

## Full Bundle Artifact Contract

When `--show-bundle` is used, the helper may include `fixture_bundle_artifact`.

The artifact must remain an in-memory fixture artifact and must follow `INGESTION_BUNDLE.schema.json`.

### `bundle_metadata`

Current fixed / derived fields:

| Field | Current value / rule |
| --- | --- |
| `bundle_id` | `fixture_daily_us_core_bundle_2026_04_23_v0_1`. |
| `run_mode` | `daily_brief_run`. |
| `generated_at` | `2026-04-23T07:15:00+08:00`. |
| `date_range.start` | `2026-04-22T07:00:00+08:00`. |
| `date_range.end` | `2026-04-23T07:00:00+08:00`. |
| `regions` | `["US"]`. |
| `source_count` | Distinct `source_id` count across bundle `items`. |
| `item_count_raw` | Current fixture raw item count, `3`. |
| `item_count_after_dedup` | Current retained dedup count, `3`. |

### `bundle_context`

Current fixed / derived fields:

| Field | Current value / rule |
| --- | --- |
| `report_target` | `daily_brief`. |
| `watchlist_topics` | Deterministically derived from fixture topic tags in the order `monetary_policy`, `labor_market`, `securities_regulation`. |
| `operator_notes` | States that the artifact is fixture-only and not produced from live fetching, scheduler execution, report composition, archive/export automation, or ai-meta-kernel runtime handoff. |

### `items`

Each item is mapped from retained deterministic fixture pipeline outputs:

| Bundle item field | Source |
| --- | --- |
| `item_id` | `NormalizedItem.item_id`. |
| `source_id` | `NormalizedItem.source_id`. |
| `authority_tier` | `config/source_registry.yaml`. |
| `region` | `NormalizedItem.region`. |
| `retrieved_at` | `NormalizedItem.retrieved_at`. |
| `published_at` | `NormalizedItem.published_at`. |
| `title` | `NormalizedItem.title`. |
| `source_url` | `NormalizedItem.source_url`. |
| `canonical_url` | `NormalizedItem.canonical_url`. |
| `content_type` | `NormalizedItem.content_type`. |
| `topic_tags` | `TagSet.topic_tags`. |
| `market_tags` | `TagSet.market_tags`. |
| `risk_tags` | `TagSet.risk_tags`. |
| `preliminary_priority` | `TriageDecision.preliminary_priority`. |
| `summary_seed` | Deterministic non-analytical fixture seed text. |
| `raw_excerpt` | `NormalizedItem.raw_excerpt`. |
| `dedup_group_id` | `DedupResult.dedup_groups`. |
| `language` | `NormalizedItem.language`. |
| `official_status` | `config/source_registry.yaml`. |
| `priority_weight` | `config/source_registry.yaml`. |
| `trust_score` | `config/source_registry.yaml`. |
| `notes` | Fixture-only note with triage reason-code marker. |

The artifact currently omits `event_cluster_id` because event clustering is explicitly deferred.

## Validation Requirements

The fixture bundle output is valid only if:

1. the in-memory artifact validates against `bundles/schemas/INGESTION_BUNDLE.schema.json`;
2. every retained triaged item appears exactly once in `items`;
3. no dedup-dropped item appears in `items`;
4. `source_count` equals the number of distinct item `source_id` values;
5. `item_count_raw` equals the current raw fixture item count;
6. `item_count_after_dedup` equals the retained dedup item count;
7. `bundle_item_count == item_count_after_dedup`;
8. every bundle item `preliminary_priority` is copied from the corresponding `TriageDecision`;
9. `priority_counts` sums to `bundle_item_count`;
10. the output retains explicit `deferred_runtime_behavior` markers.

## Deferred Runtime Behaviors

The following behaviors must remain absent from this fixture bundle assembler until explicitly implemented in a later governed task:

- `live_fetching`
- `scheduler_execution`
- `production_bundle_assembly`
- `report_composition`
- `archive_export`
- `event_clustering`
- `operator_override_persistence`
- `ai_meta_kernel_runtime_handoff`

These markers are intentionally present in `deferred_runtime_behavior` so future expansion cannot silently change the helper's scope.

## Drift Control Rules

- Do not rename compact output fields without updating this contract.
- Do not remove `schema_validation` or `invariant_validation` without replacing them with equivalent explicit status.
- Do not change `bundle_id`, `generated_at`, or date window semantics without documenting the fixture contract change.
- Do not add ad hoc fields inside `fixture_bundle_artifact`; the artifact must remain schema-governed.
- Do not add report prose, final analysis, recommendations, archive metadata, external-service output, or kernel handoff output to this helper.
- Do not add live fetching, scheduler execution, production bundle assembly, report composition, archive/export automation, event clustering, operator override persistence, or kernel handoff while leaving those behaviors listed under `deferred_runtime_behavior`.
- Do not treat `summary_seed` as a final report summary.
- Do not change this helper from `daily_us_core` to a generic bundle assembler without a new contract pass.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_bundle_assembler.py'
```

To inspect the full in-memory bundle artifact:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_fixture_bundle_assembler.py' --show-bundle
```
