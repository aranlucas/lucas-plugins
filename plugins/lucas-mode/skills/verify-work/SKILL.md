---
name: verify-work
description: Verify a specific behavior or claim with fresh evidence from the real artifact. Use for prove it works, did this fix it, before/after comparisons, or a UI, CLI, API, persistence, or performance claim that needs direct confirmation.
license: MIT
---

# Verify work

Adapted from pstack's [prove-it-works](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/principle-prove-it-works) and Cursor Team Kit's [verify-this](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/cursor-team-kit/skills/verify-this). Attribution and MIT notices are in [LICENSE](LICENSE).

1. State a falsifiable claim, its preconditions, and the observable result or threshold. Replace vague claims with a concrete condition from the request or source. Ask if the user's intent cannot be determined.
2. Choose the smallest surface that can disprove it. Use the app as its consumer does: a UI action, CLI command, public API, or library call. Follow repository instructions and existing verification harnesses. A green build alone does not establish a working Save flow or persisted data.
3. Check the instance before driving it. Confirm its build, readiness, ownership, data, and required auth. Use an isolated port, profile, and data directory where possible. Inspect third-party helpers before running them and retain required execution approvals.
4. For a change or improvement claim, capture baseline and treatment under comparable commands, data, workload, warmup, and environment. Keep the original failure or old version available without disturbing unrelated work. For an absolute behavior claim, directly test its acceptance condition; a before/after comparison is unnecessary.
5. Capture the action and resulting state. Check consequential side effects as well as what is visible. For persistence, read the written value or restart through the normal interface. Prefer a deterministic check when it earns its maintenance cost. Use literal expected results, not expectations derived from the implementation under test.
6. Compare raw evidence and return one verdict. If the artifact changed after measurement, re-run the affected proof before drawing a conclusion.
7. Clean up only processes and state this run owns. After a surprising or failed drive, doctor the instance again and reset owned state or relaunch before retrying. Retain evidence outside disposable state and confirm it survives cleanup. Report an auth, environment, or approval blocker instead of bypassing it.

## Verdict

- **VERIFIED.** Fresh direct evidence meets the stated condition. An improvement claim additionally has a valid baseline and treatment meeting the threshold without an unresolved confound.
- **NOT VERIFIED.** A valid observation disproves the claim or misses its threshold. Do not soften this verdict or weaken a journey to obtain a pass.
- **INCONCLUSIVE.** The required baseline, precondition, observation, or comparable environment is unavailable. State the precise limit; missing evidence is not a pass or proof of a product failure.

Report the verdict, claim, commands or user actions, expected and observed results, and evidence paths. Include any confound or uncovered surface. Keep output concise and normally spaced. Store only the evidence needed for the claim, without secrets, credentials, or unrelated user data. If disk capture would retain sensitive data, use redacted minimal evidence or obtain the appropriate consent.
