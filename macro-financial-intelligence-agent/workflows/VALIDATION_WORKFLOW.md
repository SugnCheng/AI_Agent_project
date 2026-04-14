# Validation Workflow

Kernel baseline: `../ai-meta-kernel/` v1.0 candidate.

## Purpose

Run the Macro-Financial Intelligence Agent as a reference implementation that tests the Meta-Layer contract.

This workflow is not a product workflow. It is a validation workflow.

## Steps

1. Select a raw request from `examples/SAMPLE_RAW_REQUESTS.md`.
2. Produce or provide a kernel handoff object using the `ai-meta-kernel` v1.0 candidate contract.
3. Check whether the handoff includes:
   - `framed_objective`
   - `task_classification`
   - `risk_profile`
   - `triggered_habits`
   - `structural_decomposition`
   - `required_checks`
   - `status_flags`
   - `downstream_recommendation`
4. Decide whether the agent may accept, restrict, or reject the handoff.
5. If accepted, map the handoff to ingestion, analysis, and reporting workflow steps.
6. If rejected, write a return-to-kernel note.
7. Record the result in `validation/RETRO_LOG.md`.

## Validation Mapping

| Agent step | Kernel capability tested |
| --- | --- |
| Handoff field inspection | Handoff contract |
| Scope and non-goal check | Framing |
| Source freshness check | Verification |
| Competing interpretation handling | Challenge loop |
| Restricted or rejected handoff | Status flags and return-to-kernel behavior |
| Confidence and uncertainty notes | Confidence and verification policy |

## Stop Conditions

Stop and return to kernel when:

- direct trading advice is requested;
- jurisdiction or time window is missing and material;
- current claims lack required verification;
- status flags block handoff;
- assumptions are being treated as facts;
- output would hide material uncertainty.
