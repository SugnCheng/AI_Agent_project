# Kernel File Exchange Fixture Validation Plan

## Purpose

This document defines the smallest governed validation strategy for the kernel-side file exchange fixtures before adapter runtime code or validation scripts are added.

It is a planning document only. It does not add validation scripts, implement file readers, implement file writers, invoke the kernel runtime, modify kernel contracts, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Authority

This validation plan is subordinate to:

- `META_LAYER_MASTER_SPEC.md`
- `meta-layer/TASK_OBJECT_SCHEMA.json`
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_CONTRACT.md`
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_FIXTURE_PLAN.md`
- `examples/file-exchange/README.md`

If validation convenience conflicts with canonical kernel contracts, canonical kernel contracts win.

## Current Fixture Scope

The current static fixture set is:

```text
examples/file-exchange/
+-- README.md
+-- envelopes/
|   +-- daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.example.json
+-- responses/
|   +-- daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_response.example.json
+-- failures/
    +-- daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_failure.example.json
```

Validation should remain static, local, and `daily_us_core`-scoped for v0.1.

## Envelope Fixture Validation

The envelope fixture must validate that it is safe kernel intake context, not a canonical kernel task object.

Minimum checks:

1. File parses as JSON.
2. Parsed content is object-like.
3. Required envelope fields exist:
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
4. `envelope_type == "kernel_input_envelope"`.
5. `source_project == "macro-financial-intelligence-agent"`.
6. `profile_id == "daily_us_core"`.
7. `run_mode == "daily_brief_run"`.
8. `report_target == "daily_brief"`.
9. `regions == ["US"]`.
10. `operator_intent` is non-empty.
11. Envelope does not contain top-level canonical task object fields:
    - `schema_version`
    - `task_id`
    - `raw_request`
    - `kernel_stage`
    - `framed_objective`
    - `task_classification`
    - `risk_profile`
    - `triggered_habits`
    - `structural_decomposition`
    - `required_checks`
    - `status_flags`
    - `verification_plan`
    - `challenge_loop`
    - `downstream_recommendation`
    - `handoff`
12. `kernel_task_object_expectation` remains expectation/context only.

The envelope validation helper should not infer kernel conclusions from the fixture.

## Response Fixture Validation

The response fixture must validate that it is a schema-valid example of a kernel-produced canonical response artifact.

Minimum checks:

1. File parses as JSON.
2. Parsed content is object-like.
3. Response validates against `meta-layer/TASK_OBJECT_SCHEMA.json`.
4. `schema_version == "0.2.0"`.
5. Required top-level fields are present:
   - `raw_request`
   - `framed_objective`
   - `task_classification`
   - `risk_profile`
   - `triggered_habits`
   - `structural_decomposition`
   - `required_checks`
   - `status_flags`
   - `verification_plan`
   - `challenge_loop`
   - `downstream_recommendation`
   - `handoff`
6. At least one `triggered_habits` item has `role == "primary"`.
7. `downstream_recommendation.mode` is one of:
   - `standard_handoff`
   - `restricted_handoff`
   - `do_not_handoff`
8. Response does not claim live fetching, scheduler execution, report composition, or external service calls occurred.

The response fixture validation helper should only validate static expected shape. It should not generate the response.

## Failure Fixture Validation

The failure fixture must validate that it is a governed blocking kernel-side failure artifact.

Minimum checks:

1. File parses as JSON.
2. Parsed content is object-like.
3. Required failure fields exist:
   - `artifact_type`
   - `artifact_version`
   - `source_project`
   - `profile_id`
   - `run_mode`
   - `report_target`
   - `regions`
   - `envelope_artifact_path`
   - `failure_stage`
   - `failure_reason`
   - `blocking`
   - `created_at`
4. `artifact_type == "kernel_exchange_failure"`.
5. `artifact_version == "0.1.0"`.
6. `source_project == "ai-meta-kernel"`.
7. `blocking == true`.
8. `failure_reason` is non-empty.
9. `failure_stage` is one of:
   - `pre_invoke`
   - `invoke`
   - `response_parse`
   - `response_schema_validation`
   - `response_state_validation`
10. Failure fixture does not contain a partial canonical task object.

The failure validation helper should preserve the rule that all v0.1 failure artifacts are blocking.

## Minimum Future Local Validation Helper Scope

The first future helper should be a local static fixture check only.

Suggested future location:

```text
ai-meta-kernel/validation/kernel_file_exchange_fixture_checks.py
```

Suggested responsibilities:

1. Load the three current fixture files.
2. Validate JSON parseability.
3. Validate envelope fixture guardrails.
4. Validate response fixture against `meta-layer/TASK_OBJECT_SCHEMA.json`.
5. Validate failure fixture blocking shape.
6. Print one compact success signal, for example:

```text
kernel-file-exchange-fixture-checks-ok
```

The helper should use only local files and approved project dependencies already present in the environment. If JSON Schema validation requires a dependency, the future implementation pass should explicitly document that dependency assumption before adding the helper.

## Fixture Drift Controls

The following changes require a governed pass before updating fixtures or validation logic:

- changing fixture file names;
- changing fixture directory locations;
- changing required envelope fields;
- allowing envelope fixtures to include canonical task object fields;
- changing `schema_version` in response fixtures;
- changing canonical response field names;
- changing `downstream_recommendation.mode` semantics;
- changing failure artifact required fields;
- adding or removing failure stages;
- allowing `blocking == false` for failure fixtures;
- broadening fixture validation beyond `daily_us_core`;
- making fixture validation invoke runtime code;
- making fixture validation generate response or failure artifacts;
- adding network, scheduler, reporting, CI, package migration, or external service behavior.

## Explicitly Deferred Behaviors

The following remain explicitly deferred:

- adding the validation helper script;
- adding runtime adapter code;
- implementing file readers;
- implementing response writers;
- implementing failure writers;
- invoking the kernel runtime;
- generating canonical task objects from envelopes;
- validating runtime artifacts;
- artifact polling;
- retry/backoff logic;
- artifact cleanup automation;
- live fetching;
- scheduler runtime;
- report composition;
- CI integration;
- package migration;
- external service calls;
- generic multi-profile validation.

## Recommended Next Phase

Implement a `Kernel-Side File Exchange Fixture Validation Helper Pass`.

That pass should add only the smallest local static fixture validation helper. It should not add adapter runtime code.
