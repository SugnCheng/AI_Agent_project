# Kernel File Exchange Adapter Scaffold Plan

## Purpose

This document defines the smallest governed plan for a future kernel-side file exchange adapter scaffold.

It translates the existing adapter plan and adapter contract into a scaffold-ready boundary for future reader, intake validation, response writer, and failure writer stubs.

This is a planning document only. It does not add adapter scaffold code, runtime invocation, file readers, file writers, schema validation implementation, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or changes to kernel contracts.

## Authority

Canonical kernel contracts remain:

- `META_LAYER_MASTER_SPEC.md`
- `meta-layer/RUNTIME_PIPELINE.md`
- `meta-layer/HANDOFF_CONTRACT.md`
- `meta-layer/TASK_OBJECT_SCHEMA.json`

This plan must remain compatible with:

- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_PLAN.md`
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_CONTRACT.md`
- `docs/KERNEL_VALIDATION_WRAPPER_PLAN.md`
- `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_OUTPUT_CONTRACT.md`
- `../macro-financial-intelligence-agent/FILE_BASED_KERNEL_EXCHANGE_CONTRACT.md`

If this plan conflicts with canonical kernel contracts, the canonical kernel contracts win.

## Current Decision

A future scaffold may define local boundary functions or objects for the file exchange adapter, but it must not implement actual kernel runtime handoff yet.

The scaffold should make the future integration boundary explicit while preserving the current blocked state:

```text
kernel input envelope artifact
-> reader stub
-> intake validation stub
-> kernel intake preparation stub
-> runtime invocation boundary placeholder
-> response writer stub OR failure writer stub
```

The scaffold must remain a boundary around the kernel. It must not become a second reasoning layer, a partial kernel runtime, or a shortcut around P0-P10.

## Smallest Future Adapter Scaffold Boundary

The smallest acceptable future scaffold boundary is:

| Boundary element | Future responsibility | v0.1 scaffold behavior |
| --- | --- | --- |
| `read_envelope_artifact(path)` | Read and parse one envelope artifact path. | May parse local JSON and return object-like envelope data, or remain a stub if the implementation pass chooses stricter no-read behavior. |
| `validate_envelope_intake(envelope)` | Apply envelope guardrails before kernel intake. | Should validate shape and guardrails only; must not create a canonical task object. |
| `prepare_kernel_intake(envelope)` | Prepare a kernel-owned context-only intake input from the envelope. | Returns the Phase R5 minimal `kernel_intake_context` and stops before P0/P1 execution and P0-P10 runtime invocation. |
| `invoke_kernel_runtime(kernel_intake)` | Produce the current candidate-only pre-writer invocation output from validated intake. | Returns the Phase R8 minimal candidate response object and stops before terminal response validation and writers. |
| `validate_kernel_response(task_object)` | Check a kernel-produced response before artifact writing. | May be a future schema-validation boundary; must not fabricate task objects. |
| `write_response_artifact(task_object, destination)` | Write a schema-valid canonical response artifact. | Must remain unimplemented or placeholder-only until response writing is explicitly approved. |
| `write_failure_artifact(failure, destination)` | Write a blocking kernel exchange failure artifact. | Must remain unimplemented or placeholder-only until failure writing is explicitly approved. |

## Reader Stub Responsibility

The future reader stub should accept exactly one envelope artifact path.

Minimum responsibilities:

1. Confirm the path points to a file.
2. Parse JSON.
3. Confirm the parsed artifact is object-like.
4. Confirm the artifact is a kernel input envelope.
5. Reject response artifacts and failure artifacts.
6. Preserve the original envelope object for later P0/P1 intake context.

The reader stub must not:

- fetch external sources;
- discover artifacts by polling;
- mutate envelope, response, or failure artifacts;
- infer macro-financial facts outside the envelope;
- generate a canonical kernel task object;
- invoke P0-P10;
- compose macro reports.

## Intake Validation Stub Responsibility

The future intake validation stub should enforce envelope guardrails before any kernel runtime invocation is attempted.

Minimum responsibilities:

1. Check required envelope fields:
   - `envelope_type`
   - `envelope_version`
   - `source_project`
   - `profile_id`
   - `run_mode`
   - `report_target`
   - `regions`
   - `operator_intent`
   - `evidence_bundle`
   - `evidence_context`
   - `kernel_task_object_expectation`
   - `deferred_runtime_behavior`
2. Confirm the envelope is evidence/context only.
3. Reject envelopes that include completed top-level canonical task object conclusions.
4. Confirm `operator_intent` is present and non-empty.
5. Preserve `evidence_bundle` and `evidence_context` as source context, not as kernel conclusions.

The intake validation stub must not:

- populate `framed_objective`;
- populate `task_classification`;
- populate `risk_profile`;
- populate `triggered_habits`;
- populate `structural_decomposition`;
- populate `required_checks`;
- populate `status_flags`;
- populate `downstream_recommendation`;
- populate `handoff`;
- downgrade kernel-owned reasoning into macro-provided assumptions.

## Response Writer Stub Responsibility

The future response writer stub should write a response artifact only after the kernel has produced a canonical task object.

Minimum responsibilities:

1. Accept only a kernel-produced task object.
2. Validate the task object against `meta-layer/TASK_OBJECT_SCHEMA.json` before writing.
3. Preserve canonical field names.
4. Use the governed response artifact naming convention:

```text
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__kernel_response.json
```

5. Refuse to write if schema validation fails.

The response writer stub must not:

- fabricate a task object from the envelope;
- patch missing canonical fields;
- write partial responses;
- hide verification gaps, restrictions, reframe needs, or blocked states;
- unlock downstream macro reporting by itself.

## Failure Writer Stub Responsibility

The future failure writer stub should write a blocking failure artifact when no valid response artifact can be produced.

Minimum responsibilities:

1. Produce a failure artifact with `artifact_type == "kernel_exchange_failure"`.
2. Use `artifact_version == "0.1.0"` unless a governed pass changes the exchange contract.
3. Use `source_project == "ai-meta-kernel"`.
4. Preserve profile context where available:
   - `profile_id`
   - `run_mode`
   - `report_target`
   - `regions`
   - `envelope_artifact_path`
5. Use one of the governed failure stages:
   - `pre_invoke`
   - `invoke`
   - `response_parse`
   - `response_schema_validation`
   - `response_state_validation`
6. Set `blocking` to `true`.

The failure writer stub must not:

- include partial canonical task objects;
- unlock downstream reporting;
- mark a failure as non-blocking in v0.1;
- suppress failure reasons needed for operator review.

## Placeholder And NotImplementedError Rules

The scaffold may use placeholders or `NotImplementedError` for boundaries that are intentionally not implemented.

Allowed placeholder areas:

- real kernel runtime invocation;
- response artifact writing;
- failure artifact writing;
- generalized multi-profile routing;
- artifact cleanup;
- retry or backoff behavior;
- wrapper inclusion.

Required placeholder behavior:

1. The placeholder must fail closed.
2. The placeholder must make the blocked behavior explicit.
3. The placeholder must not return fabricated success.
4. The placeholder must not generate canonical task objects locally from envelopes.
5. The placeholder must not silently write runtime artifacts.

The most important future placeholder is:

```text
invoke_kernel_runtime(kernel_intake) -> candidate-only response object
```

until a governed runtime implementation pass explicitly replaces it.

## Explicitly Blocked Until Future Implementation Pass

The following remain blocked:

- actual kernel runtime handoff;
- P0-P10 runtime invocation;
- canonical task object generation from an envelope;
- response artifact writing;
- failure artifact writing;
- runtime artifact polling or discovery;
- retry/backoff behavior;
- artifact cleanup automation;
- file exchange CLI command design;
- integration with a broader kernel validation wrapper;
- package layout changes;
- CI integration;
- live fetching;
- scheduler runtime;
- report composition;
- external service calls;
- generic multi-profile production exchange.

## Scaffold Drift Rules

The following changes require a governed pass before scaffold implementation:

- changing the adapter boundary;
- allowing more than one input envelope per scaffold invocation;
- changing required envelope fields;
- changing response artifact naming semantics;
- changing failure artifact shape or failure stages;
- allowing `blocking == false` for failure artifacts;
- allowing macro-side generated canonical task objects;
- allowing response writing without schema validation;
- broadening candidate-only invocation into real runtime invocation;
- adding runtime artifact polling, cleanup, retries, or watchers;
- broadening from `daily_us_core` fixture-safe behavior to generic production exchange.

## Recommended Future Scaffold Shape

A future scaffold implementation pass may create a local kernel-side module with narrow functions similar to:

```text
read_envelope_artifact(path)
validate_envelope_intake(envelope)
prepare_kernel_intake(envelope)
invoke_kernel_runtime(kernel_intake)
validate_kernel_response(task_object)
write_response_artifact(task_object, destination)
write_failure_artifact(failure, destination)
```

The exact code path should be decided in the implementation pass. That pass should not also implement runtime invocation.

## Recommended Next Phase

Implement a `Kernel-Side File Exchange Adapter Scaffold Creation Pass`.

That pass should add only local boundary stubs and fail-closed placeholders. It should not invoke the kernel runtime, generate canonical task objects from envelopes, or write response/failure artifacts unless a separate governed pass explicitly authorizes those behaviors.
