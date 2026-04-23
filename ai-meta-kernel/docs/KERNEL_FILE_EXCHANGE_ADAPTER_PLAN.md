# Kernel File Exchange Adapter Plan

## Purpose

This document defines the smallest governed v0.1 plan for a future `ai-meta-kernel` file exchange adapter.

The adapter would later read a file-based kernel input envelope produced by `macro-financial-intelligence-agent`, run the kernel-owned runtime pipeline, and write either:

- a canonical kernel task object response artifact; or
- a blocking failure artifact when no valid response can be produced.

This is a planning document only. It does not implement runtime invocation, file reading, file writing, schema validation code, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or changes to kernel contracts.

## Authority

Canonical kernel contracts remain:

- `META_LAYER_MASTER_SPEC.md`
- `meta-layer/RUNTIME_PIPELINE.md`
- `meta-layer/HANDOFF_CONTRACT.md`
- `meta-layer/TASK_OBJECT_SCHEMA.json`

The macro-side file exchange contract remains:

- `../macro-financial-intelligence-agent/FILE_BASED_KERNEL_EXCHANGE_CONTRACT.md`

If this adapter plan conflicts with canonical kernel contracts, the canonical kernel contracts win.

## v0.1 Adapter Boundary

The smallest acceptable v0.1 kernel-side adapter boundary is:

```text
kernel input envelope artifact
-> kernel-side envelope reader
-> envelope intake validation
-> kernel-owned P0/P1 intake object
-> full kernel runtime pipeline P0-P10
-> canonical TASK_OBJECT_SCHEMA response artifact
   OR blocking kernel_exchange_failure artifact
```

The adapter is a boundary around the kernel. It must not become a second reasoning system and must not weaken the kernel runtime pipeline.

## Kernel-Side File Reader Boundary

The future kernel-side reader should accept exactly one envelope artifact path.

Minimum reader responsibilities:

1. Confirm the file exists.
2. Parse it as JSON.
3. Confirm it is object-like.
4. Confirm it is a kernel input envelope, not a kernel response or failure artifact.
5. Confirm required envelope fields are present.
6. Confirm the envelope does not contain completed top-level canonical task object conclusions.
7. Preserve the original envelope as source context for P0/P1 intake.

The reader should not:

- fetch external sources;
- infer macro facts not present in the envelope;
- generate a canonical task object by shortcut;
- bypass P0-P10;
- compose reports;
- mutate macro runtime artifacts other than writing the governed response or failure artifact.

## Envelope Intake Expectations

The envelope is evidence/context only.

Expected envelope fields are defined by the macro-side file exchange contract and currently include:

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

The kernel should map the envelope into its own intake layer without treating the envelope as a completed task object.

Minimum intake mapping expectations:

| Kernel area | Source from envelope | Rule |
| --- | --- | --- |
| `raw_request.text` | `operator_intent` plus a concise envelope summary | Must represent the operator goal, not a kernel conclusion. |
| `raw_request.source_context` | envelope metadata and evidence bundle reference | Must preserve provenance and profile context. |
| P0 Intake context | full envelope object | Must remain available for framing, verification, challenge, and handoff decisions. |
| Facts / assumptions / inferences | kernel-owned extraction from evidence context | Must be separated by the kernel, not pre-decided by the macro agent. |
| Downstream recommendation | kernel-owned P9/P10 output | Must not be copied from the envelope as a conclusion. |

The kernel may use envelope fields as evidence, but must still perform framing, classification, risk calibration, habit triggering, structural decomposition, verification planning, challenge, gate, emit, and handoff packaging.

## Response Artifact Writer Expectations

If the kernel successfully completes the runtime pipeline, it should write one response artifact.

Minimum response artifact requirements:

1. Produced by `ai-meta-kernel`, not by the macro agent.
2. JSON object-like.
3. Valid against `meta-layer/TASK_OBJECT_SCHEMA.json`.
4. Includes all required top-level schema fields.
5. Preserves canonical field names:
   - `framed_objective`
   - `task_classification`
   - `risk_profile`
   - `triggered_habits`
   - `structural_decomposition`
   - `required_checks`
   - `status_flags`
   - `downstream_recommendation`
   - `handoff`
6. Uses kernel-owned status and handoff semantics:
   - `standard_handoff`
   - `restricted_handoff`
   - `do_not_handoff`
7. Does not silently hide verification gaps, restrictions, reframe needs, or blocked states.

The writer should use the macro-side file naming convention:

```text
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__kernel_response.json
```

The response artifact should be written only after schema validation succeeds.

## Failure Artifact Writer Expectations

If the kernel-side adapter cannot produce a valid response artifact, it should write one blocking failure artifact instead of fabricating a partial response.

Minimum failure cases:

- envelope file missing;
- envelope JSON parse failure;
- envelope shape invalid;
- envelope is not a kernel input envelope;
- envelope contains forbidden completed kernel task object conclusions;
- kernel runtime invocation failure;
- kernel output parse failure;
- kernel output does not validate against `TASK_OBJECT_SCHEMA.json`;
- kernel output state cannot be safely classified for handoff.

Minimum failure artifact fields should follow the macro-side exchange contract:

```json
{
  "artifact_type": "kernel_exchange_failure",
  "artifact_version": "0.1.0",
  "source_project": "ai-meta-kernel",
  "profile_id": "string",
  "run_mode": "string",
  "report_target": "string",
  "regions": ["string"],
  "envelope_artifact_path": "string",
  "failure_stage": "pre_invoke|invoke|response_parse|response_schema_validation|response_state_validation",
  "failure_reason": "string",
  "blocking": true,
  "created_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

Rules:

- `blocking` must be `true` for v0.1 failures.
- Failure artifacts must not contain partial canonical task objects.
- Failure artifacts must not unlock downstream reporting.
- Failure artifacts should preserve enough context for operator review and debugging.

## Responsibility Split

| Responsibility | Kernel side | Macro side |
| --- | --- | --- |
| Build evidence bundle | No | Yes |
| Build kernel input envelope | No | Yes |
| Write envelope artifact | No | Yes |
| Read envelope artifact | Yes | No |
| Run P0-P10 kernel pipeline | Yes | No |
| Produce canonical task object | Yes | No |
| Validate response against `TASK_OBJECT_SCHEMA.json` before writing | Yes | May re-check after reading |
| Write response artifact | Yes | No |
| Write failure artifact for kernel-side failure | Yes or thin kernel boundary wrapper | No, except static fixtures or macro-side read errors |
| Classify response as standard / restricted / blocked after reading | May emit canonical fields | Yes, for downstream unlock decision |
| Compose macro report | No | Future macro responsibility after valid kernel response |

## Explicitly Deferred Behaviors

The following remain deferred beyond this plan:

- actual kernel-side adapter implementation;
- actual runtime invocation;
- CLI command design;
- package layout changes;
- CI integration;
- artifact polling or watchers;
- retry/backoff behavior;
- artifact cleanup automation;
- multi-profile runtime expansion;
- report composition;
- live fetching;
- scheduler runtime;
- external service calls;
- operator review UI;
- archive/export automation.

## Main Constraints

1. The adapter must preserve kernel authority over P0-P10.
2. The macro envelope is not a task object.
3. The macro agent must not write response artifacts.
4. The kernel must not write a response artifact unless it validates against `TASK_OBJECT_SCHEMA.json`.
5. Failure artifacts must be blocking.
6. Restricted handoffs must not be silently promoted to standard handoffs.
7. File exchange must not become a shortcut around framing, verification, challenge, or handoff gates.

## Recommended Next Phase

Implement a `Kernel File Exchange Adapter Contract Snapshot Pass`.

That pass should stabilize the planned adapter inputs, outputs, failure stages, and artifact naming semantics before any runtime code is added.
