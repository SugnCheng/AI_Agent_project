# Kernel File Exchange Adapter Terminal Writer Implementation Boundary Plan

## Purpose

This note prepares and tracks the terminal writer implementation boundary for `ai-meta-kernel`.

It records that the response writer portion has a minimal R14 implementation. It does not implement failure writer code, modify kernel contracts, modify `meta-layer/TASK_OBJECT_SCHEMA.json`, add CLI behavior, broaden the reader, broaden intake mapping, broaden runtime invocation, broaden response validation, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, call external services, or implement actual runtime handoff.

## Planning Decision

Current Phase R12 preparation decision:

```text
prepare_terminal_writers_together_before_implementation
```

The response writer and blocking failure writer must be prepared together because they share terminal-artifact mutual exclusivity:

```text
one invocation -> exactly one terminal artifact -> response artifact OR blocking failure artifact -> never both
```

Current Phase R14 implementation status:

```text
response_writer_minimal_implementation_slice_complete
```

## Future Response Writer Boundary

The current minimal response writer input boundary accepts exactly one locally validated pre-writer response object from the governed response validation boundary.

The current minimal response writer output boundary writes exactly one local kernel response artifact only after:

- the response input matches the current R10 validated pre-writer response contract;
- destination rules are checked;
- the destination is explicit and local;
- the destination does not already exist;
- the destination parent exists;
- no failure writer has already produced a terminal artifact for the same invocation.

The writer must not repair invalid responses, synthesize missing kernel conclusions, infer missing handoff fields, or treat local validation status as macro report unlock.

## Future Failure Writer Boundary

The future failure writer input boundary may accept exactly one locally classified blocking failure object.

The future failure writer output boundary may write exactly one blocking kernel exchange failure artifact only after:

- the failure input is accepted as blocking and writer-eligible;
- required failure fields are present;
- the failure stage is governed;
- the failure object contains no partial canonical task object content;
- no response writer has already produced a terminal artifact for the same invocation.

The failure writer must not emit non-blocking failure artifacts, unlock downstream reporting, or use partial response content as a fallback task object.

## Destination And Naming Governance

Future writer implementation must preserve governed terminal artifact naming:

```text
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__kernel_response.json
{profile_id}__{run_mode}__{report_target}__{utc_timestamp}__kernel_failure.json
```

Destination behavior must remain local, explicit, and governed. R12 does not authorize queue discovery, directory polling, implicit destination inference, cleanup, fixture promotion, or CLI orchestration.

## Pre-Write Validation Expectations

Before any future write:

- exactly one invocation context must be in scope;
- response and failure writer eligibility must be mutually exclusive;
- response input must be validated before response writing;
- failure input must be classified and validated before failure writing;
- terminal artifact paths must be checked before writing;
- existing static fixtures must not be mutated;
- invalid write input must fail closed without writing either artifact unless a governed fatal-error policy says otherwise.

## Stop Boundaries

The terminal writer implementation boundary must stop before:

- CLI or local invocation orchestration;
- scheduler behavior;
- macro-side report unlock;
- report composition;
- artifact retention, cleanup, or fixture promotion automation;
- actual runtime handoff.

## Relationship To Response Validation Output Contract

The upstream response validation output contract is:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_OUTPUT_CONTRACT.md
```

R10 validated response output remains local, pre-writer, and non-terminal until it is passed to the R14 minimal response writer. R14 permits only the narrow explicit-destination response artifact write and does not authorize failure writer implementation, macro report unlock, CLI behavior, or actual handoff.

## Relationship To Existing Writer Boundary Docs

The existing writer planning and output contract remain the writer-governance background:

```text
docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_PLAN.md
docs/KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md
```

R12 narrows those concepts into an implementation-preparation package. It does not replace the existing writer-boundary governance documents and does not implement writers.

## Files Requiring Refresh If Implementation Opens Later

Any future writer broadening or failure writer implementation pass must refresh at minimum:

- `ai-meta-kernel/file_exchange_adapter_scaffold.py`;
- the focused response writer validation helper or a future failure writer helper;
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_TERMINAL_WRITER_IMPLEMENTATION_OUTPUT_CONTRACT.md`;
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_TERMINAL_WRITER_IMPLEMENTATION_VALIDATION_PLAN.md`;
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_GATE.md`;
- `docs/KERNEL_FILE_EXCHANGE_ADAPTER_IMPLEMENTATION_SEQUENCE.md`;
- `docs/KERNEL_VALIDATION_BASELINE.md`;
- `docs/KERNEL_VALIDATION_DOCUMENTATION_INDEX.md`;
- `CROSS_PROJECT_INTEGRATION_STATUS.md`.

If wrapper inclusion is proposed for any future writer helper, the wrapper output contract, wrapper failure-path coverage, validation baseline, and documentation index must be updated before completion.

## Behaviors That Remain Blocked

Phase R14 keeps blocked:

- response writer broadening beyond the minimal explicit-destination local artifact writer;
- failure writer implementation;
- response artifact writing outside the R14 minimal writer boundary;
- failure artifact writing;
- terminal artifact path generation as runtime behavior;
- CLI behavior;
- queue discovery, polling, watcher behavior, retry, backoff, or cleanup;
- fixture mutation or promotion;
- macro-side report unlock;
- runtime reader broadening;
- intake mapping broadening;
- runtime invocation broadening;
- response validation broadening;
- wrapper inclusion for standalone helpers;
- live fetching;
- scheduler runtime;
- report composition;
- CI behavior;
- package migration;
- external service calls;
- actual runtime handoff.
