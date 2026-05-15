# Kernel Validation Documentation Index

## Purpose

This document is a developer-facing index for the current `ai-meta-kernel` validation documentation surface.

It points to the current standalone helper contracts, wrapper contracts, wrapper failure-path contract, runtime reader wrapper inclusion gate and reassessment, first-slice adapter fixture validation notes, runtime envelope reader contract, helper, Phase R2 minimal implementation notes, post-reader handoff gate, Phase R5 intake mapping implementation notes and helper, post-intake mapping runtime invocation gate, Phase R8 runtime invocation implementation notes and helper, Phase R10 response validation implementation notes and helper, post-response-validation writer gate, writer-boundary notes, intake-mapping notes, baseline note, reassessment notes, and planning notes so developers can find the right validation document quickly.

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
| `validation/kernel_runtime_envelope_reader_contract_checks.py` | `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md` | Standalone reader contract helper for the future runtime envelope reader surface. Success signal: `kernel-runtime-envelope-reader-contract-checks-ok`. It is not currently included in `validation/run_all_kernel_local_checks.py`. |
| `validation/kernel_intake_mapping_contract_checks.py` | `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_OUTPUT_CONTRACT.md` | Standalone intake mapping helper for the context-only mapper. Success signal: `kernel-intake-mapping-contract-checks-ok`. It is not currently included in `validation/run_all_kernel_local_checks.py`. |
| `validation/kernel_runtime_invocation_contract_checks.py` | `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_OUTPUT_CONTRACT.md` | Standalone runtime invocation helper for the candidate-only invocation boundary. Success signal: `kernel-runtime-invocation-contract-checks-ok`. It is not currently included in `validation/run_all_kernel_local_checks.py`. |
| `validation/kernel_response_validation_contract_checks.py` | `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_OUTPUT_CONTRACT.md` | Standalone response validation helper for the local candidate-response validation boundary. Success signal: `kernel-response-validation-contract-checks-ok`. It is not currently included in `validation/run_all_kernel_local_checks.py`. |

## Wrapper Contracts

These documents describe the developer-facing local wrapper and its failure-path helper.

| Script | Contract | What it is for |
| --- | --- | --- |
| `validation/run_all_kernel_local_checks.py` | `docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md` | Current wrapper behavior: helper order, child output preservation, final success signal, stop-on-first-failure behavior, and blocked runtime behaviors. |
| `validation/kernel_validation_wrapper_failure_path_checks.py` | `docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_OUTPUT_CONTRACT.md` | Wrapper failure-path behavior: non-zero child exit, missing helper path, later-helper suppression, and final success signal suppression. |
| `validation/kernel_runtime_envelope_reader_contract_checks.py` | `docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_GATE.md` | Wrapper inclusion gate for the standalone runtime reader helper. Current decision: keep the helper outside `validation/run_all_kernel_local_checks.py`; wrapper behavior is unchanged. |
| `validation/kernel_runtime_envelope_reader_contract_checks.py` | `docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_REASSESSMENT.md` | TASK 114 reassessment for the next milestone. Current decision: keep the helper standalone; `kernel-local-validation-checks-ok` does not include reader helper coverage; `kernel-runtime-envelope-reader-contract-checks-ok` remains separately runnable. |

## First-Slice Adapter Fixture Validation

These documents describe the first implementation slice's adapter fixture validation surface. Use them after the baseline when checking whether the current fixture and scaffold helpers already cover the first-slice contract.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_VALIDATION_OUTPUT_CONTRACT.md` | Output contract for the first-slice validation surface: fixtures in scope, allowed validation, success signals, expected failures, blocked behaviors, and governed drift rules. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_HELPER_COVERAGE.md` | Helper-free coverage decision confirming the existing fixture and scaffold helpers fully cover the first-slice contract. |

## Runtime Envelope Reader Boundary Contract

This section describes the first implementation-sequence boundary for the runtime adapter path. Use it after the baseline and implementation sequence when checking what the minimal reader accepts, where it stops, and which standalone helper covers the current reader contract surface. It is not intake mapping, runtime invocation, writer behavior, or handoff execution.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md` | Output contract for the future runtime envelope reader boundary: allowed explicit local input path, successful reader output, fail-closed failure behavior, stop-before-intake guarantee, blocked behaviors, and governed change triggers. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_BOUNDARY_PLAN.md` | Phase R2 boundary note for the implemented minimal runtime reader slice. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_OUTPUT_CONTRACT.md` | Phase R2 output contract for the minimal reader implementation slice. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_VALIDATION_PLAN.md` | Phase R2 validation plan reflected by the standalone reader helper. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_READER_HANDOFF_GATE.md` | Post-reader gate note. Current decision: minimal explicit-file reader and context-only intake mapper are implemented, while actual handoff remains closed. |
| `docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_GATE.md` | Gate note defining whether and when the standalone reader helper may be included in the main local wrapper. Current decision: `runtime_reader_contract_helper_remains_standalone_outside_main_wrapper`. |
| `docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_REASSESSMENT.md` | TASK 114 reassessment note for the next milestone. Current decision: `runtime_reader_contract_helper_remains_standalone_outside_main_wrapper_for_next_milestone`. The main wrapper remains unchanged. |

| Helper | Success signal | Current status |
| --- | --- | --- |
| `validation/kernel_runtime_envelope_reader_contract_checks.py` | `kernel-runtime-envelope-reader-contract-checks-ok` | Standalone helper that exercises the current scaffold reader and intake guardrails against the runtime envelope reader output contract. It is intentionally outside `validation/run_all_kernel_local_checks.py` for the next milestone. |

The main wrapper success signal:

```text
kernel-local-validation-checks-ok
```

does not include runtime reader helper coverage at the current milestone.

## Intake-Mapping Planning And Contracts

These documents describe the future envelope-to-P0/P1 intake mapping boundary. Use them after the baseline and first-slice fixture validation notes when checking what envelope material may become future intake context and what must remain kernel-owned reasoning.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_PLAN.md` | Planning note for the future envelope-to-P0/P1 intake mapping boundary, including allowed envelope field flow and blocked behavior before implementation. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_OUTPUT_CONTRACT.md` | Output contract for future intake mapping: allowed inputs, acceptable `kernel_intake_context` output, excluded canonical fields, stop boundary, blocked behaviors, and governed change triggers. |

## Intake-Mapping Minimal Implementation

These documents describe the Phase R5 minimal context-only mapper. Use them after the reader implementation and post-reader handoff gate, before any runtime invocation proposal.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_BOUNDARY_PLAN.md` | Phase R5 boundary note for the implemented mapper from one validated `kernel_input_envelope` to one kernel-owned `kernel_intake_context`. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_OUTPUT_CONTRACT.md` | Phase R5 output contract for minimal mapping output. It excludes canonical task objects, response/failure artifacts, P0/P1 results, runtime results, and report eligibility. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_VALIDATION_PLAN.md` | Phase R5 validation plan reflected by the standalone mapper helper, including allowed field flow, excluded kernel conclusions, fail-closed behavior, and stop-before-runtime guarantees. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_INTAKE_MAPPING_RUNTIME_INVOCATION_GATE.md` | Phase R6 post-mapping gate note. Current decision: minimal reader and context-only mapper are implemented, while runtime invocation, canonical task object generation, writers, CLI, wrapper inclusion, and actual handoff remain closed. |

## Runtime Invocation Minimal Implementation

These documents describe the Phase R8 minimal candidate-only runtime invocation boundary. Use them after the post-intake mapping runtime invocation gate and before writer-boundary docs.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_BOUNDARY_PLAN.md` | Phase R8 boundary note for the implemented candidate-only invocation path from one validated `kernel_intake_context` to one candidate kernel response object. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_OUTPUT_CONTRACT.md` | Phase R8 output contract for candidate response output and fail-closed invocation failure behavior before writers exist. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_VALIDATION_PLAN.md` | Phase R8 validation plan reflected by the standalone invocation helper, including malformed intake rejection, candidate response expectations, and stop-before-writer guarantees. |

## Response Validation Minimal Implementation

These documents describe the Phase R10 minimal local response validation boundary. Use them after runtime invocation implementation docs and before writer-boundary docs.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_BOUNDARY_PLAN.md` | Phase R10 boundary note for the implemented path from one current R8 candidate response object to one local validated pre-writer response object. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_OUTPUT_CONTRACT.md` | Phase R10 output contract for local validated pre-writer response output and fail-closed validation failure behavior before writers exist. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_VALIDATION_PLAN.md` | Phase R10 validation plan reflected by the standalone response validation helper, including current candidate marker checks and stop-before-writer guarantees. |

## Writer-Boundary Planning And Contracts

These documents describe the future response writer and blocking failure writer boundaries. Use them after response validation and the post-response-validation writer gate when checking what writer behavior is planned but still blocked.

| Document | What it is for |
| --- | --- |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_RESPONSE_VALIDATION_WRITER_GATE.md` | Phase R11 gate note confirming local response validation is implemented while response/failure writers, CLI, macro reporting, and actual handoff remain closed. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_PLAN.md` | Planning note for future response writer and blocking failure writer boundaries, including validation order and blocked behavior before implementation. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md` | Output contract for future writer behavior: artifact naming, pre-write validation guarantees, mutual exclusivity, blocked behaviors, and governed change triggers. |

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
| `docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_GATE.md` | Gate note for future wrapper inclusion of the standalone runtime envelope reader helper. It records that no wrapper behavior has changed. |
| `docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_REASSESSMENT.md` | TASK 114 reassessment note confirming the reader helper remains standalone for the next milestone and wrapper success does not include reader-helper coverage. |
| `docs/KERNEL_STATIC_META_LAYER_CONTRACT_CHECK_PLAN.md` | Planning note for static Meta-Layer contract checks. |
| `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_PLAN.md` | Planning note for static file-exchange fixture checks. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_SCAFFOLD_PLAN.md` | Planning note for adapter scaffold boundary validation. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_FIXTURE_PLAN.md` | Planning note for the first acceptable adapter fixture validation slice. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_SEQUENCE.md` | Sequencing note for future runtime reader, intake mapping, runtime invocation, response validation, response writer, blocking failure writer, local invocation, and artifact policy work. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md` | Output contract for the runtime reader boundary and stop-before-intake guarantee. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_BOUNDARY_PLAN.md` | Phase R2 boundary note for the implemented minimal reader slice. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_OUTPUT_CONTRACT.md` | Phase R2 output contract for the implemented minimal reader slice. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_VALIDATION_PLAN.md` | Phase R2 validation plan reflected by current standalone reader checks. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_READER_HANDOFF_GATE.md` | Post-reader handoff gate after Phase R2. It records that the minimal explicit-file reader is implemented but intake mapping, runtime invocation, writers, CLI, wrapper inclusion, and actual handoff remain closed. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_BOUNDARY_PLAN.md` | Phase R5 boundary note for the implemented minimal context-only intake mapper. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_OUTPUT_CONTRACT.md` | Phase R5 implementation output contract for current `kernel_intake_context` output. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_VALIDATION_PLAN.md` | Phase R5 validation plan reflected by current standalone intake mapping checks. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_INTAKE_MAPPING_RUNTIME_INVOCATION_GATE.md` | Phase R6 runtime invocation gate after minimal context-only mapping. It records that runtime invocation preparation should precede implementation; Phase R8 now provides the minimal candidate-only implementation. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_BOUNDARY_PLAN.md` | Phase R8 runtime invocation implementation boundary note. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_OUTPUT_CONTRACT.md` | Phase R8 runtime invocation candidate output contract. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_VALIDATION_PLAN.md` | Phase R8 runtime invocation validation plan reflected by standalone checks. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_BOUNDARY_PLAN.md` | Phase R10 response validation implementation boundary. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_OUTPUT_CONTRACT.md` | Phase R10 response validation output contract. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_VALIDATION_PLAN.md` | Phase R10 response validation validation plan. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_RESPONSE_VALIDATION_WRITER_GATE.md` | Phase R11 post-response-validation writer gate. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_PLAN.md` | Planning note for future response/failure writer boundaries before implementation. |
| `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_PLAN.md` | Planning note for future envelope-to-P0/P1 intake mapping before implementation. |

## Practical Reading Order

For current local validation behavior:

1. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md` when checking the reader boundary and its stop-before-intake guarantee.
2. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_BOUNDARY_PLAN.md` when checking the Phase R2 implemented minimal reader boundary.
3. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_OUTPUT_CONTRACT.md` when checking minimal reader output expectations.
4. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_VALIDATION_PLAN.md` when checking current standalone implementation validation coverage.
5. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_READER_HANDOFF_GATE.md` when checking why actual handoff remains closed after the minimal reader implementation.
6. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_PLAN.md` and `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_OUTPUT_CONTRACT.md` when checking the future mapping concept.
7. Read the three Phase R5 intake mapping implementation notes and run or inspect `validation/kernel_intake_mapping_contract_checks.py` when debugging the standalone mapper helper.
8. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_INTAKE_MAPPING_RUNTIME_INVOCATION_GATE.md` when checking why runtime invocation remains closed and why runtime invocation preparation is the selected next phase.
9. Read the three Phase R8 runtime invocation implementation notes and run or inspect `validation/kernel_runtime_invocation_contract_checks.py` when debugging the standalone invocation helper.
10. Read the three Phase R10 response validation implementation notes and run or inspect `validation/kernel_response_validation_contract_checks.py` when debugging the standalone response validation helper.
11. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_RESPONSE_VALIDATION_WRITER_GATE.md` before proposing response/failure writer preparation.
12. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_PLAN.md` and `docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md` when checking future writer expectations and blocked writer behavior.
13. Run or inspect `validation/kernel_runtime_envelope_reader_contract_checks.py` when debugging the standalone reader helper. It is not part of the main wrapper.
14. Read `docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_GATE.md` when checking why the reader helper remains standalone and what future wrapper inclusion would require.
15. Read `docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_REASSESSMENT.md` when checking the TASK 114 next-milestone decision to keep the reader helper outside the main wrapper.
16. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_GATE.md` when checking the current partial gate state for reader, mapper, candidate-only invocation, and local response validation only.
17. Read `docs/KERNEL_VALIDATION_BASELINE.md` for the current milestone snapshot that records the reassessment decision, Phase R2 reader implementation, post-reader handoff gate, Phase R5 mapper implementation, Phase R6 runtime invocation gate refresh, Phase R8 candidate-only invocation implementation, Phase R10 response validation implementation, and Phase R11 writer gate.
18. Read `docs/KERNEL_VALIDATION_WRAPPER_SCAFFOLD_OUTPUT_CONTRACT.md`.
19. Read `docs/KERNEL_VALIDATION_WRAPPER_FAILURE_PATH_OUTPUT_CONTRACT.md`.
20. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_VALIDATION_OUTPUT_CONTRACT.md` when checking first-slice adapter fixture validation.
21. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_HELPER_COVERAGE.md` to confirm whether a new helper is needed.
22. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_SEQUENCE.md` when checking future runtime adapter implementation order.
23. Read the specific standalone helper contract only when debugging that helper.

For planning or governance review:

1. Read `docs/KERNEL_VALIDATION_BASELINE.md`.
2. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_FIXTURE_PLAN.md` for the first-slice adapter fixture strategy when adapter fixture validation is in scope.
3. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_SEQUENCE.md` when future runtime adapter implementation order is in scope.
4. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md` when the runtime reader boundary is in scope.
5. Read the three Phase R2 runtime reader implementation notes before proposing reader expansion or the next boundary.
6. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_READER_HANDOFF_GATE.md` before opening any post-reader boundary.
7. Read `docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_GATE.md` before proposing wrapper inclusion for the standalone reader helper.
8. Read `docs/KERNEL_VALIDATION_WRAPPER_RUNTIME_READER_HELPER_INCLUSION_REASSESSMENT.md` before changing the next-milestone standalone decision.
9. Read `docs/KERNEL_VALIDATION_BASELINE.md` to confirm the current baseline status and blocked behavior surface.
10. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_PLAN.md` when envelope-to-P0/P1 intake mapping is in scope.
11. Read the three Phase R5 intake mapping implementation notes before proposing runtime invocation.
12. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_INTAKE_MAPPING_RUNTIME_INVOCATION_GATE.md` before opening runtime invocation preparation.
13. Read the three Phase R8 runtime invocation implementation notes before proposing response validation or writer work.
14. Read the three Phase R10 response validation implementation notes before proposing writer work.
15. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_POST_RESPONSE_VALIDATION_WRITER_GATE.md` before selecting writer preparation.
16. Read `docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_PLAN.md` when response/failure writer boundaries are in scope.
17. Read the relevant plan or reassessment note.
18. Compare proposed changes against the related output contract drift rules.
19. Treat runtime behavior, CI, fetching, scheduler, reporting, package migration, and handoff execution as out of scope unless a new governed pass explicitly changes that boundary.

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

Run the standalone runtime envelope reader contract helper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\kernel_runtime_envelope_reader_contract_checks.py'
```

Expected final success signal:

```text
kernel-runtime-envelope-reader-contract-checks-ok
```

This helper is intentionally not included in `validation/run_all_kernel_local_checks.py` for the next milestone.

Run the standalone intake mapping contract helper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\kernel_intake_mapping_contract_checks.py'
```

Expected final success signal:

```text
kernel-intake-mapping-contract-checks-ok
```

This helper is intentionally not included in `validation/run_all_kernel_local_checks.py`.

Run the standalone runtime invocation contract helper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\kernel_runtime_invocation_contract_checks.py'
```

Expected final success signal:

```text
kernel-runtime-invocation-contract-checks-ok
```

This helper is intentionally not included in `validation/run_all_kernel_local_checks.py`.

Run the standalone response validation contract helper from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'ai-meta-kernel\validation\kernel_response_validation_contract_checks.py'
```

Expected final success signal:

```text
kernel-response-validation-contract-checks-ok
```

This helper is intentionally not included in `validation/run_all_kernel_local_checks.py`.

The wrapper final success signal `kernel-local-validation-checks-ok` does not include runtime reader, intake mapping, runtime invocation, or response validation helper coverage at the current milestone.

## Explicit Non-Goals

This documentation index must not silently introduce:

- runtime adapter invocation beyond the minimal candidate-only invocation;
- real P0-P10 runtime invocation;
- canonical task object generation from envelopes;
- P0/P1 intake preparation beyond context-only mapping;
- response artifact writing;
- failure artifact writing;
- response writer implementation;
- failure writer implementation;
- intake mapping beyond the minimal context-only mapper;
- treating Phase R5 context mapping as P0/P1 execution or runtime handoff authorization;
- treating the post-intake mapping runtime invocation gate as runtime invocation implementation authorization;
- treating Phase R8 candidate-only invocation as terminal response validation or writer authorization;
- treating Phase R10 local response validation as terminal schema validation or writer authorization;
- treating the Phase R11 writer gate as writer implementation authorization;
- terminal response validation as writer behavior;
- P0/P1 execution;
- runtime envelope reader expansion beyond one explicit local file;
- treating Phase R2 minimal reader implementation as intake mapping or runtime handoff authorization;
- treating the post-reader handoff gate as actual handoff authorization;
- adding the runtime envelope reader helper to the main wrapper;
- changing the runtime reader wrapper inclusion gate decision;
- changing the TASK 114 runtime reader wrapper-inclusion reassessment decision;
- treating `kernel-runtime-envelope-reader-contract-checks-ok` as part of `kernel-local-validation-checks-ok`;
- wrapper behavior changes;
- runtime directory scanning;
- artifact queue discovery;
- runtime artifact reads beyond the explicit-file reader or writes;
- live fetching;
- scheduler runtime;
- report composition;
- CI behavior;
- package migration;
- external service calls;
- validation auto-repair;
- repository structure redesign.

## Recommended Next Phase

Implement a `Kernel-Side Terminal Writer Preparation Pass`.

That pass should prepare response writer and blocking failure writer boundaries together, because they share terminal-artifact mutual exclusivity. It must not implement writers, CLI, scheduler behavior, live fetching, report composition, CI, package migration, external service calls, or actual handoff execution.
