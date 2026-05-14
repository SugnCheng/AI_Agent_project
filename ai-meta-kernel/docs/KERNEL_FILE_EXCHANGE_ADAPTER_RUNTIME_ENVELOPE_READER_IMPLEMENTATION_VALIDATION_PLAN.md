# Kernel File Exchange Adapter Runtime Envelope Reader Implementation Validation Plan

## Purpose

This note defines the validation coverage for the minimal runtime envelope reader implementation slice.

This plan is now reflected by the standalone reader helper. It does not modify wrapper behavior, add wrapper inclusion, implement intake mapping, invoke kernel runtime, write artifacts, add CLI behavior, or change kernel contracts.

## Validation Plan Decision

Current Phase R2 validation decision:

```text
minimal_reader_implementation_validated_by_standalone_helper_and_fail_closed
```

The future validation surface should stay local, deterministic, and standard-library friendly unless a later governed pass explicitly changes that boundary.

## Required Future Checks

Implementation validation covers:

- one explicit local input path;
- valid envelope parsing;
- missing path rejection;
- directory rejection;
- invalid JSON rejection;
- non-object JSON rejection;
- missing required field rejection;
- wrong artifact type rejection;
- failure artifact rejection;
- response artifact rejection;
- canonical task object field leakage rejection;
- stop-before-intake guarantee.

## Success Path Validation

The success path should confirm that one governed envelope fixture can be read, parsed, validated, and returned as the reader output without mutation or canonical task object enrichment.

The success path must not imply intake mapping, runtime invocation, response writing, failure writing, reporting unlock, or wrapper inclusion.

## Failure Path Validation

Failure checks should confirm that invalid inputs fail closed and do not continue into later adapter stages.

Failure checks must confirm that reader failures do not:

- synthesize missing fields;
- repair malformed input;
- call `prepare_kernel_intake`;
- call `invoke_kernel_runtime`;
- write response artifacts;
- write failure artifacts;
- mutate fixtures or runtime artifacts.

## Relationship To Existing Helper

The current standalone helper already covers the governed contract surface:

```text
validation/kernel_runtime_envelope_reader_contract_checks.py
```

Current signal:

```text
kernel-runtime-envelope-reader-contract-checks-ok
```

The current helper remains outside the main wrapper. Future extension or wrapper inclusion requires a governed pass that updates wrapper contracts, failure-path coverage, baseline, and index.

## Blocked In This Plan

This validation surface does not add:

- committed failing fixtures;
- wrapper inclusion;
- intake mapping;
- kernel invocation;
- response/failure writers;
- CLI behavior;
- queue discovery, polling, retry, cleanup, scheduler, report composition, CI, package migration, or external service calls.
