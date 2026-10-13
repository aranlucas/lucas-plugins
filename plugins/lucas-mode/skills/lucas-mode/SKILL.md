---
name: lucas-mode
description: Apply Lucas's engineering workflow when asked for lucas-mode, potato-mode, poteto-mode, or his working style. Make focused changes and verify the affected behavior.
license: MIT
---

# Lucas mode

Start from the requested outcome and define an observable acceptance condition. Inspect the relevant source, repository instructions, and existing checks before choosing an approach.

## Choose the workflow

Keep small corrections focused. For nontrivial work, split the task into units with observable results. Reuse project skills and harnesses when they cover the task.

- **Investigation.** Trace the question through source and observed behavior. Separate observations from inferences.
- **Bug fix.** Reproduce on the affected user surface, trace the cause, make the smallest coherent fix, and repeat the reproduction.
- **Feature or refactor.** Identify the domain boundaries and behavior that must remain stable. Extend the existing design before adding layers.
- **Performance.** Record a baseline and repeat the same workload after the change. Check what the measurement includes and what limits it.
- **Design uncertainty.** Use a small inspection or prototype to settle questions that can be observed. Ask for preferences or constraints that affect the choice.

## Verify the result

Use [verify-work](../verify-work/SKILL.md) when a fix, disputed claim, or user flow needs direct behavioral evidence. Use [project-verification](../project-verification/SKILL.md) when asked to create or maintain a reusable verification workflow.

Run the affected proof and required repository checks against the final artifact. Re-run affected checks after later edits; broaden coverage when a failure, changed surface, or unresolved risk calls for it.

## Report the outcome

Lead with what changed for the user, then explain consequential choices and verification results. Link the relevant files or evidence and state any blocker or unverified behavior.
