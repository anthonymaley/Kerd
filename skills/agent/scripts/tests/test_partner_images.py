"""Guards the image-by-path instruction added to Agent in 0.143.0.

A user reported that asking Claude to show mockups to their Codex partner sent them
to a fresh Codex with no project context instead: Agent's route could not attach an
image and said nothing about what to do. A real run showed `codex queue` refuses
attachments while a partner given the file's path opens it itself. SKILL.md now says
so beside the contribution step, and native-sessions.md carries the evidence and its
limits. This checks presence of the wording, not that a model follows it.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
AGENT = REPO / "skills" / "agent"
SKILL = AGENT / "SKILL.md"
NATIVE = AGENT / "references" / "native-sessions.md"


def flat(text):
    """Whitespace-normalized text, so a rewrap of the prose is not a rule change."""
    return " ".join(text.split())


class PartnerImageTests(unittest.TestCase):
    def setUp(self):
        self.skill = flat(SKILL.read_text(encoding="utf-8"))
        self.native = flat(NATIVE.read_text(encoding="utf-8"))

    def test_the_instruction_sends_the_path_and_keeps_the_partner(self):
        for phrase in (
            "To show a partner an image",
            "put the file's absolute path in the request text and ask the partner "
            "to open and look at it",
            "Do not try to attach it: `codex queue` refuses image attachments",
            "is a different contributor, not the partner, so use one only when the "
            "person chooses it",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.skill)

    def test_the_instruction_sits_in_the_contribution_step(self):
        step4 = self.skill.index("4. Prepare the contribution")
        rule = self.skill.index("To show a partner an image")
        step5 = self.skill.index("5. Read [native sessions]")
        self.assertLess(step4, rule)
        self.assertLess(rule, step5)

    def test_the_evidence_and_its_limits_are_recorded(self):
        self.assertIn("## Images", NATIVE.read_text(encoding="utf-8"))
        for phrase in (
            "codex queue does not support image attachments",
            "A **Claude** partner receiving an image path has not been tested",
            "it is not the partner, and the person chooses it",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.native)


if __name__ == "__main__":
    unittest.main()
