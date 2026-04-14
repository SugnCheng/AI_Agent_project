# Kernel Adoption Guide

## Purpose

This guide explains how an external downstream agent should adopt the Meta-Layer.

Reference agents should live outside `ai-meta-kernel/`. The first reference agent is the sibling project `../macro-financial-intelligence-agent/`.

## Required Integration Pattern

1. Read `META_LAYER_MASTER_SPEC.md`.
2. Accept `meta-layer/TASK_OBJECT_SCHEMA.json` as the kernel handoff contract.
3. Treat `meta-layer/prompts/KERNEL_OUTPUT_TEMPLATE.json` as a schema-compatible example, not as a final answer format.
4. Implement an adapter that consumes:
   - `framed_objective`
   - `task_classification`
   - `risk_profile`
   - `triggered_habits`
   - `structural_decomposition`
   - `required_checks`
   - `status_flags`
   - `downstream_recommendation`
5. Return the task to the kernel if the handoff is structurally insufficient.

## Downstream Agent Rules

External agents must not:

- bypass Layer 0;
- silently reconstruct missing kernel fields;
- treat assumptions as facts;
- ignore `status_flags`;
- weaken verification, risk, ethics, or uncertainty requirements.

## Sibling Project Layout

```text
AI_agent_project/
  ai-meta-kernel/
  macro-financial-intelligence-agent/
```
