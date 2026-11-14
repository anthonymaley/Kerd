"""Conductor and guide wording from the simulated non-developer walkthrough on
released 0.197.0 (first-user round 5, 2026-11-14): new findings 3, 5 and 7.
Each test pins one rule as phrase checks on whitespace-flattened text: it checks
the wording is present, not that a model follows it.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
CONDUCTOR = REPO / "skills" / "conductor"
SKILL = CONDUCTOR / "SKILL.md"
REFS = CONDUCTOR / "references"
GUIDE = REPO / "docs" / "guide" / "getting-started.md"


def flat(text):
    return " ".join(text.split())


def read(path):
    return flat(path.read_text(encoding="utf-8"))


class NeverDenyAWordItUsed(unittest.TestCase):
    """New 3: a progress line said "whether there's a remote"; asked what a remote
    is, Kerd replied "I didn't say that word to you earlier"."""

    def test_journey(self):
        journey = read(REFS / "journey.md")
        self.assertIn("**The person sees the in-between lines too.**", journey)
        self.assertIn("for a person who has not used git's words, keep them out of progress "
                      "lines too", journey)
        self.assertIn("Asked what a word means, explain it plainly and answer the worry behind "
                      "it; never claim the word wasn't said, since a progress line may have said "
                      "it.", journey)


class SaveHowTheyWantIt(unittest.TestCase):
    """New 5: "keep the technical stuff out of my way" was saved nowhere, so the
    next sitting opened on a stage label."""

    def test_record_template_and_rule(self):
        record = read(REFS / "work-record.md")
        self.assertIn("# Work: <outcome> How they want it: <a standing preference in the "
                      "person's own words", record)
        self.assertIn("**Save how they want it.** When the person says they want technical "
                      "detail kept out of the way (or is plainly not technical), write that "
                      "preference, in their words, on the record's `How they want it:` header "
                      "line the same turn, so a fresh session reads it before it speaks.", record)

    def test_entry_reads_it_back(self):
        entry = read(REFS / "entry.md")
        self.assertIn("Save that preference in their words on the sketchbook's `How they want "
                      "it:` line", entry)
        self.assertIn("On entering existing work, read that line before the first reply and "
                      "follow it as written, from the first word, even in a fresh session that "
                      "never heard them say it", entry)
        # Codex round 1: a saved wish for MORE detail must not switch on the plain-words rule.
        self.assertIn("this paragraph applies only when the line asks for less technical detail; "
                      "a line asking for more (“show me the commands”) gets that instead.", entry)
        skill = read(SKILL)
        self.assertIn("Save that preference in their words on the sketchbook's `How they want "
                      "it:` line, and read that line back on entering existing work before the "
                      "first reply.", skill)


class GuidePromptsMatchAFirstArrival(unittest.TestCase):
    """New 7: the guide showed where_we_are.py and handoff.py and promised git
    prompts; a first arrival asked for the guide read, roll_status.py and
    where_we_are.py, and no git command prompted."""

    def test_guide(self):
        guide = read(GUIDE)
        self.assertNotIn("three kinds of thing", guide)
        self.assertIn("**A quick status check.**", guide)
        self.assertIn("skills/switch/scripts/roll_status.py --project", guide)
        self.assertIn("skills/switch/scripts/where_we_are.py", guide)
        self.assertIn("Those usually run without a prompt", guide)
        section = guide.split("## Permission prompts", 1)[1].split("## Your first sitting", 1)[0]
        self.assertNotIn("handoff.py ...", section)
        self.assertNotIn("**Git checks.**", section)


if __name__ == "__main__":
    unittest.main()
