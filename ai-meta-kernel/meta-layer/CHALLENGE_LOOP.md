# Challenge Loop

Source of truth: `../META_LAYER_MASTER_SPEC.md`.

## Purpose

The challenge loop catches weak framing, weak inference, missing constraints, overconfidence, and insufficient handoff clarity before downstream execution.

## When Required

Run the full challenge loop when:

- risk is medium or high;
- H3 Weighing Decisions is triggered and risk is at least medium;
- H11 Ethical Framing is triggered;
- the task is irreversible, high-impact, or externally consequential;
- the task asks for a recommendation based on incomplete or unstable facts.

Low-risk tasks may use a shortened challenge loop, but still require a wrong-question and missing-constraint check.

## Standard Checks

1. **Wrong-question check**
   - Are we solving the surface problem or the real problem?

2. **Missing-constraint check**
   - Are critical limits, resources, time horizon, or success criteria missing?

3. **Alternative-explanation check**
   - Are there other plausible explanations or framings?

4. **Counterargument check**
   - What is the strongest objection to the current conclusion or handoff?

5. **Overconfidence check**
   - Which claims are assumptions or provisional inferences?

6. **Stakeholder check**
   - Who is affected, and are impacts asymmetric?

7. **Ethics / externality check**
   - Are fairness, privacy, safety, legitimacy, or common-good concerns present?

8. **Simplicity / robustness check**
   - Is there a simpler, more robust path?

9. **Reversibility check**
   - Is the decision reversible? If not, has review depth increased?

10. **Communication / handoff clarity check**
    - Can the downstream agent execute without misunderstanding the task?

## Outputs

The challenge loop must emit:

- checks performed;
- issues found;
- resolution or remaining concern;
- whether the task can proceed;
- whether confidence must be downgraded;
- whether the handoff must be restricted.
