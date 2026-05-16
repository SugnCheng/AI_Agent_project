# Kernel File Exchange Adapter Blocking Failure Classification Preparation

## Purpose

This note defines the smallest preparation boundary for future blocking failure classification before failure writer implementation.

It is documentation only. It does not add code, implement failure classification, implement the failure writer, write artifacts, update validation baselines, unlock macro reporting, or execute handoff.

## Current Decision

Current decision:

```text
blocking_failure_classification_preparation_baseline
```

## Why Failure Writer Cannot Proceed Directly

The failure writer cannot proceed directly because the adapter does not yet have a governed local classified blocking failure input boundary.

If failure writer implementation opened before that boundary exists, writer code would have to decide how reader, envelope validation, intake mapping, runtime invocation, response validation, and response writer errors are classified. That would mix failure classification with terminal artifact writing and would weaken the current one-invocation / one-terminal-artifact contract.

The future failure writer must receive an already classified blocking failure object. It must not invent failure type, stage, code, blocking status, macro unlock status, or artifact-writing flags.

## Intended Future Input

The intended future input is:

```text
local_classified_blocking_failure_object
```

This object should be local, explicit, and produced before any failure artifact writer boundary is called.

## Intended Future Output

The intended future output of the classification boundary is:

```text
classified_failure_object_only
```

The classification boundary must not write a failure artifact. Failure artifact writing remains a separate future terminal writer slice.

## Classification Scope

The future classification boundary should cover blocking failures from:

- reader failure;
- envelope validation failure;
- intake mapping failure;
- runtime invocation failure;
- response validation failure;
- response writer failure.

## Required Future Fields

The future classified blocking failure object should include governed fields equivalent to:

- `failure_type`;
- `failure_stage`;
- `failure_code`;
- `failure_message`;
- `source_boundary`;
- `is_blocking`;
- `terminal_artifact_written`;
- `response_artifact_written`;
- `failure_artifact_written`;
- `macro_report_unlock`.

These fields are preparation targets only. This pass does not implement their validation or construction.

## Explicitly Blocked Behaviors

This preparation pass keeps the following blocked:

- no failure writer;
- no failure artifact writing;
- no CLI;
- no retry / polling / cleanup;
- no macro report unlock;
- no actual handoff.

## Recommended Next Phase

Recommended next phase:

```text
Blocking Failure Classification Minimal Implementation Slice
```

That phase should implement the smallest local classified blocking failure object boundary and stop before failure artifact writing, CLI behavior, retry / polling / cleanup, macro report unlock, and actual handoff.
