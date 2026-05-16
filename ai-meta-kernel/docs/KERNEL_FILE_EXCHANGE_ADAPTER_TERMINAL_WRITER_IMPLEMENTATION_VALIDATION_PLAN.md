# Kernel File Exchange Adapter Terminal Writer Implementation Validation Plan

## Purpose

This note defines terminal writer validation coverage as implementation slices open.

It now records the Phase R14 standalone response writer helper. It does not modify wrapper behavior, write failure artifacts, add CLI behavior, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Validation Plan Decision

Current Phase R12 validation planning decision:

```text
plan_terminal_writer_validation_before_implementation
```

Future validation must prove that terminal writers preserve one-invocation / one-terminal-artifact behavior and stop before orchestration.

Current Phase R14 response writer helper:

```text
validation/kernel_response_writer_contract_checks.py
```

Current success signal:

```text
kernel-response-writer-contract-checks-ok
```

## Future Success Path Checks

The current response writer validation covers:

- one validated pre-writer response input;
- response writer writes exactly one response artifact;
- response artifact is a JSON object;
- response artifact declares `artifact_type == "kernel_response"`;
- response artifact destination is explicit and local;
- failure writer remains blocked and is not called;
- writer output does not unlock macro-side reporting;
- writer output does not emit CLI success.

Future failure writer validation must still cover one classified blocking failure input and exactly one blocking failure artifact once that boundary is implemented.

## Future Failure Path Checks

The current response writer validation rejects:

- non-object response write input;
- malformed validated response input;
- destination directory as file path;
- existing destination path without a governed overwrite policy;
- ambiguous or unsafe destination paths;
- writer-side repair attempts;
- fixture mutation attempts.

Failure must remain local and explicit. It must not silently write a partial artifact or unlock reporting.

Future failure writer validation must still reject non-object failure input, malformed blocking failure input, and failure input with `blocking != true`.

## Mutual Exclusivity Checks

Future checks must prove:

```text
one invocation -> response artifact XOR blocking failure artifact
```

Validation should include explicit negative cases for:

- both writers called for one invocation;
- both artifacts present after one invocation;
- neither artifact produced after a known terminal writer decision, unless a governed fatal-error policy exists.

R14 only validates the response-writer side of that rule. Full response/failure mutual exclusivity remains incomplete until the failure writer exists.

## Stop-Before-Orchestration Guarantee

Validation must prove writer implementation does not add:

- CLI behavior;
- local invocation orchestration;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- cleanup automation;
- macro-side report unlock;
- scheduler behavior;
- report composition.

## Relationship To Existing Helpers

Existing helpers remain unchanged:

```text
validation/kernel_runtime_envelope_reader_contract_checks.py
validation/kernel_intake_mapping_contract_checks.py
validation/kernel_runtime_invocation_contract_checks.py
validation/kernel_response_validation_contract_checks.py
validation/kernel_response_writer_contract_checks.py
validation/run_all_kernel_local_checks.py
```

Phase R14 adds the standalone response writer helper but does not add it to the wrapper.

## Blocked In This Plan

This validation plan does not add:

- failure writer implementation;
- response writer broadening beyond the R14 minimal explicit-destination artifact writer;
- failure artifact writing;
- CLI behavior;
- macro report unlock;
- queue discovery, polling, retry, cleanup, scheduler behavior, report composition, CI, package migration, or external service calls.
