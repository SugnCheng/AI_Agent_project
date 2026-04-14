# Changelog

## 0.1.0 - Initial Skeleton

- Created repository skeleton for Meta-Layer, reference agents, examples, validation, and future-agent notes.
- Added first draft of README, roadmap, architecture overview, constitution, runtime pipeline, task schema, kernel system prompt, macro-financial adapter spec, validation hooks, and validation matrix.

## 0.2.0 - Master Spec Alignment

- Added `META_LAYER_MASTER_SPEC.md` as canonical source of truth.
- Added alignment review.
- Expanded core kernel files for handoff, gates, flags, challenge loop, instruction hierarchy, modes, policies, habit modules, orchestration, controller prompt, and output template.
- Updated `TASK_OBJECT_SCHEMA.json` to include structured `required_checks`.

## 0.3.0 - Workspace Restructure

- Moved the Macro-Financial Intelligence Agent out of `ai-meta-kernel/` into the sibling `macro-financial-intelligence-agent/` project.
- Removed the kernel repo's agent-specific `agents/` structure.
- Added `docs/ADOPTION_GUIDE.md` for external downstream agent integration.
