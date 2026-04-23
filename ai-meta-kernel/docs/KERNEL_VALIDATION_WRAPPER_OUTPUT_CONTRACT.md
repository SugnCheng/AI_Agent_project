# Kernel Validation Wrapper Output Contract

## Purpose

This document snapshots the planned developer-facing output contract for the future kernel-side local validation wrapper:

```text
ai-meta-kernel/validation/run_all_kernel_local_checks.py
```

It fixes the wrapper's planned execution order, final success signal, failure behavior, child output preservation, process exit behavior, standalone helper policy, and drift rules.

This document does not add wrapper code, runtime adapter code, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Wrapper Path And Scope

Planned wrapper path:

```text
ai-meta-kernel/validation/run_all_kernel_local_checks.py
```

Planned wrapper scope:

- local-only validation orchestration;
- developer-facing command entrypoint;
- sequential execution of the governed kernel-side validation helpers;
- preservation of each helper's standalone contract and output.

The wrapper must not replace the standalone helpers.

## Exact Execution Order

The planned wrapper must run exactly these helpers in this order:

| Order | Helper | Required child success signal |
| --- | --- | --- |
| 1 | `validation/static_meta_layer_contract_checks.py` | `kernel-static-meta-layer-contract-checks-ok` |
| 2 | `validation/kernel_file_exchange_fixture_checks.py` | `kernel-file-exchange-fixture-checks-ok` |
| 3 | `validation/kernel_file_exchange_adapter_scaffold_checks.py` | `kernel-file-exchange-adapter-scaffold-checks-ok` |

No additional checks should run before, between, or after these helpers without a governed pass.

## Final Success Signal

If and only if all three helpers pass in the governed order, the wrapper should print exactly:

```text
kernel-local-validation-checks-ok
```

This final success signal means only that the included local validation helpers completed successfully.

It does not mean:

- kernel runtime invocation exists;
- P0-P10 execution exists;
- canonical task object generation exists;
- file-exchange runtime artifact reads or writes exist;
- response artifact writing exists;
- failure artifact writing exists;
- live fetching, scheduler runtime, report composition, CI, package migration, or external service calls exist.

## Expected Failure Output Behavior

If any helper fails, the wrapper should:

1. preserve the failing helper's stdout and stderr;
2. identify which helper failed;
3. stop before running later helpers;
4. return a non-zero process exit;
5. not print `kernel-local-validation-checks-ok`;
6. not rewrite the child helper error as a generic wrapper-only failure;
7. not downgrade child helper failures into warnings.

The wrapper may add concise phase labels, but those labels must not obscure the underlying helper output.

## Child Helper Output Preservation Rules

The wrapper should preserve child helper output according to these rules:

- child stdout remains visible;
- child stderr remains visible when present;
- child success signals remain visible;
- child failure details remain visible;
- wrapper labels are additive only;
- wrapper labels must not replace child success or failure output;
- wrapper must not infer success from partial output if the child process exits non-zero.

The wrapper should avoid verbose summaries that make child output hard to inspect.

## Process Exit Behavior

Expected process behavior:

| Condition | Wrapper behavior |
| --- | --- |
| All helpers pass | Exit zero and print `kernel-local-validation-checks-ok`. |
| Any helper exits non-zero | Stop immediately, exit non-zero, and do not print final success signal. |
| A helper script is missing | Exit non-zero and identify the missing helper. |
| Python cannot start a helper | Exit non-zero and preserve the process error. |
| `jsonschema` is missing | Exit non-zero through the relevant child helper failure. |

The wrapper should not install dependencies, repair files, create fixtures, or mutate repository state.

## Standalone Helper Policy

All included helpers remain canonical standalone checks after wrapper introduction:

- `validation/static_meta_layer_contract_checks.py`
- `validation/kernel_file_exchange_fixture_checks.py`
- `validation/kernel_file_exchange_adapter_scaffold_checks.py`

The wrapper is a convenience and baseline orchestration layer only.

Focused debugging should continue to use the standalone helper commands and their individual output contracts.

## Dependency Assumptions

The wrapper itself should use only the Python standard library.

Approved dependency assumptions are inherited from child helpers:

- `validation/static_meta_layer_contract_checks.py` uses standard library only;
- `validation/kernel_file_exchange_fixture_checks.py` requires approved `jsonschema`;
- `validation/kernel_file_exchange_adapter_scaffold_checks.py` requires approved `jsonschema` indirectly through response validation.

The wrapper must not hide missing dependency failures or install dependencies automatically.

## Blocked Runtime Behaviors

The wrapper must not silently introduce:

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
- changing stop-on-first-failure behavior;
- suppressing child stdout or stderr;
- replacing child success signals with wrapper-only summaries;
- allowing warnings to pass where errors currently fail;
- adding wrapper-level dependencies;
- removing standalone helper support;
- connecting the wrapper to CI;
- broadening validation beyond the three current helpers;
- adding runtime artifact validation;
- adding runtime adapter behavior;
- adding any file mutation or auto-repair behavior.

## Implementation Gate

Future wrapper implementation must conform to this contract unless a governed pass revises the contract first.

The first implementation pass should add only:

```text
ai-meta-kernel/validation/run_all_kernel_local_checks.py
```

It should not modify kernel contracts, helper contracts, fixtures, runtime adapter scaffolds, or downstream macro-agent files.

## Recommended Next Phase

Implement a `Kernel-Side Validation Wrapper Scaffold Pass`.

That pass may add the planned `validation/run_all_kernel_local_checks.py` wrapper if it strictly follows this output contract and preserves all three standalone helpers.
