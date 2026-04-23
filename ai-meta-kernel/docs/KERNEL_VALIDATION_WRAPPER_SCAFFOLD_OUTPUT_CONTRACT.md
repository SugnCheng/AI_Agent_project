# Kernel Validation Wrapper Scaffold Output Contract

## Purpose

This document snapshots the implemented developer-facing output contract for:

```text
ai-meta-kernel/validation/run_all_kernel_local_checks.py
```

It confirms the wrapper scaffold's actual execution behavior, final success signal, failure behavior, child output preservation, process exit behavior, standalone helper policy, and drift rules.

This document does not add runtime behavior, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Documentation Index

For the current validation documentation map, see:

```text
docs/KERNEL_VALIDATION_DOCUMENTATION_INDEX.md
```

## Actual Wrapper Path And Scope

Actual wrapper path:

```text
ai-meta-kernel/validation/run_all_kernel_local_checks.py
```

Actual scope:

- local-only validation orchestration;
- developer-facing command entrypoint;
- sequential execution of three governed kernel-side validation helpers;
- child helper stdout and stderr preservation through normal subprocess inheritance;
- stop-on-first-failure behavior.

The wrapper does not replace the standalone helpers.

## Actual Execution Order

The wrapper runs exactly these helpers in this order:

| Order | Phase label | Helper | Expected child success signal |
| --- | --- | --- | --- |
| 1 | `static Meta-Layer contract checks` | `validation/static_meta_layer_contract_checks.py` | `kernel-static-meta-layer-contract-checks-ok` |
| 2 | `kernel file-exchange fixture checks` | `validation/kernel_file_exchange_fixture_checks.py` | `kernel-file-exchange-fixture-checks-ok` |
| 3 | `kernel file-exchange adapter scaffold checks` | `validation/kernel_file_exchange_adapter_scaffold_checks.py` | `kernel-file-exchange-adapter-scaffold-checks-ok` |

The wrapper currently emits a phase label before each helper:

```text
[kernel-local-validation] running: <phase label>
```

The phase label is flushed before child execution so the visible order matches the execution order.

## Actual Final Success Signal

If all three helpers exit zero, the wrapper prints exactly:

```text
kernel-local-validation-checks-ok
```

This signal means only that the three included local validation helpers passed in the governed order.

It does not mean:

- kernel runtime invocation exists;
- P0-P10 execution exists;
- canonical task object generation exists;
- runtime artifact reads or writes exist;
- response artifact writing exists;
- failure artifact writing exists;
- live fetching, scheduler runtime, report composition, CI, package migration, or external service calls exist.

## Actual Failure Output Behavior

If a helper script is missing, the wrapper prints to stderr:

```text
kernel-local-validation-checks-failed: missing helper: <path>
```

If a helper exits non-zero, the wrapper prints to stderr:

```text
kernel-local-validation-checks-failed: <phase label> exited with <exit_code>
```

The wrapper then stops immediately and returns the failing exit code.

The wrapper does not print `kernel-local-validation-checks-ok` after a failure.

## Child Helper Output Preservation Rules

The wrapper uses subprocess execution without capturing stdout or stderr.

Current preservation behavior:

- child stdout remains visible;
- child stderr remains visible;
- child success signals remain visible;
- child failure details remain visible;
- wrapper phase labels are additive only;
- wrapper failure labels are additive only;
- wrapper does not rewrite child helper output;
- wrapper does not infer success if a child exits non-zero.

## Actual Process Exit Behavior

| Condition | Actual wrapper behavior |
| --- | --- |
| All helpers pass | Exits zero and prints `kernel-local-validation-checks-ok`. |
| Any helper exits non-zero | Stops immediately and returns that helper's non-zero exit code. |
| Helper script is missing | Stops immediately and returns `1`. |
| `jsonschema` is missing | Surfaces through the relevant child helper failure and exits non-zero. |

The wrapper does not install dependencies, create fixtures, repair files, or mutate repository state.

## Standalone Helper Policy

The following helpers remain canonical standalone checks:

- `validation/static_meta_layer_contract_checks.py`
- `validation/kernel_file_exchange_fixture_checks.py`
- `validation/kernel_file_exchange_adapter_scaffold_checks.py`

The wrapper is a convenience and baseline orchestration layer only.

Focused debugging should continue to use the standalone helper commands and their individual output contracts.

## Blocked Runtime Behaviors

The wrapper scaffold must not silently introduce:

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

- changing the wrapper path;
- changing the final success signal;
- changing execution order;
- adding or removing included helpers;
- changing phase labels in a way that affects expected output;
- changing stop-on-first-failure behavior;
- capturing, suppressing, or transforming child stdout or stderr;
- replacing child success signals with wrapper-only summaries;
- allowing warnings to pass where errors currently fail;
- adding wrapper-level dependencies;
- removing standalone helper support;
- connecting the wrapper to CI;
- broadening validation beyond the three current helpers;
- adding runtime artifact validation;
- adding runtime adapter behavior;
- adding file mutation or auto-repair behavior.

## Local Command

Run from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\run_all_kernel_local_checks.py'
```

Expected successful output includes the three child helper success signals and ends with:

```text
kernel-local-validation-checks-ok
```

## Recommended Next Phase

Implement a `Kernel-Side Validation Baseline Refresh Pass`.

That pass should update kernel-side validation baseline documentation to include the implemented wrapper scaffold while keeping runtime handoff, CI, and production validation out of scope.
