# Plan 001: Skills name only the tools their MCP servers expose, and validation enforces it

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 8b8f81e..HEAD -- scripts/sync.py tests/test_sync.py plugins/groceries plugins/shipshape plugins/system-design-companion marketplace.json README.md`
> If any in-scope file changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: LOW (validation input only; generated client manifests change only in versions/descriptions)
- **Depends on**: none
- **Category**: bug
- **Planned at**: commit `8b8f81e`, 2026-11-11

## Why this matters

The plugins ship skills that tell the agent which MCP tools to call. Two of them
name tools the live servers no longer have, so an agent following the skill calls
tools that don't exist and misses the ones that do:

- `plugins/shipshape/skills/shipshape-maintainer/SKILL.md` (written 2026-08-30)
  directs the agent to `action_plan`, `repo_readiness`, `branch_risk`,
  `delivery_hygiene`, `security_posture` and `portfolio_snapshot`. shipshape-mcp
  replaced that surface on 2026-10-15 (upstream #77, "Replace portfolio scoring
  with owner-only practices dashboard"). Its `src/mcp.ts` at `ae8870b` registers
  exactly four tools: `practices_overview`, `repo_practices`, `practice_detail`,
  and `maintenance_priorities` (the last one shipped today, upstream #136). The skill
  and README also say Shipshape "inspects public repositories only". The upstream
  README now says it covers private repositories and only the configured owner can sign in.
- `plugins/groceries/skills/shopping-assistant/SKILL.md` names `get_store`,
  `get_product`, `add_to_inventory`, `remove_from_inventory` and
  `get_meal_planning_context`. ai-shopping-mcp's contract test
  (`test/evals/mcp-agent-contract.test.ts` at `c00fbdc`) asserts those five are
  *removed*. The skill also never mentions `get_shopping_list`,
  `update_shopping_list`, `update_inventory`, the four meal-plan tools, or
  `delete_shopping_list`, which shipped today (upstream #201) and is destructive.

Nothing in this repo can detect the drift. `docs/reliability-audit.md` (2026-11-06)
recorded "no concrete instruction/API mismatch established", because validation
checks skill front matter only.

## Current state

- `scripts/sync.py`: validates portable inputs, then emits the Claude/Cursor
  catalogs and manifests. `validate_plugin()` checks skills only for front matter
  `name`/`description` (the `for skill in sorted(skills_dir.glob("*/SKILL.md"))` loop).
  Errors are appended to a shared `errors` list. Any error stops generation before
  writes, which is the repo's no-partial-write contract.
- Optional maintained inputs follow the `cursor.json` pattern: absent means
  default behavior; present means validated, with diagnostics of the form
  `plugins/<name>/<file>: <problem>`.
- `tests/test_sync.py`: subprocess journeys against a temp copy of the repo
  (`self.run_sync(*args)`, `self.snapshot_generated_files()`). Model new tests on
  `test_rejects_invalid_maintained_cursor_config_without_writes`, which asserts
  the diagnostic, no `Traceback`, and unchanged generated files for both
  `sync` and `--check`.
- Upstream tool surfaces (verified 2026-11-11):
  - groceries: 18 tools, source `aranlucas/ai-shopping-mcp@c00fbdc test/evals/mcp-agent-contract.test.ts`
  - shipshape: 4 tools, source `aranlucas/shipshape-mcp@ae8870b src/mcp.ts`
  - system-design-companion: 14 tools, source `aranlucas/system-design-companion@71ef4b3 src/worker/mcp.ts`
    (its skill's `apply_patch`, `tidy`, `layout` all exist; no rewrite needed)
  - travel and workset skills name no tools and defer to live schemas. No inventory needed.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Validate + drift | `python3 scripts/sync.py --check` | `check: passed (18 generated artifacts up to date)` and `validate: passed` |
| Regenerate | `python3 scripts/sync.py` | `sync: emitted marketplaces + 5 plugin manifests` |
| Tests | `python3 -m unittest discover --start-directory tests --pattern 'test_*.py'` | `OK` |

Set `TMPDIR` to a roomy directory first; each test copies the repository.

## Scope

**In scope**: `scripts/sync.py`, `tests/test_sync.py`,
`plugins/{groceries,shipshape,system-design-companion}/mcp-tools.json` (create),
the groceries and shipshape `SKILL.md` and `plugin.json`, `marketplace.json`,
the generated artifacts `sync.py` rewrites, and `README.md`.

**Out of scope**: travel and workset skills (they name no tools); the SDC Codex
manifest; `docs/reliability-audit.md` (dated history); any live call to an MCP
server (all return 401 without OAuth, and the generator never contacts remote URLs, by design).

## Steps

1. **Add the inventory input.** Create `plugins/<name>/mcp-tools.json` shaped
   `{"<server name from mcp.json>": {"source": "<https URL pinned to a commit>", "tools": [sorted names]}}`
   for groceries, shipshape and system-design-companion, using the lists above.
2. **Validate it in `sync.py`.** Add `validate_tool_inventory(plugin_dir, mcp, errors)`.
   It returns `None` when the file is absent. Otherwise it reports invalid JSON, a
   non-object or empty object, a server not in `mcp.json`, a non-HTTPS `source`, a
   `tools` value that is not a non-empty array of snake_case names, and repeated tools.
   Call it before the skills loop.
3. **Check skill references.** When the inventory exists, every backticked
   snake_case span (`` `[a-z][a-z0-9]*(_[a-z0-9]+)+` ``) in the plugin's skills must
   be listed. Error: `<skill path>: names MCP tool '<tool>', which plugins/<name>/mcp-tools.json does not list`.
   **Verify**: with the old skills, `python3 scripts/sync.py --check` fails, listing
   the 5 groceries and 6 shipshape tools named above (11 errors).
4. **Rewrite the two skills** against the upstream tool descriptions and server
   instructions. Keep each skill's front matter `name`, add approval guidance for
   `delete_shopping_list` and cart adds, and state Shipshape's owner-only,
   stored-evidence, read-only scope. Write non-tool values (for example the state
   "not applicable") without backticked snake_case.
5. **Update metadata.** Groceries 2.0.0 → 2.1.0 and shipshape 1.1.0 → 2.0.0 (its
   advertised capabilities changed) in both `plugin.json` and the `marketplace.json`
   entry. Update the descriptions to match. Bump catalog `metadata.version` 0.7.0 → 0.8.0.
   Run `python3 scripts/sync.py`.
6. **README.** Update the shipshape and groceries rows and the Shipshape scope
   sentence. Document `mcp-tools.json` under "Maintaining manifests".

## Test plan

In `tests/test_sync.py`:
- `test_rejects_skill_naming_tool_removed_from_inventory_without_writes`: drop
  `maintenance_priorities` from the shipshape inventory. Both modes must fail with
  the diagnostic and leave generated files unchanged. Deleting the inventory makes
  `--check` pass again, because the inventory is opt-in.
- `test_rejects_invalid_tool_inventory_without_writes`: one case per diagnostic
  in step 2, run in both modes.
- Both tests must fail against `git show 8b8f81e:scripts/sync.py`.

## Done criteria

- [ ] `python3 scripts/sync.py --check` exits 0
- [ ] the unittest command prints `OK`, including the 2 new tests
- [ ] `grep -rnE 'action_plan|repo_readiness|branch_risk|delivery_hygiene|security_posture|portfolio_snapshot|get_meal_planning_context|remove_from_inventory|add_to_inventory|get_store\b|get_product\b' plugins/*/skills` returns nothing

## STOP conditions

- An upstream contract test or `mcp.ts` no longer matches the tool lists above. Re-derive the lists, and don't guess.
- A skill needs a backticked snake_case non-tool value that cannot be rephrased.
  Report it so the reference rule can be revisited; don't add an allowlist unasked.

## Maintenance notes

- The inventory is copied by hand from upstream; it is not checked live (OAuth).
  When a packaged server ships or removes tools, refresh its list from `source`.
  Bump the commit in the URL, then fix every skill that fails.
- The reference rule assumes these servers' convention: snake_case tools, camelCase fields.
  A server that breaks it needs a different rule.
