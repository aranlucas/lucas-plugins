# Plan 005: The hand-maintained Codex manifest cannot drift from the portable inputs

> **Executor instructions**: Follow the steps, run each verification, honor the
> STOP conditions, update `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 8b8f81e..HEAD -- scripts/sync.py tests/test_sync.py plugins/system-design-companion`

## Status

- **Priority**: P3
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: tests
- **Planned at**: commit `8b8f81e`, 2026-11-11

## Why this matters

`plugins/system-design-companion/.codex-plugin/plugin.json` duplicates `name`,
`version`, `description`, `homepage`, `license`, `keywords`, and the MCP URL from
`plugin.json` and `mcp.json`. The README says it is "maintained separately", and
`scripts/sync.py` never reads it. A version bump that touches only the portable
inputs passes `--check` and ships a stale Codex manifest. Today the two match
(version `1.0.0`), so this is cheap to lock in now.

## Current state

- `.codex-plugin/plugin.json` keys: `name`, `version`, `description`, `author`,
  `homepage`, `repository`, `license`, `keywords`, `mcpServers` (with `"type": "http"`,
  the Codex spelling of streamable HTTP), `interface`, `skills`.
- `sync.py` `validate_plugin()` collects errors in `errors`, formatted
  `plugins/<name>/<file>: <problem>`.

## Steps

1. In `validate_plugin()`, when `.codex-plugin/plugin.json` exists, report a
   mismatch for each shared key (`name`, `version`, `description`, `homepage`,
   `license`, `keywords`) and for each MCP server URL.
   Don't generate the file; its `interface` block is hand-written.
2. Add a test modeled on `test_rejects_version_drift`: bump only the portable
   `version`, then expect `--check` to fail naming `.codex-plugin/plugin.json`.

## Done criteria

- [ ] `python3 scripts/sync.py --check` exits 0 on the current tree
- [ ] the unittest command prints `OK` with the new test

## STOP conditions

- If the owner wants Codex output generated rather than validated, stop. That's a larger plan.
