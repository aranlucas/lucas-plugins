# Plan 004 (direction, spike): Decide whether and how to package garmin-mcp

> **Executor instructions**: This is a design/spike plan. Produce the decision
> record described below. Do not add a plugin directory or catalog entry.
>
> **Drift check (run first)**: `git diff --stat 8b8f81e..HEAD -- ROADMAP.md marketplace.json`

## Status

- **Priority**: P3
- **Effort**: M (coarse)
- **Risk**: LOW (no code change)
- **Depends on**: 001 (a new plugin's skill should ship with an `mcp-tools.json` inventory)
- **Category**: direction
- **Planned at**: commit `8b8f81e`, 2026-11-11

## Why this matters

garmin-mcp (private repo `aranlucas/garmin-mcp`) shipped `get_garmin_week` today
(upstream #54). Its README documents a single OAuth connector at
`https://garmin-mcp.aranlucas.workers.dev/mcp` with read tools (day, week, summaries,
activity), nine Training write tools, and `delete_stored_garmin_data`. This
marketplace's `ROADMAP.md` sets a gate: "Add Digits or Garmin distribution
only after their first-use journey and target-client support are verified." The
workset plugin already covers training planning, so the overlap needs a decision.

## Questions to answer (write the answers to `docs/garmin-first-use.md`)

1. Does the OAuth flow (central Auth plus Garmin account linking) complete in
   Claude Code and in Cursor? Record each client's result and any blocker.
2. What is the first useful journey? A candidate: "review my week" via `get_garmin_week`.
   It returns no data until a device syncs, because Garmin Starter has no historical
   backfill. How should the skill explain an empty result?
3. Which tools are writes (workouts, calendar, `delete_stored_garmin_data`)? What
   approval language must the skill carry?
4. Should Garmin stay a separate plugin, or join workset, given the shared fitness domain?

## Done criteria

- [ ] `docs/garmin-first-use.md` answers all four questions with observed results
- [ ] `ROADMAP.md` updated with the decision, keeping the existing gate wording

## STOP conditions

- If the connector can't be authorized in a target client, record the blocker and stop.
