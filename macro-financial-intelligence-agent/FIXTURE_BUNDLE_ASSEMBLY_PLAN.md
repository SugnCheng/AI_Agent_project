# Fixture-Driven Bundle Assembly Plan

## Purpose

This document defines the next narrow, governed path for moving from triaged fixture items into a valid ingestion bundle artifact.

It is a planning document only. It does not implement bundle assembly runtime, report composition, live fetching, scheduler runtime, CI, package migration, external service calls, archive/export automation, or ai-meta-kernel runtime handoff.

## Chosen Slice

The first bundle assembly slice should remain scoped to:

- input source: retained deterministic fixture `NormalizedItem` objects, deterministic `TagSet` outputs, deterministic `DedupResult`, and deterministic `TriageDecision` outputs from the current fixture pipeline
- upstream fixture triage helper: `workflows/daily_us_core_fixture_triage.py`
- upstream fixture file: `fixtures/daily_us_core_raw_items.fixture.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`
- schema authority: `bundles/schemas/INGESTION_BUNDLE.schema.json`
- intended artifact shape: one schema-valid ingestion bundle object with `bundle_metadata`, `bundle_context`, and `items`

The slice should build only from triaged retained fixture items. It should not fetch, schedule, compose reports, archive outputs, or call ai-meta-kernel.

## Why This Is the Safest Next Step

Fixture-driven bundle assembly is the safest next step because the local pipeline now has deterministic fixture inputs through triage:

1. raw fixture records have already been validated against source and region scope;
2. normalized items have stable identifiers, timestamps, canonical URLs, and excerpts;
3. dedup has selected retained items and preserved dedup group membership;
4. tagging has produced schema-facing tag arrays;
5. triage has produced schema-facing `preliminary_priority` values.

This step exercises the ingestion bundle contract without introducing live data, report generation, or kernel handoff behavior.

## Existing Components to Use

| Component | Existing file | Role in bundle assembly slice |
| --- | --- | --- |
| Fixture triage helper | `workflows/daily_us_core_fixture_triage.py` | Provides deterministic triage decisions and should remain the upstream boundary. |
| Fixture triage output contract | `FIXTURE_TRIAGE_OUTPUT_CONTRACT.md` | Defines current triage output fields and deferred behavior markers. |
| Fixture tagger / deduper / normalizer helpers | `workflows/daily_us_core_fixture_tagger.py`, `workflows/daily_us_core_fixture_deduper.py`, `workflows/daily_us_core_fixture_normalizer.py` | Provide retained normalized item data, tags, and dedup groups. |
| Bundle builder scaffold | `bundles/bundle_builder.py` | Defines `BundleBuildRequest` and enum guard boundary. |
| Bundle schema validator | `bundles/bundle_schema_validator.py` | Validates the emitted artifact against `INGESTION_BUNDLE.schema.json`. |
| Ingestion bundle schema | `bundles/schemas/INGESTION_BUNDLE.schema.json` | Authoritative contract for bundle field names and required fields. |
| Source registry | `config/source_registry.yaml` | Supplies `authority_tier`, `official_status`, `priority_weight`, and `trust_score` for bundle item enrichment. |
| Run profiles | `scheduler/run_profiles.yaml` | Supplies `run_mode`, `report_target`, `regions`, source selection, and output policy context. |
| Governed examples | `bundles/examples/*.example.json` | Provide static schema-compatible reference artifacts only. |
| Unified validation wrapper | `validation/run_all_local_checks.py` | Must remain passing after any future bundle assembly scaffold change. |

## Minimum Future Helper Boundary

The next implementation pass should add a fixture-only helper such as:

```text
workflows/daily_us_core_fixture_bundle_assembler.py
```

The helper should:

1. reuse the existing fixture path through triage;
2. construct a schema-compatible in-memory ingestion bundle object;
3. validate it with `bundles/bundle_schema_validator.py`;
4. print a compact deterministic developer-facing summary;
5. optionally print the full bundle artifact with an explicit flag such as `--show-bundle`;
6. avoid writing persistent runtime output unless a later task explicitly defines an output location and retention rule.

This helper should not replace the static governed examples under `bundles/examples/`.

## Triaged Fixture Item to Bundle Item Mapping

The first slice should map only existing deterministic fixture data into schema fields. It should not invent analytical conclusions.

| Bundle item field | Source in current fixture path | First-slice rule |
| --- | --- | --- |
| `item_id` | `NormalizedItem.item_id` | Copy exactly. |
| `source_id` | `NormalizedItem.source_id` | Copy exactly; must be in `config/source_registry.yaml`. |
| `authority_tier` | Source registry entry | Copy from selected source. |
| `region` | `NormalizedItem.region` | Copy exactly; must match profile region `US`. |
| `retrieved_at` | `NormalizedItem.retrieved_at` | Copy exactly. |
| `published_at` | `NormalizedItem.published_at` | Copy exactly. |
| `title` | `NormalizedItem.title` | Copy exactly after normalization trim. |
| `source_url` | `NormalizedItem.source_url` | Copy exactly. |
| `canonical_url` | `NormalizedItem.canonical_url` | Copy exactly. |
| `content_type` | `NormalizedItem.content_type` | Copy exactly. |
| `topic_tags` | `TagSet.topic_tags` | Copy exactly. |
| `market_tags` | `TagSet.market_tags` | Copy exactly. |
| `risk_tags` | `TagSet.risk_tags` | Copy exactly. |
| `preliminary_priority` | `TriageDecision.preliminary_priority` | Copy exactly; must be one of `P1`, `P2`, `P3`, `DROP`. |
| `summary_seed` | `TriageDecision.notes` plus title/source context | Deterministic, non-analytical sentence for later reporting seed; not a report summary. |
| `raw_excerpt` | `NormalizedItem.raw_excerpt` | Copy exactly. |
| `dedup_group_id` | `DedupResult.dedup_groups` | Use the deterministic dedup group ID containing the item. |
| `language` | `NormalizedItem.language` or source registry default | Copy normalized value. |
| `official_status` | Source registry entry | Copy from selected source. |
| `priority_weight` | Source registry entry | Copy from selected source. |
| `trust_score` | Source registry entry | Copy from selected source. |
| `event_cluster_id` | Not yet implemented | Omit in first slice unless a deterministic fixture-only placeholder rule is explicitly approved later. |
| `notes` | `TriageDecision.reason_codes` and fixture marker | Short non-analytical note; may include reason-code list and fixture-only status. |

The first slice should not include full raw text, narrative analysis, final importance judgment, trading advice, report-ready conclusions, or kernel reasoning.

## Bundle Metadata Population

The first slice should populate `bundle_metadata` exactly according to `INGESTION_BUNDLE.schema.json`.

| Field | First-slice population rule |
| --- | --- |
| `bundle_id` | Deterministic fixture ID, for example `fixture_daily_us_core_bundle_2026_04_22_v0_1`. |
| `run_mode` | Copy from selected profile: `daily_brief_run`. |
| `generated_at` | Use a deterministic fixture timestamp derived from the fixture run context, not wall-clock runtime, unless a later contract explicitly permits runtime timestamps. |
| `date_range.start` | Deterministic window start for the fixture slice; should align with `daily_us_core` 24-hour lookback semantics. |
| `date_range.end` | Deterministic window end for the fixture slice; must not be earlier than `date_range.start`. |
| `regions` | Copy selected profile regions: `["US"]`. |
| `source_count` | Count distinct source IDs represented in retained bundle `items`. |
| `item_count_raw` | Count raw fixture records accepted by the fixture loader before dedup. |
| `item_count_after_dedup` | Count retained items after deterministic dedup. |

The first implementation should validate that `item_count_after_dedup <= item_count_raw` and that `len(items) == item_count_after_dedup` unless a future filtered-item rule is introduced.

## Bundle Context Population

The first slice should populate `bundle_context` exactly according to `INGESTION_BUNDLE.schema.json`.

| Field | First-slice population rule |
| --- | --- |
| `report_target` | Copy from selected profile: `daily_brief`. |
| `watchlist_topics` | Use a deterministic fixture-safe list derived from profile output intent and current fixture tags, such as `["monetary_policy", "labor_market", "securities_regulation"]`. |
| `operator_notes` | Explicitly state that the artifact is fixture-only, local, validation-facing, and not produced from live fetching or kernel handoff. |

`bundle_context` must not contain hidden runtime decisions, report prose, or ai-meta-kernel handoff content in this first slice.

## Validation Expectations

The future fixture bundle artifact should be considered valid only if:

1. it validates against `bundles/schemas/INGESTION_BUNDLE.schema.json`;
2. `run_mode` matches the selected `daily_us_core` profile;
3. `report_target` matches the selected `daily_us_core` profile;
4. every item `source_id` is selected by the `daily_us_core` profile and registered in `config/source_registry.yaml`;
5. every item `authority_tier`, `official_status`, `priority_weight`, and `trust_score` aligns with its source registry entry;
6. every item `region` is in the selected profile regions;
7. every retained triaged item appears exactly once in `items`;
8. dedup-dropped items do not appear in `items`;
9. `source_count` equals the number of distinct item `source_id` values;
10. `item_count_raw` equals fixture raw item count;
11. `item_count_after_dedup` equals retained dedup item count;
12. `len(items) == item_count_after_dedup`;
13. every `preliminary_priority` is copied from the corresponding `TriageDecision`;
14. no item contains final analysis, report conclusions, trading advice, or kernel-generated reasoning.

## Developer-Facing Summary Output

The future helper should print a compact summary with fields such as:

| Field | Meaning |
| --- | --- |
| `fixture_bundle_status` | `"ok"` when bundle assembly and validation pass. |
| `profile_id` | `daily_us_core`. |
| `run_mode` | `daily_brief_run`. |
| `report_target` | `daily_brief`. |
| `regions` | `["US"]`. |
| `bundle_id` | Deterministic fixture bundle ID. |
| `schema_validation` | `"ok"` when JSON Schema validation passes. |
| `item_count_raw` | Raw fixture item count before dedup. |
| `item_count_after_dedup` | Retained item count after dedup. |
| `bundle_item_count` | Number of items emitted in the bundle artifact. |
| `source_count` | Number of distinct item source IDs. |
| `priority_counts` | Counts of `P1`, `P2`, `P3`, and `DROP` among bundle items. |
| `deferred_runtime_behavior` | Explicit list of absent runtime behaviors. |

Optional full artifact output should require an explicit flag and should remain clearly marked as fixture-generated.

## In-Scope Next Steps

The next implementation pass should do only the following:

1. Add a fixture-only bundle assembly helper.
2. Reuse current fixture outputs through triage.
3. Map retained triaged fixture items into `INGESTION_BUNDLE.schema.json` item fields.
4. Populate `bundle_metadata` and `bundle_context` with deterministic fixture-safe values.
5. Validate the in-memory artifact against `bundles/schemas/INGESTION_BUNDLE.schema.json`.
6. Validate count, source, region, priority, and dedup invariants.
7. Print a deterministic developer-facing summary.
8. Keep report composition and ai-meta-kernel runtime handoff absent.

## Explicitly Deferred

The bundle assembly slice must not implement:

- live fetching;
- scheduler execution;
- production bundle assembly for live source material;
- report composition;
- archive/export automation;
- Notion, GitHub, or local publishing automation;
- ai-meta-kernel runtime handoff;
- event clustering;
- watchlist matching beyond deterministic fixture-safe `watchlist_topics`;
- operator override persistence;
- source universe expansion;
- open-web crawling;
- CI;
- package migration.

## Guardrails

- Preserve `INGESTION_BUNDLE.schema.json` field names exactly.
- Do not add ad hoc bundle fields.
- Do not treat `summary_seed` as a final report summary.
- Do not include full raw text in bundle items.
- Do not include dropped dedup items.
- Do not treat `preliminary_priority` as final analysis.
- Do not bypass ai-meta-kernel by adding reasoning conclusions to the bundle.
- Do not write persistent artifacts without an explicit output-location contract.
- Run `validation/run_all_local_checks.py` after future bundle assembly changes.

## Recommended Next Phase

Implement `TASK 34 - Fixture-Driven Bundle Assembly Scaffold`.

That pass should introduce the smallest local helper that converts retained triaged fixture items into an in-memory schema-valid ingestion bundle artifact and prints a compact deterministic summary, without report composition, live fetching, scheduler runtime, archive/export automation, or ai-meta-kernel runtime handoff.
