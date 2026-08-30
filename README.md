# lucas-plugins — Agent Plugins + Marketplace

[Agent Plugins](https://agent-plugins.org) v1.0 portable core for food & gym, plus a marketplace wrapper for distribution. The portable part (`plugin.json` + `mcp.json` + `skills/`) works in any v1 client; the marketplace files are the distribution layer the spec leaves to clients.

## Plugins

| Plugin | Directory | Portable core | MCP | Upstream |
|---|---|---|---|---|
| **ai-shopping** | `plugins/ai-shopping/` | `plugin.json`, `skills/shopping-assistant/SKILL.md` | `streamable-http` `https://ai-meal-planner-mcp.aranlucas.workers.dev/mcp` | [aranlucas/ai-shopping-mcp](https://github.com/aranlucas/ai-shopping-mcp) |
| **workset** | `plugins/workset/` | `plugin.json`, `skills/workset-coach/SKILL.md` | `streamable-http` `https://opengym2.up.railway.app/mcp` | [aranlucas/opengym2](https://github.com/aranlucas/opengym2) |

## Why marketplace is separate

Spec (§4–§10) defines only the plugin package (`plugin.json` at each plugin root, fixed `mcp.json`/`skills/`). It explicitly does **not** define the marketplace — that is client distribution. This repo keeps the portable core as source of truth and generates the client marketplaces:

```
marketplace.json                      # source of truth (canonical catalog)
plugins/*/plugin.json                 # portable manifests (edit these)
plugins/*/mcp.json                    # portable MCP (edit these)
plugins/*/skills/*/SKILL.md           # portable skills
.claude-plugin/marketplace.json       # generated — Claude Code
.cursor-plugin/marketplace.json       # generated — Cursor
plugins/*/.claude-plugin/plugin.json  # generated mirrors
plugins/*/.cursor-plugin/plugin.json  # generated mirrors
scripts/sync.py                       # validate + regenerate
```

## Install

**As a marketplace (picker):**

Claude Code:
```
/plugin marketplace add aranlucas/lucas-plugins
/plugin install ai-shopping@lucas-plugins
/plugin install workset@lucas-plugins
```

Cursor: Dashboard → **Plugins → Add Marketplace → Import from Repo** → `aranlucas/lucas-plugins`, then enable `ai-shopping` / `workset`.

**As direct plugin paths (no marketplace):**

Point your client at the plugin directory:
```
plugins/ai-shopping
plugins/workset
```

## Validate

```bash
python3 scripts/sync.py --check
# validates schemas and fails if generated marketplace/plugin mirrors are stale

python3 scripts/sync.py
# validates and regenerates the generated marketplace/plugin mirrors
```

Portable `plugin.json`/`mcp.json` `$schema` must match (§10.1): `https://agent-plugins.org/schemas/1.0.0/...`.
