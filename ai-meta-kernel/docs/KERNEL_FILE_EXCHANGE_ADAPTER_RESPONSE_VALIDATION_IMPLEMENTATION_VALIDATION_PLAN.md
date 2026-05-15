# Kernel File Exchange Adapter Response Validation Implementation Validation Plan

## Purpose

This note records the validation coverage for the Phase R10 minimal response validation implementation slice.

It is a developer-facing validation plan for the implemented local validator. It does not add wrapper behavior, modify `meta-layer/TASK_OBJECT_SCHEMA.json`, write response artifacts, write failure artifacts, add CLI behavior, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Validation Plan Decision

Current Phase R10 validation decision:

```text
validate_current_candidate_response_as_local_pre_writer_output
```

Validation must prove that response validation accepts only one current R8 candidate response object, returns only one local validated pre-writer response object, and stops before all writer boundaries.

## Success Path Checks

The standalone helper validates:

- valid candidate response from `invoke_kernel_runtime()` produces one locally validated response object;
- validated output remains pre-writer and non-terminal;
- validated output contains no written response artifact path;
- validated output contains no written failure artifact path;
- validated output contains no report eligibility signal;
- validated output contains no macro-side report unlock;
- the source candidate is preserved as an isolated copy;
- the helper reports `kernel-response-validation-contract-checks-ok`.

## Failure Path Checks

The standalone helper rejects:

- non-object input;
- malformed candidate response;
- terminal response artifact input;
- terminal failure artifact input;
- candidate response with response artifact path fields;
- candidate response with failure artifact path fields;
- candidate response with `terminal_artifact_written == True`;
- candidate response with `response_writer_called == True`;
- candidate response with `failure_writer_called == True`;
- candidate response with `macro_report_unlock == True`;
- candidate response with CLI success, report eligibility, external service, or written artifact fields.

Failure remains local and explicit before a failure writer exists. It does not write response or failure artifacts.

## Current Response-State Expectations

R10 validates the current candidate-only state, not terminal `TASK_OBJECT_SCHEMA` output.

At minimum, the implemented validator preserves:

- candidate type is `kernel_runtime_candidate_response`;
- candidate state is `pre_writer_non_terminal`;
- invocation stage is `kernel_runtime_invocation_candidate_only`;
- writer-called markers are false;
- macro report unlock remains false;
- current context fields remain present and object/list/string shaped as required.

If a future candidate becomes canonical-task-object-shaped, schema and response-state validation must be governed separately before any writer can run.

## Stop-Before-Writer Guarantee

Validation proves this boundary:

```text
candidate kernel response object
-> response validation
-> local validated pre-writer response object
-> stop
```

It also proves:

- no artifact writing;
- no response writer calls;
- no failure writer calls;
- no CLI behavior;
- no macro-side report unlock;
- no queue discovery, polling, watcher behavior, retry, backoff, or cleanup.

## Relationship To Existing Helpers

The response validation helper is standalone:

```text
validation/kernel_response_validation_contract_checks.py
```

Existing helpers remain unchanged:

```text
validation/kernel_runtime_envelope_reader_contract_checks.py
validation/kernel_intake_mapping_contract_checks.py
validation/kernel_runtime_invocation_contract_checks.py
validation/run_all_kernel_local_checks.py
```

R10 does not add the response validation helper to the wrapper and does not change `kernel-local-validation-checks-ok`.

## Blocked In This Plan

This validation plan does not add:

- terminal `TASK_OBJECT_SCHEMA` response validation;
- response artifact writing;
- failure artifact writing;
- terminal artifact generation;
- CLI behavior;
- macro report unlock;
- queue discovery, polling, retry, cleanup, scheduler behavior, report composition, CI, package migration, or external service calls.
