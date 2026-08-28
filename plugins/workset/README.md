# workset — Cursor Plugin

Training companion for [aranlucas/opengym2](https://github.com/aranlucas/opengym2) (workset): workout planning, set-by-set logging, and progress context.

Connects Cursor to the hosted workset MCP at `https://opengym2.up.railway.app/mcp` (Railway, OAuth via `/.well-known/oauth-protected-resource`).

Bundled `mcp.json` points to the remote MCP server — OAuth is handled by Cursor on connect.

This plugin also ships a skill and rule for Cursor agents; the app can also run locally (`go run ./cmd/opengym-api`) or wherever you host opengym2.

## Skill: workset-coach

`skills/workset-coach/SKILL.md` — activated when the user asks to plan, log, or review training.

## Source

[aranlucas/opengym2](https://github.com/aranlucas/opengym2)
