# Lucas Plugins

[![Validation](https://img.shields.io/github/actions/workflow/status/aranlucas/lucas-plugins/ci.yml?branch=main&label=manifests)](https://github.com/aranlucas/lucas-plugins/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A marketplace of remote MCP connections and skills for Claude Code, Cursor,
and compatible Agent Plugins v1 clients. The services run elsewhere; installing
these plugins does not start a local server or require their development tools.

## Available plugins

| Plugin | Use it for | Service source / documentation | Agent workflow |
| --- | --- | --- | --- |
| [`groceries`](plugins/groceries) | Kroger/QFC shopping, saved lists, carts, pantry, meal plans, and deals | [ai-shopping-mcp](https://github.com/aranlucas/ai-shopping-mcp) | [shopping-assistant](plugins/groceries/skills/shopping-assistant/SKILL.md) |
| [`workset`](plugins/workset) | Workout planning, set logging, and progress | [opengym2](https://github.com/aranlucas/opengym2) | [workset-coach](plugins/workset/skills/workset-coach/SKILL.md) |
| [`shipshape`](plugins/shipshape) | A ranked, read-only maintenance queue for your GitHub repositories | [shipshape-mcp](https://github.com/aranlucas/shipshape-mcp) | [shipshape-maintainer](plugins/shipshape/skills/shipshape-maintainer/SKILL.md) |
| [`travel`](plugins/travel) | Flights, hotels, ground transport, rental cars, and itineraries | [trvl](https://github.com/aranlucas/trvl) | [travel-planner](plugins/travel/skills/travel-planner/SKILL.md) |
| [`system-design-companion`](plugins/system-design-companion) | Create, join, edit, or review a shared Excalidraw architecture diagram | [System Design Companion](https://system-design-companion.aranlucas.workers.dev) | [system-design-companion](plugins/system-design-companion/skills/system-design-companion/SKILL.md) |

Groceries, workset, and Shipshape use OAuth; complete the client's sign-in prompt
when required. Shipshape is owner-only: it reports stored practice results for the
repositories its GitHub App tracks, including private ones. Its MCP tools are
read-only, and it never executes repository code. For System Design Companion, ask the agent to
create a diagram or give it an existing canvas share link to join.

See the [roadmap](ROADMAP.md) for planned first-use and connection-recovery work.

## Install

### Claude Code

```text
/plugin marketplace add aranlucas/lucas-plugins
/plugin install groceries@lucas-plugins
```

Replace `groceries` with any plugin name in the table above.

### Cursor

Open **Settings → Plugins → Add Marketplace → Import from Repo**, enter
`aranlucas/lucas-plugins`, and enable the plugins you need.

### Other compatible clients

Point the client at an individual directory such as `plugins/travel`.
System Design Companion also includes a [Codex manifest](plugins/system-design-companion/.codex-plugin/plugin.json).
Client support beyond the generated Claude and Cursor manifests is host-specific.

### Migrating Lucas Mode

T3 workflows moved to [t3-pstack](https://github.com/chhoumann/t3-pstack#install).
Follow its installation and per-machine setup instructions, then disable or
uninstall the old `lucas-mode@lucas-plugins` installation if enabled.

## Maintaining manifests

Edit `marketplace.json` for the catalog, and each plugin's `plugin.json` and
`mcp.json` for metadata and connections. Optional `cursor.json` holds a non-empty
`displayName`; otherwise Cursor uses the plugin name. Skills and logos are
maintained in each plugin's `skills/` and `assets/` directories.

Optional `mcp-tools.json` records, per MCP server, the tool names a skill may cite
and the upstream `source` URL (pinned to a commit) they were copied from. When it
exists, every backticked snake_case name in that plugin's skills must be listed,
so a skill cannot keep pointing at a tool the server removed. When a server's
tools change, update the list from its source, then fix the skills that fail.
Write response fields and other non-tool values without backticked snake_case.

```bash
python3 scripts/sync.py
python3 scripts/sync.py --check
python3 -m unittest discover --start-directory tests --pattern 'test_*.py'
```

Sync generates the Claude and Cursor catalogs and plugin manifests, plus Claude
`.mcp.json` mirrors. Edit the portable inputs, then run sync and review the diff.
`--check` reports drift without repairing it; CI runs that check and the tests.
System Design Companion's `.codex-plugin/plugin.json` is maintained separately.

The generator handles different client path conventions: Claude resolves
`./plugins/<name>` from the marketplace root; Cursor joins a bare plugin name to
`metadata.pluginRoot`. This conversion requires repository-specific logic beyond
JSON formatting. Generated outputs can be recreated without losing Cursor display
names because those names live in maintained `cursor.json` inputs.

Validation checks selected manifest fields, paths, versions, MCP URLs, skill
front matter, skill tool references, logos, and generated parity; it does not load the referenced JSON
schemas. Invalid inputs fail before generated files are written.

License metadata remains unresolved: groceries and workset declare ISC in their
plugin manifests, while this repository has an MIT [LICENSE](LICENSE) and no
plugin-specific ISC license files. Clarify package versus upstream-service
licensing before changing those declarations.
