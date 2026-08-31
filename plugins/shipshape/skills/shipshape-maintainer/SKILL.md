---
name: shipshape-maintainer
description: Read-only GitHub portfolio maintenance — rank repository work, inspect readiness, branch risk, delivery hygiene, and security posture. Use when the user wants to improve, publish, secure, or prioritize GitHub repositories.
---

# Shipshape Maintainer

Use the connected `shipshape` MCP to turn public GitHub evidence into a small,
ranked maintenance queue.

## Safety and scope

- Shipshape is read-only. Never imply that a tool changed a repository.
- It inspects public repositories only and never clones or executes repository
  code.
- Treat `unknown` as uncertainty, not as a passing result. Permission- or
  plan-gated GitHub signals commonly appear this way.
- Keep OAuth credentials and tool internals out of the user-facing response.

## Golden path

1. Start with `action_plan` for a specific repository when the user wants the
   next best fixes.
2. Use `repo_readiness` for publication, documentation, branch, delivery, and
   security evidence in one view.
3. Use `branch_risk` before proposing work on a named branch.
4. Use `delivery_hygiene` for CI, pinned Actions, dependency automation,
   releases, and recent activity.
5. Use `security_posture` when the user asks about exposure, CodeQL,
   Dependabot, secret scanning, or repository protection.
6. Use `portfolio_snapshot` to compare a bounded set of public repositories;
   deep scans are intentionally capped.

## Response format

Present a concise queue ordered by severity and recoverable value. For each
finding include its stable rule ID, state, confidence, evidence URL, and the
smallest practical remediation. Call out unavailable evidence separately from
confirmed failures, and avoid claiming a repository is safe when checks are
unknown.
