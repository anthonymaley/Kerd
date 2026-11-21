"""Ask once (0.203.0, design: eolas vault kerd/work/cos-mode/work.md, issue 1).

A question already asked and still unanswered is not asked again to end a later turn: the
report names it with the time it was asked and the turn ends on a named wait; it is asked
again only when a fact behind it changes; a scheduled check with nothing new ends on one line
naming the next check. It covers every Kerd user, not only a chief of staff, and leaves
Switch In's fixed arrival question and the decision block's first asking as they were.
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
    "**Asking once:** a question already asked and still unanswered is not asked again to end a "
    "later turn: the report names it with the time it was asked (“still waiting on your go for the "
    "merge, asked 10:20”) and the turn ends on a named wait for that answer, its bubble and decision "
    "block not repeated; it is asked again only when a fact behind it changes, then as a fresh "
    "question. A scheduled or recurring check that finds nothing new ends on one line naming the "
    "next check, never a question. Switch In's question belongs to an arrival the person started; an "
    "arrival a scheduled or automatic run starts asks nothing new: it names any question still open "
    "and ends on a named wait — see [asking once]({link})."
)


def flat(text):
    return " ".join(text.split())


def read(path):
    return flat(path.read_text(encoding="utf-8"))


def journey_section(heading):
    text = JOURNEY.read_text(encoding="utf-8")
    start = text.index(heading + "\n")
    rest = text[start + len(heading) + 1:]
    end = re.search(r"^#{2,3} ", rest, re.M)
    return flat(rest[:end.start()] if end else rest)


class AskOnceRuleTests(unittest.TestCase):
    def test_conductor_and_switch_carry_the_same_rule(self):
        for path, link in ((CONDUCTOR, "references/journey.md#ask-once"),
                           (SWITCH, "../conductor/references/journey.md#ask-once"),
                           (AGENT, "../conductor/references/journey.md#ask-once")):
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
                self.assertTrue(paragraphs[deciding + 1].startswith("**Asking once:**"))
                self.assertLess(body.index("**Asking once:**"), body.index("\n## "))

    def test_report_ending_asks_a_decision_once(self):
        skill = read(CONDUCTOR)
        self.assertIn("When Needs you names a decision, the turn ends on a bubble asking exactly that, "
                      "in the three lines' own terms, once: one already asked and unanswered is named "
                      "with its time and the turn ends on a named wait", skill)

    def test_conductor_stays_under_the_limit(self):
        """Room was made by tightening: the whole file (frontmatter too) stays at 500 lines or fewer."""
        text = CONDUCTOR.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertLess(len(text.split("\n---\n", 1)[1].splitlines()), 500)


class AskOnceGuideTests(unittest.TestCase):
    def setUp(self):
        self.section = journey_section("### Ask once")

    def test_the_guide_section_exists_and_is_listed(self):
        text = JOURNEY.read_text(encoding="utf-8")
        self.assertIn("  - [Ask once](#ask-once):", text)
        self.assertLess(text.index("## Question surface and host adaptation"), text.index("### Ask once"))
        self.assertLess(text.index("### Ask once"), text.index("## Visuals belong throughout"))

    def test_named_with_its_time_and_a_named_wait(self):
        for phrase in ("A question is asked once.",
                       "the report names it, with the time it was asked, in Needs you",
                       "the turn ends on a named wait for that answer: what it waits on, that the "
                       "session resumes when the person answers, and what this turn did meanwhile or "
                       "why nothing else can move",
                       "The bubble and the decision block went with the first asking and are not repeated"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.section)

    def test_asked_again_only_on_a_changed_fact(self):
        self.assertIn("Ask it again only when a fact behind it changes", self.section)
        self.assertIn("Then it is a fresh question, put in full, with its block, saying what changed.",
                      self.section)
        self.assertIn("Time passing is not a changed fact, and neither is a new turn, a roll or a new "
                      "report.", self.section)

    def test_a_quiet_scheduled_check_is_one_line(self):
        self.assertIn("finds nothing new ends on one line naming the next check and when it runs "
                      "(“Nothing new; next check 14:05.”), never a question and never a repeat of the "
                      "open ones.", self.section)

    def test_fixed_questions_and_the_first_asking_are_untouched(self):
        self.assertIn("Switch In's question belongs to an arrival the person started: they ran Switch "
                      "In, so its question answers their own request and is not a repeat.", self.section)
        self.assertIn("An arrival a scheduled or automatic run starts asks nothing new: it names any "
                      "question still open and ends on a named wait.", self.section)
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
        self.assertIn("and no picker follows. After the unchanged screen, in the caller's own line, name "
                      "any question still open with the time it was asked and end on a named wait", guide)
        self.assertIn("`\"automatic\": true` appears only when a scheduled or automatic run, not the "
                      "person, started the arrival", guide)
        self.assertIn("Its summary sets `\"automatic\": true`, so the rendered screen carries no question "
                      "(not even the first-arrival one) and no picker", read(JOURNEY))
        self.assertIn("Ordinary In always supplies this question", guide)
        self.assertNotIn("belongs to each arrival and is never a repeat", read(SWITCH))

    def test_turn_endings_point_at_it(self):
        journey = read(JOURNEY)
        self.assertIn("A decision already asked and still unanswered is not asked again: it is named "
                      "with its time and the turn ends on a named wait, as [ask once](#ask-once) says.",
                      journey)
        self.assertIn("A question already asked and still open is not asked again: the turn names it "
                      "with its time and ends on a named wait for the answer ([ask once](#ask-once)).",
                      journey)
        self.assertIn("a scheduled check that found nothing new is, when its one line names the next "
                      "check and its time.", journey)

    def test_readme_says_it_covers_everyone(self):
        readme = read(README)
        self.assertIn("**You are asked once.** A question Kerd has put to you and you haven't answered "
                      "yet is not asked again on the next turn", readme)
        what = readme[readme.index("## What Kerd lets you do"):readme.index("## What it writes")]
        self.assertIn("**You are asked once.**", what)


if __name__ == "__main__":
    unittest.main()
