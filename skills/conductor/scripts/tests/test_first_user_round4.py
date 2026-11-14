"""Conductor wording from the simulated non-developer walkthrough rerun on 0.197.0
(first-user round 4, 2026-11-14): round-3 rows 3 and 18, new findings 1, 4 and 7.
Each test pins one rule as phrase checks on whitespace-flattened text: it checks
the wording is present, not that a model follows it.
"""
from pathlib import Path
import re
import unittest

REPO = Path(__file__).resolve().parents[4]
CONDUCTOR = REPO / "skills" / "conductor"
SKILL = CONDUCTOR / "SKILL.md"
REFS = CONDUCTOR / "references"


def flat(text):
    return " ".join(text.split())


def read(path):
    return flat(path.read_text(encoding="utf-8"))


class PlainEntryForANonTechnicalPerson(unittest.TestCase):
    """New 1: after "keep the technical stuff out of my way", the first turn opened
    with a stage label, agents, "rehearsal" and "the sketchbook"."""

    def test_entry_guide(self):
        entry = read(REFS / "entry.md")
        self.assertIn("**A person who wants the technical detail kept out of the way** (they said "
                      "so, or are plainly not technical) gets the entry update as one plain line in "
                      "their own terms", entry)
        self.assertIn("No stage label (“Conductor · Shape”), no mention of agents or helpers unless "
                      "one is started, and no rehearsal or sketchbook words until they matter to "
                      "something the person does.", entry)

    def test_skill_and_language_guide(self):
        skill = read(SKILL)
        self.assertIn("A person who asked to keep technical detail out of the way, or is plainly not "
                      "technical, gets one plain line: no stage label, no agents or helpers unless one "
                      "is started, no rehearsal or sketchbook words until they matter", skill)
        self.assertIn("For a person who wants technical detail kept out of the way, the words wait "
                      "until they matter to something the person does.", skill)
        journey = read(REFS / "journey.md")
        self.assertIn("For a person who asked to keep technical detail out of the way, or is plainly "
                      "not technical, the words wait until they matter to something the person does",
                      journey)


class DraftIsDoneWhenAccepted(unittest.TestCase):
    """Row 3 + new 7: the put-down came before the person read the first draft, and a
    revision held Out back for the brief's open items."""

    def test_journey(self):
        journey = read(REFS / "journey.md")
        self.assertIn("**A draft for review is done when it is accepted.** When the work is a draft "
                      "the person will review, the goal is met when they accept it, not when it is "
                      "first written", journey)
        self.assertIn("Items an accepted draft still marks to confirm (TO CONFIRM, a date to check, "
                      "an answer someone owes) don't hold the Out back: they become open work", journey)
        self.assertIn("never commit, uncommitted, “saved to git”, push, branch, remote or working tree",
                      journey)

    def test_skill(self):
        skill = read(SKILL)
        self.assertIn("A draft for the person's review is met when they accept it, not when first "
                      "written; its to-confirm items then become open work, never a reason to hold "
                      "the Out.", skill)
        self.assertIn("never commit, uncommitted, push, branch, remote or working tree", skill)


class OneQuestionPerAsk(unittest.TestCase):
    """New 4: "Is February 10, 2027 the right date, and should I put this down…?"."""

    def test_default_goes_under_unsure(self):
        journey = read(REFS / "journey.md")
        self.assertIn("**One question per ask.** A fact Conductor can default (the year of a date, a "
                      "file name) is stated under Unsure as the default it took, not bundled into the "
                      "put-down question.", journey)
        skill = read(SKILL)
        self.assertIn("One question per ask: a fact Conductor can default (a date's year) is stated "
                      "under Unsure as the default, never bundled into the put-down question.", skill)


class StaleHeaderLinesAreRewritten(unittest.TestCase):
    """Row 18: "Drafting the brief itself is not yet approved" and "ASKED, pending"
    stayed after he approved and answered; Out only appended a settled section."""

    def test_record_guide(self):
        record = read(REFS / "work-record.md")
        self.assertIn("rewrite in that same turn the record's position and header lines (stage, "
                      "current activity, pending question, next action, and any line saying "
                      "something is not yet approved) and every field marked pending or asked that "
                      "the answer resolves", record)
        self.assertIn("A “settled” note appended below while those lines still say otherwise leaves "
                      "the record stale.", record)

    def test_skill(self):
        skill = read(SKILL)
        self.assertIn("rewrite in that same turn the sketchbook's position and header lines (stage, "
                      "current activity, pending question, next action, any “not yet approved”) and "
                      "every field marked pending that the answer resolves", skill)


class SkillLimits(unittest.TestCase):
    def test_description_and_body_fit(self):
        text = SKILL.read_text(encoding="utf-8")
        description = re.search(r'^description: "(.*)"$', text, re.M).group(1)
        self.assertLessEqual(len(description), 1024)
        self.assertLessEqual(len(text.splitlines()), 500)


if __name__ == "__main__":
    unittest.main()
