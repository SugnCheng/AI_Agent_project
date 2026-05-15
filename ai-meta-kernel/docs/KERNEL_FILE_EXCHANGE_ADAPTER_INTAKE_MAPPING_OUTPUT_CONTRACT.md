# Kernel File Exchange Adapter Intake Mapping Output Contract

## Purpose

This document snapshots the future output contract for the envelope-to-P0/P1 intake mapping boundary.

It is a developer-facing contract note only. It does not add runtime code, modify kernel contracts, prepare kernel intake, invoke kernel runtime, generate canonical task objects, write response artifacts, write failure artifacts, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Contract Decision

Current intake-mapping output contract:

```text
future_mapping_may_emit_kernel_owned_intake_context_but_not_kernel_conclusions
```

The mapping boundary is not open for implementation yet. This contract fixes the allowed input surface, acceptable future intake-context output shape, required exclusions, and stop boundary before runtime invocation.

## Allowed Envelope Inputs

Future intake mapping may accept exactly one validated kernel input envelope object.

The envelope must already satisfy the current envelope intake guardrails:

- JSON object;
- `envelope_type == "kernel_input_envelope"`;
- required envelope fields present;
- not a response artifact;
- not a failure artifact;
- no canonical task object top-level fields;
- source project and profile metadata preserved.

Allowed envelope fields for mapping:

| Envelope field | Mapping role |
| --- | --- |
| `envelope_type` | Guardrail metadata only. |
| `envelope_version` | Compatibility metadata. |
| `source_project` | Provenance metadata. |
| `profile_id` | Run/profile metadata. |
| `run_mode` | Run context metadata. |
| `report_target` | Target context metadata, not a reporting unlock. |
| `regions` | Scope context. |
| `operator_intent` | Operator request source text. |
| `evidence_bundle` | Evidence/context source. |
| `evidence_context` | Source, acquisition, and uncertainty context. |
| `kernel_task_object_expectation` | Expectation metadata only. |
| `deferred_runtime_behavior` | Explicit blocked/deferred behavior context. |

No other envelope field may become a kernel conclusion without a governed pass.

## Acceptable Future Intake-Context Output

Future mapping may emit a local intake context object for kernel-owned P0/P1 preparation.

Acceptable output shape:

```text
kernel_intake_context
```

Acceptable future intake-context contents:

- `source_envelope`: the original validated envelope object or an immutable equivalent reference;
- `operator_request`: request text derived from `operator_intent`;
- `source_context`: provenance metadata from `source_project`, `profile_id`, `run_mode`, `report_target`, and `regions`;
- `evidence_context`: evidence and acquisition context copied from `evidence_bundle` and `evidence_context`;
- `expectation_context`: non-conclusive expectation metadata from `kernel_task_object_expectation`;
- `deferred_behavior_context`: blocked/deferred behavior notes from `deferred_runtime_behavior`;
- `mapping_stage`: a marker showing the object stops at intake mapping and has not entered P0-P10 runtime.

The output must remain evidence/context for the kernel. It must not be treated as a canonical task object, response artifact, or runtime result.

## Kernel-Owned Fields Excluded From Mapping Output

The mapping output must not include or populate these canonical task object fields:

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

The mapping output must also not include:

- final report eligibility;
- response state classification;
- restricted or blocked handoff decisions;
- generated response artifact paths;
- generated failure artifact paths.

These remain kernel-owned reasoning or writer outputs after governed runtime and writer passes.

## Stop Boundary Before Runtime Invocation

The future mapping boundary must stop here:

```text
validated envelope
-> kernel_intake_context
-> stop
```

It must not continue into:

- P0/P1 execution;
- P0-P10 runtime invocation;
- canonical task object construction;
- response validation;
- response writing;
- failure writing;
- macro-side reporting.

## Blocked Behaviors

The current intake-mapping output contract must not silently introduce:

- intake mapping implementation code;
- kernel-owned P0/P1 intake object construction;
- P0/P1 execution;
- P0-P10 runtime invocation;
- canonical task object generation from envelope evidence;
- response artifact writing;
- failure artifact writing;
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

- changing allowed envelope inputs;
- changing required envelope intake guardrails;
- changing acceptable intake-context output fields;
- allowing canonical task object fields in mapping output;
- allowing mapping output to be treated as a response artifact;
- allowing mapping output to unlock reporting;
- changing the stop boundary before runtime invocation;
- adding intake mapping implementation code;
- adding P0/P1 or P0-P10 runtime execution;
- adding response or failure writer behavior;
- adding runtime reader discovery, polling, watcher, retry, cleanup, CLI, CI, scheduler behavior, live fetching, report composition, package migration, or external service calls.

## Recommended Next Phase

Implement a `Kernel-Side Response Validation Preparation Pass`.

That pass should define how a candidate kernel response object will later be validated before any response writer or failure writer is opened. It must keep response/failure writers, CLI, CI, scheduler behavior, live fetching, report composition, package migration, external service calls, and actual handoff execution out of scope.
