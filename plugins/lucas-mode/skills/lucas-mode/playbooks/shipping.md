# Shipping

Land authorized work only after independent verification of the artifact being merged.

1. Identify merge authority, repository merge policy, current base/head revisions, and the ordered dependency chain. Preserve user-reserved checkpoints.
2. Assign independent verification for each substantive PR through [T3 orchestration](../references/t3-orchestration.md). The verifier did not implement the change and receives the exact base/head, intended behavior, and runnable proof method.
3. Record the verdict, method, evidence, and revisions. A blocked verifier or a green CI badge is not an independent passing verdict.
4. Land only the contiguous verified sequence from the bottom. A passing descendant above an unverified dependency remains pending.
5. Immediately before merging, reread current revisions, reviews, checks, and mergeability. If the artifact or its integration context changed, rerun the affected proof and review. Do not use old verdicts based solely on a matching PR number or commit message.
6. Have one owner prepare and merge the current bottom PR using the repository's normal method. Do not retarget or arm descendants in advance. Auto-merge is appropriate only when the user requested merge-when-ready and all non-CI gates are satisfied.
7. Confirm the forge reports the merge and inspect the resulting base before advancing to the next PR. Recompute the chain after each merge; automatic retargeting is not guaranteed.
8. If waiting in T3, use the parent's PR watch as an event source and reassess on wake. A readiness notification is not a merge result. Stop at the first unverified or blocked dependency.

Report what merged, the verifying agents and revisions, what remains pending, and the evidence needed to advance.
