# Travel Agent Plugin

Travel planning with [trvl](https://github.com/aranlucas/trvl): search flights,
hotels, ground transport, rental cars, destinations, and trip plans.

## Prerequisite

Install Go and the trvl CLI before enabling the plugin:

```bash
go install github.com/aranlucas/trvl/cmd/trvl@latest
trvl mcp --help
```

The `trvl` executable must be on the MCP client's PATH. Go normally installs it
in `$(go env GOPATH)/bin` unless `GOBIN` is set. Restart the client after updating
its PATH. Provider credentials are optional and depend on the searches you use;
see the trvl source documentation for setup.

## Install

```text
/plugin marketplace add aranlucas/lucas-plugins
/plugin install travel@lucas-plugins
```

In Cursor, enable `travel` from the `aranlucas/lucas-plugins` marketplace.
Other Agent Plugins v1 clients can use `plugins/travel` directly.

## Contents

- MCP server: `trvl`, launched locally over stdio with `trvl mcp`.
- Skill: `travel-planner` in `skills/travel-planner/SKILL.md`.

The plugin launches the server itself; a separate `trvl mcp install` is not
needed and could register a duplicate server.
