"""What the second simulated first-user run (2026-11-14) still found in Switch.

N1: a later arrival showed TEAM "No established pairing" with no partner set up.
N2: "Contributions captured: Claude (this session) only" printed above the box.
N3: the restart line led with "Agent view" and "the session list".
N5: "Last session" described an earlier sitting the same day.
N6: Out committed code and a generated CSV it never named to the person.
N7: Out wrote fixed-name files in the shared /tmp.
N8: the first arrival said "tell me what you want", then asked a yes/no question.

Renderer checks run the code; guide checks find the wording, not that a model
follows it.
"""
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[4]
SWITCH = ROOT / "skills/switch"
SCRIPT = SWITCH / "scripts" / "where_we_are.py"
SPEC = importlib.util.spec_from_file_location("where_we_are_round2", SCRIPT)
view = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(view)

NOW = "2026-11-14 09:00 EST"


def flat(text):
    return " ".join(text.split())


def guide(rel):
    return flat((SWITCH / rel).read_text(encoding="utf-8"))


def arrival(**over):
    summary = {"project": "Tally", "phase": "working", "where": "Export works.",
               "open_work": ["Export one customer's requests."],
               "recommendation": {"text": "Export one customer's requests.", "why": "You asked."},
               "last_session": "Added a spreadsheet export.", "team": [],
               "question": {"text": "Start a Conductor session?", "proposed": None},
               "documents": [], "warnings": [], "insight": None, "base": ".",
               "restored": "yes", "restore_note": None, "first_arrival": False}
    summary.update(over)
    return summary


def table(out):
    return [line for line in out.splitlines() if line.startswith("|")]


class NoPairingNoTeamCellTests(unittest.TestCase):
    """N1: no pairing leaves the TEAM cell out, as the first arrival already does."""

    def test_an_empty_team_has_no_team_cell(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = view.render_dashboard(arrival(), NOW, 80, False, markdown=markdown)
                self.assertNotIn("TEAM", out)
                self.assertNotIn("pairing", out)
                self.assertIn("PHASE", out)

    def test_the_markdown_table_stays_well_formed(self):
        rows = table(view.render_dashboard(arrival(), NOW, 80, False, markdown=True))
        self.assertEqual(rows[0], "| PROJECT | PHASE | NEXT |")
        self.assertEqual([row.count("|") for row in rows], [4, 4, 4])

    def test_a_partner_still_shows_and_unread_still_says_so(self):
        team = [{"provider": "codex", "id": "x", "role": "Reviewer"}]
        out = view.render_dashboard(arrival(team=team), NOW, 80, False, markdown=True)
        self.assertIn("| PROJECT | PHASE | NEXT | TEAM |", out)
        self.assertIn("Codex (Reviewer)", out)
        self.assertEqual([row.count("|") for row in table(out)], [5, 5, 5])
        unread = view.render_dashboard(arrival(team=None), NOW, 80, False, markdown=True)
        self.assertIn("| PROJECT | PHASE | NEXT | TEAM |", unread)
        self.assertIn("not recorded", unread)

    def test_the_older_grid_drops_it_too(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = view.render_dashboard({"project": "Tally", "team": []}, NOW, 80, False,
                                            markdown=markdown)
                self.assertNotIn("TEAM", out)
        rows = table(view.render_dashboard({"project": "Tally", "team": []}, NOW, 80, False,
                                           markdown=True))
        self.assertEqual(rows[0], "| PROJECT | PHASE | STATE |")
        self.assertEqual([row.count("|") for row in rows], [4, 4, 4])

    def test_the_guide_says_no_cell(self):
        text = guide("references/in.md")
        self.assertIn("TEAM, the restored pairing when a partner was restored, or “not recorded” "
                      "when the team could not be read (`null`); only with no pairing (`team: []`) "
                      "does the grid have no TEAM cell.", text)
        self.assertIn("the PROJECT · PHASE · NEXT grid (TEAM added when a partner was restored or "
                      "the team could not be read; none with no pairing)", guide("SKILL.md"))


class FirstArrivalQuestionTests(unittest.TestCase):
    """N8: the question under "tell me what you want" asks for the work."""

    def test_the_renderer_asks_for_the_work_whatever_the_caller_passed(self):
        for question in ({"text": "Start a Conductor session?", "proposed": None}, None):
            for markdown in (False, True):
                with self.subTest(question=question, markdown=markdown):
                    out = view.render_dashboard(arrival(first_arrival=True, question=question),
                                                NOW, 80, False, markdown=markdown)
                    self.assertTrue(flat(out).rstrip("*").endswith("What do you want to work on?"))
                    self.assertNotIn("Start a Conductor session?", out)

    def test_a_later_arrival_keeps_its_question(self):
        out = view.render_dashboard(arrival(), NOW, 80, False, markdown=True)
        self.assertTrue(flat(out).rstrip("*").endswith("Start a Conductor session?"))
        self.assertNotIn("What do you want to work on?", out)

    def test_the_guides_name_the_first_arrival_question(self):
        self.assertIn("The question under that line is “What do you want to work on?”",
                      guide("references/in.md"))
        self.assertIn("a first arrival asks “What do you want to work on?” instead, with no picker",
                      guide("SKILL.md"))


class RestartLineTests(unittest.TestCase):
    """N3: the restart line leads with /clear and names no Agent view."""

    def test_the_line(self):
        out = view.render_closing({"project": "Tally", "saved": "committed", "handoff_ready": True,
                                   "boundary": "local_only", "verdicts": {"project": "local_only"},
                                   "tree": "clean", "host": "claude"}, NOW, 80, False, markdown=True)
        self.assertTrue(flat(out).endswith("Run /clear, then /kerd:switch in to pick up from here."))
        self.assertNotIn("Agent view", out)
        self.assertNotIn("session list", out)
        self.assertNotIn("Agent view", guide("references/out.md"))


class OutGuideTests(unittest.TestCase):
    """N2, N5, N6 and N7: wording in Out and In."""

    def test_no_checkpoint_line_when_this_session_is_alone(self):
        self.assertIn("When this session is the only contributor there is nothing to reconcile, "
                      "so show no checkpoint line.", guide("references/out.md"))
        self.assertIn("and no line when this session is the only contributor", guide("SKILL.md"))

    def test_each_sitting_gets_its_own_heading_and_in_reads_the_newest(self):
        self.assertIn("under its own heading for this sitting even when that day's log already "
                      "holds an earlier one", guide("references/out.md"))
        self.assertIn("the newest account in the newest session log, which is its last sitting "
                      "heading when one day's log holds several, not an earlier sitting that day",
                      guide("references/in.md"))

    def test_out_names_other_files_before_saving_them(self):
        text = guide("references/out.md")
        self.assertIn("Out names its own records: the start point, `TODO.md`, the session log, "
                      "any sketchbook it wrote and, with `work_notes`, `notes:outside-the-repo.md`.", text)
        self.assertIn("do not join Out's save on its own judgement: name each one to the person in "
                      "one question", text)
        self.assertIn("only after naming each to the person and hearing yes", guide("SKILL.md"))

    def test_no_fixed_names_in_shared_tmp(self):
        for rel in ("references/in.md", "references/out.md"):
            with self.subTest(rel=rel):
                text = guide(rel)
                self.assertIn("`mktemp`", text)
                self.assertRegex(text, r"fixed name in a shared folder such as `/tmp`")


class SkillBodyLimitTests(unittest.TestCase):
    def test_skill_body_stays_under_500_lines(self):
        text = (SWITCH / "SKILL.md").read_text(encoding="utf-8")
        body = re.split(r"^---$", text, maxsplit=2, flags=re.M)[2]
        self.assertLessEqual(len(body.splitlines()), 500)


if __name__ == "__main__":
    unittest.main()


class TeamValueTests(unittest.TestCase):
    """Only an empty list means no pairing; any other non-list value is unread."""

    def test_only_an_empty_list_drops_the_team_cell(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "where_we_are_team", Path(__file__).resolve().parents[1] / "where_we_are.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.team_rows([]), [])
        for value in (None, False, "", {}, 0):
            with self.subTest(value=value):
                self.assertEqual(module.team_rows(value), [("TEAM", "not recorded", None)])
