import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GENERATED_FILES = (
    Path("marketplace.json"),
    Path(".claude-plugin/marketplace.json"),
    Path(".cursor-plugin/marketplace.json"),
    Path("plugins/ai-shopping/.claude-plugin/plugin.json"),
    Path("plugins/ai-shopping/.cursor-plugin/plugin.json"),
    Path("plugins/workset/.claude-plugin/plugin.json"),
    Path("plugins/workset/.cursor-plugin/plugin.json"),
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


if __name__ == "__main__":
    unittest.main()
