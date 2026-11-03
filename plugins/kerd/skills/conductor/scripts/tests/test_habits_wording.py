"""Guards the habits agreed on 2026-11-03 in Conductor's own files.

Ready lists every open gap at once with its default, inside the go's decision block;
a concert stops only for what costs money or cannot be undone, and takes a free,
reversible default for a gap nobody foresaw, listing it under Unsure; SKILL.md points
at the weekly-review guide for "make this a skill", pasted decision notes and the
weekly review. Wording only: whether a session follows it shows in real use.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
CONDUCTOR = REPO / "skills" / "conductor"
SKILL = CONDUCTOR / "SKILL.md"
ENTRY = CONDUCTOR / "references" / "entry.md"
WEEKLY_LINK = "[weekly review](references/weekly-review.md)"


def flat(text):
    """Whitespace-normalized text, so a rewrap of the prose is not a rule change."""
    return " ".join(text.split())


class ReadyListsEveryGapTests(unittest.TestCase):
    def test_entry_lists_every_gap_with_its_default(self):
        entry = flat(ENTRY.read_text(encoding="utf-8"))
        for phrase in (
            "**At Ready, every gap still open is listed at once**, one line each with the default Conductor will use",
            "The person reads the list once, overrides any default they want changed, and the concert then runs without stopping to ask.",
            "Questions during rehearsal still come one at a time; only the gaps left at Ready come together.",
            "means we are not ready yet; say so and name it",
            "That decision block carries the open-gap list with its defaults, so the one bubble approves the go with those defaults",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, entry)
        self.assertNotIn("name the one or two things still needed", entry)

    def test_skill_carries_the_ready_list(self):
        skill = flat(SKILL.read_text(encoding="utf-8"))
        self.assertIn("At Ready, list every gap still open at once, one line each with the default Conductor will use", skill)
        self.assertIn("Rehearsal questions still come one at a time.", skill)
        self.assertIn("That decision block carries the open gaps with their defaults, so the one bubble approves the go with those defaults", skill)
        self.assertNotIn("one or two things still needed", skill)


class ConcertStopRuleTests(unittest.TestCase):
    def test_entry_states_the_stop_rule(self):
        entry = flat(ENTRY.read_text(encoding="utf-8"))
        for phrase in (
            "**What stops a concert.**",
            "what costs money (a paid job, a purchase, going past an allowance), what cannot be undone or goes outward (a push, a merge, a release, an install, a deletion, anything sent to someone), and what falls outside the agreed authority or outcome",
            "That works because Ready already filled the gaps.",
            "takes a default only when that default stays within the agreed authority, keeps the agreed outcome, costs nothing, can be undone and stays inside the work (nothing pushed, released, installed, deleted or sent to anyone)",
            "list it under **Unsure** in the next report, so the person can reverse it at the finish.",
            "Any other gap stops that passage only, while the other passages carry on, and comes back to the person as **Needs you** for that one point, not to the start.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, entry)
        self.assertNotIn("A gap the score cannot answer stops that passage", entry)

    def test_skill_states_the_stop_rule(self):
        skill = flat(SKILL.read_text(encoding="utf-8"))
        self.assertIn("In a concert, Needs you is only what costs money", skill)
        self.assertIn("or falls outside the agreed authority or outcome; Ready already filled the rest", skill)
        self.assertIn("takes a default only when it stays within the agreed authority, keeps the agreed outcome, costs nothing, can be undone and stays inside the work", skill)
        self.assertIn("listed under Unsure in the next report, so the person can reverse it at the finish", skill)
        self.assertIn("Any other gap stops that passage only, other passages carrying on", skill)
        self.assertIn("ends on one of the quiet endings (agreed completion, a pause the person asked for, Switch Out's closing box)", skill)
        self.assertNotIn("A gap the score cannot answer stops that passage", skill)


class ReportShapeInSkillTests(unittest.TestCase):
    def test_skill_names_the_three_lines(self):
        skill = flat(SKILL.read_text(encoding="utf-8"))
        for phrase in ("**Found:**", "**Needs you:**", "**Unsure:**",
                       "a check of the three lines and the last line before sending",
                       "When Needs you names a decision, the turn ends on a bubble asking exactly that"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)
        self.assertNotIn("first-line-and-last-line", skill)


class WeeklyReviewPointerTests(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text(encoding="utf-8")
        self.skill = flat(self.text)

    def test_must_hold_points_at_the_weekly_review_guide(self):
        must_hold = self.text[self.text.index("## Must hold"):self.text.index("## Open this guide when")]
        self.assertGreaterEqual(must_hold.count(WEEKLY_LINK), 3)

    def test_make_this_a_skill(self):
        for phrase in (
            "“Make this a skill”, said in the moment, is ordinary Conductor work.",
            "in the person's own project with Anthropic's skill-creator on its light path (no full eval or benchmark loop unless the person wants one)",
            "add a two-line note: how to run it, and what to check after each run",
            "On a host without skill-creator, say so and follow Anthropic's published skill guidance",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.skill)

    def test_pasted_decision_notes(self):
        for phrase in (
            "Pasted notes the person says hold decisions become one grouped list, asked once",
            "settled, as a before → after edit into the record it belongs in",
            "or dropped and never raised again",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.skill)

    def test_weekly_review_route(self):
        for phrase in (
            "The weekly review is a Conductor route Switch In offers when the project's last review is over 7 days old.",
            "five lenses (corrections, repeated jobs, questions, unsure items, missed decisions)",
            "writes nothing without the person's go",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.skill)

    def test_open_this_guide_when_lists_it(self):
        guides = self.text[self.text.index("## Open this guide when"):]
        self.assertIn("- [Weekly review](references/weekly-review.md):", guides)

    def test_description_names_the_triggers(self):
        description = self.text.split("\n")[2]
        self.assertTrue(description.startswith("description: "))
        value = description[len("description: "):].strip('"')
        self.assertIn("“make this a skill”", value)
        self.assertIn("weekly review", value)
        self.assertLessEqual(len(value), 1024)
        self.assertNotIn("<", value)
        self.assertNotIn(">", value)


if __name__ == "__main__":
    unittest.main()
