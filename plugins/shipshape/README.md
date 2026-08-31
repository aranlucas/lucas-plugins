# shipshape — Agent Plugin

[Agent Plugin](https://agent-plugins.org) for read-only GitHub portfolio
maintenance. Connects to the production Shipshape MCP server on Cloudflare
Workers.

## Install

This directory is a standalone plugin (`plugin.json` at root). Install
`plugins/shipshape` in any Agent Plugins v1 client.

## What it provides

- **MCP**: `shipshape` → `streamable-http`
  `https://shipshape-mcp.aranlucas.workers.dev/mcp` (OAuth)
- **Skill**: `shipshape-maintainer`
  (`skills/shipshape-maintainer/SKILL.md`)

The MCP exposes six read-only tools for portfolio snapshots, repository
readiness, branch risk, delivery hygiene, security posture, and deterministic
action plans. It inspects public repositories only and never mutates, clones,
or executes repository code.

## Source

Full server: [aranlucas/shipshape-mcp](https://github.com/aranlucas/shipshape-mcp)
