# Kernel File Exchange Adapter Cleanup Automation Boundary Output Contract

## Purpose

This note defines the future output contract for cleanup automation boundary
decisions after the R39 cleanup automation boundary preparation baseline.

It is an output contract only. It does not implement cleanup automation,
artifact deletion, filesystem mutation, fixture promotion automation, CLI
behavior, queue discovery, polling, retry, scheduler behavior, macro report
unlock, actual handoff, wrapper inclusion, production cross-project exchange,
or full runtime orchestration.

## Current Contract Decision

Current contract decision:

```text
cleanup_automation_boundary_output_contract_baseline
```

## Future Cleanup Decision Object Required Fields

A future cleanup decision object must include:

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

## Cleanup Eligibility Semantics

Valid cleanup eligibility values are:

- `not_eligible`: the artifact is not eligible for cleanup consideration.
- `eligible_for_review_only`: the artifact may be reviewed, but no cleanup
  action is authorized.
- `eligible_for_future_cleanup_policy`: the artifact may be considered by a
  later governed cleanup policy.
- `blocked`: cleanup consideration is blocked because the artifact state is
  invalid, unsafe, ambiguous, committed, or review-gated.
- `deferred`: cleanup consideration is deferred until a later governed pass.

## Cleanup Decision Semantics

Valid cleanup decision values are:

- `cleanup_not_implemented`: cleanup behavior does not exist in the current
  runtime adapter.
- `cleanup_blocked`: cleanup must not run for this artifact state.
- `cleanup_deferred`: cleanup may be considered later through a governed pass.
- `review_required`: manual review is required before any cleanup decision can
  advance.
- `no_action`: no cleanup action is selected.

## Artifact Category Handling

Cleanup boundary handling must preserve these category rules:

- `committed_static_fixture` must never be deletion eligible;
- `promoted_regression_fixture_candidate` requires review and must not be
  deleted;
- `generated_local_runtime_artifact` requires an explicit policy object before
  any cleanup decision;
- `dry_run_artifact_candidate` is not deleted by default;
- `temporary_validation_artifact` may only become a cleanup candidate after
  governed policy.

## Strict Locked Markers

The output contract must preserve these strict markers:

- `deletion_allowed` must remain false;
- `filesystem_mutation_allowed` must remain false;
- `fixture_promotion_allowed` must remain false unless later separately
  governed;
- `macro_report_unlock` must remain false;
- `actual_handoff_executed` must remain false;
- `cli_behavior_added` must remain false.

## Output Contract Exclusions

This output contract excludes:

- artifact deletion;
- filesystem mutation;
- cleanup automation execution;
- implicit directory sweeping;
- fixture promotion automation;
- CLI behavior;
- queue discovery;
- polling / retry / cleanup side effects;
- macro report unlock;
- actual handoff;
- wrapper inclusion.

## Validation Themes

Future validation should cover:

- decision object shape;
- valid cleanup eligibility values only;
- valid cleanup decision values only;
- committed fixtures cannot be deletion eligible;
- generated runtime artifacts require policy reference;
- `deletion_allowed` true rejected;
- `filesystem_mutation_allowed` true rejected;
- `macro_report_unlock` true rejected;
- `actual_handoff_executed` true rejected;
- `cli_behavior_added` true rejected.

## Recommended Next Phase

Recommended next phase:

```text
Cleanup Automation Boundary Validation Plan Pass
```
