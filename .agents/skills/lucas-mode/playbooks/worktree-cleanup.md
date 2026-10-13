# Worktree and simulator cleanup

Use only when cleanup is requested. Inventory actual state before removing anything.

1. List worktrees through Git or the host's managed-worktree tools and record disk usage. For each candidate, inspect branch, merge/PR state, uncommitted and untracked files, and active task ownership.
2. Cross-check live and pinned chats, child tasks, and running servers or simulators. A merged branch can still have an active worktree.
3. Classify each candidate as unused and recoverable, in use, or containing work that needs preservation. Do not infer that untracked files are disposable.
4. Use the host's archive operation for managed worktrees when available. Otherwise remove only confirmed unused worktrees through Git after preserving needed state. Avoid force-removal as the default.
5. For requested simulator cleanup, enumerate devices and runtimes, identify stale or unavailable instances, and preserve active sessions. Remove only the confirmed set.
6. Re-list and measure reclaimed space. Report what was removed and why other candidates were retained.

Read-only inventory can be partitioned among agents; removal has one owner.
