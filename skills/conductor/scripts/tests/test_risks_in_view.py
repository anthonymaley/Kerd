"""Guards the short risks list that replaced the retired risk ledger (0.142.0).

Conductor keeps risks in the sketchbook instead of a ledger: the rule sits beside
the sketchbook paragraph in SKILL.md and carries its three obligations (write the
risk down, read the list back before Ready and before the goal check, never invent
a risk to fill it), and the work record describes the matching section. The same
release removed the step check, so SKILL.md must no longer carry its heading or the
gate command. This checks presence of the wording, not that a model follows it.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
CONDUCTOR = REPO / "skills" / "conductor"
SKILL = CONDUCTOR / "SKILL.md"
RECORD = CONDUCTOR / "references" / "work-record.md"


def flat(text):
    """Whitespace-normalized text, so a rewrap of the prose is not a rule change."""
    return " ".join(text.split())


class RisksInViewTests(unittest.TestCase):
    def setUp(self):
        self.skill = SKILL.read_text(encoding="utf-8")
        self.prose = flat(self.skill)

    def test_the_rule_sits_in_rehearsal_beside_the_sketchbook(self):
        self.assertIn("**Keep the risks in view.**", self.skill)
        rehearsal = self.skill.index("## Rehearsal, then the concert")
        sketchbook = self.skill.index("**Keep a sketchbook.**")
        risks = self.skill.index("**Keep the risks in view.**")
        score = self.skill.index("**The score is written as you go.**")
        self.assertLess(rehearsal, sketchbook)
        self.assertLess(sketchbook, risks)
        self.assertLess(risks, score)

    def test_the_rule_carries_its_three_obligations(self):
        for phrase in (
            # Write it down, in the sketchbook, with its treatment or acceptance.
            "write it in the sketchbook's short risks list: the risk in one plain "
            "sentence, and what is being done about it or that it is accepted as "
            "it stands",
            # Both read-back moments, and the open-risk answer they have to produce.
            "Read the list back before saying Ready and before the goal check, and "
            "say which risks are still open",
            # The empty list is allowed, so nothing is manufactured to fill it.
            "An empty list is fine; never invent risks to fill it",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(flat(phrase), self.prose)

    def test_it_is_not_a_ledger(self):
        self.assertIn("No sizing, columns or tiers", self.prose)

    def test_rehearsal_holds_the_risks_worth_keeping_in_view(self):
        self.assertIn(
            flat("the goals, the constraints, the design, and the risks worth "
                 "keeping in view"),
            self.prose,
        )

    def test_the_work_record_describes_the_section(self):
        record = RECORD.read_text(encoding="utf-8")
        prose = flat(record)
        self.assertIn("## Risks to keep in view", record)
        for phrase in (
            # One line per risk, its treatment or acceptance, and when it was named.
            "One line per risk: the risk in a plain sentence, what is being done "
            "about it or \"accepted\", and the date it was named",
            # Stated plainly, because the retired ledger did gate things.
            "it is not a ledger and it gates nothing",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(flat(phrase), prose)

    def test_the_step_check_is_gone(self):
        self.assertNotIn("Check where the work stands", self.skill)
        self.assertNotIn("gate.py", self.skill)


if __name__ == "__main__":
    unittest.main()
