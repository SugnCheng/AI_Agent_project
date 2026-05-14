# Kernel File Exchange Adapter Runtime Envelope Reader Implementation Output Contract

## Purpose

This document snapshots the output contract for the minimal runtime envelope reader implementation slice.

This contract records the Phase R2 minimal implementation boundary. It does not authorize wrapper inclusion, intake mapping, kernel invocation, response/failure writing, CLI behavior, or kernel contract changes.

## Contract Decision

Current Phase R2 implementation output contract decision:

```text
minimal_reader_returns_one_validated_envelope_and_stops_before_intake
```

The implemented minimal reader may produce only one reader-validated `kernel_input_envelope` output from one explicit local input path.

## Allowed Future Output

A successful minimal reader implementation may output:

```text
one_validated_kernel_input_envelope_object
```

The current minimal implementation returns the validated envelope object directly. Future source-path context would require a governed pass and must remain adapter-local metadata, not a kernel conclusion.

The output must preserve the validated envelope content and must not add canonical task object fields.

## Success Signal Expectations

The current standalone contract helper signal remains:

```text
kernel-runtime-envelope-reader-contract-checks-ok
```

The main wrapper signal remains:

```text
kernel-local-validation-checks-ok
```

At Phase R2, `kernel-local-validation-checks-ok` does not include runtime reader helper coverage.

## Failure Behavior

Reader implementation failures must be fail-closed.

The reader must reject:

- missing path;
- directory path;
- invalid JSON;
- non-object JSON;
- missing required envelope fields;
- wrong artifact type;
- failure artifact input;
- response artifact input;
- canonical task object field leakage.

On failure, the reader must not repair input, synthesize fields, continue into intake mapping, invoke runtime, write response/failure artifacts, or unlock reporting.

## Stop Boundary

The implementation contract stops at:

```text
validated kernel_input_envelope object
```

It does not output:

- `kernel_intake_context`;
- canonical task object;
- response artifact;
- failure artifact;
- runtime result;
- report eligibility.

## Governed Change Triggers

The following require a governed pass before implementation:

- changing output from envelope object to intake context;
- adding wrapper inclusion;
- changing success signal semantics;
- allowing multiple input envelopes;
- allowing directory discovery;
- allowing response/failure artifacts as input;
- writing failure artifacts from reader failures;
- adding queue discovery, polling, retry, cleanup, CLI, runtime invocation, report composition, CI, package migration, or external service calls.

## Explicit Non-Authorization

This contract does not authorize intake mapping, runtime invocation, response/failure writing, wrapper inclusion, CLI behavior, or actual runtime handoff.
