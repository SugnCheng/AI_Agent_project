# Kernel File Exchange Adapter Runtime Invocation Implementation Output Contract

## Purpose

This document snapshots the output contract for the implemented minimal runtime invocation slice.

It is a developer-facing implementation contract. It does not authorize runtime invocation beyond the candidate-only slice, modify kernel contracts, execute P0/P1, invoke the real P0-P10 runtime, generate canonical task objects from envelope evidence, validate runtime responses as runtime behavior, write response artifacts, write failure artifacts, add CLI behavior, broaden reader behavior, broaden intake mapping, change wrapper behavior, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, call external services, or implement actual runtime handoff.

## Contract Decision

Current Phase R8 implementation output contract decision:

```text
minimal_runtime_invocation_returns_candidate_response_only
```

The minimal invocation implementation outputs one candidate kernel response object from one validated `kernel_intake_context`. The candidate remains pre-writer and pre-terminal-artifact.

## Allowed Future Output

The current output is:

```text
one_candidate_kernel_response_object
```

The current candidate is not canonical-task-object-shaped and is not a terminal kernel response. It must later pass `meta-layer/TASK_OBJECT_SCHEMA.json` validation and response-state validation before any writer can run.

The candidate output remains in local return value scope. It must not be treated as a durable response artifact until the response writer boundary is separately implemented.

## Outputs That Remain Prohibited

The invocation output must not be:

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

## Candidate Response Validation Expectations

Before any response writer can run in a later phase, the candidate response must be validated as:

- JSON object;
- schema-valid against `meta-layer/TASK_OBJECT_SCHEMA.json`;
- semantically compatible with governed response states and handoff expectations;
- free of writer-side repair or silent field renaming.

This output contract does not implement that validation. It records that validation is mandatory before any future write.

## Failure Behavior

Invocation failure must fail closed.

At the invocation slice, failure remains local and explicit. It must not write artifacts in the invocation slice.

The failure writer remains a separate future boundary. A failed invocation must not silently emit a failure artifact, response artifact, report unlock, CLI success signal, or downstream macro reporting signal.

## Stop Boundary

The invocation output contract stops at:

```text
candidate kernel response object
```

It does not authorize:

- response validation as runtime behavior;
- response artifact writing;
- failure artifact writing;
- CLI behavior;
- actual runtime handoff;
- macro-side reporting.

## Governed Change Triggers

The following require a governed pass before implementation:

- changing invocation input beyond one validated `kernel_intake_context`;
- allowing raw envelopes as invocation input;
- allowing macro-provided canonical task objects as invocation input;
- changing invocation output from candidate object to written artifact;
- allowing invocation failure to write failure artifacts;
- allowing candidate responses to skip schema validation before write;
- adding response validation behavior;
- adding response/failure writer behavior;
- adding CLI, queue discovery, polling, retry, cleanup, scheduler behavior, live fetching, report composition, CI, package migration, or external service calls.

## Explicit Non-Authorization

This contract authorizes only the implemented Phase R8 candidate-only invocation slice. It does not authorize terminal response validation, response/failure writers, CLI behavior, or actual runtime handoff.
