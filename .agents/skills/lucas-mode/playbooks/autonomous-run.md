# Autonomous run

Drive one task to a checkable exit condition. A standing multi-track program uses [Orchestrate](orchestrate.md).

1. Record the predicate, authorized scope, and any budget or explicit checkpoint.
2. Choose the matching implementation or investigation playbook. Delegate bounded independent work through [T3 orchestration](../references/t3-orchestration.md).
3. Each iteration changes one justified thing, checks the predicate on the real artifact, and keeps or discards the change based on evidence.
4. Keep a [decision trail](../references/decision-trail.md) with the hypothesis, result, and next action. Pivot when a premise repeatedly fails; do not keep stacking unmeasured fixes.
5. Use T3 child-completion notifications and, for requested PR monitoring, parent-owned PR watches. When only external work remains, yield and resume on its event. Do not invent Cursor loop commands or create polling agents.
6. Handle blockers within scope. Record unrelated discoveries without expanding the run. Report a required user decision or a concrete environment limit while progressing independent work.
7. Stop when the predicate is met, the user stops the run, or a genuine blocker prevents progress. Never relax the acceptance condition to declare success.

Report the exit condition, accepted and discarded attempts, verified result, and any remaining gap.
