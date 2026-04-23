# Validation Baseline Snapshot

## Purpose

This document snapshots the current unified local validation baseline for `macro-financial-intelligence-agent` v0.1.

It is a developer-facing baseline note only. It does not implement runtime behavior, live fetching, scheduler execution, report composition, CI, package migration, external service calls, archive/export automation, or ai-meta-kernel runtime handoff.

## Current Unified Wrapper

The current unified local validation entrypoint is:

```text
validation/run_all_local_checks.py
```

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\validation\run_all_local_checks.py'
```

Expected final output:

```text
all-local-validation-checks-ok
```

## Included Validation Layers

The wrapper currently runs these layers in order:

| Order | Script | Responsibility |
| --- | --- | --- |
| 1 | `validation/scaffold_contract_checks.py` | Validates minimum scaffold contracts, including `RawItem` required fields, bundle build enum guards, and governed example bundle alignment. |
| 2 | `validation/dependency_backed_contract_checks.py` | Validates approved dependency-backed behavior: PyYAML config loading and jsonschema validation of governed ingestion bundle examples. |
| 3 | `validation/semantic_contract_checks.py` | Validates currently in-scope cross-file semantic rules across source registry, run profiles, bundle schema, and example bundles. |
| 4 | `validation/kernel_exchange_fixture_regression_checks.py` | Validates file-based kernel exchange fixture branches for standard, restricted, blocked, and failure artifact cases using the read-response scaffold. |

## Wrapper Non-Goals

The unified wrapper must not silently introduce:

- live fetching;
- open-web crawling;
- scheduler runtime;
- report composition;
- archive/export automation;
- ai-meta-kernel runtime invocation;
- kernel response generation;
- kernel failure artifact generation;
- canonical kernel task object generation inside the macro agent;
- artifact polling or watcher behavior;
- retry/backoff runtime behavior;
- runtime artifact mutation or deletion;
- external service calls;
- CI behavior;
- package layout migration;
- generic multi-profile production orchestration.

## Current Baseline Guarantees

When the wrapper passes, it confirms only that:

1. governed local scaffold contracts are still coherent;
2. approved dependency-backed config/schema checks still pass;
3. currently in-scope semantic config and bundle relationships remain valid;
4. file-based kernel exchange fixture regression still classifies:
   - standard response as `standard`;
   - restricted response as `restricted`;
   - blocked response as `blocked`;
   - failure artifact as `blocked`.

Passing the wrapper does not mean:

- live acquisition works;
- schedules execute;
- production preprocessing is complete;
- reports can be composed;
- ai-meta-kernel runtime handoff exists;
- downstream reporting is unlocked.

## Changes Requiring A Governed Validation Pass

The following changes require a new governed validation pass before being added to the wrapper:

- adding any check that performs network access;
- adding any check that executes scheduler behavior;
- adding any check that composes reports;
- adding any check that invokes ai-meta-kernel runtime;
- adding any check that writes, deletes, or mutates runtime exchange artifacts beyond explicit local fixture setup;
- adding a new dependency required by validation;
- changing expected `standard` / `restricted` / `blocked` semantics;
- changing file-based exchange artifact naming or directory rules;
- broadening validation from `daily_us_core` to additional profiles;
- turning this wrapper into CI or production gating.

## Relationship To Runtime Readiness

This baseline complements `KERNEL_RUNTIME_INTEGRATION_READINESS.md`, but it does not replace it.

The validation wrapper proves local fixture and contract coherence. It does not prove that the macro agent is ready for actual ai-meta-kernel runtime invocation.

## Recommended Next Phase

If the next milestone is still validation-focused, add a small output contract snapshot for `run_all_local_checks.py`.

If the next milestone moves toward runtime integration, first update the runtime readiness note so it reflects the completed file-based exchange scaffold, response reader, failure fixture, and regression validation baseline.
