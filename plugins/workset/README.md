# workset — Agent Plugin

[Agent Plugin](https://agent-plugins.org) for `workset` (opengym2) — workout planning, set-by-set logging, and progress context.

## Install

This directory is a standalone plugin (`plugin.json` at root). Install the path `plugins/workset` in any Agent Plugins v1 client.

## What it provides

- **MCP**: `workset` → `streamable-http` `https://opengym2.up.railway.app/mcp` (OAuth, `/.well-known/oauth-protected-resource`)
- **Skill**: `workset-coach` (`skills/workset-coach/SKILL.md`)

App also runs locally: `go run ./cmd/opengym-api` in [aranlucas/opengym2](https://github.com/aranlucas/opengym2).

## Source

[aranlucas/opengym2](https://github.com/aranlucas/opengym2)
