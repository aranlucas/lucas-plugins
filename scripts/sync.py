#!/usr/bin/env python3
"""Sync portable Agent Plugins core to client marketplace manifests.

Source of truth:
  marketplace.json  (canonical catalog, pluginRoot + source)
  plugins/*/plugin.json  (portable, https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
  plugins/*/mcp.json     (portable, https://agent-plugins.org/schemas/1.0.0/mcp.schema.json) -> Cursor expects type http via mcpServers field

This script validates and *emits*:
  .claude-plugin/marketplace.json
  .cursor-plugin/marketplace.json
  plugins/*/.claude-plugin/plugin.json
  plugins/*/.cursor-plugin/plugin.json  (with mcpServers + http translation)

Fixes double-prefix bug: with pluginRoot "./plugins", source must be "./ai-shopping" not "./plugins/ai-shopping"
Cursor joins pluginRoot + source and sparse-checkouts plugins/plugins/ai-shopping if double-prefixed.
"""
import json, pathlib, sys, shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load(p): return json.loads(p.read_text())
def save(p, data): 
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2)+"\n")

def fix_source(source, plugin_root="./plugins"):
    # if pluginRoot is ./plugins and source is ./plugins/x -> ./x
    if source.startswith("./plugins/") and plugin_root == "./plugins":
        return source.replace("./plugins/", "./", 1)
    return source

def main():
    ok=True
    # 1. Validate portable
    for d in [ROOT/"plugins/ai-shopping", ROOT/"plugins/workset"]:
        for f in [d/"plugin.json", d/"mcp.json"]:
            if not f.exists():
                print(f"missing {f}", file=sys.stderr); ok=False; continue
            try:
                data=load(f)
                assert "$schema" in data, f"{f} missing $schema"
            except Exception as e:
                print(f"invalid {f}: {e}", file=sys.stderr); ok=False
        for skill in (d/"skills").glob("*/SKILL.md"):
            if not skill.read_text().startswith("---"):
                print(f"bad frontmatter {skill}", file=sys.stderr); ok=False

    # 2. Sync marketplaces from canonical marketplace.json
    canon = ROOT/"marketplace.json"
    if not canon.exists():
        print("missing marketplace.json", file=sys.stderr); sys.exit(1)
    mp = load(canon)
    plugin_root = mp.get("metadata", {}).get("pluginRoot", "./plugins")

    # Fix double-prefix in canonical
    for pl in mp.get("plugins", []):
        orig = pl.get("source","")
        fixed = fix_source(orig, plugin_root)
        if orig != fixed:
            print(f"fix {pl['name']}: source {orig} -> {fixed}")
            pl["source"] = fixed
    # Save canonical if fixed
    save(canon, mp)

    # Emit .claude-plugin/marketplace.json (verbatim copy with $schema)
    save(ROOT/".claude-plugin/marketplace.json", mp)

    # Emit .cursor-plugin/marketplace.json (Cursor variant: no $schema on plugins, description short)
    cursor_mp = {
        "name": mp["name"],
        "owner": mp["owner"],
        "metadata": {
            "description": mp["metadata"]["description"],
            "version": mp["metadata"]["version"],
            "pluginRoot": mp["metadata"]["pluginRoot"],
        },
        "plugins": [
            {"name": p["name"], "source": p["source"], "description": p["description"]}
            for p in mp["plugins"]
        ]
    }
    save(ROOT/".cursor-plugin/marketplace.json", cursor_mp)

    # 3. Sync per-plugin client manifests
    for d in [ROOT/"plugins/ai-shopping", ROOT/"plugins/workset"]:
        name = d.name
        portable = load(d/"plugin.json")
        # .claude-plugin/plugin.json - minimal portable mirror
        claude_out = ROOT/f"plugins/{name}/.claude-plugin/plugin.json"
        claude_data = {
            "name": portable["name"],
            "version": portable["version"],
            "description": portable["description"],
            "author": portable["author"],
            "homepage": portable.get("homepage"),
            "repository": portable.get("repository"),
        }
        # remove None
        claude_data = {k:v for k,v in claude_data.items() if v is not None}
        save(claude_out, claude_data)

        # .cursor-plugin/plugin.json - must include mcpServers + logo
        cursor_out = ROOT/f"plugins/{name}/.cursor-plugin/plugin.json"
        existing = load(cursor_out) if cursor_out.exists() else {}
        cursor_data = {
            "name": portable["name"],
            "displayName": existing.get("displayName") or ("AI Shopping (Kroger/QFC)" if name=="ai-shopping" else "workset — Workout Planner"),
            "version": portable["version"],
            "description": portable["description"] if name=="workset" else "Kroger/QFC shopping for Cursor — product search, cart, shopping lists, pantry, weekly deals, and meal-planning context via MCP.",
            "author": portable["author"],
            "homepage": portable.get("homepage"),
            "repository": portable.get("repository"),
            "license": portable.get("license","ISC"),
            "keywords": portable.get("keywords", []),
            "logo": "assets/logo.svg",
            "mcpServers": "./mcp.json",
        }
        save(cursor_out, cursor_data)

        # Ensure mcp.json transport is http for Cursor (portable uses streamable-http, Cursor uses http)
        # Keep portable as http per user fix - translate if needed
        mcp_p = d/"mcp.json"
        mcp = load(mcp_p)
        for srv in mcp.get("mcpServers", {}).values():
            if srv.get("type") == "streamable-http":
                srv["type"] = "http"
                print(f"translate {name} mcp type streamable-http -> http for Cursor")
        save(mcp_p, mcp)

    print("sync: emitted marketplaces + client manifests")
    print("validate:", "passed" if ok else "failed")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
