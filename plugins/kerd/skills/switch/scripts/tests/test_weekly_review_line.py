"""Switch In offers the weekly review as one Open work line when it is due.

Agreed with Anthony on 2026-11-03: In finds the newest weekly review record in its
one folder; none, or over 7 days old, adds a single Open work line that runs as a
Conductor route, recommended only when nothing else is buildable. Since the
2026-11-13 first-user walkthrough the line waits for history (3+ session logs,
7+ days) and is named as Kerd's look back, not a "weekly review" meeting. This checks that
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
            "“Kerd's look back at recent sessions (weekly review): last one N days ago”",
            "“Kerd's look back at recent sessions (weekly review): never run”",
            "It runs as a Conductor route when picked.",
            "It is the recommendation only when nothing else is buildable.",
            "One line, never a list, never repeated elsewhere on the screen.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, section)

    def test_must_hold_carries_it(self):
        text = flat("SKILL.md")
        self.assertIn("find the newest weekly review record in its one folder, never a sweep", text)
        self.assertIn("“Kerd's look back at recent sessions (weekly review): last one N days ago”", text)
        self.assertIn("recommended only when nothing else is buildable", text)

    def test_the_line_waits_for_history(self):
        # First-user walkthrough 2026-11-13, finding 9: a one-day-old project with
        # one sitting was told to run "the weekly review", taken for a meeting.
        section = flat("references/in.md")
        for phrase in (
            "It appears only once the project has history, read in three bounded lookups, each of which can fail:",
            "At least 3 are needed; fewer than 3: no line, however old the project.",
            # Final review, items 5 and 6: one definition, and a failed git read is unknown.
            "The first Kerd record is the oldest dated session log, or the date `CONTEXT.md` was first "
            "committed when that is older.",
            "`git log --diff-filter=A --format=%as -- CONTEXT.md`",
            "an empty result (`CONTEXT.md` never committed) leaves the session-log date, and a failed git "
            "read is unknown, so the line is not shown.",
            "At least 7 days since the first Kerd record are needed.",
            "is meant to say whose review it is, Kerd's look back at its own sessions, as distinct "
            "from any review meeting the person holds.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, section)
        self.assertNotIn("“Weekly review: never run”", section)
        self.assertNotIn("A failed or empty read here leaves the session-log date", section)
        skill = flat("SKILL.md")
        self.assertIn("The weekly review line waits for history: at least 3 session logs and at least "
                      "7 days since the first Kerd record, which is the oldest dated session log, or "
                      "`CONTEXT.md`'s first commit when that is older; with fewer than 3 session logs "
                      "there is no line", skill)

    def test_an_unreadable_folder_is_unknown_not_absent(self):
        # Review round 1, item 2: a failed read must not become "never run".
        section = flat("references/in.md")
        for phrase in (
            "A folder that does not exist is a successful read with nothing in it.",
            "A folder that exists but cannot be read, or a read that errors, is unknown, not absent:",
            "an unknown session count or review date shows no line, and an unreadable review "
            "folder is never reported as “never run”.",
            "Only successful reads with enough dated evidence show the line.",
            # Review round 2, item 4: an unreadable vault.json leaves the folder unknown.
            "Choosing the folder is itself a read: a `kivna/vault.json` that exists but cannot be read or "
            "parsed, or a notes root it names that cannot be reached, leaves the folder unknown, and the "
            "line is not shown.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, section)
        self.assertIn("a read that fails is unknown, not absent, so it shows no line either", flat("SKILL.md"))

    def test_the_link_resolves(self):
        self.assertTrue((ROOT / "skills/conductor/references/weekly-review.md").is_file())


if __name__ == "__main__":
    unittest.main()
