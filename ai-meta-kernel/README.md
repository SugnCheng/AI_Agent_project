# AI Meta Kernel

AI Meta Kernel is a specification-first project for a reusable meta-cognitive layer that must run before any downstream agent performs domain work.

The workspace has two deliberately separate projects:

1. **Meta-Layer / Meta-Cognitive Kernel**
   - The primary product of this repository.
   - Provides shared framing, risk calibration, habit triggering, verification, challenge loops, and handoff contracts.
   - Produces a structured task object and handoff artifact before downstream agent execution.
   - Optimizes for transferable reasoning discipline over agent-specific convenience.

2. **Macro-Financial Intelligence Agent**
   - A sibling reference implementation in `../macro-financial-intelligence-agent/`, not the final product.
   - Used to test whether the Meta-Layer is complete, usable, and transferable.
   - Focuses on evidence synthesis, policy-risk monitoring, market-risk context, research reporting, and archive/export workflows for Hong Kong, Macau, Taiwan, Japan, the United States, and Europe.
   - Must not produce direct trading instructions or personalized investment recommendations.

## Current Scope

This initial version creates a reviewable documentation and prompt skeleton. It intentionally avoids implementation code until the kernel contracts are stable.

## Repository Map

- `docs/`: project vision, architecture, terminology, and decisions.
- `meta-layer/`: core kernel constitution, runtime pipeline, policies, prompts, habits, and orchestration rules.
- `examples/`: sample raw requests, kernel outputs, handoff objects, and report outlines.
- `validation/`: validation plan, matrix, failure cases, and retrospective template.
- `future-agents/`: notes for future downstream agents that should later validate transferability.

Reference agents live outside this kernel repo. The first reference agent is `../macro-financial-intelligence-agent/`.

## Operating Principle

Every downstream agent must receive work through the Meta-Layer. The kernel is responsible for clarifying intent, surfacing risk, selecting relevant reasoning habits, defining verification requirements, challenging weak assumptions, and packaging a handoff object.

If a downstream agent would prefer a shortcut that bypasses framing, verification, ethics, or handoff discipline, the shortcut is invalid by default.

## First Review Questions

- Does the kernel pipeline capture the right pre-agent responsibilities?
- Are the risk and verification gates explicit enough to be tested?
- Does the macro-financial reference agent validate the kernel without becoming the center of the project?
- Are handoff objects concrete enough for future agents to consume?
