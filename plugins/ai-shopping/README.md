# ai-shopping — Agent Plugin

[Agent Plugin](https://agent-plugins.org) for Kroger/QFC shopping. Connects to the remote MCP at `https://ai-meal-planner-mcp.aranlucas.workers.dev/mcp`.

## Install

This directory is a standalone plugin (`plugin.json` at root). Install the path `plugins/ai-shopping` in any Agent Plugins v1 client (Cursor, VS Code, Claude Code, etc.).

## What it provides

- **MCP**: `ai-shopping` → `streamable-http` `https://ai-meal-planner-mcp.aranlucas.workers.dev/mcp` (OAuth)
- **Skill**: `shopping-assistant` (`skills/shopping-assistant/SKILL.md`)

## Source

Full server: [aranlucas/ai-shopping-mcp](https://github.com/aranlucas/ai-shopping-mcp)
