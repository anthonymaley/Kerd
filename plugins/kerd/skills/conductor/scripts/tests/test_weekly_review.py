"""Guards the weekly review reference agreed with Anthony on 2026-11-03.

The review looks back over the current project's own week through five lenses,
raises missed decisions once without nagging, writes a dated record Switch In reads,
and turns repeated jobs into skills with Anthropic's skill-creator on the person's go.
Kivna's intake no longer points at Conductor's retired pre-flight inventory. This
checks that the wording is present, not that a model follows it.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
REVIEW = REPO / "skills" / "conductor" / "references" / "weekly-review.md"
KIVNA = REPO / "skills" / "kivna" / "SKILL.md"


def flat(path):
    return " ".join(path.read_text(encoding="utf-8").split())


class WeeklyReviewTests(unittest.TestCase):
    def setUp(self):
        self.text = flat(REVIEW)

    def test_contents_lists_every_section(self):
        for anchor in (
            "#the-weekly-review",
            "#five-lenses",
            "#missed-decisions-without-nagging",
            "#the-review-record",
            "#make-this-a-skill-in-the-moment",
            "#pasted-notes-that-hold-decisions",
        ):
            with self.subTest(anchor=anchor):
                self.assertIn(f"]({anchor})", self.text)

    def test_why_cites_the_source_without_new_figures(self):
        self.assertIn("“How employment is changing at Anthropic” (2026-10-16)", self.text)
        self.assertIn("human attention is the bottleneck", self.text)
        self.assertIn("rose from 10% to 22%", self.text)
        self.assertNotIn("roughly doubled", self.text)

    def test_the_review_reads_its_own_project_in_the_window_and_writes_nothing_first(self):
        for phrase in (
            "last 7 days, or the window the person names",
            "`kivna/sessions/`",
            "`~/.claude/projects/<project-dir>/*.jsonl`",
            "its Codex history where it exists",
            "The folder name is only a candidate",
            "Choose files from their metadata first, before any chat content is read",
            "canonical absolute path",
            "take only the events whose own timestamps fall inside the window",
            "The review writes nothing until the person says go.",
            "**Found**, **Needs you** and **Unsure**",
            "ranks items by the time each would save the person",
            "At most five items are on screen",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_five_lenses(self):
        for lens in (
            "**Corrections.**",
            "**Repeated jobs.**",
            "**Questions.**",
            "**Unsure items.**",
            "**Missed decisions.**",
        ):
            with self.subTest(lens=lens):
                self.assertIn(lens, self.text)
        self.assertIn("give the exact wording to add", self.text)
        self.assertIn("could the person answer it cold?", self.text)

    def test_missed_decisions_never_nag(self):
        for phrase in (
            "Only a decision whose subject is still live in open work survives.",
            "is dropped without being raised",
            "Survivors appear as one grouped list",
            "> 💬 **Are these settled?**",
            "shown as a before → after edit",
            "**Solved or drop:** never raised again.",
            "**Skipped:** stays as it is and is not asked again.",
            "decision ledger in the review folder",
            "checks the ledger and leaves out anything already there",
            "the no-repeat promise cannot hold without it",
            "reviewed-through time",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_the_record_paths_and_date(self):
        self.assertIn("`notes:weekly-review/<YYYY-MM-DD>.md`", self.text)
        self.assertIn("`docs/work/weekly-review/<YYYY-MM-DD>.md`", self.text)
        self.assertIn("Its date is what Switch In reads", self.text)
        self.assertIn("Writing this record after the person's go is part of the review", self.text)

    def test_make_this_a_skill_uses_skill_creator_light(self):
        for phrase in (
            "Anthropic's skill-creator",
            "asking for its light path: no full eval or benchmark loop unless the person asks",
            "a script only for deterministic work",
            "how to run it, and what to check after each run",
            "A host without skill-creator: say so",
            "built only on the person's go",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)

    def test_pasted_notes_get_the_list_at_once(self):
        self.assertIn("at once, rather than waiting for the week", self.text)


class KivnaIntakeTests(unittest.TestCase):
    def test_intake_stands_without_the_retired_pre_flight_inventory(self):
        text = flat(KIVNA)
        self.assertNotIn("pre-flight inventory", text)
        self.assertIn("ask everything in one round (≤5 prompts). Show the prompts as labelled fields", text)


if __name__ == "__main__":
    unittest.main()
