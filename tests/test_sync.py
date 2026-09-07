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
