# Kernel File Exchange Adapter Contract Snapshot

## Purpose

This document snapshots the current developer-facing contract for the future `ai-meta-kernel` file exchange adapter.

It stabilizes the adapter boundary, envelope intake expectations, response/failure artifact responsibilities, ownership boundaries, and drift rules. It does not implement runtime invocation, file reading, file writing, schema validation code, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or changes to kernel contracts.

## Scope

This contract applies to the planned kernel-side adapter described in:

- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_PLAN.md`

It must remain compatible with:

- `META_LAYER_MASTER_SPEC.md`
- `meta-layer/RUNTIME_PIPELINE.md`
- `meta-layer/HANDOFF_CONTRACT.md`
- `meta-layer/TASK_OBJECT_SCHEMA.json`
- `../macro-financial-intelligence-agent/FILE_BASED_KERNEL_EXCHANGE_CONTRACT.md`

If this snapshot conflicts with canonical kernel contracts, the canonical kernel contracts win.

## Current Adapter Boundary

The current v0.1 adapter boundary is fixed as:

```text
kernel input envelope artifact
-> kernel-side envelope reader
-> envelope intake validation
-> kernel-owned P0/P1 intake object
-> full kernel runtime pipeline P0-P10
-> canonical TASK_OBJECT_SCHEMA response artifact
   OR blocking kernel_exchange_failure artifact
```

The adapter is a boundary around the kernel. It must not become a second reasoning system, an alternate pipeline, or a shortcut around P0-P10.

## Envelope Intake Contract

The kernel-side adapter may accept exactly one envelope artifact path as input.

The envelope must be treated as evidence/context only.

Current expected envelope fields are:

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

Minimum intake checks:

1. The artifact path exists.
2. The artifact parses as JSON.
3. The parsed artifact is object-like.
4. The artifact is a kernel input envelope, not a response or failure artifact.
5. Required envelope fields are present.
6. The envelope does not contain completed top-level canonical task object conclusions.
7. The original envelope is preserved as source context for kernel intake.

Minimum mapping expectations:

| Kernel target | Source | Contract |
| --- | --- | --- |
| `raw_request.text` | `operator_intent` plus a concise envelope summary | Must represent the operator goal, not a kernel conclusion. |
| `raw_request.source_context` | envelope metadata and evidence bundle reference | Must preserve provenance and profile context. |
| P0/P1 intake context | full envelope object | Must remain available to framing, verification, challenge, and handoff logic. |
| `structural_decomposition` | kernel-owned extraction | Must be produced by the kernel, not copied as a macro conclusion. |
| `downstream_recommendation` | kernel-owned P9/P10 output | Must not be copied from the envelope as a conclusion. |

## Kernel Response Artifact Writer Contract

When the kernel completes the runtime pipeline successfully, it may write one response artifact.

The response artifact must:

1. be produced by `ai-meta-kernel`;
2. be JSON object-like;
3. validate against `meta-layer/TASK_OBJECT_SCHEMA.json`;
4. include all required top-level schema fields;
5. preserve canonical field names;
6. preserve kernel-owned status and handoff semantics;
7. surface verification gaps, restrictions, reframe needs, and blocked states.

The response artifact must not be written if schema validation fails.

Current response artifact naming expectation:

```text
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__kernel_response.json
```

The response artifact is the only successful kernel output artifact in this v0.1 file exchange boundary.

## Kernel Failure Artifact Writer Contract

When the adapter cannot produce a valid response artifact, it must produce a blocking failure artifact instead of a partial task object.

Current failure stages:

- `pre_invoke`
- `invoke`
- `response_parse`
- `response_schema_validation`
- `response_state_validation`

Minimum failure artifact shape:

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

Failure artifact rules:

- `blocking` must be `true`.
- Failure artifacts must not include partial canonical task objects.
- Failure artifacts must not unlock downstream reporting.
- Failure artifacts must preserve enough context for operator review and debugging.

## Ownership Boundaries

| Area | Kernel side owns | Macro side owns |
| --- | --- | --- |
| Evidence bundle construction | No | Yes |
| Kernel input envelope construction | No | Yes |
| Envelope artifact writing | No | Yes |
| Envelope artifact reading | Yes | No |
| Envelope intake validation | Yes | May validate before write, but not as kernel authority |
| P0-P10 runtime pipeline | Yes | No |
| Canonical task object construction | Yes | No |
| Response artifact writing | Yes | No |
| Kernel-side failure artifact writing | Yes or a thin kernel boundary wrapper | No, except governed fixtures or macro-side read errors |
| Response artifact re-validation after read | Optional | Yes before downstream unlock |
| Report composition | No | Future macro responsibility after valid kernel response |

## Drift Rules

The following changes require a governed contract pass before implementation:

- changing the adapter boundary;
- allowing more than one input envelope per invocation;
- changing required envelope fields;
- changing envelope-to-intake mapping expectations;
- changing response artifact naming semantics;
- changing failure artifact shape;
- adding or removing failure stages;
- allowing response artifacts to be written before schema validation;
- allowing failure artifacts with `blocking == false`;
- allowing the macro agent to write kernel response artifacts;
- allowing the macro agent to generate canonical task objects;
- adding runtime invocation behavior;
- adding artifact polling, watcher, retry, cleanup, or mutation behavior;
- broadening from `daily_us_core` to generic multi-profile exchange;
- adding external service calls, CI, package migration, scheduler runtime, or report composition.

## Explicitly Absent Behaviors

The following behaviors remain explicitly absent:

- actual kernel-side adapter implementation;
- actual runtime invocation;
- file reader implementation;
- response writer implementation;
- failure writer implementation;
- CLI command design;
- schema validation code;
- package layout changes;
- CI integration;
- artifact polling or watcher behavior;
- retry/backoff behavior;
- artifact cleanup automation;
- multi-profile runtime expansion;
- report composition;
- live fetching;
- scheduler runtime;
- external service calls;
- operator review UI;
- archive/export automation.

## Recommended Next Phase

Implement a `Kernel-Side File Exchange Adapter Fixture Planning Pass`.

That pass should define the smallest static envelope fixture and expected response/failure fixture strategy for testing the adapter contract before any runtime code is added.
