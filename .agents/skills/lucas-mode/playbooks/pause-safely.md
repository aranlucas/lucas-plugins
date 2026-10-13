# Pause safely

Use for an explicit pause or a necessary handoff. “Going to bed, keep going” remains an autonomous-run request.

1. Stop new dispatch. Finish the current atomic operation or leave a documented recoverable boundary.
2. Cancel owned child tasks through the host's lifecycle tools and confirm writers stopped. Stop parent-owned PR watches when the user is stopping monitoring.
3. Preserve work on disk. Record uncommitted changes or make a scoped checkpoint commit when appropriate to the repository and existing authorization. Do not reset or discard unrelated work.
4. Write a resume note with the goal, constraints, workspace, branch/revisions, task IDs, completed evidence, pending work, and first action on resumption. Link the existing ledger and trail instead of duplicating them.
5. Report exactly what remains live or could not be stopped.

A pause is not completion. Resume through [Session pickup](session-pickup.md).
