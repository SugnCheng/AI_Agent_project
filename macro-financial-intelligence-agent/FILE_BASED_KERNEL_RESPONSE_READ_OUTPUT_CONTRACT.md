# File-Based Kernel Response Read Output Contract Snapshot

## Purpose

This document snapshots the current developer-facing output contract for `workflows/daily_us_core_read_kernel_response_artifact.py`.

It stabilizes the compact decision fields, artifact match semantics, blocked / restricted / standard drift rules, and downstream unlock guardrails for the local read-response scaffold. It does not implement ai-meta-kernel runtime handoff, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or artifact mutation.

## Scope

This contract applies only to:

- script: `workflows/daily_us_core_read_kernel_response_artifact.py`
- planning source: `FILE_BASED_KERNEL_RESPONSE_READ_PLAN.md`
- file exchange contract: `FILE_BASED_KERNEL_EXCHANGE_CONTRACT.md`
- response validation contract: `KERNEL_RESPONSE_VALIDATION_OUTPUT_CONTRACT.md`
- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`

The scaffold reads local response or failure artifacts and emits a compact downstream decision. It must not invoke ai-meta-kernel runtime and must not generate a canonical kernel task object.

## Accepted Inputs

The scaffold accepts exactly one of:

- `--response-artifact`
- `--failure-artifact`
- `--envelope-artifact`
- `--artifact-stem`

Rules:

- Explicit response/failure paths are read directly.
- `--envelope-artifact` and `--artifact-stem` derive matching response/failure artifact paths from the governed file exchange stem.
- Derived runtime response artifacts live under `runtime/kernel_exchange/responses/`.
- Derived runtime failure artifacts live under `runtime/kernel_exchange/failures/`.

## Compact Output Fields

| Field | Current value / type | Meaning | Fixed for current slice? | Drift rule |
| --- | --- | --- | --- | --- |
| `kernel_exchange_read_response_status` | `"ok"` | The reader completed local classification without invoking kernel runtime. | Yes | Additional statuses require contract update. |
| `artifact_match_status` | string enum-like value | How the input mapped to response/failure artifacts. | Yes | New values require contract update. |
| `artifact_kind` | `"kernel_response"`, `"kernel_failure"`, `"ambiguous"`, or `null` | Artifact class used for the decision. | Yes | Must not imply macro-produced kernel responses. |
| `response_artifact_path` | string or `null` | Repo-relative response path read or expected. | No | Must remain traceable. |
| `failure_artifact_path` | string or `null` | Repo-relative failure path read or expected. | No | Must remain traceable. |
| `kernel_response_validation` | `"ok"`, `"failed"`, `"not_run"`, or `"not_applicable"` | Schema/response validation status. | Yes | Must not be treated as the only unlock condition. |
| `schema_error_count` | integer | Count of kernel schema errors when response validation runs. | Yes | Must be zero when validation did not run. |
| `schema_errors` | list of strings | Kernel schema validation errors. | Yes | Empty when validation passes or does not run. |
| `kernel_response_state` | `"standard"`, `"restricted"`, or `"blocked"` | Final response state after validation and state classification. | Yes | Do not add state values without contract update. |
| `blocking_reasons` | list of strings | Reasons downstream reporting must remain blocked. | Yes | Must be non-empty when state is `blocked`. |
| `restricting_reasons` | list of strings | Reasons downstream reporting is allowed only with restrictions. | Yes | Must be preserved for `restricted`. |
| `downstream_reporting_allowed` | boolean | Whether downstream reporting may proceed at all. | Yes | True only for `standard` or `restricted` response states. |
| `downstream_reporting_mode` | `"standard"`, `"restricted"`, or `"blocked"` | Required downstream continuation mode. | Yes | Must equal the effective state. |
| `kernel_runtime_invocation_performed` | `false` | Confirms no ai-meta-kernel runtime invocation occurred. | Yes | Must remain false in this scaffold. |
| `canonical_task_object_generated_locally` | `false` | Confirms the macro agent did not generate a canonical task object. | Yes | Must remain false. |
| `report_composition_performed` | `false` | Confirms no report composition occurred. | Yes | Must remain false in this scaffold. |

## Artifact Match Semantics

Current `artifact_match_status` values:

| Value | Meaning | Required decision |
| --- | --- | --- |
| `explicit_response` | An explicit response artifact path was provided and exists. | Validate response, then classify state. |
| `explicit_failure` | An explicit failure artifact path was provided and exists. | Block downstream reporting. |
| `missing_explicit_response_artifact` | Explicit response path does not exist. | Block. |
| `missing_explicit_failure_artifact` | Explicit failure path does not exist. | Block. |
| `missing_envelope_artifact` | Explicit envelope path does not exist. | Block. |
| `response_only` | A derived response artifact exists and matching failure artifact does not. | Validate response, then classify state. |
| `failure_only` | A derived failure artifact exists and matching response artifact does not. | Block. |
| `both_response_and_failure` | Both derived response and failure artifacts exist for one stem. | Block and require operator review. |
| `no_matching_artifact` | Neither derived response nor failure artifact exists. | Block. |

## Current Response Validation Semantics

For `kernel_response` artifacts:

1. Parse JSON.
2. Confirm object-like response through existing kernel response validation helper.
3. Validate against `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`.
4. Apply blocked / restricted / standard state detection from `KERNEL_RESPONSE_VALIDATION_OUTPUT_CONTRACT.md`.
5. Force state to `blocked` if schema validation fails.

The reader reuses the existing validation helper rather than defining a second independent kernel response validator.

## Failure Artifact Semantics

For `kernel_failure` artifacts, v0.1 requires:

- object-like JSON;
- `artifact_type == "kernel_exchange_failure"`;
- `blocking == true`;
- valid `failure_stage`;
- non-empty `failure_reason`.

Any failure artifact keeps:

- `kernel_response_validation == "not_applicable"`;
- `kernel_response_state == "blocked"`;
- `downstream_reporting_allowed == false`;
- `downstream_reporting_mode == "blocked"`.

## Blocked / Restricted / Standard Drift Rules

- `blocked` must prevent report composition.
- `restricted` may allow only constrained future reporting that preserves kernel restrictions, uncertainty, and required checks.
- `standard` may allow normal governed macro reporting, but does not bypass human review.
- Schema-valid response is not sufficient for unlock; state classification still applies.
- Failure artifacts are always blocking in v0.1.
- Missing artifacts are always blocking.
- Ambiguous response/failure pairs are always blocking.
- Restricted responses must not be silently promoted to standard.
- Macro local convenience must not override kernel `status_flags`, `downstream_recommendation.mode`, `handoff.handoff_ready`, or `challenge_loop.result`.

## Downstream Unlock Guardrails

Downstream reporting may proceed only when:

- `kernel_response_validation == "ok"`;
- `kernel_response_state` is `standard` or `restricted`;
- `downstream_reporting_allowed == true`;
- `downstream_reporting_mode` is `standard` or `restricted`;
- no failure artifact is controlling the decision;
- no ambiguity between response and failure artifacts exists.

Even when reporting is allowed:

- `restricted` must preserve restrictions and uncertainty;
- human review checkpoints remain required;
- report composition is not performed by this scaffold.

## Explicitly Absent Behaviors

The following behaviors remain explicitly absent:

- actual ai-meta-kernel runtime invocation;
- kernel response generation;
- kernel failure artifact generation;
- canonical kernel task object generation inside the macro agent;
- report composition;
- live fetching;
- scheduler execution;
- archive/export automation;
- artifact polling;
- retry/backoff behavior;
- artifact deletion or mutation;
- external service calls;
- CI;
- package migration;
- generic multi-profile exchange.

## Local Commands

Validate a static standard response fixture:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_read_kernel_response_artifact.py' --response-artifact 'macro-financial-intelligence-agent\fixtures\kernel_responses\daily_us_core_standard_kernel_response.example.json'
```

Check a runtime artifact stem:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python 'macro-financial-intelligence-agent\workflows\daily_us_core_read_kernel_response_artifact.py' --artifact-stem 'daily_us_core__daily_brief_run__daily_brief__20260423T000000Z'
```
