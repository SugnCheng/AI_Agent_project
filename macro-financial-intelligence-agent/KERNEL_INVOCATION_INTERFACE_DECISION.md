# Kernel Invocation Interface Decision

## Purpose

This document decides the smallest acceptable v0.1 interface for a future handoff from `macro-financial-intelligence-agent` to `ai-meta-kernel`.

It is a decision document only. It does not implement runtime handoff, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or canonical task object generation inside the macro agent.

## Decision Summary

Recommended v0.1 interface:

**File-based envelope / response exchange.**

In v0.1, the macro agent should eventually write or provide a validated kernel input envelope as a JSON artifact, then receive a kernel-produced `TASK_OBJECT_SCHEMA.json` response artifact. The macro agent may validate the response and enforce blocked / restricted states, but must not generate the canonical task object itself.

## Candidate Options

| Option | Description | Pros | Cons | v0.1 decision |
| --- | --- | --- | --- | --- |
| Local CLI boundary | Macro invokes a kernel CLI command and passes an envelope path or stdin JSON. | Simple operator mental model; easy to script later; good separation between projects. | Requires defining CLI args, stdout/stderr contract, exit codes, and artifact handling. | Defer. Useful after file contract is stable. |
| Local Python function boundary | Macro imports or calls a kernel Python function directly. | Fastest in-process path; easiest to unit test once package layout exists. | Pushes toward package migration/import coupling; risks making macro depend on kernel internals; harder to preserve project separation now. | Do not choose for v0.1. |
| File-based envelope / response exchange | Macro prepares an envelope JSON artifact; kernel consumes it and emits a response JSON artifact. | Smallest explicit contract; preserves project separation; no package migration; easy to inspect, diff, archive, and validate; compatible with later CLI. | More manual at first; requires artifact naming/location rules; not an execution mechanism by itself. | Choose for v0.1. |

## Why File-Based Exchange Is Smallest Acceptable Now

The current repo already has:

- deterministic kernel input envelope construction;
- explicit non-impersonation guardrails;
- response validation against `TASK_OBJECT_SCHEMA.json`;
- static response fixtures for `standard`, `restricted`, and `blocked`;
- local validation helpers for response-state classification.

The missing piece is not execution speed. The missing piece is a stable boundary contract.

File-based exchange solves that first:

1. The macro agent can preserve its role as evidence/context producer.
2. The kernel can preserve ownership of P0-P10.
3. Both sides can inspect exactly what crossed the boundary.
4. The response can be validated before any downstream reporting unlocks.
5. No package migration, service runtime, or CLI contract is required yet.

## Proposed v0.1 Boundary Shape

This decision does not implement the boundary, but the eventual shape should be:

```text
macro agent:
  build validated kernel input envelope
  write envelope JSON artifact

ai-meta-kernel:
  read envelope JSON artifact
  run P0-P10 runtime pipeline
  write kernel response JSON artifact conforming to TASK_OBJECT_SCHEMA.json

macro agent:
  validate response JSON artifact
  classify response state as standard / restricted / blocked
  keep reporting blocked unless kernel handoff permits continuation
```

## Minimal Artifact Expectations

The future envelope artifact should preserve the current envelope contract:

- `envelope_type`
- `envelope_version`
- `source_project`
- `profile_id`
- `run_mode`
- `report_target`
- `regions`
- `operator_intent`
- `evidence_bundle`
- `evidence_context`
- `kernel_task_object_expectation`
- `deferred_runtime_behavior`

The future kernel response artifact must conform to:

- `../ai-meta-kernel/meta-layer/TASK_OBJECT_SCHEMA.json`

The macro agent must continue to treat these as separate artifact classes:

- macro-produced envelope artifact;
- kernel-produced task object artifact.

## Required Guardrails

- The macro agent must not write a completed canonical task object.
- The macro agent must not fill kernel-owned conclusions into the envelope.
- The kernel must own P0-P10 from intake through handoff.
- A schema-valid response is necessary but not sufficient; blocked / restricted state detection still applies.
- `do_not_handoff`, `needs_reframe`, `needs_user_clarification`, and `handoff_ready == false` must block downstream reporting.
- `restricted_handoff` and restricting flags must preserve downstream restrictions.
- File-based exchange must not imply live fetching, scheduler execution, or report composition.

## Tradeoffs

### Benefits

- Keeps the two sibling projects decoupled.
- Avoids premature package migration.
- Makes envelope and response artifacts reviewable.
- Makes regression testing straightforward.
- Leaves room for a later CLI wrapper without changing the core artifact contract.

### Costs

- Requires explicit artifact paths and naming conventions in a future pass.
- Does not by itself execute kernel runtime.
- May be less ergonomic than a direct Python function call.
- Requires cleanup / retention policy decisions before production use.

## Explicitly Deferred

Choosing file-based exchange does not authorize:

- actual kernel runtime implementation;
- CLI wrapper implementation;
- Python package migration;
- direct Python imports from macro into kernel runtime internals;
- live fetching;
- scheduler runtime;
- report composition;
- archive/export automation;
- external service calls;
- CI integration;
- multi-profile production orchestration;
- automatic artifact persistence or retention policy.

## Open Decisions For Next Pass

The next governed pass should decide:

1. Envelope artifact directory.
2. Kernel response artifact directory.
3. Artifact naming convention.
4. Whether artifacts are committed fixtures, ignored runtime outputs, or both in separate locations.
5. Minimal metadata required for traceability.
6. Transport-level failure format when kernel runtime cannot produce a valid task object.
7. Whether the existing boundary scaffold should gain a write-envelope-only mode.

## Recommended Next Phase

Implement a `File-Based Kernel Exchange Contract Pass`.

That pass should define artifact paths, filenames, expected JSON shapes, and failure artifacts. It should still avoid actual runtime invocation, live fetching, scheduler runtime, and report composition.
