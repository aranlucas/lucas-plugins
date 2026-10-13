# Agent workflows

Use [T3 orchestration](t3-orchestration.md) for every dispatch, model selection, complete brief, and result lifecycle.

## Ground

For a narrow question, assign one read-only researcher or inspect it directly when delegation would add no useful separation. For a subsystem, partition two to four independent angles: entry points, state ownership, external boundaries, and tests are common cuts.

Each researcher traces concrete calls and data flow, cites files and symbols, and distinguishes observed behavior from inferred intent. For rationale, inspect history, issues, or design notes before treating the present structure as deliberate.

Synthesize a working model: what enters, who owns state, where decisions live, what leaves, and what can fail. Resolve contradictions from source. Use this artifact as shared grounding for designers and implementers.

## Architect and arena

1. Ground the affected systems. Write caller usage first, then the types, signatures, module boundaries, and invariants it requires.
2. Derive a small rubric from the task: correctness, integration fit, reader load, and verification cost. For a consequential design, assign at least two structurally distinct candidates with the same brief and separate output paths. Prefer available model diversity.
3. Wait until candidates finish writing. Have a separate read-only judge compare them by neutral path labels against the rubric. The coordinator reads every candidate too.
4. Pick a coherent base. Resolve disagreements by examining evidence and assumptions, not vote counts. Port worthwhile ideas from other candidates deliberately; do not average incompatible designs.
5. Delegate implementation against the selected contract. A new parameter, shared state, or type escape hatch is evidence to revisit the design. Record justified deviations.
6. When the same workaround recurs across independent sites, re-ground and redesign instead of accumulating exceptions. Return to distinct candidates if the contract was wrong.
7. Verify the integrated artifact, including any grafted pieces. Report the alternatives, base choice, rejected ideas, and evidence.

Use scratch type sketches for design-only tasks. Honor a requested checkpoint before implementation. Mechanical edits with a settled shape do not need an arena.

## Swarm

Choose the shape before dispatch: partitioned coverage, a race on the same brief, or a mixture. State the completion predicate and selection rule (first valid result, rank all, or synthesize the best). Record the required slices and concurrency budget.

Give every worker an independent scope or output, exact revisions, and the measurement method when applicable. Keep shared mutations serialized. Dispatch within the host's capacity; refill available slots as independent results arrive.

Accept only results tied to the requested artifacts and method. A missing slice is a coverage gap. Retry a malformed result once with the missing contract clarified; after another miss, report the gap. In a race, stop losing writers before taking ownership of their artifacts.

Return one consolidated result with coverage, evidenced issues, dropouts, and the declared selection rule. A deterministic transformation is preferable to many workers repeating mechanical edits.

## Independent review

Frame the intent and the exact revision or stable diff. Give reviewers the same intent, surrounding context, acceptance conditions, and relevant evidence. Reviewers do not edit the artifact they judge.

For substantive delegated work, obtain an independent review; use multiple models for contested or high-impact decisions when available. Each reviewer reports a reproducible failure or concrete reasoning, file pointers, impact, and remaining uncertainty. Style preferences without a task-relevant consequence are not defects.

Read findings yourself. Group duplicates and classify them:

- **Act.** Supported correctness, security, or maintenance issue that affects the requested outcome.
- **Consider.** A real tradeoff whose benefit may not justify changing this work.
- **Dismiss.** Incorrect, already handled, or outside the task, with the evidence explaining why.

One well-proved finding outweighs unsupported agreement. After a fix, start a fresh review round with the prior objections and new revision through the T3 lifecycle. Re-run affected proof. Keep a required review pending when no reviewer can run; continue work that does not depend on it.
