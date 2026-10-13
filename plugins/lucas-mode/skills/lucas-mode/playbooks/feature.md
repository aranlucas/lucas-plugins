# Feature

**You own the design. Plan, review, verify.** Delegate implementation. Stay in the lead.

1. [Ground](../references/agent-workflows.md#ground) over the affected subsystem.
2. [Architect](../references/agent-workflows.md#architect-and-arena) for parallel design exploration.
3. Write the throughput checkpoint as four todo items. A dimension that genuinely does not apply (single file, no fan-out) keeps its item with `n/a: <reason>` rather than being dropped:
   - **Blocking first steps.** Gates run before fan-out.
   - **Independent workstreams.** Disjoint files, services, or layers parallelize. Shared writes serialize.
   - **Shared mutable state.** Default to splitting the target (the [separate before serializing shared state](../references/principles/separate-before-serializing-shared-state.md) principle). Serialize only for real invariants.
   - **Smallest safe decomposition.** If one worker is best, name why.
4. Delegate code-writing to a subagent through [T3 orchestration](../references/t3-orchestration.md) with the selected implementation model and a specific scope (file paths, named data shape and its organizing structure per [model the domain](../references/principles/model-the-domain.md), a state machine over scattered booleans, a table/registry over branching, a typed model over repeated shape assumptions, chosen before the delegate writes logic, and success criteria). When the implementation admits multiple valid shapes (error handling, abstraction layer, test structure), delegate via the [Arena](../references/agent-workflows.md#architect-and-arena) workflow instead so the runners surface the alternatives and the cross-judge guards the pick. Keep implementation and review separate for nontrivial changes. If delegation is unavailable, report that limit and retain the independent review gate. T3 parents waiting only on async children yield for completion notifications. Keep comments for non-obvious constraints and reasons. Surgical edits, re-ground against the source for upstream-derived files. Port shared-primitive improvements to all consumers and verify each. Commit liberally.
5. Verify on the matching surface. "Inconclusive" or wrong-surface is not a pass. Flag it.
6. Organize authorized commits into small, ordered units. Stack follow-ups when appropriate.
   Use the [sequence verifiable units](../references/principles/sequence-verifiable-units.md) principle, building, verifying, and committing each small unit before the next.
7. If the design is contested, [Independent review](../references/agent-workflows.md#independent-review) before shipping.
8. Run [Opening a PR](opening-a-pr.md).

Code-coupled work (one feature, one migration) goes to a single owner with the checkpoint inline. That owner fans out internally after the blocking phase. Parent-level fan-out is for slices that produce independent artifacts (audits, cross-subsystem investigations, competing experiments). Rewrite the checkpoint at phase boundaries. Spawn a fresh owner rather than chaining interrupts.

**Reply:** what you built, what you chose and why, the throughput checkpoint, open decisions. Tables for design alternatives.
