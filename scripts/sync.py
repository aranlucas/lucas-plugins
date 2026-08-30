#!/usr/bin/env python3
"""Validate the portable plugins and emit Claude/Cursor marketplace files.

Use ``--check`` in CI to validate that generated files are current without
rewriting the checkout.

Source of truth:
  marketplace.json
  plugins/*/plugin.json
  plugins/*/mcp.json
  plugins/*/skills/*/SKILL.md

Claude marketplace paths require a leading ``./``. Cursor's importer expects
bare paths and joins ``metadata.pluginRoot`` with each plugin's ``source``;
emitting the Claude form there can make it request ``plugins/plugins/<name>``.
"""

import argparse
import json
import pathlib
import re
import sys
from urllib.parse import urlparse


ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
MCP_TYPES = {"stdio", "streamable-http", "sse"}
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")


def load(path):
    return json.loads(path.read_text())


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(data))


def render(data):
    return json.dumps(data, indent=2) + "\n"


def clean_path(value):
    """Return a normalized, repository-relative marketplace path."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("must be a non-empty string")
    value = value.strip()
    while value.startswith("./"):
        value = value[2:]
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value in {"", "."}:
        raise ValueError(f"must be a safe repository-relative path: {value!r}")
    return path.as_posix()


def parse_frontmatter(path):
    text = path.read_text()
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("missing closing YAML frontmatter delimiter") from exc

    values = {}
    for line in lines[1:end]:
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def validate_plugin(name, plugin_dir, errors):
    manifest_path = plugin_dir / "plugin.json"
    mcp_path = plugin_dir / "mcp.json"

    if not manifest_path.is_file():
        errors.append(f"{manifest_path.relative_to(ROOT)}: missing")
        return

    try:
        manifest = load(manifest_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{manifest_path.relative_to(ROOT)}: invalid JSON: {exc}")
        return

    if manifest.get("$schema") != PLUGIN_SCHEMA:
        errors.append(f"{manifest_path.relative_to(ROOT)}: expected $schema {PLUGIN_SCHEMA}")
    if manifest.get("name") != name:
        errors.append(
            f"{manifest_path.relative_to(ROOT)}: name must match marketplace entry {name!r}"
        )

    if mcp_path.exists():
        try:
            mcp = load(mcp_path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{mcp_path.relative_to(ROOT)}: invalid JSON: {exc}")
            mcp = None

        if mcp is not None:
            if mcp.get("$schema") != MCP_SCHEMA:
                errors.append(f"{mcp_path.relative_to(ROOT)}: expected $schema {MCP_SCHEMA}")
            servers = mcp.get("mcpServers")
            if not isinstance(servers, dict):
                errors.append(f"{mcp_path.relative_to(ROOT)}: mcpServers must be an object")
            else:
                for server_name, server in servers.items():
                    label = f"{mcp_path.relative_to(ROOT)}: mcpServers.{server_name}"
                    if not isinstance(server, dict):
                        errors.append(f"{label} must be an object")
                        continue
                    server_type = server.get("type")
                    if server_type not in MCP_TYPES:
                        errors.append(
                            f"{label}.type must be one of {sorted(MCP_TYPES)}, got {server_type!r}"
                        )
                    if server_type in {"streamable-http", "sse"}:
                        url = server.get("url")
                        parsed = urlparse(url) if isinstance(url, str) else None
                        if not parsed or parsed.scheme not in {"http", "https"} or not parsed.netloc:
                            errors.append(f"{label}.url must be an absolute HTTP(S) URL")

    skills_dir = plugin_dir / "skills"
    if skills_dir.exists():
        for skill in sorted(skills_dir.glob("*/SKILL.md")):
            try:
                frontmatter = parse_frontmatter(skill)
            except (OSError, ValueError) as exc:
                errors.append(f"{skill.relative_to(ROOT)}: {exc}")
                continue
            if frontmatter.get("name") != skill.parent.name:
                errors.append(
                    f"{skill.relative_to(ROOT)}: name must match directory {skill.parent.name!r}"
                )
            if not frontmatter.get("description"):
                errors.append(f"{skill.relative_to(ROOT)}: description is required")


def build_artifacts(marketplace, resolved):
    """Build the files emitted by sync without writing any of them."""
    artifacts = {
        pathlib.Path("marketplace.json"): marketplace,
        pathlib.Path(".claude-plugin/marketplace.json"): marketplace,
    }

    metadata = marketplace["metadata"]
    cursor_marketplace = {
        "name": marketplace["name"],
        "owner": marketplace["owner"],
        "metadata": {
            "description": metadata["description"],
            "version": metadata["version"],
            "pluginRoot": metadata["pluginRoot"].removeprefix("./"),
        },
        "plugins": [
            {
                "name": entry["name"],
                "source": source,
                "description": entry["description"],
                "version": entry.get("version"),
                "author": entry.get("author"),
            }
            for _, entry, source, _ in resolved
        ],
    }
    for entry in cursor_marketplace["plugins"]:
        for key in ["version", "author"]:
            if entry[key] is None:
                del entry[key]
    artifacts[pathlib.Path(".cursor-plugin/marketplace.json")] = cursor_marketplace

    for name, _, _, plugin_dir in resolved:
        portable = load(plugin_dir / "plugin.json")
        common = {
            "name": portable["name"],
            "version": portable.get("version"),
            "description": portable.get("description"),
            "author": portable.get("author"),
            "homepage": portable.get("homepage"),
            "repository": portable.get("repository"),
            "license": portable.get("license"),
            "keywords": portable.get("keywords"),
        }

        claude_data = {
            key: value
            for key, value in common.items()
            if key not in {"license", "keywords"} and value is not None
        }
        artifacts[
            plugin_dir.relative_to(ROOT) / ".claude-plugin/plugin.json"
        ] = claude_data

        existing_path = plugin_dir / ".cursor-plugin/plugin.json"
        existing = load(existing_path) if existing_path.exists() else {}
        cursor_data = {
            **{key: value for key, value in common.items() if value is not None},
            "displayName": existing.get("displayName")
            or ("AI Shopping (Kroger/QFC)" if name == "ai-shopping" else name),
            "logo": "assets/logo.svg",
        }
        artifacts[
            plugin_dir.relative_to(ROOT) / ".cursor-plugin/plugin.json"
        ] = cursor_data

    return artifacts


def check_artifacts(artifacts):
    stale = []
    for relative_path, data in artifacts.items():
        path = ROOT / relative_path
        expected = render(data).encode()
        try:
            actual = path.read_bytes()
        except OSError:
            stale.append(f"{relative_path}: missing")
            continue
        if actual != expected:
            stale.append(f"{relative_path}: stale")

    if stale:
        for error in stale:
            print(f"error: generated artifact {error}", file=sys.stderr)
        print(
            f"check: failed ({len(stale)} generated artifact(s) out of date)",
            file=sys.stderr,
        )
        return False

    print(f"check: passed ({len(artifacts)} generated artifacts up to date)")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate portable plugins and sync marketplace artifacts."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate generated artifacts without rewriting any files",
    )
    args = parser.parse_args(argv)

    canonical_path = ROOT / "marketplace.json"
    try:
        marketplace = load(canonical_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid marketplace.json: {exc}", file=sys.stderr)
        return 1

    errors = []
    metadata = marketplace.setdefault("metadata", {})
    try:
        plugin_root = clean_path(metadata.get("pluginRoot", "plugins"))
    except ValueError as exc:
        errors.append(f"marketplace.json: metadata.pluginRoot {exc}")
        plugin_root = "plugins"
    metadata["pluginRoot"] = f"./{plugin_root}"

    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        errors.append("marketplace.json: plugins must be an array")
        entries = []

    seen = set()
    resolved = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"marketplace.json: plugins[{index}] must be an object")
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            errors.append(f"marketplace.json: plugins[{index}].name is not lowercase kebab-case")
            continue
        if name in seen:
            errors.append(f"marketplace.json: duplicate plugin name {name!r}")
        seen.add(name)

        try:
            source = clean_path(entry.get("source", name))
        except ValueError as exc:
            errors.append(f"marketplace.json: plugins[{index}].source {exc}")
            continue

        # Historical catalogs used source="./plugins/name" with pluginRoot="./plugins".
        # Keep only the path relative to pluginRoot so clients join it exactly once.
        prefix = f"{plugin_root}/"
        if source.startswith(prefix):
            source = source[len(prefix) :]
        entry["source"] = f"./{source}"

        plugin_dir = ROOT / plugin_root / source
        try:
            plugin_dir.resolve().relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"marketplace.json: source for {name!r} escapes the repository")
            continue
        if not plugin_dir.is_dir():
            errors.append(
                f"marketplace.json: {plugin_root}/{source} does not exist for plugin {name!r}"
            )
            continue
        resolved.append((name, entry, source, plugin_dir))
        validate_plugin(name, plugin_dir, errors)

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"validate: failed ({len(errors)} error(s))", file=sys.stderr)
        return 1

    artifacts = build_artifacts(marketplace, resolved)
    if args.check:
        if not check_artifacts(artifacts):
            return 1
        print("validate: passed")
        return 0

    for relative_path, data in artifacts.items():
        save(ROOT / relative_path, data)

    print(f"sync: emitted marketplaces + {len(resolved)} plugin manifests")
    print("validate: passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
