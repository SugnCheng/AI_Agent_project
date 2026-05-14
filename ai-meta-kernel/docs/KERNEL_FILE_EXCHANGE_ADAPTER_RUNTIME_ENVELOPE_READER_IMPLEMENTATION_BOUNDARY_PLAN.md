# Kernel File Exchange Adapter Runtime Envelope Reader Implementation Boundary Plan

## Purpose

This note defines the smallest acceptable runtime envelope reader implementation boundary for `ai-meta-kernel`.

This note now records the Phase R2 minimal reader implementation boundary. It does not modify `validation/run_all_kernel_local_checks.py`, add wrapper inclusion, prepare intake, invoke kernel runtime, write artifacts, add CLI behavior, or change kernel contracts.

## Planning Decision

Current Phase R2 boundary decision:

```text
minimal_explicit_local_runtime_envelope_reader_slice_implemented
```

The implemented slice turns the governed reader boundary into the smallest local implementation surface. It still stops before intake mapping and runtime invocation.

## Intended Input Boundary

The reader may accept exactly one explicit local file path for one kernel input envelope artifact.

The future reader must not accept:

- runtime directories as primary input;
- queue discovery;
- polling or watcher behavior;
- multiple envelopes per invocation;
- response artifacts;
- failure artifacts;
- remote URLs;
- macro-generated canonical task objects.

## Intended Output Boundary

The reader returns one parsed and validated `kernel_input_envelope` object.

The future reader output must not be:

- `kernel_intake_context`;
- a canonical task object;
- a kernel response artifact;
- a kernel failure artifact;
- a runtime result;
- a reporting unlock.

## Validation Responsibilities

The implementation must preserve the current reader guardrails:

- explicit local path exists;
- path is a file, not a directory;
- content is valid JSON;
- parsed JSON is an object;
- object is a `kernel_input_envelope`;
- required envelope fields are present;
- response and failure artifacts are rejected;
- canonical task object top-level fields are rejected;
- output stops before intake mapping.

## Failure Behavior

Reader failures must be local, explicit, and fail-closed.

On failure, the future reader must not:

- repair malformed JSON;
- synthesize missing envelope fields;
- continue into intake mapping;
- invoke P0/P1 or P0-P10 runtime;
- write response artifacts;
- write failure artifacts;
- unlock macro-side reporting.

Future conversion of reader failures into blocking failure artifacts remains a separate writer-boundary implementation concern.

## Stop-Before-Intake Boundary

The future reader implementation must stop here:

```text
one explicit local envelope path
-> parsed and reader-validated kernel_input_envelope object
-> stop
```

It must not continue into:

- `kernel_intake_context` construction;
- P0/P1 intake preparation;
- P0/P1 execution;
- P0-P10 runtime invocation;
- response validation;
- response writing;
- failure writing;
- CLI orchestration;
- macro-side reporting.

## Relationship To Existing Standalone Helper

The existing standalone helper remains:

```text
validation/kernel_runtime_envelope_reader_contract_checks.py
```

Its current success signal remains:

```text
kernel-runtime-envelope-reader-contract-checks-ok
```

The helper remains outside:

```text
validation/run_all_kernel_local_checks.py
```

The Phase R2 implementation is validated by this helper. Wrapper inclusion remains separately governed.

## Files Requiring Refresh If Implementation Opens Later

A later reader behavior broadening pass must refresh at minimum:

- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_OUTPUT_CONTRACT.md`
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_VALIDATION_PLAN.md`
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_GATE.md`
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_SEQUENCE.md`
- `docs/KERNEL_VALIDATION_BASELINE.md`
- `docs/KERNEL_VALIDATION_DOCUMENTATION_INDEX.md`
- `CROSS_PROJECT_INTEGRATION_STATUS.md`

If wrapper inclusion is proposed, that pass must also refresh wrapper output and failure-path governance before changing `validation/run_all_kernel_local_checks.py`.

## Behaviors That Remain Blocked

Phase R2 does not open:

- reader behavior beyond one explicit local envelope path;
- wrapper inclusion;
- intake mapping;
- P0/P1 or P0-P10 invocation;
- canonical task object generation;
- response or failure artifact writing;
- CLI behavior;
- queue discovery, polling, retry, watcher, or cleanup behavior;
- live fetching, scheduler runtime, report composition, CI, package migration, or external service calls.
