# Kernel Validation Wrapper Runtime Reader Helper Inclusion Gate

## Purpose

This note defines the gate for whether and when the standalone runtime envelope reader contract helper may be included in the main kernel local validation wrapper.

It is a developer-facing gate note only. It does not modify `validation/run_all_kernel_local_checks.py`, add runtime code, modify kernel contracts, invoke kernel runtime, write artifacts, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Current Inclusion Decision

Current decision:

```text
runtime_reader_contract_helper_remains_standalone_outside_main_wrapper
```

The standalone helper is:

```text
validation/kernel_runtime_envelope_reader_contract_checks.py
```

Its success signal is:

```text
kernel-runtime-envelope-reader-contract-checks-ok
```

The main wrapper remains unchanged:

```text
validation/run_all_kernel_local_checks.py
```

The helper is not currently included in the wrapper's `CHECKS` list.

## Why It Remains Standalone

The helper remains standalone because the current wrapper is the stable three-helper success-path baseline:

1. static Meta-Layer contract checks;
2. kernel file-exchange fixture checks;
3. kernel file-exchange adapter scaffold checks.

The runtime envelope reader helper covers a newly governed future boundary. It validates scaffold-level reader and intake guardrails, but that boundary is not yet a runtime implementation surface.

Keeping it standalone preserves:

- the existing wrapper output contract;
- the existing wrapper execution order;
- the existing final success signal meaning;
- a clear distinction between current local validation baseline and future runtime-adapter boundary validation;
- focused debugging for reader-contract failures without broadening wrapper behavior.

## Prerequisites Before Wrapper Inclusion

The helper may be considered for wrapper inclusion only after a governed pass confirms all of the following:

1. The reader helper has a stable output contract reference and success signal.
2. The reader helper remains deterministic, local-only, and free of file mutation.
3. The helper still uses only Python standard library plus the existing scaffold module.
4. The helper still does not create runtime artifacts, discover queues, poll, retry, clean up, invoke runtime, or write response/failure artifacts.
5. The wrapper execution order is explicitly re-reviewed.
6. The final wrapper success signal meaning is updated to include reader-contract coverage.
7. The wrapper failure-path helper is updated or confirmed to still cover stop-on-first-failure and success-signal suppression with the expanded `CHECKS` list.
8. The validation baseline is updated before or with inclusion.
9. The validation documentation index is updated before or with inclusion.
10. No runtime reader implementation has been silently introduced as part of inclusion.

## Documents And Contracts To Update If Inclusion Happens Later

If a later governed pass includes the reader helper in `validation/run_all_kernel_local_checks.py`, that pass must update at minimum:

| File | Required update |
| --- | --- |
| `validation/run_all_kernel_local_checks.py` | Add the reader helper to `CHECKS` in a governed execution position. |
| `docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md` | Update wrapper helper order, final success signal meaning, and blocked behavior scope. |
| `docs/KERNEL_VALIDATION_BASELINE.md` | Record that the reader helper is now wrapper-included rather than standalone-only. |
| `docs/KERNEL_VALIDATION_DOCUMENTATION_INDEX.md` | Update navigation, commands, and standalone/wrapper status. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md` | Confirm success signal references and wrapper relationship remain accurate if needed. |
| `validation/kernel_validation_wrapper_failure_path_checks.py` | Confirm or update failure-path coverage for the expanded wrapper helper list. |

Any inclusion pass must run both the expanded wrapper and the wrapper failure-path helper locally before completion.

## What Must Remain Blocked

Wrapper inclusion must not silently introduce:

- runtime envelope reader implementation;
- runtime directory scanning;
- artifact queue discovery;
- artifact polling or watcher behavior;
- retry/backoff behavior;
- cleanup automation;
- intake mapping implementation;
- `kernel_intake_context` construction;
- P0/P1 execution;
- P0-P10 runtime invocation;
- canonical task object generation from envelope evidence;
- response artifact writing;
- failure artifact writing;
- CLI behavior;
- live fetching;
- scheduler runtime;
- report composition;
- archive/export automation;
- CI behavior;
- package migration;
- external service calls;
- kernel contract modifications;
- macro-side production of kernel response artifacts.

## Recommended Next Phase

Implement a `Kernel-Side Validation Baseline Wrapper Inclusion Gate Refresh Pass`.

That pass should update the validation baseline so this wrapper inclusion gate is discoverable and the reader helper's standalone status remains explicit, while keeping wrapper behavior, reader implementation code, intake mapping code, runtime invocation, response/failure writers, CLI, CI, scheduler behavior, live fetching, report composition, package migration, external service calls, and actual handoff execution out of scope.
