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
GENERATED_FILES = (
    Path("marketplace.json"),
    Path(".claude-plugin/marketplace.json"),
    Path(".cursor-plugin/marketplace.json"),
    *(Path(f"plugins/{name}/{artifact}")
      for name in PLUGIN_NAMES
      for artifact in (".claude-plugin/plugin.json", ".mcp.json", ".cursor-plugin/plugin.json")),
)


class SyncScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name) / "repository"
        shutil.copytree(
            REPOSITORY_ROOT,
            self.root,
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

    def test_check_rejects_display_name_drift_and_sync_repairs_it(self):
        target = self.root / "plugins/workset/.cursor-plugin/plugin.json"
        original = self.snapshot_generated_files()
        stale = json.loads(target.read_text())
        stale["displayName"] = "Accidentally edited generated name"
        target.write_text(json.dumps(stale, indent=2) + "\n")
        before_check = self.snapshot_generated_files()

        result = self.run_sync("--check")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("plugins/workset/.cursor-plugin/plugin.json: stale", result.stderr)
        self.assertEqual(before_check, self.snapshot_generated_files())
        repair = self.run_sync()
        self.assertEqual(repair.returncode, 0, repair.stderr)
        self.assertEqual(original, self.snapshot_generated_files())

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

    def test_claude_mcp_mirrors_match_portable_servers(self):
        for plugin in PLUGIN_NAMES:
            portable = json.loads((self.root / f"plugins/{plugin}/mcp.json").read_text())
            claude = json.loads((self.root / f"plugins/{plugin}/.mcp.json").read_text())

            self.assertNotIn("$schema", claude)
            self.assertEqual(claude["mcpServers"], portable["mcpServers"])

    def test_marketplace_sources_match_each_client_path_model(self):
        claude = json.loads((self.root / ".claude-plugin/marketplace.json").read_text())
        cursor = json.loads((self.root / ".cursor-plugin/marketplace.json").read_text())

        self.assertEqual(claude["metadata"]["pluginRoot"], "./plugins")
        self.assertEqual(
            [plugin["source"] for plugin in claude["plugins"]],
            [f"./plugins/{plugin['name']}" for plugin in claude["plugins"]],
        )
        self.assertEqual(
            [plugin["source"] for plugin in cursor["plugins"]],
            [plugin["name"] for plugin in cursor["plugins"]],
        )

    def test_claude_manifests_declare_the_default_skill_directory(self):
        for plugin in PLUGIN_NAMES:
            manifest = json.loads(
                (self.root / f"plugins/{plugin}/.claude-plugin/plugin.json").read_text()
            )
            self.assertEqual(manifest["skills"], "./skills/")
            portable = json.loads((self.root / f"plugins/{plugin}/plugin.json").read_text())
            self.assertEqual(manifest["keywords"], portable["keywords"])

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
