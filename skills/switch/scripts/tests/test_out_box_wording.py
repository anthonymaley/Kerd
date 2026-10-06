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


if __name__ == "__main__":
    unittest.main()
