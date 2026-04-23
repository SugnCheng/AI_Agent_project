# Kernel Validation Wrapper Plan

## Purpose

This document defines the smallest governed plan for whether and how the current kernel-side file exchange fixture validation helper should later remain standalone or be included in a broader `ai-meta-kernel` local validation wrapper.

It is a planning document only. It does not add wrapper code, runtime adapter code, live fetching, scheduler runtime, report composition, CI, package migration, external service calls, or actual runtime handoff.

## Current Decision

The current helper should remain standalone for now.

Current helper:

```text
validation/kernel_file_exchange_fixture_checks.py
```

Current success signal:

```text
kernel-file-exchange-fixture-checks-ok
```

Reasoning:

- The helper validates only one narrow fixture set.
- There is no governed `ai-meta-kernel` unified validation wrapper yet.
- Adding a wrapper now would create orchestration surface area before the kernel-side validation baseline is defined.
- Keeping the helper standalone reduces the risk of quietly turning fixture checks into broader runtime validation.

## Conditions For Future Wrapper Inclusion

The helper may be included in a broader kernel-side local validation wrapper only after a governed pass defines:

1. the wrapper path and name;
2. the full list of included validation layers;
3. the execution order;
4. the final success signal;
5. stop-on-first-failure behavior;
6. dependency assumptions, especially `jsonschema`;
7. whether child script output is preserved;
8. which checks remain standalone even after wrapper inclusion;
9. which behaviors the wrapper must never perform.

The fixture helper should not be included in a wrapper until its output contract remains stable:

- `docs/KERNEL_FILE_EXCHANGE_FIXTURE_VALIDATION_OUTPUT_CONTRACT.md`

## Candidate Future Wrapper Scope

A future wrapper, if created, should be local-only and validation-only.

Suggested future location:

```text
ai-meta-kernel/validation/run_all_kernel_local_checks.py
```

Possible future scope:

| Order | Candidate check | Rationale |
| --- | --- | --- |
| 1 | Existing static meta-layer contract checks, if formalized | Validate canonical kernel contracts before adapter-related fixtures. |
| 2 | `validation/kernel_file_exchange_fixture_checks.py` | Validate kernel-side file exchange fixtures after core contracts are stable. |

No broader scope should be assumed until a governed wrapper implementation pass defines it.

## Execution Order Assumptions

If a wrapper is later introduced, execution order matters:

1. Core kernel contract/schema checks should run before file exchange fixture checks.
2. Adapter or fixture checks should not mask failures in canonical Meta-Layer contracts.
3. The wrapper should stop on first failure unless a governed pass explicitly chooses a different behavior.
4. The wrapper should preserve child script output so failure causes remain visible.
5. The wrapper should not reinterpret or downgrade child failures.

## Wrapper Behaviors That Must Remain Blocked

A future wrapper must not silently introduce:

- runtime adapter invocation;
- file exchange runtime artifact reads;
- file exchange runtime artifact writes;
- canonical task object generation from envelopes;
- response artifact generation;
- failure artifact generation;
- artifact polling;
- retry/backoff behavior;
- artifact cleanup automation;
- live fetching;
- scheduler runtime;
- report composition;
- CI behavior;
- package migration;
- external service calls;
- generic multi-profile production validation.

## Changes Requiring A Governed Pass

The following changes require a governed pass before implementation:

- creating a unified kernel validation wrapper;
- adding `kernel_file_exchange_fixture_checks.py` to any wrapper;
- changing the helper success signal;
- changing wrapper success signal;
- changing execution order;
- changing stop-on-first-failure behavior;
- suppressing child script output;
- adding or removing validation layers;
- changing dependency assumptions;
- adding runtime artifact validation;
- broadening fixture validation beyond `daily_us_core`;
- connecting wrapper execution to CI;
- invoking any runtime adapter code.

## Explicit Non-Goals

This plan does not:

- implement a wrapper;
- modify `kernel_file_exchange_fixture_checks.py`;
- modify fixtures;
- modify `TASK_OBJECT_SCHEMA.json`;
- add validation dependencies;
- add CI;
- add runtime file exchange behavior;
- add macro-agent validation behavior.

## Recommended Next Phase

Implement a `Kernel-Side Validation Wrapper Output Contract Planning Pass` only if a broader wrapper becomes necessary.

Otherwise, keep `validation/kernel_file_exchange_fixture_checks.py` standalone until additional kernel-side validation layers are formalized.
