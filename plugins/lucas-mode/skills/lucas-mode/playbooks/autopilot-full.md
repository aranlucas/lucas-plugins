# Autopilot full

Use for a queue of independent changes with one owner per deliverable. The coordinator owns verification and reconciliation. Each owner carries its assigned change through implementation and correction.

1. Record the queue, acceptance condition for each item, shared constraints, and delivery authority. Respect items reserved for the user and any plan-then-wait instruction.
2. Follow [T3 orchestration](../references/t3-orchestration.md). Dispatch one owner per independent change with exclusive writes, complete context, verification method, and reporting milestones. Use [Orchestrate](orchestrate.md) for the rolling queue and durable ledger.
3. Owners return a code-ready revision and evidence. The parent dispatches independent reviewers or test workers against that revision. Reviewers report to the parent; they do not approve their own implementation.
4. Reconcile every finding with the actual goal. Send supported issues to a fresh fix task with consolidated context, then start a new review round at the corrected revision.
5. Prepare PRs through [Opening a PR](opening-a-pr.md) when in scope. For requested monitoring, the parent owns [Babysit](babysit.md) and T3 PR watches; child owners return rather than polling indefinitely.
6. When merge authority is explicit, the designated integration owner follows [Shipping](shipping.md). Otherwise stop each item at its requested delivery state. Green checks alone are not a merge verdict.
7. Refill capacity as independent units finish. Before replacing a stuck writer, inspect its status, cancel it, and confirm it stopped. Reconcile late results against the current revision.
8. Close after all children and requested deliverables are accounted for, including failures and deferred items.

Report the queue with owner, revision, review verdict, verification evidence, and delivery state. Keep decision trails for long runs and surface only changes that affect the user's next decision.
