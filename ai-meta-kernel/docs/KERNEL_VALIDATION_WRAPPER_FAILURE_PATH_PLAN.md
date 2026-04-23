# Kernel Validation Wrapper Failure-Path Plan

## Purpose

This document decides whether the implemented kernel-side local validation wrapper needs governed failure-path checks, and defines the smallest acceptable strategy.

It is a planning document only. It does not add wrapper failure code, runtime code, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Current Context

Implemented wrapper:

```text
validation/run_all_kernel_local_checks.py
```

Current baseline:

```text
docs/KERNEL_VALIDATION_BASELINE.md
```

Current wrapper behavior contract:

```text
docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md
```

The wrapper is now the developer-facing local validation entrypoint. It runs three standalone helpers in order and stops on first failure.

## Planning Decision

Wrapper-level failure-path checks are now justified.

Reasoning:

- the wrapper is now part of the kernel-side validation baseline;
- the wrapper has behavior that is not fully covered by child helper success checks;
- stop-on-first-failure is contractually important;
- missing-helper behavior is contractually important;
- final success signal suppression after failure is contractually important;
- these checks can be implemented without mutating real helper files or adding runtime behavior.

## Failure Conditions That Matter Most

The first failure-path check should cover only wrapper-level behavior:

| Priority | Failure condition | Why it matters |
| --- | --- | --- |
| 1 | A child helper exits non-zero. | Confirms wrapper stops immediately, returns the child exit code, and does not print final success. |
| 2 | A configured helper path is missing. | Confirms wrapper emits the governed missing-helper failure and returns `1`. |
| 3 | A failing child appears before a later passing child. | Confirms later helpers are not run after an earlier failure. |

The normal success path is already covered by running:

```text
validation/run_all_kernel_local_checks.py
```

The first failure-path check should not duplicate every child helper's own validation contract.

## Recommended Strategy

Use a small local validation helper with temporary helper scripts.

Suggested future helper path:

```text
ai-meta-kernel/validation/kernel_validation_wrapper_failure_path_checks.py
```

Recommended approach:

1. Import `validation/run_all_kernel_local_checks.py` as a module.
2. Temporarily replace its `CHECKS` list with controlled test entries.
3. Use `tempfile.TemporaryDirectory()` to create small helper scripts.
4. Create one helper script that exits non-zero.
5. Create one helper script that would pass if run after the failing helper.
6. Use a deliberately missing path for the missing-helper case.
7. Call the wrapper's `main()` directly for each scenario.
8. Capture stdout and stderr at the Python level.
9. Assert return codes, stop behavior, and final success signal suppression.

This avoids:

- renaming real validation helpers;
- deleting real files;
- modifying kernel contracts;
- invoking runtime adapter behavior;
- writing generated runtime artifacts;
- depending on shell-specific failure simulation.

## Minimum Scenarios

### Scenario A: Child Helper Exits Non-Zero

Setup:

- first temp helper exits with code `7`;
- second temp helper writes a marker file if executed.

Expected behavior:

- wrapper returns `7`;
- wrapper prints failure text for the first helper;
- wrapper does not print `kernel-local-validation-checks-ok`;
- second helper marker is not created.

### Scenario B: Missing Helper Path

Setup:

- wrapper `CHECKS` contains one missing helper path.

Expected behavior:

- wrapper returns `1`;
- wrapper emits `kernel-local-validation-checks-failed: missing helper: <path>` to stderr;
- wrapper does not print `kernel-local-validation-checks-ok`.

## Fixture, Temp File, Or Test Helper Decision

Use temporary helper scripts, not committed fixture files.

Reasoning:

- wrapper failure behavior is process-control behavior, not data-fixture behavior;
- temporary helpers avoid committing intentionally failing files into the governed validation tree;
- temp files allow stop-on-first-failure to be tested without touching real helper scripts;
- no repository mutation is needed outside the future validation helper itself.

Committed fixture files are not needed for the first wrapper failure-path check.

## Out Of Scope

The failure-path helper must not test or introduce:

- real child helper failures by mutating real helper files;
- runtime adapter invocation;
- P0-P10 runtime invocation;
- canonical task object generation from envelopes;
- response artifact writing;
- failure artifact writing;
- runtime artifact reads or writes;
- artifact polling;
- retry/backoff behavior;
- cleanup automation outside temporary directories;
- live fetching;
- scheduler runtime;
- report composition;
- CI behavior;
- package migration;
- external service calls.

## Changes Requiring A Governed Pass

The following changes require a governed pass before implementation:

- testing failure paths by renaming or modifying real helper files;
- adding committed failing fixture scripts;
- changing wrapper success or failure signals;
- changing wrapper exit-code semantics;
- changing wrapper stop-on-first-failure behavior;
- adding wrapper-level dependencies;
- connecting the failure-path helper to CI;
- adding runtime behavior or artifact validation.

## Recommended Next Phase

Implement a `Kernel-Side Validation Wrapper Failure-Path Helper Pass`.

That pass should add only the local failure-path validation helper described here, use standard library only, and avoid modifying the wrapper unless a concrete contract mismatch is discovered.
