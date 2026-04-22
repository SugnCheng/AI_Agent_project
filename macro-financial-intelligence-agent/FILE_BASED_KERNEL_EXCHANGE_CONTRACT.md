# File-Based Kernel Exchange Contract

## Purpose

This document defines the v0.1 file-based exchange contract for future handoff between `macro-financial-intelligence-agent` and `ai-meta-kernel`.

It is a contract document only. It does not implement runtime handoff, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or canonical task object generation inside the macro agent.

## Interface Choice

The selected v0.1 interface is:

**File-based envelope / response exchange.**

The macro agent writes a kernel input envelope artifact. The kernel later reads that artifact and writes a kernel response artifact conforming to `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`.

## Artifact Classes

There are three artifact classes:

| Artifact class | Producer | Consumer | Meaning |
| --- | --- | --- | --- |
| Kernel input envelope | macro agent | ai-meta-kernel | Evidence/context prepared for kernel P0/P1 intake. |
| Kernel response | ai-meta-kernel | macro agent | Canonical kernel-produced task object. |
| Kernel failure artifact | ai-meta-kernel or boundary wrapper | macro agent/operator | Transport-level failure when no valid kernel response exists. |

The macro agent must not produce a kernel response artifact.

## Directory Contract

### Runtime Exchange Directories

Runtime artifacts should live under:

```text
macro-financial-intelligence-agent/runtime/kernel_exchange/
+-- envelopes/
+-- responses/
+-- failures/
```

These directories are for generated runtime artifacts and should not be treated as governed fixtures.

### Fixture Directories

Committed static fixtures remain under:

```text
macro-financial-intelligence-agent/fixtures/kernel_responses/
```

Future envelope fixtures, if needed, should use:

```text
macro-financial-intelligence-agent/fixtures/kernel_envelopes/
```

Fixture artifacts are reviewable examples. Runtime artifacts are generated execution material.

## Naming Convention

Runtime artifact filenames should use:

```text
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__{artifact_kind}.json
```

Where:

- `profile_id` is the governed run profile, for example `daily_us_core`.
- `run_mode` is the governed run mode, for example `daily_brief_run`.
- `report_target` is the governed report target, for example `daily_brief`.
- `utc_timestamp` uses compact UTC format: `YYYYMMDDTHHMMSSZ`.
- `artifact_kind` is one of:
  - `kernel_input_envelope`
  - `kernel_response`
  - `kernel_failure`

Example:

```text
daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.json
daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_response.json
daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_failure.json
```

The timestamp must be generated at artifact creation time in future runtime code. This contract does not add that code.

## Fixture vs Runtime Artifacts

| Type | Location | Committed? | Purpose |
| --- | --- | --- | --- |
| Fixture response | `fixtures/kernel_responses/` | Yes | Regression examples for standard / restricted / blocked validation paths. |
| Fixture envelope | `fixtures/kernel_envelopes/` | Optional future | Stable examples for envelope shape validation. |
| Runtime envelope | `runtime/kernel_exchange/envelopes/` | No by default | Generated macro-to-kernel input material. |
| Runtime response | `runtime/kernel_exchange/responses/` | No by default | Generated kernel-to-macro task object material. |
| Runtime failure | `runtime/kernel_exchange/failures/` | No by default | Generated error/failure material when no valid kernel response exists. |

Runtime artifacts should be ignored by version control unless a future task intentionally promotes one into a reviewed fixture.

## Kernel Input Envelope Artifact Expectations

A runtime envelope artifact must preserve the current envelope contract and include:

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

The envelope artifact must not contain completed canonical kernel fields as top-level conclusions.

The envelope artifact must continue to satisfy:

- `KERNEL_INPUT_ENVELOPE_OUTPUT_CONTRACT.md`

## Kernel Response Artifact Expectations

A runtime response artifact must:

- be produced by `ai-meta-kernel`, not the macro agent;
- be JSON object-like;
- validate against `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`;
- include all required top-level kernel fields from the schema;
- preserve `status_flags`, `downstream_recommendation`, and `handoff` without macro-side reinterpretation;
- be checked by the existing future kernel response validation helper before downstream reporting is allowed.

A schema-valid response may still be blocked or restricted. The macro agent must apply the semantics in:

- `KERNEL_RESPONSE_VALIDATION_OUTPUT_CONTRACT.md`

## Failure Artifact Shape

If the kernel runtime cannot produce a valid kernel response artifact, a failure artifact should be written instead of fabricating a response.

Failure artifacts should use:

```json
{
  "artifact_type": "kernel_exchange_failure",
  "artifact_version": "0.1.0",
  "source_project": "macro-financial-intelligence-agent",
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
- A failure artifact must not include a partial canonical task object.
- A failure artifact must not unlock reporting.
- A failure artifact may reference the envelope path for traceability.

## Retention / Cleanup Expectations For v0.1

Runtime exchange artifacts are local generated material.

v0.1 expectations:

- Do not commit runtime exchange artifacts by default.
- Keep runtime artifacts long enough for local review and debugging.
- Promote an artifact to `fixtures/` only through an explicit governed fixture pass.
- Do not auto-delete artifacts in v0.1 runtime scaffolds.
- Do not add retention automation yet.

The future implementation pass should update `.gitignore` before generating runtime artifacts.

## Guardrails

- Do not modify upstream kernel contracts to fit macro-agent convenience.
- Do not generate a canonical kernel response inside the macro agent.
- Do not treat an envelope artifact as a kernel response artifact.
- Do not proceed to reporting without a valid kernel response artifact.
- Do not proceed to unrestricted reporting from a restricted response.
- Do not proceed to reporting from a blocked response or failure artifact.
- Do not add live fetching, scheduler runtime, report composition, or external service calls as part of file exchange scaffolding.

## Open Decisions Deferred Beyond This Contract

The following remain deferred:

- actual creation of `runtime/kernel_exchange/` directories;
- `.gitignore` update for runtime exchange artifacts;
- write-envelope helper implementation;
- kernel-side file reader implementation;
- kernel-side response writer implementation;
- failure artifact writer implementation;
- CLI wrapper;
- package migration;
- CI integration;
- operator review UI or workflow automation.

## Recommended Next Phase

Implement a `File-Based Exchange Scaffold Pass`.

That pass may add local directory placeholders, `.gitignore` rules, and a write-envelope-only scaffold, but should still avoid actual kernel runtime invocation, live fetching, scheduler runtime, report composition, and external service calls.
