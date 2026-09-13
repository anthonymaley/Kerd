"""What the view may and may not say about a record."""

import importlib.util
from pathlib import Path
import unicodedata
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "where_we_are.py"
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


def flatten(text):
    """Collapse wrapping and indentation so a whole value can be compared."""
    return " ".join(text.split())


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

    def test_a_field_running_over_several_lines_is_read_whole(self):
        """A question written across lines must not be shown as its first line."""
        text = ("# Work: x\n\n## Now\nStage: Agree\n"
                "Pending question: Do the two checks pass, could you see what was\n"
                "happening, and did it finish without you asking again?\n"
                "Proposed answer: one is yours to judge\n")
        out = render(text)
        flat = " ".join(line.strip("│ ") for line in box_lines(out)).split()
        self.assertIn("did it finish without you asking again?", " ".join(flat))
        self.assertIn("Proposed: one is yours to judge", " ".join(flat))
        self.assertNotIn("Proposed: not recorded", out)

    def test_a_stage_written_with_trailing_punctuation_is_recognised(self):
        """Records write "Stage: Complete." as readily as "Stage: Complete"."""
        self.assertIn("[NOW: Complete]", render("# Work: x\n\n## Now\nStage: Complete.\n"))

    def test_current_activity_and_next_action_are_shown_or_labelled(self):
        out = render("# Work: x\n\n## Now\nStage: Deliver\nNext action: ask the producer\n")
        self.assertIn("next   ask the producer", out)
        self.assertIn("doing  not recorded", out)

    def test_the_records_own_now_subheading_orients_when_no_stage_is_given(self):
        text = "# Work: x\n\n## Now\n\n### Pickup after local closeout\n\nPosition: main\n"
        out = render(text)
        self.assertIn("position, from this record's own Now heading: Pickup after local", out)

    def test_a_recorded_stage_is_not_duplicated_by_the_subheading_line(self):
        text = "# Work: x\n\n## Now\nStage: Deliver\n\n### Some heading\n\nbody\n"
        self.assertNotIn("position, from this record's own", render(text))

    def test_links_the_record_carries_are_offered_deduplicated_and_capped(self):
        body = "".join(f"[label {n}](target-{n}.md)\n" for n in range(7))
        out = render(f"# Work: x\n\n## Now\nStage: Deliver\n\n{body}[again](target-0.md)\n")
        self.assertIn("[NOW: Deliver]", out)
        self.assertIn("LINKS THE RECORD ALREADY CARRIES (first 5 of 7)", out)
        self.assertIn("→ target-0.md (label 0)", out)
        self.assertNotIn("target-6.md", out)

    def test_prose_running_straight_into_a_field_is_labelled_not_shown_as_a_stage(self):
        """The continuation rule can swallow a following paragraph; that must be
        visible as an unrecognised stage, never rendered as a confident one."""
        out = render("# Work: x\n\n## Now\nStage: Deliver\nand then a paragraph follows here\n")
        self.assertIn("is not one of these", out)
        self.assertNotIn("[NOW:", out)

    def test_a_record_without_links_shows_no_empty_links_heading(self):
        self.assertNotIn("LINKS THE RECORD", render("# Work: x\n\n## Now\nStage: Deliver\n"))

    def test_a_compact_update_names_the_work_the_actor_and_whether_you_are_needed(self):
        text = ("# Work: x\n\n## Jobs\n- [done] Agreed · producer\n"
                "- [active] Build it · Claude Opus 5 — renderer\n\n## Now\nStage: Deliver\n")
        out = view.compact("record.md", text, NOW)
        self.assertIn("● Build it · Claude Opus 5", out)
        self.assertIn("You: nothing needed.", out)
        self.assertIn("as recorded — not observed", out)

    def test_a_compact_update_is_short_and_is_not_the_whole_view(self):
        text = ("# Work: x\n\n## Jobs\n- [active] Build it · Claude Opus 5\n\n"
                "## Now\nStage: Deliver\nNext action: keep going\n")
        out = view.compact("record.md", text, NOW)
        self.assertLessEqual(len(out.splitlines()), 4)
        for absent in ("JOURNEY", "Understand →", "JOBS (as recorded", "LINKS THE RECORD"):
            self.assertNotIn(absent, out)

    def test_a_compact_update_makes_a_waiting_decision_unmistakable(self):
        text = ("# Work: x\n\n## Jobs\n- [active] Build it · Claude Opus 5\n\n"
                "## Now\nStage: Agree\nPending question: Which way?\n")
        out = view.compact("record.md", text, NOW)
        self.assertIn("You: a decision is waiting — Which way?", out)
        self.assertNotIn("nothing needed", out)

    def test_a_compact_update_reports_blocked_work_with_its_blocker(self):
        text = ("# Work: x\n\n## Jobs\n- [blocked] Ship it — waiting on the key\n\n"
                "## Now\nStage: Deliver\n")
        out = view.compact("record.md", text, NOW)
        self.assertIn("⨯ blocked: Ship it — waiting on the key", out)

    def test_a_compact_update_with_no_active_job_says_so_plainly(self):
        out = view.compact("record.md", "# Work: x\n\n## Now\nStage: Deliver\n", NOW)
        self.assertIn("no job recorded as active", out)
        self.assertNotIn("not recorded as active", out.replace("no job recorded as active", ""))

    def test_every_line_fits_the_requested_width(self):
        for width in (60, 80, 100):
            with self.subTest(width=width):
                out = render(FULL, width)
                self.assertLessEqual(max(display_columns(line) for line in out.splitlines()), width)


if __name__ == "__main__":
    unittest.main()


DASH = """# Work: the candidate track

## Jobs

- [done] Build the "Where we are" view · Claude Opus 5 — reviewed and corrected
- [active] Shape the welcome dashboard · producer
- [blocked] Install the candidate — the setup choice is not made

## Agreement

Controlled adoption of Conductor, Switch and Visuals.

## Now

Record updated: 2026-09-09 21:00 EDT
Stage: Deliver
Phase: Controlled adoption
Pending question: How do you want to enter the candidate?
Proposed answer: install it
Reply with: Install / Hand-load
Insight: your usual command still opens the old door.

See the [Design](design.md) and the [Tasks](consolidation.md).
"""

QUIET = """# Work: a quiet record

## Jobs

- [done] Ship the thing · Claude Opus 5

## Agreement

Standing agreement recorded.

## Now

Record updated: 2026-09-09 21:00 EDT
Phase: Controlled adoption
Pending question: none
Next action: pick the next slice
"""


def dash(text, width=80, color=False, record="record.md"):
    return view.dashboard(record, text, NOW, width, color)


def strip_ansi(text):
    import re as _re
    return _re.sub(r"\x1b\[[0-9;]*m", "", text)


class DashboardTests(unittest.TestCase):
    def test_an_open_job_is_the_task_even_with_no_activity_field(self):
        """Corrected: no current activity does not mean no selected task."""
        self.assertIn("Shape the welcome dashboard", dash(DASH))
        self.assertNotIn("Not selected yet", dash(DASH))

    def test_task_shows_the_recorded_activity_when_there_is_one(self):
        out = dash(DASH.replace("Stage: Deliver", "Stage: Deliver\nCurrent activity: draw it"))
        self.assertIn("draw it", out)
        self.assertNotIn("Not selected yet", out)

    def test_phase_is_the_recorded_phase_verbatim(self):
        self.assertIn("Controlled adoption", dash(DASH))

    def test_phase_falls_back_to_stage_then_to_not_recorded(self):
        self.assertIn("Deliver", dash(DASH.replace("Phase: Controlled adoption", "")))
        self.assertIn(view.UNRECORDED,
                      dash(DASH.replace("Phase: Controlled adoption", "").replace("Stage: Deliver", "")))

    def test_state_reports_a_pending_decision_over_a_next_action(self):
        self.assertIn("Decision pending", dash(DASH))

    def test_state_uses_next_action_when_nothing_is_pending(self):
        self.assertIn("pick the next slice", dash(QUIET))

    def test_you_box_is_amber_only_while_a_decision_is_pending(self):
        self.assertIn("\x1b[33m", dash(DASH, color=True))
        self.assertNotIn("\x1b[33m", dash(QUIET, color=True))

    def test_colour_is_absent_when_it_is_switched_off(self):
        self.assertNotIn("\x1b[", dash(DASH, color=False))

    def test_ansi_never_changes_a_bordered_line_width(self):
        plain = [line for line in dash(DASH, color=False).splitlines() if line.startswith("│")]
        painted = [strip_ansi(line) for line in dash(DASH, color=True).splitlines()
                   if strip_ansi(line).startswith("│")]
        self.assertTrue(plain)
        self.assertEqual(plain, painted)
        for line in plain:
            self.assertEqual(display_columns(line), 80)

    def test_a_blocked_job_is_reported_as_a_warning(self):
        out = dash(DASH)
        self.assertIn("Install the candidate", out)
        self.assertIn("blocked", out.lower())

    def test_a_clean_record_shows_no_warning_block(self):
        self.assertNotIn("⚠", dash(QUIET))

    def test_last_session_is_summarised_from_a_recorded_done_job(self):
        self.assertIn("LAST SESSION", dash(DASH))
        self.assertIn("Where we are", dash(DASH))

    def test_this_session_is_the_active_job_and_says_so_when_there_is_none(self):
        self.assertIn("Shape the welcome dashboard", dash(DASH))
        self.assertIn("Nothing agreed yet", dash(QUIET))

    def test_links_that_do_not_resolve_are_not_offered_as_navigation(self):
        out = dash(DASH)
        self.assertIn("cannot be opened", out)
        self.assertEqual(out.count("design.md"), 1, "a broken target is named once, as a warning")
        self.assertNotIn("design.md", "\n".join(
            line for line in out.splitlines() if line.strip().startswith("→")))

    def test_links_that_resolve_are_shown_with_label_and_path(self):
        import tempfile, os
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "sub"), exist_ok=True)
            record = os.path.join(tmp, "sub", "work.md")
            open(os.path.join(tmp, "sub", "design.md"), "w").close()
            open(os.path.join(tmp, "sub", "consolidation.md"), "w").close()
            out = dash(DASH, record=record)
        self.assertIn("Design", out)
        self.assertIn("design.md", out)
        self.assertNotIn("cannot be opened", out)

    def test_one_source_block_names_the_record_once_with_both_stamps(self):
        for w in (80, 120):
            out = dash(DASH, width=w)
            self.assertEqual(out.count("read:"), 1, "the source is named once, not per field")
            tail = "\n".join(out.splitlines()[-2:])
            self.assertIn("2026-09-09 21:00 EDT", tail)
            self.assertIn(NOW, tail)

    def test_insight_is_shown_when_recorded_and_absent_when_not(self):
        self.assertIn("old door", dash(DASH))
        self.assertNotIn("★", dash(QUIET))

    def test_every_line_fits_the_requested_width(self):
        for text in (DASH, QUIET):
            for w in (60, 80, 100):
                for line in dash(text, width=w).splitlines():
                    self.assertLessEqual(display_columns(line), w)


class QuestionPlacementTests(unittest.TestCase):
    """Presentation checks, not proof that a model interprets authority correctly."""

    def summary(self):
        return {
            "task": "Design the next change",
            "state": "Factual clarification pending; design not authorized",
            "this_session": "Clarify the conflicting reports. Design still needs approval.",
            "question": {"text": "Did you see the preview?",
                         "proposed": "The notes disagree; neither establishes what you saw.",
                         "reply": "Yes / No / Not sure"},
            "warnings": ["The log records a claim, not independent observation."],
            "source": "Current work and delivery notes",
        }

    def test_default_question_is_once_inside_you(self):
        out = view.render_dashboard(self.summary(), NOW, color=False)
        self.assertEqual(out.count("Did you see the preview?"), 1)
        self.assertIn("Did you see the preview?", out.split("YOU", 1)[1].split("╰", 1)[0])

    def test_question_below_is_once_outside_you_and_preserves_qualifications(self):
        for width in (50, 78, 100):
            out = view.render_dashboard(self.summary(), NOW, width, False, question_below=True)
            self.assertEqual(out.count("Did you see the preview?"), 1)
            self.assertNotIn("Did you see the preview?", out.split("YOU", 1)[1].split("╰", 1)[0])
            self.assertTrue(out.endswith("Did you see the preview?"))
            self.assertNotIn("Nothing needs you", out)
            plain = flatten(out.replace("│", " "))
            self.assertIn(self.summary()["this_session"], plain)
            self.assertIn(self.summary()["warnings"][0], plain)
            self.assertIn(self.summary()["question"]["proposed"], plain)
            for line in out.splitlines():
                self.assertLessEqual(display_columns(line), width)

    def test_question_below_without_question_does_not_invent_one(self):
        out = view.render_dashboard({}, NOW, color=False, question_below=True)
        self.assertIn("Nothing needs you right now.", out)
        self.assertNotIn("question below", out)

    def test_summary_cli_places_question_below(self):
        import json
        import subprocess
        result = subprocess.run([sys.executable, str(SCRIPT), "--summary", "-",
                                 "--question-below", "--no-color"],
                                input=json.dumps(self.summary()), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Did you see the preview?"), 1)
        self.assertTrue(result.stdout.rstrip().endswith("Did you see the preview?"))

    def test_record_cli_places_question_below(self):
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "work.md"
            path.write_text("# Preview\n\n## Now\n\nPending question: Did you see the preview?\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), "--record", str(path),
                                     "--dashboard", "--question-below", "--no-color"],
                                    text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("Did you see the preview?"), 1)
        self.assertTrue(result.stdout.rstrip().endswith("Did you see the preview?"))


class NothingFirstTests(unittest.TestCase):
    """A record writes "none." and then explains why. The word is the answer;
    the explanation is not a task."""

    def test_a_leading_none_is_read_as_no_task_and_its_reason_is_kept(self):
        text = QUIET.replace("Next action: pick the next slice",
                             "Current activity: none. The build is reviewed and pushed.\n"
                             "Next action: none. Left to ordinary use.")
        out = dash(text)
        self.assertIn("Not selected yet", out)
        self.assertIn("The build is reviewed and pushed.", out)
        self.assertNotIn("TASK    none.", out)

    def test_a_bare_none_still_carries_no_reason(self):
        out = dash(QUIET.replace("Next action: pick the next slice", "Next action: none"))
        self.assertIn(view.UNRECORDED, out)

    def test_a_value_merely_starting_with_a_word_like_nonetheless_is_untouched(self):
        out = dash(QUIET.replace("Next action: pick the next slice",
                                 "Next action: nonetheless ship it"))
        self.assertIn("nonetheless ship it", out)


PAUSED = """# Work: paused work

## Jobs

- [done] Agree the shape · producer
- [blocked] Ship the adapter — waiting on the producer's word

## Agreement

Agreed and paused.

## Now

Record updated: 2026-09-09 21:00 EDT
Phase: Controlled adoption
Pending question: none
"""

SELECTED_NONE = PAUSED.replace(
    "Pending question: none",
    "Current activity: none\nPending question: none").replace(
    "- [blocked] Ship the adapter — waiting on the producer's word\n", "")


class TaskHonestyTests(unittest.TestCase):
    """No current activity is not the same claim as no selected task."""

    def test_an_active_job_is_the_task_when_no_activity_field_exists(self):
        text = PAUSED.replace("- [blocked] Ship the adapter",
                              "- [active] Ship the adapter")
        out = dash(text)
        self.assertIn("Ship the adapter", out)
        self.assertNotIn("Not selected yet", out)

    def test_blocked_work_is_still_selected_work(self):
        out = dash(PAUSED)
        self.assertNotIn("Not selected yet", out)
        self.assertIn("Ship the adapter", out)
        self.assertIn("Blocked", out)

    def test_an_absent_activity_field_is_not_recorded_not_unselected(self):
        text = PAUSED.replace("- [blocked] Ship the adapter — waiting on the producer's word\n", "")
        out = dash(text)
        self.assertIn(view.UNRECORDED, out)
        self.assertNotIn("Not selected yet", out)

    def test_not_selected_needs_the_record_to_say_so_and_no_job_open(self):
        self.assertIn("Not selected yet", dash(SELECTED_NONE))


class BannerTests(unittest.TestCase):
    """The tick is a claim about the pickup, not about the render succeeding."""

    def test_direct_record_rendering_claims_no_session_restore(self):
        out = dash(DASH)
        self.assertNotIn("SESSION RESTORED", out)
        self.assertNotIn("✓", out.splitlines()[0])

    def test_a_completed_pickup_shows_the_green_tick(self):
        out = view.dashboard("record.md", DASH, NOW, 80, True, restored="yes")
        self.assertIn("SESSION RESTORED ✓", out)
        self.assertIn("\x1b[32m", out.splitlines()[0])

    def test_an_incomplete_pickup_says_so_and_is_not_green(self):
        out = view.dashboard("record.md", DASH, NOW, 80, True,
                             restored="partial", restore_note="TODO.md missing")
        self.assertIn("PICKUP INCOMPLETE", out)
        self.assertNotIn("\x1b[32m", out.splitlines()[0])
        self.assertIn("TODO.md missing", out)


class InMemorySummaryTests(unittest.TestCase):
    """Switch passes what it already read; no file is created for the dashboard."""

    def test_a_summary_renders_without_any_record_on_disk(self):
        out = view.render_dashboard({
            "phase": "Controlled adoption",
            "task": "Not selected yet",
            "state": "Setup choice pending",
            "last_session": "Built the view.",
            "this_session": "Nothing agreed yet.",
            "source": "CONTEXT.md, TODO.md, consolidation.md",
            "updated": "2026-09-09 21:00 EDT",
            "restored": "yes",
        }, NOW, 80, False)
        self.assertIn("Controlled adoption", out)
        self.assertIn("SESSION RESTORED", out)
        self.assertIn("CONTEXT.md, TODO.md, consolidation.md", out)

    def test_a_summary_omits_blocks_it_has_nothing_for(self):
        out = view.render_dashboard({"source": "consolidation.md"}, NOW, 80, False)
        self.assertNotIn("★", out)
        self.assertNotIn("⚠", out)
        self.assertIn(view.UNRECORDED, out)

    def test_summary_documents_are_still_checked_against_disk(self):
        out = view.render_dashboard(
            {"source": "x", "documents": [["Tasks", "nope-not-here.md"]]}, NOW, 80, False)
        self.assertIn("cannot be opened", out)

    def test_now_items_render_as_a_list_under_the_frame(self):
        """The immediate work is on screen; the backlog stays behind a link."""
        out = view.render_dashboard(
            {"source": "x", "now": ["Re-run the Codex route on 0.109.0",
                                    "Run one real Conductor session"]}, NOW, 80, False)
        self.assertIn(" NOW", out)
        self.assertIn("\u25cb Re-run the Codex route on 0.109.0", out)
        self.assertIn("\u25cb Run one real Conductor session", out)
        self.assertLess(out.index(" NOW"), out.index(" LAST SESSION"))

    def test_a_now_written_as_one_string_is_one_item_not_a_bullet_per_letter(self):
        out = view.render_dashboard({"source": "x", "now": "Close the gap"}, NOW, 80, False)
        self.assertIn("\u25cb Close the gap", out)
        self.assertNotIn("\u25cb C\n", out)

    def test_now_is_part_of_the_frame_so_an_empty_list_still_shows_the_label(self):
        out = view.render_dashboard({"source": "x"}, NOW, 80, False)
        self.assertIn(" NOW", out)
        self.assertIn("no immediate work recorded", out)


class DocumentedExampleTests(unittest.TestCase):
    """The guide's example is the renderer's input contract.

    Switch fills the shape from the example it already reads at pickup, never by
    inspecting this module. These checks bind on rendered VALUES, not on key
    lists: a field the renderer stops reading, or reads partially, fails here.
    """

    GUIDE = Path(__file__).resolve().parents[2] / "references" / "in-out.md"

    def example(self):
        import json, re
        blocks = re.findall(r"```json\n(.*?)```", self.GUIDE.read_text(), re.S)
        self.assertTrue(blocks, "in-out.md carries no json example for the renderer")
        return json.loads(blocks[0])

    def rendered(self, width=78):
        return view.render_dashboard(self.example(), NOW, width, False)

    def test_the_example_uses_only_keys_the_renderer_reads(self):
        unknown = set(self.example()) - set(view.SUMMARY_KEYS)
        self.assertFalse(unknown, f"example carries keys the renderer ignores: {unknown}")

    def test_the_example_shows_every_key_so_nothing_needs_looking_up(self):
        missing = set(view.SUMMARY_KEYS) - set(self.example())
        self.assertFalse(missing, f"example omits keys a caller would have to discover: {missing}")

    def test_every_documented_value_reaches_the_screen_in_full(self):
        """SUMMARY_KEYS is only a list, and a prefix match hides truncation.

        Wrapping is normalized away and the WHOLE value compared, so a narrative
        cut short — where the end of the sentence carries the qualification —
        fails here instead of passing on its first sixty characters.
        """
        out = flatten(self.rendered(100))
        example = self.example()
        checked = 0
        for key in ("phase", "task", "state", "last_session", "this_session",
                    "insight", "source", "updated"):
            value = example.get(key)
            if not value:
                continue
            self.assertIn(flatten(value), out, f"{key} is missing or cut short on screen")
            checked += 1
        self.assertGreaterEqual(checked, 7, "too few fields carry a value to test with")

    def test_the_complete_question_renders_inside_the_you_box(self):
        out = self.rendered(100)
        lines = out.splitlines()
        top = next(i for i, l in enumerate(lines) if l.startswith("╭─ YOU"))
        bottom = next(i for i, l in enumerate(lines[top:], top) if l.startswith("╰"))
        box = " ".join(l.strip("│ ").strip() for l in lines[top:bottom + 1])
        question = self.example()["question"]
        self.assertIn(question["text"], box, "the whole question must appear, not its first word")
        self.assertIn(question["proposed"], box)
        self.assertIn(question["reply"], box)

    def test_every_warning_and_document_reaches_the_screen(self):
        out = self.rendered(100)
        flat = flatten(out)
        for warning in self.example().get("warnings") or []:
            self.assertIn(flatten(warning), flat, "a warning is missing or cut short")
        for label, path in self.example().get("documents") or []:
            self.assertIn(label, out)
            self.assertIn(path, out)
        for item in self.example().get("now") or []:
            self.assertIn(flatten(item), flat, "a NOW item is missing or cut short")
        self.assertTrue(self.example().get("now"), "the example must show the NOW list")

    def test_the_example_does_not_contradict_itself(self):
        example = self.example()
        task, this = example.get("task") or "", example.get("this_session") or ""
        if task and task.lower() not in ("not selected yet", view.UNRECORDED):
            self.assertNotIn("nothing agreed", this.lower(),
                             "a selected task and an empty session contradict each other")

    def test_arrival_decisions_use_the_existing_you_box_once(self):
        # Content fixtures, not a claim that an LLM follows the arrival guide.
        for case in ("design", "unknown-stage", "continue", "pending", "no-task"):
            with self.subTest(case=case):
                summary = self.example()
                if case == "unknown-stage":
                    summary["phase"] = None
                elif case == "continue":
                    summary.update(state="Continuing under your explicit request",
                                   this_session="Design the alert; no deployment.", question=None)
                elif case == "pending":
                    summary.update(state="Decision pending", question={
                        "text": "Which channel should receive the alert?",
                        "proposed": "Use the existing operations channel; do not create a service.",
                        "reply": "Use it / Change"})
                elif case == "no-task":
                    summary.update(phase=None, task="Not selected yet", now=[],
                                   state="No saved next action", this_session="No work selected.",
                                   question=None)
                out = view.render_dashboard(summary, NOW, 78, False)
                lines = out.splitlines()
                top = next(i for i, line in enumerate(lines) if line.startswith("╭─ YOU"))
                bottom = next(i for i in range(top + 1, len(lines)) if lines[i].startswith("╰"))
                box = flatten(" ".join(line.strip("│ ") for line in lines[top + 1:bottom]))
                self.assertEqual(sum(line.strip() == "NOW" for line in lines), 1)
                self.assertNotIn("JOURNEY", out)
                question = summary["question"]
                if question:
                    for value in question.values():
                        self.assertIn(flatten(value), box)
                    self.assertNotIn("Nothing needs you", out)
                    self.assertEqual(flatten(out).count(flatten(question["text"])), 1)
                else:
                    self.assertIn("Nothing needs you right now", box)
                    self.assertNotIn("approve?", out)
                if case == "design":
                    self.assertIn("Implementation and deployment are not included in this approval.",
                                  flatten(out))
                if case in ("unknown-stage", "no-task"):
                    self.assertIn(view.UNRECORDED, out)


class ClosingBoxTests(unittest.TestCase):
    """Switch Out ends on one box that says how far the save reached.

    The box never claims the session exited or the context was cleared: a save
    is a Git fact, and the terminal the person is sitting in is still open.
    """

    GUIDE = Path(__file__).resolve().parents[2] / "references" / "in-out.md"

    def example(self):
        import json, re
        blocks = re.findall(r"```json\n(.*?)```", self.GUIDE.read_text(), re.S)
        self.assertGreaterEqual(len(blocks), 2, "in-out.md carries no json example for the closing box")
        return json.loads(blocks[1])

    def base(self, **over):
        summary = {"project": "Kerd", "branch": "main", "saved": "remote-verified",
                   "commit": "2e59ab7", "files": 15, "remote": "origin/main",
                   "local_only": ["kerd-laptop-result.patch"], "tree": "clean",
                   "closed": "2026-09-12 12:40 EDT",
                   "next": "Run one real Conductor session on 0.112.0.",
                   "reading_set": ["CONTEXT.md", "TODO.md ## Now", "kivna/sessions/2026-09-12.md"],
                   "measured": "23,482 bytes, about 5,871 tokens estimated, within the 8,000 target",
                   "log": "kivna/sessions/2026-09-12.md"}
        summary.update(over)
        return summary

    def test_remote_verified_save_shows_the_saved_banner_and_every_field(self):
        out = view.render_closing(self.base(), NOW, 80, False)
        flat = flatten(out)
        self.assertIn("SESSION SAVED", out)
        for value in ("origin/main", "2e59ab7", "15 files", "kerd-laptop-result.patch", "clean",
                      "2026-09-12 12:40 EDT", "Run one real Conductor session on 0.112.0.",
                      "TODO.md ## Now", "23,482 bytes", "kivna/sessions/2026-09-12.md"):
            self.assertIn(flatten(value), flat, f"{value!r} missing or cut short on screen")

    def test_the_three_save_states_are_told_apart_and_never_confused_with_exit(self):
        for saved, banner, absent in (("remote-verified", "SESSION SAVED", "NOT ON THE REMOTE"),
                                      ("committed", "SAVED LOCALLY", "SESSION SAVED"),
                                      ("not-saved", "NOT SAVED", "SESSION SAVED")):
            with self.subTest(saved=saved):
                out = view.render_closing(self.base(saved=saved), NOW, 80, False)
                self.assertIn(banner, out)
                self.assertNotIn(absent, out)
                self.assertNotIn("exited", out.lower())
                self.assertNotIn("cleared", out.lower())
                self.assertIn("still open", out)

    def test_the_free_context_hint_follows_only_a_confirmed_save(self):
        for saved, hint in (("remote-verified", "Free context"), ("committed", "Free context"),
                            ("not-saved", "resolve the save"), (None, "resolve the save"),
                            ("something-else", "resolve the save")):
            with self.subTest(saved=saved):
                out = view.render_closing(self.base(saved=saved), NOW, 80, False)
                self.assertIn(hint, out)
                self.assertIn("still open", out)
                if hint != "Free context":
                    self.assertNotIn("/clear", out)

    def test_an_unknown_save_status_is_not_reported_as_nothing_committed(self):
        for summary in ({}, {"saved": "weird"}, self.base(saved=None)):
            with self.subTest(summary=summary):
                out = view.render_closing(summary, NOW, 80, False)
                self.assertIn("SAVE STATUS NOT RECORDED", out)
                self.assertNotIn("nothing committed", out)
                self.assertNotIn("NOT SAVED", out)
                self.assertNotIn("SESSION SAVED", out)

    def test_every_line_including_a_long_log_path_fits_the_width(self):
        long_log = "docs/work/" + "long-work-name-" * 7 + "/session.md"
        for width in (78, 100):
            out = view.render_closing(self.base(log=long_log), NOW, width, False)
            over = [line for line in out.splitlines() if len(line) > width]
            self.assertFalse(over, f"lines wider than {width}: {over}")
            # A path has no spaces to wrap at, so compare with all whitespace removed.
            self.assertIn("".join(long_log.split()), "".join(out.split()))

    def test_a_committed_but_unpushed_save_says_so_in_words(self):
        out = view.render_closing(self.base(saved="committed"), NOW, 80, False)
        self.assertIn("not verified on the remote", flatten(out))

    def test_confirmed_save_hint_does_not_assume_a_claude_slash_command(self):
        out = flatten(view.render_closing(self.base(), NOW, 80, False))
        self.assertIn("start a new conversation in your client", out)
        self.assertIn("then ask Kerd to switch in", out)
        self.assertNotIn("/clear", out)

    def test_local_only_leftovers_and_a_dirty_tree_are_named_not_hidden(self):
        out = view.render_closing(self.base(tree="2 unassigned changes left, not saved",
                                            local_only=["a.patch", "b/__pycache__/"]), NOW, 80, False)
        flat = flatten(out)
        self.assertIn("2 unassigned changes left, not saved", flat)
        self.assertIn("a.patch", flat); self.assertIn("b/__pycache__/", flat)

    def test_missing_fields_degrade_to_not_recorded_rather_than_crashing(self):
        out = view.render_closing({"saved": "remote-verified"}, NOW, 80, False)
        self.assertIn(view.UNRECORDED, out)
        self.assertIn("SESSION SAVED", out)
        self.assertNotIn("files)", out)

    def test_the_guide_example_uses_only_keys_the_renderer_reads_and_all_reach_the_screen(self):
        example = self.example()
        unknown = set(example) - set(view.CLOSING_KEYS)
        self.assertFalse(unknown, f"example carries keys the renderer ignores: {unknown}")
        missing = set(view.CLOSING_KEYS) - set(example)
        self.assertFalse(missing, f"example omits keys a caller would have to discover: {missing}")
        out = flatten(view.render_closing(example, NOW, 100, False))
        for key in ("commit", "remote", "tree", "closed", "next", "measured", "log"):
            self.assertIn(flatten(str(example[key])), out, f"{key} is missing or cut short on screen")
        for item in example["local_only"] + example["reading_set"]:
            self.assertIn(flatten(item), out)

    def test_the_cli_reads_the_closing_summary_from_stdin(self):
        import json, subprocess
        result = subprocess.run([sys.executable, str(Path(view.__file__)), "--closing", "-", "--no-color"],
                                input=json.dumps(self.base()), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SESSION SAVED", result.stdout)


class OmissionContractTests(unittest.TestCase):
    """What the guide promises about absent fields must match what runs."""

    def test_an_empty_summary_renders_without_claiming_a_source(self):
        out = view.render_dashboard({}, NOW, 78, False)
        self.assertNotIn("None", out, "an absent source must not print as None")
        self.assertIn(view.UNRECORDED, out)

    def test_blocks_that_always_appear_do_so_even_when_empty(self):
        out = view.render_dashboard({}, NOW, 78, False)
        for always in ("PHASE", "TASK", "STATE", "LAST SESSION", "THIS SESSION", "YOU"):
            self.assertIn(always, out)

    def test_blocks_that_are_omitted_when_empty_are_absent(self):
        out = view.render_dashboard({}, NOW, 78, False)
        for omitted in ("⚠", "DOCUMENTS", "★"):
            self.assertNotIn(omitted, out)
