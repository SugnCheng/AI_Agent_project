# Kernel File Exchange Adapter Response Validation Implementation Output Contract

## Purpose

This document snapshots the output contract for the Phase R10 minimal response validation implementation slice.

It is a developer-facing implementation contract. It does not modify kernel contracts, modify `meta-layer/TASK_OBJECT_SCHEMA.json`, write response artifacts, write failure artifacts, add CLI behavior, broaden reader behavior, broaden intake mapping, broaden runtime invocation beyond candidate-only output, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, call external services, or implement actual runtime handoff.

## Contract Decision

Current Phase R10 output contract decision:

```text
current_candidate_response_validates_to_local_pre_writer_response_only
```

The implemented validator outputs one local validated response object from one current R8 candidate response object. The output remains pre-writer and pre-terminal-artifact.

The current candidate response is not canonical-task-object-shaped. R10 therefore validates the current candidate-only contract and does not claim `meta-layer/TASK_OBJECT_SCHEMA.json` success.

## Current Output

The implemented output is:

```text
one_local_validated_pre_writer_response_object
```

The output contains:

- `validated_response_type == "kernel_candidate_response_validation"`;
- `validated_response_state == "validated_pre_writer_non_terminal"`;
- `source_candidate` as an isolated copy of the validated candidate;
- `response_writer_allowed == False`;
- `failure_writer_allowed == False`;
- `macro_report_unlock == False`;
- `validation_stage == "candidate_response_validated_pre_writer"`.

The validated output remains in memory or local return value scope. It must not be treated as a durable response artifact until the response writer boundary is separately implemented.

If a future candidate response becomes canonical-task-object-shaped, a separate governed pass must define how `meta-layer/TASK_OBJECT_SCHEMA.json` validation applies before any writer can run.

## Outputs That Remain Prohibited

The validation output must not be:

- written response artifact;
- written failure artifact;
- response artifact path;
- failure artifact path;
- report eligibility signal;
- macro-side report unlock;
- CLI success signal;
- scheduler result;
- external-service result;
- artifact cleanup decision.

## Failure Behavior

Validation failure fails closed.

The validator rejects malformed candidates, terminal artifacts, artifact paths, writer-called markers, terminal-artifact-written markers, macro-report unlock markers, and forbidden terminal output fields. Failure remains local and explicit and must not write artifacts.

The failure writer remains a separate future boundary. A failed validation must not silently emit a failure artifact, response artifact, report unlock, CLI success signal, or downstream macro reporting signal.

## Stop Boundary

The response validation output contract stops at:

```text
local validated pre-writer response object
```

It does not authorize:

- response artifact writing;
- failure artifact writing;
- terminal canonical task object validation;
- CLI behavior;
- actual runtime handoff;
- macro-side reporting.

## Governed Change Triggers

The following require a governed pass before implementation:

- changing validation input beyond one current R8 candidate response object;
- accepting written artifacts as validation input;
- allowing macro-produced canonical task objects as validation input;
- changing validation output from local object to written artifact;
- treating the current candidate as `TASK_OBJECT_SCHEMA`-valid terminal output;
- allowing validation failure to write failure artifacts;
- allowing validation to repair missing kernel conclusions;
- changing `TASK_OBJECT_SCHEMA.json`;
- adding response/failure writer behavior;
- adding the standalone response validation helper to the main wrapper;
- adding CLI, queue discovery, polling, retry, cleanup, scheduler behavior, live fetching, report composition, CI, package migration, or external service calls.

## Explicit Non-Authorization

This contract authorizes only the Phase R10 local response validation slice. It does not authorize response/failure writers, terminal artifact generation, CLI behavior, macro report unlock, or actual runtime handoff.
