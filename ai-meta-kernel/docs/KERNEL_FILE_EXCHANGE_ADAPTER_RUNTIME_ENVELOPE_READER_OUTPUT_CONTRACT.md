# Kernel File Exchange Adapter Runtime Envelope Reader Output Contract

## Purpose

This document snapshots the future output contract for the kernel-side runtime envelope reader boundary.

It is a developer-facing contract note only. It does not add runtime code, modify kernel contracts, prepare kernel intake, invoke kernel runtime, generate canonical task objects, write response artifacts, write failure artifacts, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Contract Decision

Current runtime envelope reader output contract:

```text
future_reader_accepts_one_explicit_local_envelope_and_stops_before_intake_mapping
```

The future reader boundary may read exactly one explicitly provided local kernel input envelope artifact. It may perform reader-level file, JSON, object, and envelope guardrail checks. It must stop before envelope-to-intake mapping, P0/P1 execution, P0-P10 runtime invocation, response validation, response writing, or failure writing.

## Allowed Reader Input

The future reader may accept exactly one local file path that points to a kernel input envelope artifact.

Allowed input properties:

- explicit local path provided by the caller or a governed local invocation boundary;
- file exists;
- path resolves to a file, not a directory;
- file content is UTF-8 JSON;
- parsed JSON is a JSON object;
- object has `envelope_type == "kernel_input_envelope"`;
- object is not a kernel response artifact;
- object is not a kernel exchange failure artifact;
- object contains the required envelope fields from the adapter contract;
- object does not contain top-level canonical task object fields.

The reader must not accept:

- a runtime directory as the primary input;
- implicit queue discovery;
- multiple envelope artifacts in one invocation;
- response artifacts as envelope input;
- failure artifacts as envelope input;
- generated macro-side canonical task objects;
- remote URLs or external service inputs.

## Successful Reader Output

A successful reader output means:

```text
one_validated_kernel_input_envelope_object
```

The reader may return the parsed envelope object and adapter-local source path context needed by later governed steps.

The successful output must preserve:

- the original envelope content;
- `source_project`;
- `profile_id`;
- `run_mode`;
- `report_target`;
- `regions`;
- `operator_intent`;
- `evidence_bundle`;
- `evidence_context`;
- `kernel_task_object_expectation`;
- `deferred_runtime_behavior`.

The successful output must not add or populate canonical task object fields, including:

- `schema_version`;
- `task_id`;
- `raw_request`;
- `kernel_stage`;
- `framed_objective`;
- `task_classification`;
- `risk_profile`;
- `triggered_habits`;
- `structural_decomposition`;
- `required_checks`;
- `status_flags`;
- `verification_plan`;
- `challenge_loop`;
- `downstream_recommendation`;
- `handoff`.

The successful reader output is not a response artifact, failure artifact, canonical task object, intake context, runtime result, or reporting unlock.

## Failure Behavior

Reader failure must be local, explicit, and fail-closed.

The reader must fail if:

- no input path is provided;
- more than one input path is provided;
- the input path does not exist;
- the input path is not a file;
- the file cannot be read as UTF-8 JSON;
- the parsed value is not a JSON object;
- `envelope_type` is missing or is not `kernel_input_envelope`;
- the object is a response artifact;
- the object is a failure artifact;
- required envelope fields are missing;
- top-level canonical task object fields are present;
- source/profile metadata needed by later governed steps is absent.

On failure, the reader must not:

- repair the envelope;
- synthesize missing fields;
- continue into intake mapping;
- invoke P0/P1 or P0-P10 runtime;
- write a response artifact;
- write a failure artifact;
- unlock macro-side reporting.

Future conversion of reader failures into blocking failure artifacts requires a separate governed failure writer implementation pass.

## Stop Boundary Before Intake Mapping

The future reader boundary must stop here:

```text
explicit local envelope path
-> parsed and reader-validated kernel_input_envelope object
-> stop
```

It must not continue into:

- `kernel_intake_context` construction;
- P0/P1 intake preparation;
- P0/P1 execution;
- P0-P10 runtime invocation;
- canonical task object construction;
- response validation;
- response writing;
- failure writing;
- macro-side reporting.

## Blocked Behaviors

The current reader output contract must not silently introduce:

- runtime directory scanning;
- artifact queue discovery;
- artifact polling or watcher behavior;
- retry/backoff behavior;
- cleanup automation;
- intake mapping implementation code;
- kernel-owned P0/P1 intake object construction;
- P0/P1 execution;
- P0-P10 runtime invocation;
- canonical task object generation from envelope evidence;
- response artifact writing;
- failure artifact writing;
- CLI command behavior;
- multi-profile runtime expansion;
- live fetching;
- scheduler runtime;
- report composition;
- archive/export automation;
- CI behavior;
- package migration;
- external service calls;
- kernel contract modifications;
- macro-side production of kernel response artifacts.

## Governed Change Triggers

The following changes require a governed pass before implementation:

- allowing reader input from a directory instead of one explicit file path;
- allowing more than one envelope per invocation;
- adding runtime artifact discovery, polling, watcher, retry, or cleanup behavior;
- changing required envelope reader guardrails;
- allowing response or failure artifacts as reader input;
- allowing canonical task object fields inside reader output;
- changing the stop boundary before intake mapping;
- allowing reader output to be treated as `kernel_intake_context`;
- allowing reader output to unlock reporting;
- adding reader implementation code beyond the existing scaffold boundary;
- adding intake mapping code, P0/P1 or P0-P10 runtime execution, response validation, response writing, failure writing, CLI, CI, scheduler behavior, live fetching, report composition, package migration, or external service calls.

## Recommended Next Phase

Implement a `Kernel-Side Runtime Envelope Reader Baseline Refresh Pass`.

That pass should update the relevant kernel-side baseline or documentation index so this reader output contract is discoverable, while keeping reader implementation code, intake mapping code, runtime invocation, canonical task object generation, response/failure writers, CLI, CI, scheduler behavior, live fetching, report composition, package migration, external service calls, and actual handoff execution out of scope.
