# lucas-plugins — Agent Plugins

Collection of [Agent Plugins](https://agent-plugins.org) (open standard, v1.0) for food & gym. Portable across Cursor, VS Code, Claude Code, and other conformant clients — each subfolder is a standalone plugin ( `plugin.json` at its root).

## Plugins

| Plugin | Directory | What it provides | Upstream |
|---|---|---|---|
| **ai-shopping** | `plugins/ai-shopping/` | Kroger/QFC shopping — product search, cart, lists, pantry, weekly deals, meal-planning context via MCP | [aranlucas/ai-shopping-mcp](https://github.com/aranlucas/ai-shopping-mcp) + `https://ai-meal-planner-mcp.aranlucas.workers.dev/mcp` |
| **workset** | `plugins/workset/` | `workset` workout planning & set-by-set training log (`opengym2`) — MCP at `https://opengym2.up.railway.app/mcp` + `workset-coach` skill | [aranlucas/opengym2](https://github.com/aranlucas/opengym2) |

## Install

Each plugin is directory-installable (spec §4). Point your client at the plugin directory, e.g.:

```bash
# example — client that installs from a local or git path
# Cursor / VS Code / Claude Code (Agent Plugins v1) — use the plugin path directly
plugins/ai-shopping
plugins/workset
```

Or clone and add via your client’s plugin UI:

```bash
git clone https://github.com/aranlucas/lucas-plugins.git
# then add `lucas-plugins/plugins/ai-shopping` and `lucas-plugins/plugins/workset` in your client
```

## Layout per plugin (spec §4.2)

```
plugin.json          # required manifest ($schema https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
mcp.json             # MCP servers ( $schema .../mcp.schema.json, type streamable-http )
skills/<name>/SKILL.md
```

Only `skills/` and `mcp.json` are portable in v1 — rules/agents/hooks are Cursor-specific extensions and not included here.

## Validation

Validate `plugin.json` and `mcp.json` against the schemas above. `plugin.json`/`mcp.json` `$schema` versions must match (spec §10.1).

## Sources

- MCP server: [aranlucas/ai-shopping-mcp](https://github.com/aranlucas/ai-shopping-mcp)
- Training app: [aranlucas/opengym2](https://github.com/aranlucas/opengym2)
