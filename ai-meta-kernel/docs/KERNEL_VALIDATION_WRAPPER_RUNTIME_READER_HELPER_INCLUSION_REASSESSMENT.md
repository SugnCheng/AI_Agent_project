# Kernel Validation Wrapper Runtime Reader Helper Inclusion Reassessment

## Purpose

This note reassesses whether the standalone runtime envelope reader contract helper should be added to the main kernel local validation wrapper for the next milestone.

This is a documentation-only reassessment. It does not modify wrapper behavior, runtime behavior, kernel contracts, or validation helper code.

## Current Reassessment Decision

Decision:

```text
runtime_reader_contract_helper_remains_standalone_outside_main_wrapper_for_next_milestone
```

The standalone helper remains:

```text
validation/kernel_runtime_envelope_reader_contract_checks.py
```

Its standalone success signal remains:

```text
kernel-runtime-envelope-reader-contract-checks-ok
```

The main wrapper remains:

```text
validation/run_all_kernel_local_checks.py
```

The main wrapper success signal remains:

```text
kernel-local-validation-checks-ok
```

## Reasons To Keep The Helper Standalone

Keeping the runtime reader helper standalone preserves the current wrapper output contract. The wrapper success signal currently means that the stable kernel-local validation wrapper checks passed, not that every future runtime adapter boundary helper has been promoted into default wrapper scope.

The runtime envelope reader boundary is still a governed future implementation boundary. Its helper validates contract shape and blocked behavior expectations, but it does not implement runtime reader behavior and does not perform runtime handoff.

Keeping it standalone also keeps failure diagnosis narrow while the reader boundary remains pre-runtime. A wrapper inclusion pass would broaden wrapper scope and require coordinated documentation, failure-path, and baseline updates.

## Reasons To Include Later

The helper may be considered for wrapper inclusion only after a governed pass decides that runtime envelope reader contract validation is part of the default kernel-local validation surface.

Before inclusion, the project should confirm that the helper's scope is stable enough to be covered by the wrapper success signal, that its failure behavior is appropriate for default local checks, and that wrapper failure-path validation remains accurate after the helper list changes.

## Impact If Inclusion Happened

If the helper were added to the main wrapper, the final wrapper success signal:

```text
kernel-local-validation-checks-ok
```

would also imply that the runtime envelope reader contract helper passed. That would broaden the meaning of wrapper success beyond the current three-helper baseline.

Wrapper inclusion would also change the expected execution order, failure propagation surface, and later-helper suppression expectations covered by wrapper failure-path validation.

## Governed Passes Required Before Inclusion

Future inclusion requires a governed wrapper inclusion implementation pass that updates `validation/run_all_kernel_local_checks.py` intentionally.

That pass must be accompanied by:

- a wrapper output contract refresh
- a wrapper failure-path helper reassessment or update
- a validation baseline refresh
- a validation documentation index refresh
- a reader helper relationship update if the standalone status changes
- confirmation that no runtime reader implementation, queue discovery, polling, retry, cleanup, CLI, or runtime invocation is introduced by inclusion

## Behaviors That Remain Blocked

The following remain explicitly blocked at this milestone:

- adding the reader helper to `validation/run_all_kernel_local_checks.py`
- changing the wrapper success signal
- changing the wrapper helper order
- modifying kernel contracts
- implementing runtime envelope reading
- implementing intake mapping
- invoking P0/P1 or broader kernel runtime
- writing response or blocking failure artifacts
- adding queue discovery, polling, retry, cleanup, or CLI behavior
- adding live fetching, scheduler runtime, report composition, CI, package migration, or external service calls

## Recommended Next Phase

Refresh the kernel validation baseline so it records this reassessment decision alongside the existing wrapper inclusion gate, while preserving that the reader helper remains standalone and the main wrapper remains unchanged.
