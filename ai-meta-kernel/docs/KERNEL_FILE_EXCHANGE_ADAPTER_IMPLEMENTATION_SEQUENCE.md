# Kernel File Exchange Adapter Implementation Sequence

## Purpose

This note defines the intended future implementation order for the kernel-side file exchange adapter runtime path in `ai-meta-kernel`.

It is a developer-facing sequencing note only. It does not add runtime code, modify kernel contracts, invoke kernel runtime, write response artifacts, write failure artifacts, add CLI behavior, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Sequencing Decision

Current sequencing decision:

```text
implement_runtime_adapter_in_governed_pre_runtime_to_writer_order
```

The adapter should advance only through small governed passes. Each step must preserve the current kernel ownership boundary: the macro agent may provide evidence/context envelopes, but `ai-meta-kernel` owns intake interpretation, runtime reasoning, canonical task object production, response validation, and terminal artifact writing.

Phase R2 has implemented the first minimal reader slice for one explicit local input path. Phase R5 has implemented the minimal context-only envelope-to-intake mapping slice. Phase R6 refreshes the runtime invocation gate after that mapping slice. Phase R7 prepared the future runtime invocation implementation boundary. Phase R8 implements the minimal candidate-only runtime invocation slice. Phase R9 prepared the response validation boundary. Phase R10 implements the minimal local candidate-response validation slice. This does not open response/failure writers, CLI behavior, macro reporting, or actual handoff.

## Intended Implementation Order

The future implementation order should be:

1. Runtime envelope reader boundary.
2. Envelope-to-intake mapping boundary.
3. Kernel runtime invocation boundary.
4. Kernel response validation boundary.
5. Response writer boundary.
6. Blocking failure writer boundary.
7. Local invocation boundary.
8. Runtime artifact retention and cleanup policy.

This order is intentionally narrow. It prevents writer behavior, CLI behavior, scheduler behavior, reporting behavior, and cleanup automation from arriving before the kernel can locally validate the inputs and outputs it owns.

## Step 1: Runtime Envelope Reader Boundary

Purpose:

- read exactly one local kernel input envelope artifact from a governed path or explicitly provided file;
- parse JSON deterministically;
- validate that the object is a `kernel_input_envelope`;
- stop before intake mapping.

Current status:

```text
minimal_explicit_file_reader_implemented_and_validated
```

Depends on:

- `KERNEL_FILE_EXCHANGE_ADAPTER_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_VALIDATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_BOUNDARY_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_VALIDATION_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_POST_READER_HANDOFF_GATE.md`;
- existing static fixture validation and adapter scaffold checks.

Must still not include:

- runtime queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- intake mapping;
- P0/P1 or P0-P10 invocation;
- response or failure writing;
- CLI behavior unless opened by a separate governed pass.

Additional governed pass required:

- a separate governed pass before reader behavior is broadened beyond one explicit local file.

## Step 2: Envelope-To-Intake Mapping Boundary

Purpose:

- convert one validated envelope into a kernel-owned `kernel_intake_context`;
- carry only allowed evidence, provenance, operator request, expectation, and deferred-behavior context;
- stop before P0/P1 execution.

Current status:

```text
minimal_context_only_intake_mapping_implemented_and_validated
```

Depends on:

- runtime envelope reader boundary;
- `KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_BOUNDARY_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_VALIDATION_PLAN.md`;
- envelope guardrails that exclude canonical task object top-level fields.
- `validation/kernel_intake_mapping_contract_checks.py`.

Must still not include:

- canonical task object generation;
- task classification conclusions;
- risk profile conclusions;
- status flags;
- handoff decisions;
- response state classification;
- P0/P1 or P0-P10 execution;
- response or failure writing.

Additional governed pass required:

- a governed pass before mapping output is broadened beyond context-only `kernel_intake_context`.
- any future code change must still prove context-only output or explicitly govern the next boundary before P0/P1 execution.

## Step 3: Kernel Runtime Invocation Boundary

Purpose:

- pass a validated `kernel_intake_context` into a kernel-owned runtime entrypoint;
- preserve `ai-meta-kernel` as the only owner of P0-P10 reasoning and canonical task object production;
- return a candidate kernel response object for validation.

Depends on:

- intake mapping implementation;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_BOUNDARY_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_VALIDATION_PLAN.md`;
- a defined kernel-owned P0/P1 or P0-P10 invocation entrypoint;
- unchanged canonical kernel contracts.

Current status:

```text
minimal_candidate_only_runtime_invocation_implemented_and_validated
```

Must still not include:

- macro-side reasoning substitution;
- schema repair after runtime output;
- terminal response validation;
- response artifact writing;
- failure artifact writing;
- scheduler execution;
- report composition;
- external service calls.

Additional governed pass required:

- a post-response-validation writer gate before any validated local response is treated as writer-ready or passed to writers.

## Step 4: Kernel Response Validation Boundary

Purpose:

- validate the current candidate kernel response as a JSON object;
- validate the current candidate-only / pre-writer / non-terminal response markers;
- return one local validated response object before any terminal artifact is written.

Depends on:

- kernel runtime invocation boundary;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_BOUNDARY_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_VALIDATION_PLAN.md`;
- `TASK_OBJECT_SCHEMA.json`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md`.

Current status:

```text
minimal_local_response_validation_implemented_and_validated
```

Must still not include:

- response artifact writing before validation passes;
- terminal `TASK_OBJECT_SCHEMA` response validation for the current non-canonical candidate;
- partial task object repair;
- silent field renaming;
- failure artifact writing without governed failure semantics;
- macro-side response production.

Additional governed pass required:

- a post-response-validation writer gate or response writer preparation pass before any validated local response is passed to writers.

## Step 5: Response Writer Boundary

Purpose:

- write exactly one successful kernel response artifact after response validation passes;
- preserve the governed response filename pattern;
- keep canonical kernel task object fields unchanged.

Depends on:

- response validation boundary;
- `KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md`;
- governed artifact path and naming rules.

Must still not include:

- writing invalid or partial task objects;
- writing both response and failure artifacts for the same invocation;
- artifact polling or watcher behavior;
- cleanup automation;
- report composition;
- macro-side response writing.

Additional governed pass required:

- a response writer implementation pass with validation coverage for naming, schema validation, and mutual exclusivity.

## Step 6: Blocking Failure Writer Boundary

Purpose:

- write exactly one blocking failure artifact when a valid response artifact cannot be produced;
- preserve governed failure stages;
- ensure failures do not unlock downstream reporting.

Depends on:

- runtime reader, intake mapping, invocation, response validation, and response writer failure points being explicitly classified;
- `KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md`.

Must still not include:

- non-blocking failure artifacts;
- partial canonical task object content in failure artifacts;
- both response and failure artifacts for one invocation;
- hidden continuation after terminal failure;
- report unlock behavior.

Additional governed pass required:

- a blocking failure writer implementation pass with validation coverage for required fields, failure stages, blocking semantics, and mutual exclusivity.

## Step 7: Local Invocation Boundary

Purpose:

- define how a developer invokes one local adapter run once reader, mapping, runtime invocation, response validation, and writers are implemented;
- keep invocation local, explicit, and deterministic.

Depends on:

- implemented and validated runtime reader;
- implemented and validated intake mapping;
- implemented and validated runtime invocation;
- implemented and validated response/failure terminal artifact behavior.

Must still not include:

- scheduler runtime;
- live fetching;
- report composition;
- CI behavior;
- multi-profile automation;
- open-ended runtime directory scanning unless separately governed.

Additional governed pass required:

- a local invocation or CLI output contract before any command boundary is added.

## Step 8: Runtime Artifact Retention And Cleanup Policy

Purpose:

- decide when generated runtime artifacts are retained, cleaned up, or promoted into reviewed fixtures;
- keep generated runtime material distinct from committed static fixtures.

Depends on:

- local invocation boundary;
- terminal artifact writer behavior;
- human review expectations for restricted, blocked, failed, missing, or ambiguous states.

Must still not include:

- automatic fixture promotion;
- archive/export automation;
- scheduler cleanup;
- CI cleanup;
- report unlock behavior.

Additional governed pass required:

- an artifact retention, cleanup, and fixture promotion policy before automation touches generated runtime artifacts.

## Blocked Behaviors Across All Steps

No step in this sequence may silently introduce:

- runtime reader behavior beyond one explicit local file before a governed broadening pass opens;
- live fetching;
- uncontrolled open-web crawling;
- scheduler runtime;
- report composition;
- archive/export automation;
- CI behavior;
- package migration;
- external service calls;
- source governance changes;
- kernel contract modifications;
- schema drift;
- macro-side canonical kernel task object generation;
- macro-side kernel response artifact writing;
- hidden runtime handoff.

## Recommended Next Phase

Implement a `Kernel-Side Post-Response-Validation Writer Gate Refresh Pass`.

That pass should record that minimal local response validation exists, confirm response/failure writers remain closed, and select the next governed writer-preparation or writer-implementation boundary. It must keep response/failure writers, CLI, scheduler behavior, live fetching, report composition, CI, package migration, external service calls, and actual handoff execution out of scope unless separately governed.
