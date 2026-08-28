# lucas-plugins

Food & gym plugins by Lucas.

## Plugins

| Plugin | Stack | What it does | Link |
|---|---|---|---|
| **ai-shopping-mcp** | Cloudflare Workers + MCP | Kroger/QFC shopping — OAuth, product search, cart, lists, weekly deals, pantry/kitchen inventory. Hosted at `https://ai-meal-planner-mcp.aranlucas.workers.dev/mcp`. | [aranlucas/ai-shopping-mcp](https://github.com/aranlucas/ai-shopping-mcp) |
| **opengym2** (workset) | Go + SQLite + React | Self-hosted workout planning & set-by-set training log — passkey auth, PWA. | [aranlucas/opengym2](https://github.com/aranlucas/opengym2) |

## Quick start

### ai-shopping-mcp

```json
{
  "mcpServers": {
    "ai-shopping-list": {
      "command": "pnpm",
      "args": ["dlx", "mcp-remote", "https://ai-meal-planner-mcp.aranlucas.workers.dev/mcp"]
    }
  }
}
```

### opengym2

```bash
git clone https://github.com/aranlucas/opengym2.git
cd opengym2
cp .env.example .env
go run ./cmd/opengym-api
```

## License

Each plugin retains its original license — see the individual repos.
