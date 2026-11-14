"""Newcomer-facing wording from the first-user walkthrough (2026-11-13) and the first
weekly review's findings #3 and #4. Each test pins one rule as phrase checks on
whitespace-flattened text: it checks the wording is present, not that a model
follows it.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
CONDUCTOR = REPO / "skills" / "conductor"
SKILL = CONDUCTOR / "SKILL.md"
REFS = CONDUCTOR / "references"
AGENT = REPO / "skills" / "agent" / "SKILL.md"


def flat(text):
    return " ".join(text.split())


def read(path):
    return flat(path.read_text(encoding="utf-8"))


def section(path, heading):
    text = path.read_text(encoding="utf-8")
    start = text.index(heading)
    rest = text[start + len(heading):]
    level = heading.split(" ", 1)[0]
    ends = [i for i in (rest.find("\n" + level + " "), rest.find("\n## ")) if i != -1]
    return flat(rest[: min(ends)] if ends else rest)


class InlineEntryIsOnePlainLine(unittest.TestCase):
    """Walkthrough #6: one inline task showed a Controller/model/effort grid, a Fit
    line and the journey line; the person had to ask what they meant."""

    def test_startup_view_gives_inline_work_one_plain_line(self):
        view = section(REFS / "orchestration.md", "## One visible startup view")
        self.assertIn("**One task Conductor does itself gets one plain line.**", view)
        self.assertIn("No grid, no Fit line, no model or effort evidence and no journey line", view)
        self.assertIn("“**Conductor · Shape — fix the heading.** I'll make the edit myself, "
                      "check the diff and stop before committing.”", view)

    def test_grid_and_pair_evidence_are_conditional_on_dispatch(self):
        execution = read(REFS / "execution.md")
        self.assertIn("when contributors are dispatched, show its task/who/model/effort/status grid", execution)
        self.assertIn("one task this session does itself keeps the [one plain line]", execution)
        orchestration = read(REFS / "orchestration.md")
        self.assertIn("When contributors are dispatched, state the main pair's fit and evidence limits briefly", orchestration)
        self.assertIn("One task this session does itself shows none of this", orchestration)
        self.assertIn("The suitability assessment still happens for every task; with contributors "
                      "dispatched, give a brief visible reason for retaining or inheriting a pair.", orchestration)
        self.assertNotIn("of this: it gets the [one plain line](#one-visible-startup-view). Give a brief reason",
                         orchestration)
        self.assertIn("When contributors are dispatched, show the person a short useful explanation as "
                      "the Fit line under the work grid", read(REFS / "guidance" / "model-choice.md"))
        self.assertIn("say so in one clause on the startup view's Fit line when contributors are "
                      "dispatched; inline work with nothing dispatched keeps this internal.",
                      read(REFS / "guidance" / "README.md"))
        self.assertIn("and, when contributors are dispatched, say in one clause on the Fit line", execution)
        self.assertIn("when contributors are dispatched, disclose the missing profile on the Fit line; "
                      "inline work notes it internally", execution)
        self.assertIn("state the brief task-based reason for retaining or inheriting it visibly when "
                      "contributors are dispatched, and keep it internal for one task done inline",
                      read(REFS / "model-jobs.md"))
        shape = section(REFS / "journey.md", "### The shape of every report")
        self.assertIn("Where contributors were dispatched, the grid, Fit lines, `Change read ·` line", shape)
        self.assertIn("Inline work with nothing dispatched keeps its plain treatment: no grid or Fit lines.", shape)

    def test_walkthrough_evidence_is_scoped(self):
        view = section(REFS / "orchestration.md", "## One visible startup view")
        self.assertIn("In the simulated first-user walkthrough of 2026-11-13 (one persona)", view)
        self.assertNotIn("a newcomer reads those as machinery", view)

    def test_old_inline_controller_example_is_gone(self):
        view = section(REFS / "orchestration.md", "## One visible startup view")
        self.assertNotIn("Include a controller row even when no worker launches", view)
        self.assertNotIn("Fit · Controller", view)
        self.assertNotIn("Live effort unknown unless verified", view)

    def test_dispatch_still_shows_the_grid_and_fit_lines(self):
        view = section(REFS / "orchestration.md", "## One visible startup view")
        self.assertIn("**When Conductor dispatches contributors**", view)
        self.assertIn("The go shows the grid for every job it will dispatch", view)
        self.assertIn("A grid row naming a model without its Fit line is incomplete.", view)
        self.assertIn("Exactly one row per grid is the controller row", view)
        skill = read(SKILL)
        self.assertIn("and the task/who/model/effort grid for the controller and every composer, "
                      "player and reviewer job the go will dispatch, each with its Fit line", skill)

    def test_go_without_ready_still_shows_the_grid_before_dispatch(self):
        """Eval conductor-go, 4 of 4 runs: a go in the opening prompt showed no grid
        or Fit line (three still dispatched), since the go text assumed a Ready."""
        entry = read(REFS / "entry.md")
        for phrase in ("staffing for this work is not on screen",
                       "Before the first `Agent` call",
                       "a row for the controller and every job about to be dispatched",
                       "a Fit line for each",
                       "dispatch in the same turn",
                       "the go is not put to the person again",
                       "Work that dispatches nothing gives the one plain line instead",
                       "assignments its sketchbook already records under that go without showing them again",
                       "a job not in that record gets its row and Fit line first"):
            self.assertIn(phrase, entry)
        skill = read(SKILL)
        self.assertIn("staffing for this work is not on screen", skill)
        self.assertIn("before the first `Agent` call", skill)
        view = section(REFS / "orchestration.md", "## One visible startup view")
        self.assertIn("staffing for this work is not on screen", view)

    def test_skill_entry_must_hold_matches_the_guides(self):
        skill = read(SKILL)
        self.assertIn("when contributors are dispatched, the grid with current model/effort "
                      "evidence and a Fit line per job; when the work is one task Conductor "
                      "does itself, one plain line saying what it will do and where it stops, "
                      "with no grid, Fit line, model/effort evidence or journey line", skill)
        entry = read(REFS / "entry.md")
        self.assertIn("When the work is one task Conductor does itself, the update is "
                      "[one plain line](orchestration.md#one-visible-startup-view): what it "
                      "will do and where it stops, with no grid, Fit line, model/effort "
                      "evidence or journey line.", entry)
        self.assertNotIn("Use the grid for contributors, or a practical inline reason.", entry)

    def test_journey_frame_and_grid_section_agree(self):
        journey = read(REFS / "journey.md")
        self.assertIn("For one task Conductor does itself, leave the journey line out, at "
                      "entry and at that task's decision", journey)
        self.assertIn("One task this session does inline, with nothing dispatched, gets the "
                      "[one plain line](orchestration.md#one-visible-startup-view) instead: "
                      "no grid and no Fit line.", journey)
        self.assertNotIn("even when the result is one inline task and no worker", journey)


class DocWordsAreGlossedOnce(unittest.TestCase):
    """Walkthrough #7: the session said Shape/Agree/Deliver and never the words the
    README teaches (rehearsal, sketchbook, concert)."""

    def test_skill_names_each_doc_word_with_its_gloss(self):
        skill = read(SKILL)
        self.assertIn("Speak the words the docs teach.", skill)
        self.assertIn("name that word once with its plain gloss", skill)
        for gloss in ("“this is rehearsal: we work out what you want”",
                      "“I keep our notes, the sketchbook, at docs/work/<work>/work.md”",
                      "“the concert: I build what we agreed on its own branch”"):
            self.assertIn(gloss, skill)
        self.assertIn("The stage names (Understand, Shape, Agree, Deliver, Complete) stay as they are", skill)

    def test_journey_language_section_carries_the_rule(self):
        language = section(REFS / "journey.md", "## Relaxed, useful language")
        self.assertIn("**Speak the words the docs teach.**", language)
        self.assertIn("The first time in a sitting that the work is in rehearsal, has a "
                      "sketchbook or goes to a concert, name that word once with its plain gloss", language)
        self.assertIn("rehearsal is Understand through Agree and the concert is Deliver", language)
        # Small work ships in rehearsal (entry.md), so the gloss does not say "before anything is built".
        self.assertIn("“This is rehearsal: we work out what you want.”", language)
        self.assertNotIn("before anything is built", language)
        # Evidence is one simulated walkthrough; the mapping difficulty is an inference.
        self.assertIn("In the one simulated first-user walkthrough (2026-11-13)", language)
        self.assertIn("is an inference from that run", language)


class FinishNamesSwitchOut(unittest.TestCase):
    """Walkthrough #12: a finished export ended on “tell me next week”, with no Out
    and no mention of it. Reconciled with “Switch Out at the end is run, not asked”."""

    def test_finish_runs_out_and_names_the_command(self):
        finish = section(REFS / "journey.md", "### One clear finish")
        self.assertIn("**A newcomer learns where Out lives.**", finish)
        self.assertIn("a next item that waits for later (“next week”, someone else's answer) "
                      "does not hold the Out back: name that item, then run Out.", finish)
        self.assertIn("“That's done. I'm putting this down for today with `/kerd:switch out`, "
                      "so `/kerd:switch in` picks it up next time.”", finish)
        self.assertIn("Where the host gives no way to start a skill from the session, the turn "
                      "ends on the one question that hands it over", finish)
        # The existing ruling still stands beside it, qualified by the host limitation.
        self.assertIn("**Switch Out at the end is run, not asked.**", finish)
        self.assertIn("Where the host can start the skill, it never asks", finish)

    def test_skill_finish_must_hold(self):
        skill = read(SKILL)
        self.assertIn("When the agreed goal is met and nothing is outstanding, the controlling "
                      "session runs Switch Out itself, unasked, and says so in plain words "
                      "naming `/kerd:switch out`", skill)
        self.assertIn("`> 💬 **Put this down for today with /kerd:switch out?**`", skill)


class WeeklyReviewWaitsForHistory(unittest.TestCase):
    """Switch's threshold (P1, 2026-11-13): no weekly review line before 3 session logs
    and 7+ days of history; Conductor's route says the same."""

    def test_skill_and_guide_carry_switchs_threshold(self):
        # The definition is Switch In's lookup, pointed to rather than restated loosely.
        self.assertIn("at least 3 session logs and 7+ days of history as [Switch In's lookup]"
                      "(../switch/references/in.md#in) reads it (the oldest dated session log, "
                      "or CONTEXT.md's first commit when older)", read(SKILL))
        self.assertIn("as [Switch In's lookup](../../switch/references/in.md#in) reads it: the oldest "
                      "dated session log, or CONTEXT.md's first commit when older (fewer than 3 logs: "
                      "not offered)", read(REFS / "weekly-review.md"))
        for path in (SKILL, REFS / "weekly-review.md"):
            self.assertNotIn("first Kerd record", read(path))


class QuestionsAboutTheWorkNotThePerson(unittest.TestCase):
    """Weekly review #3: “Is the standing Codex reviewer setup the part that's
    confusing you?”, a bare “the reviewer is running”, and a wake instruction that
    never named which Codex window."""

    RULE = "never ask whether the person is confused: answer what they asked, with one recommendation;"

    def test_asking_line_in_conductor_and_agent(self):
        for path in (SKILL, AGENT):
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8")
                asking = flat(text[text.index("**Asking the person:**"):].split("\n", 1)[0])
                self.assertIn(self.RULE, asking)

    def test_agent_says_which_session_and_names_the_window(self):
        agent = read(AGENT)
        self.assertIn("When starting a worker or reviewer, say in one line which session it is "
                      "(a fresh one-off, or which partner by alias), its model, effort and access", agent)
        self.assertIn("never a bare “the reviewer is running”", agent)
        self.assertIn("When asking the person to type in a partner's window, name that window "
                      "by its thread title", agent)


class LiteralGitPathsWhereCommandsAreWritten(unittest.TestCase):
    """Weekly review #4: six misses of the literal-path git rule, each costing a
    second approval when the guard refused."""

    def test_rule_and_rerun_live_in_the_delivery_guide(self):
        rule = section(REFS / "execution.md", "### Write git commands with the repo's literal path")
        self.assertIn("name the repo by its literal absolute path (`git -C /abs/path …`)", rule)
        self.assertIn("When the guard refuses a command only for its form", rule)
        self.assertIn("rerun the same command with the literal path under the approval that "
                      "already covered it", rule)
        self.assertIn("is not a form refusal and goes back to the person", rule)

    def test_entry_guide_points_there_without_a_second_copy(self):
        entry = read(REFS / "entry.md")
        self.assertIn("execution.md#write-git-commands-with-the-repos-literal-path", entry)
        self.assertNotIn("an ask nobody answers within 30 s refuses the command", entry)


if __name__ == "__main__":
    unittest.main()
