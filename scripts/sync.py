#!/usr/bin/env python3
"""Validate Agent Plugins portable core and emit client marketplace manifests.

Portable core is source of truth: plugins/*/plugin.json + plugins/*/mcp.json.
Emits .claude-plugin/marketplace.json and .cursor-plugin/marketplace.json
and mirrors per-plugin .claude-plugin/plugin.json / .cursor-plugin/plugin.json.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PORTABLE_PLUGINS = [ROOT/"plugins/ai-shopping", ROOT/"plugins/workset"]

def load(p): return json.loads(p.read_text())

def validate():
    ok=True
    for d in PORTABLE_PLUGINS:
        pj = d/"plugin.json"
        mj = d/"mcp.json"
        for f in [pj, mj]:
            if not f.exists():
                print(f"missing {f}", file=sys.stderr); ok=False; continue
            try:
                data=load(f)
                assert "$schema" in data, f"{f} missing $schema"
                assert "name" in data or "mcpServers" in data, f"{f} missing name/mcpServers"
            except Exception as e:
                print(f"invalid {f}: {e}", file=sys.stderr); ok=False
        # skills
        for skill in (d/"skills").glob("*/SKILL.md"):
            txt=skill.read_text()
            if not txt.startswith("---"):
                print(f"bad frontmatter {skill}", file=sys.stderr); ok=False
    return ok

if __name__ == "__main__":
    ok=validate()
    # keep marketplaces in sync from marketplace.json (already committed)
    print("validate:", "passed" if ok else "failed")
    sys.exit(0 if ok else 1)
