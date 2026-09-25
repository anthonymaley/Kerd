"""Private working notes (work_notes): a public project's repo can stay public
while Conductor's sketchbooks move to a private vault repo. This pins the
conductor-side half of that fixed contract: the sketchbook paragraph and the
default record location both carry the `work_notes` conditional, without
losing the docs/work/ default they replace only when the key is set. This
checks presence of the wording, not that a model follows it.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
SKILL = REPO / "skills" / "conductor" / "SKILL.md"


def flat(text):
    return " ".join(text.split())


class PrivateNotesWordingTests(unittest.TestCase):
    def setUp(self):
        self.skill = SKILL.read_text(encoding="utf-8")
        self.prose = flat(self.skill)

    def test_sketchbook_paragraph_carries_the_conditional(self):
        sketchbook = self.skill.index("**Keep a sketchbook.**")
        conditional = self.skill.index("When `kivna/vault.json` carries")
        self.assertLess(sketchbook, conditional)
        for phrase in (
            "When `kivna/vault.json` carries `\"work_notes\": \"vault\"`, write the "
            "sketchbook (and its diagrams, evidence and drafts) to "
            "`<notes root>/<work>/work.md` instead of the repo, so a public project's "
            "working notes stay in the private vault repo; point to it as "
            "`notes:<work>/work.md`.",
            "Without that key, the sketchbook stays at "
            "`docs/work/<work>/work.md` and is committed with the project as today.",
        ):
            with self.subTest(phrase=phrase[:50]):
                self.assertIn(flat(phrase), self.prose)

    def test_record_agreement_section_carries_the_conditional(self):
        self.assertIn(
            flat(
                "Keep one readable record per work package, normally "
                "`docs/work/<short-work-name>/work.md`, or `notes:<short-work-name>/work.md` in "
                "the private vault repo when `kivna/vault.json` sets `work_notes`; use a "
                "suitable existing location instead when the project already has one."
            ),
            self.prose,
        )

    def test_docs_work_default_still_stands_without_the_key(self):
        # The pre-existing default location is still stated plainly, not replaced.
        self.assertIn("docs/work/<short-work-name>/work.md", self.skill)
        self.assertIn("docs/work/<work>/work.md", self.skill)


if __name__ == "__main__":
    unittest.main()
