# Multi-phase plan

Use when the requested deliverable is a plan for phases or multiple PRs. Planning does not itself authorize execution.

1. Ground the relevant subsystems through read-only research agents. Gather source paths, ownership, conventions, launch commands, and available verification surfaces.
2. Separate observable uncertainties from product choices. Resolve the former with evidence or an authorized scratch prototype. Keep unresolved product constraints explicit.
3. Define the dependency graph. Independent changes branch from the base; a dependent change waits for its prerequisite or builds on its exact branch revision.
4. Write an executable plan. Each unit contains:
   - Outcome and consumer-visible acceptance condition.
   - Dependencies, input revision, and files or boundaries it owns.
   - Implementation steps and the intended data shape.
   - Verification commands or user actions, expected results, and evidence locations.
   - Review responsibility, integration owner, and any user checkpoint.
5. Name the execution workflow: [Autopilot full](autopilot-full.md) for independent deliverables, [Autopilot stack](autopilot-stack.md) for one dependent chain, or [Orchestrate](orchestrate.md) for a standing program.
6. Check that every acceptance condition has a plausible observation, every dependency exists, and parallel writers have disjoint ownership. Use an independent reviewer for a substantial plan.

Scale verification to the changed surface. A UI change needs the user journey; a performance claim needs comparable measurements. Do not manufacture ten lanes or a benchmark for a change that has no such claim.

Deliver the plan path, dependency order, checkpoints, resolved uncertainties, and remaining questions. Start implementation only when it is part of the user's request.
