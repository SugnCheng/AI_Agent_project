# Breaking Change Rules

## Purpose

Define how changes to the Meta-Layer v1.0 Candidate baseline should be classified.

## Non-Breaking Changes

These changes normally do not require a breaking-change review:

- grammar, typo, or formatting fixes;
- clarifying examples that do not change contract behavior;
- adding non-normative notes;
- adding validation cases that do not change required fields;
- improving wording while preserving obligations;
- adding reference-agent examples that do not modify the kernel contract.

## Review-Required Changes

These changes require explicit review before merge:

- adding optional fields to the task object schema;
- adding new `status_flags` candidates;
- adding new risk categories;
- adding new downstream output formats;
- changing validation scoring thresholds;
- changing K1/K2/K3 guidance without changing their core meaning;
- adding new reference agent adapters;
- changing examples in a way that may imply new contract behavior.

## Breaking Changes

These changes are breaking:

- removing or renaming any top-level task object field;
- changing canonical field names such as `framed_objective`, `task_classification`, `risk_profile`, `triggered_habits`, `structural_decomposition`, `required_checks`, `status_flags`, or `downstream_recommendation`;
- changing the shape of `required_checks`;
- changing allowed values or meanings of `status_flags`;
- changing allowed values or meanings of `downstream_recommendation.mode`;
- weakening verification, risk, ethics, uncertainty, or reframe requirements;
- allowing downstream agents to bypass Layer 0;
- making Macro-Financial Intelligence Agent a direct trading recommendation agent;
- changing the canonical source-of-truth rule;
- making `KERNEL_OUTPUT_TEMPLATE.json` incompatible with `TASK_OBJECT_SCHEMA.json`.

## Required Breaking Change Process

A breaking change should include:

- affected files;
- reason for change;
- migration note;
- updated schema or prompt contract;
- updated validation cases;
- explicit statement that the v1.0 candidate baseline is superseded.
