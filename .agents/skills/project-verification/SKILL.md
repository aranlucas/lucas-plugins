---
name: project-verification
description: Create or maintain a repository-local verification skill and feature map grounded in source and exercised against the real app. Use for make a verification skill for this repo or audit an existing verification workflow.
license: MIT
---

# Project verification

Adapted from pstack's [create-verification-skill](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/create-verification-skill) and [maintain-verification-skill](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/maintain-verification-skill). Attribution and MIT notices are in [LICENSE](LICENSE).

Choose **create** for a new project workflow or **maintain** for an existing one. Inspect repository instructions, skills, runtime configuration, and harnesses before writing anything. Preserve the project's established discovery convention. Prefer `.agents/skills/verify-<app>/SKILL.md` for a new Codex project skill; add a relative `.claude/skills/verify-<app>` link only when Claude/T3 support is needed and no conflicting entry exists. See the sibling [T3 compatibility reference](../lucas-mode/references/t3.md) for provider differences.

## Create

Interview the repo through source and executable evidence. Identify the consumer surface, launch command, readiness condition, prerequisites, driver, observable state, and isolation limits. Prefer the project's own harness and commands. If the base cannot start, report the exact blocker or fix it only within the task's authorized scope. Do not invent commands against an unproven base.

Write a skill with valid `name` and `description` frontmatter and these grounded sections:

- **Launch.** Exact commands, required nonsecret configuration, migrations or seeds, readiness that means usable, and owned shutdown. Short-lived CLIs run in fresh isolated sessions; servers usually use one owned instance driven serially.
- **Doctor.** A read-only check of the correct build, readiness, owned port/profile, and auth before the first drive and after any surprising result. If a healthy process hides a wedged UI, restore known state or relaunch.
- **Drive.** Real routes, commands, selectors, or public APIs. Use stable handles. Drive the consumer path, including consequential side effects. Do not substitute internal setters or test-only endpoints for the claim being proved.
- **Evidence.** Exact location outside disposable app state, actions to capture, literal expected results, and limits. Observe what a dry-run actually skips. Mocks can prove an isolated contract but cannot establish an unexercised live integration.
- **Cleanup.** Remove only instances and scratch state the run created. Never kill by process name or delete a shared profile. Confirm that proof artifacts survive successful and failed iterations.

Add `features/README.md` as an index and a small set of feature files grounded in real entry points. Each records the user goal, prerequisites, route, drive recipe, expected observable result, and gotchas. Map alternate entry points when they materially change the journey. Keep helpers only when they provide repeatable value; inspect them, document invocation, and execute them when permitted.

Follow the generated instructions once end to end: launch, doctor, drive a mapped feature, capture evidence, and clean up. Fix harness failures within scope and re-drive. Check retained evidence after cleanup. An unexecuted workflow remains a draft. Name any stand-in or untested target and the setup differences it hides.

## Maintain

Locate the existing skill and feature map. Ask which target if several genuinely fit; if none exists, report that and offer creation without silently expanding scope.

Limit edits to the verification skill and its owned harness. Read each mapped feature's source, reconcile the index, and look for concrete missing entry points. Independent source readers are useful only when authorized; the runtime driver remains one owner. Merge recipes into as few app states as practical without dropping coverage.

Run the skill's launch and doctor, then exercise every mapped feature. Keep coverage notes with source entry points, attempted routes, observed results, evidence, and blockers. An unreachable journey needs the attempted route and concrete missing prerequisite. An unavailable credential produces a coverage limit, not a pass.

Classify findings before editing:

- **Documentation drift.** The map incorrectly describes working behavior. Correct it from source and observation.
- **Harness gap.** The app works but the driver cannot prove it. Fix the owned harness and re-drive it.
- **Product regression.** The requested or documented behavior is broken. Report the evidence. Preserve the expected journey; do not redefine success to hide the failure or edit product code during maintenance.

Clean up owned state after every failed iteration and after the final drive. Keep and check accumulated evidence. If a doctor failure comes from skill drift, correct it and retry once before reporting the limit.

Report **clean**, **changed**, or **blocked**, with source and live coverage stated separately. A changed workflow needs evidence from the corrected instructions. Local changes are the deliverable unless the user authorized a PR; an authorized PR remains draft. This skill grants no permission to publish, merge, deploy, or schedule future maintenance.
