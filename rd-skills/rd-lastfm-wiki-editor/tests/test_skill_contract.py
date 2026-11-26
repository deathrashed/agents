"""Basic portable package contract checks; no external services required."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_required_yaml_metadata_and_folder_name(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        front = skill.split("---", 2)[1]
        self.assertIn(f"name: {ROOT.name}", front)
        match = re.search(r"^description: (.+)$", front, re.M)
        self.assertIsNotNone(match)
        self.assertTrue(1 <= len(match.group(1)) <= 1024)
        self.assertIn('version: "1.1.0"', front)

    def test_all_local_markdown_references_exist(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for relative in re.findall(r"\]\((references/[^)]+\.md)\)", skill):
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_nonpublication_boundary_is_prominent(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("never submit, save, publish", text)
        self.assertIn("never submit anything to last.fm", text)
        self.assertIn("user publishes manually", text)
        self.assertIn("artwork-sourcing.md", text)
        self.assertIn("page-inspection.md", text)


if __name__ == "__main__":
    unittest.main()
