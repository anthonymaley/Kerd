"""What the view may and may not say about a record."""

import importlib.util
from pathlib import Path
import unicodedata
import unittest

SCRIPT = Path(__file__).resolve().parent / "where_we_are.py"
SPEC = importlib.util.spec_from_file_location("where_we_are_tested", SCRIPT)
view = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(view)

NOW = "2026-09-09 12:26 EDT"

FULL = """# Work: a small view

## Jobs

- [done] Direction agreed · producer — five corrections → work.md
- [active] Build it · Claude Opus 5 — renderer and checks
- [next] Review it · Claude Sonnet 5
- [blocked] Publish it — waiting on the producer's word
- [blocked] Archive it
- vague line with no bracket
- [wibble] Odd state

## Agreement

Agreed today, in the producer's words: "direction approved".

## Now

Record updated: 2026-09-09 12:00 EDT
Stage: Deliver
Pending question: none
Next action: review
"""


def render(text, width=80):
    return view.render("record.md", text, NOW, width)


def display_columns(line):
    """Measured here rather than borrowed from the module, so a wrong metric
    in the implementation cannot make its own alignment tests pass."""
    return sum(0 if unicodedata.category(c) in ("Mn", "Me", "Cf")
               else 2 if unicodedata.east_asian_width(c) in ("W", "F") else 1
               for c in line)


def box_lines(out):
    return [line for line in out.splitlines() if line.startswith(("┌", "│", "├", "└"))]


class ViewTests(unittest.TestCase):
    def test_explicit_headings_render_outcome_stage_and_jobs(self):
        out = render(FULL)
        self.assertIn("a small view", out)
        self.assertIn("[NOW: Deliver]", out)
        self.assertIn("✓ done", out)
        self.assertIn("● active", out)
        self.assertIn("Build it", out)
        self.assertIn("→ work.md", out)

    def test_missing_outcome_and_stage_are_labelled_never_guessed(self):
        out = render("## Now\nNext action: something\n")
        self.assertIn("outcome not recorded", out)
        self.assertIn("stage not recorded", out)
        self.assertNotIn("[NOW:", out)

    def test_unrecognised_stage_is_reported_as_recorded_not_mapped_to_a_known_one(self):
        out = render("# Work: x\n\n## Now\nStage: halfway through building\n")
        self.assertIn('recorded stage "halfway through building" is not one of these', out)
        self.assertNotIn("[NOW:", out)

    def test_rendered_at_and_record_updated_are_separate_and_unknown_when_absent(self):
        out = render("# Work: x\n\n## Now\nStage: Shape\n")
        self.assertIn(f"rendered at: {NOW}", out)
        self.assertIn("record updated: unknown", out)

    def test_record_updated_uses_only_what_the_record_states(self):
        self.assertIn("record updated: 2026-09-09 12:00 EDT", render(FULL))

    def test_an_assigned_model_never_reads_as_a_running_job(self):
        out = render(FULL)
        self.assertIn("by: Claude Sonnet 5 (assigned, not started)", out)
        self.assertNotIn("running", out.replace("not that a job is running now.", "")
                                    .replace("was last updated, not that a job is running", ""))
        self.assertIn("as recorded — not observed", out)

    def test_pending_question_of_none_is_not_shown_as_a_decision(self):
        """The record says there is no question; the view must not invent one."""
        out = render(FULL)
        self.assertNotIn("YOU DECIDE", out)
        self.assertIn("no decision is recorded as pending", out)

    def test_a_real_pending_question_is_fully_bounded_with_answer_and_reply(self):
        text = ("# Work: x\n\n## Now\nStage: Agree\n"
                "Pending question: Is the source rule right?\n"
                "Proposed answer: read the explicit headings\n")
        out = render(text)
        box = [line for line in out.splitlines() if line.startswith(("┌", "│", "├", "└"))]
        self.assertTrue(box)
        self.assertEqual({display_columns(line) for line in box}, {80})
        joined = "\n".join(box)
        for expected in ("YOU DECIDE", "Is the source rule right?",
                         "Proposed: read the explicit headings", "Reply: Correct / Change"):
            self.assertIn(expected, joined)

    def test_a_question_without_a_proposed_answer_says_so_inside_the_box(self):
        out = render("# Work: x\n\n## Now\nStage: Agree\nPending question: Which way?\n")
        self.assertIn("Proposed: not recorded", out)

    def test_unlabelled_and_unknown_job_lines_are_kept_and_flagged(self):
        out = render(FULL)
        self.assertIn("? unlab    vague line with no bracket", out)
        self.assertIn("? unlab    Odd state", out)
        self.assertIn('"wibble" is not a recorded state', out)

    def test_blocked_job_without_a_recorded_blocker_says_so(self):
        out = render(FULL)
        self.assertIn("waiting on the producer's word", out)
        self.assertIn("blocker not recorded", out)

    def test_absent_jobs_section_is_reported_not_faked(self):
        self.assertIn("no jobs recorded in this record", render("# Work: x\n\n## Now\nStage: Shape\n"))


    def test_a_repeated_section_is_labelled_and_not_silently_resolved(self):
        """A second "## Now" must not quietly discard the first one's decision."""
        text = ("# Work: x\n\n## Now\nStage: Agree\n"
                "Pending question: Should we ship Friday?\n\n## Now\nNext action: none\n")
        out = render(text)
        self.assertIn('more than one "## Now" section', out)
        self.assertNotIn("Should we ship Friday?", out)
        self.assertNotIn("[NOW:", out)

    def test_headings_inside_fenced_code_cannot_pose_as_record_state(self):
        text = ("# Work: x\n\n## Now\nStage: Shape\nPending question: none\n\n"
                "```\n## Now\nStage: Complete\nPending question: fake?\n```\n")
        out = render(text)
        self.assertNotIn("fake?", out)
        self.assertIn("[NOW: Shape]", out)
        self.assertNotIn('more than one "## Now"', out)

    def test_a_field_stated_twice_is_labelled_rather_than_chosen_between(self):
        out = render("# Work: x\n\n## Now\nStage: Shape\nStage: Complete\n")
        self.assertIn("stage is recorded 2 times; not read", out)
        self.assertNotIn("[NOW:", out)

    def test_punctuation_inside_a_title_is_not_torn_into_fields(self):
        out = render("# Work: x\n\n## Jobs\n- [active] Fix the A·B pipeline\n\n## Now\nStage: Deliver\n")
        self.assertIn("Fix the A·B pipeline", out)
        self.assertNotIn("by:", out)

    def test_spaced_separators_still_parse_actor_detail_and_evidence(self):
        out = render("# Work: x\n\n## Jobs\n- [done] Ship it · Claude — tested → notes.md\n\n## Now\nStage: Deliver\n")
        for expected in ("Ship it", "by: Claude", "tested", "→ notes.md"):
            self.assertIn(expected, out)

    def test_an_unbreakable_word_cannot_push_the_box_open(self):
        out = render("# Work: x\n\n## Now\nStage: Agree\nPending question: " + "A" * 120 + "\n")
        self.assertEqual({display_columns(line) for line in box_lines(out)}, {80})

    def test_wide_characters_keep_the_box_bounded_in_real_columns(self):
        text = ("# Work: x\n\n## Now\nStage: Agree\n"
                "Pending question: 這是一個很長的中文問題需要決定嗎這是一個很長的中文問題需要決定嗎\n")
        out = render(text)
        self.assertEqual({display_columns(line) for line in box_lines(out)}, {80})

    def test_wide_characters_respect_the_requested_width_everywhere(self):
        text = ("# Work: 這是一個很長的中文標題這是一個很長的中文標題這是一個很長的中文標題\n\n"
                "## Jobs\n- [active] 這是一個很長的中文工作項目名稱這是一個很長的中文工作項目名稱\n\n"
                "## Now\nStage: Deliver\n")
        for width in (60, 80):
            with self.subTest(width=width):
                out = render(text, width)
                self.assertLessEqual(max(display_columns(l) for l in out.splitlines()), width)

    def test_a_timestamp_outside_the_status_section_is_not_used_as_record_updated(self):
        text = "# Work: x\n\n## Direction\nRecord updated: 2020-01-01 00:00 EDT\n\n## Now\nStage: Shape\n"
        out = render(text)
        self.assertIn("record updated: unknown", out)
        self.assertNotIn("2020-01-01", out)

    def test_every_line_fits_the_requested_width(self):
        for width in (60, 80, 100):
            with self.subTest(width=width):
                out = render(FULL, width)
                self.assertLessEqual(max(display_columns(line) for line in out.splitlines()), width)


if __name__ == "__main__":
    unittest.main()
