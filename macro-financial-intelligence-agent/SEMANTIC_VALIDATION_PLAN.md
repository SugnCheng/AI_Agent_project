# Semantic Validation Plan

## Purpose

This document defines the next cross-file semantic validation rules for macro-financial-intelligence-agent v0.1.

It is a planning document only. It does not implement semantic validation runtime, live fetching, scheduler execution, report composition, CI, package migration, or kernel contract changes.

## Scope

Semantic validation sits above file parsing and JSON Schema validation.

It should check whether separately valid files agree with each other across:

- `config/source_registry.yaml`
- `scheduler/run_profiles.yaml`
- `bundles/schemas/INGESTION_BUNDLE.schema.json`
- `bundles/examples/*.example.json`
- `acquisition/source_registry_loader.py`
- `scheduler/run_profiles_loader.py`
- `bundles/bundle_schema_validator.py`

## Proposed Validation Layers

| Layer | Responsibility | Current status |
| --- | --- | --- |
| Loader shape checks | Parse YAML and confirm minimum top-level shape. | Implemented minimally in loaders. |
| JSON Schema checks | Validate ingestion bundle object shape. | Implemented via `bundle_schema_validator.py`. |
| Semantic validation | Validate cross-file consistency and governed behavior. | Planned here, not implemented yet. |

## Top-Priority v0.1 Rules

### SV-01: Run Profile Source References Must Exist

Why it matters:

Run profiles must not reference unknown sources. Unknown sources would bypass the whitelist registry and weaken acquisition governance.

Files spanned:

- `scheduler/run_profiles.yaml`
- `config/source_registry.yaml`
- `scheduler/run_profiles_loader.py`
- `acquisition/source_registry_loader.py`

Recommended implementation layer:

Separate semantic validation layer.

Rationale:

This rule needs data from both structured loaders. It should not be hidden inside either loader.

v0.1 scope:

In scope now.

Expected failure example:

- `include_source_ids` contains `unknown_source_id`.

### SV-02: Active Profiles Must Not Select Disabled Sources Without Explicit Justification

Why it matters:

The registry can contain disabled sources for future scope or manual approval. Active governed profiles should not select disabled sources unless a documented override exists.

Files spanned:

- `config/source_registry.yaml`
- `scheduler/run_profiles.yaml`

Recommended implementation layer:

Separate semantic validation layer.

Rationale:

This is a policy rule combining registry state and profile state.

v0.1 scope:

In scope now for active profiles only.

Deferred detail:

Define the exact override mechanism later. For now, no silent override.

### SV-03: Run Mode Values Must Align Across Profiles and Bundle Schema

Why it matters:

Run modes route downstream behavior and report expectations. Drift between `run_profiles.yaml` and `INGESTION_BUNDLE.schema.json` would make bundle validation unreliable.

Files spanned:

- `scheduler/run_profiles.yaml`
- `bundles/schemas/INGESTION_BUNDLE.schema.json`
- `bundles/examples/*.example.json`

Recommended implementation layer:

Separate semantic validation layer, with support from `bundle_schema_validator.py`.

v0.1 scope:

In scope now.

Expected check:

- Every `profiles[].run_mode` appears in schema enum.
- Every example `bundle_metadata.run_mode` appears in both schema enum and run profile run modes.

### SV-04: Report Target Values Must Map to Templates

Why it matters:

Reports are template-governed. A valid bundle should point to a report target with an existing operational template.

Files spanned:

- `scheduler/run_profiles.yaml`
- `bundles/schemas/INGESTION_BUNDLE.schema.json`
- `bundles/examples/*.example.json`
- `reporting/templates/`

Recommended implementation layer:

Separate semantic validation layer.

v0.1 scope:

In scope now.

Expected mapping:

| report_target | template |
| --- | --- |
| `daily_brief` | `reporting/templates/DAILY_BRIEF_TEMPLATE.md` |
| `weekly_intelligence_report` | `reporting/templates/WEEKLY_INTELLIGENCE_REPORT_TEMPLATE.md` |
| `special_event_memo` | `reporting/templates/SPECIAL_EVENT_MEMO_TEMPLATE.md` |

### SV-05: Bundle Date and Count Invariants

Why it matters:

JSON Schema can validate field shape, but not all semantic relationships.

Files spanned:

- `bundles/examples/*.example.json`
- future generated bundle outputs

Recommended implementation layer:

Bundle semantic validator helper, separate from JSON Schema shape validation.

v0.1 scope:

In scope now for examples.

Expected checks:

- `date_range.end` must not be earlier than `date_range.start`.
- `item_count_after_dedup` must equal `len(items)`.
- `item_count_after_dedup` must not exceed `item_count_raw`.
- `source_count` must not exceed the number of distinct item `source_id` values when `items` is non-empty.
- empty bundles must have `item_count_raw = 0`, `item_count_after_dedup = 0`, and `items = []`.

### SV-06: Bundle Item Source IDs Must Exist in Registry

Why it matters:

Example and future generated bundles should not contain items from unapproved or unknown sources.

Files spanned:

- `bundles/examples/*.example.json`
- `config/source_registry.yaml`

Recommended implementation layer:

Separate semantic validation layer.

v0.1 scope:

In scope now.

Expected check:

- Every bundle item `source_id` exists in `source_registry.yaml`.

### SV-07: Bundle Item Authority Tier Must Match Registry Source Tier

Why it matters:

An item should not locally upgrade or downgrade source authority without explicit governance. Mismatched tiers weaken source-quality reporting.

Files spanned:

- `bundles/examples/*.example.json`
- `config/source_registry.yaml`

Recommended implementation layer:

Separate semantic validation layer.

v0.1 scope:

In scope now.

Expected check:

- Item `authority_tier` equals the registered `authority_tier` for its `source_id`.

### SV-08: Region Scope Consistency

Why it matters:

Run profiles and bundles should preserve jurisdiction scope. Incorrect region mapping can distort macro/policy framing.

Files spanned:

- `config/source_registry.yaml`
- `scheduler/run_profiles.yaml`
- `bundles/examples/*.example.json`

Recommended implementation layer:

Separate semantic validation layer.

v0.1 scope:

Partially in scope now.

Expected checks now:

- Profile regions must exist in registry `regions`.
- Bundle metadata regions must exist in registry `regions` or be an explicitly approved cross-region label.
- Item region should match registered source region.

Deferred detail:

- Define approved cross-region labels such as `GLOBAL` or `CROSS_REGION`.
- Define when a source from one region may be included in a cross-region report.

## Deferred Semantic Rules

### DSV-01: Fetch Method Runtime Capability

Reason for deferral:

There is no fetcher runtime yet. Checking whether a fetch method is implemented would be premature.

Future rule:

- Enabled sources selected by active profiles must use fetch methods supported by the runtime.

### DSV-02: Cron Syntax and Schedule Execution Semantics

Reason for deferral:

No scheduler runtime exists.

Future rule:

- Cron expressions must parse and match expected timezone semantics.

### DSV-03: Topic / Market / Risk Tag Vocabulary Enforcement

Reason for deferral:

Controlled vocabularies for tags have not been formally defined.

Future rule:

- `topic_tags`, `market_tags`, and `risk_tags` must come from governed vocabularies.

### DSV-04: Triage Scoring Correctness

Reason for deferral:

Triage scoring is still scaffold-only.

Future rule:

- `preliminary_priority` should be reproducible from `TRIAGE_RULES.md` and source/item metadata.

### DSV-05: Handoff Compatibility With ai-meta-kernel Task Objects

Reason for deferral:

Current examples stop at ingestion bundle shape. Kernel handoff execution is not implemented.

Future rule:

- Bundle-to-kernel handoff objects must preserve source traceability, risk categories, required checks, and status flags.

## Recommended Implementation Sequence

1. Add a separate semantic validation helper, for example `validation/semantic_contract_checks.py`.
2. Use existing PyYAML loaders and `bundle_schema_validator.py` as inputs.
3. Implement SV-01 through SV-07 first.
4. Implement the limited portion of SV-08 that uses existing region codes.
5. Keep all deferred rules documented but not enforced until their upstream contracts exist.

## Non-Goals

This plan does not authorize:

- live fetching,
- scheduler runtime,
- report composition,
- source expansion,
- package migration,
- CI setup,
- kernel contract changes.
