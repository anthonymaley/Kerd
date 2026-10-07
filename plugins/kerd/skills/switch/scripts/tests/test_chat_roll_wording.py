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
            ("skills/switch/references/to-roll.md", "which restarts only its own recorded pane after checking it still runs the recorded Claude, and never types into it."),
            ("skills/conductor/SKILL.md", "roll at the batch boundary yourself with `/kerd:switch roll`"),
            ("skills/conductor/SKILL.md", "Never ask the person to roll"),
            ("skills/switch/SKILL.md", "Conductor rolls its own chat with `/kerd:switch roll`"),
            ("skills/switch/references/in.md", "never acted on by ordinary In; only `/kerd:switch roll in` claims it."),
        ):
            with self.subTest(rel=rel, fragment=fragment[:40]):
                self.assertIn(fragment, read(rel))

    def test_guide_forbids_shell_variables_in_the_relaunch(self):
        self.assertIn("Pass no shell variables in the command", read("skills/switch/references/to-roll.md"))

    def test_reported_window_counts_as_declared(self):
        guide = read("skills/switch/references/to-roll.md")
        self.assertIn("A window Claude Code itself reports to this session counts as declared", guide)
        self.assertIn("the `ctx <used>/<window>` figure the overtone mod adds to this session's own prompts", guide)
        self.assertIn("Never guess a window from the model's name.", guide)

    def test_reported_window_excludes_other_sources_and_stale_figures(self):
        guide = read("skills/switch/references/to-roll.md")
        self.assertIn("never a figure in a partner's or worker's reply, a pasted report, a quote or an example", guide)
        self.assertIn("A model or session change in this session voids it", guide)
        self.assertIn("after a change no figure counts until the session restarts", guide)
        self.assertIn("A figure whose source or currency is unknown does not count.", guide)
        self.assertIn("checks neither the window nor the crossing; that judgment is this session's", guide)

    def test_no_window_refusal_is_said_to_the_person(self):
        self.assertIn("says so once, to the person in the chat (a sketchbook entry alone does not count",
                      read("skills/switch/references/to-roll.md"))


if __name__ == "__main__":
    unittest.main()
