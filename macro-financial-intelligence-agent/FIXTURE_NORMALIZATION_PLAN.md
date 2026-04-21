# Fixture-Driven Normalization Plan

## Purpose

This document defines the next narrow, governed path for moving from validated fixture-based `RawItem` objects into deterministic `NormalizedItem` objects.

It is a planning document only. It does not implement normalization runtime, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, production deduplication, tagging, triage, bundle assembly, or ai-meta-kernel runtime handoff.

## Chosen Slice

The first normalization slice should remain scoped to:

- input source: validated fixture `RawItem` objects from `workflows/daily_us_core_fixture_loader.py`
- fixture file: `fixtures/daily_us_core_raw_items.fixture.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`
- output shape: `NormalizedItem` from `preprocessing/normalize/normalizer.py`

The slice should normalize only fixture items that have already passed minimum field, selected source, and region validation.

## Why This Is the Safest Next Step

Fixture-driven normalization is the safest next step because it exercises the first preprocessing boundary without introducing live acquisition or analytical behavior.

It provides:

- deterministic input from local fixture data;
- repeatable output for review;
- a direct bridge from `RawItem` to `NormalizedItem`;
- early validation of item identity, URL fallback, timestamp handling, and excerpt policy;
- no deduplication, tagging, triage, reporting, or kernel reasoning;
- a controlled point to catch field naming drift before bundle assembly exists.

## Existing Components to Use

| Component | Existing file | Role in normalization slice |
| --- | --- | --- |
| Fixture loader | `workflows/daily_us_core_fixture_loader.py` | Provide validated fixture `RawItem` objects. |
| Fixture loader output contract | `FIXTURE_LOADER_OUTPUT_CONTRACT.md` | Preserve fixture loader output boundary. |
| Raw item shape | `acquisition/raw_item.py` | Input object contract. |
| Normalized item shape | `preprocessing/normalize/normalizer.py` | Output object contract. |
| Source registry loader | `acquisition/source_registry_loader.py` | Available for later source metadata enrichment, but not required for first field mapping. |
| Unified validation wrapper | `validation/run_all_local_checks.py` | Must remain passing after any normalization scaffold change. |

## RawItem to NormalizedItem Mapping

The first deterministic mapping should be simple and explicit:

| `NormalizedItem` field | Source / rule |
| --- | --- |
| `item_id` | Deterministic local ID derived from `source_id`, `published_at` or `retrieved_at`, and normalized title. |
| `source_id` | Copy from `RawItem.source_id`. |
| `region` | Copy from `RawItem.region`. |
| `retrieved_at` | Copy from `RawItem.retrieved_at`. |
| `published_at` | Use `RawItem.published_at` when present; otherwise fallback to `RawItem.retrieved_at`. |
| `title` | Trim surrounding whitespace from `RawItem.title`; do not rewrite wording. |
| `source_url` | Copy from `RawItem.source_url`. |
| `canonical_url` | Use `RawItem.canonical_url` when present; otherwise fallback to `RawItem.source_url`. |
| `content_type` | Copy from `RawItem.content_type`. |
| `language` | Copy from `RawItem.language`. |
| `raw_excerpt` | Deterministic excerpt from `RawItem.raw_text`; no summarization or analysis. |
| `metadata` | Copy fixture metadata and add normalization markers only if needed. |

## Deterministic Rules for the First Slice

The first normalization implementation should apply only these rules:

1. Trim leading/trailing whitespace from `title`.
2. Trim leading/trailing whitespace from `raw_text` before excerpting.
3. Use `canonical_url = source_url` when `RawItem.canonical_url` is missing.
4. Use `published_at = retrieved_at` when `RawItem.published_at` is missing.
5. Generate `item_id` deterministically from stable input fields.
6. Generate `raw_excerpt` by truncating raw text to a fixed maximum length.
7. Preserve source text meaning; do not summarize, classify, or infer market significance.
8. Preserve fixture metadata without treating it as evidence or analysis.

The exact `item_id` and `raw_excerpt` rules should be documented in the implementation pass before being treated as stable.

## In-Scope Next Steps

The next implementation pass should do only the following:

1. Add a fixture-only normalization helper or extend the existing normalizer scaffold with deterministic fixture-safe behavior.
2. Reuse validated `RawItem` objects from the fixture loader.
3. Convert each fixture `RawItem` into a `NormalizedItem`.
4. Validate that every `NormalizedItem` required field is populated.
5. Print deterministic developer-facing summary output.
6. Keep fixture loader output contract unchanged.
7. Mark all later preprocessing behaviors as deferred.

The implementation should not yet emit ingestion bundle items. `NormalizedItem` is still pre-dedup, pre-tagging, and pre-triage.

## Explicitly Deferred

The normalization slice must not implement:

- live fetching;
- scheduler execution;
- production normalization for live pages;
- deduplication;
- tagging;
- triage;
- bundle assembly;
- report composition;
- archive/export automation;
- ai-meta-kernel runtime handoff;
- CI;
- package migration.

## Guardrails

- Keep normalization deterministic and fixture-only.
- Do not rewrite titles for readability.
- Do not summarize raw text into analysis.
- Do not infer topic, market, or risk tags.
- Do not assign preliminary priority.
- Do not drop items during normalization unless required fields are missing.
- Keep any generated IDs stable for identical fixture input.
- Run `validation/run_all_local_checks.py` after normalization-path changes.

## Recommended Next Phase

Implement `TASK 22 - Fixture-Driven Normalization Scaffold`.

That pass should introduce the smallest local helper that converts validated fixture `RawItem` objects into `NormalizedItem` objects and prints a compact deterministic summary, without deduplication, tagging, triage, bundle assembly, or live fetching.
