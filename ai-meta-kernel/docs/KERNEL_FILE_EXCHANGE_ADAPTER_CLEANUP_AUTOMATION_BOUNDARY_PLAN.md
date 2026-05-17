# Kernel File Exchange Adapter Cleanup Automation Boundary Plan

## Purpose

This note prepares the cleanup automation boundary after the runtime artifact
policy milestone sync.

It is a boundary preparation document only. It does not implement cleanup
automation, artifact deletion, filesystem mutation, fixture promotion
automation, CLI behavior, queue discovery, polling, retry, scheduler behavior,
macro report unlock, actual handoff, wrapper inclusion, production
cross-project exchange, or full runtime orchestration.

## Current Boundary Decision

Current boundary decision:

```text
cleanup_automation_boundary_preparation_baseline
```

## Why Cleanup Automation Is Not Yet Implemented

Cleanup automation is not yet implemented because:

- runtime artifacts can exist after bounded local invocation;
- the runtime artifact policy helper validates policy object semantics only;
- deletion, mutation, and cleanup side effects require separate governance;
- fixture promotion must remain review-gated.

## Intended Future Cleanup Purpose

Future cleanup automation may eventually:

- identify generated local runtime artifacts;
- distinguish reviewable artifacts from disposable temporary validation
  artifacts;
- apply explicit governed cleanup policy only;
- avoid deleting committed fixtures or promotion candidates;
- avoid cleanup side effects during validation helpers.

## Intended Future Input Surface

A future cleanup boundary may accept only:

- explicit artifact path or explicit artifact manifest;
- explicit policy object;
- explicit cleanup mode if governed later.

The future input surface must not include:

- queue discovery;
- scheduler input;
- implicit directory sweeping.

## Intended Future Output Surface

A future cleanup boundary may produce:

- cleanup decision object.

The future output surface must preserve:

- no deletion unless separately implemented later;
- no macro report unlock;
- no actual handoff;
- no CLI marker.

## Explicit Blocked Behaviors

The following remain blocked:

- cleanup automation implementation;
- artifact deletion;
- filesystem mutation;
- fixture promotion automation;
- fixture promotion without review;
- implicit directory sweeping;
- CLI;
- queue discovery;
- polling / watcher;
- retry / backoff;
- scheduler;
- macro report unlock;
- actual handoff;
- wrapper inclusion;
- production cross-project exchange.

## Future Validation Themes

Future validation should prove:

- explicit input only;
- committed fixtures are never deleted;
- promoted fixture candidates require review;
- generated artifacts require a policy object;
- dry-run candidates are not deleted by default;
- temporary validation artifacts may only be cleanup candidates after governed
  policy;
- `macro_report_unlock` remains false;
- `actual_handoff_executed` remains false;
- `cli_behavior_added` remains false.

## Recommended Next Phase

Recommended next phase:

```text
Cleanup Automation Boundary Output Contract Pass
```
