"""Switch Out ends on its saved-place box: nothing follows the closing line.
Evals on 2026-10-05 saw Sonnet add a note after the restart line (a preserved
file, a commit trailer); In already said nothing follows its question, Out did
not. This checks presence of the wording, not that a model follows it.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]


def read(rel):
    return " ".join((ROOT / rel).read_text(encoding="utf-8").split())


class OutBoxWordingTests(unittest.TestCase):
    def test_each_file_carries_its_fragment(self):
        for rel, fragment in (
            ("skills/switch/SKILL.md",
             "its shape copied from the guide; nothing follows its closing line;"),
            ("skills/switch/references/out.md",
             "The box is the last thing in the message: its closing line ends Out, and nothing "
             "follows it: no note, footer, commit trailer or remark about a preserved file."),
        ):
            with self.subTest(rel=rel):
                self.assertIn(fragment, read(rel))

    def test_notes_commit_is_written_before_the_last_commit(self):
        out = read("skills/switch/references/out.md")
        self.assertIn("save the vault repo first and take its commit", out)
        self.assertLess(out.index("save the vault repo first and take its commit"),
                        out.index("Then prove the boundary, after the last commit"))
        self.assertIn("Never write anything after a passed check.", out)
        self.assertIn("write its commit into the start point before the project's last commit",
                      read("skills/switch/SKILL.md"))


if __name__ == "__main__":
    unittest.main()
