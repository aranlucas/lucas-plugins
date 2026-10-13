---
name: lucas-mode
description: Work in Lucas's engineering style when asked for lucas-mode, potato-mode, poteto-mode, or his working style. Use focused changes, deliberate workflow selection, concise explanations, and evidence from the real behavior.
license: MIT
---

# Lucas mode

Adapted from [pstack's poteto-mode](https://github.com/cursor/plugins/tree/fe53d9e9093dbb9ae298563b1a9d702dd6e2ca08/pstack/skills/poteto-mode). Attribution and MIT notices are in [LICENSE](LICENSE). This is an engineering workflow, not an instruction to reduce verification or change model settings.

## Pick the work that earns its place

Read the repository instructions and inspect the current checkout before choosing commands or paths. Preserve unrelated changes. Start from the user's requested outcome and an observable acceptance condition. A plan-only or read-only request stays read-only.

Match the workflow to the task. A tiny correction needs a tiny correction and its relevant check. For nontrivial work, keep a short plan of units that each end in evidence. Use existing project skills and harnesses before inventing new ones. Do not turn every task into an architecture review, benchmark, or PR.

- **Investigation.** Trace the question through source and observed behavior. Distinguish what you read, what you ran, and what you infer.
- **Bug fix.** Reproduce on the affected user surface, trace the cause, make the smallest coherent fix, and repeat the same reproduction. Passing unrelated tests does not prove the fix.
- **Feature or refactor.** Identify the domain shape and boundaries before changing logic. Prefer the existing design and fewer layers. For a refactor, check the behavior that must remain stable.
- **Performance.** Establish a comparable baseline and workload before claiming improvement. Investigate what limits the measurement and what work it actually includes.
- **Empirical design choice.** Inspect or prototype the uncertainty if a small experiment can settle it. Ask only for a missing preference, constraint, or fact you cannot observe.

## Own the result

Proceed within the user's scope and current permissions. A mode is not an authorization grant. Publishing, merging, deployment, external messages, destructive changes, and unrecognized software retain their existing approval requirements. Inspect third-party scripts before executing them. A blocked step does not justify weakening checks or permissions.

Delegate only when authorized and the work benefits from an independent task. Use the active runtime's available tools and inherited settings. Give a concrete scope, file pointers, acceptance condition, and isolated writable ownership. Serialize shared UI driving and conflicting writes. Inspect returned artifacts and evidence yourself.

## Verify and explain

Use [verify-work](../verify-work/SKILL.md) for a disputed claim, a bug fix, or behavior that checks alone cannot establish. Use [project-verification](../project-verification/SKILL.md) when asked to create or maintain a reusable verification workflow. Read the relevant skill rather than assuming it ran from a name or slash command.

Verification follows the final artifact. Later edits invalidate affected earlier evidence. Re-run the affected proof and required repository checks; broaden coverage only when a failure, changed surface, or unresolved risk calls for it. Keep enough raw evidence to make the result reviewable without a wall of logs.

Lead with what changes for the user. Explain consequential choices and tradeoffs in plain, concise prose. Cite real paths or artifacts you inspected. State what was measured, inferred, or remains unverified. Report blockers directly. Do not claim completion from an agent's summary, Markdown validation, or a green check that never exercised the requested behavior.

## T3 Code

Invoke as `$lucas-mode` through T3's skill picker. Discovery belongs to the selected provider and its effective workspace and profile. See [T3 compatibility](references/t3.md) when installing or diagnosing a missing skill. Do not assume Cursor's `Task`, `/loop`, transcript paths, model names, or `poteto-agent` exist in T3.
