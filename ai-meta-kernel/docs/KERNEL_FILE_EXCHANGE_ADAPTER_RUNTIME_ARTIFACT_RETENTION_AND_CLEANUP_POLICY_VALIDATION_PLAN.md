# Kernel File Exchange Adapter Runtime Artifact Retention And Cleanup Policy Validation Plan

## Purpose

This note defines the future validation plan for runtime artifact retention and
cleanup policy outputs after the R32 preparation baseline and R33 output
contract baseline.

It is a validation plan only. It does not implement validation helper code,
cleanup automation, artifact deletion, fixture promotion automation, CLI
behavior, queue discovery, polling, retry, macro report unlock, actual
handoff, wrapper inclusion, scheduler behavior, production cross-project
exchange, or runtime orchestration.

## Current Validation Decision

Current validation decision:

```text
runtime_artifact_retention_cleanup_policy_validation_plan_baseline
```

## Validation Scope

Future validation should cover:

- future policy output object shape;
- valid artifact category semantics;
- retention decision semantics;
- promotion decision semantics;
- cleanup decision semantics;
- commit eligibility markers;
- cleanup-blocked markers;
- downstream locked markers.

## Artifact-Category Validation Themes

Future validation should prove:

- `committed_static_fixture` is allowed only when already reviewed;
- `generated_local_runtime_artifact` defaults to `commit_allowed` false;
- `dry_run_artifact_candidate` has `commit_allowed` false;
- `temporary_validation_artifact` has `commit_allowed` false by default;
- `promoted_regression_fixture_candidate` requires review.

## Retention Validation Themes

Future validation should prove:

- `retain_local` does not imply `commit_allowed`;
- `ignore_for_commit` keeps `commit_allowed` false;
- `review_for_promotion` requires a promotion review marker;
- `cleanup_deferred` does not trigger cleanup automation;
- `blocked` prevents promotion and commit.

## Promotion Validation Themes

Future validation should prove:

- `not_promoted` keeps `fixture_promotion_allowed` false;
- `review_required` must not equal automatic promotion;
- `promotion_candidate_only` still requires review;
- `rejected` blocks promotion.

## Cleanup Validation Themes

Future validation should prove:

- `cleanup_not_implemented` means no cleanup action;
- `cleanup_blocked` prevents deletion;
- `cleanup_deferred` does not delete artifacts;
- `explicit_manual_review_required` requires review before deletion.

## Fail-Closed Validation Themes

Future validation should reject:

- unknown `artifact_category`;
- unknown `retention_decision`;
- unknown `promotion_decision`;
- unknown `cleanup_decision`;
- generated runtime artifact with `commit_allowed` true unless reviewed
  promotion candidate;
- dry-run candidate with `commit_allowed` true;
- `cleanup_automation_allowed` true;
- `fixture_promotion_allowed` true unless governed reviewed promotion state
  exists;
- `macro_report_unlock` true;
- `actual_handoff_executed` true;
- `cli_behavior_added` true.

## Wrapper Stance

Future validation helper stance:

- future helper should remain standalone unless separately governed;
- do not add future helper to `run_all_kernel_local_checks.py` by default;
- `kernel-local-validation-checks-ok` must not silently broaden.

## Explicit Blocked Behaviors

This validation plan does not unlock:

- validation helper implementation;
- cleanup automation;
- artifact deletion;
- fixture promotion automation;
- CLI;
- queue discovery;
- polling / retry / cleanup;
- macro report unlock;
- actual handoff;
- wrapper inclusion.

## Recommended Next Phase

Recommended next phase:

```text
Runtime Artifact Retention And Cleanup Policy Implementation Gate Pass
```
