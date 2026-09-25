# System Design Companion — Agent Plugin

Collaborate on a shared Excalidraw canvas for system design. Create diagrams,
add architecture components and connections, and review a design with your agent.

## Install

From the Lucas Plugins marketplace in Claude Code:

```text
/plugin install system-design-companion@lucas-plugins
```

In Cursor, enable **System Design Companion** from the marketplace.
Other compatible clients can use this plugin directory directly. A Codex manifest
is included in `.codex-plugin/plugin.json`.

## Connection

The plugin connects to the remote MCP server over Streamable HTTP:

`https://system-design-companion.aranlucas.workers.dev/mcp`

No local server or CLI is required.

## Use

Ask the agent to create a diagram, or paste an existing canvas share link and ask
it to join. For example:

- “Create a system design diagram for a URL shortener.”
- “Join this diagram and add a cache in front of the database.”
- “Review this architecture and explain its tradeoffs.”

The server provides session instructions and tools for reading the canvas,
editing components and connections, arranging diagrams, and reviewing designs.
