# Kernel File Exchange Adapter Implementation Sequence

## Purpose

This note defines the intended future implementation order for the kernel-side file exchange adapter runtime path in `ai-meta-kernel`.

It is a developer-facing sequencing note only. It does not modify kernel contracts, invoke real P0-P10 runtime, add CLI behavior, add live fetching, add scheduler runtime, add report composition, add CI, add package migration, or call external services.

## Sequencing Decision

Current sequencing decision:

```text
implement_runtime_adapter_in_governed_pre_runtime_to_writer_order
```

The adapter should advance only through small governed passes. Each step must preserve the current kernel ownership boundary: the macro agent may provide evidence/context envelopes, but `ai-meta-kernel` owns intake interpretation, runtime reasoning, canonical task object production, response validation, and terminal artifact writing.

Phase R2 has implemented the first minimal reader slice for one explicit local input path. Phase R5 has implemented the minimal context-only envelope-to-intake mapping slice. Phase R6 refreshes the runtime invocation gate after that mapping slice. Phase R7 prepared the future runtime invocation implementation boundary. Phase R8 implements the minimal candidate-only runtime invocation slice. Phase R9 prepared the response validation boundary. Phase R10 implements the minimal local candidate-response validation slice. Phase R11 refreshes the writer gate after local response validation. Phase R12 prepares terminal writer implementation boundaries. Phase R13 selects response writer first, then failure writer. Phase R14 implements the minimal explicit-destination response writer. Phase R17 implements blocking failure classification. Phase R19 implements the minimal explicit-destination failure writer. R21 prepares the local terminal writer dry-run gate. R22 implements the minimal local terminal writer dry-run boundary. R23 refreshes the post-dry-run gate. R24 syncs the terminal writer dry-run milestone. R25 prepares the local invocation boundary. R26 defines the local invocation output contract. R27 defines the local invocation validation plan. R28 refreshes the local invocation implementation gate. R29 implements the minimal local invocation boundary. R30 refreshes the post-local-invocation implementation gate. The local invocation milestone is now synced, runtime artifact retention and cleanup policy preparation exists, runtime artifact retention and cleanup policy output contract exists, and runtime artifact retention and cleanup policy validation plan is current. The next sequence item is runtime artifact retention and cleanup policy implementation gate. This does not implement validation helper code, CLI behavior, queue discovery, polling, retry, cleanup automation, artifact deletion, fixture promotion automation, macro reporting, actual handoff, wrapper inclusion, production cross-project exchange, or full terminal writer orchestration.

## Intended Implementation Order

The future implementation order should be:

1. Runtime envelope reader boundary.
2. Envelope-to-intake mapping boundary.
3. Kernel runtime invocation boundary.
4. Kernel response validation boundary.
5. Response writer boundary.
6. Blocking failure classification boundary.
7. Blocking failure writer boundary.
8. Local terminal writer dry-run gate.
9. Terminal writer dry-run milestone sync.
10. Local invocation boundary preparation.
11. Local invocation boundary output contract.
12. Local invocation boundary validation plan.
13. Local invocation boundary implementation gate.
14. Local invocation minimal implementation.
15. Post-local-invocation implementation gate refresh.
16. Local invocation milestone sync.
17. Runtime artifact retention and cleanup policy preparation.
18. Runtime artifact retention and cleanup policy output contract.
19. Runtime artifact retention and cleanup policy validation plan.
20. Runtime artifact retention and cleanup policy implementation gate.
21. Runtime artifact retention and cleanup policy.

This order is intentionally narrow. It prevents writer behavior, CLI behavior, scheduler behavior, reporting behavior, and cleanup automation from arriving before the kernel can locally validate the inputs and outputs it owns.

## Step 1: Runtime Envelope Reader Boundary

Purpose:

- read exactly one local kernel input envelope artifact from a governed path or explicitly provided file;
- parse JSON deterministically;
- validate that the object is a `kernel_input_envelope`;
- stop before intake mapping.

Current status:

```text
minimal_explicit_file_reader_implemented_and_validated
```

Depends on:

- `KERNEL_FILE_EXCHANGE_ADAPTER_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_FIRST_SLICE_VALIDATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_BOUNDARY_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_ENVELOPE_READER_IMPLEMENTATION_VALIDATION_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_POST_READER_HANDOFF_GATE.md`;
- existing static fixture validation and adapter scaffold checks.

Must still not include:

- runtime queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- intake mapping;
- P0/P1 or P0-P10 invocation;
- response or failure writing;
- CLI behavior unless opened by a separate governed pass.

Additional governed pass required:

- a separate governed pass before reader behavior is broadened beyond one explicit local file.

## Step 2: Envelope-To-Intake Mapping Boundary

Purpose:

- convert one validated envelope into a kernel-owned `kernel_intake_context`;
- carry only allowed evidence, provenance, operator request, expectation, and deferred-behavior context;
- stop before P0/P1 execution.

Current status:

```text
minimal_context_only_intake_mapping_implemented_and_validated
```

Depends on:

- runtime envelope reader boundary;
- `KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_BOUNDARY_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_INTAKE_MAPPING_IMPLEMENTATION_VALIDATION_PLAN.md`;
- envelope guardrails that exclude canonical task object top-level fields.
- `validation/kernel_intake_mapping_contract_checks.py`.

Must still not include:

- canonical task object generation;
- task classification conclusions;
- risk profile conclusions;
- status flags;
- handoff decisions;
- response state classification;
- P0/P1 or P0-P10 execution;
- response or failure writing.

Additional governed pass required:

- a governed pass before mapping output is broadened beyond context-only `kernel_intake_context`.
- any future code change must still prove context-only output or explicitly govern the next boundary before P0/P1 execution.

## Step 3: Kernel Runtime Invocation Boundary

Purpose:

- pass a validated `kernel_intake_context` into a kernel-owned runtime entrypoint;
- preserve `ai-meta-kernel` as the only owner of P0-P10 reasoning and canonical task object production;
- return a candidate kernel response object for validation.

Depends on:

- intake mapping implementation;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_BOUNDARY_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RUNTIME_INVOCATION_IMPLEMENTATION_VALIDATION_PLAN.md`;
- a defined kernel-owned P0/P1 or P0-P10 invocation entrypoint;
- unchanged canonical kernel contracts.

Current status:

```text
minimal_candidate_only_runtime_invocation_implemented_and_validated
```

Must still not include:

- macro-side reasoning substitution;
- schema repair after runtime output;
- terminal response validation;
- response artifact writing;
- failure artifact writing;
- scheduler execution;
- report composition;
- external service calls.

Additional governed pass required:

- a terminal writer preparation pass before any validated local response is treated as writer-ready or passed to writers.

## Step 4: Kernel Response Validation Boundary

Purpose:

- validate the current candidate kernel response as a JSON object;
- validate the current candidate-only / pre-writer / non-terminal response markers;
- return one local validated response object before any terminal artifact is written.

Depends on:

- kernel runtime invocation boundary;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_BOUNDARY_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_RESPONSE_VALIDATION_IMPLEMENTATION_VALIDATION_PLAN.md`;
- `TASK_OBJECT_SCHEMA.json`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md`.

Current status:

```text
minimal_local_response_validation_implemented_and_validated
```

Must still not include:

- response artifact writing before validation passes;
- terminal `TASK_OBJECT_SCHEMA` response validation for the current non-canonical candidate;
- partial task object repair;
- silent field renaming;
- failure artifact writing without governed failure semantics;
- macro-side response production.

Additional governed pass required:

- a terminal writer preparation pass before any validated local response is passed to response or failure writers.

## Step 5: Response Writer Boundary

Purpose:

- write exactly one successful kernel response artifact after response validation passes;
- preserve the governed response filename pattern;
- keep canonical kernel task object fields unchanged.

Depends on:

- response validation boundary;
- `KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_TERMINAL_WRITER_IMPLEMENTATION_BOUNDARY_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_TERMINAL_WRITER_IMPLEMENTATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_TERMINAL_WRITER_IMPLEMENTATION_VALIDATION_PLAN.md`;
- `validation/kernel_response_writer_contract_checks.py`;
- governed artifact path and naming rules.

Current status:

```text
minimal_response_writer_implemented_and_validated
```

Must still not include:

- broadening response writing beyond one explicit local destination;
- overwriting existing response artifacts;
- writing invalid or partial task objects;
- writing both response and failure artifacts for the same invocation;
- failure artifact writing;
- artifact polling or watcher behavior;
- cleanup automation;
- report composition;
- macro-side response writing.

Additional governed pass required:

- a local terminal writer dry-run gate before response/failure writer availability is treated as orchestration readiness.

## Step 6: Blocking Failure Classification Boundary

Purpose:

- classify one local blocking failure source before failure writing;
- preserve governed failure stages;
- keep classification local, pre-writer, and non-terminal.

Current status:

```text
blocking_failure_classification_implemented_and_validated
```

Depends on:

- governed reader, intake mapping, invocation, response validation, and response writer failure stages;
- `validation/kernel_blocking_failure_classification_contract_checks.py`.

Must still not include:

- failure artifact writing;
- terminal writer calls;
- CLI behavior;
- queue discovery, polling, retry, or cleanup;
- macro report unlock;
- actual handoff.

Additional governed pass required:

- none for the minimal classification boundary; any broadening of failure stages or fields requires a separate governed pass.

## Step 7: Blocking Failure Writer Boundary

Purpose:

- write exactly one blocking failure artifact when a valid response artifact cannot be produced;
- preserve governed failure stages;
- ensure failures do not unlock downstream reporting.

Current status:

```text
minimal_failure_writer_implemented_and_validated
```

Depends on:

- a governed classified blocking failure input boundary;
- `KERNEL_FILE_EXCHANGE_ADAPTER_WRITER_BOUNDARY_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_TERMINAL_WRITER_IMPLEMENTATION_BOUNDARY_PLAN.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_TERMINAL_WRITER_IMPLEMENTATION_OUTPUT_CONTRACT.md`;
- `KERNEL_FILE_EXCHANGE_ADAPTER_TERMINAL_WRITER_IMPLEMENTATION_VALIDATION_PLAN.md`.
- `validation/kernel_failure_writer_contract_checks.py`.

Must still not include:

- non-blocking failure artifacts;
- partial canonical task object content in failure artifacts;
- both response and failure artifacts for one invocation;
- hidden continuation after terminal failure;
- report unlock behavior.

Additional governed pass required:

- a local terminal writer dry-run gate before writer availability is treated as orchestration readiness.

## Step 8: Local Terminal Writer Dry-Run Gate

Purpose:

- define how to exercise the existing minimal response writer and minimal failure writer in a governed local dry run;
- prove response/failure terminal selection expectations without adding CLI behavior or runtime handoff;
- keep the dry run local, explicit, and deterministic.

Current status:

```text
local_terminal_writer_dry_run_minimal_implementation_complete_and_post_gate_refreshed
```

Depends on:

- implemented and validated minimal response writer;
- implemented and validated blocking failure classification;
- implemented and validated minimal failure writer.

Must still not include:

- real artifact writing from dry-run;
- local invocation boundary from the dry-run step itself;
- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- artifact cleanup;
- macro report unlock;
- actual handoff.

Additional governed pass required:

- terminal writer dry-run milestone sync before local invocation or CLI behavior is proposed.

## Step 9: Terminal Writer Dry-Run Milestone Sync

Purpose:

- record that terminal writer local surfaces are now dry-run testable;
- preserve the distinction between dry-run candidates and real artifact writes;
- keep local invocation and CLI planning closed until the milestone is synced.

Current status:

```text
terminal_writer_dry_run_milestone_synced_local_invocation_boundary_ready
```

Depends on:

- implemented and validated minimal response writer;
- implemented and validated blocking failure classification;
- implemented and validated minimal failure writer;
- implemented and validated minimal local terminal writer dry-run boundary;
- refreshed post-local-terminal-writer-dry-run gate.

Must still not include:

- local invocation boundary;
- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- artifact cleanup;
- macro report unlock;
- actual handoff;
- full runtime orchestration.

Additional governed pass required:

- local invocation boundary preparation before any command boundary is added.
  This historical requirement has since been completed through R25-R29.

## Step 10: Local Invocation Boundary

Purpose:

- define how a developer invokes one local adapter run once reader, mapping, runtime invocation, response validation, and writers are implemented;
- keep invocation local, explicit, and deterministic.

Depends on:

- implemented and validated runtime reader;
- implemented and validated intake mapping;
- implemented and validated runtime invocation;
- implemented and validated response/failure terminal artifact behavior;
- completed terminal writer dry-run milestone sync.
- `KERNEL_FILE_EXCHANGE_ADAPTER_LOCAL_INVOCATION_BOUNDARY_PLAN.md`.

Current status:

```text
local_invocation_boundary_preparation_baseline
```

The current phase prepares the future boundary, intended input surface, intended
output surface, stop conditions, and validation themes. It does not implement a
local invocation function or command boundary.

Must still not include:

- local invocation implementation;
- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- artifact cleanup;
- macro report unlock;
- actual handoff;
- scheduler runtime;
- live fetching;
- report composition;
- CI behavior;
- multi-profile automation;
- open-ended runtime directory scanning unless separately governed.

Additional governed pass required:

- local invocation boundary output contract before any local invocation
  implementation or command boundary is implemented.

## Step 11: Local Invocation Boundary Output Contract

Purpose:

- define the local invocation result object;
- define whether terminal path outputs are candidates or written artifact paths;
- preserve exactly one terminal response or failure path for each future local
  invocation;
- keep macro report unlock and actual handoff markers absent or false.

Depends on:

- local invocation boundary preparation;
- terminal writer dry-run milestone sync;
- implemented and validated response/failure writer boundaries.
- `KERNEL_FILE_EXCHANGE_ADAPTER_LOCAL_INVOCATION_BOUNDARY_OUTPUT_CONTRACT.md`.

Current status:

```text
local_invocation_boundary_output_contract_baseline
```

The current phase defines the result object, terminal response/failure path
semantics, failure routing expectations, and blocked downstream behavior. It
does not implement local invocation code or CLI behavior.

Must still not include:

- local invocation implementation;
- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- artifact cleanup;
- macro report unlock;
- actual handoff;
- scheduler runtime;
- report composition.

Additional governed pass required:

- local invocation boundary validation plan before any local invocation
  implementation gate or command boundary is added.

## Step 12: Local Invocation Boundary Validation Plan

Purpose:

- define validation coverage for the local invocation result object;
- prove exactly one terminal path;
- reject dual artifact paths;
- preserve locked macro report and handoff markers;
- keep standalone helpers outside the wrapper until a separate governed wrapper
  inclusion pass.

Depends on:

- local invocation boundary output contract;
- implemented and validated response/failure writer boundaries;
- terminal writer dry-run milestone sync.
- `KERNEL_FILE_EXCHANGE_ADAPTER_LOCAL_INVOCATION_BOUNDARY_VALIDATION_PLAN.md`.

Current status:

```text
local_invocation_boundary_validation_plan_baseline
```

The current phase defines future validation coverage for local invocation result
object shape, terminal path selection, failure routing, fail-closed rejected
states, locked downstream markers, and standalone helper stance. It does not
implement local invocation code or validation helper code.

Must still not include:

- local invocation implementation;
- validation helper implementation;
- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- artifact cleanup;
- macro report unlock;
- actual handoff;
- scheduler runtime;
- report composition.

Additional governed pass required:

- local invocation boundary implementation gate before any local invocation code
  or validation helper code is added.

## Step 13: Local Invocation Boundary Implementation Gate

Purpose:

- decide whether the minimal local invocation implementation slice may open;
- preserve the explicit-input and explicit-output-destination boundary;
- keep CLI behavior, queue discovery, polling, retry, cleanup, macro report
  unlock, actual handoff, and wrapper inclusion closed unless separately
  governed.

Depends on:

- local invocation boundary plan;
- local invocation boundary output contract;
- local invocation boundary validation plan;
- implemented and validated reader, intake, candidate invocation, response
  validation, response writer, failure classification, failure writer, and
  terminal dry-run boundaries.
- `KERNEL_FILE_EXCHANGE_ADAPTER_LOCAL_INVOCATION_IMPLEMENTATION_GATE.md`.

Current status:

```text
local_invocation_implementation_gate_refreshed
```

Minimal local invocation implementation gate is complete. R29 has since
implemented the minimal local invocation slice.

Must still not include:

- local invocation implementation;
- validation helper implementation;
- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- artifact cleanup;
- macro report unlock;
- actual handoff;
- scheduler runtime;
- report composition.

Additional governed pass required:

- post-local-invocation gate refresh before any milestone sync or CLI, queue,
  scheduler, macro integration, production exchange, or handoff planning.

## Step 14: Local Invocation Minimal Implementation

Purpose:

- implement one explicit-envelope-path local invocation boundary;
- use one explicit output destination policy;
- return one deterministic local invocation result object;
- select exactly one terminal path;
- produce one response artifact path or one failure artifact path, never both;
- keep macro report unlock, actual handoff, and CLI behavior false.

Depends on:

- local invocation boundary implementation gate;
- implemented and validated reader, intake, candidate invocation, response
  validation, response writer, failure classification, failure writer, and
  terminal dry-run boundaries.

Current status:

```text
local_invocation_minimal_implementation_slice_complete
```

The minimal local invocation boundary is implemented and validated by a
standalone helper. It is limited to one explicit envelope path, one explicit
output destination policy, one deterministic result object, exactly one
terminal path, and one response artifact path or one failure artifact path,
never both.

Must still not include:

- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- artifact cleanup;
- scheduler runtime;
- live fetching;
- report composition;
- macro report unlock;
- actual handoff;
- wrapper inclusion;
- full runtime orchestration.

Additional governed pass required:

- post-local-invocation implementation gate refresh before milestone sync.

## Step 15: Post-Local-Invocation Implementation Gate Refresh

Purpose:

- record that the minimal local invocation boundary exists;
- distinguish minimal local invocation from CLI, queue worker, scheduler,
  macro report unlock, actual handoff, production exchange, and full runtime
  adapter readiness;
- decide the next governed phase.

Depends on:

- local invocation minimal implementation;
- standalone local invocation helper;
- `KERNEL_FILE_EXCHANGE_ADAPTER_POST_LOCAL_INVOCATION_IMPLEMENTATION_GATE.md`.

Current status:

```text
post_local_invocation_implementation_gate_refreshed
```

Must still not include:

- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- artifact cleanup;
- scheduler runtime;
- live fetching;
- report composition;
- macro report unlock;
- actual handoff;
- wrapper inclusion;
- production cross-project exchange;
- full runtime orchestration.

Additional governed pass required:

- local invocation milestone sync before any CLI, queue, scheduler, macro
  integration, production exchange, or handoff planning.

## Step 16: Local Invocation Milestone Sync

Purpose:

- sync the completed local invocation milestone;
- preserve the distinction between local invocation and production runtime
  exchange;
- keep CLI, queue, scheduler, macro reporting, and handoff behavior closed.

Depends on:

- post-local-invocation implementation gate refresh;
- minimal local invocation implementation;
- standalone local invocation helper.

Current status:

```text
local_invocation_milestone_synced_runtime_artifact_policy_ready
```

The local invocation milestone is synced. The minimal local invocation boundary
exists and remains bounded to explicit local envelope input, explicit output
destination policy, exactly one terminal path, and no macro report unlock or
actual handoff.

Must still not include:

- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- artifact cleanup;
- scheduler runtime;
- macro report unlock;
- actual handoff;
- wrapper inclusion;
- production cross-project exchange;
- full runtime orchestration.

Additional governed pass required:

- runtime artifact retention and cleanup policy preparation before generated
  runtime artifacts are governed for retention, review, fixture promotion, or
  cleanup decisions.

## Step 17: Runtime Artifact Retention And Cleanup Policy Preparation

Purpose:

- prepare the policy surface for generated runtime artifact retention, review,
  fixture promotion, and cleanup decisions;
- keep policy preparation distinct from cleanup automation;
- preserve the difference between local artifacts and production
  cross-project exchange.

Depends on:

- synced local invocation milestone;
- terminal artifact writer behavior;
- human review expectations for restricted, blocked, failed, missing, or
  ambiguous states.

Current status:

```text
runtime_artifact_retention_cleanup_policy_preparation_baseline
```

Must still not include:

- cleanup automation;
- artifact deletion implementation;
- automatic fixture promotion;
- fixture promotion automation;
- archive/export automation;
- scheduler cleanup;
- CI cleanup;
- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- macro report unlock;
- actual handoff;
- production cross-project exchange;
- full runtime orchestration.

Additional governed pass required:

- runtime artifact retention and cleanup policy output contract before
  automation, deletion behavior, or fixture promotion automation touches
  generated runtime artifacts.

## Step 18: Runtime Artifact Retention And Cleanup Policy Output Contract

Purpose:

- define the required output shape for the retention and cleanup policy;
- preserve artifact category distinctions before any automation is introduced;
- keep deletion and fixture promotion as governed future behavior only.

Depends on:

- runtime artifact retention and cleanup policy preparation;
- local invocation minimal implementation;
- terminal artifact writer behavior;
- human review expectations for restricted, blocked, failed, missing, or ambiguous states.

Current status:

```text
runtime_artifact_retention_cleanup_policy_output_contract_baseline
```

Must still not include:

- cleanup implementation;
- artifact deletion implementation;
- fixture promotion automation;
- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- scheduler runtime;
- macro report unlock;
- actual handoff;
- production cross-project exchange.

Additional governed pass required:

- runtime artifact retention and cleanup policy validation plan before cleanup
  implementation, deletion behavior, fixture promotion automation, or
  validation helper code is considered.

## Step 19: Runtime Artifact Retention And Cleanup Policy Validation Plan

Purpose:

- define validation coverage for the future policy output object;
- prove valid artifact categories, retention decisions, promotion decisions,
  cleanup decisions, and locked markers;
- keep validation planning separate from validation helper implementation.

Depends on:

- runtime artifact retention and cleanup policy output contract;
- local invocation minimal implementation;
- terminal artifact writer behavior;
- human review expectations for restricted, blocked, failed, missing, or ambiguous states.

Current status:

```text
runtime_artifact_retention_cleanup_policy_validation_plan_baseline
```

Must still not include:

- cleanup implementation;
- artifact deletion implementation;
- fixture promotion automation;
- validation helper implementation;
- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- scheduler runtime;
- macro report unlock;
- actual handoff;
- production cross-project exchange.

Additional governed pass required:

- runtime artifact retention and cleanup policy implementation gate before
  validation helper implementation, cleanup implementation, deletion behavior,
  or fixture promotion automation is considered.

## Step 20: Runtime Artifact Retention And Cleanup Policy Implementation Gate

Purpose:

- decide whether a minimal policy implementation slice may open;
- preserve validation helper implementation, cleanup implementation, deletion
  behavior, and fixture promotion automation as closed unless separately
  governed;
- keep CLI, queue discovery, polling, retry, macro report unlock, and actual
  handoff closed.

Depends on:

- runtime artifact retention and cleanup policy preparation;
- runtime artifact retention and cleanup policy output contract;
- runtime artifact retention and cleanup policy validation plan;
- local invocation minimal implementation;
- terminal artifact writer behavior.

Current status:

```text
runtime_artifact_retention_cleanup_policy_implementation_gate_next
```

Must still not include:

- validation helper implementation;
- cleanup implementation;
- artifact deletion implementation;
- fixture promotion automation;
- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- scheduler runtime;
- macro report unlock;
- actual handoff;
- production cross-project exchange.

Additional governed pass required:

- runtime artifact retention and cleanup policy decision before cleanup
  implementation, deletion behavior, or fixture promotion automation is
  considered.

## Step 21: Runtime Artifact Retention And Cleanup Policy

Purpose:

- decide when generated runtime artifacts are retained, cleaned up, or promoted into reviewed fixtures;
- keep generated runtime material distinct from committed static fixtures.

Depends on:

- local invocation minimal implementation;
- terminal artifact writer behavior;
- human review expectations for restricted, blocked, failed, missing, or ambiguous states.

Must still not include:

- cleanup implementation;
- artifact deletion implementation;
- automatic fixture promotion;
- fixture promotion automation;
- validation helper implementation;
- archive/export automation;
- scheduler cleanup;
- CI cleanup;
- report unlock behavior.

Additional governed pass required:

- an artifact retention, cleanup, and fixture promotion policy before automation touches generated runtime artifacts.

## Blocked Behaviors Across All Steps

No step in this sequence may silently introduce:

- runtime reader behavior beyond one explicit local file before a governed broadening pass opens;
- live fetching;
- uncontrolled open-web crawling;
- scheduler runtime;
- report composition;
- archive/export automation;
- CI behavior;
- package migration;
- external service calls;
- source governance changes;
- kernel contract modifications;
- schema drift;
- macro-side canonical kernel task object generation;
- macro-side kernel response artifact writing;
- production cross-project exchange;
- cleanup implementation;
- artifact deletion implementation;
- fixture promotion automation;
- validation helper implementation;
- CLI behavior;
- queue discovery;
- polling or watcher behavior;
- retry/backoff behavior;
- hidden runtime handoff.

## Recommended Next Phase

Perform a `runtime artifact retention and cleanup policy implementation gate`.

That pass should decide whether any minimal policy implementation slice may
open without implementing validation helper code, cleanup automation, artifact
deletion, fixture promotion automation, CLI behavior, queue discovery,
polling, retry, scheduler behavior, live fetching, report composition, CI,
package migration, external service calls, macro report unlock, actual handoff
execution, wrapper inclusion, production cross-project exchange, or full
runtime orchestration.
