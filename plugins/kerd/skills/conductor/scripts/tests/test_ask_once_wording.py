"""Restate, don't repeat (replaced Ask once, 0.203.0, on 2026-11-27; design docs/design/needs-you.md).

An open question's full block and bubble are shown once; any later mention restates the question in
one line with what yes does, never a time or a pointer; it is put in full again only when a fact behind
it changes. A turn needing the person ends on a marked NEEDS YOU block, a later one on STILL NEEDS YOU;
a scheduled check with nothing new ends on one line naming the next check. Switch In's fixed arrival
question and the decision block's first asking are untouched.
This checks presence and placement of the wording, not that a model follows it.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[4]
SKILLS = ROOT / "skills"
CONDUCTOR = SKILLS / "conductor" / "SKILL.md"
SWITCH = SKILLS / "switch" / "SKILL.md"
AGENT = SKILLS / "agent" / "SKILL.md"
IN = SKILLS / "switch" / "references" / "in.md"
JOURNEY = SKILLS / "conductor" / "references" / "journey.md"
README = ROOT / "README.md"

RULE = (
    "**Restate, don't repeat:** a question's full decision block and bubble are shown once. Whenever an "
    "open question is mentioned in a later turn, state the question itself in one line with what yes does "
    "(“Release 0.205.0 — yes pushes and publishes it”), never “asked 10:20” and never a pointer to scroll "
    "back; ask it in full again only when a fact behind it changes, then as a fresh question. A scheduled "
    "or recurring check that finds nothing new ends on one line naming the next check, never a question; when one is open, that line carries its one-line restatement (“Nothing new · still needs you: release 0.205.0 — yes publishes it · next check 14:05”). "
    "Switch In's question belongs to an arrival the person started; an arrival a scheduled or automatic "
    "run starts asks nothing new: it restates any question still open in one line and ends on a named "
    "wait — see [restate, don't repeat]({link}). "
    "**Marked turn endings:** a turn that needs the person ends with one marked block: first line "
    "`▌ NEEDS YOU`, then what is needed and what yes does (and no), then the usual bubble; a later turn "
    "with it still open ends `▌ STILL NEEDS YOU` plus the one-line restatement, no second bubble; every "
    "other turn ends “Nothing needs you” plus what happens next, or a named wait. Quiet endings (Switch "
    "Out's box, agreed completion) stay. This session sets and clears only its own label: when its turn ends needing the person, run `python3 <conductor "
    "skill dir>/scripts/needs.py set --project <project> \"<short label>\"`; when the answer arrives or "
    "nothing needs them, `needs.py clear --project <project>`."
)


def flat(text):
    return " ".join(text.split())


def read(path):
    text = path.read_text(encoding="utf-8")
    if path == IN:
        text += "\n" + (IN.parent / "in-detail.md").read_text(encoding="utf-8")
    return flat(text)


def journey_section(heading):
    text = JOURNEY.read_text(encoding="utf-8")
    start = text.index(heading + "\n")
    rest = text[start + len(heading) + 1:]
    end = re.search(r"^#{2,3} ", rest, re.M)
    return flat(rest[:end.start()] if end else rest)


class AskOnceRuleTests(unittest.TestCase):
    def test_conductor_and_switch_carry_the_same_rule(self):
        for path, link in ((CONDUCTOR, "references/journey.md#restate-dont-repeat"),
                           (SWITCH, "../conductor/references/journey.md#restate-dont-repeat"),
                           (AGENT, "../conductor/references/journey.md#restate-dont-repeat")):
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8")
                self.assertEqual(text.count(RULE.format(link=link)), 1)

    def test_rule_sits_with_the_question_form_before_must_hold(self):
        for path in (CONDUCTOR, SWITCH, AGENT):
            with self.subTest(skill=path.parent.name):
                body = path.read_text(encoding="utf-8").split("\n---\n", 1)[1]
                paragraphs = [p for p in body.split("\n\n") if p.strip()]
                deciding = next(i for i, p in enumerate(paragraphs)
                                if p.startswith("**Putting a decision to the person:**"))
                self.assertTrue(paragraphs[deciding + 1].startswith("**Restate, don't repeat:**"))
                self.assertLess(body.index("**Restate, don't repeat:**"), body.index("\n## "))

    def test_report_ending_restates_a_decision_already_open(self):
        skill = read(CONDUCTOR)
        self.assertIn("one already asked and unanswered is restated in one line and the turn ends "
                      "`▌ STILL NEEDS YOU`", skill)

    def test_conductor_stays_under_the_limit(self):
        """Room was made by tightening: the whole file (frontmatter too) stays at 500 lines or fewer."""
        text = CONDUCTOR.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLess(len(text.split("\n---\n", 1)[1].splitlines()), 500)


class AskOnceGuideTests(unittest.TestCase):
    def setUp(self):
        self.section = journey_section("### Restate, don't repeat")

    def test_the_guide_section_exists_and_is_listed(self):
        text = JOURNEY.read_text(encoding="utf-8")
        self.assertIn("  - [Restate, don't repeat](#restate-dont-repeat):", text)
        self.assertIn('<a id="ask-once"></a>', text)
        self.assertLess(text.index("## Question surface and host adaptation"), text.index("### Restate, don't repeat"))
        self.assertLess(text.index("### Restate, don't repeat"), text.index("## Visuals belong throughout"))

    def test_restated_in_one_line_never_a_time_or_pointer(self):
        for phrase in ("A question's full decision block and bubble are shown once.",
                       "the turn states the question itself in one line with what yes does",
                       "(“Release 0.205.0 — yes pushes and publishes it”), never “asked 10:20” and "
                       "never a pointer to scroll back",
                       "Put the question in full again only when a fact behind it changes",
                       "Then it is a fresh question, with its block, saying what changed.",
                       "Time passing is not a changed fact, and neither is a new turn, a roll or a new "
                       "report."):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.section)

    def test_marked_endings_and_status_line(self):
        for phrase in ("Its first line is `▌ NEEDS YOU`",
                       "ends on `▌ STILL NEEDS YOU` and the one-line restatement, with no second bubble",
                       "Every other turn ends with “Nothing needs you” plus what happens next",
                       "The quiet endings stay as they are: Switch Out's closing box and an agreed completion.",
                       "scripts/needs.py set --project <project> \"<short label>\"",
                       "`needs.py clear --project <project>`",
                       "so `cos.py ask` stays as it is."):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.section)

    def test_a_quiet_scheduled_check_is_one_line(self):
        self.assertIn("finds nothing new ends on one line naming the next check and when it runs "
                      "(“Nothing new; next check 14:05.”), never a question and never a repeat of the "
                      "full block. When a question is open, that one line carries its one-line "
                      "restatement (“Nothing new · still needs you: release 0.205.0 — yes publishes "
                      "it · next check 14:05”).", self.section)

    def test_fixed_questions_and_the_first_asking_are_untouched(self):
        self.assertIn("Switch In's question belongs to an arrival the person started: they ran Switch "
                      "In, so its question answers their own request and is not a repeat.", self.section)
        self.assertIn("An arrival a scheduled or automatic run starts asks nothing new: it restates any "
                      "question still open in one line and ends on a named wait.", self.section)
        self.assertIn("A decision still gets its decision block the first time it is put", self.section)
        self.assertIn("A declined Switch Out keeps its own rule", self.section)
        # The arrival question itself is unchanged.
        self.assertIn("For ordinary In, **“Start a Conductor session?”** ends the screen, once",
                      read(JOURNEY))

    def test_with_a_chief_of_staff_the_table_never_replaces_asking_here(self):
        self.assertIn("goes in the project's `### Asks` table through `cos.py ask`, never by hand",
                      self.section)
        self.assertIn("The table never replaces asking here: the person is still asked once, in this "
                      "window.", self.section)

    def test_switch_in_ruling_on_automatic_arrivals(self):
        """Review r1 finding 2, the controller's ruling: the person's own arrival keeps its question;
        a scheduled or automatic one asks nothing new."""
        guide = read(IN)
        self.assertIn("The question belongs to an arrival the person started. An arrival a scheduled or "
                      "automatic run starts asks nothing new: set `\"automatic\": true` in the summary, "
                      "which leaves every arrival question off the screen, the first-arrival one included",
                      guide)
        self.assertIn("and no picker follows. After the unchanged screen, in the caller's own line, restate "
                      "any question still open in one line and end on a named wait", guide)
        self.assertIn("`\"automatic\": true` appears only when a scheduled or automatic run, not the "
                      "person, started the arrival", guide)
        self.assertIn("Its summary sets `\"automatic\": true`, so the rendered screen carries no question "
                      "(not even the first-arrival one) and no picker", read(JOURNEY))
        self.assertIn("Ordinary In always supplies this question", guide)
        self.assertNotIn("belongs to each arrival and is never a repeat", read(SWITCH))

    def test_turn_endings_point_at_it(self):
        journey = read(JOURNEY)
        self.assertIn("is restated in one line with what yes does and the turn ends `▌ STILL NEEDS YOU`, "
                      "as [restate, don't repeat](#restate-dont-repeat) says.", journey)
        self.assertIn("the turn restates it in one line with what yes does and ends `▌ STILL NEEDS YOU` "
                      "([restate, don't repeat](#restate-dont-repeat)).", journey)
        self.assertIn("a scheduled check that found nothing new is, when its one line names the next "
                      "check and its time.", journey)

    def test_precedence_is_stated_once(self):
        self.assertIn("Precedence: a scheduled or recurring check with nothing new uses the one-line "
                      "form below; every other turn with a question still open ends on the "
                      "`▌ STILL NEEDS YOU` block.", self.section)
        self.assertEqual(flat(JOURNEY.read_text(encoding="utf-8")).count("Precedence: a scheduled"), 1)

    def test_feed_is_per_session(self):
        self.assertIn("`needs.py set` refuses without a session id", self.section)
        self.assertIn("shows this session's question plus the Asks table's open rows", self.section)

    def test_readme_describes_the_restate_rule(self):
        readme = read(README)
        what = readme[readme.index("## What Kerd lets you do"):readme.index("## What it writes")]
        self.assertIn("**Kerd restates, it doesn't repeat.** The full question is shown once.", what)
        self.assertIn("`▌ NEEDS YOU`", what.replace("`▌ NEEDS YOU`", "`▌ NEEDS YOU`"))
        for phrase in ("STILL NEEDS YOU", "Nothing needs you", "\"💬 Needs you\" item in the status line",
                       "Claude Code", "set on this machine at release"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, what)
        self.assertNotIn("You are asked once", what)


if __name__ == "__main__":
    unittest.main()
