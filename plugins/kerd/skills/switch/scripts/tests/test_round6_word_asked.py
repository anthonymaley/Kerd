"""Never deny Kerd's own words; Out's progress lines keep push and remote out.

First-user round 6 (a simulated first-user walkthrough, Proposal 3): asked about a push, a
fresh session said "I didn't say anything about a push earlier", though sitting 1's
in-between line had said "without a push since there's nowhere to push to". A fresh
session cannot see what an earlier one said, so it must not claim either way. Switch
and Conductor carry the rule beside the question form; Out's in-between lines rule
names the words narration never uses. These check the words, not that a model
follows them.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / "skills"

RULE = ("Asked about a word, explain it plainly and answer the worry behind it. Never say Kerd "
        "did or did not use it: a fresh session cannot see what an earlier one said.")
# Round 6 leftover 4 (h22, 2026-11-21): "The saved place also isn't on any other device yet"
# reached the person; Kerd's record words stay in the records.
RECORD_WORDS = ("Kerd's own record words (“the saved place”, “handoff”) stay in the records: to the "
                "person, say what they mean (“your notes, saved on this computer”).")
NARRATION = ("narration never says push, pushed, remote or “nowhere to push to”, only what it "
             "means for their files (“saved on this computer”)")


def flat(text):
    return " ".join(text.split())


class NeverDenyKerdsOwnWords(unittest.TestCase):
    def test_switch_and_conductor_carry_it_beside_the_question_form(self):
        for skill in ("switch", "conductor"):
            with self.subTest(skill=skill):
                text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertEqual(flat(text).count(RULE), 1)
                paragraphs = [p for p in text.split("\n\n") if p.strip()]
                asking = next(i for i, p in enumerate(paragraphs)
                              if p.startswith("**Asking the person:**"))
                self.assertTrue(flat(paragraphs[asking + 1]).startswith(RULE))
                self.assertIn(RECORD_WORDS, flat(paragraphs[asking + 1]))
                body = text.split("\n---\n", 1)[1]
                self.assertLess(body.index(RULE), body.index("\n## "))


class OutProgressLinesKeepGitWordsOut(unittest.TestCase):
    def test_out_names_the_words_narration_never_uses(self):
        text = flat((SKILLS / "switch" / "references" / "out.md").read_text(encoding="utf-8"))
        self.assertEqual(text.count(NARRATION), 1)
        # It belongs to the in-between lines rule, right after its example.
        self.assertIn("That includes the short progress lines between steps, which the person sees "
                      "too (“checking what's saved”, not “whether there's a remote”): " + NARRATION,
                      text)


if __name__ == "__main__":
    unittest.main()
