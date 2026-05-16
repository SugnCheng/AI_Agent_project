# Kernel File Exchange Adapter Local Invocation Implementation Gate

## Purpose

This note refreshes the implementation gate for the kernel-side local
invocation boundary after the R25 boundary plan, R26 output contract, and R27
validation plan.

It decides whether the next governed phase may open the minimal local
invocation implementation slice. It does not implement local invocation code,
validation helper code, CLI behavior, queue discovery, polling, retry, cleanup,
scheduler behavior, macro report unlock, actual handoff, wrapper inclusion, or
full runtime orchestration.

## Current Gate Decision

Current gate decision:

```text
local_invocation_implementation_gate_refreshed
```

The minimal local invocation implementation slice may be opened next, but only
under the bounded shape defined by this gate.

## Prerequisites Now In Place

The following prerequisites are now in place:

- R25 local invocation boundary plan exists;
- R26 local invocation output contract exists;
- R27 local invocation validation plan exists;
- minimal reader exists;
- minimal intake mapper exists;
- candidate-only invocation exists;
- local response validation exists;
- response writer exists;
- blocking failure classification exists;
- failure writer exists;
- local terminal writer dry-run exists.

## Implementation Readiness Assessment

Minimal local invocation implementation may be opened next.

That opening is allowed only if it remains bounded to explicit local input and
explicit local output destination policy.

That opening must not add CLI behavior, queue discovery, polling, retry,
cleanup, macro report unlock, or actual handoff.

Any future helper must remain standalone unless wrapper inclusion is separately
governed.

## Allowed Next Implementation Shape

The next implementation slice may include only:

- one explicit envelope path;
- one explicit output destination policy;
- one deterministic local invocation result object;
- exactly one selected terminal path;
- one response artifact path or one failure artifact path;
- never both;
- `macro_report_unlock` false;
- `actual_handoff_executed` false;
- `cli_behavior_added` false.

## Blocked Behaviors

This gate keeps the following blocked:

- CLI;
- queue discovery;
- polling / watcher;
- retry / backoff;
- cleanup;
- scheduler;
- live fetching;
- report composition;
- macro report unlock;
- actual handoff;
- wrapper inclusion;
- full runtime orchestration.

## Recommended Next Phase

Recommended next phase:

```text
Local Invocation Minimal Implementation Slice
```
