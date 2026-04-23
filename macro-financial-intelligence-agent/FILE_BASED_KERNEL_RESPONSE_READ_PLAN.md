# File-Based Kernel Response Read Plan

## Purpose

This document defines the smallest governed v0.1 path for how `macro-financial-intelligence-agent` should later read a file-based kernel response artifact or failure artifact.

It is a planning document only. It does not implement ai-meta-kernel runtime handoff, response reading, failure reading, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or downstream reporting.

## Authority Boundary

`ai-meta-kernel` remains the upstream reasoning authority.

The macro agent may later:

- locate a response or failure artifact that matches a previously written envelope artifact;
- parse and validate the artifact;
- classify the result as `standard`, `restricted`, or `blocked`;
- keep downstream reporting blocked unless the validated kernel response permits continuation.

The macro agent must not:

- generate a canonical kernel task object;
- reinterpret kernel `status_flags` for convenience;
- treat a failure artifact as a response artifact;
- unlock downstream reporting from a failure artifact;
- proceed from a schema-valid response without applying blocked / restricted semantics.

## Chosen Minimal Boundary

The first read-response slice should remain scoped to:

- profile: `daily_us_core`
- run mode: `daily_brief_run`
- report target: `daily_brief`
- region: `US`
- envelope artifact location: `runtime/kernel_exchange/envelopes/`
- response artifact location: `runtime/kernel_exchange/responses/`
- failure artifact location: `runtime/kernel_exchange/failures/`

The read boundary should accept one explicit envelope artifact path or artifact stem. It should then look for exactly matching response or failure artifacts using the file-based exchange naming convention.

## Artifact Discovery Semantics

Given an envelope artifact named:

```text
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__kernel_input_envelope.json
```

the future reader should derive:

```text
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__kernel_response.json
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__kernel_failure.json
```

Discovery rules:

1. The reader should prefer explicit artifact paths over directory scanning.
2. If both a response artifact and failure artifact exist for the same stem, the result must be blocked and require operator review.
3. If only a failure artifact exists, the result is blocked.
4. If only a response artifact exists, validate it before any downstream decision.
5. If neither exists, the result is blocked with a pending-response state.
6. Runtime artifacts remain generated local material and should not be committed by default.

## Required Validation Order

The future read helper should validate in this order:

1. **Envelope reference validation**
   - Confirm the originating envelope path or stem is present.
   - Confirm naming parts match the governed profile, run mode, report target, and timestamp format.

2. **Artifact class validation**
   - Confirm the discovered artifact kind is either `kernel_response` or `kernel_failure`.
   - Reject ambiguous or mismatched artifact kinds.

3. **Failure artifact validation**
   - If reading a failure artifact, require `artifact_type == "kernel_exchange_failure"`.
   - Require `blocking == true` for v0.1.
   - Require `failure_stage` and `failure_reason`.
   - Keep downstream reporting blocked.

4. **Response artifact parse validation**
   - Confirm the response is valid JSON.
   - Confirm the response is object-like.
   - Do not accept arrays, strings, or partial fragments as kernel responses.

5. **Kernel schema validation**
   - Validate response artifacts against `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`.
   - Reuse existing response validation semantics from `KERNEL_RESPONSE_VALIDATION_OUTPUT_CONTRACT.md`.

6. **Kernel state classification**
   - Classify the response as `standard`, `restricted`, or `blocked`.
   - Apply blocked / restricted semantics after schema validation.

7. **Downstream unlock decision**
   - Unlock unrestricted reporting only for `standard`.
   - Allow only constrained continuation for `restricted`.
   - Keep reporting blocked for `blocked`, failure artifacts, parse failures, schema failures, ambiguous artifacts, or missing artifacts.

## State Handling

| Read result | Required state | Downstream effect |
| --- | --- | --- |
| No response or failure artifact found | `blocked` | Reporting remains blocked; wait or retry manually. |
| Failure artifact found | `blocked` | Reporting remains blocked; surface failure reason. |
| Both response and failure artifacts found | `blocked` | Reporting remains blocked; operator review required. |
| Response is invalid JSON or not object-like | `blocked` | Reporting remains blocked; surface parse/type failure. |
| Response fails kernel schema validation | `blocked` | Reporting remains blocked; surface schema errors. |
| Response state is `blocked` | `blocked` | Reporting remains blocked; preserve blocking reasons. |
| Response state is `restricted` | `restricted` | Reporting may continue only within kernel restrictions. |
| Response state is `standard` | `standard` | Reporting may continue under normal governed macro workflow. |

## Unlock Decision Rules

The future reader should emit a compact decision object with enough information for downstream helpers to decide whether they may continue.

Minimum planned fields:

- `kernel_exchange_read_response_status`
- `artifact_match_status`
- `artifact_kind`
- `response_artifact_path`
- `failure_artifact_path`
- `kernel_response_validation`
- `kernel_response_state`
- `blocking_reasons`
- `restricting_reasons`
- `downstream_reporting_allowed`
- `downstream_reporting_mode`

Planned `downstream_reporting_mode` values:

- `blocked`
- `restricted`
- `standard`

Rules:

- `blocked` means no report composition may proceed.
- `restricted` means any future reporter must preserve kernel restrictions, uncertainty, and required checks.
- `standard` means the response permits normal governed macro reporting, but does not bypass review workflow.

## Main Constraints

- The macro agent must not create or repair kernel response content.
- File presence does not prove validity.
- Schema validity does not prove downstream permission.
- Failure artifacts are always blocking in v0.1.
- Restricted responses cannot be silently promoted to standard.
- The read helper must not invoke ai-meta-kernel runtime.
- The read helper must not compose reports.
- The read helper must not delete or mutate runtime artifacts.

## Explicitly Deferred

The following remain deferred:

- actual response/failure artifact reader implementation;
- directory polling or watcher behavior;
- retry/backoff behavior;
- automatic kernel invocation;
- kernel-side response writer implementation;
- failure artifact writer implementation;
- report composer integration;
- operator review UI;
- artifact cleanup or retention automation;
- live fetching;
- scheduler runtime;
- archive/export automation;
- external service calls;
- CI;
- package migration;
- generic multi-profile exchange.

## Recommended Next Phase

Implement a `File-Based Exchange Read-Response Scaffold Pass`.

That pass should add a local helper that can read an explicit generated response or failure artifact path, reuse existing kernel response validation helpers, classify `standard` / `restricted` / `blocked`, and keep downstream reporting blocked unless the validated response permits continuation. It should still avoid actual ai-meta-kernel invocation, report composition, live fetching, scheduler runtime, and external service calls.
