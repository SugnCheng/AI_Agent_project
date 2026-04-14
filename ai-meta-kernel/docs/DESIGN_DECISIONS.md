# Design Decisions

## DD-001: Kernel Before Reference Agents

Decision: Build the Meta-Layer before expanding downstream agents.

Reason: Reference agents exist to validate the kernel. If agent convenience drives the design too early, the kernel may overfit to one domain.

## DD-002: Macro-Financial Agent as First Reference

Decision: Use Macro-Financial Intelligence Agent as the first reference implementation.

Reason: It stresses source quality, recency, policy interpretation, uncertainty, and financial-risk boundaries without making direct trading advice the default product.

## DD-003: Habit Modules as Reusable Units

Decision: Model Minerva-style habits as H1-H11 modules.

Reason: The kernel should trigger reusable cognitive operations across tasks instead of relying on scenario-specific prompts.
