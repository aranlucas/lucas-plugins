# Lucas Plugins

A small collection of [Agent Plugins](https://agent-plugins.org) for Claude Code, Cursor, and other compatible clients.

## Plugins

| Plugin | What it does | Source |
| --- | --- | --- |
| [ai-shopping](plugins/ai-shopping) | Search Kroger/QFC, manage your cart and lists, and plan meals. | [ai-shopping-mcp](https://github.com/aranlucas/ai-shopping-mcp) |
| [workset](plugins/workset) | Plan workouts, log sets, and review training progress. | [Set and Signal](https://github.com/aranlucas/opengym2) |
| [shipshape](plugins/shipshape) | Review public GitHub repositories and get a ranked maintenance plan. | [shipshape-mcp](https://github.com/aranlucas/shipshape-mcp) |
| [travel](plugins/travel) | Search flights, hotels, ground transport, rental cars, and destinations. | [trvl](https://github.com/aranlucas/trvl) |

## Install

### Claude Code

Add the marketplace, then install the plugin you want:

```text
/plugin marketplace add aranlucas/lucas-plugins
/plugin install ai-shopping@lucas-plugins
```

Replace `ai-shopping` with `workset`, `shipshape`, or `travel` to install another plugin. OAuth-backed plugins will ask you to sign in the first time you use them. Travel requires the [trvl CLI on your client's PATH](plugins/travel#prerequisite).

### Cursor

Open **Settings → Plugins → Add Marketplace → Import from Repo**, enter `aranlucas/lucas-plugins`, and enable the plugins you want.

### Other clients

Use a plugin directory directly, such as `plugins/ai-shopping`. Each plugin follows the Agent Plugins v1 format.

## Development

Edit the files in `plugins/` or `marketplace.json`, then validate and regenerate the client-specific files:

```bash
python3 scripts/sync.py
python3 scripts/sync.py --check
python3 -m unittest discover --start-directory tests --pattern 'test_*.py'
```

The root `marketplace.json`, each plugin's `plugin.json` and `mcp.json`, skills,
and assets are maintained sources. `scripts/sync.py` generates the Claude and
Cursor catalogs, client manifests, and `.mcp.json` mirrors. Cursor display names
are currently preserved from its generated manifests. Do not hand-edit other
generated fields. CI checks generated files and runs the sync tests.
