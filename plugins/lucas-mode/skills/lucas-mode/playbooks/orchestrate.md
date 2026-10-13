# Orchestrate

Use for a standing project that outlives one agent: multiple workstreams, dependent deliverables, and repeated implementation/review rounds. One task with an exit condition uses [Autonomous run](autonomous-run.md); an ambitious single run uses [Figure it out](figure-it-out.md).

The coordinator owns briefs, dependencies, integration, and judgments. Workers own changes. Add a sub-coordinator only when a track has enough independent work to justify another coordination layer.

## Frame and record

1. State a countable completion predicate, scope, constraints, delivery shape, and any user-specified time or agent budget.
2. Ground the affected systems and settle consequential design choices with [agent workflows](../references/agent-workflows.md). Identify the blocking foundations before fan-out.
3. Read [T3 orchestration](../references/t3-orchestration.md), discover runnable providers/models, and choose roles. Do not equate the catalog's top-level batch limit with child-task capacity.
4. Create a task-specific coordinator directory with standing instructions, unit briefs, a task ledger, verification receipts, and a [decision trail](../references/decision-trail.md). One coordinator writes these records; workers publish separate artifacts.

A ledger row records unit ID, dependencies, task ID, owner, workspace, branch, base/head revisions, state, evidence, and next action. States distinguish ready, running, waiting on children, needs review, verified, integrated, and blocked. Preserve failed attempts with their reasons instead of silently overwriting them.

## Pilot and scale

Push one representative unit through brief, dispatch, implementation, independent review, behavioral proof, and integration before multiplying a novel workflow. Use the pilot to falsify the brief, environment, and verification method.

Then maintain a rolling window of ready units. Refill slots when results arrive; do not wait for the slowest member of a fixed batch before starting unrelated work. A shared API or data shape is a blocking dependency. One coupled change has one owner, who may delegate disjoint subparts if the runtime allows it.

Every brief carries the complete current constraints and relevant upstream findings. A dependency is a context relay, not just an ordering edge. Give each writer an exclusive workspace or file scope. Serialize Git and stack operations. Keep a shared browser, simulator, or other mutable driver under one owner.

## Reconcile completion events

Finish the current atomic action before processing a notification. At a safe boundary:

1. Match each event to its task ID, unit, expected revision, and current ownership.
2. Read the task result. A child waiting on nested work is pending. Record failures and missing evidence explicitly.
3. Inspect the actual output and queue independent review where needed. Large diffs become review tasks instead of consuming the coordinator's whole context.
4. Relay accepted findings into newly ready briefs. Dispatch fresh tasks for fix or review rounds, with consolidated context.
5. Update the ledger and completion counts from evidence. Continue useful work; when only async children remain, yield for T3's completion notifications.

## Verify and integrate

A receipt binds the unit's base/head revision to the method, observed result, evidence path, and reviewer. A worker's tests are useful evidence; they do not substitute for an independent review when the workflow requires one.

Use a separate verifier for judgment-heavy, behavioral, or high-impact work. A cheap deterministic check can be run by the worker and inspected by the coordinator without a second agent repeating one command.

Integrate verified units continuously. Keep one integration owner for each branch or stack. Resolve conflicts through a scoped implementation task, then verify the integrated result. New edits or changed bases require fresh affected proof. A verified descendant does not make an unverified dependency ready to land.

Keep the ordered PR list and revisions in the ledger. Use [Shipping](shipping.md) only for authorized landing; otherwise deliver verified changes or PRs for review. Let the parent own any T3 PR watch.

## Failures and recovery

Check liveness through task state and real artifacts, not transcript timestamps or an agent saying it is done. On a timeout, inspect the existing task before retrying. Before replacing a writer, cancel it and confirm it stopped.

For an environment failure, retry once when a concrete recovery is available. For excessive scope, narrow the unit. After two unsuccessful retries, record the blocker and replan around it. A late result must be reconciled against current revisions before acceptance.

On a user stop, stop new dispatch, cancel child work, and checkpoint. On resumption, read the standing instructions, ledger, task states, branches, and receipts before starting replacement work.

Close only when every task is accounted for, the requested artifact meets the predicate, and integration has been verified. Report completed units, remaining gaps, current revisions, review/verification limits, and the durable state path.
