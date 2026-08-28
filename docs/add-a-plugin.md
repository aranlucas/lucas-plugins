# Add a plugin

Same steps as the [Cursor template](https://github.com/cursor/plugin-template/blob/main/docs/add-a-plugin.md).

1. `mkdir -p plugins/my-plugin/.cursor-plugin`
2. Add `plugins/my-plugin/.cursor-plugin/plugin.json` (`name` kebab-case, required)
3. Add components: `rules/*.mdc`, `skills/*/SKILL.md`, `agents/*.md`, `commands/*`, `hooks/hooks.json`, `mcp.json`, `assets/logo.svg`
4. Register in `.cursor-plugin/marketplace.json` → `plugins[]` with matching `name` + `source`
5. `node scripts/validate-template.mjs`
