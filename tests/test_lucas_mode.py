import re
import shutil
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGED_SKILLS = REPOSITORY_ROOT / "plugins/lucas-mode/skills"


class LucasModeBundleTests(unittest.TestCase):
    def test_local_references_resolve_in_relocated_skill_bundle(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "skills"
            shutil.copytree(PACKAGED_SKILLS, bundle)
            for document in bundle.rglob("*.md"):
                links = re.findall(r"\[[^\]]+\]\(([^\s)]+)\)", document.read_text())
                for link in links:
                    target = urlsplit(link)
                    if target.scheme or target.netloc:
                        continue
                    with self.subTest(document=document.relative_to(bundle), link=link):
                        destination = (
                            document.parent / unquote(target.path)
                            if target.path else document
                        ).resolve()
                        self.assertTrue(destination.is_relative_to(bundle.resolve()))
                        self.assertTrue(destination.is_file(), f"Missing reference: {link}")
                        if target.fragment:
                            headings = re.findall(
                                r"^#{1,6} +(.+)$", destination.read_text(), re.MULTILINE
                            )
                            anchors = {
                                re.sub(r"[^\w\s-]", "", heading.lower()).replace(" ", "-")
                                for heading in headings
                            }
                            self.assertIn(unquote(target.fragment), anchors)

    def test_generated_bundle_contains_every_supporting_resource(self):
        for source in PACKAGED_SKILLS.rglob("*"):
            if not source.is_file():
                continue
            relative = source.relative_to(PACKAGED_SKILLS)
            with self.subTest(resource=relative):
                codex = REPOSITORY_ROOT / ".agents/skills" / relative
                claude = REPOSITORY_ROOT / ".claude/skills" / relative
                self.assertFalse(codex.is_symlink())
                self.assertEqual(codex.read_bytes(), source.read_bytes())
                self.assertEqual(claude.resolve(), source.resolve())


if __name__ == "__main__":
    unittest.main()
