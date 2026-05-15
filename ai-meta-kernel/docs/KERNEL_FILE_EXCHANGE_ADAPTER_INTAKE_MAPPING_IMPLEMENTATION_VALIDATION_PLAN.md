# Kernel File Exchange Adapter Intake Mapping Implementation Validation Plan

## Purpose

This note defines the validation coverage for the minimal envelope-to-intake mapping implementation slice.

This validation plan is reflected by a standalone helper. It does not change wrapper behavior, execute P0/P1, invoke P0-P10 runtime, write response artifacts, write failure artifacts, add CLI behavior, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Validation Plan Decision

Current Phase R5 validation decision:

```text
minimal_intake_mapping_validated_by_standalone_helper_and_stops_before_runtime
```

Validation proves that the mapper converts one validated envelope into context only, without generating kernel conclusions or crossing into runtime execution.

## Required Future Checks

The current standalone helper validates:

- one validated envelope input is accepted;
- allowed envelope fields flow only into approved context roles;
- canonical task object fields are excluded from mapping output;
- no kernel conclusions are generated during mapping;
- no response artifact output is produced;
- no failure artifact output is produced;
- no P0/P1 execution occurs;
- no P0-P10 runtime invocation occurs;
- invalid mapping input fails closed;
- output stops before runtime.

## Success Path Validation

The success path uses one reader-validated `kernel_input_envelope` and confirms that the mapper returns one `kernel_intake_context`.

The expected output should preserve evidence, provenance, operator request text, expectation metadata, and deferred-behavior context without adding canonical task object fields or runtime conclusions.

Success must not imply response eligibility, report eligibility, P0/P1 execution, P0-P10 invocation, response writing, failure writing, CLI behavior, or wrapper inclusion.

## Failure Path Validation

Failure checks should confirm fail-closed behavior for:

- non-object input;
- input that has not passed envelope guardrails;
- missing required envelope fields;
- response artifact input;
- failure artifact input;
- top-level canonical task object field leakage;
- attempted direct population of kernel-owned conclusion fields.

Failure checks must also confirm the mapper does not repair input, synthesize missing fields, call `invoke_kernel_runtime`, write response artifacts, write failure artifacts, mutate fixtures, or unlock reporting.

## Stop-Before-Runtime Guarantee

Validation makes the stop boundary explicit:

```text
validated kernel_input_envelope
-> kernel_intake_context
-> stop
```

The validation surface must not cross into:

- P0/P1 execution;
- P0-P10 runtime invocation;
- canonical task object construction;
- response validation;
- response writing;
- failure writing;
- macro-side reporting.

## Relationship To Existing Helpers

The current intake mapping helper is:

```text
validation/kernel_intake_mapping_contract_checks.py
```

Current success signal:

```text
kernel-intake-mapping-contract-checks-ok
```

The helper remains standalone and is not included in `validation/run_all_kernel_local_checks.py`.

The reader helper remains separate:

```text
validation/kernel_runtime_envelope_reader_contract_checks.py
```

## Blocked In This Plan

This validation surface does not add:

- wrapper inclusion;
- P0/P1 execution;
- P0-P10 runtime invocation;
- response/failure writers;
- CLI behavior;
- queue discovery, polling, retry, cleanup, scheduler, report composition, CI, package migration, or external service calls.
