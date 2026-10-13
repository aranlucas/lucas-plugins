# Session pickup

Resume from recorded state without recreating completed work.

1. Read the prior task summary, standing instructions, ledger, and latest decision-trail entries. In T3 use the known thread ID with `t3_thread_read`; page backward or recover truncated items only as needed.
2. Reconcile the actual checkout, branch, revisions, outstanding diffs, child task IDs, and pending watches with that record.
3. Separate completed, pending, and invalidated work. Reuse evidence still tied to the current artifact; recheck claims whose inputs or revisions changed.
4. Do not assume an agent died because its parent restarted. Inspect existing task status before dispatching a replacement, and preserve exclusive write ownership.
5. Route remaining work to its playbook with the original request and all later constraints. A fresh delegated task needs that consolidated brief.

Report the inherited state, the resume point, and the next verified outcome. Keep unsupported inherited claims labeled until checked.
