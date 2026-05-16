# Kernel File Exchange Adapter Local Invocation Boundary Plan

## Purpose

This note prepares the kernel-side local invocation boundary after the terminal
writer dry-run milestone sync.

It defines the intended future boundary, inputs, outputs, stop conditions, and
validation themes. It does not implement local invocation code, CLI behavior,
queue discovery, polling, retry, cleanup, macro report unlock, actual handoff,
or scheduler/runtime orchestration.

## Current Boundary Decision

Current boundary decision:

```text
local_invocation_boundary_preparation_baseline
```

This preparation baseline records that terminal writer local surfaces are
dry-run testable, but no governed local invocation implementation exists yet.

## Why Local Invocation Is Not Yet Implemented

Local invocation is not yet implemented because the repository still needs a
separate output contract for the local invocation result object and terminal
artifact path semantics.

The current implemented surfaces are intentionally smaller:

- explicit-file envelope reader;
- context-only `kernel_intake_context` mapper;
- candidate-only runtime invocation;
- local pre-writer response validation;
- explicit-destination response writer;
- blocking failure classification;
- explicit-destination failure writer;
- terminal writer dry-run artifact candidates.

Those pieces do not yet define a single governed local run boundary. Adding
that boundary before its output contract is fixed would risk silently creating
CLI behavior, artifact discovery, retry behavior, cleanup behavior, macro report
unlock, or actual handoff semantics.

## Intended Future Local Invocation Purpose

The future local invocation boundary should support:

- one explicit local envelope input;
- one local deterministic adapter run;
- a strict stop before CLI behavior, queue discovery, polling, retry, cleanup,
  macro report unlock, actual handoff, scheduler behavior, and report
  composition.

It should remain a kernel-side local invocation boundary only. It must not
become a macro-agent scheduler, queue processor, or report unlock mechanism.

## Intended Future High-Level Path

The intended future path is:

1. read envelope;
2. prepare intake context;
3. perform candidate-only invocation;
4. run local response validation;
5. select one terminal path;
6. write one response artifact or one failure artifact;
7. never write both for the same invocation.

If any required stage fails before a valid response artifact can be produced,
the future boundary should route to the governed blocking failure path rather
than continue silently.

## Intended Future Input Surface

The future input surface should remain explicit and local:

- explicit envelope path;
- explicit output directory or explicit destination policy;
- optional `dry_run` flag, if governed later.

The future input surface should not include queue directories, implicit runtime
discovery, scheduler configuration, report targets that unlock downstream
reporting, or external service configuration.

## Intended Future Output Surface

The future output surface should include:

- local invocation result object;
- one terminal artifact path candidate or written artifact path, depending on
  the future implementation decision;
- no macro report unlock;
- no actual handoff marker.

The output contract must preserve terminal mutual exclusivity: a single local
invocation may produce a response path or a failure path, never both.

## Explicit Blocked Behaviors

This preparation baseline keeps the following blocked:

- CLI;
- queue discovery;
- polling / watcher behavior;
- retry / backoff;
- cleanup;
- scheduler;
- report composition;
- macro report unlock;
- actual handoff.

## Required Future Validation Themes

Future validation should prove:

- explicit input only;
- exactly one terminal path;
- no dual-write;
- existing destination rejected;
- failed stage produces blocking failure path;
- `macro_report_unlock` remains false;
- standalone helpers remain outside wrapper.

## Recommended Next Phase

Recommended next phase:

```text
Local Invocation Boundary Output Contract Pass
```
