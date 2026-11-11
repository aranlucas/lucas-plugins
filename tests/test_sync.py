import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAMES = tuple(
    entry["name"]
    for entry in json.loads((REPOSITORY_ROOT / "marketplace.json").read_text())["plugins"]
)
MCP_PLUGIN_NAMES = tuple(
    name for name in PLUGIN_NAMES
    if (REPOSITORY_ROOT / f"plugins/{name}/mcp.json").is_file()
)
GENERATED_FILES = (
    Path("marketplace.json"),
    Path(".claude-plugin/marketplace.json"),
    Path(".cursor-plugin/marketplace.json"),
    *(Path(f"plugins/{name}/{artifact}")
      for name in PLUGIN_NAMES
      for artifact in (".claude-plugin/plugin.json", ".cursor-plugin/plugin.json")),
    *(Path(f"plugins/{name}/.mcp.json") for name in MCP_PLUGIN_NAMES),
)


class SyncScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name) / "repository"
        shutil.copytree(
            REPOSITORY_ROOT,
            self.root,
            symlinks=True,
            ignore=shutil.ignore_patterns(".git", "__pycache__"),
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_sync(self, *args):
        return subprocess.run(
            [sys.executable, str(self.root / "scripts/sync.py"), *args],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

    def snapshot_generated_files(self):
        return {
            path: (self.root / path).read_bytes()
            for path in GENERATED_FILES
        }

    def test_check_leaves_current_artifacts_unchanged(self):
        before = self.snapshot_generated_files()

        result = self.run_sync("--check")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("check: passed", result.stdout)
        self.assertEqual(before, self.snapshot_generated_files())

    def test_check_reports_stale_artifact_without_rewriting_it(self):
        target = self.root / ".cursor-plugin/marketplace.json"
        original = self.snapshot_generated_files()
        stale = json.loads(target.read_text())
        stale["plugins"][0]["description"] = "stale generated description"
        target.write_text(json.dumps(stale, indent=2) + "\n")
        before_check = self.snapshot_generated_files()

        result = self.run_sync("--check")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "generated artifact .cursor-plugin/marketplace.json: stale",
            result.stderr,
        )
        self.assertEqual(before_check, self.snapshot_generated_files())

        repair = self.run_sync()

        self.assertEqual(repair.returncode, 0, repair.stderr)
        self.assertEqual(original, self.snapshot_generated_files())
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_sync_recreates_all_generated_artifacts_without_losing_display_names(self):
        original = self.snapshot_generated_files()
        for path in GENERATED_FILES:
            if path != Path("marketplace.json"):
                (self.root / path).unlink()

        result = self.run_sync()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(original, self.snapshot_generated_files())
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_sync_repairs_invalid_generated_cursor_json(self):
        target = self.root / "plugins/workset/.cursor-plugin/plugin.json"
        original = self.snapshot_generated_files()
        target.write_text("{broken json")
        before_check = self.snapshot_generated_files()

        result = self.run_sync("--check")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("plugins/workset/.cursor-plugin/plugin.json: stale", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(before_check, self.snapshot_generated_files())
        repair = self.run_sync()
        self.assertEqual(repair.returncode, 0, repair.stderr)
        self.assertEqual(original, self.snapshot_generated_files())

    def test_sync_uses_maintained_cursor_display_name(self):
        config = self.root / "plugins/workset/cursor.json"
        config.write_text(json.dumps({"displayName": "Updated workout planner"}))
        before_check = self.snapshot_generated_files()

        result = self.run_sync("--check")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("plugins/workset/.cursor-plugin/plugin.json: stale", result.stderr)
        self.assertEqual(before_check, self.snapshot_generated_files())
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads(
            (self.root / "plugins/workset/.cursor-plugin/plugin.json").read_text()
        )
        self.assertEqual(manifest["displayName"], "Updated workout planner")
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_sync_defaults_cursor_display_name_to_plugin_name(self):
        (self.root / "plugins/workset/cursor.json").unlink()

        result = self.run_sync()

        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads(
            (self.root / "plugins/workset/.cursor-plugin/plugin.json").read_text()
        )
        self.assertEqual(manifest["displayName"], "workset")
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_rejects_invalid_maintained_cursor_config_without_writes(self):
        config = self.root / "plugins/workset/cursor.json"
        original = self.snapshot_generated_files()
        for content, diagnostic in (
            ("{broken json", "invalid JSON"),
            ("null", "must be an object"),
            ("[]", "must be an object"),
            ("{}", "displayName must be a non-empty string"),
            ('{"displayName": null}', "displayName must be a non-empty string"),
            ('{"displayName": 12}', "displayName must be a non-empty string"),
            ('{"displayName": "  "}', "displayName must be a non-empty string"),
        ):
            for args in ((), ("--check",)):
                with self.subTest(content=content, args=args):
                    config.write_text(content)
                    result = self.run_sync(*args)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(f"plugins/workset/cursor.json: {diagnostic}", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(original, self.snapshot_generated_files())

    def test_removed_mcp_source_removes_generated_connection(self):
        (self.root / "plugins/travel/mcp.json").unlink()
        mirror = self.root / "plugins/travel/.mcp.json"
        before = self.snapshot_generated_files()
        result = self.run_sync("--check")
        self.assertEqual(result.returncode, 1, "removed MCP must fail check")
        self.assertIn("plugins/travel/.mcp.json: obsolete", result.stderr)
        self.assertEqual(before, self.snapshot_generated_files())
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(mirror.exists())
        self.assertTrue((self.root / "plugins/workset/.mcp.json").is_file())
        self.assertEqual(self.run_sync().returncode, 0)
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_generated_symlinks_cannot_overwrite_external_files(self):
        outside = Path(self.temp_dir.name) / "external"
        outside.mkdir()
        sentinel = outside / "marketplace.json"
        sentinel.write_bytes(b"external sentinel")
        # An earlier stale output must not be repaired before rejection.
        (self.root / ".claude-plugin/marketplace.json").write_bytes(b"stale catalog")
        # Both leaf links and directory links used to redirect writes outside.
        for directory_link in (False, True):
            target = self.root / ".cursor-plugin"
            saved = self.root / "cursor-backup"
            target.rename(saved)
            if directory_link:
                target.symlink_to(outside, target_is_directory=True)
            else:
                target.mkdir()
                (target / "marketplace.json").symlink_to(sentinel)
            try:
                before = self.snapshot_generated_files()
                for args in ((), ("--check",)):
                    with self.subTest(directory_link=directory_link, args=args):
                        result = self.run_sync(*args)
                        self.assertEqual(result.returncode, 1, "symlink output must fail")
                        self.assertIn("generated output must not use symlinks", result.stderr)
                        self.assertEqual(sentinel.read_bytes(), b"external sentinel")
                        self.assertEqual(before, self.snapshot_generated_files())
            finally:
                if directory_link:
                    target.unlink()
                else:
                    shutil.rmtree(target)
                saved.rename(target)

    def test_claude_mcp_mirrors_match_portable_servers(self):
        for plugin in MCP_PLUGIN_NAMES:
            portable = json.loads((self.root / f"plugins/{plugin}/mcp.json").read_text())
            claude = json.loads((self.root / f"plugins/{plugin}/.mcp.json").read_text())

            self.assertNotIn("$schema", claude)
            self.assertEqual(claude["mcpServers"], portable["mcpServers"])

    def test_marketplace_sources_match_each_client_path_model(self):
        target = self.root / "marketplace.json"
        marketplace = json.loads(target.read_text())
        marketplace["metadata"]["pluginRoot"] = "./extensions"
        for entry in marketplace["plugins"]:
            entry["source"] = entry["name"]
            if entry["name"] == "travel":
                entry["source"] = "./extensions/trip-planner"
        target.write_text(json.dumps(marketplace))
        (self.root / "plugins").rename(self.root / "extensions")
        (self.root / "extensions/travel").rename(self.root / "extensions/trip-planner")

        result = self.run_sync()

        self.assertEqual(result.returncode, 0, result.stderr)
        claude = json.loads((self.root / ".claude-plugin/marketplace.json").read_text())
        cursor = json.loads((self.root / ".cursor-plugin/marketplace.json").read_text())
        self.assertEqual(claude["metadata"]["pluginRoot"], "./extensions")
        self.assertEqual(cursor["metadata"]["pluginRoot"], "extensions")
        claude_sources = {plugin["name"]: plugin["source"] for plugin in claude["plugins"]}
        cursor_sources = {plugin["name"]: plugin["source"] for plugin in cursor["plugins"]}
        self.assertEqual(claude_sources["travel"], "./extensions/trip-planner")
        self.assertEqual(cursor_sources["travel"], "trip-planner")
        self.assertEqual(claude_sources["workset"], "./extensions/workset")
        self.assertEqual(cursor_sources["workset"], "workset")
        self.assertTrue(
            (self.root / "extensions/trip-planner/.claude-plugin/plugin.json").is_file()
        )
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_claude_manifests_declare_the_default_skill_directory(self):
        for plugin in PLUGIN_NAMES:
            manifest = json.loads(
                (self.root / f"plugins/{plugin}/.claude-plugin/plugin.json").read_text()
            )
            self.assertEqual(manifest["skills"], "./skills/")
            portable = json.loads((self.root / f"plugins/{plugin}/plugin.json").read_text())
            self.assertEqual(manifest["keywords"], portable["keywords"])

    def test_rejects_invalid_marketplace_shapes_without_writes(self):
        target = self.root / "marketplace.json"
        canonical = json.loads(target.read_text())
        cases = [
            ([], "marketplace.json: must be an object"),
            (None, "marketplace.json: must be an object"),
            ({**canonical, "metadata": None}, "marketplace.json: metadata must be an object"),
            ({**canonical, "metadata": []}, "marketplace.json: metadata must be an object"),
            ({**canonical, "metadata": {**canonical["metadata"], "description": None}},
             "marketplace.json: metadata.description must be a non-empty string"),
            ({**canonical, "metadata": {**canonical["metadata"], "version": "  "}},
             "marketplace.json: metadata.version must be a non-empty string"),
            ({key: value for key, value in canonical.items() if key != "name"},
             "marketplace.json: name must be a non-empty string"),
            ({key: value for key, value in canonical.items() if key != "owner"},
             "marketplace.json: owner must be an object"),
            ({**canonical, "metadata": {"pluginRoot": "./plugins"}},
             "marketplace.json: metadata.description must be a non-empty string"),
            ({**canonical, "plugins": [
                {key: value for key, value in entry.items() if key != "description"}
                for entry in canonical["plugins"]
            ]}, "marketplace.json: plugins[0].description must be a non-empty string"),
        ]
        for marketplace, diagnostic in cases:
            for args in ((), ("--check",)):
                with self.subTest(marketplace=marketplace, args=args):
                    target.write_text(json.dumps(marketplace))
                    before = self.snapshot_generated_files()
                    result = self.run_sync(*args)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn(diagnostic, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(before, self.snapshot_generated_files())

    def test_rejects_malformed_portable_mcp_without_writes(self):
        target = self.root / "plugins/travel/mcp.json"
        schema = json.loads(target.read_text())["$schema"]
        cases = [("{broken json", "invalid JSON")]
        non_objects = (None, False, True, 0, 1.5, "", "mcp", [], ["server"])
        for value in non_objects:
            cases.append((json.dumps(value), "must be an object"))
            cases.append((json.dumps({"$schema": schema, "mcpServers": value}),
                          "mcpServers must be an object"))
            cases.append((json.dumps({"$schema": schema, "mcpServers": {"test": value}}),
                          "mcpServers.test must be an object"))
        cases.append((json.dumps({"$schema": schema}), "mcpServers must be an object"))
        for server_type in (*non_objects, {}, "unsupported"):
            cases.append((json.dumps({"$schema": schema, "mcpServers": {
                "test": {"type": server_type}
            }}), "mcpServers.test.type must be one of"))
        cases.append((json.dumps({"$schema": schema, "mcpServers": {"test": {}}}),
                      "mcpServers.test.type must be one of"))
        for server_type in ("streamable-http", "sse"):
            for url in (None, "/mcp", "https://[invalid/mcp", "https://:443/mcp",
                        "https://example.com:invalid/mcp", "https://example.com:70000/mcp"):
                cases.append((json.dumps({"$schema": schema, "mcpServers": {
                    "test": {"type": server_type, "url": url}
                }}), "mcpServers.test.url must be an absolute HTTP(S) URL"))

        for content, diagnostic in cases:
            for args in ((), ("--check",)):
                with self.subTest(content=content, args=args):
                    target.write_text(content)
                    before = {
                        path.relative_to(self.root): path.read_bytes()
                        for path in self.root.rglob("*") if path.is_file()
                    }
                    result = self.run_sync(*args)
                    after = {
                        path.relative_to(self.root): path.read_bytes()
                        for path in self.root.rglob("*") if path.is_file()
                    }
                    self.assertEqual(before, after)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn(f"plugins/travel/mcp.json: {diagnostic}", result.stderr)
                    self.assertIn("validate: failed", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_rejects_invalid_stdio_configuration(self):
        target = self.root / "plugins/travel/mcp.json"
        original = json.loads(target.read_text())
        for server in (
            {"type": "stdio", "args": ["mcp"]},
            {"type": "stdio", "command": "trvl", "args": "mcp"},
        ):
            with self.subTest(server=server):
                original["mcpServers"]["trvl"] = server
                target.write_text(json.dumps(original))
                result = self.run_sync("--check")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("mcpServers.trvl", result.stderr)

    def test_registered_plugin_with_invalid_manifest_reports_only_validation_error(self):
        target = self.root / "plugins/travel/plugin.json"
        for content, diagnostic in (("{broken json", "invalid JSON"),
                                    ("[]", "must be an object")):
            with self.subTest(content=content):
                target.write_text(content)
                before = self.snapshot_generated_files()

                result = self.run_sync()

                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(f"plugins/travel/plugin.json: {diagnostic}", result.stderr)
                self.assertNotIn("plugin is not registered", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(before, self.snapshot_generated_files())

    def test_rejects_version_drift(self):
        target = self.root / "plugins/travel/plugin.json"
        manifest = json.loads(target.read_text())
        manifest["version"] = "9.0.0"
        target.write_text(json.dumps(manifest))
        result = self.run_sync("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("version must match marketplace entry", result.stderr)

    def test_rejects_missing_logo_and_skill(self):
        (self.root / "plugins/travel/assets/logo.svg").unlink()
        (self.root / "plugins/travel/skills/travel-planner/SKILL.md").unlink()
        result = self.run_sync("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing Cursor logo", result.stderr)
        self.assertIn("travel-planner/SKILL.md: missing", result.stderr)

    def test_rejects_skill_naming_tool_removed_from_inventory_without_writes(self):
        # The maintenance workflow: a server drops a tool, the inventory is updated
        # from upstream, and every skill that still sends the agent there must fail.
        inventory_path = self.root / "plugins/shipshape/mcp-tools.json"
        inventory = json.loads(inventory_path.read_text())
        inventory["shipshape"]["tools"].remove("maintenance_priorities")
        inventory_path.write_text(json.dumps(inventory))
        before = self.snapshot_generated_files()

        for args in ((), ("--check",)):
            with self.subTest(args=args):
                result = self.run_sync(*args)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(
                    "plugins/shipshape/skills/shipshape-maintainer/SKILL.md: names MCP tool "
                    "'maintenance_priorities', which plugins/shipshape/mcp-tools.json "
                    "does not list",
                    result.stderr,
                )
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(before, self.snapshot_generated_files())

        # The inventory is opt-in: without one, skill text is not checked.
        inventory_path.unlink()
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_rejects_invalid_tool_inventory_without_writes(self):
        target = self.root / "plugins/shipshape/mcp-tools.json"
        valid = json.loads(target.read_text())["shipshape"]
        prefix = "plugins/shipshape/mcp-tools.json:"
        cases = [
            ("{broken json", f"{prefix} invalid JSON"),
            ("[]", f"{prefix} must be a non-empty object keyed by MCP server name"),
            ("{}", f"{prefix} must be a non-empty object keyed by MCP server name"),
            (json.dumps({"shipshape": valid, "github": valid}),
             f"{prefix} github is not a server in mcp.json"),
            (json.dumps({"shipshape": []}), f"{prefix} shipshape must be an object"),
            (json.dumps({"shipshape": {**valid, "tools": ["repo_practices"] * 2}}),
             f"{prefix} shipshape.tools must not repeat a tool"),
        ]
        for source in (None, "", "github.com/aranlucas/shipshape-mcp",
                       "http://github.com/aranlucas/shipshape-mcp", "https://[invalid/mcp"):
            cases.append((json.dumps({"shipshape": {**valid, "source": source}}),
                          f"{prefix} shipshape.source must be an absolute HTTPS URL"))
        for tools in (None, [], "repo_practices", [1], ["RepoPractices"], ["repo-practices"]):
            cases.append((json.dumps({"shipshape": {**valid, "tools": tools}}),
                          f"{prefix} shipshape.tools must be a non-empty array of "
                          "snake_case tool names"))

        for content, diagnostic in cases:
            for args in ((), ("--check",)):
                with self.subTest(content=content, args=args):
                    target.write_text(content)
                    before = self.snapshot_generated_files()
                    result = self.run_sync(*args)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertIn(diagnostic, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(before, self.snapshot_generated_files())

    def test_rejects_unregistered_plugin(self):
        target = self.root / "marketplace.json"
        marketplace = json.loads(target.read_text())
        marketplace["plugins"] = [p for p in marketplace["plugins"] if p["name"] != "travel"]
        target.write_text(json.dumps(marketplace))
        result = self.run_sync("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("plugin is not registered", result.stderr)


if __name__ == "__main__":
    unittest.main()
