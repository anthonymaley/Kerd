"""Guards the shape of Conductor's reports: three opening lines, then five items.

Every report opens with Found, Needs you and Unsure (agreed 2026-11-03), replacing
the earlier result-first, position-second pair; where the work stands folds into Found.

A correction of Conductor's own earlier claim is part of the result, not a sixth item.

Conductor's presentation guide states the six rules a report of work follows, shows
one report from real use that fails them and the same report in shape, and keeps the
two guards that stop the shape costing anything: the display cap never limits what is
read, checked or recorded, and a limit or failed check still appears. SKILL.md points
at the section, and the finish format defers to it. This checks that the wording and
its anchors are present, not that a model follows them; only a real sitting or an
independent reader shows that.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
CONDUCTOR = REPO / "skills" / "conductor"
JOURNEY = CONDUCTOR / "references" / "journey.md"
SKILL = CONDUCTOR / "SKILL.md"
ANCHOR = "the-shape-of-every-report"


def flat(text):
    """Whitespace-normalized text, so a rewrap of the prose is not a rule change."""
    return " ".join(text.split())


class ReportShapeTests(unittest.TestCase):
    def setUp(self):
        self.journey = JOURNEY.read_text(encoding="utf-8")
        self.prose = flat(self.journey)

    def section(self):
        start = self.journey.index("### The shape of every report")
        end = self.journey.index("### Keep the tasks visible while the work unfolds")
        self.assertLess(start, end)
        return flat(self.journey[start:end])

    def test_the_section_states_all_six_rules(self):
        section = self.section()
        for rule in (
            "Three labelled lines open every report.",
            "**Found:** what was found or decided, or what the person has now and where to look at it",
            "**Needs you:** the decision or approval needed from the person, or \u201cnothing\u201d.",
            "**Unsure:** what Conductor was not sure about in this result, in one line",
            "The ending follows Needs you.",
            "At most five items on screen.",
            "One thing at a time.",
            "A correction of your own earlier claim never competes for those five.",
            "Before sending, read only the three lines and the last line.",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, section)

    def test_a_single_job_restates_where_it_stands(self):
        """The position line was missing in 10 of 10 runs (unattended-sweep evidence,
        report-shape.md); it now folds into Found and is still restated every time."""
        section = self.section()
        self.assertIn(
            "A single job restates it too: \u201cDone and committed locally, not pushed; "
            "next: the output options.\u201d",
            section,
        )
        self.assertIn("with where the work stands folded in", section)
        self.assertNotIn("Second line: where the work stands", section)
        self.assertNotIn("read only the first line and the last line", section)

    def test_tidying_the_finished_item_is_not_the_next_item(self):
        """Two of two finishes offered to tidy the finished item (report-shape.md, proposal 2)."""
        finish = flat(self.journey[self.journey.index("### One clear finish"):])
        self.assertIn(
            "Tidying the record of the item just finished is not the next item.",
            finish.split("Avoid a report of internal instruction-following", 1)[0],
        )

    def test_the_section_comes_before_the_delivery_formats_it_governs(self):
        shape = self.journey.index("### The shape of every report")
        for later in (
            "#### Delegation grid and preparation updates",
            "### One clear finish",
        ):
            with self.subTest(later=later):
                self.assertLess(shape, self.journey.index(later))

    def test_the_display_cap_never_limits_what_is_kept(self):
        section = self.section()
        self.assertIn(
            "This shapes what is displayed, never what is read, checked or recorded",
            section,
        )
        self.assertIn("nothing is dropped", section)

    def test_shape_does_not_license_hiding_a_limit_or_a_blocker(self):
        section = self.section()
        self.assertIn("This governs the shape of reports, not their honesty.", section)
        self.assertIn(
            "A problem that blocks the work or risks harm is not a side finding; "
            "it goes in the three lines. It joins Found and does not replace it",
            section,
        )

    def test_a_failing_and_a_passing_report_are_both_shown(self):
        section = self.section()
        self.assertIn("A report that fails this, from real use:", section)
        self.assertIn("The same return, in shape:", section)
        # The passing example itself leads with the result, not the grid.
        passing = self.journey[self.journey.index("The same return, in shape:"):]
        body = passing.split("```markdown", 1)[1].split("```", 1)[0].strip()
        lines = body.splitlines()
        self.assertTrue(lines[0].startswith("**Found:** the README is rebuilt"))
        self.assertIn("**Needs you:** nothing.", body)
        self.assertIn("**Unsure:**", body)
        self.assertLess(body.index("**Found:**"), body.index("**Needs you:**"))
        self.assertLess(body.index("**Needs you:**"), body.index("**Unsure:**"))
        self.assertNotIn("| Task |", body)

    def test_a_decision_in_needs_you_is_the_bubble(self):
        section = self.section()
        self.assertIn(
            "When Needs you names a decision, the turn ends on a bubble asking exactly "
            "what Needs you says, using only terms that already appear in the three lines",
            section,
        )
        self.assertIn(
            "When Needs you is \u201cnothing\u201d, the turn does not stop there: it keeps "
            "working, ends on a named wait for the job",
            section,
        )
        self.assertIn("Never invent work or a wait to fill it.", section)
        example = self.journey[self.journey.index("When it names\na decision"):]
        body = example.split("```markdown", 1)[1].split("```", 1)[0]
        self.assertIn("**Needs you:** approve merging `concert/export-fix` into main and pushing.", body)
        self.assertTrue(body.strip().splitlines()[-1].startswith(
            "> \U0001f4ac **Merge `concert/export-fix` into main and push \u2014 approve?**"))

    def test_skill_and_finish_point_at_the_section(self):
        self.assertIn(f"references/journey.md#{ANCHOR}", SKILL.read_text(encoding="utf-8"))
        finish = self.journey[self.journey.index("### One clear finish"):]
        self.assertIn(f"(#{ANCHOR})", finish[:400])


if __name__ == "__main__":
    unittest.main()
