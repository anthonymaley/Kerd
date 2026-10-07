"""Switch's SKILL.md opens by sending the model to the action's guide first.
Haiku evals on 2026-10-07 (0.175.3): 0 of 18 runs opened the guide, In scored
~0.6 and Out ~0.2, and Out once closed without saving. With this line on a
scratch copy: 18 of 18 read the guide, In 1.00 (8 of 9), Out 0.67-0.81. This
checks presence and position of the wording, not that a model follows it.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / "skills/switch/SKILL.md"


class ReadGuideFirstTests(unittest.TestCase):
    def test_first_instruction_names_each_guide(self):
        text = " ".join(SKILL.read_text(encoding="utf-8").split())
        self.assertIn("**First, before any other tool call:** read this skill's guide for the named "
                      "action", text)
        self.assertIn("for In, `references/in.md` in full; for Out, `references/out.md` in full;", text)

    def test_host_neutral_reader(self):
        # codex-tui 2026-10-07: the Codex package copies this line and has no Read tool.
        text = " ".join(SKILL.read_text(encoding="utf-8").split())
        self.assertIn("with the host's file reader (the Read tool in Claude Code)", text)
        self.assertNotIn("use the Read tool on this skill's guide", text)

    def test_to_and_roll_keep_section_routing(self):
        # codex-tui 2026-10-07: to-roll.md stops everyday To before managed detail.
        text = " ".join(SKILL.read_text(encoding="utf-8").split())
        self.assertIn("for To or Roll, `references/to-roll.md` from its contents, then only the "
                      "sections it routes that action to.", text)
        self.assertIn("Run every command in the person's project, never in this skill's directory.", text)

    def test_it_comes_before_everything_else_in_the_body(self):
        body = SKILL.read_text(encoding="utf-8").split("\n# Switch\n", 1)[1]
        self.assertTrue(body.lstrip().startswith("**First, before any other tool call:**"))

    def test_named_guides_exist(self):
        for rel in ("in.md", "out.md", "to-roll.md"):
            self.assertTrue((SKILL.parent / "references" / rel).is_file(), rel)


if __name__ == "__main__":
    unittest.main()
