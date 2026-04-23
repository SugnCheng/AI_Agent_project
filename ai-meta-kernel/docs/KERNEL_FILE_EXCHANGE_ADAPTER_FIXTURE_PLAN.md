# Kernel File Exchange Adapter Fixture Plan

## Purpose

This document defines the smallest governed fixture strategy for testing the future `ai-meta-kernel` file exchange adapter before runtime code is added.

It is a planning document only. It does not create fixtures, implement file reading, implement file writing, invoke the kernel runtime, modify kernel contracts, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Authority

This fixture plan is subordinate to:

- `META_LAYER_MASTER_SPEC.md`
- `meta-layer/TASK_OBJECT_SCHEMA.json`
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_PLAN.md`
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_CONTRACT.md`
- `../macro-financial-intelligence-agent/FILE_BASED_KERNEL_EXCHANGE_CONTRACT.md`

If fixture convenience conflicts with kernel contracts, kernel contracts win.

## Fixture Strategy Summary

The v0.1 fixture strategy should cover exactly three fixture classes:

| Fixture class | Purpose | Owner |
| --- | --- | --- |
| Kernel input envelope fixture | Test kernel-side envelope intake validation before runtime invocation exists. | Kernel-side fixture derived from macro envelope contract. |
| Expected response fixture | Test shape expectations for a kernel-produced canonical task object artifact. | Kernel side. |
| Expected failure fixture | Test shape expectations for blocking kernel-side failure artifacts. | Kernel side, aligned with macro exchange contract. |

The first fixture set should remain static, small, deterministic, and `daily_us_core`-scoped.

## Minimal Static Envelope Fixture Strategy

The first static envelope fixture should represent one valid `daily_us_core` envelope artifact.

Recommended future location:

```text
ai-meta-kernel/examples/file-exchange/envelopes/
```

Recommended file:

```text
daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_input_envelope.example.json
```

Minimum envelope fixture expectations:

- includes the current envelope fields from the adapter contract;
- uses `source_project == "macro-financial-intelligence-agent"`;
- uses `profile_id == "daily_us_core"`;
- uses `run_mode == "daily_brief_run"`;
- uses `report_target == "daily_brief"`;
- uses `regions == ["US"]`;
- contains a compact `operator_intent`;
- contains a small evidence bundle reference or reduced evidence payload;
- contains `kernel_task_object_expectation` as expectations only;
- does not contain a completed canonical task object;
- does not contain top-level `framed_objective`, `task_classification`, `risk_profile`, `triggered_habits`, `structural_decomposition`, `required_checks`, `status_flags`, `verification_plan`, `challenge_loop`, `downstream_recommendation`, or `handoff`.

The fixture should test the adapter's ability to preserve evidence/context and reject macro-side conclusion leakage.

## Expected Response Fixture Strategy

The first response fixture should represent a minimal schema-valid kernel response artifact for the same `daily_us_core` envelope.

Recommended future location:

```text
ai-meta-kernel/examples/file-exchange/responses/
```

Recommended file:

```text
daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_response.example.json
```

Minimum response fixture expectations:

- validates against `meta-layer/TASK_OBJECT_SCHEMA.json`;
- uses `schema_version == "0.2.0"`;
- includes all required top-level kernel task object fields;
- uses canonical field names exactly;
- demonstrates kernel-owned decomposition of facts, assumptions, inferences, unknowns, constraints, stakeholders, and tradeoffs;
- includes at least one primary triggered habit;
- includes `verification_plan`;
- includes `challenge_loop`;
- includes `downstream_recommendation`;
- includes `handoff`;
- does not claim live fetching, report composition, scheduler execution, or external service calls occurred.

The response fixture should be used only as a static expected-shape artifact. It should not imply that kernel runtime invocation has been implemented.

## Expected Failure Fixture Strategy

The first failure fixture should represent a blocking kernel-side adapter failure.

Recommended future location:

```text
ai-meta-kernel/examples/file-exchange/failures/
```

Recommended file:

```text
daily_us_core__daily_brief_run__daily_brief__20260423T000000Z__kernel_failure.example.json
```

Minimum failure fixture expectations:

- uses `artifact_type == "kernel_exchange_failure"`;
- uses `artifact_version == "0.1.0"`;
- uses `source_project == "ai-meta-kernel"`;
- uses `profile_id == "daily_us_core"`;
- uses `run_mode == "daily_brief_run"`;
- uses `report_target == "daily_brief"`;
- uses `regions == ["US"]`;
- references the matching envelope fixture path;
- uses one governed failure stage;
- includes non-empty `failure_reason`;
- uses `blocking == true`;
- includes `created_at`;
- does not contain a partial canonical task object;
- does not unlock downstream reporting.

The first failure fixture should probably use `failure_stage == "pre_invoke"` or `failure_stage == "response_schema_validation"` because those are easiest to reason about before runtime code exists.

## Kernel-Side vs Macro-Side Fixtures

| Fixture type | Kernel side | Macro side |
| --- | --- | --- |
| Envelope fixture | May keep a copied or reduced fixture for adapter intake tests. | Owns generated envelope shape and runtime envelope writer fixtures. |
| Response fixture | Owns expected canonical task object response examples. | May keep response fixtures for downstream read/classification regression. |
| Failure fixture | Owns kernel-side failure shape examples. | May keep failure fixtures for downstream read/classification regression. |
| Ingestion bundle fixture | Should not own macro ingestion bundle fixtures. | Owns ingestion bundle examples and fixture pipeline artifacts. |

Kernel-side fixtures should validate kernel adapter assumptions. Macro-side fixtures should validate macro pipeline and downstream exchange behavior.

## Fixture Drift Controls

The following fixture changes require a governed pass:

- changing envelope required fields;
- adding top-level canonical task object fields to envelope fixtures;
- changing response fixture schema version;
- changing response fixture canonical field names;
- changing response fixture handoff mode semantics;
- changing failure artifact shape;
- adding or removing failure stages;
- allowing failure fixtures with `blocking == false`;
- changing file naming semantics;
- broadening fixtures beyond `daily_us_core`;
- copying macro ingestion bundle internals into kernel fixtures without a reduced adapter-testing purpose;
- using fixtures to imply live runtime behavior exists.

## Explicitly Deferred Behaviors

The following remain explicitly deferred:

- creating the actual fixture files;
- implementing fixture validation scripts;
- implementing the kernel-side file reader;
- implementing response artifact writing;
- implementing failure artifact writing;
- invoking the kernel runtime;
- generating canonical task objects from fixtures at runtime;
- creating a CLI;
- adding CI;
- adding package migration;
- adding live fetching;
- adding scheduler runtime;
- adding report composition;
- adding external service calls;
- adding generic multi-profile fixture coverage.

## Recommended Next Phase

Implement a `Kernel-Side File Exchange Adapter Fixture Creation Pass`.

That pass should add only the smallest static envelope, response, and failure fixture files under a governed kernel-side examples path. It should not add runtime adapter code.
