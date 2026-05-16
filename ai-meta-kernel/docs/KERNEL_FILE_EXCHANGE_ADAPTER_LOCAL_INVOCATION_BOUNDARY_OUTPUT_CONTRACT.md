# Kernel File Exchange Adapter Local Invocation Boundary Output Contract

## Purpose

This note defines the future output contract for the kernel-side local
invocation boundary after R25 preparation.

It defines the future local invocation result object, terminal path semantics,
failure routing expectations, and blocked downstream behavior. It does not
implement local invocation code, CLI behavior, queue discovery, polling, retry,
cleanup, macro report unlock, actual handoff, or scheduler/runtime
orchestration.

## Current Contract Decision

Current contract decision:

```text
local_invocation_boundary_output_contract_baseline
```

This baseline fixes the intended local invocation result shape before any
future implementation or validation helper is added.

## Future Invocation Input Contract

The future local invocation boundary should accept only explicit local inputs:

- explicit local envelope path;
- explicit local output destination policy;
- no queue discovery;
- no scheduler input;
- no external service input.

The input contract must not infer work from directories, queues, scheduler
state, environment state, live sources, or downstream reporting configuration.

## Future Invocation Result Object Required Fields

The future local invocation result object should include these required fields:

- `invocation_type`;
- `invocation_state`;
- `invocation_stage`;
- `source_envelope_path`;
- `selected_terminal_path`;
- `response_artifact_path`;
- `failure_artifact_path`;
- `terminal_artifact_written`;
- `response_writer_called`;
- `failure_writer_called`;
- `macro_report_unlock`;
- `actual_handoff_executed`;
- `cli_behavior_added`.

The result object should remain local and descriptive. It must not become a CLI
success signal, macro report unlock marker, scheduler state object, or actual
handoff record.

## Terminal Path Semantics

The `selected_terminal_path` value may be:

- `response`;
- `failure`.

Response path semantics:

- `selected_terminal_path` is `response`;
- `response_artifact_path` is required;
- `failure_artifact_path` is absent or null;
- `response_writer_called` may be true only for a future non-dry-run response
  write;
- `failure_writer_called` must remain false.

Failure path semantics:

- `selected_terminal_path` is `failure`;
- `failure_artifact_path` is required;
- `response_artifact_path` is absent or null;
- `failure_writer_called` may be true only for a future non-dry-run failure
  write;
- `response_writer_called` must remain false.

For one invocation, the result must never contain both response and failure
artifact paths.

## Failure Routing Expectations

The future local invocation boundary should route blocking failures as follows:

- reader failure routes to blocking failure path;
- intake mapping failure routes to blocking failure path;
- runtime invocation failure routes to blocking failure path;
- response validation failure routes to blocking failure path;
- response writer failure routes to blocking failure path if writer failure can
  be safely classified.

Failure routing must remain fail-closed. A failure result must not unlock macro
reporting, execute handoff, emit CLI success behavior, poll for replacement
work, retry automatically, or clean up artifacts.

## Strict Blocked Downstream Behavior

This output contract keeps the following downstream behavior blocked:

- no macro report unlock;
- no actual handoff;
- no CLI behavior;
- no queue discovery;
- no polling / retry / cleanup.

The result object must preserve these locked markers:

- `macro_report_unlock` is false;
- `actual_handoff_executed` is false;
- `cli_behavior_added` is false.

## Validation Themes

Future validation should prove:

- result object shape;
- exactly one terminal path;
- no dual artifact paths;
- `macro_report_unlock` false;
- `actual_handoff_executed` false;
- wrapper helpers remain standalone.

## Recommended Next Phase

Recommended next phase:

```text
Local Invocation Boundary Validation Plan Pass
```
