# Decision trail

For long, unattended, or multi-phase work, keep one append-only TSV per coordinator with these columns:

```text
ts	phase	decision	why	evidence	result
```

Record decisions and checkpoints, not every tool call: a design choice, completed unit, rejected hypothesis, revised brief, blocker, or verification result. Use concrete language. Evidence cells point to a revision, task ID, PR, source location, or retained artifact.

Keep cells single-line and escape tabs/newlines. Prefix spreadsheet formula-leading values when the trail will be opened in a spreadsheet. Each file has one writer; workers return evidence to the coordinator rather than concurrently appending.

Store the trail in a task-specific local working directory. Commit it when the deliverable needs an auditable history; otherwise keep it outside committed source. A replacement coordinator first records its identity and the prior run it inherits.

At checkpoints, reconcile rows with task results and actual artifacts. Supersede incorrect rows with a correction instead of erasing history. For substantial unattended work, have an independent reviewer inspect decisions, evidence gaps, and skipped verification.

The final report links the trail and explains what needs attention. The trail supplements the delivered artifact; it does not prove correctness by itself.
