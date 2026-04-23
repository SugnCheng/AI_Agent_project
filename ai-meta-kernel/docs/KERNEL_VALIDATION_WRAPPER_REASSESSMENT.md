# Kernel Validation Wrapper Reassessment

## Purpose

This document reassesses whether the current kernel-side standalone validation helpers are sufficient to justify wrapper planning or wrapper inclusion.

It records a governed decision only. It does not add wrapper code, runtime adapter code, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Current Standalone Helpers

The current kernel-side validation helpers are:

| Helper | Scope | Success signal |
| --- | --- | --- |
| `validation/kernel_file_exchange_fixture_checks.py` | Validates the static `daily_us_core` envelope, response, and failure fixtures. | `kernel-file-exchange-fixture-checks-ok` |
| `validation/kernel_file_exchange_adapter_scaffold_checks.py` | Exercises the current adapter scaffold boundary against the same static fixtures and confirms blocked boundaries remain fail-closed. | `kernel-file-exchange-adapter-scaffold-checks-ok` |

Both helpers are local, static, fixture-scoped, and `daily_us_core` scoped.

## Current Output Contracts

The helpers already have output contracts:

- `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_OUTPUT_CONTRACT.md`
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_SCAFFOLD_CHECK_OUTPUT_CONTRACT.md`

These contracts fix each helper's execution scope, success signal, expected failure behavior, and drift rules.

## Reassessment

The current helper set is now larger than when `docs/KERNEL_VALIDATION_WRAPPER_PLAN.md` was first written, but it is still narrow.

Current observations:

1. There are two standalone helpers, not a broad validation suite.
2. Both helpers exercise one file-exchange fixture family.
3. Neither helper validates the full Meta-Layer baseline.
4. Neither helper invokes runtime behavior.
5. Neither helper writes response or failure artifacts.
6. Neither helper needs orchestration to preserve correctness.
7. A wrapper would currently add a third coordination surface before there is enough validation breadth to justify it.

## Governed Decision

Keep the current kernel-side validation helpers standalone for now.

Do not begin wrapper implementation yet.

Reasoning:

- The helpers remain narrow and independently understandable.
- Each helper already has a stable output contract.
- A wrapper would add orchestration overhead without materially improving validation coverage.
- There is still no formal static Meta-Layer baseline validation helper to run before file-exchange checks.
- Introducing a wrapper now could imply a broader kernel validation baseline than currently exists.

## Conditions For Future Wrapper Planning

Wrapper planning becomes justified when at least one of the following is true:

1. A static Meta-Layer contract/schema validation helper is added.
2. More than two standalone kernel-side validation helpers exist and their execution order matters.
3. File-exchange adapter checks begin depending on prior core-kernel contract checks.
4. A governed baseline requires one command to prove kernel-side local validation health.
5. Human review burden increases because standalone commands become hard to track.

Before wrapper implementation, a governed pass must define:

- wrapper path and name;
- included validation layers;
- execution order;
- final success signal;
- stop-on-first-failure behavior;
- child output preservation behavior;
- dependency assumptions, especially `jsonschema`;
- which helpers remain standalone;
- which runtime behaviors remain blocked.

## Wrapper Behaviors That Remain Blocked

A future wrapper must not silently introduce:

- runtime adapter invocation;
- P0-P10 runtime invocation;
- canonical task object generation from envelopes;
- response artifact writing;
- failure artifact writing;
- runtime artifact reads or writes;
- artifact polling;
- retry/backoff behavior;
- artifact cleanup automation;
- live fetching;
- scheduler runtime;
- report composition;
- CI behavior;
- package migration;
- external service calls.

## Recommended Next Phase

Implement a `Kernel-Side Static Meta-Layer Contract Check Planning Pass`.

That pass should decide whether the kernel needs a standalone static check for canonical files such as:

- `META_LAYER_MASTER_SPEC.md`
- `meta-layer/RUNTIME_PIPELINE.md`
- `meta-layer/HANDOFF_CONTRACT.md`
- `meta-layer/TASK_OBJECT_SCHEMA.json`

Only after such a core-kernel check exists should wrapper planning be reconsidered.
