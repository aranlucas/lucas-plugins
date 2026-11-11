---
name: shipshape-maintainer
description: Read-only GitHub maintenance queue — rank the engineering practices tracked repositories fail, with stored check evidence and remediation guidance. Use when the user wants to know what to fix next across their GitHub repositories, or why a repository fails a practice.
---

# Shipshape Maintainer

Use the connected `shipshape` MCP to turn Shipshape's stored practice results into
a small, ranked maintenance queue.

## Safety and scope

- Shipshape's MCP tools are read-only. Never imply that a tool changed a
  repository, re-ran a check, or edited the practice catalog.
- Results cover the repositories Shipshape's GitHub App tracks, which can include
  private repositories. Only the configured owner can sign in. Keep private
  repository details in the conversation unless the user asks to share them.
- Results are stored evidence from earlier evaluations, not a live scan. Report
  each result's `checkedAt` time when recency matters.
- Treat `unknown` as uncertainty, not as a passing result. Permission- or
  plan-gated GitHub signals commonly appear this way.
- Keep OAuth credentials and tool internals out of the user-facing response.

## Golden path

1. Start with `maintenance_priorities` (optionally `owner`, and `limit` up to 50)
   when the user asks what to fix next. It ranks failing practices by how many
   active repositories fail them and lists unknown results separately; forks and
   archived repositories are excluded.
2. Use `repo_practices` with `owner` and `repo` for one tracked repository's
   results and checks.
3. Use `practice_detail` with a practice `id` for its definition, remediation
   instructions, and pass/fail counts.
4. Use `practices_overview` (optionally filtered by `owner` or `state`) for the
   full repository-by-practice matrix.

## Response format

Present a concise queue in the ranked order. For each action include the practice
id and title, the affected repositories, the failing checks as evidence, and the
smallest practical remediation from `practice_detail`. Mention how many
repositories were not yet checked (`unchecked`) and how many actions the limit
left out (`remaining`). List unknown results separately from confirmed failures,
and never call a repository compliant when checks are unknown.
