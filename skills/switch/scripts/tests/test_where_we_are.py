"""What the view may and may not say about a record."""

import importlib.util
import re
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
        # A clean record's source time must not be later than the fixture clock.
        self.assertNotIn("⚠", dash(QUIET.replace("21:00 EDT", "12:00 EDT")))

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
            tail = out.split("read:", 1)[1].split("END OF PICKUP", 1)[0]
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


class TimestampOrderTests(unittest.TestCase):
    def test_future_source_time_is_flagged_without_rewriting_it(self):
        source = "2026-09-12 22:27 EDT"
        out = view.render_dashboard({"updated": source}, "2026-09-12 22:26 EDT", color=False)
        self.assertIn("NEEDS ATTENTION", out)
        self.assertIn("Source update time sorts after render time", flatten(out.replace("│", " ")))
        self.assertIn(source, out)
        self.assertIn("rendered 2026-09-12 22:26 EDT", out)

    def test_equal_or_earlier_source_time_needs_no_warning(self):
        for source in ("2026-09-12 22:26 EDT", "2026-09-11 23:59 EDT"):
            out = view.render_dashboard({"updated": source}, "2026-09-12 22:26 EDT", color=False)
            self.assertNotIn("NEEDS ATTENTION", out)

    def test_unknown_or_incomparable_times_are_not_guessed(self):
        for source in (None, "", "yesterday", "2026-02-30 22:27 EDT",
                       "2026-09-12 22:27 UTC", "2026-09-12T22:27:00Z", 123):
            out = view.render_dashboard({"updated": source}, "2026-09-12 22:26 EDT", color=False)
            self.assertNotIn("NEEDS ATTENTION", out)
        self.assertIn("updated unknown", view.render_dashboard({}, NOW, color=False))

    def test_warning_keeps_existing_warning_and_one_question(self):
        summary = {"updated": "2026-09-12 22:27 EDT", "warnings": ["Setup not approved."],
                   "question": {"text": "Which project should be used?"}}
        out = view.render_dashboard(summary, "2026-09-12 22:26 EDT", 50, False, True)
        self.assertIn("Setup not approved.", out)
        self.assertEqual(out.count("Which project should be used?"), 1)
        self.assertEqual(summary["warnings"], ["Setup not approved."])
        for line in out.splitlines():
            self.assertLessEqual(display_columns(line), 50)


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

    def test_default_question_is_once_after_end(self):
        out = view.render_dashboard(self.summary(), NOW, color=False)
        self.assertEqual(out.count("Did you see the preview?"), 1)
        self.assertIn("Did you see the preview?", out.split("END OF PICKUP", 1)[1])

    def test_question_below_is_once_outside_you_and_preserves_qualifications(self):
        for width in (50, 78, 100):
            out = view.render_dashboard(self.summary(), NOW, width, False, question_below=True)
            self.assertEqual(out.count("Did you see the preview?"), 1)
            self.assertNotIn("Did you see the preview?", out.split("END OF PICKUP", 1)[0])
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
        self.assertNotIn("─ YOU", out)
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
        self.assertIn("1. Re-run the Codex route on 0.109.0", out)
        self.assertIn("2. Run one real Conductor session", out)
        self.assertLess(out.index(" NOW"), out.index(" LAST SESSION"))

    def test_a_now_written_as_one_string_is_one_item_not_a_bullet_per_letter(self):
        out = view.render_dashboard({"source": "x", "now": "Close the gap"}, NOW, 80, False)
        self.assertIn("1. Close the gap", out)
        self.assertNotIn("2. ", out)

    def test_now_is_part_of_the_frame_so_an_empty_list_still_shows_the_label(self):
        out = view.render_dashboard({"source": "x"}, NOW, 80, False)
        self.assertIn(" NOW", out)
        self.assertIn("no immediate work recorded", out)


class RecommendationTests(unittest.TestCase):
    def summary(self):
        return {"restored": "yes", "question": {
            "text": "Can you run these checks on Master now?",
            "proposed": "At Master, check the installed build.\n\n"
                        "1. Open Review on a folder containing rushes/.\n"
                        "2. Check oldest-first order and that Keep or Mark advances once.\n\n"
                        "No build, install or deploy. Report only checks you actually ran.",
            "reply": "Yes / No / Later"}}

    def test_recommendation_preserves_spacing_steps_and_limits_in_both_modes(self):
        for markdown in (False, True):
            for width in (40, 64, 78):
                out = view.render_dashboard(self.summary(), NOW, width, False,
                                            question_below=True, markdown=markdown)
                section = out.split('Scope / recommendation', 1)[1].split('END OF PICKUP', 1)[0]
                rows = section.splitlines()
                content = flatten(MarkdownTests.visible(section))
                self.assertIn(flatten(self.summary()['question']['proposed']), content)
                self.assertNotIn('─ YOU', out)
                self.assertGreaterEqual(sum(not row.strip() for row in rows), 3)
                self.assertIn('1. Open Review', MarkdownTests.visible(section))
                self.assertNotIn('Reply:', out)
                self.assertNotIn('Yes / No / Later', out)
                self.assertNotIn('Your answer is needed', out)
                end = flatten(MarkdownTests.visible(out.split('END OF PICKUP', 1)[1])).rstrip('*')
                self.assertTrue(end.endswith(self.summary()['question']['text']))
                self.assertEqual(flatten(MarkdownTests.visible(out)).count(self.summary()['question']['text']), 1)
                if not markdown:
                    self.assertTrue(all(display_columns(row) <= width for row in rows))

    def test_wrapped_number_and_bullet_lines_have_hanging_indent(self):
        for prefix in ('1. ', '12. ', '- ', '* '):
            rows = view.recommendation_rows(prefix + 'a long action with an important final qualification', 24)
            self.assertTrue(rows[0].startswith(prefix))
            self.assertTrue(all(row.startswith(' ' * len(prefix)) for row in rows[1:]))
            self.assertIn('final qualification', flatten(' '.join(rows)))

    def test_wide_characters_fit_without_losing_steps(self):
        rows = view.recommendation_rows('1. 檢查所有的步驟並保留最後的限制條件', 18)
        self.assertTrue(all(display_columns(row) <= 18 for row in rows))
        self.assertEqual(''.join(row.strip() for row in rows).replace('1. ', ''),
                         '檢查所有的步驟並保留最後的限制條件')

    def test_legacy_single_paragraph_is_not_invented_as_a_checklist(self):
        text = 'Review the design only. No implementation is authorized.'
        rows = view.recommendation_rows(text, 40)
        self.assertEqual(flatten(' '.join(rows)), text)
        self.assertFalse(any(row.startswith('1.') for row in rows))

    def test_documented_proposal_keeps_steps_and_restrictions(self):
        summary = DocumentedExampleTests().example()
        out = view.render_dashboard(summary, NOW, markdown=True)
        content = flatten(MarkdownTests.visible(out))
        self.assertIsNone(summary['question']['proposed'])
        self.assertIn(flatten(summary['recommendation']['why']), content)
        self.assertNotIn('Scope / recommendation', out)
        self.assertNotIn('reply', summary['question'])


class TeamTests(unittest.TestCase):
    def test_plain_colon_text_does_not_become_an_owner(self):
        items = ["Deferred until rows 1-5 carry evidence: a fresh Codex Switch In",
                 "Note: the time is 14:30",
                 "Record the result on rows 1, 2 and 4: the version loaded"]
        out = view.render_dashboard({"now": items}, NOW, markdown=True)
        for i, item in enumerate(items, 1):
            self.assertIn(f"{i}. {item}", out)
        self.assertNotIn("**Note", out)
        self.assertNotIn("**Deferred", out)
        self.assertNotIn("**Record", out)

    def test_actual_helper_undefined_role_has_no_nested_parentheses(self):
        rows = view.team_rows([dict(provider="codex", id="sample",
                                   role="established partner (role not defined)")])
        self.assertEqual(rows, [("TEAM", "Codex (partner · role unassigned)", None)])

    def test_explicit_owner_has_no_markdown_in_terminal(self):
        out = view.render_dashboard({"now": ["**Anthony:** Assess the arrival."]}, NOW, color=False)
        self.assertIn("1. Anthony: Assess the arrival.", out)
        self.assertNotIn("**", out)

    def test_legacy_proposal_keeps_real_markdown_list_structure(self):
        text = "Check only.\n\n1. First check.\n2. Final check.\n\nNo deployment."
        out = view.render_dashboard({"question": {"text": "Can you check now?", "proposed": text}},
                                    NOW, markdown=True)
        self.assertIn("\n  1. First check.\n  2. Final check.\n", out)
        self.assertIn("\n\n  No deployment.\n", out)
        self.assertNotIn("1\\.", out)

    def test_owner_labels_are_emphasized_without_assigning_missing_owners(self):
        out = view.render_dashboard({"now": [
            "**Anthony:** Assess this arrival.",
            "**Claude · after assessment:** Record the verdict.",
            "**Owner unassigned:** Run the clarification check.",
            "Review the remaining design"]}, NOW, markdown=True)
        for expected in (
            "1. **Anthony:** Assess this arrival.",
            "2. **Claude · after assessment:** Record the verdict.",
            "3. **Owner unassigned:** Run the clarification check.",
            "4. Review the remaining design"):
            self.assertIn(expected, out)
        self.assertNotIn("─ YOU", out)
        self.assertNotIn("💬", out)

    def test_question_callout_escapes_markup_and_keeps_whole_question(self):
        question = "Can you check **all** cases\nwithout deploying?"
        out = view.render_dashboard({"restored": "yes", "question": {"text": question}},
                                    NOW, markdown=True)
        ending = out.rsplit("```", 1)[1].strip()
        self.assertEqual(ending, "> 💬 **Can you check \\*\\*all\\*\\* cases without deploying?**")
        self.assertNotIn("─ YOU", out)
        self.assertEqual(out.count("💬"), 1)

    def test_one_roster_line_without_ids_or_routine_notice_status(self):
        team = [
            dict(provider="claude", id="12345678-aaaa", role="arrival & closeout", self=True),
            dict(provider="codex", id="87654321-bbbb", status="submitted-unconfirmed")]
        for markdown in (False, True):
            out = view.render_dashboard(dict(team=team), NOW, color=False, markdown=markdown)
            text = flatten(out.replace("│", ""))
            self.assertIn("Claude (arrival & closeout) + Codex (partner · role unassigned)", text)
            self.assertNotIn("12345678", out)
            self.assertNotIn("87654321", out)
            self.assertNotIn("PEER", out)
            self.assertNotIn("submitted", out)
            self.assertEqual(out.count("TEAM"), 1)

    def test_duplicate_identity_groups_but_same_provider_different_members_survive(self):
        member = dict(provider="claude", id="one", role="Reviewer")
        rows = view.team_rows([member, member, dict(provider="claude", id="two", role="Builder")])
        self.assertEqual(rows, [("TEAM", "Claude (Reviewer) + Claude (Builder)", None)])

    def test_unknown_empty_and_unselected_are_distinct(self):
        self.assertIn("not recorded", view.team_rows(None)[0][1])
        self.assertIn("No established pairing", view.team_rows([])[0][1])
        self.assertIn("recipient not selected", view.team_rows([dict(provider="codex")])[0][1])

    def test_actionable_routing_warning_is_preserved_when_supplied(self):
        warning = "Review cannot be routed: established Claude partner is unavailable."
        out = view.render_dashboard(dict(warnings=[warning]), NOW, markdown=True)
        self.assertIn(warning, MarkdownTests.visible(out))
        self.assertIn("**ATTENTION**", out)


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
        unknown = set(self.example()) - set(view.OPEN_WORK_KEYS)
        self.assertFalse(unknown, f"example carries keys the arrival ignores: {unknown}")

    def test_the_example_shows_every_key_so_nothing_needs_looking_up(self):
        missing = set(view.OPEN_WORK_KEYS) - set(self.example())
        self.assertFalse(missing, f"example omits keys a caller would have to discover: {missing}")

    def test_every_documented_value_reaches_the_screen_in_full(self):
        """Wrapping is normalized away and the WHOLE value compared, so a
        sentence cut short, where the end carries the qualification, fails."""
        example = self.example()
        for width in (78, 100):
            with self.subTest(width=width):
                out = flatten(view.render_dashboard(example, NOW, width, False))
                values = [example[key] for key in ("where", "phase", "last_session", "insight")]
                values += [item.replace("**", "") for item in example["open_work"]]
                values += [example["recommendation"]["text"], example["recommendation"]["why"]]
                for value in values:
                    self.assertIn(flatten(value), out, f"{value[:40]!r} is missing or cut short")

    def test_markdown_shows_open_work_and_one_recommendation_with_why(self):
        example = self.example()
        out = view.render_dashboard(example, NOW, 100, False, markdown=True)
        before = out.split("💬", 1)[0]
        self.assertIn("**Open work**", before)
        for index, _ in enumerate(example["open_work"], 1):
            self.assertIn(f"\n{index}. ", before)
        self.assertEqual(before.count("**Recommended:**"), 1)
        self.assertEqual(before.count("**Why:**"), 1)
        self.assertLess(before.index("**Open work**"), before.index("**Recommended:**"))
        # The grid leads, with phase and next; no copied saved step.
        self.assertTrue(out.split("\n")[2].startswith("| PROJECT | PHASE | NEXT | TEAM |"))
        self.assertIn(f"| {example['phase']} | {example['recommendation']['text']} |", out)
        self.assertNotIn("**NOW**", out)
        self.assertNotIn("THIS SESSION", out)

    def test_the_question_ends_the_screen_once_with_no_footer(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = view.render_dashboard(self.example(), NOW, 100, False, markdown=markdown)
                question = self.example()["question"]["text"]
                self.assertTrue(out.rstrip().rstrip("*").endswith(question))
                self.assertEqual(out.count(question), 1)
                self.assertEqual(out.count("💬"), 1)
                for gone in ("END OF PICKUP", "rendered", "Read:", "read:"):
                    self.assertNotIn(gone, out)

    def test_every_warning_and_document_reaches_the_screen(self):
        out = view.render_dashboard(self.example(), NOW, 100, False)
        flat = flatten(out)
        for warning in self.example().get("warnings") or []:
            self.assertIn(flatten(warning), flat, "a warning is missing or cut short")
        for label, path in self.example().get("documents") or []:
            self.assertIn(label, out)
            self.assertIn(path, out)

    def test_an_incomplete_or_unconfirmed_arrival_says_so_without_an_end_marker(self):
        for restored, heading, note in (("partial", "SWITCH IN INCOMPLETE", "Missing context"),
                                        (None, "SWITCH IN STATUS UNKNOWN", "Restoration not confirmed.")):
            for markdown in (False, True):
                with self.subTest(restored=restored, markdown=markdown):
                    summary = self.example()
                    summary.update(restored=restored, restore_note=None)
                    out = view.render_dashboard(summary, NOW, 78, False, markdown=markdown)
                    self.assertIn(heading, out)
                    self.assertIn(note, out)
                    self.assertNotIn("SWITCH IN COMPLETE", out)
                    self.assertNotIn("END OF PICKUP", out)

    def test_the_example_asks_to_start_a_conductor_session(self):
        question = self.example()["question"]
        self.assertEqual(question["text"], "Start a Conductor session?")
        self.assertIsNone(question.get("proposed"))

    def test_nothing_open_says_so_rather_than_inventing_work(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                summary = self.example()
                summary.update(open_work=[], recommendation=None)
                out = view.render_dashboard(summary, NOW, 78, False, markdown=markdown)
                self.assertIn("No open work is recorded.", out)
                self.assertIn("No recommendation: nothing actionable is open.", out)

    def test_every_line_fits_the_requested_width(self):
        for width in (60, 78):
            with self.subTest(width=width):
                out = view.render_dashboard(self.example(), NOW, width, False)
                self.assertTrue(all(view.columns(line) <= width for line in out.splitlines()))

    def test_null_open_work_and_recommendation_keep_the_new_layout(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                summary = self.example()
                summary.update(open_work=None, recommendation=None)
                out = view.render_dashboard(summary, NOW, 78, False, markdown=markdown)
                self.assertIn("No open work is recorded.", out)
                self.assertIn("Nothing actionable is open", out)
                self.assertNotIn("**NOW**", out)
                self.assertNotIn("THIS SESSION", out)

    def test_a_why_without_a_recommendation_is_not_shown(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                summary = self.example()
                summary["recommendation"] = {"text": None, "why": "orphan reason"}
                out = view.render_dashboard(summary, NOW, 78, False, markdown=markdown)
                self.assertIn("No recommendation: nothing actionable is open.", out)
                self.assertNotIn("orphan reason", out)

    def test_long_team_and_project_name_fit_the_width_without_being_cut(self):
        summary = self.example()
        summary["project"] = "A very long project name that cannot share its line"
        summary["team"] = [{"provider": "claude", "id": str(n), "role": "a long descriptive role " * 2}
                           for n in range(3)]
        out = view.render_dashboard(summary, NOW, 60, False)
        self.assertTrue(all(view.columns(line) <= 60 for line in out.splitlines()))
        self.assertIn("SWITCH IN COMPLETE", out)
        self.assertIn("CANNOT SHARE ITS LINE", flatten(out))

    def test_open_work_as_one_string_is_one_item(self):
        summary = self.example()
        summary["open_work"] = "Sign off the migration"
        out = view.render_dashboard(summary, NOW, 78, False)
        self.assertIn("1. Sign off the migration", out)
        self.assertNotIn("2. ", out)

    def test_legacy_summary_without_open_work_keeps_the_grid(self):
        legacy = {"project": "Kerd", "phase": "p", "now": ["**Claude:** do x"],
                  "question": {"text": "Start a Conductor session?", "proposed": None},
                  "restored": "yes"}
        out = view.render_dashboard(legacy, NOW, 100, False, markdown=True)
        self.assertIn("| PROJECT | PHASE | STATE | TEAM |", out)
        self.assertIn("**NOW**", out)


class ClosingBoxTests(unittest.TestCase):
    """Switch Out ends on a grid, this session's changes, the next step with
    its reason, and one closing line.

    Save mechanics stay in the records; a save problem is shown under Attention
    whenever it is true. The box never claims the session exited or the
    context was cleared, and never offers /clear before a confirmed save with
    memory ready.
    """

    GUIDE = Path(__file__).resolve().parents[2] / "references" / "in-out.md"

    def example(self):
        import json, re
        blocks = re.findall(r"```json\n(.*?)```", self.GUIDE.read_text(), re.S)
        self.assertGreaterEqual(len(blocks), 2, "in-out.md carries no json example for the closing box")
        return json.loads(blocks[1])

    def base(self, **over):
        summary = {"project": "Kerd", "branch": "main", "saved": "remote-verified", "handoff_ready": True,
                   "boundary": "passed", "phase": "Launch: 2 of 5 done", "released": "0.136.0 → 0.138.0",
                   "this_session": ["The risk-rating change was accepted.",
                                    "Conductor checks where your work stands in your own project."],
                   "next": "Start the diagnostic pilot.",
                   "why": "It is the first real work item driven in someone else's project.",
                   "tree": "clean", "warnings": [], "host": "claude"}
        summary.update(over)
        return summary

    def render(self, markdown, **over):
        return view.render_closing(self.base(**over), NOW, 80, False, markdown=markdown)

    def test_a_confirmed_save_shows_the_grid_changes_next_and_why(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = flatten(self.render(markdown))
                self.assertIn("SESSION SAVED", out)
                for value in ("Pushed to main", "Launch: 2 of 5 done", "0.136.0 → 0.138.0",
                              "Start the diagnostic pilot.",
                              "The risk-rating change was accepted.",
                              "Conductor checks where your work stands in your own project.",
                              "It is the first real work item driven in someone else's project."):
                    self.assertIn(flatten(value), out)
                self.assertNotIn("ATTENTION", out)

    def test_the_grid_leads_the_markdown_box(self):
        out = self.render(True)
        self.assertEqual(out.split("\n")[2], "| PROJECT | SAVED | PHASE | RELEASED |")
        self.assertIn("| Kerd | Pushed to main | Launch: 2 of 5 done | 0.136.0 → 0.138.0 |", out)

    def test_the_next_step_appears_once(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                self.assertEqual(self.render(markdown).count("Start the diagnostic pilot."), 1)
        self.assertIn("| Nothing released |", self.render(True, released=None))

    def test_the_closing_line_is_last_and_names_the_restart(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = self.render(markdown).rstrip()
                self.assertTrue(flatten(out).endswith(
                    "Exit and restart or /clear and /kerd:switch in to pick up from here."))

    def test_under_codex_the_closing_line_names_no_claude_command(self):
        for host in ("codex", "Codex", "codex-cli", "something"):
            with self.subTest(host=host):
                out = flatten(self.render(True, host=host))
                self.assertTrue(out.endswith("Exit and restart, then switch in to pick up from here."))
                self.assertNotIn("/clear", out)
        for host in ("claude", "Claude", None):
            with self.subTest(host=host):
                self.assertIn("/clear", flatten(self.render(True, host=host)))

    def test_a_failed_save_under_codex_still_keeps_the_session_open(self):
        out = flatten(self.render(True, host="codex", saved="not-saved"))
        self.assertIn("Keep this session open", out)
        self.assertNotIn("Exit and restart", out)

    def test_a_dirty_tree_or_a_warning_alone_raises_attention(self):
        for over in ({"tree": "2 files left, not saved"}, {"warnings": ["Designation failed."]}):
            for markdown in (False, True):
                with self.subTest(over=over, markdown=markdown):
                    out = self.render(markdown, **over)
                    self.assertIn("ATTENTION", out)
                    body = out.split("ATTENTION", 1)[1]
                    self.assertIn(flatten(str(list(over.values())[0]).strip("[]'")), flatten(body))
        for tree in ("clean", "Clean", "clean."):
            with self.subTest(tree=tree):
                self.assertNotIn("ATTENTION", self.render(True, tree=tree))

    def test_a_pushed_save_without_a_branch_does_not_say_not_recorded(self):
        out = self.render(True, branch=None)
        self.assertIn("| Pushed |", out)

    def test_save_mechanics_stay_off_the_screen(self):
        out = self.render(True, commit="2e59ab7", files=15, remote="origin/main",
                          local_only=["kerd-laptop-result.patch"], measured="23,482 bytes",
                          reading_set=["CONTEXT.md"], log="kivna/sessions/2026-09-12.md",
                          closed="2026-09-12 12:40 EDT")
        for gone in ("2e59ab7", "15 files", "origin/main", "kerd-laptop-result.patch", "23,482",
                     "READ FIRST", "LOG", "Rendered", "MEMORY", "TREE"):
            self.assertNotIn(gone, out)

    def test_the_save_states_are_told_apart_and_never_confused_with_exit(self):
        for saved, banner, cell, absent in (("remote-verified", "SESSION SAVED", "Pushed to main", "NOT SAVED"),
                                            ("committed", "SAVED LOCALLY", "Committed, not pushed", "SESSION SAVED"),
                                            ("not-saved", "NOT SAVED", "Not saved", "SESSION SAVED")):
            for markdown in (False, True):
                with self.subTest(saved=saved, markdown=markdown):
                    out = self.render(markdown, saved=saved)
                    self.assertIn(banner, out)
                    self.assertIn(cell, out)
                    self.assertNotIn(absent, out)
                    self.assertNotIn("exited", out.lower())
                    self.assertNotIn("cleared", out.lower().replace("before clearing", ""))

    def test_a_save_problem_is_named_under_attention(self):
        for saved, words in (("committed", "not verified on the remote"),
                             ("not-saved", "Nothing was committed"),
                             (None, "save status was not recorded")):
            for markdown in (False, True):
                with self.subTest(saved=saved, markdown=markdown):
                    out = flatten(self.render(markdown, saved=saved))
                    self.assertIn("ATTENTION", out)
                    self.assertIn(words, out)

    def test_restart_is_offered_only_after_a_confirmed_save_with_memory_ready(self):
        for markdown in (False, True):
            for saved in ("remote-verified", "committed", "not-saved", None, "weird"):
                for ready in (True, False, None, "true", 1):
                    with self.subTest(markdown=markdown, saved=saved, ready=ready):
                        out = flatten(self.render(markdown, saved=saved, handoff_ready=ready))
                        allowed = saved in ("remote-verified", "committed") and ready is True
                        self.assertEqual("/clear" in out, allowed)
                        self.assertEqual("Exit and restart" in out, allowed)
                        if not allowed:
                            self.assertIn("Keep this session open", out)
                        if ready is False:
                            self.assertIn("Memory for the next session is incomplete", out)
                        elif ready is not True:
                            self.assertIn("memory is ready for the next session was not recorded", out)

    def test_the_tick_and_restart_wait_for_a_passed_boundary_check(self):
        failure = "No remote branch contains this commit; the work exists only on this machine."
        for boundary, words in ((None, "boundary check was not recorded"),
                                ("weird", "Boundary check failed: weird"),
                                ([failure], failure), (failure, failure)):
            for markdown in (False, True):
                with self.subTest(boundary=boundary, markdown=markdown):
                    out = flatten(self.render(markdown, boundary=boundary))
                    self.assertNotIn("\u2713", out)
                    self.assertNotIn("Exit and restart", out)
                    self.assertIn("Keep this session open and resolve the boundary check", out)
                    self.assertIn("ATTENTION", out)
                    if markdown:  # the terminal panel wraps long lines inside its border
                        self.assertIn(flatten(words), out.split("ATTENTION", 1)[1])
        summary = self.base()
        del summary["boundary"]
        self.assertNotIn("Exit and restart", view.render_closing(summary, NOW, 80, False))
        self.assertIn("SESSION SAVED \u2713", self.render(True))

    def test_a_stash_count_in_warnings_does_not_withhold_the_restart(self):
        out = flatten(self.render(True, warnings=["2 stashes on this machine, not saved."]))
        self.assertIn("2 stashes on this machine", out)
        self.assertIn("Exit and restart", out)

    def test_an_unknown_save_status_is_not_reported_as_nothing_committed(self):
        for summary in ({}, {"saved": "weird"}, self.base(saved=None)):
            with self.subTest(summary=summary):
                out = view.render_closing(summary, NOW, 80, False)
                self.assertIn("SAVE STATUS NOT RECORDED", out)
                self.assertNotIn("Nothing was committed", out)
                self.assertNotIn("NOT SAVED", out)
                self.assertNotIn("SESSION SAVED", out)

    def test_a_dirty_tree_and_warnings_are_named_not_hidden(self):
        out = flatten(self.render(True, tree="2 unassigned changes left, not saved",
                                  warnings=["Role designation failed; pairing recovery unavailable."]))
        self.assertIn("2 unassigned changes left, not saved", out)
        self.assertIn("Role designation failed; pairing recovery unavailable.", out)

    def test_every_line_fits_the_width(self):
        long_change = "A very long description of what changed " * 5
        for width in (60, 78, 100):
            out = view.render_closing(self.base(this_session=[long_change], saved="committed"),
                                      NOW, width, False)
            over = [line for line in out.splitlines() if view.columns(line) > width]
            self.assertFalse(over, f"lines wider than {width}: {over}")
            self.assertIn(flatten(long_change), flatten(out))

    def test_missing_fields_degrade_to_not_recorded_rather_than_crashing(self):
        out = view.render_closing({"saved": "remote-verified", "handoff_ready": True}, NOW, 80, False)
        self.assertIn(view.UNRECORDED, out)
        self.assertIn("Nothing recorded.", out)
        self.assertIn("SESSION SAVED", out)

    def test_the_guide_example_uses_only_keys_the_renderer_reads_and_all_reach_the_screen(self):
        example = self.example()
        unknown = set(example) - set(view.CLOSING_KEYS)
        self.assertFalse(unknown, f"example carries keys the renderer ignores: {unknown}")
        missing = set(view.CLOSING_KEYS) - set(example)
        self.assertFalse(missing, f"example omits keys a caller would have to discover: {missing}")
        out = flatten(view.render_closing(example, NOW, 100, False, markdown=True))
        for key in ("project", "phase", "released", "next", "why"):
            self.assertIn(flatten(str(example[key])), out, f"{key} is missing or cut short on screen")
        for item in example["this_session"]:
            self.assertIn(flatten(item), out)

    def test_the_cli_reads_the_closing_summary_from_stdin(self):
        import json, subprocess
        result = subprocess.run([sys.executable, str(Path(view.__file__)), "--closing", "-", "--no-color"],
                                input=json.dumps(self.base()), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SESSION SAVED", result.stdout)


class MarkdownTests(unittest.TestCase):
    def test_grid_has_four_cells_and_untrusted_values_cannot_add_columns(self):
        summary = self.arrival(project="A | B\n### injected", phase="Build `x|y`",
                               state="<b>Waiting</b>",
                               team=[dict(provider="claude", id="private-id", role="Build | review")])
        out = view.render_dashboard(summary, NOW, markdown=True)
        rows = [line for line in out.splitlines() if line.startswith("|")]
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], "| PROJECT | PHASE | STATE | TEAM |")
        self.assertEqual(len(re.split(r"(?<!\\)\|", rows[2])), 6)
        for value in ("A | B ### injected", "Build `x|y`", "<b>Waiting</b>", "Build | review"):
            self.assertIn(value, self.visible(rows[2]))
        self.assertNotIn("private-id", out)

    def test_three_sections_are_bullets_with_actions_nested_under_now(self):
        out = view.render_dashboard(self.arrival(task=None, task_reason=None,
            now=["**Anthony:** Check the result.", "**Claude:** Record the verdict."]), NOW, markdown=True)
        self.assertIn("- **LAST SESSION**\n\n  Built the first slice", out)
        self.assertIn("- **THIS SESSION**\n\n  Review the full change", out)
        self.assertIn("- **NOW**\n\n  1. **Anthony:** Check the result.\n  2. **Claude:** Record the verdict.", out)
        self.assertNotIn("Focus:", out)
        self.assertNotIn("┌", out)
        self.assertNotIn("─ YOU", out)

    def test_legacy_task_context_survives_without_inventing_an_action(self):
        out = view.render_dashboard(self.arrival(now=[], task="Await approval", task_reason="Never deploy."),
                                    NOW, markdown=True)
        self.assertIn("  Focus: Await approval", out)
        self.assertIn("  Task context: Never deploy.", out)
        self.assertIn("no immediate work recorded", out)
        self.assertNotIn("  1.", out)

    def test_task_already_named_in_now_does_not_repeat_as_focus(self):
        out = view.render_dashboard(self.arrival(task="Check the view", task_reason="No release.",
                                    now=["**Anthony:** Check the view"]), NOW, markdown=True)
        self.assertNotIn("Focus:", out)
        self.assertIn("Task context: No release.", out)

    def test_task_is_not_hidden_by_negative_or_qualified_mentions(self):
        for now in (["**Claude:** Design the alert"], ["**Claude:** Deploy the alert only after approval"]):
            out = view.render_dashboard(self.arrival(task="Deploy the alert", task_reason=None,
                this_session="Proposed: design; deploy the alert is not included.", now=now),
                NOW, markdown=True)
            self.assertIn("  Focus: Deploy the alert", out)
            self.assertIn("deploy the alert is not included.", out)

    @staticmethod
    def visible(text):
        import re
        # CommonMark punctuation escapes, independently decoded for full-value checks.
        return re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])", r"\1", text)

    def arrival(self, **over):
        summary = {"project": "Example project", "restored": "yes", "phase": "Testing", "task": "Check the view",
                   "state": "Review pending", "task_reason": "No release yet.",
                   "state_reason": "Waiting for evidence, not permission.",
                   "now": ["Review", "Correct findings"],
                   "last_session": "Built the first slice, not released.",
                   "this_session": "Review the full change, without editing it.",
                   "warnings": ["Device verification remains unobserved."],
                   "question": {"text": "Which project should receive the install?",
                                "proposed": "Use the existing test project only.",
                                "reply": "Name the project"},
                   "insight": "An accepted queue message is not a completed review.",
                   "source": "TODO.md ## Now", "updated": "2026-09-09 12:00 EDT"}
        summary.update(over)
        return summary

    @staticmethod
    def text_of_box(out, title):
        lines = out.splitlines()
        start = next(i for i, line in enumerate(lines) if line.startswith("┌─ " + title))
        end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("└"))
        return flatten(" ".join(line.strip("│ ") for line in lines[start + 1:end]))

    def test_arrival_preserves_complete_values_and_bounds_the_question_once(self):
        summary = self.arrival()
        out = view.render_dashboard(summary, NOW, markdown=True)
        visible = self.visible(out)
        all_text = flatten(" ".join(line.strip("│ ") for line in visible.splitlines()))
        for key in ("project", "phase", "task", "state", "task_reason", "state_reason",
                    "last_session", "this_session", "insight", "source", "updated"):
            self.assertIn(summary[key], all_text)
        for value in summary["now"] + summary["warnings"]:
            self.assertIn(value, visible)
        you = visible.split("END OF PICKUP", 1)[0]
        self.assertIn(summary["question"]["proposed"], you)
        self.assertNotIn(summary["question"]["reply"], you)
        self.assertNotIn(summary["question"]["text"], you)
        self.assertEqual(visible.count(summary["question"]["text"]), 1)
        self.assertIn("**KERD · SWITCH IN COMPLETE ✓ · Kerd " + view.kerd_version() + "**", out)
        self.assertIn("- **LAST SESSION**\n\n  ", out)
        self.assertIn("> **★ Insight**", out)
        self.assertNotIn("\x1b", out)
        self.assertTrue(out.startswith("**KERD · SWITCH IN"))
        self.assertTrue(visible.endswith("━━ END OF PICKUP · SESSION READY ━━\n```\n\n"
                                         + "> 💬 **" + summary["question"]["text"] + "**"))

    def test_markdown_cli_question_is_first_content_after_end_without_opt_in(self):
        import json, subprocess
        question = "Can you approve this dashboard now?"
        for restored in ("yes", "partial", None):
            summary = self.arrival(restored=restored, question={
                "text": question, "proposed": "Judge the presentation only, not the implementation.",
                "reply": "Approve or describe what needs changing"})
            result = subprocess.run([sys.executable, str(SCRIPT), "--summary", "-", "--markdown"],
                                    input=json.dumps(summary), text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            out = self.visible(result.stdout)
            self.assertEqual(out.rsplit("```", 1)[1].strip(), "> 💬 **" + question + "**")
            self.assertEqual(out.count(question), 1)
            self.assertIn(summary["question"]["proposed"], out.split("END OF PICKUP", 1)[0])

    def test_markdown_without_a_question_stops_at_end(self):
        for question in (None, {}, {"text": ""}):
            out = view.render_dashboard(self.arrival(question=question), NOW, markdown=True)
            self.assertTrue(out.endswith("━━ END OF PICKUP · SESSION READY ━━\n```"))
            self.assertNotIn("─ YOU", out)

    def test_now_numbers_supplied_priority_order_without_reordering_or_dropping(self):
        items = [f"Action {i}: preserve the full scope and qualification for this step."
                 for i in range(1, 13)]
        for markdown in (False, True):
            out = self.visible(view.render_dashboard(self.arrival(now=items), NOW,
                                                     width=40, color=False, markdown=markdown))
            section = out.split("**NOW**\n" if markdown else " NOW\n", 1)[1]
            section = section.split("**ATTENTION**" if markdown else " LAST SESSION", 1)[0]
            positions = []
            for i, item in enumerate(items, 1):
                expected = f"{i}. {item}"
                plain = flatten(section.replace('**', ''))
                self.assertIn(expected, plain)
                positions.append(plain.index(expected))
            self.assertEqual(positions, sorted(positions))
            if not markdown:
                self.assertTrue(all(display_columns(line) <= 40 for line in section.splitlines()))

    def test_question_below_retains_context_and_asks_once_outside_you(self):
        summary = self.arrival()
        out = self.visible(view.render_dashboard(summary, NOW, question_below=True, markdown=True))
        question = summary["question"]["text"]
        self.assertEqual(out.count(question), 1)
        self.assertTrue(out.endswith(question + "**"))
        you = out.split("END OF PICKUP", 1)[0]
        self.assertNotIn(question, you)
        self.assertIn(summary["question"]["proposed"], you)

    def test_long_arrival_lines_retain_their_qualifying_endings(self):
        summary = self.arrival(
            now=["Owed: read the device settings, report the build and its differences; "
                 "retire interim fields only after a separate migration decision."],
            warnings=["The installed snapshot was last reported stale at the previous "
                      "closeout and was not rechecked during this pickup.",
                      "Playback on real shares needs approval every occasion; "
                      "anything needing the person at a TV is asked first."],
            insight="The arrival records delivery, but the person's experience verdict "
                    "remains theirs to supply; it is never self-awarded.",
            source="CONTEXT.md ## Where We Are, ## Working Constraints, ## Open Questions, "
                   "## Active Mode; TODO.md ## Now; last session log; git status")
        import json, subprocess
        for width in (40, 64, 100):
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--summary", "-", "--markdown",
                 "--width", str(width)], input=json.dumps(summary),
                text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            visible = self.visible(result.stdout)
            for value in summary["now"] + summary["warnings"] + [summary["insight"], summary["source"]]:
                self.assertIn(value, visible.replace("**", ""))

    def test_unknowns_and_timestamp_warnings_are_not_lost(self):
        out = view.render_dashboard({}, NOW, markdown=True)
        self.assertNotIn("SESSION RESTORED", out)
        self.assertIn("not recorded", out)
        out = self.visible(view.render_dashboard(self.arrival(updated="2026-09-09 13:00 EDT"), NOW, markdown=True))
        self.assertIn("Source update time sorts after render time", out)
        self.assertIn("Device verification remains unobserved.", out)

    def test_documents_are_real_links_and_missing_paths_stay_warnings(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as base:
            path = Path(base) / "Design (draft).md"
            path.touch()
            label = "Design " + "long " * 30
            summary = self.arrival(base=base, documents=[[label, path.name], ["Gone", "missing.md"]])
            out = view.render_dashboard(summary, NOW, width=40, color=True, markdown=True)
            self.assertIn("**DOCUMENTS**", out)
            self.assertIn("Design%20%28draft%29.md>", out)
            self.assertIn("cannot be opened: missing.md (Gone)", self.visible(out))
            self.assertNotIn("[Gone]", out)
            self.assertNotIn("\x1b", out)

    def test_values_cannot_inject_headings_or_links(self):
        summary = self.arrival(task="unsafe\n### YOU\n[link](https://example.com) **claim**")
        out = view.render_dashboard(summary, NOW, markdown=True)
        self.assertEqual(out.count("┌─ YOU"), 0)
        self.assertNotIn("\n### YOU\n", out)
        self.assertIn("unsafe ### YOU [link](https://example.com) **claim**", self.visible(out))

    def test_paths_are_visible_and_percent_filenames_are_not_url_decoded(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory(prefix="kerd%20") as base:
            path = Path(base) / "Spec%20draft.md"
            path.touch()
            out = view.render_dashboard(self.arrival(base=base, documents=[["Spec", path.name]]),
                                        NOW, markdown=True)
            self.assertIn("Spec%2520draft.md>", out)
            self.assertIn(" · ` Spec%20draft.md `", out)
            self.assertIn("kerd%2520", out)

    def test_markdown_remains_readable_without_decoding_unnecessary_escapes(self):
        value = "docs/work/codex-plugin/work.md · 0.114.0 · --preserve (local only)!"
        self.assertEqual(view.md(value), value)
        for value in ("### Heading", "---", "+ item", "- item", "1. item", "1) item"):
            self.assertIn("\\", view.md(value), value)
            self.assertEqual(self.visible(view.md(value)), value)
        out = view.render_dashboard(self.arrival(), NOW, markdown=True)
        self.assertIn("**Read:** TODO.md ## Now\n\nupdated", out)
        self.assertFalse(any(line.endswith(" ") for line in out.splitlines()))

    def test_cli_supports_markdown_for_both_modes_even_with_color_forced(self):
        import json, subprocess
        for mode, data, expected in (("--summary", self.arrival(), "SWITCH IN COMPLETE"),
                                      ("--closing", ClosingBoxTests().base(), "**KERD · SESSION SAVED ✓**")):
            result = subprocess.run([sys.executable, str(SCRIPT), mode, "-", "--markdown", "--color"],
                                    input=json.dumps(data), text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(expected, result.stdout)
            self.assertNotIn("\x1b", result.stdout)

    def test_compact_layout_order_and_width(self):
        for width in (40, 52, 80):
            out = view.render_dashboard(self.arrival(documents=[["Design", "https://example.com/design"]]),
                                        NOW, width=width, markdown=True)
            order = ["**KERD", "| PROJECT | PHASE | STATE | TEAM |", "- **LAST SESSION**", "- **THIS SESSION**", "- **NOW**",
                     "**ATTENTION**", "**DOCUMENTS**", "END OF PICKUP"]
            positions = [out.index(label) for label in order]
            self.assertEqual(positions, sorted(positions))
            box = [line for line in out.splitlines() if line.startswith(("┌", "│", "└"))]
            self.assertFalse(box, "arrival must not reintroduce boxes")
            self.assertIn("| Example project | Testing |", out)
            self.assertNotIn("\x1b", out)

    def test_completion_is_not_changed_by_dirty_tree_or_missing_log_warning(self):
        summary = self.arrival(warnings=["Dirty tree; push not authorized.",
                                        "No log, but required context recovered from work record."])
        out = view.render_dashboard(summary, NOW, markdown=True)
        self.assertIn("SWITCH IN COMPLETE", out)
        self.assertIn("END OF PICKUP · SESSION READY", out)
        for state in ("partial", "no", None, "weird"):
            out = view.render_dashboard(dict(summary, restored=state, restore_note="Missing scope ruling."),
                                        NOW, markdown=True)
            self.assertNotIn("SWITCH IN COMPLETE", out)
            self.assertNotIn("SESSION READY", out)
            self.assertIn("Missing scope ruling.", out)

    def test_backticks_in_values_cannot_introduce_fences(self):
        out = view.render_dashboard(self.arrival(task="Keep ``` literal"), NOW, markdown=True)
        self.assertTrue(out.startswith("**KERD"))
        self.assertIn("Keep ``` literal", self.visible(out))
        self.assertEqual(out.count("```"), 2, "only the END marker is fenced")


class MemoryReadinessTests(unittest.TestCase):
    def test_git_save_and_memory_readiness_are_independent(self):
        for markdown in (False, True):
            for saved in ("remote-verified", "committed", "not-saved", None):
                for ready in (True, False, None, "true", 1):
                    with self.subTest(markdown=markdown, saved=saved, ready=ready):
                        summary = ClosingBoxTests().base(saved=saved, handoff_ready=ready,
                            next="Recover the partner's unrecorded verification limits before resuming.")
                        out = flatten(view.render_closing(summary, NOW, color=False, markdown=markdown))
                        allowed = saved in ("remote-verified", "committed") and ready is True
                        self.assertEqual("Exit and restart" in out, allowed)
                        if not allowed:
                            self.assertIn("Keep this session open", out)
                        if saved == "remote-verified":
                            self.assertIn("SESSION SAVED", out)
                        self.assertIn(summary["next"], out)
                        if ready is False:
                            self.assertIn("Memory for the next session is incomplete", out)
                        elif ready is not True:
                            self.assertIn("was not recorded", out)

class OmissionContractTests(unittest.TestCase):
    """What the guide promises about absent fields must match what runs."""

    def test_an_empty_summary_renders_without_claiming_a_source(self):
        out = view.render_dashboard({}, NOW, 78, False)
        self.assertNotIn("None", out, "an absent source must not print as None")
        self.assertIn(view.UNRECORDED, out)

    def test_blocks_that_always_appear_do_so_even_when_empty(self):
        out = view.render_dashboard({}, NOW, 78, False)
        for always in ("PHASE", "TASK", "STATE", "LAST SESSION", "THIS SESSION", "TEAM", "NOW"):
            self.assertIn(always, out)

    def test_blocks_that_are_omitted_when_empty_are_absent(self):
        out = view.render_dashboard({}, NOW, 78, False)
        for omitted in ("⚠", "DOCUMENTS", "★"):
            self.assertNotIn(omitted, out)


class KerdVersionTests(unittest.TestCase):
    """The arrival names the Kerd build that drew it, read from the package's
    own manifest, so nobody has to guess which build a pickup came from."""

    ARRIVAL = {"project": "Seinn", "restored": "yes", "where": "Plays video.",
               "open_work": ["Decide the endorsement model."],
               "recommendation": {"text": "Shape the endorsement model.", "why": "It blocks release."}}

    def package(self, directory, manifests):
        import shutil
        scripts = Path(directory) / "skills" / "switch" / "scripts"
        scripts.mkdir(parents=True)
        shutil.copy(SCRIPT, scripts / "where_we_are.py")
        for name, text in manifests.items():
            (Path(directory) / name).mkdir()
            (Path(directory) / name / "plugin.json").write_text(text, encoding="utf-8")
        spec = importlib.util.spec_from_file_location("where_we_are_packaged", scripts / "where_we_are.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_the_arrival_names_the_version_its_package_declares(self):
        import tempfile
        for manifest in (".claude-plugin", ".codex-plugin"):
            with tempfile.TemporaryDirectory() as directory:
                module = self.package(directory, {manifest: '{"name": "kerd", "version": "9.8.7"}'})
                out = module.render_dashboard(self.ARRIVAL, NOW, markdown=True)
                self.assertIn("**SEINN · SWITCH IN COMPLETE ✓ · Kerd 9.8.7**", out)
                self.assertIn("Kerd 9.8.7", module.render_dashboard(self.ARRIVAL, NOW, 80, False))

    def test_an_unreadable_version_is_said_not_guessed(self):
        import tempfile
        for manifests in ({}, {".claude-plugin": "not json"}, {".claude-plugin": '{"version": ""}'}):
            with tempfile.TemporaryDirectory() as directory:
                out = self.package(directory, manifests).render_dashboard(self.ARRIVAL, NOW, markdown=True)
                self.assertIn("SWITCH IN COMPLETE ✓ · Kerd version not read", out)

    def test_the_older_grid_names_the_version_too(self):
        import tempfile
        older = {"project": "Seinn", "restored": "yes", "task": "Check the view", "state": "Ready"}
        with tempfile.TemporaryDirectory() as directory:
            module = self.package(directory, {".claude-plugin": '{"version": "9.8.7"}'})
            self.assertIn("**KERD · SWITCH IN COMPLETE ✓ · Kerd 9.8.7**",
                          module.render_dashboard(older, NOW, markdown=True))
            self.assertIn("KERD · Kerd 9.8.7", module.render_dashboard(older, NOW, 80, False))
        with tempfile.TemporaryDirectory() as directory:
            module = self.package(directory, {})
            self.assertIn("Kerd version not read", module.render_dashboard(older, NOW, markdown=True))
            self.assertIn("Kerd version not read", module.render_dashboard(older, NOW, 80, False))

    def test_this_checkout_reports_its_own_release(self):
        import json
        declared = json.loads((SCRIPT.parents[3] / ".claude-plugin" / "plugin.json").read_text())["version"]
        self.assertEqual(view.kerd_version(), declared)
