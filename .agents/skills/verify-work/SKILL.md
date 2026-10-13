---
name: verify-work
description: Verify a behavior or claim with direct evidence from the real artifact. Use when asked to prove a fix works, check a user flow, or compare behavior or performance before and after a change.
license: MIT
---

# Verify work

## Gather evidence

1. State a falsifiable claim, its preconditions, and the expected result or threshold. Derive the acceptance condition from the request or documented contract, independently of the implementation under test.
2. Exercise the smallest consumer surface that can disprove the claim: a UI action, CLI command, public API, or library call. Reuse the project's verification harness. A passing build alone cannot establish that a user flow works.
3. Confirm the instance's build, readiness, test data, and required authentication. Use an isolated port, profile, and data directory where applicable.
4. For a fix or improvement claim, capture before and after evidence with comparable commands, data, workload, warmup, and environment. Preserve the original failure or old version. For an absolute behavior claim, test its acceptance condition directly.
5. Capture the action and resulting state, including consequential side effects. For persistence, read back the value through the normal interface after a reload or restart. Re-run affected observations if the artifact changes after measurement.
6. After a surprising or failed run, recheck instance health and reset owned state before retrying. Clean up only processes and scratch state created for the run. Keep minimal, redacted evidence outside disposable state and confirm it survives cleanup.

## Verdict

- **VERIFIED.** Direct evidence meets the stated condition. An improvement claim also has comparable before and after measurements meeting the threshold.
- **NOT VERIFIED.** A valid observation disproves the claim or misses its threshold. Keep the original acceptance condition when reporting the failure.
- **INCONCLUSIVE.** A required baseline, precondition, or observation is unavailable, or a confounding difference prevents comparison. State what is missing.

Report the verdict, claim, commands or user actions, expected and observed results, and evidence paths. Include any uncovered surface or limit on the conclusion.
