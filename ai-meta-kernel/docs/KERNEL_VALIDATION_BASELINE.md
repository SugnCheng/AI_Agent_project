# Kernel Validation Baseline

## Purpose

This document refreshes the current kernel-side validation baseline for `ai-meta-kernel`.

It records the current standalone validation helpers, the implemented local validation wrapper, the wrapper failure-path helper, what success-path and failure-path validation mean, what they do not mean, and which runtime behaviors remain explicitly blocked.

This is a baseline note only. It does not add runtime code, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Current Standalone Validation Helpers

The current kernel-side standalone helpers are:

| Helper | Responsibility | Success signal | Output contract |
| --- | --- | --- | --- |
| `validation/static_meta_layer_contract_checks.py` | Checks static core Meta-Layer contract artifacts, including master spec, runtime pipeline, handoff contract, and task object schema. | `kernel-static-meta-layer-contract-checks-ok` | `docs/KERNEL_STATIC_META_LAYER_CONTRACT_CHECK_OUTPUT_CONTRACT.md` |
| `validation/kernel_file_exchange_fixture_checks.py` | Checks the governed static `daily_us_core` file-exchange envelope, response, and failure fixtures. | `kernel-file-exchange-fixture-checks-ok` | `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_OUTPUT_CONTRACT.md` |
| `validation/kernel_file_exchange_adapter_scaffold_checks.py` | Checks the current file-exchange adapter scaffold boundary and confirms blocked placeholder functions remain fail-closed. | `kernel-file-exchange-adapter-scaffold-checks-ok` | `docs/KERNEL_FILE_EXCHANGE_ADAPTER_SCAFFOLD_CHECK_OUTPUT_CONTRACT.md` |

These helpers remain canonical standalone checks.

They may be run individually for focused debugging even though a wrapper now exists.

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
- production validation is complete.

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
- adding runtime artifact validation;
- adding runtime adapter behavior;
- adding file mutation, cleanup, or auto-repair behavior.

## Current Baseline Status

The current baseline is:

```text
standalone_helpers_plus_local_wrapper_plus_wrapper_failure_path_helper
```

The kernel now has a usable local success-path validation entrypoint plus a focused wrapper failure-path helper while preserving individually reviewable helper contracts.

## Recommended Next Phase

Implement a `Kernel-Side Validation Documentation Index Pass`.

That pass should make the kernel validation docs easier to navigate by linking the standalone helper contracts, wrapper contract, failure-path contract, and baseline note while keeping runtime behavior, CI, package migration, and actual kernel runtime handoff out of scope.
