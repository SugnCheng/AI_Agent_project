# Kernel Response Validation Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for `workflows/daily_us_core_kernel_runtime_boundary.py`.

It exists to prevent silent drift in future kernel response validation, especially blocked / restricted / standard state detection. It does not define or implement ai-meta-kernel runtime invocation, canonical kernel task object generation, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, archive/export automation, or production handoff.

## Scope

This contract applies only to:

- script: `workflows/daily_us_core_kernel_runtime_boundary.py`
- input envelope helper: `workflows/daily_us_core_fixture_kernel_input_envelope.py`
- envelope contract: `KERNEL_INPUT_ENVELOPE_OUTPUT_CONTRACT.md`
- integration plan: `KERNEL_RUNTIME_INTEGRATION_PLAN.md`
- upstream kernel handoff contract: `../ai-meta-kernel/meta-layer/HANDOFF_CONTRACT.md`
- upstream kernel task schema: `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`

The scaffold prepares a local future invocation boundary. It must not invoke the kernel and must not synthesize a kernel response.

## Compact Boundary Output Fields

When run without `--kernel-response-json`, the helper prints a compact boundary object with these fields:

| Field | Current value / type | Meaning | Fixed for current slice? | Future expansion rule |
| --- | --- | --- | --- | --- |
| `kernel_runtime_boundary_status` | `"prepared"` | The local boundary scaffold was prepared without invoking kernel runtime. | Yes | Additional values require explicit contract update. |
| `source_project` | `"macro-financial-intelligence-agent"` | Downstream validation project preparing the envelope. | Yes | Must not imply ownership of `ai-meta-kernel`. |
| `profile_id` | `"daily_us_core"` | Governed profile inherited from the envelope. | Yes | Do not broaden this helper beyond the profile without a new pass. |
| `run_mode` | `"daily_brief_run"` | Run mode inherited from the envelope. | Yes | Must remain aligned with `scheduler/run_profiles.yaml`. |
| `report_target` | `"daily_brief"` | Intended downstream report target as context only. | Yes | Must not be treated as a kernel decision. |
| `regions` | `["US"]` | Region scope inherited from the envelope. | Yes | Additional regions require profile/config approval. |
| `envelope_type` | `"macro_fixture_bundle_kernel_input"` | Envelope type produced by the upstream envelope helper. | Yes | Must remain aligned with `KERNEL_INPUT_ENVELOPE_OUTPUT_CONTRACT.md`. |
| `envelope_version` | `"0.1.0"` | Local envelope version. | Yes | Must remain aligned with `KERNEL_INPUT_ENVELOPE_OUTPUT_CONTRACT.md`. |
| `kernel_invocation_implemented` | `false` | Confirms actual ai-meta-kernel runtime invocation is absent. | Yes | May become true only after governed runtime handoff implementation. |
| `canonical_task_object_generated_locally` | `false` | Confirms the macro agent did not generate a canonical task object. | Yes | Must remain false in this scaffold. |
| `future_kernel_response_validation_available` | `true` | Indicates local validation helpers exist for future kernel-produced responses. | Yes | Removing this requires a contract update. |
| `downstream_reporting_blocked` | `true` | Confirms reporting cannot proceed from this scaffold alone. | Yes | May change only after a governed kernel runtime response path exists. |
| `deferred_runtime_behavior` | list of strings | Explicit marker of behavior still absent. | Yes | May shrink only when intentionally implemented and documented. |

## Current Fixed Compact Output

The current scaffold fixes this compact shape:

```json
{
  "kernel_runtime_boundary_status": "prepared",
  "source_project": "macro-financial-intelligence-agent",
  "profile_id": "daily_us_core",
  "run_mode": "daily_brief_run",
  "report_target": "daily_brief",
  "regions": ["US"],
  "envelope_type": "macro_fixture_bundle_kernel_input",
  "envelope_version": "0.1.0",
  "kernel_invocation_implemented": false,
  "canonical_task_object_generated_locally": false,
  "future_kernel_response_validation_available": true,
  "downstream_reporting_blocked": true
}
```

The actual output also includes `deferred_runtime_behavior`.

## Optional Future Kernel Response Validation Output

When run with `--kernel-response-json <path>`, the compact boundary output adds:

```json
{
  "future_kernel_response_check": {
    "kernel_response_validation": "ok",
    "schema_error_count": 0,
    "schema_errors": [],
    "kernel_response_state": "standard",
    "blocking_reasons": [],
    "restricting_reasons": [],
    "downstream_reporting_allowed": true
  }
}
```

The helper validates a supplied future kernel-produced object. It does not call kernel runtime and does not generate the object locally.

## Future Kernel Response Validation Fields

| Field | Type / values | Meaning |
| --- | --- | --- |
| `kernel_response_validation` | `"ok"` or `"failed"` | Whether the supplied response passed local schema validation against `TASK_OBJECT_SCHEMA.json`. |
| `schema_error_count` | integer | Number of schema validation errors found. |
| `schema_errors` | list of strings | Human-readable schema errors. Empty when validation passes. |
| `kernel_response_state` | `"standard"`, `"restricted"`, or `"blocked"` | Local handoff-state classification derived from kernel fields. |
| `blocking_reasons` | list of strings | Reasons downstream macro reporting must not proceed. |
| `restricting_reasons` | list of strings | Reasons downstream macro reporting may proceed only under restrictions. |
| `downstream_reporting_allowed` | boolean | True only for `standard` or `restricted`; false for `blocked`. |

## Fixed Blocked / Restricted Semantics

The current scaffold classifies a future kernel response as `blocked` when any of the following are true:

- response is not object-like;
- `downstream_recommendation.mode` is missing or invalid;
- `downstream_recommendation.mode == "do_not_handoff"`;
- `handoff.handoff_ready` is not `true`;
- `status_flags` contains `needs_reframe`;
- `status_flags` contains `needs_user_clarification`;
- `challenge_loop.result` is one of:
  - `clarify_first`
  - `reframe_first`
  - `escalate`
  - `decline`

The current scaffold classifies a future kernel response as `restricted` when it is not blocked and either:

- `downstream_recommendation.mode == "restricted_handoff"`;
- `status_flags` contains any of:
  - `needs_verification`
  - `needs_user_alignment`
  - `high_risk_restricted`
  - `ethics_escalated`

The current scaffold classifies a future kernel response as `standard` only when:

- no blocking condition is present;
- no restricting condition is present;
- `downstream_recommendation.mode == "standard_handoff"`;
- `handoff.handoff_ready == true`.

## Schema Validation Semantics

The helper validates future kernel responses against:

- `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`

Before schema validation, it also checks:

- response is object-like;
- all required top-level kernel fields are present.

The required fields are read from the upstream schema rather than duplicated manually.

## Drift Control Rules

- Do not rename compact boundary output fields without updating this contract.
- Do not remove `kernel_invocation_implemented` while runtime invocation remains absent.
- Do not set `kernel_invocation_implemented` to `true` without a governed runtime implementation pass.
- Do not remove `canonical_task_object_generated_locally`.
- Do not set `canonical_task_object_generated_locally` to `true` in the macro agent.
- Do not allow `downstream_reporting_blocked` to become `false` unless a real kernel response path exists and the response permits handoff.
- Do not weaken blocked / restricted semantics for convenience.
- Do not let the macro agent reinterpret kernel `status_flags` as non-binding.
- Do not treat schema-valid response as sufficient when blocked / restricted state detection says otherwise.

## Deferred Runtime Behaviors

The following behaviors remain explicitly absent:

- actual ai-meta-kernel runtime invocation;
- canonical kernel task object generation inside the macro agent;
- kernel response consumption by a report composer;
- downstream macro reporting;
- live fetching;
- scheduler execution;
- production bundle processing;
- archive/export automation;
- external service calls;
- CI;
- package migration;
- generic multi-profile runtime integration.

## Local Commands

Run the boundary scaffold from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_kernel_runtime_boundary.py'
```

Validate a future kernel-produced response JSON file:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_kernel_runtime_boundary.py' --kernel-response-json '<path-to-future-kernel-response.json>'
```
