# Kernel File Exchange Adapter Runtime Invocation Implementation Validation Plan

## Purpose

This note defines the future validation coverage expected before a minimal runtime invocation implementation slice is opened.

It is a documentation-only validation plan. It does not create implementation tests, add helpers, modify wrapper behavior, implement runtime invocation, execute P0/P1, invoke P0-P10 runtime, generate canonical task objects from envelope evidence, validate runtime responses as runtime behavior, write response artifacts, write failure artifacts, add CLI behavior, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Validation Plan Decision

Current Phase R7 validation planning decision:

```text
plan_runtime_invocation_validation_before_implementation
```

Future validation must prove that invocation accepts only one validated `kernel_intake_context`, returns only a candidate kernel response object, and stops before all writer boundaries.

## Future Success Path Checks

Once invocation implementation is opened, validation should cover:

- one validated `kernel_intake_context` input from the current mapper;
- preservation of reader and mapper boundaries;
- invocation through a kernel-owned boundary only;
- candidate response object returned as a JSON object;
- candidate response marked as pre-writer or otherwise kept outside terminal artifact scope;
- no response artifact written;
- no failure artifact written;
- no CLI success signal emitted;
- no macro-side report unlock.

## Future Failure Path Checks

Future validation should reject:

- non-object input;
- malformed intake context;
- intake context missing required context-only fields;
- `mapping_stage` values other than `kernel_intake_context_pre_runtime` unless separately governed;
- raw `kernel_input_envelope` input;
- canonical task object passed as intake input;
- response artifact input;
- failure artifact input;
- macro-generated kernel conclusions.

Failure must remain local and explicit before a failure writer exists. It must not write response or failure artifacts.

## Candidate Response Validation Expectations

Future validation should confirm that candidate responses are treated as candidates only.

Before any writer phase, separate governed response validation must check:

- JSON object shape;
- `meta-layer/TASK_OBJECT_SCHEMA.json` compliance;
- response-state and handoff semantics;
- no schema repair;
- no silent field renaming;
- no writer-side inference of kernel conclusions.

This plan does not add response validation behavior in Phase R7.

## Stop-Before-Writer Guarantee

Validation must prove this boundary:

```text
kernel_intake_context
-> runtime invocation
-> candidate kernel response object
-> stop
```

It must also prove:

- no reader broadening;
- no mapper broadening;
- no artifact writing;
- no response writer calls;
- no failure writer calls;
- no CLI behavior;
- no macro-side report unlock;
- no queue discovery, polling, watcher behavior, retry, backoff, or cleanup.

## Relationship To Existing Helpers

Existing helpers remain unchanged:

```text
validation/kernel_runtime_envelope_reader_contract_checks.py
validation/kernel_intake_mapping_contract_checks.py
validation/run_all_kernel_local_checks.py
```

Phase R7 does not add a runtime invocation helper and does not add any standalone helper to the wrapper.

## Blocked In This Plan

This validation plan does not add:

- runtime invocation implementation;
- P0/P1 execution;
- P0-P10 runtime invocation;
- canonical task object generation from envelope evidence;
- response validation as runtime behavior;
- response/failure writers;
- CLI behavior;
- queue discovery, polling, retry, cleanup, scheduler behavior, report composition, CI, package migration, or external service calls.

