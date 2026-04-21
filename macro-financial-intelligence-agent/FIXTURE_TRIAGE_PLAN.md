# Fixture-Driven Triage Plan

## Purpose

This document defines the next narrow, governed path for moving from tagged retained fixture items into deterministic preliminary triage outputs.

It is a planning document only. It does not implement triage runtime, production triage, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, bundle assembly, or ai-meta-kernel runtime handoff.

## Chosen Slice

The first triage slice should remain scoped to:

- input source: retained deterministic fixture `NormalizedItem` objects plus deterministic `TagSet` outputs from `workflows/daily_us_core_fixture_tagger.py`
- upstream deduper: `workflows/daily_us_core_fixture_deduper.py`
- upstream fixture file: `fixtures/daily_us_core_raw_items.fixture.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`
- rule authority: `preprocessing/triage/TRIAGE_RULES.md`
- output shape: `TriageDecision` from `preprocessing/triage/triage_scaffold.py`

The slice should triage only retained, tagged fixture items that have already passed fixture loading, deterministic normalization, deterministic dedup, and deterministic tagging.

## Why This Is the Safest Next Step

Fixture-driven triage is the safest next step because it exercises the first priority-assignment boundary after item identity and descriptive metadata are stable.

It provides:

- deterministic local input from retained tagged fixture items;
- repeatable preliminary priority output for review;
- early validation of `P1` / `P2` / `P3` / `DROP` handling;
- a controlled point to translate `TRIAGE_RULES.md` into reviewable rule codes;
- no final analysis, report drafting, bundle assembly, or kernel reasoning.

## Existing Components to Use

| Component | Existing file | Role in triage slice |
| --- | --- | --- |
| Fixture tagger | `workflows/daily_us_core_fixture_tagger.py` | Provide retained deterministic items and `TagSet` outputs. |
| Fixture tagger output contract | `FIXTURE_TAGGER_OUTPUT_CONTRACT.md` | Preserve tagging output boundary. |
| Fixture deduper | `workflows/daily_us_core_fixture_deduper.py` | Preserve retained/dropped item boundary. |
| Triage rules | `preprocessing/triage/TRIAGE_RULES.md` | Governing rule source for preliminary priority. |
| Triage scaffold | `preprocessing/triage/triage_scaffold.py` | Output object contract. |
| Source registry | `config/source_registry.yaml` | Source authority and official status lookup. |
| Unified validation wrapper | `validation/run_all_local_checks.py` | Must remain passing after any triage scaffold change. |

## Minimum Triage Output Shape

The first triage output should map cleanly to the existing `TriageDecision` shape:

| Field | Minimum v0.1 meaning |
| --- | --- |
| `preliminary_priority` | One of `P1`, `P2`, `P3`, or `DROP` from `TRIAGE_RULES.md`. |
| `reason_codes` | Deterministic rule codes explaining the preliminary priority. |
| `notes` | Short non-analytical note for developer/operator review. |

Recommended developer-facing summary fields for the future helper:

| Field | Meaning |
| --- | --- |
| `fixture_triage_status` | `"ok"` when deterministic fixture triage completes. |
| `profile_id` | Must remain `daily_us_core` for the first helper. |
| `run_mode` | Must remain `daily_brief_run`. |
| `report_target` | Must remain `daily_brief`. |
| `regions` | Must remain `["US"]`. |
| `tagged_item_count` | Number of retained tagged fixture items received from tagging. |
| `triaged_item_count` | Number of items assigned a `TriageDecision`. |
| `triage_mode` | Suggested value: `"fixture_rule_based_v0_1"`. |
| `triage_rules_version` | Suggested value: `"TRIAGE_RULES_v0_1"`. |
| `priority_counts` | Count of `P1`, `P2`, `P3`, and `DROP` decisions. |
| `deferred_runtime_behavior` | Explicit list of behaviors still absent. |

Optional compact item summaries may include:

| Field | Meaning |
| --- | --- |
| `item_id` | Retained normalized item identifier. |
| `source_id` | Source ID copied from the retained item. |
| `preliminary_priority` | Deterministic preliminary priority. |
| `reason_codes` | Deterministic reason codes. |
| `topic_tags` | Existing tags passed through for review context. |
| `market_tags` | Existing tags passed through for review context. |
| `risk_tags` | Existing tags passed through for review context. |

## Deterministic Rules for the First Slice

The first triage implementation should apply only these rules from `TRIAGE_RULES.md`:

1. Accept retained tagged fixture items only.
2. Reject or fail visibly if required minimum metadata is missing: `item_id`, `source_id`, `region`, `published_at`, `title`, `canonical_url`, and `content_type`.
3. Add `+4` for `TIER_1` official sources.
4. Add `+3` for policy or regulation relevance when topic/risk tags indicate monetary policy or securities regulation.
5. Add `+3` for rates, inflation, labor, liquidity, credit, or macro relevance when tags indicate rates, macro data, labor, or inflation/growth.
6. Apply mandatory escalation to `P1` for central bank communication, official labor/macro release, or major regulatory/rule action fixture categories.
7. Map score to priority using `TRIAGE_RULES.md`: `>= 7` to `P1`, `4-6` to `P2`, `1-3` to `P3`, `<= 0` to `DROP`.
8. Keep reason code ordering deterministic.
9. Do not infer market impact, write narrative analysis, or replace ai-meta-kernel reasoning.

The first fixture slice should not implement negative scoring except for visible validation failures, because the current fixture path already excludes dropped dedup items, out-of-scope regions, unapproved sources, and missing metadata.

## Expected Fixture Decisions

The current fixture set should produce deterministic preliminary priorities:

| Source | Expected priority | Grounded reason codes |
| --- | --- | --- |
| `fed_fomc` | `P1` | `TIER_1_OFFICIAL`, `POLICY_RELEVANCE`, `RATES_RELEVANCE`, `MANDATORY_CENTRAL_BANK_COMMUNICATION` |
| `bls` | `P1` | `TIER_1_OFFICIAL`, `MACRO_MARKET_RELEVANCE`, `LABOR_RELEVANCE`, `MANDATORY_OFFICIAL_MACRO_RELEASE` |
| `sec_press` | `P1` | `TIER_1_OFFICIAL`, `REGULATORY_RELEVANCE`, `MARKET_STRUCTURE_RELEVANCE`, `MANDATORY_REGULATORY_ACTION_CANDIDATE` |

These priorities remain preliminary. They are candidate packaging signals, not final importance judgments.

## Validation Expectations

The first triage output should be considered valid only if:

1. every tagged retained item receives exactly one `TriageDecision`;
2. every `preliminary_priority` is one of `P1`, `P2`, `P3`, or `DROP`;
3. `triaged_item_count == tagged_item_count`;
4. every emitted reason code comes from the fixture triage rule set;
5. required minimum metadata is present for every triaged item;
6. dropped dedup items are not triaged;
7. priority counts sum to `triaged_item_count`;
8. output retains explicit deferred-behavior markers.

## In-Scope Next Steps

The next implementation pass should do only the following:

1. Add a fixture-only triage helper or extend the triage scaffold with deterministic fixture-safe behavior.
2. Reuse retained tagged fixture items from the fixture tagger.
3. Look up source authority/status from `config/source_registry.yaml`.
4. Apply the deterministic scoring and mandatory escalation rules listed above.
5. Produce `TriageDecision` outputs.
6. Validate count, priority, reason-code, and metadata invariants.
7. Print deterministic developer-facing summary output.
8. Keep fixture tagger output contract unchanged.
9. Mark bundle assembly and all later behaviors as deferred.

The implementation should not yet emit ingestion bundle items. Triage output remains pre-bundle-assembly and pre-kernel-handoff.

## Explicitly Deferred

The triage slice must not implement:

- live fetching;
- scheduler execution;
- production triage for live pages;
- advanced negative scoring;
- watchlist matching;
- event-chain continuity detection;
- operator override persistence;
- bundle assembly;
- report composition;
- archive/export automation;
- ai-meta-kernel runtime handoff;
- CI;
- package migration.

## Guardrails

- Keep triage deterministic and fixture-only.
- Do not triage dropped dedup items.
- Do not treat `P1` as final importance or recommendation.
- Do not generate narrative analysis in triage.
- Do not bypass ai-meta-kernel with triage priority.
- Do not mutate `NormalizedItem` or `TagSet` content during triage.
- Keep operator override behavior outside hidden runtime logic.
- Run `validation/run_all_local_checks.py` after triage-path changes.

## Recommended Next Phase

Implement `TASK 31 - Fixture-Driven Triage Scaffold`.

That pass should introduce the smallest local helper that converts retained tagged fixture items into `TriageDecision` outputs and prints a compact deterministic summary, without production triage, bundle assembly, report composition, or live fetching.
