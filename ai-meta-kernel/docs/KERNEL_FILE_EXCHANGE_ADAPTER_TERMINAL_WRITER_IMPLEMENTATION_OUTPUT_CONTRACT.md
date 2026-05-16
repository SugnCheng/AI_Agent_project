# Kernel File Exchange Adapter Terminal Writer Implementation Output Contract

## Purpose

This document snapshots the output contract for terminal writer implementation slices.

It records that the minimal response writer is implemented in Phase R14 and the minimal failure writer is implemented in Phase R19. It does not authorize local orchestration, CLI behavior, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, macro report unlock, or actual runtime handoff.

## Contract Decision

Current Phase R12 output contract decision:

```text
future_terminal_writers_emit_exactly_one_artifact_or_fail_closed
```

Future terminal writers may output exactly one terminal artifact for one invocation:

- one written kernel response artifact; or
- one written blocking kernel exchange failure artifact.

They must never output both for the same invocation.

Current Phase R14 response writer status:

```text
response_writer_minimal_implementation_slice_complete
```

Current Phase R19 failure writer status:

```text
failure_writer_minimal_implementation_slice_complete
```

## Current Minimal Response Writer Output

The current R14 minimal response writer may output:

```text
one_written_kernel_response_artifact
```

Only after the current R10 validated pre-writer response input is accepted by the R14 writer boundary.

The current response artifact must:

- be produced by `ai-meta-kernel`;
- be a JSON object;
- declare `artifact_type == "kernel_response"`;
- declare `artifact_state == "written_response_artifact"`;
- preserve the source validated response under a governed source field;
- declare `terminal_artifact_written == true`;
- declare `response_writer_called == true`;
- declare `failure_writer_called == false`;
- declare `macro_report_unlock == false`;
- use an explicit local destination that does not already exist;
- not write or prepare a failure artifact.

## Current Minimal Failure Writer Output

The current R19 minimal failure writer may output:

```text
one_written_blocking_kernel_exchange_failure_artifact
```

Only after a local classified blocking failure input is accepted by the R19 writer boundary.

The current failure artifact must:

- be produced by `ai-meta-kernel` or a thin kernel-owned adapter boundary;
- be a JSON object;
- use governed failure artifact naming;
- declare `artifact_type == "kernel_exchange_failure"`;
- declare `blocking == true`;
- include governed failure stage and reason fields;
- contain no partial canonical task object content;
- not be written if response writer output has already been selected for the same invocation.

## Prohibited Outputs

Terminal writer output must not include:

- both response and failure artifacts for one invocation;
- report eligibility signal;
- macro-side report unlock;
- CLI success signal;
- external-service result;
- scheduler result;
- cleanup decision;
- fixture promotion decision;
- partial canonical task object fallback;
- non-blocking failure artifact.

## Failure Behavior

Invalid writer input must fail closed.

The current response writer must not repair invalid validated response objects, synthesize missing kernel conclusions, infer terminal artifact names from ambiguous context, overwrite existing destination paths, or silently skip failure-writer closure checks.

Future failure writer implementation must not synthesize missing failure fields, infer terminal artifact names from ambiguous context, or silently skip mutual-exclusivity checks.

If neither terminal artifact can be safely written, that fatal local condition must remain explicit until a separately governed fatal-error policy exists.

## Stop Boundary

The future terminal writer output contract stops at:

```text
written terminal artifact
```

It does not authorize:

- CLI behavior;
- macro-side reporting;
- scheduler behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- cleanup automation;
- actual runtime handoff.

## Governed Change Triggers

The following require a governed pass before implementation:

- changing response artifact naming semantics;
- changing failure artifact naming semantics;
- changing response writer input beyond one validated pre-writer response;
- changing failure writer input beyond one classified blocking failure;
- allowing both artifacts for one invocation;
- allowing non-blocking failure artifacts;
- allowing macro report unlock from writer output;
- broadening response writer code beyond the R14 minimal explicit-destination writer;
- adding failure writer code;
- adding CLI, queue discovery, polling, retry, cleanup, scheduler behavior, live fetching, report composition, CI, package migration, or external service calls.

## Current Milestone Limit

This contract records the R14 minimal response writer output and the R19 minimal failure writer output. It does not authorize response writer broadening, failure writer broadening, local terminal writer dry-run orchestration, CLI behavior, macro report unlock, or actual runtime handoff.
