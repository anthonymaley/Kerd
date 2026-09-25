"""The chat roll (0.154.0) is named where earlier text said the outer chat could not be
replaced, so the old refusals and the new route do not contradict each other."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]


def read(rel):
    return " ".join((ROOT / rel).read_text(encoding="utf-8").split())


class ChatRollWordingTests(unittest.TestCase):
    def test_old_refusals_are_gone(self):
        self.assertNotIn("It does not implement automatic replacement of the outer Conductor chat",
                         read("skills/switch/references/to-roll.md"))
        self.assertNotIn("not pressure-aware Claude coordination or automatic replacement of its TUI",
                         read("skills/conductor/references/managed-conductor.md"))

    def test_each_rule_names_the_chat_roll_exception(self):
        for rel, fragment in (
            ("skills/switch/references/to-roll.md", "### Roll the Conductor chat (tmux)"),
            ("skills/switch/references/to-roll.md", "Nothing is typed into Claude."),
            ("skills/switch/references/to-roll.md", "A refusal stops and says why; it never becomes ordinary In."),
            ("skills/switch/references/to.md", "which restarts only its own recorded pane after checking it still runs the recorded Claude, and never types into it."),
            ("skills/conductor/SKILL.md", "roll at the batch boundary yourself with `/kerd:switch roll`"),
            ("skills/conductor/SKILL.md", "Never ask the person to roll"),
            ("skills/switch/SKILL.md", "Conductor rolls its own chat with `/kerd:switch roll`"),
            ("skills/switch/references/in-out.md", "never acted on by ordinary In; only `/kerd:switch roll in` claims it."),
        ):
            with self.subTest(rel=rel, fragment=fragment[:40]):
                self.assertIn(fragment, read(rel))

    def test_guide_forbids_shell_variables_in_the_relaunch(self):
        self.assertIn("Pass no shell variables in the command", read("skills/switch/references/to-roll.md"))


if __name__ == "__main__":
    unittest.main()
