# File-Based Kernel Exchange Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for `workflows/daily_us_core_write_kernel_envelope_artifact.py`.

It stabilizes the compact output fields, artifact naming semantics, and generated-artifact guardrails for the write-envelope-only scaffold. It does not implement ai-meta-kernel runtime handoff, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or kernel response handling.

## Scope

This contract applies only to:

- script: `workflows/daily_us_core_write_kernel_envelope_artifact.py`
- file exchange contract: `FILE_BASED_KERNEL_EXCHANGE_CONTRACT.md`
- envelope contract: `KERNEL_INPUT_ENVELOPE_OUTPUT_CONTRACT.md`
- invocation decision: `KERNEL_INVOCATION_INTERFACE_DECISION.md`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`

The scaffold writes a macro-produced kernel input envelope artifact. It must not invoke ai-meta-kernel runtime and must not generate a canonical kernel task object.

## Compact Output Fields

| Field | Current value / type | Meaning | Fixed for current slice? | Drift rule |
| --- | --- | --- | --- | --- |
| `kernel_exchange_write_envelope_status` | `"ok"` | Envelope artifact was written successfully. | Yes | Additional statuses require a contract update. |
| `artifact_kind` | `"kernel_input_envelope"` | Artifact class written by this scaffold. | Yes | Must not be changed to `kernel_response` or `kernel_failure`. |
| `artifact_path` | string | Repo-relative path to the generated envelope artifact. | No | Must remain under `macro-financial-intelligence-agent/runtime/kernel_exchange/envelopes/`. |
| `artifact_filename` | string | Generated artifact filename following the file exchange naming convention. | No | Must follow the naming convention in this contract. |
| `profile_id` | `"daily_us_core"` | Governed run profile used to produce the envelope. | Yes | Broader profiles require a new governed pass. |
| `run_mode` | `"daily_brief_run"` | Governed run mode inherited from the envelope. | Yes | Must remain aligned with `scheduler/run_profiles.yaml`. |
| `report_target` | `"daily_brief"` | Intended downstream report target as context only. | Yes | Must not be treated as a kernel decision. |
| `regions` | `["US"]` | Region scope inherited from the envelope. | Yes | Additional regions require config/profile approval. |
| `envelope_type` | `"macro_fixture_bundle_kernel_input"` | Envelope type produced by the fixture envelope helper. | Yes | Must remain aligned with `KERNEL_INPUT_ENVELOPE_OUTPUT_CONTRACT.md`. |
| `envelope_version` | `"0.1.0"` | Local envelope contract version. | Yes | Version changes require explicit contract review. |
| `kernel_invocation_performed` | `false` | Confirms no ai-meta-kernel runtime invocation occurred. | Yes | Must remain false until actual runtime handoff is implemented. |
| `kernel_response_read` | `false` | Confirms no kernel response artifact was read. | Yes | Must remain false in this write-envelope scaffold. |
| `kernel_response_written` | `false` | Confirms no kernel response artifact was written by the macro agent. | Yes | Must remain false; macro must not produce kernel responses. |
| `canonical_task_object_generated_locally` | `false` | Confirms the macro agent did not generate a canonical kernel task object. | Yes | Must remain false. |
| `downstream_reporting_unlocked` | `false` | Confirms reporting remains blocked after writing the envelope. | Yes | Must remain false until a valid kernel response permits continuation. |
| `deferred_runtime_behavior` | list of strings | Explicit list of behavior absent from this scaffold. | Yes | Items may be removed only when intentionally implemented and documented. |

## Current Compact Output Shape

The current scaffold fixes this compact output shape:

```json
{
  "kernel_exchange_write_envelope_status": "ok",
  "artifact_kind": "kernel_input_envelope",
  "artifact_path": "macro-financial-intelligence-agent/runtime/kernel_exchange/envelopes/<artifact_filename>",
  "artifact_filename": "daily_us_core__daily_brief_run__daily_brief__<YYYYMMDDTHHMMSSZ>__kernel_input_envelope.json",
  "profile_id": "daily_us_core",
  "run_mode": "daily_brief_run",
  "report_target": "daily_brief",
  "regions": ["US"],
  "envelope_type": "macro_fixture_bundle_kernel_input",
  "envelope_version": "0.1.0",
  "kernel_invocation_performed": false,
  "kernel_response_read": false,
  "kernel_response_written": false,
  "canonical_task_object_generated_locally": false,
  "downstream_reporting_unlocked": false
}
```

The actual output also includes `deferred_runtime_behavior`.

## Artifact Naming Semantics

Generated envelope artifacts must use:

```text
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__kernel_input_envelope.json
```

For the current slice:

```text
daily_us_core__daily_brief_run__daily_brief__YYYYMMDDTHHMMSSZ__kernel_input_envelope.json
```

Rules:

- `utc_timestamp` must use compact UTC format: `YYYYMMDDTHHMMSSZ`.
- The optional `--timestamp` argument is for deterministic local checks only.
- Generated artifacts must be written under `runtime/kernel_exchange/envelopes/`.
- This scaffold must not write response or failure artifacts.

## Generated Artifact Guardrails

- Runtime envelope JSON artifacts are generated local material and are ignored by Git by default.
- Runtime artifacts must not be committed unless a future governed fixture pass explicitly promotes one into `fixtures/`.
- The generated envelope is evidence/context for ai-meta-kernel intake, not a canonical kernel task object.
- Do not rename compact output fields without updating this contract.
- Do not change artifact directory or filename semantics without updating `FILE_BASED_KERNEL_EXCHANGE_CONTRACT.md`.
- Do not set any kernel invocation, response read/write, local canonical task object, or reporting unlock flag to `true` in this scaffold.
- Do not allow downstream reporting to proceed from a written envelope alone.

## Deferred Runtime Behaviors

The following behaviors remain explicitly absent:

- actual ai-meta-kernel runtime invocation;
- kernel response artifact reading;
- kernel response artifact writing;
- failure artifact writing;
- canonical kernel task object generation inside the macro agent;
- downstream macro reporting;
- live fetching;
- scheduler execution;
- report composition;
- archive/export automation;
- external service calls;
- CI;
- package migration;
- generic multi-profile file exchange.

## Local Commands

Run the write-envelope scaffold from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_write_kernel_envelope_artifact.py'
```

Run with a deterministic timestamp:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_write_kernel_envelope_artifact.py' --timestamp '20260423T000000Z'
```
