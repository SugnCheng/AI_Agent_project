# First Runtime Slice Plan

## Purpose

This document defines the first narrow, governed runtime slice for `macro-financial-intelligence-agent` v0.1.

It is a planning document only. It does not implement live fetching, scheduler runtime, report composition, CI, package migration, or ai-meta-kernel runtime handoff.

## Chosen Slice

The first runtime slice should be a local deterministic dry-run for the existing profile:

- `profile_id`: `daily_us_core`
- `run_mode`: `daily_brief_run`
- `report_target`: `daily_brief`
- `region`: `US`

The dry-run should exercise the smallest end-to-end path that can prove the governed contracts work together without touching the network.

## Why This Is the Safest First Step

`daily_us_core` is the safest first runtime target because:

- it is already enabled in `scheduler/run_profiles.yaml`;
- it uses only explicitly registered source IDs from `config/source_registry.yaml`;
- its current selected sources are enabled and `TIER_1`;
- it maps to an existing report target and template;
- existing example bundles already demonstrate daily US bundle shape;
- current validation scripts already cover config loading, schema validation, and cross-file semantic consistency.

This keeps the first runtime slice contract-first, deterministic, and reviewable.

## Existing Components to Use

The slice should use existing components only:

| Component | Existing file | Intended role in first slice |
| --- | --- | --- |
| Source registry loader | `acquisition/source_registry_loader.py` | Load governed whitelist source definitions. |
| Run profiles loader | `scheduler/run_profiles_loader.py` | Load and select `daily_us_core`. |
| Raw item scaffold | `acquisition/raw_item.py` | Define future raw item boundary; no live items yet. |
| Bundle builder scaffold | `bundles/bundle_builder.py` | Validate request enum alignment before build behavior exists. |
| Bundle schema validator | `bundles/bundle_schema_validator.py` | Validate any emitted dry-run bundle artifact. |
| Unified validation wrapper | `validation/run_all_local_checks.py` | Confirm the repository remains contract-valid after dry-run changes. |
| Existing examples | `bundles/examples/*.example.json` | Provide reference shapes, including no-new-items behavior. |

## In-Scope Dry-Run Steps

The next implementation pass should implement only this deterministic path:

1. Load `config/source_registry.yaml` through `SourceRegistryLoader`.
2. Load `scheduler/run_profiles.yaml` through `RunProfilesLoader`.
3. Select the enabled profile with `profile_id = daily_us_core`.
4. Resolve the profile's `include_source_ids` against the loaded registry.
5. Confirm selected sources are enabled, registered, and within profile authority tiers.
6. Construct a dry-run `BundleBuildRequest` with:
   - `run_mode = daily_brief_run`
   - `report_target = daily_brief`
   - `regions = ["US"]`
   - `items = []`
   - `item_count_raw = 0`
7. Validate request enum alignment through `IngestionBundleBuilder.validate_request_enums`.
8. Emit or compare against a no-new-items bundle shape only if the emitted artifact can pass:
   - `INGESTION_BUNDLE.schema.json`
   - semantic count/date/source invariants
9. Run `validation/run_all_local_checks.py` after any dry-run slice change.

The first implementation should prefer an explicit local script or helper under the existing flat scaffold layout. It should not require package migration.

## Expected Output of the First Slice

The first dry-run should produce developer-facing output only, such as:

- selected profile ID;
- selected source IDs;
- selected run mode;
- selected report target;
- dry-run item counts;
- validation result.

If a dry-run bundle artifact is written, it should be clearly marked as generated local output and should not replace governed example artifacts.

## Explicitly Deferred

The first runtime slice must not implement:

- live HTTP fetching;
- open-web crawling;
- source discovery or source registry mutation;
- real cron / scheduler execution;
- production normalization, dedup, tagging, or triage logic;
- full ingestion bundle assembly from live items;
- report composition;
- archive/export automation;
- ai-meta-kernel runtime handoff;
- CI;
- package layout migration.

## Guardrails for the Next Implementation Pass

- Use `daily_us_core` only unless the operator explicitly approves another profile.
- Treat `scheduler/run_profiles.yaml` and `config/source_registry.yaml` as governed inputs.
- Do not silently select disabled sources.
- Do not interpret `schedule.cron` as an executable scheduler.
- Keep output local and deterministic.
- Preserve the three existing validation layers and the unified wrapper.
- Add TODO markers where live behavior is intentionally deferred.

## Recommended Next Phase

Implement `TASK 15 - Daily US Core Dry-Run Orchestrator Scaffold`.

That pass should add a minimal local helper that performs the in-scope dry-run steps above, then runs or instructs the operator to run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\validation\run_all_local_checks.py'
```

The helper should remain local-only and must not fetch, schedule, compose reports, or call external services.
