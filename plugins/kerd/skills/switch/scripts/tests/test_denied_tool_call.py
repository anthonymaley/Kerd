"""A denied tool call is the person's decision: never offered another route.

First-user round 6 (a simulated first-user walkthrough, new finding 2, probe `09`): with the
Read of `references/in.md` denied, Switch In ended "Should I read the guide through Bash
instead, or will you grant read access to that folder?", offering a way around the
refusal in an X-or-Y question. Round 5 and probe `31` stopped correctly, so the wording
varied across runs. Each skill whose SKILL.md sends the model to a guide carries the
rule in its body, which loads before the guide. This checks presence and position of
the wording, not that a model follows it. Anthony's agreed choice (2026-11-21): keep the
open question and add one sentence on how to approve the read next time, never
"permission settings".
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]
SKILLS = ROOT / "skills"
GUIDE_FIRST = ("switch", "conductor", "agent", "visuals")
RULE = (
    "**When a tool call is denied:** the denial is the person's decision, a denied read of this "
    "skill's guide included. Never offer or use another tool, a shell command or any other route "
    "to get the same thing; a denied file read is not retried through the shell. Stop, say plainly "
    "what was refused and what that means for the step (without its guide, the step cannot run), "
    "say in one sentence how to approve it next time, naming the command that runs the step "
    "(for Switch In: “Run `/kerd:switch in` again and choose to allow the read when Claude Code "
    "asks.”), never pointing to permission settings, "
    "and ask one open question about how they want to go on (“How would you like to go on?”), "
    "as one speech-bubble line, never “X, or Y?”."
)


def flat(text):
    """Whitespace-normalized text, so a rewrap of the prose is not a rule change."""
    return " ".join(text.split())


class DeniedToolCallTests(unittest.TestCase):
    def test_each_guide_first_skill_carries_the_rule_once(self):
        for skill in GUIDE_FIRST:
            with self.subTest(skill=skill):
                text = flat((SKILLS / skill / "SKILL.md").read_text(encoding="utf-8"))
                self.assertEqual(text.count(flat(RULE)), 1)

    def test_every_skill_with_a_guide_folder_is_covered(self):
        with_guides = sorted(p.parent.name for p in SKILLS.glob("*/references") if p.is_dir())
        self.assertEqual(with_guides, sorted(GUIDE_FIRST))

    def test_rule_is_in_the_body_before_any_section(self):
        # The body loads before the guide; a rule after the first heading could be
        # skimmed past on the way to the guide read it governs.
        for skill in GUIDE_FIRST:
            with self.subTest(skill=skill):
                text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
                body = text.split("\n---\n", 1)[1]
                first_section = body.find("\n## ")
                self.assertGreater(first_section, 0)
                self.assertIn("**When a tool call is denied:**", body[:first_section])

    def test_switch_puts_it_straight_after_the_guide_read(self):
        text = (SKILLS / "switch" / "SKILL.md").read_text(encoding="utf-8")
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        first = next(i for i, p in enumerate(paragraphs)
                     if p.startswith("**First, before any other tool call:**"))
        self.assertTrue(paragraphs[first + 1].startswith("**When a tool call is denied:**"))

    def test_the_round_6_offer_does_not_come_back(self):
        for path in sorted(SKILLS.glob("*/SKILL.md")):
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("through Bash instead", text)
                self.assertNotIn("read it another way", text)
                # Round 6, probe 09: "Allow reads on … in your permission settings", which a
                # newcomer can't do; the rule names the prompt Claude Code shows instead.
                self.assertNotIn("in your permission settings", text)

    def test_how_to_approve_next_time_comes_before_the_question(self):
        # Agreed open choice (2026-11-21): keep the open question, add one sentence on
        # approving next time, said before the bubble so the question stays last.
        rule = flat(RULE)
        self.assertLess(rule.index("how to approve it next time"), rule.index("ask one open question"))
        self.assertIn("when Claude Code asks", rule)

    def test_how_to_approve_names_the_command(self):
        # Round 6 leftover 3 (probe g09a/b, 2026-11-21): "run the step again" left a
        # newcomer without the command to type.
        self.assertIn("naming the command that runs the step", flat(RULE))
        self.assertIn("`/kerd:switch in` again", flat(RULE))


if __name__ == "__main__":
    unittest.main()
