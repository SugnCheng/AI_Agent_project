# Fixture-Driven Tagging Plan

## Purpose

This document defines the next narrow, governed path for moving from retained deterministic fixture `NormalizedItem` objects into deterministic tag outputs.

It is a planning document only. It does not implement tagging runtime, production tagging, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, triage, bundle assembly, or ai-meta-kernel runtime handoff.

## Chosen Slice

The first tagging slice should remain scoped to:

- input source: retained deterministic fixture `NormalizedItem` objects from `workflows/daily_us_core_fixture_deduper.py`
- upstream normalizer: `workflows/daily_us_core_fixture_normalizer.py`
- upstream fixture file: `fixtures/daily_us_core_raw_items.fixture.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`
- output shape: `TagSet` from `preprocessing/tagging/tagger.py`

The slice should tag only retained fixture items that have already passed fixture loading, deterministic normalization, and deterministic dedup.

## Why This Is the Safest Next Step

Fixture-driven tagging is the safest next step because it exercises the first descriptive metadata boundary after item retention is stable.

It provides:

- deterministic local input from retained fixture items;
- repeatable metadata output for review;
- an early check that tag fields can align with the ingestion bundle schema later;
- a controlled point to define initial vocabularies before triage exists;
- no priority scoring, final analysis, report drafting, or kernel reasoning.

## Existing Components to Use

| Component | Existing file | Role in tagging slice |
| --- | --- | --- |
| Fixture deduper | `workflows/daily_us_core_fixture_deduper.py` | Provide retained deterministic `NormalizedItem` objects. |
| Fixture deduper output contract | `FIXTURE_DEDUPER_OUTPUT_CONTRACT.md` | Preserve dedup output boundary. |
| Normalized item shape | `preprocessing/normalize/normalizer.py` | Input object contract. |
| Tag set shape | `preprocessing/tagging/tagger.py` | Output object contract. |
| Ingestion bundle schema | `bundles/schemas/INGESTION_BUNDLE.schema.json` | Later target field compatibility for tag arrays. |
| Unified validation wrapper | `validation/run_all_local_checks.py` | Must remain passing after any tagging scaffold change. |

## Minimum Tag Output Shape

The first tag output should map cleanly to the existing `TagSet` shape:

| Field | Minimum v0.1 meaning |
| --- | --- |
| `topic_tags` | Descriptive subject tags derived from source ID, content type, and fixture text keywords. |
| `market_tags` | Descriptive market/asset-context tags derived from deterministic source and content cues. |
| `risk_tags` | Descriptive risk-context tags derived from deterministic source and content cues. |

Recommended developer-facing summary fields for the future helper:

| Field | Meaning |
| --- | --- |
| `fixture_tagging_status` | `"ok"` when deterministic fixture tagging completes. |
| `profile_id` | Must remain `daily_us_core` for the first helper. |
| `run_mode` | Must remain `daily_brief_run`. |
| `report_target` | Must remain `daily_brief`. |
| `regions` | Must remain `["US"]`. |
| `retained_item_count` | Number of retained normalized items received from dedup. |
| `tagged_item_count` | Number of retained items that received a `TagSet`. |
| `tagging_mode` | Suggested value: `"fixture_rule_based_v0_1"`. |
| `tag_vocabulary_version` | Suggested value: `"fixture_tags_v0_1"`. |
| `deferred_runtime_behavior` | Explicit list of behaviors still absent. |

Optional compact item summaries may include:

| Field | Meaning |
| --- | --- |
| `item_id` | Retained normalized item identifier. |
| `source_id` | Source ID copied from the retained item. |
| `topic_tags` | Deterministic topic tags for the retained item. |
| `market_tags` | Deterministic market-context tags for the retained item. |
| `risk_tags` | Deterministic risk-context tags for the retained item. |

## Initial Controlled Tag Vocabulary

The first tagging implementation should use a tiny controlled vocabulary rather than open-ended generated labels.

Recommended initial `topic_tags`:

- `monetary_policy`
- `labor_market`
- `securities_regulation`

Recommended initial `market_tags`:

- `rates`
- `macro_data`
- `equities`
- `credit`

Recommended initial `risk_tags`:

- `policy_path`
- `inflation_growth`
- `regulatory`
- `market_structure`

These labels are intentionally conservative. They are descriptive metadata only and must not be treated as final analysis, priority, or recommendation.

## Deterministic Rules for the First Slice

The first tagging implementation should apply only these rules:

1. Accept retained fixture `NormalizedItem` objects only.
2. Use `source_id`, `content_type`, normalized `title`, and `raw_excerpt` as deterministic inputs.
3. Assign tags from the controlled vocabulary only.
4. For `fed_fomc`, assign `topic_tags = ["monetary_policy"]`, `market_tags = ["rates"]`, and `risk_tags = ["policy_path"]`.
5. For `bls`, assign `topic_tags = ["labor_market"]`, `market_tags = ["macro_data"]`, and `risk_tags = ["inflation_growth"]`.
6. For `sec_press`, assign `topic_tags = ["securities_regulation"]`, `market_tags = ["equities"]`, and `risk_tags = ["regulatory"]`.
7. Keep tag ordering deterministic.
8. Do not infer importance, priority, market impact, investment action, or report conclusions.

If a retained fixture item does not match the approved deterministic rules, the helper should fail visibly rather than inventing new tags.

## Validation Expectations

The first tagging output should be considered valid only if:

1. every retained input item receives exactly one `TagSet`;
2. every tag is drawn from the controlled vocabulary;
3. tag arrays are non-empty for the current fixture items;
4. `tagged_item_count == retained_item_count`;
5. tag ordering is deterministic;
6. no dropped dedup item is tagged;
7. the output retains explicit deferred-behavior markers.

## In-Scope Next Steps

The next implementation pass should do only the following:

1. Add a fixture-only tagging helper or extend the tagger scaffold with deterministic fixture-safe behavior.
2. Reuse retained deterministic `NormalizedItem` objects from the fixture deduper.
3. Assign `TagSet` objects with controlled vocabulary tags.
4. Validate count and vocabulary invariants.
5. Print deterministic developer-facing summary output.
6. Keep fixture deduper output contract unchanged.
7. Mark triage, bundle assembly, and all later behaviors as deferred.

The implementation should not yet emit ingestion bundle items. Tag output is still pre-triage and pre-bundle-assembly.

## Explicitly Deferred

The tagging slice must not implement:

- live fetching;
- scheduler execution;
- production tagging for live pages;
- open-ended tag generation;
- ML/AI-assisted classification;
- priority scoring;
- triage;
- bundle assembly;
- report composition;
- archive/export automation;
- ai-meta-kernel runtime handoff;
- CI;
- package migration.

## Guardrails

- Keep tagging deterministic and fixture-only.
- Do not tag dropped dedup items.
- Do not invent tags outside the controlled vocabulary.
- Do not treat tags as final analysis or recommendation.
- Do not assign preliminary priority during tagging.
- Do not mutate `NormalizedItem` content during tagging.
- Do not use source authority or confidence scoring in this slice.
- Run `validation/run_all_local_checks.py` after tagging-path changes.

## Recommended Next Phase

Implement `TASK 28 - Fixture-Driven Tagging Scaffold`.

That pass should introduce the smallest local helper that converts retained deterministic fixture `NormalizedItem` objects into `TagSet` outputs and prints a compact deterministic summary, without production tagging, triage, bundle assembly, or live fetching.
