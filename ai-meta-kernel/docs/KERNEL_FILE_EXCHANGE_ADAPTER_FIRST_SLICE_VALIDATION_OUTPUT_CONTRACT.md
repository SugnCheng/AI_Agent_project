# Kernel File Exchange Adapter First-Slice Validation Output Contract

## Purpose

This document snapshots the output contract for the first implementation slice's adapter fixture validation surface.

It is a developer-facing contract note only. It does not add runtime code, modify kernel contracts, invoke kernel runtime, write response artifacts, write failure artifacts, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Contract Decision

Current first-slice validation contract:

```text
validate_existing_daily_us_core_static_adapter_fixtures_and_fail_closed_scaffold_boundaries
```

The first slice may validate static fixture shape and current adapter scaffold guardrails only. A successful validation means the committed examples remain compatible with the documented file-exchange boundary and that blocked runtime boundaries still fail closed.

## Fixtures In Scope

The first slice includes exactly the existing `daily_us_core` static fixture set:

| Fixture role | Path |
| --- | --- |
| Kernel input envelope | `examples/file-exchange/envelopes/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.example.json` |
| Expected kernel response | `examples/file-exchange/responses/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_response.example.json` |
| Expected blocking failure | `examples/file-exchange/failures/daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_failure.example.json` |

No additional profiles, fixture classes, generated artifacts, or committed failing fixtures belong to this slice.

## Allowed Validation Surface

The first slice may validate that:

1. the envelope fixture exists and parses as a JSON object;
2. the envelope fixture is a `kernel_input_envelope`;
3. the envelope fixture satisfies the current envelope intake guardrails;
4. the envelope fixture does not contain canonical task object top-level fields;
5. the response fixture exists and parses as a JSON object;
6. the response fixture validates against `meta-layer/TASK_OBJECT_SCHEMA.json`;
7. the failure fixture exists and parses as a JSON object;
8. the failure fixture is a blocking kernel exchange failure;
9. the failure fixture does not contain partial canonical task object content;
10. `prepare_kernel_intake` remains context-only and stops before runtime;
11. `invoke_kernel_runtime` remains intentionally unimplemented;
12. `write_response_artifact` remains intentionally unimplemented;
13. `write_failure_artifact` remains intentionally unimplemented.

The validation surface is local-only and deterministic. It may read static fixtures and schema files. It must not discover live work, scan runtime artifact queues, mutate fixture files, or write output artifacts.

## Success Signal

The current success signal should remain the existing local helper outputs:

```text
kernel-file-exchange-fixture-checks-ok
kernel-file-exchange-adapter-scaffold-checks-ok
```

When run through the kernel local validation wrapper, the combined kernel-side success signal should remain:

```text
kernel-local-validation-checks-ok
```

These signals mean only that the static fixture contract and scaffold guardrails pass locally. They do not mean that runtime handoff, kernel execution, response writing, failure writing, scheduler behavior, or macro-side reporting is implemented.

## Expected Failure Behavior

First-slice validation should fail if:

- the envelope fixture is missing, invalid JSON, not a JSON object, missing required envelope fields, not a `kernel_input_envelope`, or contains canonical task object top-level fields;
- the response fixture is missing, invalid JSON, not a JSON object, or invalid against `TASK_OBJECT_SCHEMA.json`;
- the failure fixture is missing, invalid JSON, not a JSON object, not blocking, or contains partial canonical task object content;
- any blocked scaffold boundary stops failing closed.

Failure should be local and explicit. The helper should not repair fixtures, generate replacement artifacts, call runtime code, or continue as if a partial contract were valid.

## Blocked Behaviors

The first slice must continue to block:

- runtime adapter invocation;
- P0-P10 kernel runtime execution;
- envelope-to-P0/P1 intake preparation;
- canonical task object generation from envelope evidence;
- response artifact writing;
- failure artifact writing;
- runtime artifact directory scanning;
- artifact polling or watcher behavior;
- retry/backoff behavior;
- cleanup automation;
- CLI command design;
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

- adding fixture classes beyond envelope, expected response, and blocking failure;
- adding profiles beyond `daily_us_core`;
- changing fixture filenames, path conventions, or naming semantics;
- changing envelope intake required fields;
- allowing canonical task object fields inside envelope fixtures;
- changing response validation away from `TASK_OBJECT_SCHEMA.json`;
- changing failure fixture shape or allowing non-blocking failure examples;
- adding generated runtime artifacts as committed fixtures;
- changing success signal text;
- broadening validation into reader discovery, writer behavior, runtime invocation, CLI, CI, scheduler behavior, live fetching, report composition, package migration, or actual handoff execution.

## Recommended Next Phase

Implement a `Kernel-Side Adapter Fixture Validation Helper Pass`.

That pass may add the smallest local helper needed to enforce this first-slice output contract if the existing helpers are not sufficient, but it should still avoid runtime code, response/failure writers, CLI, CI, scheduler behavior, live fetching, report composition, package migration, external service calls, and actual handoff execution.
