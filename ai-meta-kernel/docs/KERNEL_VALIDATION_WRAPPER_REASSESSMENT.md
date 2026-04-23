# Kernel Validation Wrapper Reassessment

## Purpose

This document reassesses whether the current kernel-side standalone validation helpers are sufficient to justify wrapper planning or future wrapper inclusion.

It records a governed decision only. It does not add wrapper code, runtime adapter code, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Current Standalone Helpers

The current kernel-side validation helpers are:

| Helper | Scope | Success signal | Output contract |
| --- | --- | --- | --- |
| `validation/static_meta_layer_contract_checks.py` | Validates static core Meta-Layer contract artifacts, including the master spec, runtime pipeline, handoff contract, and task object schema. | `kernel-static-meta-layer-contract-checks-ok` | `docs/KERNEL_STATIC_META_LAYER_CONTRACT_CHECK_OUTPUT_CONTRACT.md` |
| `validation/kernel_file_exchange_fixture_checks.py` | Validates the static `daily_us_core` envelope, response, and failure fixtures. | `kernel-file-exchange-fixture-checks-ok` | `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_OUTPUT_CONTRACT.md` |
| `validation/kernel_file_exchange_adapter_scaffold_checks.py` | Exercises the current adapter scaffold boundary against the static fixtures and confirms blocked boundaries remain fail-closed. | `kernel-file-exchange-adapter-scaffold-checks-ok` | `docs/KERNEL_FILE_EXCHANGE_ADAPTER_SCAFFOLD_CHECK_OUTPUT_CONTRACT.md` |

All three helpers are local, standalone, and developer-facing.

They do not invoke kernel runtime, generate canonical task objects from envelopes, write response artifacts, write failure artifacts, run live fetching, run scheduler behavior, compose reports, call external services, or connect to CI.

## Breadth Change Since Prior Reassessment

The validation breadth is now materially broader than the prior reassessment.

Earlier state:

- two standalone helpers existed;
- both helpers focused on one file-exchange fixture family;
- no helper checked the core Meta-Layer contract artifacts.

Current state:

- three standalone helpers exist;
- one helper checks static core Meta-Layer contract artifacts;
- one helper checks the governed file-exchange fixtures;
- one helper checks the adapter scaffold boundary and fail-closed placeholders;
- each helper has its own output contract and fixed success signal.

This creates a meaningful validation sequence rather than only a pair of related fixture checks.

## Natural Execution Order

If a future wrapper is planned, the current natural execution order should be:

1. `validation/static_meta_layer_contract_checks.py`
2. `validation/kernel_file_exchange_fixture_checks.py`
3. `validation/kernel_file_exchange_adapter_scaffold_checks.py`

Reasoning:

- core Meta-Layer contract health should be checked before file-exchange fixture validation;
- fixture validity should be checked before scaffold boundary checks that depend on those fixtures;
- scaffold fail-closed behavior should remain the final local boundary check until runtime handoff is intentionally implemented.

## Reassessment

The helper set is no longer too narrow to justify wrapper planning.

Current observations:

1. There are now three standalone helpers, not two.
2. The helpers span core contract validation, file-exchange fixture validation, and adapter scaffold boundary validation.
3. Execution order now matters enough to document explicitly.
4. The existing standalone commands remain useful and should not be removed.
5. A wrapper would now add clarity if it is treated as local validation orchestration only.
6. A wrapper would still be premature if implemented before its own scope, output contract, success signal, and blocked behaviors are governed.

## Governed Decision

Begin wrapper planning now.

Keep all three helpers standalone until a dedicated wrapper planning pass and wrapper output contract are completed.

Do not add wrapper code in this pass.

Reasoning:

- validation breadth now covers more than one concern family;
- the expected execution order is clear enough to govern;
- one-command local validation would now reduce operator tracking burden;
- wrapper implementation still needs its own contract before code exists;
- preserving standalone helpers keeps the current validation surfaces reviewable.

## Conditions Before Wrapper Implementation

Before wrapper code is added, a governed wrapper planning pass must define:

- wrapper path and name;
- included validation layers;
- execution order;
- final success signal;
- stop-on-first-failure behavior;
- child helper output preservation behavior;
- dependency assumptions, especially `jsonschema`;
- whether `PYTHONDONTWRITEBYTECODE` remains a documented recommendation only;
- whether the wrapper uses subprocess execution or direct Python imports;
- how helper failures are surfaced;
- whether standalone helper commands remain canonical for focused checks;
- which runtime behaviors remain blocked.

Before wrapper implementation, a wrapper output contract should also be created or planned so future output drift is controlled.

## Wrapper Behaviors That Remain Blocked

A future wrapper must not silently introduce:

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
- external service calls.

## Recommended Next Phase

Implement a `Kernel-Side Validation Wrapper Planning Pass`.

That pass should define the future local wrapper boundary, likely around the three current helpers:

- `validation/static_meta_layer_contract_checks.py`
- `validation/kernel_file_exchange_fixture_checks.py`
- `validation/kernel_file_exchange_adapter_scaffold_checks.py`

It should still avoid wrapper code until the wrapper path, execution order, success signal, failure behavior, dependency assumptions, standalone-helper policy, and blocked runtime behaviors are explicitly governed.
