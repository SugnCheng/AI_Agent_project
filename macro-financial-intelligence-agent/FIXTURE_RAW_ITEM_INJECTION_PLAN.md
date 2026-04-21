# Fixture-Based Raw Item Injection Plan

## Purpose

This document defines the next narrow, governed path for introducing local fixture-based raw items after the `daily_us_core` dry-run helper.

It is a planning document only. It does not implement fixture loading, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or ai-meta-kernel runtime handoff.

## Chosen Slice

The first fixture-based slice should remain scoped to:

- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`
- source set: enabled `TIER_1` sources already selected by `daily_us_core`

The first fixture path should inject local raw items only after the dry-run profile/source validation succeeds.

## Why Fixture Injection Is the Safest Next Step

Fixture injection is the safest next implementation step because it allows the project to exercise preprocessing boundaries without introducing uncontrolled acquisition behavior.

It provides:

- deterministic input data;
- repeatable local validation;
- no network dependency;
- no source universe expansion;
- clear source traceability back to `config/source_registry.yaml`;
- a narrow bridge from no-new-items dry-run output toward item-bearing bundle construction;
- a controlled way to test normalization, dedup, tagging, and triage scaffolds before live fetching exists.

## Existing Components to Use

| Component | Existing file | Role in fixture slice |
| --- | --- | --- |
| Dry-run helper | `workflows/daily_us_core_dry_run.py` | Validate profile/source selection before fixture injection. |
| Dry-run output contract | `DRY_RUN_OUTPUT_CONTRACT.md` | Preserve dry-run summary and deferred-behavior markers. |
| Source registry loader | `acquisition/source_registry_loader.py` | Validate fixture `source_id` values against governed sources. |
| Run profiles loader | `scheduler/run_profiles_loader.py` | Keep fixture scope bound to `daily_us_core`. |
| Raw item shape | `acquisition/raw_item.py` | Convert fixture records into `RawItem` objects and run `validate_minimum_fields()`. |
| Normalization scaffold | `preprocessing/normalize/normalizer.py` | Future fixture-driven normalization boundary. |
| Dedup scaffold | `preprocessing/dedup/deduper.py` | Future deterministic duplicate grouping boundary. |
| Tagging scaffold | `preprocessing/tagging/tagger.py` | Future rule-based tag assignment boundary. |
| Triage scaffold | `preprocessing/triage/triage_scaffold.py` | Future preliminary priority assignment boundary. |
| Triage rules | `preprocessing/triage/TRIAGE_RULES.md` | Govern fixture triage expectations when implemented. |
| Bundle schema validator | `bundles/bundle_schema_validator.py` | Validate any future fixture-derived bundle artifact. |
| Semantic checks | `validation/semantic_contract_checks.py` | Validate future fixture-derived bundle semantics. |

## Minimum Fixture Set

The first fixture set should be small and intentionally boring. It should contain three to four local raw item records.

Recommended minimum:

1. `fed_fomc` policy communication fixture
   - source: `fed_fomc`
   - purpose: high-authority central bank item
   - expected future triage: likely `P1`

2. `bls` economic release fixture
   - source: `bls`
   - purpose: official macro/statistics item
   - expected future triage: likely `P1`

3. `sec_press` regulatory fixture
   - source: `sec_press`
   - purpose: official regulatory action / rule / enforcement item
   - expected future triage: likely `P1` or `P2` depending content

4. Optional near-duplicate fixture
   - source: one already used above
   - purpose: exercise future dedup behavior
   - expected future behavior: one retained item plus one dropped/linked duplicate

Do not include media stubs, disabled sources, Japan/Taiwan sources, or cross-region records in the first fixture slice.

## Fixture Record Shape

Each fixture raw item should map cleanly to `RawItem` fields:

| Field | Requirement |
| --- | --- |
| `source_id` | Must exist in `config/source_registry.yaml` and be selected by `daily_us_core`. |
| `retrieved_at` | Static ISO-like timestamp for deterministic tests. |
| `source_url` | Official source URL or stable example URL under the registered source. |
| `title` | Non-empty fixture title. |
| `raw_text` | Short deterministic text, not full scraped content. |
| `content_type` | Must align with source `content_modes` where practical. |
| `region` | Must be `US` for the first slice. |
| `language` | Should be `en`. |
| `published_at` | Optional but recommended for future normalization. |
| `canonical_url` | Optional but recommended; may equal `source_url`. |
| `metadata` | Optional fixture notes only; no hidden analysis. |

## In-Scope Next Steps

The next implementation pass should do only the following:

1. Add a small local fixture file for `daily_us_core`.
2. Add a local fixture loader or helper that reads the fixture file.
3. Convert fixture records into `RawItem` objects.
4. Run `RawItem.validate_minimum_fields()` on every fixture.
5. Validate every fixture `source_id` against `daily_us_core` selected sources.
6. Validate fixture `region` against the selected profile region.
7. Print deterministic developer-facing summary output.
8. Preserve the current dry-run output contract and make fixture mode visibly separate from no-new-items dry-run mode.

The first fixture pass should stop at raw item validation. It should not pretend that normalization, dedup, tagging, or triage are complete.

## Later Fixture-Driven Steps

After raw fixture injection is stable, later passes can incrementally exercise:

1. deterministic normalization from `RawItem` to `NormalizedItem`;
2. simple fixture-only dedup grouping;
3. rule-based tag assignment using controlled vocabularies;
4. preliminary triage using `TRIAGE_RULES.md`;
5. fixture-derived ingestion bundle artifact validation.

Each step should add validation before expanding behavior.

## Explicitly Deferred

The fixture slice must not implement:

- live fetching;
- open-web crawling;
- source registry mutation;
- scheduler execution;
- report composition;
- archive/export automation;
- ai-meta-kernel runtime handoff;
- production normalization;
- production deduplication;
- production tagging;
- production triage;
- CI;
- package migration.

## Guardrails

- Keep fixture data local and small.
- Do not add fixture records from disabled sources.
- Do not use fixtures to expand source governance.
- Do not encode market analysis in fixture metadata.
- Do not treat fixture triage expectations as final analysis.
- Keep all fixture-generated artifacts clearly marked as local fixture output.
- Run `validation/run_all_local_checks.py` after fixture-path changes.

## Recommended Next Phase

Implement `TASK 19 - Daily US Core Raw Fixture Loader Scaffold`.

That pass should add the minimum fixture file and a local helper that validates fixture records as `RawItem` objects, without invoking live fetching or production preprocessing logic.
