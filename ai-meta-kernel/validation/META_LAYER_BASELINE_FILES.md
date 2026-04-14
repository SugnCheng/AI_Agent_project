# Meta-Layer v1.0 Candidate Baseline Files

## Purpose

This file lists the v1.0 candidate baseline files and their role in the Meta-Layer contract.

## Core Baseline

| File | Role |
| --- | --- |
| `META_LAYER_MASTER_SPEC.md` | Canonical mother spec and source of truth. |
| `docs/META_LAYER_V1_FREEZE_NOTE.md` | Freeze scope, frozen areas, and deferred work. |
| `docs/ALIGNMENT_REVIEW.md` | Strict alignment review against the mother spec. |
| `meta-layer/README.md` | Meta-Layer directory overview. |
| `meta-layer/CONSTITUTION.md` | Kernel constitution and policy priority. |
| `meta-layer/RUNTIME_PIPELINE.md` | Runtime pipeline and handoff stages. |
| `meta-layer/TASK_OBJECT_SCHEMA.json` | Machine-readable task object contract. |
| `meta-layer/HANDOFF_CONTRACT.md` | Downstream handoff obligations and return-to-kernel rules. |
| `meta-layer/DECISION_GATES.md` | Gate A-F and gate-controlled fields. |
| `meta-layer/STATUS_FLAGS.md` | Status flag semantics and interactions. |
| `meta-layer/CHALLENGE_LOOP.md` | Required challenge-loop checks. |
| `meta-layer/INSTRUCTION_HIERARCHY.md` | Instruction and policy priority rules. |
| `meta-layer/KERNEL_MODES.md` | K1/K2/K3 mode definitions. |
| `meta-layer/REFRAME_PROTOCOL.md` | Reframe triggers and return format. |

## Habit Modules

| File | Role |
| --- | --- |
| `meta-layer/habits/H1_EVALUATING_CLAIMS.md` | Claim, evidence, source, and plausibility habit. |
| `meta-layer/habits/H2_ANALYZING_INFERENCES.md` | Observation, inference, and competing hypothesis habit. |
| `meta-layer/habits/H3_WEIGHING_DECISIONS.md` | Alternatives, tradeoffs, stakeholder, and reversibility habit. |
| `meta-layer/habits/H4_FACILITATING_DISCOVERY.md` | Hypothesis, model, prediction, and next-test habit. |
| `meta-layer/habits/H5_SOLVING_PROBLEMS.md` | Goal-obstacle-constraint and feasibility habit. |
| `meta-layer/habits/H6_DESIGN_THINKING.md` | Iterative creation and prototype/final distinction habit. |
| `meta-layer/habits/H7_COMPOSITION.md` | Clear expression and audience-fit habit. |
| `meta-layer/habits/H8_MULTIMODAL_DESIGN.md` | Information hierarchy and cognitive-load habit. |
| `meta-layer/habits/H9_NEGOTIATION.md` | Positions/interests and persuasion process habit. |
| `meta-layer/habits/H10_WORKING_WITH_DIFFERENCES.md` | Role, motivation, and collaboration-difference habit. |
| `meta-layer/habits/H11_ETHICAL_FRAMING.md` | Ethics, impacted parties, legitimacy, and boundary habit. |

## Policy Layer

| File | Role |
| --- | --- |
| `meta-layer/policies/MEMORY_POLICY.md` | Memory scope, admission, provenance, and conflict rules. |
| `meta-layer/policies/USER_PREFERENCE_POLICY.md` | Preference categories, priority, and alignment triggers. |
| `meta-layer/policies/CONFIDENCE_POLICY.md` | Confidence levels, downgrades, and disclosure requirements. |
| `meta-layer/policies/VERIFICATION_POLICY.md` | Verification triggers, priority, and failure handling. |
| `meta-layer/policies/REFRAME_POLICY.md` | Mandatory reframe cases and integrity rules. |
| `meta-layer/policies/ESCALATION_POLICY.md` | Risk, ethics, verification, ambiguity, and specialization escalation. |

## Orchestration And Prompts

| File | Role |
| --- | --- |
| `meta-layer/orchestration/ORCHESTRATOR_PSEUDOCODE.md` | Kernel orchestration pseudocode. |
| `meta-layer/orchestration/TRIGGER_MATRIX.md` | Task type to habit trigger mapping. |
| `meta-layer/orchestration/MODULE_INTERACTION_RULES.md` | Module override and interaction rules. |
| `meta-layer/prompts/KERNEL_SYSTEM_PROMPT.md` | Codex-ready kernel system prompt. |
| `meta-layer/prompts/KERNEL_CONTROLLER_PROMPT.md` | Controller workflow prompt. |
| `meta-layer/prompts/KERNEL_OUTPUT_TEMPLATE.json` | Schema-compatible output template. |

## Validation Baseline

| File | Role |
| --- | --- |
| `validation/KERNEL_VALIDATION_MATRIX.md` | Capability-level validation matrix. |
| `validation/TEST_PLAN.md` | Validation test groups and required artifacts. |
| `validation/FAILURE_CASES.md` | Known failure cases to test against. |
| `validation/RETRO_TEMPLATE.md` | Template for feeding validation findings back into the kernel. |
| `validation/BREAKING_CHANGE_RULES.md` | Change classification rules. |
