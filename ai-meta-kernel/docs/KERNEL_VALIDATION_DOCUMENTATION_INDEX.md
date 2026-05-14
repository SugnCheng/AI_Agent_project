# Kernel Validation Documentation Index

## Purpose

This document is a developer-facing index for the current `ai-meta-kernel` validation documentation surface.

It points to the current standalone helper contracts, wrapper contracts, wrapper failure-path contract, first-slice adapter fixture validation notes, runtime envelope reader contract, writer-boundary notes, intake-mapping notes, baseline note, reassessment notes, and planning notes so developers can find the right validation document quickly.

This index does not add runtime behavior, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Start Here

| Document | Use it for |
| --- | --- |
| `docs/KERNEL_VALIDATION_BASELINE.md` | Current validation baseline: what exists now, what success-path validation means, what failure-path validation means, and what remains blocked. |
| `docs/KERNEL_VALIDATION_DOCUMENTATION_INDEX.md` | Navigation map for the validation docs. |

## Standalone Validation Helpers And Contracts

These documents describe the individually runnable validation helpers. Use them when debugging a specific validation surface before using the wrapper.

| Helper | Output contract | What it is for |
| --- | --- | --- |
| `validation/static_meta_layer_contract_checks.py` | `docs/KERNEL_STATIC_META_LAYER_CONTRACT_CHECK_OUTPUT_CONTRACT.md` | Static checks for canonical Meta-Layer contract artifacts, schema shape, required fields, handoff modes, and P0-P10 references. |
| `validation/kernel_file_exchange_fixture_checks.py` | `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_OUTPUT_CONTRACT.md` | Static validation for the governed `daily_us_core` file-exchange envelope, response, and failure fixtures. |
| `validation/kernel_file_exchange_adapter_scaffold_checks.py` | `docs/KERNEL_FILE_EXCHANGE_ADAPTER_SCAFFOLD_CHECK_OUTPUT_CONTRACT.md` | Scaffold boundary checks for fixture reads, response validation, and fail-closed adapter placeholders. |

## Wrapper Contracts

These documents describe the developer-facing local wrapper and its failure-path helper.

| Script | Contract | What it is for |
| --- | --- | --- |
| `validation/run_all_kernel_local_checks.py` | `docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md` | Current wrapper behavior: helper order, child output preservation, final success signal, stop-on-first-failure behavior, and blocked runtime behaviors. |
| `validation/kernel_validation_wrapper_failure_path_checks.py` | `docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_OUTPUT_CONTRACT.md` | Wrapper failure-path behavior: non-zero child exit, missing helper path, later-helper suppression, and final success signal suppression. |

## First-Slice Adapter Fixture Validation

These documents describe the first implementation slice's adapter fixture validation surface. Use them after the baseline when checking whether the current fixture and scaffold helpers already cover the first-slice contract.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_VALIDATION_OUTPUT_CONTRACT.md` | Output contract for the first-slice validation surface: fixtures in scope, allowed validation, success signals, expected failures, blocked behaviors, and governed drift rules. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_HELPER_COVERAGE.md` | Helper-free coverage decision confirming the existing fixture and scaffold helpers fully cover the first-slice contract. |

## Runtime Envelope Reader Boundary Contract

This document describes the first future implementation-sequence boundary for the runtime adapter path. Use it after the baseline and implementation sequence when checking what the future reader may accept and where it must stop. It is not implemented runtime behavior.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md` | Output contract for the future runtime envelope reader boundary: allowed explicit local input path, successful reader output, fail-closed failure behavior, stop-before-intake guarantee, blocked behaviors, and governed change triggers. |

## Writer-Boundary Planning And Contracts

These documents describe the future response writer and blocking failure writer boundaries. Use them after the baseline and first-slice fixture validation notes when checking what writer behavior is planned but still blocked.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_PLAN.md` | Planning note for future response writer and blocking failure writer boundaries, including validation order and blocked behavior before implementation. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md` | Output contract for future writer behavior: artifact naming, pre-write validation guarantees, mutual exclusivity, blocked behaviors, and governed change triggers. |

## Intake-Mapping Planning And Contracts

These documents describe the future envelope-to-P0/P1 intake mapping boundary. Use them after the baseline and first-slice fixture validation notes when checking what envelope material may become future intake context and what must remain kernel-owned reasoning.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_PLAN.md` | Planning note for the future envelope-to-P0/P1 intake mapping boundary, including allowed envelope field flow and blocked behavior before implementation. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_OUTPUT_CONTRACT.md` | Output contract for future intake mapping: allowed inputs, acceptable `kernel_intake_context` output, excluded canonical fields, stop boundary, blocked behaviors, and governed change triggers. |

## Baseline, Reassessment, And Planning Notes

These documents explain how the validation surface evolved and what decisions have already been bounded.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_VALIDATION_BASELINE.md` | Current milestone snapshot for standalone helpers, local wrapper, failure-path helper, success-path meaning, failure-path meaning, and governed drift rules. |
| `docs/KERNEL_VALIDATION_WRAPPER_REASSESSMENT.md` | Reassessment note for whether wrapper orchestration is justified from the current standalone helper surface. |
| `docs/KERNEL_VALIDATION_WRAPPER_PLAN.md` | Planning note for the local validation wrapper before implementation. |
| `docs/KERNEL_VALIDATION_WRAPPER_OUTPUT_CONTRACT.md` | Earlier wrapper output contract snapshot retained for wrapper-contract history. |
| `docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md` | Current implemented wrapper scaffold output contract. Prefer this over older wrapper contract notes when checking current behavior. |
| `docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_PLAN.md` | Planning note for the wrapper failure-path helper before implementation. |
| `docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_OUTPUT_CONTRACT.md` | Current implemented wrapper failure-path output contract. |
| `docs/KERNEL_STATIC_META_LAYER_CONTRACT_CHECK_PLAN.md` | Planning note for static Meta-Layer contract checks. |
| `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_PLAN.md` | Planning note for static file-exchange fixture checks. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_SCAFFOLD_PLAN.md` | Planning note for adapter scaffold boundary validation. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_FIXTURE_PLAN.md` | Planning note for the first acceptable adapter fixture validation slice. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_SEQUENCE.md` | Sequencing note for future runtime reader, intake mapping, runtime invocation, response validation, response writer, blocking failure writer, local invocation, and artifact policy work. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md` | Output contract for the first future runtime adapter implementation-sequence boundary. It remains non-implementation governance. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_PLAN.md` | Planning note for future response/failure writer boundaries before implementation. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_PLAN.md` | Planning note for future envelope-to-P0/P1 intake mapping before implementation. |

## Practical Reading Order

For current local validation behavior:

1. Read `docs/KERNEL_VALIDATION_BASELINE.md`.
2. Read `docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md`.
3. Read `docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_OUTPUT_CONTRACT.md`.
4. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_VALIDATION_OUTPUT_CONTRACT.md` when checking first-slice adapter fixture validation.
5. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_HELPER_COVERAGE.md` to confirm whether a new helper is needed.
6. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_SEQUENCE.md` when checking future runtime adapter implementation order.
7. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md` when checking the first future reader boundary and its stop-before-intake guarantee.
8. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md` when checking future writer expectations and blocked writer behavior.
9. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_OUTPUT_CONTRACT.md` when checking future intake-context expectations and blocked mapping behavior.
10. Read the specific standalone helper contract only when debugging that helper.

For planning or governance review:

1. Read `docs/KERNEL_VALIDATION_BASELINE.md`.
2. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_FIXTURE_PLAN.md` for the first-slice adapter fixture strategy when adapter fixture validation is in scope.
3. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_SEQUENCE.md` when future runtime adapter implementation order is in scope.
4. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md` when the first future runtime reader boundary is in scope.
5. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_PLAN.md` when response/failure writer boundaries are in scope.
6. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_PLAN.md` when envelope-to-P0/P1 intake mapping is in scope.
7. Read the relevant plan or reassessment note.
8. Compare proposed changes against the related output contract drift rules.
9. Treat runtime behavior, CI, fetching, scheduler, reporting, package migration, and handoff execution as out of scope unless a new governed pass explicitly changes that boundary.

## Current Local Commands

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

## Explicit Non-Goals

This documentation index must not silently introduce:

- runtime adapter invocation;
- P0-P10 runtime invocation;
- canonical task object generation from envelopes;
- kernel intake preparation;
- response artifact writing;
- failure artifact writing;
- response writer implementation;
- failure writer implementation;
- intake mapping implementation;
- P0/P1 execution;
- runtime envelope reader implementation;
- runtime directory scanning;
- artifact queue discovery;
- runtime artifact reads or writes;
- live fetching;
- scheduler runtime;
- report composition;
- CI behavior;
- package migration;
- external service calls;
- validation auto-repair;
- repository structure redesign.

## Recommended Next Phase

Implement a `Kernel-Side Runtime Envelope Reader Helper Coverage Pass`.

That pass should determine whether the existing scaffold and validation helpers already cover the runtime envelope reader output contract surface, and add no helper unless there is a minimal local-only coverage gap. It should still avoid reader implementation code, intake mapping code, runtime invocation, response/failure writers, CLI, CI, scheduler behavior, live fetching, report composition, package migration, external service calls, and actual handoff execution.
