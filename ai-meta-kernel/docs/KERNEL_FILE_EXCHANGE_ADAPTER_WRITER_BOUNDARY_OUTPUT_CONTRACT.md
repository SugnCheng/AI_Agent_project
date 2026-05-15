# Kernel File Exchange Adapter Writer Boundary Output Contract

## Purpose

This document snapshots the future output contract for kernel-side response writer and blocking failure writer boundaries.

It is a developer-facing contract note only. It does not add runtime code, modify kernel contracts, invoke kernel runtime, write response artifacts, write failure artifacts, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Contract Decision

Current writer-boundary output contract:

```text
future_writers_must_validate_before_write_and_emit_exactly_one_terminal_artifact
```

The future writer boundary is not open for implementation yet. This contract fixes the expected output shape and pre-write guarantees that must be preserved when a later governed implementation pass opens response or failure writing.

## Future Response Writer Output Expectations

The future response writer may eventually write one successful kernel response artifact for one validated envelope invocation.

Expected response artifact name:

```text
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__kernel_response.json
```

Expected response artifact properties:

- produced by `ai-meta-kernel`;
- JSON object;
- valid against `meta-layer/TASK_OBJECT_SCHEMA.json`;
- canonical field names preserved;
- kernel-owned status, verification, challenge, recommendation, and handoff semantics preserved;
- restrictions, reframe needs, blocked states, and verification gaps surfaced when present;
- written only after all response pre-write validations pass.

The response writer must not emit partial task objects, repair invalid task objects, infer missing kernel conclusions, or write a response artifact after schema validation fails.

## Future Blocking Failure Writer Output Expectations

The future blocking failure writer may eventually write one failure artifact when a valid response artifact cannot be produced.

Expected failure artifact name:

```text
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__kernel_failure.json
```

Expected failure artifact properties:

- produced by `ai-meta-kernel` or a thin kernel-owned adapter boundary;
- JSON object;
- `artifact_type == "kernel_exchange_failure"`;
- `artifact_version == "0.1.0"`;
- `source_project == "ai-meta-kernel"`;
- `blocking == true`;
- includes `profile_id`, `run_mode`, `report_target`, `regions`, `envelope_artifact_path`, `failure_stage`, `failure_reason`, and `created_at`;
- uses a governed failure stage;
- contains no partial canonical task object content;
- does not unlock downstream reporting.

Current governed failure stages:

- `pre_invoke`
- `invoke`
- `response_parse`
- `response_schema_validation`
- `response_state_validation`

## Pre-Write Validation Requirements

Future writer implementation must preserve this validation order:

1. Confirm exactly one local envelope invocation context is in scope.
2. Confirm the envelope has passed kernel-side envelope intake validation.
3. Confirm kernel-owned intake and runtime execution are available through governed implementation passes.
4. For a candidate response, confirm it is a JSON object.
5. Validate the candidate response against `meta-layer/TASK_OBJECT_SCHEMA.json`.
6. Validate response state and handoff semantics before any response write.
7. Write a response artifact only after response validation succeeds.
8. If response production or validation fails, build a blocking failure object instead of a partial response.
9. Confirm the failure object is a JSON object with the required failure fields.
10. Confirm `blocking == true` and failure stage is governed.
11. Confirm the failure object contains no partial canonical task object content.
12. Write a failure artifact only after failure validation succeeds.

No writer should mutate the input envelope, mutate static fixtures, repair invalid kernel outputs, or silently continue after a failed pre-write validation.

## Mutual Exclusivity Rules

For one envelope invocation, the future writer boundary may emit exactly one terminal artifact:

| Condition | Allowed terminal artifact |
| --- | --- |
| Valid kernel response passes all pre-write validation | One response artifact |
| Runtime, parsing, schema, or response state validation fails | One blocking failure artifact |

The writer boundary must not write both a response artifact and a failure artifact for the same invocation.

The writer boundary must not write neither artifact after a terminal failure is known unless a governed fatal-error policy explicitly defines that behavior.

Changing this mutual exclusivity rule requires a governed pass.

## Blocked Behaviors

The current writer-boundary contract must not silently introduce:

- response artifact writing;
- failure artifact writing;
- envelope-to-P0/P1 intake implementation;
- P0-P10 runtime invocation;
- canonical task object generation from envelope evidence;
- runtime artifact directory scanning;
- artifact polling or watcher behavior;
- retry/backoff behavior;
- cleanup automation;
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

- changing response artifact naming semantics;
- changing failure artifact naming semantics;
- changing response schema validation requirements;
- allowing response writes before schema and state validation;
- allowing failure artifacts with `blocking == false`;
- changing required failure fields;
- adding, removing, or renaming failure stages;
- allowing partial canonical task object content in failure artifacts;
- allowing both response and failure artifacts for one invocation;
- allowing macro-side production of kernel response artifacts;
- adding writer implementation code;
- adding runtime reader discovery, polling, watcher, retry, cleanup, CLI, CI, scheduler behavior, live fetching, report composition, package migration, or external service calls.

## Recommended Next Phase

Implement a `Kernel-Side Terminal Writer Implementation Gate Pass`.

That pass should decide whether the first writer implementation opening is a combined minimal terminal writer slice or separate response-writer / failure-writer slices. It must keep writer code, CLI, CI, scheduler behavior, live fetching, report composition, package migration, external service calls, and actual handoff execution out of scope unless separately governed.
