# Opening a PR

Use at the delivery step when creating or updating a PR is in scope.

1. Inspect the current checkout, base, branch, and unrelated changes. Continue an existing PR on its branch. Isolate competing writes before modifying shared state.
2. Review the final diff for unintended scope, redundant abstractions, and comments that merely narrate code. Preserve useful explanations of non-obvious constraints.
3. Run the required repository checks and the affected behavioral proof. Record actual results and any limits.
4. Organize commits into coherent verifiable units. Stage only the intended files. Follow the repository's history conventions rather than rewriting shared history as a cleanup habit.
5. Write the title and body around the final problem and resulting behavior. Include consequential tradeoffs and the evidence a reviewer needs. Keep detailed experiment logs in linked artifacts.
6. Use the available forge integration or authenticated CLI. For a stack, target the immediate parent branch; independent changes target the repository base. Preserve a requested draft or review state.
7. Register every created PR with T3's `link_pull_request` when running inside T3, or the current host's attachment tool. Verify the returned URL and status.
8. Return the PR and verification outcome. Start [Babysit](babysit.md) only when ongoing monitoring was requested.

A worker reports its revision, evidence, and any PR to the coordinator. The parent owns integration and watches.
