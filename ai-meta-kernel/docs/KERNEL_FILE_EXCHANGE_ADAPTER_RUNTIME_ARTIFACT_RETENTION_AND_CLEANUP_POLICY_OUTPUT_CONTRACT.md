# Kernel File Exchange Adapter Runtime Artifact Retention And Cleanup Policy Output Contract

## Purpose

This note defines the future output contract for runtime artifact retention and
cleanup policy decisions after the R32 policy preparation baseline.

It is an output contract only. It does not implement cleanup automation,
artifact deletion, fixture promotion automation, CLI behavior, queue discovery,
polling, retry, macro report unlock, actual handoff, scheduler behavior,
production cross-project exchange, or runtime orchestration.

## Current Contract Decision

Current contract decision:

```text
runtime_artifact_retention_cleanup_policy_output_contract_baseline
```

## Future Policy Output Object Required Fields

A future runtime artifact retention and cleanup policy output object must
include:

- `policy_type`;
- `policy_state`;
- `policy_stage`;
- `artifact_category`;
- `retention_decision`;
- `promotion_decision`;
- `cleanup_decision`;
- `commit_allowed`;
- `cleanup_automation_allowed`;
- `fixture_promotion_allowed`;
- `macro_report_unlock`;
- `actual_handoff_executed`;
- `cli_behavior_added`.

## Artifact Category Semantics

Valid artifact categories are:

- `committed_static_fixture`: a reviewed fixture already intended to be
  committed as durable validation material.
- `generated_local_runtime_artifact`: a local artifact written by bounded
  runtime adapter behavior; not commit-allowed by default.
- `dry_run_artifact_candidate`: a non-written or candidate-only artifact shape
  used to exercise terminal path expectations; not commit-allowed.
- `temporary_validation_artifact`: local validation material created only to
  support a validation run; not durable fixture material by default.
- `promoted_regression_fixture_candidate`: generated material selected for
  possible fixture promotion, still requiring review before commit.

## Retention Decision Semantics

Valid retention decisions are:

- `retain_local`: keep as local material without committing.
- `ignore_for_commit`: leave out of committed fixture surfaces.
- `review_for_promotion`: route for human review before fixture promotion.
- `cleanup_deferred`: defer cleanup until a governed policy allows cleanup
  behavior.
- `blocked`: block retention or promotion because the artifact is invalid,
  unsafe, private, ambiguous, or otherwise unsuitable.

## Promotion Decision Semantics

Valid promotion decisions are:

- `not_promoted`: no fixture promotion is selected.
- `review_required`: human review is required before promotion.
- `promotion_candidate_only`: the artifact may be evaluated as a fixture
  candidate, but is not promoted yet.
- `rejected`: the artifact is not eligible for fixture promotion.

## Cleanup Decision Semantics

Valid cleanup decisions are:

- `cleanup_not_implemented`: cleanup behavior does not exist in the current
  runtime adapter.
- `cleanup_blocked`: cleanup must not run for this artifact state.
- `cleanup_deferred`: cleanup policy may be considered later through a
  governed pass.
- `explicit_manual_review_required`: manual review is required before any
  cleanup decision is applied.

## Strict Markers

The output contract must preserve these strict markers:

- generated runtime artifacts are not commit-allowed by default;
- promotion requires review;
- cleanup automation remains false;
- fixture promotion automation remains false;
- `macro_report_unlock` remains false;
- `actual_handoff_executed` remains false;
- `cli_behavior_added` remains false.

## Validation Themes

Future validation should cover:

- policy object shape;
- valid artifact categories only;
- generated runtime artifacts default to `commit_allowed` false;
- dry-run candidates are not `commit_allowed`;
- promoted fixture candidates require review;
- cleanup automation false;
- macro unlock false;
- actual handoff false;
- CLI false.

## Recommended Next Phase

Recommended next phase:

```text
Runtime Artifact Retention And Cleanup Policy Validation Plan Pass
```
