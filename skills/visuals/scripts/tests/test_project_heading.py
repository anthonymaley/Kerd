"""Guards the Visuals rule that the project leads a render's top heading.

Anthony, 2026-09-26 09:09, on a diagram that named only its subject: the project
"needs to be top heading: 'KERD: Invoice export · proposal from notes.md · not
built'". This checks the written rule, not whether a model follows it.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
SKILL = REPO / "skills" / "visuals" / "SKILL.md"
GUIDE = REPO / "docs" / "guide" / "visuals.md"


def flat(text):
    return " ".join(text.split())


class ProjectHeadingTests(unittest.TestCase):
    def test_the_rule_puts_the_project_first_in_the_top_heading(self):
        prose = flat(SKILL.read_text(encoding="utf-8"))
        for phrase in (
            "as the first words of the top heading",
            "the first line of text in the render, whatever the tool calls it (eyebrow, kicker, title): "
            "the name in capitals and a colon",
            "`KERD: Invoice export · proposal from notes.md · not built`",
            "A name elsewhere in the picture does not satisfy this",
            "Where a template supplies an eyebrow naming the diagram type or status, replace it with "
            "this line; a colon, not a dot, follows the name",
            "the project leading the top heading",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(flat(phrase), prose)

    def test_the_old_anywhere_placement_does_not_return(self):
        prose = flat(SKILL.read_text(encoding="utf-8"))
        self.assertNotIn("in the title or a small identity label", prose)

    def test_the_starter_the_skill_points_to_leads_with_the_project(self):
        """The starter is copied; it must model the heading, so it has no exemption."""
        starter = (SKILL.parent / "assets" / "review-flow.html").read_text(encoding="utf-8")
        self.assertIn('<p class="eyebrow">KERD: ', starter)
        self.assertNotIn("sole exception", flat(SKILL.read_text(encoding="utf-8")))

    def test_the_guide_says_the_same(self):
        prose = flat(GUIDE.read_text(encoding="utf-8"))
        self.assertIn("leads the render's top heading, in capitals with a colon", prose)


    def test_states_differ_in_more_than_one_way(self):
        """Anthony, 2026-09-26 09:17: grey dashed and green dashed "look the same"."""
        prose = flat(SKILL.read_text(encoding="utf-8"))
        for phrase in (
            "what exists today in a solid outline, what is proposed in a dashed outline, and the "
            "change the view is about on plain paper with a solid accent border, heavier than the rest",
            "Two states that differ only by colour, or only by dash, read as the same thing at a glance",
            "states that look different at a glance",
            "Every box takes its state, including a result that exists only once the change ships: "
            "that result is proposed, so it is dashed",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(flat(phrase), prose)


if __name__ == "__main__":
    unittest.main()
