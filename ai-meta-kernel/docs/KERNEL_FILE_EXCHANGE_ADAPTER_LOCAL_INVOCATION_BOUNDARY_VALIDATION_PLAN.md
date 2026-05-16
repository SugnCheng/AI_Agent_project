# Kernel File Exchange Adapter Local Invocation Boundary Validation Plan

## Purpose

This note defines the validation plan for the future kernel-side local
invocation boundary after the R25 boundary plan and R26 output contract.

It defines how future validation should prove the local invocation result
object, terminal path selection, failure routing, and blocked downstream
behavior. It does not implement local invocation code, validation helper code,
CLI behavior, queue discovery, polling, retry, cleanup, macro report unlock,
actual handoff, or wrapper inclusion.

## Current Validation Decision

Current validation decision:

```text
local_invocation_boundary_validation_plan_baseline
```

This baseline fixes the future validation scope before any helper or runtime
implementation is added.

## Validation Scope

Future validation should cover:

- future local invocation result object shape;
- `selected_terminal_path` semantics;
- response-only terminal path;
- failure-only terminal path;
- no dual artifact paths;
- blocking failure routing;
- locked downstream markers.

## Success-Path Validation Themes

Future success-path validation should prove:

- one explicit local envelope path;
- one explicit output destination policy;
- one local invocation result object;
- `selected_terminal_path == response`;
- `response_artifact_path` present;
- `failure_artifact_path` absent or null;
- `response_writer_called` true only within future governed non-dry-run path;
- `failure_writer_called` false;
- `macro_report_unlock` false;
- `actual_handoff_executed` false;
- `cli_behavior_added` false.

## Failure-Path Validation Themes

Future failure-path validation should prove:

- reader failure routes to blocking failure path;
- intake mapping failure routes to blocking failure path;
- runtime invocation failure routes to blocking failure path;
- response validation failure routes to blocking failure path;
- response writer failure routes to blocking failure path only if safely
  classified;
- `selected_terminal_path == failure`;
- `failure_artifact_path` present;
- `response_artifact_path` absent or null;
- `failure_writer_called` true only within future governed non-dry-run path;
- `response_writer_called` false;
- `macro_report_unlock` false;
- `actual_handoff_executed` false;
- `cli_behavior_added` false.

## Fail-Closed Validation Themes

Future fail-closed validation should prove:

- non-explicit input rejected;
- queue-like input rejected;
- missing output destination policy rejected;
- ambiguous `selected_terminal_path` rejected;
- both `response_artifact_path` and `failure_artifact_path` rejected;
- `macro_report_unlock` true rejected;
- `actual_handoff_executed` true rejected;
- `cli_behavior_added` true rejected;
- polling / retry / cleanup markers rejected.

## Wrapper Stance

The future helper should remain standalone unless separately governed.

Do not add the future helper to `validation/run_all_kernel_local_checks.py` by
default.

`kernel-local-validation-checks-ok` must not silently broaden.

## Explicit Blocked Behaviors

This validation plan keeps the following blocked:

- no local invocation implementation;
- no validation helper implementation;
- no CLI;
- no queue discovery;
- no polling / retry / cleanup;
- no macro report unlock;
- no actual handoff;
- no wrapper inclusion.

## Recommended Next Phase

Recommended next phase:

```text
Local Invocation Boundary Implementation Gate Pass
```
