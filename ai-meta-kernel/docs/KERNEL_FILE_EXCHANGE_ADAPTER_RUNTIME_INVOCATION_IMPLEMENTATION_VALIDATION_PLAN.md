# Kernel File Exchange Adapter Runtime Invocation Implementation Validation Plan

## Purpose

This note defines the validation coverage for the minimal runtime invocation implementation slice.

This validation plan is reflected by a standalone helper. It does not modify wrapper behavior, execute P0/P1, invoke the real P0-P10 runtime, generate canonical task objects from envelope evidence, validate runtime responses as runtime behavior, write response artifacts, write failure artifacts, add CLI behavior, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Validation Plan Decision

Current Phase R8 validation decision:

```text
minimal_runtime_invocation_validated_by_standalone_helper_and_stops_before_writers
```

Validation proves that invocation accepts only one validated `kernel_intake_context`, returns only a candidate kernel response object, and stops before all writer boundaries.

## Success Path Checks

The current standalone helper validates:

- one validated `kernel_intake_context` input from the current mapper;
- preservation of reader and mapper boundaries;
- invocation through a kernel-owned boundary only;
- candidate response object returned as a JSON object;
- candidate response marked as pre-writer or otherwise kept outside terminal artifact scope;
- no response artifact written;
- no failure artifact written;
- no CLI success signal emitted;
- no macro-side report unlock.

## Failure Path Checks

The current standalone helper rejects:

- non-object input;
- malformed intake context;
- intake context missing required context-only fields;
- `mapping_stage` values other than `kernel_intake_context_pre_runtime` unless separately governed;
- raw `kernel_input_envelope` input;
- canonical task object passed as intake input;
- response artifact input;
- failure artifact input;
- macro-generated kernel conclusions.

Failure remains local and explicit before a failure writer exists. It must not write response or failure artifacts.

## Candidate Response Validation Expectations

Validation confirms that candidate responses are treated as candidates only.

Before any writer phase, separate governed response validation must check:

- JSON object shape;
- `meta-layer/TASK_OBJECT_SCHEMA.json` compliance;
- response-state and handoff semantics;
- no schema repair;
- no silent field renaming;
- no writer-side inference of kernel conclusions.

This plan does not add response validation behavior in Phase R8.

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

The current invocation helper is:

```text
validation/kernel_runtime_invocation_contract_checks.py
```

Current success signal:

```text
kernel-runtime-invocation-contract-checks-ok
```

The helper remains standalone and is not included in `validation/run_all_kernel_local_checks.py`.

## Blocked In This Plan

This validation plan does not add:

- runtime invocation beyond the minimal candidate-only implementation;
- P0/P1 execution;
- P0-P10 runtime invocation;
- canonical task object generation from envelope evidence;
- response validation as runtime behavior;
- response/failure writers;
- CLI behavior;
- queue discovery, polling, retry, cleanup, scheduler behavior, report composition, CI, package migration, or external service calls.
