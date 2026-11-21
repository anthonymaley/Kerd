"""A finished revision of delivered work ends in Switch Out, in the same turn.

First-user round 6 (batch-1114, first-user-6.md, Proposal 2; sitting-2 reruns
2026-11-21): 0 of 4 revisions of an accepted brief ran Out; two ended with no
question, two asked "Put this down for today…?" though Claude Code can start Out.
A handoff saying "Edit launch-brief.md only" also kept Kerd's records out. The rule
is pinned in Conductor's Finish and in journey.md's One clear finish; the eval case
is evals/conductor-revision-out. These check the words, not that a model follows them.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
CONDUCTOR = REPO / "skills" / "conductor"

RULE = (
    "A requested change to delivered work is finished when the change is made and shown; then, "
    "while these conditions hold (nothing else outstanding, remaining authorized work first, a "
    "draft not yet accepted waits for acceptance, a request to keep the session open holds, this "
    "session owns the Out), run `/kerd:switch out` in that same turn after a short Found line, "
    "unasked. A handoff that limits which files the work edits never limits Out, and Out keeps its "
    "own save authority: it still asks before saving the person's own files."
)
# Codex review of 45636539..9e111bc0 (High): the sentence read as overriding the rules
# around it. Each condition it stays subject to is named in it.
CONDITIONS = (
    "nothing else outstanding", "remaining authorized work first",
    "a draft not yet accepted waits for acceptance", "a request to keep the session open holds",
    "this session owns the Out", "Out keeps its own save authority",
    "it still asks before saving the person's own files",
)
FALLBACK = "`> 💬 **Put this down for today with /kerd:switch out?**`"


def flat(text):
    return " ".join(text.split())


def section(text, start, end):
    return flat(text[text.index(start):text.index(end)])


class RevisionEndsInOut(unittest.TestCase):
    def test_finish_carries_it_once(self):
        text = (CONDUCTOR / "SKILL.md").read_text(encoding="utf-8")
        finish = section(text, "### Finish", "### Skills, notes and the weekly review")
        self.assertEqual(finish.count(RULE), 1)
        self.assertEqual(flat(text).count(RULE), 1)

    def test_one_clear_finish_carries_it_once(self):
        text = (CONDUCTOR / "references" / "journey.md").read_text(encoding="utf-8")
        finish = section(text, "### One clear finish", "**A draft for review is done when it is accepted.**")
        self.assertEqual(finish.count(RULE), 1)
        self.assertEqual(flat(text).count(RULE), 1)

    def test_it_stays_subject_to_the_surrounding_conditions(self):
        for condition in CONDITIONS:
            with self.subTest(condition=condition):
                self.assertIn(condition, RULE)
        # The unasked Out comes only after the conditions, never before them.
        self.assertLess(RULE.index("while these conditions hold"), RULE.index("run `/kerd:switch out`"))

    def test_put_down_question_stays_only_for_hosts_without_a_skill_start(self):
        skill = flat((CONDUCTOR / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual(skill.count(FALLBACK), 1)
        before = skill[:skill.index(FALLBACK)]
        self.assertTrue(before.rstrip().endswith("Where the host gives no way to start the skill, the turn "
                                        "ends on the one question"))
        # The new rule comes before the fallback, so the run-it-yourself case is read first.
        self.assertLess(skill.index(RULE), skill.index(FALLBACK))


if __name__ == "__main__":
    unittest.main()
