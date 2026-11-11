# Plan 002: Every plugin's "service source" link resolves for a public reader

> **Executor instructions**: Follow this plan step by step and run each
> verification. Honor the STOP conditions. Update this plan's row in
> `plans/README.md` when done.
>
> **Drift check (run first)**: `git diff --stat 8b8f81e..HEAD -- README.md plugins/workset plugins/travel marketplace.json`

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (independent of 001; if 001 has landed, its README edits are adjacent but don't conflict)
- **Category**: docs
- **Planned at**: commit `8b8f81e`, 2026-11-11

## Why this matters

The workset plugin's homepage, skill and README point users at
`https://github.com/aranlucas/opengym2`, which returns HTTP 404 (`curl -o /dev/null -w '%{http_code}'`
→ `404`; `gh api repos/aranlucas/opengym2` → Not Found). The service still runs at
`https://opengym2.up.railway.app/mcp`. That host is declared in
`aranlucas/set-and-signal` (`.railway/railway.go:5`,
`const publicDomain = "opengym2.up.railway.app"`), a public repository described as
"Self-hostable workout planner and training log with … MCP". The travel plugin
links `https://github.com/aranlucas/trvl`, which is **private** (`gh repo view` →
`PRIVATE`), so public readers also get a 404.

## Current state

- `README.md:15`: workset row links `[opengym2](https://github.com/aranlucas/opengym2)`
- `README.md:17`: travel row links `[trvl](https://github.com/aranlucas/trvl)`
- `plugins/workset/plugin.json:5,10`: description ends "for opengym2."; `homepage` is the dead URL
- `plugins/workset/skills/workset-coach/SKILL.md:3,8,19`: three opengym2 mentions, one a link
- `plugins/travel/plugin.json:10`: `homepage` is the private repo

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Validate | `python3 scripts/sync.py --check` | exit 0 |
| Regenerate | `python3 scripts/sync.py` | exit 0 |
| Tests | `python3 -m unittest discover --start-directory tests --pattern 'test_*.py'` | `OK` |
| Link check | `curl -s -o /dev/null -w '%{http_code}' <url>` | `200` |

## Scope

In: the files listed above, plus the generated manifests that `sync.py` rewrites.
Out: `mcp.json` URLs (still live). Don't rename the `workset` plugin or its skill.

## Steps

1. Replace the workset links with `https://github.com/aranlucas/set-and-signal`.
   Call the product "Set & Signal" and keep "workset" as the plugin name. Bump workset
   1.1.0 → 1.1.1 in `plugin.json` and the `marketplace.json` entry, then run `python3 scripts/sync.py`.
2. For travel, point `homepage` at a public page. If none exists, use this
   repository's `plugins/travel` URL, and label the README cell "private service" instead of linking.
   **Verify**: every `https://github.com/...` URL under `README.md` and `plugins/*/plugin.json` returns 200 with curl.

## Done criteria

- [ ] `grep -rn 'github.com/aranlucas/opengym2' README.md plugins` returns nothing
- [ ] `python3 scripts/sync.py --check` exits 0 and the unittest command prints `OK`

## STOP conditions

- `set-and-signal` no longer declares `opengym2.up.railway.app`. In that case the
  workset service may have moved, so report it and don't edit links.
- The owner has a public trvl docs URL you can't confirm. Ask rather than invent one.

## Maintenance notes

An automated link check would need network access in CI. That's deliberately not proposed here;
the generator never contacts remote URLs.
