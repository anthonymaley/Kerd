"""Switch In offers the weekly review as one Open work line when it is due.

Agreed with Anthony on 2026-11-03: In finds the newest weekly review record in its
one folder; none, or over 7 days old, adds a single Open work line that runs as a
Conductor route, recommended only when nothing else is buildable. This checks that
the wording is present, not that a model follows it.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]
SWITCH = ROOT / "skills/switch"


def flat(rel):
    return " ".join((SWITCH / rel).read_text(encoding="utf-8").split())


class WeeklyReviewLineTests(unittest.TestCase):
    def test_in_guide_states_the_line(self):
        text = flat("references/in.md")
        start = text.index("### Compose the arrival in Switch")
        end = text.index("### Restore the existing team")
        section = text[start:end]
        for phrase in (
            "**The weekly review line.**",
            "../../conductor/references/weekly-review.md#the-review-record",
            "`notes:weekly-review/`",
            "`docs/work/weekly-review/`",
            "it is a bounded lookup, not a sweep",
            "over 7 days old",
            "“Weekly review: last one N days ago”",
            "“Weekly review: never run”",
            "runs as a Conductor route when picked",
            "It is the recommendation only when nothing else is buildable.",
            "One line, never a list, never repeated elsewhere on the screen.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, section)

    def test_must_hold_carries_it(self):
        text = flat("SKILL.md")
        self.assertIn("Find the newest weekly review record in its one folder, never a sweep", text)
        self.assertIn("“Weekly review: last one N days ago”", text)
        self.assertIn("recommended only when nothing else is buildable", text)

    def test_the_link_resolves(self):
        self.assertTrue((ROOT / "skills/conductor/references/weekly-review.md").is_file())


if __name__ == "__main__":
    unittest.main()
