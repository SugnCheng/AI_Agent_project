# Kernel File Exchange Adapter Implementation Gate

## Purpose

This note defines the implementation gate for beginning actual kernel-side file exchange adapter work in `ai-meta-kernel`.

It is a developer-facing gate note only. It does not implement runtime handoff, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or changes to kernel contracts.

## Gate Decision

Current decision:

```text
runtime_adapter_implementation_gate_not_yet_open
```

The projects are aligned enough for a kernel-side adapter fixture planning pass. They are not yet ready for actual runtime handoff or response/failure artifact writing.

The next acceptable step is planning and fixture strategy for the kernel-side adapter boundary, not runtime execution.

## Already Satisfied Prerequisites

The following prerequisites are already satisfied:

| Area | Current status |
| --- | --- |
| Cross-project authority | `ai-meta-kernel` remains upstream reasoning authority; macro agent remains downstream evidence pipeline. |
| Interface choice | v0.1 file-based envelope / response exchange is selected. |
| Macro evidence boundary | Macro agent can prepare evidence/context without generating canonical kernel task objects. |
| Macro envelope path | Macro agent can build and write governed kernel input envelope artifacts. |
| Macro response read path | Macro agent can read and classify standard, restricted, blocked, and failure fixture states. |
| Kernel adapter contract | Kernel-side adapter boundary, ownership, response/failure responsibilities, and drift rules are documented. |
| Kernel scaffold boundary | Current scaffold keeps runtime invocation, intake preparation, response writing, and failure writing fail-closed. |
| Kernel validation surface | Static contract checks, file-exchange fixture checks, adapter scaffold checks, wrapper checks, and wrapper failure-path checks exist. |
| Cross-project status | Current status snapshot confirms file-based exchange alignment while runtime handoff remains unimplemented. |

## Unsatisfied Prerequisites

The following prerequisites remain unsatisfied before actual runtime adapter implementation can begin:

| Missing prerequisite | Why it blocks implementation |
| --- | --- |
| Kernel-side envelope fixture strategy | The adapter needs a stable static fixture target before runtime file reader behavior expands. |
| Kernel-side response/failure fixture strategy | Response and failure writer behavior needs expected fixture shapes before implementation. |
| Envelope-to-P0/P1 intake decision | The mapping from envelope evidence/context into kernel-owned intake must be defined without weakening `RUNTIME_PIPELINE.md`. |
| Kernel-owned task object production path | The kernel must own canonical task object construction; macro-side substitutes remain forbidden. |
| Runtime invocation boundary | The future P0-P10 invocation entrypoint is not implemented or exposed. |
| Response writer output contract | The exact writer behavior, validation order, and output signal need a governed pass. |
| Failure writer output contract | Blocking failure artifact creation semantics need a governed implementation contract. |
| Operator review checkpoint | Restricted and blocked outputs need a defined review surface before reporting unlocks. |
| Runtime artifact retention decision | Generated artifact retention, promotion to fixtures, and cleanup remain governed future decisions. |

## First Acceptable Implementation Slice

The first acceptable implementation slice, after a fixture planning pass, should be:

```text
kernel_side_file_exchange_adapter_fixture_validation_slice
```

That slice may include only:

- one committed static kernel input envelope fixture or a clearly documented fixture strategy;
- local validation that the fixture satisfies the existing envelope intake contract;
- local validation that the fixture does not contain completed canonical task object conclusions;
- local validation that the current scaffold keeps blocked boundaries fail-closed;
- output contract documentation for the new validation helper if one is added;
- no runtime invocation.

The slice should preserve the current adapter scaffold boundary:

```text
read envelope artifact
-> validate envelope intake
-> stop before kernel intake preparation and runtime invocation
```

## What Must Remain Blocked In The First Slice

The first implementation slice must not include:

- P0-P10 runtime invocation;
- kernel-owned canonical task object generation;
- response artifact writing;
- failure artifact writing;
- CLI command design;
- artifact polling or watcher behavior;
- retry/backoff behavior;
- artifact cleanup automation;
- multi-profile runtime expansion;
- live fetching;
- scheduler runtime;
- report composition;
- archive/export automation;
- CI behavior;
- package migration;
- external service calls;
- changes to `META_LAYER_MASTER_SPEC.md`;
- changes to `meta-layer/RUNTIME_PIPELINE.md`;
- changes to `meta-layer/HANDOFF_CONTRACT.md`;
- changes to `meta-layer/TASK_OBJECT_SCHEMA.json`;
- any macro-side production of kernel response artifacts.

## Conditions To Open Actual Runtime Adapter Implementation

Actual runtime adapter implementation should not begin until all of the following are true:

1. Kernel-side envelope fixture strategy is documented.
2. Expected response and failure fixture strategy is documented.
3. Envelope intake validation is covered by local kernel-side validation.
4. Existing kernel validation wrapper still passes.
5. Existing wrapper failure-path helper still passes.
6. Macro unified local validation still passes.
7. Envelope-to-P0/P1 mapping is defined as kernel-owned intake, not macro-owned reasoning.
8. Response writer behavior is governed by an output contract before implementation.
9. Failure writer behavior is governed by an output contract before implementation.
10. Restricted, blocked, failed, missing, and ambiguous states remain blocking or review-gated before reporting.

## Explicit Non-Goals

This gate note must not silently introduce:

- runtime adapter invocation;
- P0-P10 runtime execution;
- canonical task object generation from envelopes;
- response artifact writing;
- failure artifact writing;
- live fetching;
- uncontrolled open-web crawling;
- scheduler runtime;
- report composition;
- archive/export automation;
- CI integration;
- package migration;
- external service calls;
- source governance changes;
- schema drift;
- hidden runtime handoff.

## Recommended Next Phase

Implement a `Kernel-Side File Exchange Adapter Fixture Planning Pass`.

That pass should define the smallest static kernel-side envelope fixture and expected response/failure fixture strategy for testing the adapter boundary before any runtime reader expansion, response writer, failure writer, CLI, CI, scheduler behavior, live fetching, report composition, package migration, or actual handoff execution is added.
