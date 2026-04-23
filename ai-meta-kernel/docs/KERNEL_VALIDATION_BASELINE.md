# Kernel Validation Baseline

## Purpose

This document refreshes the current kernel-side validation baseline for `ai-meta-kernel`.

It records the current standalone validation helpers, the implemented local validation wrapper, the wrapper failure-path helper, the first-slice adapter fixture validation surface, the writer-boundary planning and output contract surfaces, what success-path and failure-path validation mean, what they do not mean, and which runtime behaviors remain explicitly blocked.

This is a baseline note only. It does not add runtime code, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Documentation Index

For the current validation documentation map, see:

```text
docs/KERNEL_VALIDATION_DOCUMENTATION_INDEX.md
```

## Current Standalone Validation Helpers

The current kernel-side standalone helpers are:

| Helper | Responsibility | Success signal | Output contract |
| --- | --- | --- | --- |
| `validation/static_meta_layer_contract_checks.py` | Checks static core Meta-Layer contract artifacts, including master spec, runtime pipeline, handoff contract, and task object schema. | `kernel-static-meta-layer-contract-checks-ok` | `docs/KERNEL_STATIC_META_LAYER_CONTRACT_CHECK_OUTPUT_CONTRACT.md` |
| `validation/kernel_file_exchange_fixture_checks.py` | Checks the governed static `daily_us_core` file-exchange envelope, response, and failure fixtures. | `kernel-file-exchange-fixture-checks-ok` | `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_OUTPUT_CONTRACT.md` |
| `validation/kernel_file_exchange_adapter_scaffold_checks.py` | Checks the current file-exchange adapter scaffold boundary and confirms blocked placeholder functions remain fail-closed. | `kernel-file-exchange-adapter-scaffold-checks-ok` | `docs/KERNEL_FILE_EXCHANGE_ADAPTER_SCAFFOLD_CHECK_OUTPUT_CONTRACT.md` |

These helpers remain canonical standalone checks.

They may be run individually for focused debugging even though a wrapper now exists.

## Current First-Slice Adapter Fixture Validation Surface

The current first implementation slice validation surface is:

```text
validate_existing_daily_us_core_static_adapter_fixtures_and_fail_closed_scaffold_boundaries
```

It is governed by:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_VALIDATION_OUTPUT_CONTRACT.md
docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_HELPER_COVERAGE.md
```

The first-slice surface covers only:

- the existing `daily_us_core` static kernel input envelope fixture;
- the existing `daily_us_core` expected kernel response fixture;
- the existing `daily_us_core` expected blocking kernel failure fixture;
- the current fail-closed adapter scaffold boundaries.

Helper-free coverage decision:

```text
existing_helpers_fully_cover_first_slice_adapter_fixture_validation_contract
```

No new validation helper is currently needed for this slice.

Current coverage is provided by:

| Helper | First-slice coverage |
| --- | --- |
| `validation/kernel_file_exchange_fixture_checks.py` | Validates fixture existence, JSON object shape, governed `daily_us_core` values, response schema validity, blocking failure shape, and forbidden canonical task object leakage in envelope/failure fixtures. |
| `validation/kernel_file_exchange_adapter_scaffold_checks.py` | Exercises the scaffold against the static fixtures and confirms `prepare_kernel_intake`, `invoke_kernel_runtime`, `write_response_artifact`, and `write_failure_artifact` remain fail-closed. |

This surface is local-only and deterministic. It does not scan runtime artifact directories, discover live work, mutate fixtures, generate artifacts, or call runtime code.

## Current Writer-Boundary Planning And Output Contract Surface

The current writer-boundary planning decision is:

```text
plan_response_and_blocking_failure_writers_before_implementation
```

It is documented in:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_PLAN.md
```

The current writer-boundary output contract is:

```text
future_writers_must_validate_before_write_and_emit_exactly_one_terminal_artifact
```

It is documented in:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md
```

At the current stage, these documents mean:

- future response writer and blocking failure writer boundaries are planned before implementation;
- future response artifacts must be schema-validated before write;
- future blocking failure artifacts must remain `blocking == true`;
- one envelope invocation should produce exactly one terminal artifact: response or blocking failure;
- failure stages, artifact naming expectations, and pre-write validation order are governed before implementation.

At the current stage, these documents do not mean:

- response writing exists;
- failure writing exists;
- runtime handoff exists;
- P0-P10 runtime invocation exists;
- canonical task object generation from envelopes exists;
- writer code is authorized in the current baseline.

## Current Local Validation Wrapper

Implemented wrapper:

```text
validation/run_all_kernel_local_checks.py
```

Wrapper role:

- local-only validation orchestration;
- developer-facing command entrypoint;
- sequential execution of the three governed standalone helpers;
- child stdout and stderr preservation;
- stop-on-first-failure behavior.

The wrapper's implemented behavior is governed by:

```text
docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md
```

## Current Wrapper Failure-Path Helper

Implemented failure-path helper:

```text
validation/kernel_validation_wrapper_failure_path_checks.py
```

Failure-path helper role:

- local-only validation of wrapper failure-path behavior;
- developer-facing helper for wrapper process-control checks;
- imports `validation/run_all_kernel_local_checks.py` as a module;
- temporarily replaces the wrapper module's `CHECKS` list with controlled test entries;
- uses temporary helper scripts and a temporary marker file to verify stop-on-first-failure behavior;
- checks a deliberately missing helper path;
- verifies final wrapper success signal suppression on failure;
- does not mutate real validation helper files.

The failure-path helper's implemented behavior is governed by:

```text
docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_OUTPUT_CONTRACT.md
```

## Wrapper Execution Order

The wrapper runs exactly this order:

1. `validation/static_meta_layer_contract_checks.py`
2. `validation/kernel_file_exchange_fixture_checks.py`
3. `validation/kernel_file_exchange_adapter_scaffold_checks.py`

Reasoning:

- core Meta-Layer static contracts should pass before file-exchange fixtures are trusted;
- file-exchange fixtures should pass before adapter scaffold boundary checks rely on them;
- adapter scaffold fail-closed behavior should remain the final local check until runtime handoff is intentionally implemented.

## Local Command

Run the success-path wrapper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\run_all_kernel_local_checks.py'
```

Expected final success signal:

```text
kernel-local-validation-checks-ok
```

Run the wrapper failure-path helper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\kernel_validation_wrapper_failure_path_checks.py'
```

Expected final success signal:

```text
kernel-validation-wrapper-failure-path-checks-ok
```

## What Success-Path Validation Means

A successful local wrapper run means:

- the core static Meta-Layer contract helper passed;
- the governed static file-exchange fixtures passed;
- the adapter scaffold boundary helper passed;
- the first-slice adapter fixture validation surface is covered by the existing fixture and scaffold helpers;
- the helper-free first-slice coverage decision remains valid for the current `daily_us_core` static fixture set;
- the writer-boundary plan and output contract are documented as future governed surfaces, not implemented behavior;
- all three helpers passed in the governed order;
- the wrapper reached the final success signal.

It is the current success-path local validation baseline signal only.

It does not exercise wrapper child-failure or missing-helper paths. Those paths are covered separately by the wrapper failure-path helper.

## What Failure-Path Validation Means

A successful wrapper failure-path helper run means:

- a temporary child helper exiting non-zero causes the wrapper to return that child exit code;
- the wrapper emits the expected failure message for a child non-zero exit;
- the wrapper stops before running a later helper after an earlier failure;
- the wrapper does not print `kernel-local-validation-checks-ok` after a child failure;
- a missing configured helper path causes the wrapper to return `1`;
- the wrapper emits the expected missing-helper failure message;
- the wrapper does not print `kernel-local-validation-checks-ok` after a missing helper;
- real validation helpers were not renamed, modified, deleted, or made to fail.

It is a local wrapper process-control validation signal only.

## What Local Validation Does Not Mean

A successful success-path wrapper run or failure-path helper run does not mean:

- kernel runtime exists;
- P0-P10 runtime execution exists;
- canonical task object generation exists;
- file-exchange runtime intake exists;
- runtime artifact reads or writes exist;
- response artifact writing exists;
- failure artifact writing exists;
- downstream macro reporting is unlocked;
- live fetching or scheduler runtime works;
- CI has run;
- production validation is complete;
- first-slice fixture validation has opened runtime handoff;
- writer-boundary planning has opened response or failure artifact writing.

## Explicitly Blocked Runtime Behaviors

The current validation baseline must not silently introduce:

- runtime adapter invocation;
- P0-P10 runtime invocation;
- canonical task object generation from envelopes;
- kernel intake preparation;
- response artifact writing;
- failure artifact writing;
- runtime artifact reads or writes;
- runtime artifact polling;
- retry/backoff behavior;
- artifact cleanup automation;
- live fetching;
- scheduler runtime;
- report composition;
- CI behavior;
- package migration;
- external service calls;
- generic multi-profile production validation;
- contract auto-repair.

The first-slice adapter fixture validation surface also must not silently introduce:

- additional fixture classes beyond envelope, expected response, and blocking failure;
- additional profiles beyond `daily_us_core`;
- generated runtime artifacts as committed fixtures;
- runtime reader discovery;
- response or failure writer behavior;
- CLI command behavior;
- macro-side production of kernel response artifacts.

The writer-boundary planning and output contract surfaces also must not silently introduce:

- response writer implementation;
- failure writer implementation;
- response artifact emission;
- failure artifact emission;
- writing both response and failure artifacts for one invocation;
- writing failure artifacts with `blocking == false`;
- writing response artifacts before schema and state validation;
- partial canonical task object content in failure artifacts;
- writer-side repair of invalid kernel outputs.

## Changes Requiring A Governed Pass

The following changes require a governed pass before implementation:

- adding or removing standalone validation helpers;
- changing helper success signals;
- changing helper output contracts;
- changing wrapper execution order;
- changing wrapper final success signal;
- changing stop-on-first-failure behavior;
- suppressing, capturing, or transforming child stdout or stderr;
- adding wrapper-level dependencies;
- removing standalone helper support;
- changing the wrapper failure-path helper path;
- changing the wrapper failure-path helper success signal;
- changing the wrapper failure-path helper's monkeypatched `CHECKS` strategy;
- replacing temporary helper scripts with committed failing fixtures;
- mutating real validation helpers to simulate wrapper failure behavior;
- connecting validation to CI;
- broadening validation beyond the current standalone helper, wrapper, and wrapper failure-path helper baseline;
- changing fixture scope beyond the current governed static fixtures;
- changing the first-slice adapter fixture validation contract;
- changing the helper-free first-slice coverage decision;
- adding a new first-slice validation helper when existing helpers still cover the contract;
- changing the existing `daily_us_core` fixture set used by first-slice validation;
- changing the writer-boundary planning decision;
- changing the writer-boundary output contract decision;
- changing response or failure artifact naming semantics;
- changing writer mutual exclusivity rules;
- changing writer pre-write validation order;
- adding response or failure writer implementation;
- adding runtime artifact validation;
- adding runtime adapter behavior;
- adding file mutation, cleanup, or auto-repair behavior.

## Current Baseline Status

The current baseline is:

```text
standalone_helpers_plus_local_wrapper_plus_wrapper_failure_path_helper_plus_first_slice_adapter_fixture_coverage_plus_writer_boundary_contracts
```

The kernel now has a usable local success-path validation entrypoint, a focused wrapper failure-path helper, an explicit helper-free first-slice adapter fixture validation coverage decision, and governed writer-boundary planning/output contracts while preserving individually reviewable helper contracts.

## Recommended Next Phase

Implement a `Kernel-Side Validation Documentation Index Writer-Boundary Refresh Pass`.

That pass should refresh the kernel validation documentation index so the writer-boundary plan and writer-boundary output contract are easy to find while keeping runtime behavior, CI, package migration, and actual kernel runtime handoff out of scope.
