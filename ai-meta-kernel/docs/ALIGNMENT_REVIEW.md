# Alignment Review

Review source: `META_LAYER_MASTER_SPEC.md`

Review mode: Canonicalization Pass.

## Strict Status Standard

- `aligned`: substantively equivalent to the master spec for that file's responsibility.
- `partially_aligned`: has core correspondence, but omits important sections, details, constraints, or decision consequences.
- `misaligned`: direction or structure diverges from the master spec, or weakens a material obligation.

This review intentionally uses a stricter standard than the initial bootstrap review.

## Summary

The repository now has a fuller formal `META_LAYER_MASTER_SPEC.md`, and the split files broadly follow the same direction.

However, not every split file is yet substantively equivalent to the master spec. Several files remain useful first-pass drafts but should be treated as `partially_aligned` until they preserve the same operational consequences as the mother spec.

The Macro-Financial Intelligence Agent remains a validation reference implementation, not the project center.

## File-Level Review

| File | Status | Reason |
| --- | --- | --- |
| `META_LAYER_MASTER_SPEC.md` | aligned | Formal mother spec now preserves the required canonical sections and stricter alignment rule. |
| `AGENTS.md` | partially_aligned | Correctly says Meta-Layer comes first and reference agents must not bypass it, but does not fully encode the strict policy priority, gate consequences, or H1-H11 trigger obligations. |
| `README.md` | partially_aligned | Correct project framing, but does not fully state the canonical alignment rule or full mother-spec hierarchy. |
| `ROADMAP.md` | partially_aligned | Correct phase ordering, but not yet tied to stricter canonical fidelity milestones. |
| `docs/ARCHITECTURE_OVERVIEW.md` | partially_aligned | Captures three-layer flow and reference-agent boundary, but lacks full Layer 0/1/2 decision authority language and tool-led reasoning constraint depth. |
| `meta-layer/CONSTITUTION.md` | partially_aligned | Contains C-01 through C-10 and policy priority, but still compresses some details from the formal mother spec. |
| `meta-layer/RUNTIME_PIPELINE.md` | partially_aligned | Contains classify, decompose, gate, and handoff, but uses P0-P12 rather than the mother spec's P0-P10 canonical sequence and adds return/retro stages that should be marked as post-kernel extension. |
| `meta-layer/TASK_OBJECT_SCHEMA.json` | partially_aligned | Core field names are normalized with the mother spec; remaining partial alignment is about schema-level examples, modes, and full decision consequences rather than naming. |
| `meta-layer/prompts/KERNEL_SYSTEM_PROMPT.md` | partially_aligned | Captures core role and output contract, but does not yet include the full instruction hierarchy and mode behavior. |
| `../macro-financial-intelligence-agent/ADAPTER_SPEC.md` | partially_aligned | Correctly treats the agent as validation reference and rejects trading advice, but should more explicitly map each workflow to kernel validation goals. |
| `../macro-financial-intelligence-agent/VALIDATION_HOOKS.md` | partially_aligned | Covers core validation hooks, but does not yet fully score policy interaction, mode behavior, and return-to-kernel behavior. |
| `validation/KERNEL_VALIDATION_MATRIX.md` | partially_aligned | Covers major kernel capabilities, but still needs stricter pass/fail tests for policy priority, mode selection, and task object contract equivalence. |
| `meta-layer/HANDOFF_CONTRACT.md` | partially_aligned | Strong first-pass contract and now uses canonical task object field naming; still needs richer examples for return-to-kernel behavior. |
| `meta-layer/DECISION_GATES.md` | partially_aligned | Captures Gate A-F, but needs direct traceability to P8 Gate and status flag derivation. |
| `meta-layer/STATUS_FLAGS.md` | partially_aligned | Captures required flags and interactions, but needs examples of blocking versus delegated unresolved states. |
| `meta-layer/CHALLENGE_LOOP.md` | partially_aligned | Captures all ten checks, but should explicitly define shortened K1 versus full K3 behavior. |
| `meta-layer/INSTRUCTION_HIERARCHY.md` | aligned | Substantively reflects constitution, risk/verification, reframe, user alignment, style, and downstream convenience ordering. |
| `meta-layer/KERNEL_MODES.md` | aligned | Substantively matches K1/K2/K3 mode definitions and restrictions. |
| `meta-layer/policies/MEMORY_POLICY.md` | partially_aligned | Captures scope separation and provenance, but needs direct integration with task/session/long-term update examples. |
| `meta-layer/policies/USER_PREFERENCE_POLICY.md` | aligned | Substantively matches preference categories, alignment triggers, and non-override constraints. |
| `meta-layer/policies/CONFIDENCE_POLICY.md` | aligned | Substantively matches confidence levels, high-confidence requirements, forced downgrade, and disclosure. |
| `meta-layer/policies/VERIFICATION_POLICY.md` | aligned | Substantively matches mandatory verification cases, priority handling, failure behavior, and handoff requirement. |
| `meta-layer/policies/REFRAME_POLICY.md` | aligned | Substantively matches mandatory reframe cases and integrity rule. |
| `meta-layer/policies/ESCALATION_POLICY.md` | aligned | Substantively matches escalation categories and required consequences. |
| `meta-layer/orchestration/TRIGGER_MATRIX.md` | partially_aligned | Captures routing and overrides, but should include exact primary/secondary task classification consequences and examples. |
| `meta-layer/orchestration/MODULE_INTERACTION_RULES.md` | aligned | Substantively captures trigger selection, primary/support distinction, ethical override, decision override, evidence override, reframe override, and output normalization. |
| `meta-layer/orchestration/ORCHESTRATOR_PSEUDOCODE.md` | partially_aligned | Correct overall flow, but should be normalized to the mother spec's P0-P10 naming and gate semantics. |
| `meta-layer/prompts/KERNEL_CONTROLLER_PROMPT.md` | partially_aligned | Correct controller sequence, but not yet fully equivalent to the canonical system prompt hierarchy. |
| `meta-layer/prompts/KERNEL_OUTPUT_TEMPLATE.json` | partially_aligned | Naming now matches `TASK_OBJECT_SCHEMA.json`; still a template and not a full example covering all modes and gate outcomes. |

## No Current Misalignment Findings

No file currently appears to reverse or contradict the mother spec's direction. The remaining issues are mostly partial alignment, naming drift, or incomplete operational detail.

## Canonical Fidelity Gaps To Fix Next

1. Decide whether `RUNTIME_PIPELINE.md` should use exactly P0-P10 or explicitly mark P11/P12 as post-kernel extension.
2. Expand `KERNEL_SYSTEM_PROMPT.md` and `KERNEL_CONTROLLER_PROMPT.md` to encode mode behavior and instruction hierarchy more completely.
3. Add policy-priority tests and mode-selection tests to `validation/KERNEL_VALIDATION_MATRIX.md`.
4. Tighten `VALIDATION_HOOKS.md` so each macro-financial workflow maps to framing, classification, verification, challenge, status flag, policy, and handoff validation.
5. Add schema-level validation examples for each handoff mode.

## Deferred Work

Do not prioritize new Macro-Financial Intelligence Agent features until the canonical naming and kernel prompt hierarchy are reconciled.
