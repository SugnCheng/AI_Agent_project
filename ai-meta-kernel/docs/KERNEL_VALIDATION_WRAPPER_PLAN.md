# Kernel Validation Wrapper Plan

## Purpose

This document defines the smallest governed local validation wrapper plan for `ai-meta-kernel` now that three standalone validation helpers exist.

It is a planning document only. It does not add wrapper code, runtime adapter code, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Planning Basis

The current wrapper-readiness decision is recorded in:

```text
docs/KERNEL_VALIDATION_WRAPPER_REASSESSMENT.md
```

That reassessment concludes that wrapper planning is now justified, but wrapper implementation must remain blocked until the wrapper boundary and output contract are governed.

## Proposed Wrapper Path And Name

Proposed future wrapper path:

```text
ai-meta-kernel/validation/run_all_kernel_local_checks.py
```

Proposed wrapper role:

```text
kernel local validation wrapper
```

The wrapper should be local-only, developer-facing, and validation-only.

It should orchestrate existing standalone helpers. It should not replace them.

## Included Validation Helpers

The first governed wrapper should include exactly these helpers:

| Order | Helper | Responsibility | Success signal |
| --- | --- | --- | --- |
| 1 | `validation/static_meta_layer_contract_checks.py` | Checks static core Meta-Layer contract artifacts. | `kernel-static-meta-layer-contract-checks-ok` |
| 2 | `validation/kernel_file_exchange_fixture_checks.py` | Checks static kernel-side file-exchange fixtures. | `kernel-file-exchange-fixture-checks-ok` |
| 3 | `validation/kernel_file_exchange_adapter_scaffold_checks.py` | Checks the current adapter scaffold boundary and fail-closed placeholders. | `kernel-file-exchange-adapter-scaffold-checks-ok` |

No additional helpers should be included in the first wrapper without a governed pass.

## Execution Order

The wrapper should run helpers in this order:

1. `validation/static_meta_layer_contract_checks.py`
2. `validation/kernel_file_exchange_fixture_checks.py`
3. `validation/kernel_file_exchange_adapter_scaffold_checks.py`

Reasoning:

- core Meta-Layer contract health should be verified before fixture checks;
- file-exchange fixture validity should be verified before scaffold checks that depend on those fixtures;
- scaffold fail-closed behavior should remain the final local boundary check until runtime handoff is intentionally implemented.

## Final Success Signal

Proposed final wrapper success signal:

```text
kernel-local-validation-checks-ok
```

This signal should mean only that the included local validation helpers passed in the governed order.

It must not imply:

- runtime adapter invocation exists;
- P0-P10 runtime execution exists;
- canonical task object generation exists;
- response or failure artifact writing exists;
- live fetching, scheduler runtime, report composition, CI, package migration, or external service behavior exists.

## Stop-On-First-Failure Behavior

The wrapper should stop on the first failed helper.

Failure behavior should be:

1. preserve the failing helper's output and error details;
2. return a non-zero process exit;
3. not print `kernel-local-validation-checks-ok`;
4. not continue to later helpers after an earlier failure;
5. not downgrade helper failures into warnings.

This keeps root cause visibility high and avoids masking earlier contract failures with later dependent checks.

## Child Helper Output Preservation

The wrapper should preserve child helper output.

Minimum expected behavior:

- each child helper's stdout should remain visible;
- child stderr should remain visible when failures occur;
- the wrapper should add only concise phase labels or summaries;
- the wrapper should not suppress, rewrite, or reinterpret child success signals;
- the wrapper should not claim success unless all child helpers exit successfully.

The wrapper output contract should decide exact formatting before implementation.

## Dependency Assumptions

Current helper dependencies:

| Helper | Dependency assumptions |
| --- | --- |
| `validation/static_meta_layer_contract_checks.py` | Python standard library only. |
| `validation/kernel_file_exchange_fixture_checks.py` | Requires approved `jsonschema`. |
| `validation/kernel_file_exchange_adapter_scaffold_checks.py` | Requires approved `jsonschema` indirectly through response validation. |

The wrapper itself should prefer Python standard library only.

The wrapper should not install dependencies, manage virtual environments, or hide missing dependency errors. Missing `jsonschema` should surface through the relevant child helper failure.

`PYTHONDONTWRITEBYTECODE=1` may remain a documented local command recommendation. It should not become a hidden dependency.

## Standalone Helper Policy

All included helpers should remain standalone after wrapper introduction.

Reasoning:

- focused checks remain useful during local debugging;
- output contracts already exist for each helper;
- wrapper orchestration should not become the only supported validation path;
- standalone helpers make drift easier to isolate.

The wrapper should be treated as a convenience and baseline orchestration layer, not as a replacement for individual helper contracts.

## Blocked Runtime Behaviors

The future wrapper must not silently introduce:

- runtime adapter invocation;
- P0-P10 runtime invocation;
- canonical task object generation from envelopes;
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
- generic multi-profile production validation.

## Changes Requiring A Governed Pass

The following changes require a governed pass before implementation:

- changing the proposed wrapper path;
- changing the proposed wrapper success signal;
- changing included helpers;
- changing execution order;
- changing stop-on-first-failure behavior;
- suppressing or transforming child helper output;
- adding dependencies to the wrapper itself;
- removing standalone helper support;
- broadening validation beyond the three current helpers;
- connecting wrapper execution to CI;
- adding runtime artifact validation;
- adding any runtime adapter behavior.

## Implementation Gate

Wrapper code should not be added until a wrapper output contract is created.

That output contract should define:

- exact execution phase labels;
- exact final success signal;
- expected failure output behavior;
- child output preservation behavior;
- process exit behavior;
- drift rules;
- explicit non-goals and blocked runtime behaviors.

## Recommended Next Phase

Implement a `Kernel-Side Validation Wrapper Output Contract Snapshot Pass`.

That pass should create a contract for the planned wrapper output before any wrapper code exists. Only after that contract is in place should a future implementation pass add `validation/run_all_kernel_local_checks.py`.
