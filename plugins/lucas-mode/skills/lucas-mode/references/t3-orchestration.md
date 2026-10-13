# T3 orchestration

Use this reference whenever a playbook delegates work. Tool names below are T3 MCP operations; discover the installed namespace and read its current schema before calling.

## Choose the execution path

Call `orchestrator_capabilities`. Check `parentThreadId`, inherited provider/model, runtime and interaction modes, provider constraints, `canRunChildTask`, `canRunCrossProviderChildTask`, and the available model options.

- A non-null parent thread and runnable provider are prerequisites for T3-owned child tasks. A tool being visible in another host does not supply a T3 parent.
- Prefer native subagents for same-provider work only when the native tool supports the selected model. Use `delegate_task` for cross-provider work, a model absent from the native tool, or explicitly T3-owned children.
- Use provider instance IDs, model IDs, and option IDs from the live catalog. Respect role preferences already supplied by the user; otherwise inherit for ordinary implementation and select available diversity for design/review. Preserve permission modes.
- `create_threads` and `t3_thread_launch` create ordinary top-level chats. They are not substitutes for child delegation; use them only for a user-requested separate chat.
- Outside T3, use the host's native delegation when available. Keep the same brief and review contracts. Report unavailable T3 execution or model diversity rather than claiming it ran.

## Roles and ownership

| Role | Responsibility | Expected artifact |
| --- | --- | --- |
| Coordinator | Frame, decompose, dispatch, reconcile, integrate | Plan, task ledger, final verified result |
| Research | Read a bounded subsystem or evidence set | Cited flow, constraints, uncertainties |
| Design | Explore one complete alternative | Caller usage, types, boundaries, tradeoffs |
| Implementation | Change an assigned scope | Diff, revision, checks, deviations |
| Review | Challenge a specific artifact independently | Evidenced findings and verdict |
| Test | Drive the consumer surface or measurement | Method, observations, raw evidence |

One writer owns each overlapping file set. Children must not concurrently stage, commit, reset, rebase, or switch branches in a shared checkout. Allocate real isolated worktrees for competing implementations when the host supports them; record their paths in the briefs. A delegation call does not create isolation by itself. Serialize shared UI sessions, profiles, ports, and integration. Read-only review can run concurrently against a stable snapshot.

## Write a complete brief

T3 `delegate_task` supplies only the task prompt, without parent conversation history. Include:

```text
GOAL: Observable outcome.
CONTEXT: User request, later constraints, source paths, relevant prior findings.
WORKSPACE: Absolute checkout path and base/head revisions.
READ: Absolute Lucas Mode path and relevant playbook/reference paths.
SCOPE: Allowed writes, forbidden paths, branch/worktree owner.
ACCEPTANCE: Conditions that must hold.
VERIFY: Commands or consumer actions; prerequisites and known limits.
REPORT: PASS, ISSUES, or BLOCKED; revision; files; actions run;
        evidence paths; deviations; unresolved questions.
```

Collapse the template for small tasks while retaining its substance. Inline any information the child cannot read from the selected environment. Confirm path accessibility before assigning writes. A reviewer receives the intent and actual artifact, not an instruction to endorse the author's conclusion.

## Dispatch and receive

1. Call `delegate_task` with a concrete `role`, `title`, full `task`, and `mode: "async"`. Set `target.providerInstanceId`, `target.model`, and `target.options` only to catalog values when overriding inheritance.
2. Use a unique `clientRequestId` per logical task or review round. Reuse it for transport retries of that same request so an uncertain response does not create duplicate workers.
3. Record the returned `taskId`, `childThreadId`, provider/model, scope, and revision. The task ID owns the delegated lifecycle; the child thread is backing storage.
4. Continue independent work. Async completion wakes the parent. If nothing independent remains, end the turn with work recorded as pending and resume on notification. Do not spawn watchers or repeatedly poll.
5. Use `task_status` when a result is needed mid-turn. Inspect `workState`: `waiting_for_children` is still pending; consume `result_available`. A terminal status may still have later `hasPendingChildRuns`.
6. Read the result and inspect its actual artifacts. A terminal result read acknowledges automatic delivery. For missing detail, use `t3_thread_read` on the returned child thread with pagination; recover truncated text before judging it.
7. Record the accepted result, gaps, or required next round. Failed or cancelled tasks do not count as coverage.

If using `mode: "wait"`, its timeout is only the parent's wait budget. `waitTimedOut: true` does not cancel the child: retain the task ID and consult status later. Avoid waiting synchronously when independent work exists.

## Review rounds and corrections

Each T3 review round is a new `delegate_task` call. Include the original brief, current revision, prior findings, responses, and unresolved objections. Assign a fresh request ID and task ID. Do not send a new review round to the old `childThreadId` through `t3_thread_send`; thread messages do not reopen a completed delegated task.

Preserve independent judgments. Prefer a different model/provider for review where runnable. Multiple fresh reviewers on one model are independent sessions, not cross-model evidence. The coordinator verifies findings, groups duplicates, and classifies each as act, consider, or dismiss with reasons.

If a required independent reviewer cannot run, keep the review gate pending and continue unrelated work. A self-review or CI result cannot be relabeled as that review. For optional exploration, a clearly labeled sequential pass is a useful fallback.

## Cancellation and recovery

Use `task_cancel` with the task ID to stop an obsolete or conflicting task. It also stops nested work and later runs in the backing child. Confirm the stop before transferring write ownership; `cancel_requested` alone is not proof the writer has stopped. Published terminal results remain readable.

After interruption, reconcile the task ledger with current task status, branches, revisions, and on-disk artifacts before retrying. On an unknown dispatch outcome, retry the same request ID. On a new attempt after failure, use a new ID and a consolidated brief. Narrow repeated failures; after two unsuccessful retries, record the blocker and replan rather than creating an endless fan-out.

## PR events

For user-requested ongoing PR monitoring, the parent calls `watch_pull_request` after handling existing feedback. T3 wakes it for meaningful changes; subagents do not own watches. Stop with `unwatch_pull_request` when handing the work back. A wake is input for a readiness check, not permission to merge.

Skill discovery and installation are separate from orchestration; consult [T3 discovery](t3.md) only when a skill cannot be found.
