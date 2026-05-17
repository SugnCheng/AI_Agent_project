# Kernel File Exchange Adapter Cleanup Automation Boundary Validation Plan

## Purpose

This note defines the future validation plan for cleanup automation boundary
outputs after the R39 boundary preparation baseline and R40 output contract.

It is a validation plan only. It does not implement validation helper code,
cleanup automation, artifact deletion, filesystem mutation, fixture promotion
automation, CLI behavior, queue discovery, polling, retry, scheduler behavior,
macro report unlock, actual handoff, wrapper inclusion, production
cross-project exchange, or full runtime orchestration.

## Current Validation Decision

Current validation decision:

```text
cleanup_automation_boundary_validation_plan_baseline
```

## Validation Scope

Future validation should cover:

- future cleanup decision object shape;
- cleanup eligibility semantics;
- cleanup decision semantics;
- artifact category handling;
- strict locked markers;
- fail-closed behavior;
- wrapper stance.

## Cleanup Decision Object Shape Validation

Future validation should require fields equivalent to:

- `cleanup_type`;
- `cleanup_state`;
- `cleanup_stage`;
- `source_artifact_path`;
- `artifact_category`;
- `policy_reference`;
- `cleanup_eligibility`;
- `cleanup_decision`;
- `deletion_allowed`;
- `filesystem_mutation_allowed`;
- `fixture_promotion_allowed`;
- `manual_review_required`;
- `macro_report_unlock`;
- `actual_handoff_executed`;
- `cli_behavior_added`.

## Cleanup Eligibility Validation Themes

Future validation should prove:

- only valid cleanup eligibility values are accepted:
  - `not_eligible`;
  - `eligible_for_review_only`;
  - `eligible_for_future_cleanup_policy`;
  - `blocked`;
  - `deferred`;
- unknown eligibility value is rejected;
- eligibility must not imply deletion;
- eligibility must not imply filesystem mutation;
- eligibility must not imply fixture promotion.

## Cleanup Decision Validation Themes

Future validation should prove:

- only valid cleanup decision values are accepted:
  - `cleanup_not_implemented`;
  - `cleanup_blocked`;
  - `cleanup_deferred`;
  - `review_required`;
  - `no_action`;
- unknown cleanup decision is rejected;
- `cleanup_not_implemented` means no cleanup action;
- `cleanup_blocked` prevents deletion;
- `cleanup_deferred` does not trigger deletion;
- `review_required` does not equal automatic approval;
- `no_action` does not mutate filesystem.

## Artifact Category Validation Themes

Future validation should prove:

- `committed_static_fixture` must never be deletion eligible;
- `promoted_regression_fixture_candidate` requires review and must not be
  deleted;
- `generated_local_runtime_artifact` requires explicit `policy_reference`;
- `dry_run_artifact_candidate` is not deleted by default;
- `temporary_validation_artifact` may only be a cleanup candidate after
  governed policy;
- unknown `artifact_category` is rejected.

## Strict Locked Marker Validation Themes

Future validation should reject:

- `deletion_allowed` true;
- `filesystem_mutation_allowed` true;
- `fixture_promotion_allowed` true unless later separately governed;
- `macro_report_unlock` true;
- `actual_handoff_executed` true;
- `cli_behavior_added` true.

## Fail-Closed Validation Themes

Future validation should reject:

- non-object cleanup decision;
- missing required field;
- unknown cleanup eligibility;
- unknown cleanup decision;
- unknown artifact category;
- committed fixture with deletion eligibility;
- generated runtime artifact without `policy_reference`;
- any cleanup execution marker;
- any filesystem mutation marker;
- any macro unlock / actual handoff / CLI marker.

## Wrapper Stance

Future validation helper stance:

- future helper, if implemented later, should remain standalone unless
  separately governed;
- do not add future helper to `run_all_kernel_local_checks.py` by default;
- `kernel-local-validation-checks-ok` must not silently broaden.

## Explicit Blocked Behaviors

This validation plan does not unlock:

- validation helper implementation;
- cleanup automation;
- artifact deletion;
- filesystem mutation;
- fixture promotion automation;
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

## Recommended Next Phase

Recommended next phase:

```text
Cleanup Automation Boundary Implementation Gate Pass
```
