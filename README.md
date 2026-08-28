# lucas-plugins — Cursor Marketplace

Multi-plugin Cursor marketplace for food & gym:

- **ai-shopping** — Kroger/QFC shopping via remote MCP (`https://ai-meal-planner-mcp.aranlucas.workers.dev/mcp`), plus the `shopping-assistant` skill.
- **workset** — workout planner & training log companion (`aranlucas/opengym2`), with the `workset-coach` skill.

## Layout

```
.cursor-plugin/marketplace.json
plugins/ai-shopping/.cursor-plugin/plugin.json  + mcp.json, skills/, rules/
plugins/workset/.cursor-plugin/plugin.json      + skills/, rules/
scripts/validate-template.mjs
```

## Validate

```bash
node scripts/validate-template.mjs
```

## Publish

Submit the repo at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish). Each plugin is installable from **Customize → Plugins** once listed; community fallback is [cursor.directory](https://cursor.directory). See `docs/add-a-plugin.md`.

## Sources

- MCP server: [aranlucas/ai-shopping-mcp](https://github.com/aranlucas/ai-shopping-mcp)
- Training app: [aranlucas/opengym2](https://github.com/aranlucas/opengym2)
