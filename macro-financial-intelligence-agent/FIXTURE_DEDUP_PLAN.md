# Fixture-Driven Dedup Plan

## Purpose

This document defines the next narrow, governed path for moving from deterministic fixture-based `NormalizedItem` objects into deterministic dedup results.

It is a planning document only. It does not implement dedup runtime, production deduplication, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, tagging, triage, bundle assembly, or ai-meta-kernel runtime handoff.

## Chosen Slice

The first dedup slice should remain scoped to:

- input source: deterministic fixture `NormalizedItem` objects from `workflows/daily_us_core_fixture_normalizer.py`
- upstream fixture file: `fixtures/daily_us_core_raw_items.fixture.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`
- output shape: `DedupResult` from `preprocessing/dedup/deduper.py`

The slice should deduplicate only fixture items that have already passed fixture loading and deterministic normalization.

## Why This Is the Safest Next Step

Fixture-driven dedup is the safest next step because it exercises the first item-reduction boundary without introducing source acquisition, semantic analysis, tagging, triage, reporting, or kernel reasoning.

It provides:

- deterministic local input from the current fixture normalizer;
- repeatable retained/dropped output for review;
- early validation of duplicate grouping and retained-item accounting;
- a controlled point to catch identity and count drift before bundle assembly exists;
- no production source ranking, fuzzy matching, market interpretation, or downstream report behavior.

## Existing Components to Use

| Component | Existing file | Role in dedup slice |
| --- | --- | --- |
| Fixture normalizer | `workflows/daily_us_core_fixture_normalizer.py` | Provide deterministic fixture `NormalizedItem` objects. |
| Fixture normalizer output contract | `FIXTURE_NORMALIZER_OUTPUT_CONTRACT.md` | Preserve normalization output boundary. |
| Normalized item shape | `preprocessing/normalize/normalizer.py` | Input object contract. |
| Dedup result shape | `preprocessing/dedup/deduper.py` | Output object contract. |
| Unified validation wrapper | `validation/run_all_local_checks.py` | Must remain passing after any dedup scaffold change. |

## Duplicate Grouping Model

The first dedup implementation should use exact deterministic keys only. It should not use fuzzy matching, embeddings, AI summarization, inferred topic similarity, or market-significance interpretation.

Recommended grouping keys, in order:

1. `canonical_url_key`: normalized `canonical_url` after trimming whitespace, lowercasing scheme/host behavior by simple lowercase conversion, and removing a trailing slash.
2. `source_timestamp_title_key`: fallback key built from `source_id`, `published_at`, and a whitespace-collapsed lowercase `title`.

The first implementation should prefer `canonical_url_key` when available because the current fixture normalizer guarantees `canonical_url` is populated through fallback to `source_url`.

## Deterministic Rules for the First Slice

The first dedup implementation should apply only these rules:

1. Accept fixture-derived `NormalizedItem` objects only.
2. Build one duplicate key per item using `canonical_url_key`.
3. Group items by exact duplicate key.
4. Retain every singleton group.
5. For groups with more than one item, retain one deterministic representative.
6. Select the retained representative by lexicographically lowest `item_id` until source precedence rules are explicitly defined.
7. Mark all other items in the group as dropped.
8. Preserve dropped item IDs for review; do not delete evidence silently.
9. Do not infer article similarity, policy importance, market impact, tags, or preliminary priority.

The source-precedence rule from `preprocessing/dedup/deduper.py` remains unresolved for production behavior. The first fixture slice should not pretend to solve it.

## Minimum Retained / Dropped Output

The dedup result should map cleanly to the existing `DedupResult` shape:

| Field | Minimum v0.1 meaning |
| --- | --- |
| `retained_items` | List of retained `NormalizedItem` objects after exact deterministic grouping. |
| `dropped_items` | List of duplicate `NormalizedItem` objects not retained. Empty when no duplicates are found. |
| `dedup_groups` | Mapping from deterministic dedup group ID to ordered item IDs in that group. |

Recommended developer-facing summary fields for the future helper:

| Field | Meaning |
| --- | --- |
| `fixture_dedup_status` | `"ok"` when deterministic fixture dedup completes. |
| `profile_id` | Must remain `daily_us_core` for the first helper. |
| `run_mode` | Must remain `daily_brief_run`. |
| `report_target` | Must remain `daily_brief`. |
| `regions` | Must remain `["US"]`. |
| `normalized_item_count` | Number of input `NormalizedItem` objects. |
| `retained_item_count` | Number of retained normalized items. |
| `dropped_item_count` | Number of duplicate normalized items dropped. |
| `dedup_group_count` | Number of dedup groups emitted. |
| `dedup_mode` | Suggested value: `"fixture_exact_url_v0_1"`. |
| `deferred_runtime_behavior` | Explicit list of behaviors still absent. |

## Validation Expectations

The first dedup output should be considered valid only if:

1. every input item has a populated `item_id` and `canonical_url`;
2. every input item appears in exactly one dedup group;
3. `retained_item_count + dropped_item_count == normalized_item_count`;
4. every dropped item belongs to a group with more than one item;
5. every retained item belongs to a group with at least one item;
6. `dedup_groups` stores item IDs only, not full item bodies;
7. the output retains explicit deferred-behavior markers.

## In-Scope Next Steps

The next implementation pass should do only the following:

1. Add a fixture-only dedup helper or extend the deduper scaffold with deterministic fixture-safe behavior.
2. Reuse deterministic `NormalizedItem` objects from the fixture normalizer.
3. Build exact duplicate groups using `canonical_url_key`.
4. Produce a `DedupResult` with retained items, dropped items, and dedup groups.
5. Validate count invariants and item membership invariants.
6. Print deterministic developer-facing summary output.
7. Keep fixture normalizer output contract unchanged.
8. Mark all later preprocessing behaviors as deferred.

The implementation should not yet emit ingestion bundle items. Dedup output is still pre-tagging, pre-triage, and pre-bundle-assembly.

## Explicitly Deferred

The dedup slice must not implement:

- live fetching;
- scheduler execution;
- production deduplication for live pages;
- fuzzy matching;
- embedding or AI-assisted similarity detection;
- official-source precedence;
- cross-source media-vs-official source ranking;
- tagging;
- triage;
- bundle assembly;
- report composition;
- archive/export automation;
- ai-meta-kernel runtime handoff;
- CI;
- package migration.

## Guardrails

- Keep dedup deterministic and fixture-only.
- Do not drop singleton items.
- Do not infer semantic equivalence beyond exact duplicate keys.
- Do not treat dedup as source credibility analysis.
- Do not assign tags or preliminary priority during dedup.
- Do not remove duplicate evidence without retaining dropped item IDs in the dedup result.
- Do not mutate `NormalizedItem` content during dedup.
- Run `validation/run_all_local_checks.py` after dedup-path changes.

## Recommended Next Phase

Implement `TASK 25 - Fixture-Driven Dedup Scaffold`.

That pass should introduce the smallest local helper that converts deterministic fixture `NormalizedItem` objects into a `DedupResult` and prints a compact deterministic summary, without production deduplication, tagging, triage, bundle assembly, or live fetching.
