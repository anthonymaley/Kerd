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
        # codex-tui 2026-10-07: concrete is not eligible; weigh, never auto-pick.
        self.assertIn("A row the records defer, park or hold until something happens is not eligible.", text)
        self.assertIn("Weigh the saved selection as above;", text)
        self.assertNotIn("Recommend the saved selection when it is a concrete item", text)

    def test_in_keeps_the_grounded_route_for_a_pending_choice(self):
        # codex-tui 2026-10-07: only passive waiting is excluded, not a route that resolves a choice.
        text = flat("references/in.md")
        self.assertIn("Proposing a grounded route to resolve a saved unresolved choice (below) is not waiting", text)
        self.assertIn("For a saved unresolved choice, recommend one grounded route", text)
        self.assertIn("never a meta-item such as “use Kerd on real work”", text)

    def test_out_never_saves_a_watch_item(self):
        text = flat("references/out.md")
        self.assertIn("So is watching for behaviour in real use, and only waiting for the person to decide", text)
        self.assertIn("select one concrete item from the Backlog or the records that they do not defer, park or hold", text)
        self.assertIn("a grounded route that resolves a pending choice is a concrete item", text)
        self.assertIn("“keep using it and watch” is never the saved next step", text)

    def test_must_hold_lines_carry_both(self):
        text = flat("SKILL.md")
        self.assertIn("an item that only waits (to watch real use, or for the person to decide) is never the "
                      "recommendation", text)
        self.assertIn("skipping deferred or parked ones", text)
        self.assertIn("never an item that only waits as the next step", text)


if __name__ == "__main__":
    unittest.main()
