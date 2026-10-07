"""Switch never recommends or saves a watch item as the next step.
2026-10-07: with TODO.md's Now holding only watch items and Anthony's decisions,
Switch Out saved "keep using Kerd on real work" and Switch In recommended it
(09:58 and 10:44 sittings); Anthony had to ask for options both times. The 11:49
arrival offered a concrete item because the Out before it saved one. This checks
the wording is present, not that a model follows it.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]
SWITCH = ROOT / "skills/switch"


def flat(rel):
    return " ".join((SWITCH / rel).read_text(encoding="utf-8").split())


class NothingBuildableWordingTests(unittest.TestCase):
    def test_in_treats_watching_as_not_buildable(self):
        text = flat("references/in.md")
        self.assertIn("**Watching is not buildable.**", text)
        self.assertIn("nothing in Now can be built; it holds things to watch and your decisions", text)
        self.assertIn("read the project's Backlog section (that one section, not the archive)", text)
        self.assertIn("never a meta-item such as “use Kerd on real work”", text)

    def test_out_never_saves_a_watch_item(self):
        text = flat("references/out.md")
        self.assertIn("So is watching for behaviour in real use, and a decision only the person can make", text)
        self.assertIn("select one concrete item from the Backlog or the records", text)
        self.assertIn("“keep using it and watch” is never the saved next step", text)

    def test_must_hold_lines_carry_both(self):
        text = flat("SKILL.md")
        self.assertIn("a watch item or the person's decision is never the recommendation", text)
        self.assertIn("never a watch item or the person's decision as the next step", text)


if __name__ == "__main__":
    unittest.main()
