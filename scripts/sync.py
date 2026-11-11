#!/usr/bin/env python3
"""Validate the portable plugins and emit Claude/Cursor marketplace files.

Use ``--check`` in CI to validate that generated files are current without
rewriting the checkout.

Source of truth:
  marketplace.json
  plugins/*/plugin.json
  plugins/*/mcp.json
  plugins/*/cursor.json (optional Cursor presentation metadata)
  plugins/*/mcp-tools.json (optional MCP tool inventory; validation input only)
  plugins/*/skills/*/SKILL.md

When a plugin has ``mcp-tools.json``, each backticked snake_case name in its
skills must be a tool that the inventory records. The inventory names the
upstream source each list was copied from, so a skill cannot keep sending the
agent to a tool the server has removed.

Claude Code discovers plugin MCP servers from ``.mcp.json`` at the plugin
root. The portable ``mcp.json`` remains the source of truth; this script emits
the Claude-compatible mirror without the portable schema extension.

Claude resolves explicit ``./plugins/<name>`` sources from the marketplace
root. Cursor's importer instead expects bare names and joins them with
``metadata.pluginRoot``; the two catalogs are emitted separately below.
"""

import argparse
import json
import pathlib
import re
import sys
from dataclasses import dataclass
from urllib.parse import urlparse


ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
MCP_TYPES = {"stdio", "streamable-http", "sse"}
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
TOOL_NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
# The packaged servers name tools in snake_case and response fields in
# camelCase, so a backticked snake_case span in a skill is a tool reference.
SKILL_TOOL_REF_RE = re.compile(r"`([a-z][a-z0-9]*(?:_[a-z0-9]+)+)`")


@dataclass
class Plugin:
    name: str
    entry: dict
    source: str
    directory: pathlib.Path
    manifest: dict
    mcp: dict | None
    cursor: dict
    has_skills: bool


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


def validate_tool_inventory(plugin_dir, mcp, errors):
    """Return the inventoried tool names, or None when the plugin has no inventory."""
    path = plugin_dir / "mcp-tools.json"
    if not path.exists():
        return None
    label = path.relative_to(ROOT)
    try:
        inventory = load(path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: invalid JSON: {exc}")
        return None
    if not isinstance(inventory, dict) or not inventory:
        errors.append(f"{label}: must be a non-empty object keyed by MCP server name")
        return None

    servers = mcp.get("mcpServers") if isinstance(mcp, dict) else None
    servers = servers if isinstance(servers, dict) else {}
    tools = set()
    for server_name, record in inventory.items():
        prefix = f"{label}: {server_name}"
        if server_name not in servers:
            errors.append(f"{prefix} is not a server in mcp.json")
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        source = record.get("source")
        try:
            parsed = urlparse(source) if isinstance(source, str) else None
        except ValueError:
            parsed = None
        if not parsed or parsed.scheme != "https" or not parsed.hostname:
            errors.append(f"{prefix}.source must be an absolute HTTPS URL")
        names = record.get("tools")
        if (
            not isinstance(names, list)
            or not names
            or not all(isinstance(tool, str) and TOOL_NAME_RE.fullmatch(tool) for tool in names)
        ):
            errors.append(f"{prefix}.tools must be a non-empty array of snake_case tool names")
            continue
        if len(set(names)) != len(names):
            errors.append(f"{prefix}.tools must not repeat a tool")
        tools.update(names)
    return tools


def validate_plugin(name, plugin_dir, errors, entry, source):
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

    if not isinstance(manifest, dict):
        errors.append(f"{manifest_path.relative_to(ROOT)}: must be an object")
        return
    for field in ("version", "description"):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            errors.append(f"{manifest_path.relative_to(ROOT)}: {field} is required")
    if entry.get("version") != manifest.get("version"):
        errors.append(f"{manifest_path.relative_to(ROOT)}: version must match marketplace entry")
    if not (plugin_dir / "assets/logo.svg").is_file():
        errors.append(f"{plugin_dir.relative_to(ROOT)}/assets/logo.svg: missing Cursor logo")
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        errors.append(f"{manifest_path.relative_to(ROOT)}: expected $schema {PLUGIN_SCHEMA}")
    if manifest.get("name") != name:
        errors.append(
            f"{manifest_path.relative_to(ROOT)}: name must match marketplace entry {name!r}"
        )

    cursor_path = plugin_dir / "cursor.json"
    cursor_config = {}
    if cursor_path.exists():
        try:
            cursor_config = load(cursor_path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{cursor_path.relative_to(ROOT)}: invalid JSON: {exc}")
        else:
            if not isinstance(cursor_config, dict):
                errors.append(f"{cursor_path.relative_to(ROOT)}: must be an object")
            elif (
                not isinstance(cursor_config.get("displayName"), str)
                or not cursor_config["displayName"].strip()
            ):
                errors.append(
                    f"{cursor_path.relative_to(ROOT)}: displayName must be a non-empty string"
                )

    mcp = None
    if mcp_path.exists():
        try:
            mcp = load(mcp_path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{mcp_path.relative_to(ROOT)}: invalid JSON: {exc}")
            mcp = None

        else:
            if not isinstance(mcp, dict):
                errors.append(f"{mcp_path.relative_to(ROOT)}: must be an object")
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
                    if not isinstance(server_type, str) or server_type not in MCP_TYPES:
                        errors.append(
                            f"{label}.type must be one of {sorted(MCP_TYPES)}, got {server_type!r}"
                        )
                        continue
                    if server_type == "stdio":
                        command = server.get("command")
                        if not isinstance(command, str) or not command.strip():
                            errors.append(f"{label}.command must be a non-empty string")
                        args = server.get("args", [])
                        if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
                            errors.append(f"{label}.args must be an array of strings")
                    if server_type in {"streamable-http", "sse"}:
                        url = server.get("url")
                        try:
                            parsed = urlparse(url) if isinstance(url, str) else None
                            if parsed:
                                # urllib validates the port only when this property is read.
                                _ = parsed.port
                        except ValueError:
                            parsed = None
                        if not parsed or parsed.scheme not in {"http", "https"} or not parsed.hostname:
                            errors.append(f"{label}.url must be an absolute HTTP(S) URL")

    tools = validate_tool_inventory(plugin_dir, mcp, errors)

    skills_dir = plugin_dir / "skills"
    if skills_dir.exists():
        for directory in sorted(skills_dir.iterdir()):
            if directory.is_dir() and not (directory / "SKILL.md").is_file():
                errors.append(f"{directory.relative_to(ROOT)}/SKILL.md: missing")
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
            if tools is not None:
                cited = set(SKILL_TOOL_REF_RE.findall(skill.read_text()))
                for tool in sorted(cited - tools):
                    errors.append(
                        f"{skill.relative_to(ROOT)}: names MCP tool {tool!r}, which "
                        f"{plugin_dir.relative_to(ROOT)}/mcp-tools.json does not list"
                    )

    return Plugin(name, entry, source, plugin_dir, manifest, mcp, cursor_config,
                  skills_dir.is_dir())


def build_artifacts(marketplace, resolved):
    # The canonical catalog is also the Claude Code catalog. Its sources are
    # explicit paths from the marketplace root (for example,
    # ``./plugins/shipshape``), which works on Claude Code versions that do not
    # yet support ``metadata.pluginRoot``. Cursor gets a separate catalog below
    # with bare names under its ``pluginRoot`` convention.
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
                "name": plugin.name,
                "source": plugin.source,
                "description": plugin.entry["description"],
                **{key: plugin.entry[key] for key in ("version", "author")
                   if plugin.entry.get(key) is not None},
            }
            for plugin in resolved
        ],
    }
    artifacts[pathlib.Path(".cursor-plugin/marketplace.json")] = cursor_marketplace

    for plugin in resolved:
        plugin_dir = plugin.directory
        common = {
            key: plugin.manifest[key]
            for key in ("name", "version", "description", "author", "homepage",
                        "repository", "license", "keywords")
            if plugin.manifest.get(key) is not None
        }

        claude_data = common.copy()
        if plugin.has_skills:
            # Keep the component path explicit, matching Claude Code's
            # first-party marketplace template while retaining the portable
            # fixed-layout source of truth.
            claude_data["skills"] = "./skills/"
        artifacts[
            plugin_dir.relative_to(ROOT) / ".claude-plugin/plugin.json"
        ] = claude_data

        # Agent Plugins keeps the portable MCP schema in mcp.json, while Claude
        # Code loads plugin servers from the root-level .mcp.json convention.
        if plugin.mcp is not None:
            claude_mcp = {
                key: value for key, value in plugin.mcp.items() if key != "$schema"
            }
            artifacts[plugin_dir.relative_to(ROOT) / ".mcp.json"] = claude_mcp

        cursor_data = {
            **common,
            "displayName": plugin.cursor.get("displayName", plugin.name),
            "logo": "assets/logo.svg",
        }
        artifacts[
            plugin_dir.relative_to(ROOT) / ".cursor-plugin/plugin.json"
        ] = cursor_data

    return artifacts


def obsolete_artifacts(resolved):
    """Only the generated MCP mirror is conditional within a registered plugin."""
    return [plugin.directory.relative_to(ROOT) / ".mcp.json"
            for plugin in resolved if plugin.mcp is None]


def validate_output_paths(paths):
    # Reject links at every output component, including dangling links. Checking
    # the whole plan first prevents partial writes before an unsafe later output.
    errors = []
    for relative_path in paths:
        path = ROOT / relative_path
        for component in (path, *path.parents):
            if component == ROOT:
                break
            if component.is_symlink():
                errors.append(f"{relative_path}: generated output must not use symlinks")
                break
    return errors


def check_artifacts(artifacts, obsolete=()):
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

    for relative_path in obsolete:
        if (ROOT / relative_path).exists():
            stale.append(f"{relative_path}: obsolete")

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
    if not isinstance(marketplace, dict):
        print("error: marketplace.json: must be an object", file=sys.stderr)
        return 1
    if not isinstance(marketplace.get("name"), str) or not marketplace["name"].strip():
        errors.append("marketplace.json: name must be a non-empty string")
    if not isinstance(marketplace.get("owner"), dict):
        errors.append("marketplace.json: owner must be an object")

    metadata = marketplace.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("marketplace.json: metadata must be an object")
        metadata = {}
    for field in ("description", "version"):
        if not isinstance(metadata.get(field), str) or not metadata[field].strip():
            errors.append(f"marketplace.json: metadata.{field} must be a non-empty string")
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
    registered = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"marketplace.json: plugins[{index}] must be an object")
            continue
        if not isinstance(entry.get("description"), str) or not entry["description"].strip():
            errors.append(
                f"marketplace.json: plugins[{index}].description must be a non-empty string"
            )
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
        entry["source"] = f"./{plugin_root}/{source}"

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
        registered.add(plugin_dir.resolve())
        plugin = validate_plugin(name, plugin_dir, errors, entry, source)
        if plugin is not None:
            resolved.append(plugin)

    for manifest_path in sorted((ROOT / plugin_root).glob("*/plugin.json")):
        if manifest_path.parent.resolve() not in registered:
            errors.append(f"{manifest_path.relative_to(ROOT)}: plugin is not registered in marketplace")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"validate: failed ({len(errors)} error(s))", file=sys.stderr)
        return 1

    artifacts = build_artifacts(marketplace, resolved)
    obsolete = obsolete_artifacts(resolved)
    output_errors = validate_output_paths([*artifacts, *obsolete])
    if output_errors:
        for error in output_errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    if args.check:
        if not check_artifacts(artifacts, obsolete):
            return 1
        print("validate: passed")
        return 0

    for relative_path, data in artifacts.items():
        save(ROOT / relative_path, data)

    for relative_path in obsolete:
        (ROOT / relative_path).unlink(missing_ok=True)

    print(f"sync: emitted marketplaces + {len(resolved)} plugin manifests")
    print("validate: passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
