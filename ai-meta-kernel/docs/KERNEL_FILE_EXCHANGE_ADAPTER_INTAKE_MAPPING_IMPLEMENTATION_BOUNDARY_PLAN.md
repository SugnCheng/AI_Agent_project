# Kernel File Exchange Adapter Intake Mapping Implementation Boundary Plan

## Purpose

This note defines the smallest acceptable future envelope-to-intake mapping implementation boundary for `ai-meta-kernel`.

It is a preparation note only. It does not add intake mapping code, modify kernel contracts, execute P0/P1, invoke P0-P10 runtime, generate canonical task objects, write response artifacts, write failure artifacts, add CLI behavior, broaden reader behavior, change wrapper behavior, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Planning Decision

Current Phase R4 preparation decision:

```text
prepare_minimal_envelope_to_intake_mapping_implementation_boundary_without_code
```

The future implementation slice may convert one validated `kernel_input_envelope` into one kernel-owned `kernel_intake_context`. It must stop before P0/P1 execution and before P0-P10 runtime invocation.

## Intended Input Boundary

The future mapping implementation may accept exactly one validated `kernel_input_envelope` object.

The input must already satisfy the runtime reader and envelope guardrails:

- JSON object;
- `envelope_type == "kernel_input_envelope"`;
- required envelope fields present;
- not a response artifact;
- not a failure artifact;
- no top-level canonical task object fields;
- source/profile/run metadata preserved.

The mapper must not accept:

- file paths directly;
- runtime directories;
- multiple envelopes per invocation;
- response artifacts;
- failure artifacts;
- macro-generated canonical task objects;
- unvalidated JSON objects.

## Intended Output Boundary

The future mapping implementation may output exactly one kernel-owned context object:

```text
kernel_intake_context
```

This output is input context for future kernel-owned P0/P1 preparation. It is not a canonical task object, response artifact, failure artifact, P0/P1 result, P0-P10 runtime result, or report eligibility signal.

## Allowed Source Fields From Envelope

The future mapper may carry these envelope fields only as evidence, metadata, request text, expectation context, or deferred-behavior context:

| Envelope field | Allowed role |
| --- | --- |
| `envelope_type` | Guardrail metadata only. |
| `envelope_version` | Compatibility metadata. |
| `source_project` | Provenance metadata. |
| `profile_id` | Run/profile metadata. |
| `run_mode` | Run context metadata. |
| `report_target` | Target context metadata, not a reporting unlock. |
| `regions` | Scope context. |
| `operator_intent` | Operator request source text. |
| `evidence_bundle` | Evidence/context source. |
| `evidence_context` | Source, acquisition, and uncertainty context. |
| `kernel_task_object_expectation` | Non-conclusive expectation metadata. |
| `deferred_runtime_behavior` | Explicit blocked/deferred behavior context. |

The original validated envelope should remain available as source context or an equivalent immutable reference.

## Fields That Must Remain Excluded

The future mapping output must not include or populate canonical task object fields:

- `schema_version`;
- `task_id`;
- `raw_request`;
- `kernel_stage`;
- `framed_objective`;
- `task_classification`;
- `risk_profile`;
- `triggered_habits`;
- `structural_decomposition`;
- `required_checks`;
- `status_flags`;
- `verification_plan`;
- `challenge_loop`;
- `downstream_recommendation`;
- `handoff`.

It must also exclude final report eligibility, response state classification, restricted/blocked handoff decisions, generated response artifact paths, and generated failure artifact paths.

## Evidence And Context Versus Kernel Conclusions

The mapper may preserve macro-provided evidence and operator context. It must not convert that material into kernel-owned conclusions.

Kernel-owned conclusions remain downstream of P0/P1 and P0-P10 runtime behavior, including framing, classification, risk calibration, verification planning, challenge loop, status flags, downstream recommendation, and handoff.

## Stop-Before-P0/P1 Boundary

The future implementation boundary must stop here:

```text
validated kernel_input_envelope
-> kernel_intake_context
-> stop
```

It must not continue into:

- P0/P1 execution;
- P0-P10 runtime invocation;
- canonical task object construction;
- response validation;
- response writing;
- failure writing;
- macro-side reporting.

## Relationship To Existing Intake Mapping Governance

This note prepares the implementation boundary for the existing governance documents:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_PLAN.md
docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_OUTPUT_CONTRACT.md
```

Those documents define the future mapping concept and output contract. This Phase R4 note fixes the smallest future implementation slice but does not authorize implementation in this phase.

## Relationship To Minimal Runtime Reader

The Phase R2 runtime reader produces the validated envelope that a future mapper may accept. The reader still stops before mapping, and the standalone reader helper remains outside the main wrapper.

The future mapper must not broaden reader behavior, read files directly, discover queues, poll runtime directories, retry, clean up artifacts, or write terminal artifacts.

## Files Requiring Refresh If Implementation Opens Later

A future intake mapping implementation slice must refresh at minimum:

- `ai-meta-kernel/file_exchange_adapter_scaffold.py`
- `ai-meta-kernel/docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_OUTPUT_CONTRACT.md`
- `ai-meta-kernel/docs/KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_VALIDATION_PLAN.md`
- `ai-meta-kernel/docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_GATE.md`
- `ai-meta-kernel/docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_SEQUENCE.md`
- `ai-meta-kernel/docs/KERNEL_VALIDATION_BASELINE.md`
- `ai-meta-kernel/docs/KERNEL_VALIDATION_DOCUMENTATION_INDEX.md`
- `CROSS_PROJECT_INTEGRATION_STATUS.md`

If a new helper is added, its output contract, standalone/wrapper relationship, and wrapper exclusion must also be documented before completion.

## Behaviors That Remain Blocked

Phase R4 keeps the following blocked:

- intake mapping implementation code;
- P0/P1 execution;
- P0-P10 runtime invocation;
- canonical task object generation;
- response validation as runtime behavior;
- response artifact writing;
- failure artifact writing;
- CLI behavior;
- runtime directory scanning;
- queue discovery;
- polling, watcher, retry, backoff, or cleanup behavior;
- wrapper inclusion for the standalone reader helper;
- live fetching;
- scheduler runtime;
- report composition;
- CI behavior;
- package migration;
- external service calls;
- actual runtime handoff.
