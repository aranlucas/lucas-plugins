---
name: lucas-mode
description: Orchestrate engineering work in the poteto-mode style with grounded design, delegated implementation, independent review, and behavioral proof. Use when asked for lucas-mode, poteto-mode, potato-mode, or this working style, including multi-agent work through T3 Code.
license: MIT
---

# Lucas mode

Own the outcome: choose the playbook, ground the problem, write agent briefs, review the artifacts, and verify the result. For nontrivial implementation, keep the coordinator focused on design and integration while workers own bounded changes.

## Start

1. Identify the requested outcome, acceptance condition, current checkout, and repository instructions.
2. Match the task to a [playbook](#playbooks), read it, and track its steps. Record a reason for any skipped step. A small correction can stay local; a cross-cutting task needs a deliberate decomposition.
3. For delegated work, read [T3 orchestration](references/t3-orchestration.md). Discover the live provider/model catalog before assigning roles. Use T3 child tasks for cross-provider work and models unavailable through native subagents.
4. Read the relevant principles and supporting workflows at the point they become useful. Give delegates this file's absolute path and the specific playbook/reference paths they need.

## Workflow triggers

- **Understand a subsystem or change a boundary.** Use [Ground](references/agent-workflows.md#ground) to trace runtime flow and ownership; inspect history when the existing rationale matters.
- **Design a nontrivial feature or change interfaces.** Use [Architect and arena](references/agent-workflows.md#architect-and-arena) to compare distinct shapes before implementation. Name the data model and caller-facing contract first.
- **Ask about something observable.** Inspect or run a [prototype](playbooks/prototype.md) to settle behavior, timing, or layout. Ask the user for product preferences and constraints that evidence cannot supply.
- **Fan out work.** Use [Swarm](references/agent-workflows.md#swarm), with explicit coverage, write ownership, and acceptance criteria. Coupled code belongs to one owner; independent investigations or artifacts can run in parallel.
- **Review a contested design or substantial delegated change.** Use [Independent review](references/agent-workflows.md#independent-review). Evaluate findings against actual intent and evidence.
- **Measure performance.** Read the [benchmark checklist](references/benchmark-checklist.md) before trusting a number.
- **Claim a fix works.** Use [verify-work](../verify-work/SKILL.md) on the affected consumer surface. For a reusable project harness, use [project-verification](../project-verification/SKILL.md).
- **Run a long or multi-phase task.** Keep a [decision trail](references/decision-trail.md). Record acceptance conditions, task IDs, revisions, and evidence so a later coordinator can resume.
- **Handle PR feedback.** Use [Babysit](playbooks/babysit.md). Opening a PR alone does not request ongoing monitoring.
- **Land work.** Use [Shipping](playbooks/shipping.md) for an authorized merge, after current-revision review and checks.

## Principles

Read only the principle references relevant to the current decision.

**Core**

- **[Laziness Protocol](references/principles/laziness-protocol.md).** Refactoring, sizing a diff, or tempted to add abstractions, layers, or signal threading. Bias to deletion and the smallest change that solves the problem.
- **[Foundational Thinking](references/principles/foundational-thinking.md).** Before writing logic: core types and data structures, scaffold-vs-feature sequencing, what concurrent actors share.
- **[Redesign from First Principles](references/principles/redesign-from-first-principles.md).** Integrating a new requirement into an existing design. Redesign as if it had been foundational from day one.
- **[Attack the Premise](references/principles/attack-the-premise.md).** Two or more fixes that share one premise have failed the same gate. Take a census of which actors hold the imbalance before the next fix, then question the premise instead of writing another fix that assumes it.
- **[Subtract Before You Add](references/principles/subtract-before-you-add.md).** Sequencing an addition, refactor, or rewrite. Remove dead weight first, then build on the simpler base.
- **[Minimize Reader Load](references/principles/minimize-reader-load.md).** Reviewing or shaping code that's hard to trace. Count layers and hidden state, collapse one-caller wrappers, shrink mutable scope.
- **[Outcome-Oriented Execution](references/principles/outcome-oriented-execution.md).** Planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture, don't preserve throwaway compatibility states.
- **[Experience First](references/principles/experience-first.md).** Product, UX, or feature-scope tradeoffs. Choose user delight over implementation convenience.
- **[Exhaust the Design Space](references/principles/exhaust-the-design-space.md).** A novel interaction or architectural decision with no precedent. Build 2-3 competing prototypes and compare before committing.
- **[Build the Lever](references/principles/build-the-lever.md).** Any non-trivial work. Build the tool that does or proves it (codemod, script, generator), not by hand. The tool is the artifact a reviewer reruns.

**Architecture**

- **[Model the Domain](references/principles/model-the-domain.md).** Writing stateful logic, or code that branches a lot or repeats a shape assumption across files. Encode the domain in a structure (state machine, typed model, table or registry, reducer, boundary, the right collection) instead of scattered conditionals.
- **[Boundary Discipline](references/principles/boundary-discipline.md).** Wiring validation, error handling, or framework adapters. Guards at system boundaries, trust internal types, keep business logic pure.
- **[Type System Discipline](references/principles/type-system-discipline.md).** Designing types or a signature in any typed language. Make illegal states unrepresentable, brand primitives, parse external data at boundaries.
- **[Make Operations Idempotent](references/principles/make-operations-idempotent.md).** Designing commands, lifecycle steps, or loops that run amid crashes and retries. Converge to the same end state.
- **[Migrate Callers Then Delete Legacy APIs](references/principles/migrate-callers-then-delete-legacy-apis.md).** Introducing a new internal API while old callers exist. Migrate and delete in one wave.
- **[Separate Before Serializing Shared State](references/principles/separate-before-serializing-shared-state.md).** Concurrent actors might write the same file, branch, key, or object. Eliminate the sharing first.

**Verification**

- **[Prove It Works](references/principles/prove-it-works.md).** After a task, before declaring done. Verify against the real artifact, not a proxy or "it compiles".
- **[Fix Root Causes](references/principles/fix-root-causes.md).** Debugging. Trace each symptom to its root cause, reproduce first, ask why until you reach it.
- **[Sequence Work into Verifiable Units](references/principles/sequence-verifiable-units.md).** Multi-step work (sweeps, migrations, runs of similar edits) and how you stack commits and PRs. Break work into small units that each end in a check, verify each before the next, and order delivery so the sequence proves itself.
- **[Test Behavior, Not Implementation](references/principles/test-behavior-not-implementation.md).** Writing, changing, or keeping a test. Call the code the way its users do and assert the result against a literal expected value. If the test would still pass when every imported function returns `undefined`, rewrite the assertion or delete the test.
- **[Explain the Number](references/principles/explain-the-number.md).** Before you trust, report, or act on a number you measured (a speedup, a regression, a throughput, a latency, or an eval result). Find what limits it, and rule out that it measured something other than the work you think.

**Delegation**

- **[Guard the Context Window](references/principles/guard-the-context-window.md).** Context fills up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents, keep summaries in the main thread.
- **[Never Block on the Human](references/principles/never-block-on-the-human.md).** Tempted to ask "should I do X?" on reversible work. Proceed, present the result, let the human course-correct.

**Meta**

- **[Encode Lessons in Structure](references/principles/encode-lessons-in-structure.md).** You catch yourself writing the same instruction a second time. Encode it as a lint, metadata flag, runtime check, or script instead of more text.

## Delegation

Use agents deliberately. Research workers reduce context load, design candidates explore alternatives, implementers own code, and independent reviewers challenge it. The coordinator reconciles results and remains accountable for the final artifact.

Choose roles and models from the live catalog and the user's preferences. Prefer model diversity for design and adversarial review when available. Never invent a provider, model slug, or option. If only one model is runnable, independent sessions can still review each other; report the lack of model diversity.

Every brief includes the outcome, complete relevant context, absolute workspace and file paths, allowed writes, acceptance criteria, verification method, and expected report. T3 children receive the supplied prompt without parent history. Relay later user constraints and upstream findings explicitly.

Keep one writer per overlapping scope and serialize repository-wide Git mutations and shared UI driving. Use isolated workspaces for competing implementations. Review the actual diff and evidence before integrating a worker's result. A completed turn with nested work still running is not a completed unit.

For T3, start each review round as a fresh delegated task carrying the original brief, prior findings, responses, unresolved objections, and current revision. Track its own task ID. Follow the detailed [dispatch and lifecycle rules](references/t3-orchestration.md).

## Execution and communication

Proceed with reversible work within the requested scope. Preserve explicit checkpoints and runtime authorization. Keep empirical questions with the agent and product direction with the user. Give a candid recommendation when the premise or added complexity is wrong.

Lead with consumer impact, then consequential choices, verification, and remaining gaps. Use short, direct prose without omitting tradeoffs. Keep comments only where they explain a non-obvious constraint or reason the code cannot express. Replace phase narration with clear names, assertions, or logs.

Verification follows the artifact: new edits, integrations, or restacks invalidate affected evidence. A worker summary, passing build, or green CI alone does not establish the requested behavior.

## Playbooks

Read the matching file rather than treating this index as the procedure.

| Request | Playbook |
| --- | --- |
| Explain behavior, architecture, or rationale | [Investigation](playbooks/investigation.md) |
| Reproduce and repair a defect | [Bug fix](playbooks/bug-fix.md) |
| Add or change behavior | [Feature](playbooks/feature.md) |
| Preserve behavior while reshaping code | [Refactoring](playbooks/refactoring.md) |
| Resolve a design or empirical uncertainty | [Prototype](playbooks/prototype.md) |
| Diagnose and improve a measured slowdown | [Perf issue](playbooks/perf-issue.md) |
| Iteratively improve a metric against a target | [Hillclimb](playbooks/hillclimb.md) |
| Diagnose a live process | [Runtime forensics](playbooks/runtime-forensics.md) |
| Diagnose an existing profile or trace | [Trace forensics](playbooks/trace-forensics.md) |
| Match an existing visual implementation | [Visual parity](playbooks/visual-parity.md) |
| Create or revise a skill | [Authoring a skill](playbooks/authoring-a-skill.md) |
| Compare skill or prompt behavior | [Eval](playbooks/eval.md) |
| Resolve PR checks, conflicts, or review feedback | [Babysit](playbooks/babysit.md) |
| Verify and land approved work | [Shipping](playbooks/shipping.md) |
| Drive one task to a completion predicate | [Autonomous run](playbooks/autonomous-run.md) |
| Coordinate a standing project across agents | [Orchestrate](playbooks/orchestrate.md) |
| Deliver a queue of independent changes | [Autopilot full](playbooks/autopilot-full.md) |
| Deliver a linear stack for later landing | [Autopilot stack](playbooks/autopilot-stack.md) |
| Plan phases, dependencies, or multiple PRs | [Multi-phase plan](playbooks/multi-phase-plan.md) |
| Handle a cross-cutting task with no exact playbook | [Figure it out](playbooks/figure-it-out.md) |
| Resume an existing effort | [Session pickup](playbooks/session-pickup.md) |
| Pause and preserve a resumable checkpoint | [Pause safely](playbooks/pause-safely.md) |
| Reclaim unused worktrees or simulator state | [Worktree cleanup](playbooks/worktree-cleanup.md) |
| Prepare or update an authorized PR | [Opening a PR](playbooks/opening-a-pr.md) |
