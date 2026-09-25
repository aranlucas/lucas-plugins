# Travel Agent Plugin

Travel planning with [trvl](https://github.com/aranlucas/trvl): search flights,
hotels, ground transport, rental cars, destinations, and trip plans.

## Install

```text
/plugin marketplace add aranlucas/lucas-plugins
/plugin install travel@lucas-plugins
```

In Cursor, enable `travel` from the `aranlucas/lucas-plugins` marketplace.
Other Agent Plugins v1 clients can use `plugins/travel` directly.

## Connection

The plugin connects over Streamable HTTP to the hosted MCP server:

`https://trvl-production.up.railway.app/mcp`

No local trvl CLI or Go installation is needed.

## Contents

- MCP server: `trvl`, connected to the hosted endpoint over Streamable HTTP.
- Skill: `travel-planner` in `skills/travel-planner/SKILL.md`.
