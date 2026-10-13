---
name: project-verification
description: Create or maintain a repository-local verification skill and feature map. Use when asked to build a reusable verification workflow for a project or audit an existing one against source and running behavior.
license: MIT
---

# Project verification

Choose **create** for a new workflow or **maintain** for an existing one. Inspect repository instructions, skills, runtime configuration, and harnesses. Preserve the project's skill discovery convention; for a new Codex project skill, use `.agents/skills/verify-<app>/SKILL.md`. Consult the [T3 discovery reference](../lucas-mode/references/t3.md) only when configuring or troubleshooting provider discovery.

## Create

Identify the consumer surface, launch command, readiness condition, prerequisites, driver, observable state, and isolation limits from source and a running instance. Reuse the project's harness and commands. If the app cannot start, record the blocker and mark untested instructions as draft.

Write a skill with `name` and `description` frontmatter and the following operational details:

- **Launch.** Exact commands, nonsecret configuration, migrations or seeds, and readiness checks. Use fresh isolated sessions for short-lived CLIs and one owned instance for serial server or UI interactions.
- **Doctor.** Read-only checks of the build, usable interface, port/profile, and authentication before driving and after surprising results.
- **Drive.** Consumer routes, commands, selectors, or public APIs and their consequential side effects. Avoid internal setters or test-only endpoints that bypass the behavior being verified.
- **Evidence.** Capture actions and literal expected results in a location outside disposable app state. Record what mocks and dry runs leave untested.
- **Cleanup.** Identify and remove only processes and scratch state created by the run; preserve evidence. Avoid process-name kills and shared-profile deletion.

Add `features/README.md` as an index linking to feature recipes. Each recipe records the user goal, source entry point, prerequisites, route, actions, expected observable result, and relevant pitfalls. Include alternate entry points when they change the journey. Add helpers only for repeatable operations, document their invocation, and run them to validate their behavior.

Follow the generated instructions end to end: launch, doctor, drive a mapped feature, capture evidence, and clean up. Correct harness failures and repeat the affected steps. Check that evidence survives cleanup and identify recipes or targets that remain untested.

## Maintain

Locate the existing skill and feature map. Clarify the target if several fit; if none exists, report the missing workflow.

Read each mapped feature's source, reconcile the index, and identify missing entry points. Group recipes that can share app state without dropping coverage or contaminating later observations.

Run launch and doctor, then exercise every mapped feature. Record source entry points, attempted routes, observed results, evidence, and blockers. For unreachable journeys, name the attempted route and missing prerequisite.

Classify findings before editing:

- **Documentation drift.** The map incorrectly describes working behavior. Correct it from source and observation.
- **Harness gap.** The app works but the driver cannot prove it. Fix the owned harness and re-drive it.
- **Product regression.** The requested or documented behavior is broken. Report the evidence and preserve the expected journey. Keep maintenance edits scoped to the skill and its harness unless product fixes were also requested.

Clean up owned state after failed iterations and the final drive, preserving accumulated evidence. If a doctor failure comes from skill drift, correct it and retry once before reporting the blocker.

Report **clean**, **changed**, or **blocked**, with source and live coverage stated separately. Include evidence from corrected instructions and list any remaining untested journeys.
