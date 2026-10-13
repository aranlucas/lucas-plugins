# Autopilot stack

Build a queue as one linear base-branch chain for the user to review and land.

1. Frame the sequence and dependencies. Use [Autopilot full](autopilot-full.md) for owner briefs, implementation, and independent review, with stack delivery as the acceptance condition.
2. Assign one topology owner. Workers write only their assigned scopes or isolated branches; they report head revision and intended parent. They do not retarget, rebase, or merge the shared chain.
3. Integrate only a verified unit. The root targets the repository base; each child targets its parent branch and is based on the recorded parent revision.
4. Parallelize research, tests on stable snapshots, and independent artifacts. Serialize changes that depend on the same unfinished API or branch state.
5. When the base moves, the topology owner coordinates the update from bottom to top. Assign conflicts to the owner of the affected code. Preserve unrelated work and repository history rules.
6. Re-run affected proof and review after restacks or edits. Keep receipts tied to current revisions; do not carry a verdict forward merely because the PR number is unchanged.
7. Deliver the ordered chain and its evidence. This workflow ends at delivery; it does not arm auto-merge or land descendants.

Report root and tip, dependency order, one verdict per current head, and any blocked or excluded unit. If the user later asks to land the chain, use [Shipping](shipping.md).
