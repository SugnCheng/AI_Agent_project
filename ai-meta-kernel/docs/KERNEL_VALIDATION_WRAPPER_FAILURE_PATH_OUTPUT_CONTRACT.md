# Kernel Validation Wrapper Failure-Path Output Contract

## Purpose

This document snapshots the current developer-facing output contract for:

```text
ai-meta-kernel/validation/kernel_validation_wrapper_failure_path_checks.py
```

It fixes the helper's current execution scope, success signal, expected failure behavior, strategy assumptions, drift rules, and explicitly absent runtime behaviors.

This document does not add runtime behavior, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Actual Helper Path And Scope

Actual helper path:

```text
ai-meta-kernel/validation/kernel_validation_wrapper_failure_path_checks.py
```

Actual scope:

- local-only wrapper failure-path validation;
- developer-facing validation helper;
- imports `validation/run_all_kernel_local_checks.py` as a module;
- temporarily replaces the wrapper module's `CHECKS` list with controlled test entries;
- verifies wrapper process-control behavior without changing real validation helpers;
- uses only Python standard library.

The helper validates wrapper behavior only. It does not validate the full kernel runtime, macro-agent runtime, or downstream handoff execution.

## Current Success Signal

If all failure-path checks pass, the helper prints exactly:

```text
kernel-validation-wrapper-failure-path-checks-ok
```

This signal means only that the wrapper failure-path scenarios passed locally.

It does not mean:

- the wrapper's normal success path was run;
- kernel runtime invocation exists;
- P0-P10 execution exists;
- canonical task object generation exists;
- runtime artifact reads or writes exist;
- live fetching, scheduler runtime, report composition, CI, package migration, or external service calls exist.

## Current Failure Behavior

The helper raises `AssertionError` if the wrapper behavior no longer matches the expected failure-path contract.

Expected checked behavior:

| Scenario | Expected wrapper behavior |
| --- | --- |
| Temporary child helper exits non-zero | Wrapper returns the child exit code `7`. |
| Temporary child helper exits non-zero | Wrapper emits `kernel-local-validation-checks-failed: intentional failing helper exited with 7` to stderr. |
| Temporary child helper exits non-zero | Wrapper does not print `kernel-local-validation-checks-ok`. |
| Earlier helper fails before later helper | Later helper is not run. |
| Configured helper path is missing | Wrapper returns `1`. |
| Configured helper path is missing | Wrapper emits `kernel-local-validation-checks-failed: missing helper:` to stderr. |
| Configured helper path is missing | Wrapper does not print `kernel-local-validation-checks-ok`. |

The helper itself does not define a separate failure signal. Python assertion output is the current failure surface.

## Strategy Assumptions

The helper currently depends on these assumptions:

- the wrapper module exposes `CHECKS` and `main()`;
- replacing `CHECKS` during the check is acceptable and restored before exit;
- temporary helper scripts are created under `ai-meta-kernel/validation/` and deleted after use;
- temporary helper scripts are not committed fixtures;
- real validation helper files are not renamed, edited, deleted, or made to fail;
- wrapper stdout and stderr are captured at the Python level for assertions;
- the final wrapper success signal remains `kernel-local-validation-checks-ok`;
- the failure-path helper success signal remains `kernel-validation-wrapper-failure-path-checks-ok`.

## Blocked Runtime Behaviors

The failure-path helper must not silently introduce:

- runtime adapter invocation;
- P0-P10 runtime invocation;
- canonical task object generation from envelopes;
- kernel intake preparation;
- response artifact writing;
- failure artifact writing;
- runtime artifact reads or writes;
- runtime artifact polling;
- retry/backoff behavior;
- artifact cleanup automation beyond deleting its own temporary helper directory;
- live fetching;
- scheduler runtime;
- report composition;
- CI behavior;
- package migration;
- external service calls;
- mutation of real validation helper files;
- committed failing fixture scripts;
- wrapper auto-repair or contract repair.

## Changes Requiring A Governed Pass

The following changes require a governed pass before implementation:

- changing the helper path;
- changing the helper success signal;
- changing wrapper failure signals asserted by the helper;
- changing wrapper exit-code semantics asserted by the helper;
- changing wrapper stop-on-first-failure behavior;
- replacing temporary helper scripts with committed failing fixtures;
- mutating, renaming, or deleting real validation helper files to simulate failure;
- changing the monkeypatched `CHECKS` strategy;
- broadening the helper beyond wrapper failure-path behavior;
- adding non-standard-library dependencies;
- connecting this helper to CI;
- adding runtime artifact validation;
- adding runtime adapter behavior or actual handoff execution.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\kernel_validation_wrapper_failure_path_checks.py'
```

Expected successful output:

```text
kernel-validation-wrapper-failure-path-checks-ok
```

## Recommended Next Phase

Implement a `Kernel-Side Validation Baseline Refresh Pass`.

That pass should update the kernel validation baseline to reference the wrapper failure-path helper and this output contract while keeping runtime handoff, CI, scheduler behavior, live fetching, and report composition out of scope.
