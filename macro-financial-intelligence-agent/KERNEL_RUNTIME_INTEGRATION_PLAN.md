# Kernel Runtime Integration Plan

## Purpose

This document defines the next narrow, governed path for integrating the macro agent's fixture kernel input envelope with ai-meta-kernel runtime.

It is a planning document only. It does not implement kernel runtime handoff, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, archive/export automation, or production bundle processing.

## Authority Boundary

`ai-meta-kernel` remains the upstream reasoning authority.

The macro agent may:

- validate its evidence bundle;
- build a kernel input envelope;
- submit that envelope to a future kernel invocation boundary;
- validate that the returned kernel object satisfies the kernel contract.

The macro agent must not:

- generate a canonical kernel task object itself;
- bypass the kernel runtime pipeline;
- reinterpret kernel `status_flags`;
- convert a restricted or blocked kernel response into downstream execution permission.

Relevant upstream contracts:

- `../ai-meta-kernel/meta-layer/RUNTIME_PIPELINE.md`
- `../ai-meta-kernel/meta-layer/HANDOFF_CONTRACT.md`
- `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`

## Chosen Slice

The first runtime integration slice should remain scoped to:

- input: deterministic envelope from `workflows/daily_us_core_fixture_kernel_input_envelope.py`
- upstream envelope contract: `KERNEL_INPUT_ENVELOPE_OUTPUT_CONTRACT.md`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`
- output expectation: a kernel-produced object conforming to `TASK_OBJECT_SCHEMA.json`

The first slice should be a local fixture-only invocation boundary. It should not include live data, report composition, scheduler execution, or external service calls.

## Why This Is the Safest Next Step

The current envelope helper already proves that the macro agent can package validated evidence without pretending to be the kernel.

The next safe boundary is to define what must happen immediately before and after a kernel runtime invocation:

1. macro-side evidence and envelope validation must pass;
2. kernel runtime must own P0-P10 of the runtime pipeline;
3. macro-side execution may resume only after the kernel returns a valid task object;
4. blocked or restricted kernel responses must stop or constrain downstream macro reporting.

This preserves authority order while preparing for real integration.

## Existing Components To Use

| Component | Existing file | Role in integration slice |
| --- | --- | --- |
| Fixture kernel input envelope helper | `workflows/daily_us_core_fixture_kernel_input_envelope.py` | Produces deterministic macro-side input material. |
| Envelope output contract | `KERNEL_INPUT_ENVELOPE_OUTPUT_CONTRACT.md` | Defines compact output, full envelope shape, and non-impersonation guardrails. |
| Fixture bundle assembler | `workflows/daily_us_core_fixture_bundle_assembler.py` | Produces schema-valid evidence bundle used by the envelope. |
| Kernel runtime pipeline | `../ai-meta-kernel/meta-layer/RUNTIME_PIPELINE.md` | Governs P0-P10 from intake through handoff packaging. |
| Kernel handoff contract | `../ai-meta-kernel/meta-layer/HANDOFF_CONTRACT.md` | Defines required handoff fields and downstream obligations. |
| Kernel task object schema | `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json` | Defines the minimum valid kernel response object. |

## Proposed Future Integration Boundary

The first runtime integration helper should eventually follow this sequence:

```text
1. Build fixture kernel input envelope.
2. Validate envelope does not impersonate a kernel task object.
3. Submit envelope to ai-meta-kernel runtime boundary.
4. Kernel runs P0-P10:
   intake -> normalize -> frame -> classify -> trigger -> decompose ->
   calibrate -> challenge -> gate -> emit -> handoff.
5. Receive kernel-produced task object.
6. Validate task object against TASK_OBJECT_SCHEMA.json.
7. Apply handoff gate:
   - proceed only if status and handoff mode allow it;
   - otherwise stop and surface the blocking reason.
```

The implementation of step 3 is explicitly deferred.

## Pre-Handoff Validations Macro Agent Must Complete

Before invoking kernel runtime, the macro agent must complete these validations:

| Validation | Source | Required outcome |
| --- | --- | --- |
| Evidence bundle schema validation | `daily_us_core_fixture_bundle_assembler.py` | `schema_validation == "ok"`. |
| Evidence bundle invariant validation | `daily_us_core_fixture_bundle_assembler.py` | `invariant_validation == "ok"`. |
| Envelope validation | `daily_us_core_fixture_kernel_input_envelope.py` | `envelope_validation == "ok"`. |
| Kernel object non-impersonation | `daily_us_core_fixture_kernel_input_envelope.py` | `canonical_task_object_generated == false`. |
| Required envelope fields | `KERNEL_INPUT_ENVELOPE_OUTPUT_CONTRACT.md` | All required envelope fields present. |
| Deferred behavior transparency | Envelope output | Deferred markers include `kernel_runtime_execution` and `ai_meta_kernel_runtime_handoff` before integration is implemented. |
| Source/runtime boundary | Repo governance | No live fetching, scheduler execution, or report composition occurred before kernel invocation. |

If any validation fails, the macro agent must not invoke kernel runtime.

## Kernel Runtime Responsibilities

Once invoked, the kernel must own the runtime pipeline:

| Pipeline phase | Kernel responsibility |
| --- | --- |
| P0 Intake | Treat the envelope and operator intent as raw request/context. |
| P1 Normalize | Convert envelope into the canonical task object shape. |
| P2 Frame | Define surface request, core goal, scope, non-goals, and success criteria. |
| P3 Classify | Assign task type without deferring to macro-agent labels. |
| P4 Trigger | Select required H1-H11 habits. |
| P5 Decompose | Separate facts, assumptions, inferences, unknowns, constraints, stakeholders, and tradeoffs. |
| P6 Calibrate | Set risk level, categories, ambiguity, alignment need, and confidence ceiling. |
| P7 Challenge | Run challenge loop appropriate to financial/time-sensitive evidence. |
| P8 Gate | Decide whether handoff proceeds, proceeds with constraints, requires clarification/reframe, escalates, or declines. |
| P9 Emit | Produce schema-valid task object. |
| P10 Handoff | Emit downstream recommendation and handoff instructions. |

The macro agent must not override these outputs for convenience.

## Minimum Valid Kernel Response

A kernel response is minimally valid only if it satisfies `TASK_OBJECT_SCHEMA.json` and includes:

- `schema_version`
- `task_id`
- `raw_request`
- `kernel_stage`
- `framed_objective`
- `task_classification`
- `risk_profile`
- `triggered_habits`
- `structural_decomposition`
- `required_checks`
- `status_flags`
- `verification_plan`
- `challenge_loop`
- `downstream_recommendation`
- `handoff`

Additional semantic requirements before macro reporting may continue:

1. `schema_version` must match the kernel schema const.
2. `triggered_habits` must contain at least one primary habit.
3. `risk_profile.categories` must not combine `none_identified` with other categories.
4. `structural_decomposition` must separate facts, assumptions, inferences, unknowns, constraints, stakeholders, and `tradeoffs`.
5. `required_checks.must_verify` must reflect source/date/factual verification needs when material.
6. `verification_plan.required` must be true or explicitly justified as false.
7. `challenge_loop.performed` must be true for any restricted or medium/high risk continuation.
8. `downstream_recommendation.mode` must be one of `standard_handoff`, `restricted_handoff`, or `do_not_handoff`.
9. `handoff.handoff_ready` must align with `status_flags` and `downstream_recommendation.mode`.

## Conditions Required Before Downstream Macro Reporting Continues

Downstream macro reporting may continue only if:

1. the kernel response validates against `TASK_OBJECT_SCHEMA.json`;
2. `status_flags` does not include `needs_reframe` or `needs_user_clarification`;
3. unresolved `needs_verification` is either absent or explicitly allowed by `restricted_handoff`;
4. `downstream_recommendation.mode` is `standard_handoff` or `restricted_handoff`;
5. `handoff.handoff_ready` is true;
6. all `required_checks` assigned to the macro agent are preserved;
7. uncertainty and source limitations remain visible for reporting;
8. the report target is compatible with the kernel's `downstream_recommendation.output_format`.

If `restricted_handoff` is returned, report generation must preserve the restrictions and may not produce unrestricted conclusions.

## Blocking Failure Modes

The macro agent must block downstream execution when any of these occur:

| Failure mode | Required handling |
| --- | --- |
| Envelope validation fails | Do not invoke kernel; surface local validation error. |
| Kernel runtime unavailable | Do not fabricate a task object; mark handoff unavailable. |
| Kernel response is not valid JSON/object | Block downstream execution. |
| Kernel response fails `TASK_OBJECT_SCHEMA.json` | Block downstream execution and record schema failure. |
| Kernel omits required handoff fields | Block downstream execution. |
| `status_flags` includes `needs_reframe` | Return to kernel/user reframe path. |
| `status_flags` includes `needs_user_clarification` | Request clarification before reporting. |
| `downstream_recommendation.mode == "do_not_handoff"` | Do not proceed to macro reporting. |
| `handoff.handoff_ready == false` | Do not proceed to macro reporting. |
| Required verification is unresolved but output asks for firm conclusions | Restrict or block reporting. |
| Kernel output conflicts with macro convenience | Follow kernel output. |

## Refusal / Escalation Conditions

The macro agent must not continue if the kernel response:

- flags `high_risk_restricted` without explicit downstream restrictions;
- flags `ethics_escalated` without ethics-aware instructions;
- detects that the task is asking for direct investment advice rather than research reporting;
- requires user alignment before proceeding;
- requires source verification that has not been completed or assigned;
- returns `challenge_loop.result` as `clarify_first`, `reframe_first`, `escalate`, or `decline`.

## In-Scope Next Steps

The next implementation pass should do only the following:

1. Add a local planning-aligned integration boundary scaffold, if approved.
2. Reuse the current envelope helper output.
3. Define a placeholder `invoke_kernel_runtime(envelope)` boundary that intentionally raises `NotImplementedError`.
4. Add response validation helpers for future kernel task objects, without producing them locally.
5. Keep downstream reporting blocked until a real kernel response exists.

No actual kernel runtime invocation should be implemented in the next scaffold unless separately approved.

## Explicitly Deferred

The kernel runtime integration slice must not implement:

- actual ai-meta-kernel runtime invocation;
- canonical kernel task object generation inside the macro agent;
- report composition;
- live fetching;
- scheduler execution;
- production bundle assembly;
- archive/export automation;
- external service calls;
- CI;
- package migration;
- generic multi-profile runtime integration.

## Guardrails

- Do not modify `../ai-meta-kernel/meta-layer/RUNTIME_PIPELINE.md`.
- Do not modify `../ai-meta-kernel/meta-layer/HANDOFF_CONTRACT.md`.
- Do not modify `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`.
- Do not let macro-agent local fields override kernel `status_flags`.
- Do not infer readiness from successful bundle/envelope validation alone.
- Do not convert `preliminary_priority` into kernel risk.
- Do not continue to reporting when kernel handoff is blocked or restricted beyond the reporter's allowed scope.
- Do not synthesize a fake kernel response for convenience.

## Recommended Next Phase

Implement `TASK 40 - Kernel Runtime Boundary Scaffold`.

That pass should add a local boundary scaffold and response-validation shape without invoking ai-meta-kernel runtime, without generating canonical task objects in the macro agent, and without enabling downstream report composition.
