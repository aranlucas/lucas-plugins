# Lucas Plugins

## Give your coding agent a better weekend.

[![Validation](https://img.shields.io/github/actions/workflow/status/aranlucas/lucas-plugins/validate.yml?branch=main&label=manifests)](https://github.com/aranlucas/lucas-plugins/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Lucas Plugins is a portable Agent Plugins v1 marketplace for the hosted tools I use from Claude Code, Cursor, Codex, and other compatible clients. Install the grocery plugin before meal planning, the workset plugin after the gym, or Shipshape when a repository needs a release-readiness pass. Five remote MCP connections arrive with client-specific manifests and, where useful, a matching skill.

## Available plugins

| Plugin | Purpose | Hosted connection | Skill |
| --- | --- | --- | --- |
| [`groceries`](plugins/groceries) | Kroger/QFC product search, carts, lists, pantry, deals, and meal-planning context. | `ai-meal-planner-mcp.aranlucas.workers.dev/mcp` | `shopping-assistant` |
| [`workset`](plugins/workset) | Workout planning, set-by-set logging, and training progress context. | `opengym2.up.railway.app/mcp` | `workset-coach` |
| [`shipshape`](plugins/shipshape) | Read-only GitHub portfolio readiness, branch risk, delivery hygiene, security posture, and ranked action plans. | `shipshape-mcp.aranlucas.workers.dev/mcp` | `shipshape-maintainer` |
| [`travel`](plugins/travel) | Flight, hotel, ground transport, rental car, destination, and trip planning. | `trvl-production.up.railway.app/mcp` | `travel-planner` |
| [`system-design-companion`](plugins/system-design-companion) | Shared Excalidraw system-design diagrams and architecture review. | `system-design-companion.aranlucas.workers.dev/mcp` | `system-design-companion` |

The remote endpoints are configured in each plugin’s `mcp.json`; no local server is started by this repository. The individual plugin READMEs document OAuth or other service-specific behavior.

## Install

### Claude Code

Add this repository as a marketplace, then install one or more plugins:

```text
/plugin marketplace add aranlucas/lucas-plugins
/plugin install groceries@lucas-plugins
```

Replace `groceries` with `workset`, `shipshape`, `travel`, or `system-design-companion`. Plugins that use OAuth prompt for sign-in when their service requires it.

### Cursor

Open **Settings → Plugins → Add Marketplace → Import from Repo**, enter `aranlucas/lucas-plugins`, and enable the plugins you need.

### Other Agent Plugins clients

Point the client at an individual directory such as `plugins/travel`. Each directory contains a portable `plugin.json`, optional `mcp.json`, skills, and logo. The Codex manifest for System Design Companion is kept in that plugin’s `.codex-plugin/` directory.

## Repository structure and generated files

The source of truth is:

- `marketplace.json` for the catalog and versions.
- `plugins/*/plugin.json` for portable plugin metadata.
- `plugins/*/mcp.json` for portable MCP server definitions.
- `plugins/*/skills/*/SKILL.md` and `plugins/*/assets/` for skills and logos.

`scripts/sync.py` generates the Claude and Cursor marketplace catalogs, client manifests, and Claude `.mcp.json` mirrors. Do not hand-edit those generated fields.

## Development and validation

```bash
python3 scripts/sync.py
python3 scripts/sync.py --check
python3 -m unittest discover --start-directory tests --pattern 'test_*.py'
```

The validation workflow checks manifest paths, versions, schemas, MCP URLs, skill front matter, logos, and generated-file parity. The marketplace metadata is currently version `0.5.2`; plugin versions are recorded in `marketplace.json`.
