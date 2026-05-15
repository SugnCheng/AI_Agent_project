# Kernel File Exchange Adapter Terminal Writer Implementation Output Contract

## Purpose

This document snapshots the output contract for a future minimal terminal writer implementation slice.

It is a preparation contract only. It does not authorize writer code, response artifact writing, failure artifact writing, CLI behavior, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Contract Decision

Current Phase R12 output contract decision:

```text
future_terminal_writers_emit_exactly_one_artifact_or_fail_closed
```

Future terminal writers may output exactly one terminal artifact for one invocation:

- one written kernel response artifact; or
- one written blocking kernel exchange failure artifact.

They must never output both for the same invocation.

## Future Response Writer Output

The future response writer may output:

```text
one_written_kernel_response_artifact
```

Only after a validated pre-writer response input is accepted by a governed writer implementation boundary.

The future response artifact must:

- be produced by `ai-meta-kernel`;
- be a JSON object;
- use governed response artifact naming;
- preserve canonical response fields;
- pass required pre-write validation;
- not be written if failure writer output has already been selected for the same invocation.

## Future Failure Writer Output

The future failure writer may output:

```text
one_written_blocking_kernel_exchange_failure_artifact
```

Only after a local classified blocking failure input is accepted by a governed writer implementation boundary.

The future failure artifact must:

- be produced by `ai-meta-kernel` or a thin kernel-owned adapter boundary;
- be a JSON object;
- use governed failure artifact naming;
- declare `artifact_type == "kernel_exchange_failure"`;
- declare `blocking == true`;
- include governed failure stage and reason fields;
- contain no partial canonical task object content;
- not be written if response writer output has already been selected for the same invocation.

## Prohibited Outputs

Future terminal writer output must not include:

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

Future writer implementation must not repair invalid response objects, synthesize missing failure fields, infer terminal artifact names from ambiguous context, or silently skip mutual-exclusivity checks.

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
- adding writer code;
- adding CLI, queue discovery, polling, retry, cleanup, scheduler behavior, live fetching, report composition, CI, package migration, or external service calls.

## Explicit Non-Authorization

This contract authorizes no code implementation in Phase R12. It prepares only the future terminal writer output boundary for a later governed implementation slice.
