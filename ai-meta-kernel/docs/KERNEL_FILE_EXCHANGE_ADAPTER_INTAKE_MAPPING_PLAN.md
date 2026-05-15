# Kernel File Exchange Adapter Intake Mapping Plan

## Purpose

This document defines the smallest governed planning note for the future envelope-to-P0/P1 intake mapping boundary.

It is a planning document only. It does not add runtime code, modify kernel contracts, prepare kernel intake, invoke kernel runtime, generate canonical task objects, write response artifacts, write failure artifacts, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Planning Decision

Current intake-mapping planning decision:

```text
plan_envelope_to_kernel_owned_p0_p1_intake_before_implementation
```

The future mapping boundary may translate validated envelope evidence/context into kernel-owned intake context. It must not convert macro-provided material into completed kernel conclusions.

## Intake Mapping Boundary

The future boundary is:

```text
validated kernel input envelope
-> kernel-owned P0/P1 intake context
-> stop before P0-P10 runtime invocation
```

This boundary should preserve the original envelope as source context for the kernel. It should prepare only the minimum intake material needed for P0/P1 framing and clarification, not a canonical task object.

## Envelope Fields That May Flow Into Intake

The following envelope fields may flow into future kernel-owned intake as evidence, metadata, or context:

| Envelope field | Allowed intake role |
| --- | --- |
| `envelope_type` | Artifact type guardrail only. |
| `envelope_version` | Envelope compatibility metadata. |
| `source_project` | Provenance metadata. |
| `profile_id` | Run/profile context. |
| `run_mode` | Run intent context. |
| `report_target` | Downstream target context, not a reporting unlock. |
| `regions` | Scope context for framing and verification. |
| `operator_intent` | Primary source for `raw_request.text` or equivalent intake request text. |
| `evidence_bundle` | Evidence/context source for kernel framing and verification. |
| `evidence_context` | Source metadata, acquisition context, and uncertainty context. |
| `kernel_task_object_expectation` | Expectation metadata only; not kernel conclusions. |
| `deferred_runtime_behavior` | Explicit blocked/deferred behavior context. |

The full validated envelope should remain available to the kernel as source context for P0/P1. The mapping should preserve provenance and should not drop source boundaries that matter for verification.

## Kernel-Owned Reasoning That Must Not Be Macro-Provided

The following must remain kernel-owned and must not be copied from the envelope as macro-provided conclusions:

- `schema_version`;
- `task_id`;
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
- `handoff`;
- final report eligibility;
- response state classification;
- restricted or blocked handoff decisions.

Macro-provided evidence may inform these fields only after the kernel runtime performs its own framing, classification, verification, challenge, and handoff logic.

## Minimum Mapping Expectations

Future implementation should preserve these minimum expectations:

1. Accept exactly one validated envelope object.
2. Preserve the original envelope as source context.
3. Use `operator_intent` as the operator goal input, not as a framed kernel objective.
4. Carry `profile_id`, `run_mode`, `report_target`, and `regions` as metadata.
5. Carry `evidence_bundle` and `evidence_context` as evidence/context only.
6. Treat `kernel_task_object_expectation` as expectation metadata only.
7. Carry `deferred_runtime_behavior` as explicit blocked/deferred behavior context.
8. Do not construct a `TASK_OBJECT_SCHEMA.json` response object.
9. Do not infer or fill canonical task object fields.
10. Stop before P0-P10 runtime invocation.

## Blocked Before Implementation

The following remain blocked before intake mapping implementation:

- intake mapping code;
- kernel-owned P0/P1 intake object construction;
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

- changing required envelope fields;
- changing which envelope fields may flow into intake;
- allowing envelope fields to populate canonical task object conclusions directly;
- changing the boundary from one envelope per invocation;
- changing the preserved source-context requirement;
- adding P0/P1 intake implementation code;
- adding P0-P10 runtime invocation;
- adding response or failure writer behavior;
- adding runtime reader discovery, polling, watcher, retry, cleanup, CLI, CI, scheduler behavior, live fetching, report composition, package migration, or external service calls.

## Recommended Next Phase

Implement a `Kernel-Side Runtime Invocation Preparation Pass`.

That pass should define the future runtime invocation boundary, expected `kernel_intake_context` input, expected candidate response output, failure semantics, validation plan, and blocked writer/CLI/reporting behaviors while keeping P0/P1 execution, P0-P10 runtime invocation implementation, canonical task object generation, response/failure writers, CLI, CI, scheduler behavior, live fetching, report composition, package migration, external service calls, and actual handoff execution out of scope.
