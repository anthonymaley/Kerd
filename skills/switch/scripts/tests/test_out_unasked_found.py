"""An unasked Out opens with what changed and names itself before any save question.

First-user round 6 (`h21`) and the leftovers reruns (k2, k3, 2026-11-22): after a revision,
Out started unasked in the same turn, as Conductor's finish asks, but went straight to its
save question with no Found line and never named `/kerd:switch out`, in 3 of 3 runs.
Conductor's finish carries the rule; once Out's guide loads, the reply is composed from
out.md, so the step sits near the top of Out there too. This checks the words and their
order, not that a model follows them.
"""
from pathlib import Path
import unittest

OUT = Path(__file__).resolve().parents[2] / "references" / "out.md"


def flat(text):
    return " ".join(text.split())


class UnaskedOutOpensWithFound(unittest.TestCase):
    def setUp(self):
        self.text = flat(OUT.read_text(encoding="utf-8"))

    def test_step_present_in_order(self):
        start = self.text.index("**Started unasked after a change.**")
        rule = self.text[start:start + 700]
        found = rule.index("opens with a short Found line")
        names = rule.index("`/kerd:switch out`")
        question = rule.index("only then any save question")
        self.assertLess(found, names)
        self.assertLess(names, question)

    def test_step_sits_in_the_out_section_before_the_save_question(self):
        section = self.text.index("## Out ")
        step = self.text.index("**Started unasked after a change.**")
        save_question = self.text.index("name each one to the person in one question")
        self.assertLess(section, step)
        self.assertLess(step, save_question)


if __name__ == "__main__":
    unittest.main()
