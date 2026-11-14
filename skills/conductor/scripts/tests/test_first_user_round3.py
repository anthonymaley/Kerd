"""Conductor wording from the simulated non-developer walkthrough on 0.196.0
(first-user round 3, 2026-11-14), findings 2, 3, 6, 9 and 18. Each test pins one
rule as phrase checks on whitespace-flattened text: it checks the wording is
present, not that a model follows it.
"""
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[4]
CONDUCTOR = REPO / "skills" / "conductor"
SKILL = CONDUCTOR / "SKILL.md"
REFS = CONDUCTOR / "references"


def flat(text):
    return " ".join(text.split())


def read(path):
    return flat(path.read_text(encoding="utf-8"))


class WorkFolderAndDeliverable(unittest.TestCase):
    """#2: a brief landed at docs/work/overture/launch-brief.md, a name the person
    never used, and not where he would look."""

    def test_record_guide_names_the_folder_from_the_persons_words(self):
        record = read(REFS / "work-record.md")
        self.assertIn("Name `<short-work-name>` from the person's own words for the work "
                      "(“the launch brief” → `launch-brief`), never a label they have not used", record)
        self.assertIn("A deliverable the person will use themselves (a brief, a plan, a letter) "
                      "goes beside their own files, where they would look for it, unless they "
                      "name another place; code goes where the project keeps its code.", record)
        self.assertIn("The record, its diagrams and supporting detail stay in the record's own "
                      "location (the work folder, or the vault when `work_notes` is set).", record)

    def test_skill_must_hold_carries_it(self):
        skill = read(SKILL)
        self.assertIn("Name `<work>` from the person's own words for the work, never an invented "
                      "label; a deliverable they will use themselves (a brief, a plan, a letter) "
                      "goes beside their own files, where they would look, while the sketchbook "
                      "and its supporting material stay in their configured place (the work "
                      "folder, or the vault).", skill)
        self.assertNotIn("with only the sketchbook in the work folder", skill)


class FinishedRevisionPutsWorkDown(unittest.TestCase):
    """#3: a finished revision ended in git words with no Out and no put-down."""

    def test_finished_revision_fires_the_out(self):
        skill = read(SKILL)
        self.assertIn("When the agreed goal is met and nothing is outstanding, a finished "
                      "revision or requested change to delivered work included, the controlling "
                      "session runs Switch Out itself, unasked", skill)
        journey = read(REFS / "journey.md")
        self.assertIn("**A newcomer learns where Out lives.** When the agreed goal is met and "
                      "nothing is outstanding, a finished revision or requested change to "
                      "delivered work included, a next item", journey)

    def test_saved_words_not_git_words(self):
        journey = read(REFS / "journey.md")
        self.assertIn("**Saved, not git words.** To a person who has not used git's words in "
                      "this work, say what the state means for their files, “saved on this "
                      "computer”, “not saved yet”, “there is no copy anywhere else”, never "
                      "commit, uncommitted, “saved to git”, push, branch, remote or working tree.", journey)
        self.assertIn("Someone who uses those words gets them back.", journey)
        skill = read(SKILL)
        self.assertIn("To a person who has not used git's words in this work, say what it means "
                      "for their files (“saved on this computer”, “not saved yet”), never commit, "
                      "uncommitted, push, branch, remote or working tree", skill)


class EditOnlyTheAgreedFiles(unittest.TestCase):
    """#6: revising the brief, Conductor also changed the person's notes.md unasked."""

    def test_source_material_change_is_a_question_first(self):
        execution = read(REFS / "execution.md")
        self.assertIn("**Edit within the agreed scope**: the files the agreed work covers, its own "
                      "records, and any change the request explicitly asks for. A change to the "
                      "person's own source material outside that scope (their notes, data or other "
                      "documents), even one the work implies, is offered as one question first, "
                      "with the change shown, never made and reported afterwards.", execution)
        skill = read(SKILL)
        self.assertIn("Edit within the agreed scope: the files the work covers, its own records "
                      "and any change the request explicitly asks for. A change to the person's own "
                      "source material outside that scope (their notes, data or other documents), "
                      "even one the work implies, is offered as a question first, never made and "
                      "reported afterwards", skill)
        # Ordinary implementation is not limited to files named one by one.
        for text in (execution, skill):
            self.assertNotIn("Edit only the files the agreed work names", text)


class AskTheReadingFormatOnce(unittest.TestCase):
    """#9: a brief for sales and comms was written as .md without asking how they read."""

    def test_format_question_before_drafting(self):
        understanding = read(REFS / "understanding.md")
        self.assertIn("**A document other people will read: ask its format only while it is open.**",
                      understanding)
        self.assertIn("and what they will read it in is unresolved and would change the "
                      "deliverable, ask once, before drafting: a shared doc, slides, an email, a PDF.",
                      understanding)
        self.assertIn("Don't ask when the context already sets the format (the person named it, the "
                      "project's existing documents or the destination fix it) or the person has "
                      "said to go ahead; use what the context sets, or Markdown, and say which.",
                      understanding)
        self.assertIn("a format already named is not asked again", understanding)
        skill = read(SKILL)
        self.assertIn("A document other people will read, its format unresolved and material to the "
                      "result: before drafting, ask once what they will read it in (a shared doc, "
                      "slides, an email, a PDF); never when the context sets it or the person said "
                      "to go ahead; when they don't mind, write Markdown and say so", skill)


class PositionLineFollowsApproval(unittest.TestCase):
    """#18: the sketchbook still read "Waiting on the owner's reaction" after he approved."""

    def test_position_updated_in_the_same_turn(self):
        record = read(REFS / "work-record.md")
        self.assertIn("When the person approves or answers, rewrite in that same turn the record's "
                      "position and header lines", record)
        skill = read(SKILL)
        self.assertIn("When they approve or answer, rewrite in that same turn the sketchbook's "
                      "position and header lines", skill)


class OneLineBeforeDispatchGridAfter(unittest.TestCase):
    """Review r2: Agent's one-line session note before dispatch and Conductor's
    grid-at-the-end rule read as one rule across the two skills."""

    def test_agent_and_conductor_agree(self):
        agent = read(REPO / "skills" / "agent" / "SKILL.md")
        self.assertIn("That one line can come before the dispatch, since a single line before a "
                      "tool call is shown as written; under Conductor, the grid and Fit lines end "
                      "the response that sends the job", agent)
        self.assertIn("../conductor/references/orchestration.md#one-visible-startup-view", agent)
        orchestration = read(REFS / "orchestration.md")
        self.assertIn("A one-line note before the calls is fine", orchestration)
        self.assertIn("as is Agent's one-line session note", orchestration)
        self.assertIn("Only the grid and Fit lines wait for the end.", orchestration)


class FirstUseGlossUsesTheRealPlace(unittest.TestCase):
    """Review r2: the gloss named a fixed docs/work path and "branch" to a person who
    never used git's words."""

    def test_gloss_names_the_actual_place_and_plain_words(self):
        skill = read(SKILL)
        self.assertIn("“I keep our notes, the sketchbook, at <where the record actually lives>”", skill)
        self.assertIn("“the concert: I build what we agreed apart from your files, and it joins "
                      "them when you say”, or “on its own branch” to someone who uses git's words", skill)
        journey = read(REFS / "journey.md")
        self.assertIn("“The concert: I build what we agreed apart from your files, and it joins "
                      "them when you say.” (To someone who uses git's words: “on its own branch”.)", journey)
        for text in (skill, journey):
            self.assertNotIn("the sketchbook, at docs/work/<work>/work.md", text)


if __name__ == "__main__":
    unittest.main()
