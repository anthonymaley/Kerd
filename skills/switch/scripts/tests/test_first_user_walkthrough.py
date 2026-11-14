"""Breaks a first outside user met in Switch, from the 2026-11-13 walkthrough.

A simulated newcomer ("Pat") on a small project with no remote and no Kerd
records found: Out said keep the session open forever (finding 1), Out wrote no
session log or TODO.md (4), the first arrival was an empty grid (5), the owner
line used a real name (10), the closing box showed escaped backticks (15) and
PHASE read "not recorded" after Out recorded one (16). The renderer checks run
the code; the guide checks find the wording, not that a model follows it.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[4]
SWITCH = ROOT / "skills/switch"
SCRIPT = SWITCH / "scripts" / "where_we_are.py"
SPEC = importlib.util.spec_from_file_location("where_we_are_first_user", SCRIPT)
view = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(view)

NOW = "2026-11-13 22:00 EST"
RESTART = "Run /clear, then /kerd:switch in to pick up from here."
# First-user round 3 (#5): plain words, never a claim that no backup exists.
LOCAL_LINE = "Saved on this computer only; no other copy was checked."
FIRST_LINE = ("Kerd has nothing saved here yet. Tell me what you want to work on and "
              "Conductor will shape it with you.")


def flat(text):
    return " ".join(text.split())


def guide(rel):
    return flat((SWITCH / rel).read_text(encoding="utf-8"))


def closing(**over):
    summary = {"project": "Tally", "branch": "main", "saved": "committed", "handoff_ready": True,
               "boundary": "local_only", "verdicts": {"project": "local_only"},
               "phase": "Spreadsheet export done",
               "released": None, "this_session": ["Tally can save your list as a spreadsheet."],
               "next": "Export one customer's requests.", "why": "You may want it next week.",
               "next_in": [], "tree": "clean", "warnings": [], "host": "claude"}
    summary.update(over)
    return summary


class NoRemoteOutTests(unittest.TestCase):
    """Finding 1: with no remote, a committed clean save is a confirmed local save."""

    def test_local_only_shows_one_plain_line_and_the_restart(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = view.render_closing(closing(), NOW, 80, False, markdown=markdown)
                text = flat(out)
                self.assertTrue(text.endswith(RESTART))
                self.assertEqual(text.count(LOCAL_LINE), 1)
                self.assertIn("SAVED LOCALLY", out)
                self.assertNotIn("✓", out)
                lowered = text.lower()
                for gone in ("failed", "push", "keep this session open", "boundary check"):
                    self.assertNotIn(gone, lowered)
                self.assertIn("Saved on this computer", out)
                self.assertNotIn("Committed on this computer", out)
                self.assertNotIn("remote", lowered)

    def test_a_remote_with_an_unpushed_commit_is_unchanged(self):
        failures = ["No branch on a configured remote, as checked by this fetch, contains this commit."]
        for boundary in (failures, ["The fetch failed, so the remote state is unknown; "
                                    "cached refs are not verification."] + failures):
            for markdown in (False, True):
                with self.subTest(boundary=boundary, markdown=markdown):
                    text = flat(view.render_closing(closing(boundary=boundary), NOW, 80, False,
                                                    markdown=markdown))
                    self.assertNotIn(RESTART, text)
                    self.assertNotIn(LOCAL_LINE, text)
                    self.assertIn("not yet copied to your remote (committed, not pushed)", text)
                    self.assertIn("Keep this session open and resolve the boundary check", text)
                    if markdown:  # the terminal panel wraps long lines inside its border
                        self.assertIn("push before switching devices", text)
                        self.assertIn("Boundary check failed: " + failures[0], text)

    def test_local_only_waits_for_memory_and_a_save(self):
        text = flat(view.render_closing(closing(handoff_ready=False), NOW, 80, False, markdown=True))
        self.assertNotIn(RESTART, text)
        self.assertIn("Keep this session open and resolve the missing handoff context", text)
        text = flat(view.render_closing(closing(saved="not-saved"), NOW, 80, False, markdown=True))
        self.assertNotIn(RESTART, text)
        self.assertIn("Keep this session open and resolve the save", text)
        self.assertNotIn(LOCAL_LINE, text)

    def test_a_pushed_project_with_a_local_only_vault_says_which_part_is_local(self):
        # Review rounds 2 and 3: the line comes from the check's per-repo
        # verdicts, not from `saved`; the save is confirmed, no tick.
        text = flat(view.render_closing(closing(saved="remote-verified",
                                                verdicts={"project": "ok", "notes": "local_only"}),
                                        NOW, 80, False, markdown=True))
        self.assertTrue(text.endswith(RESTART))
        self.assertIn("your notes are saved on this computer only; no other copy was checked", text.lower())
        self.assertNotIn(LOCAL_LINE, text)
        self.assertNotIn("✓", text)

    def test_the_guides_name_local_only(self):
        out = guide("references/out.md")
        for phrase in (
            "has nowhere to push: save without `--push`",
            "(`git remote` succeeds and prints nothing; a failed read is not “no remote”)",
            "A vault with no remote configured is saved without `--push`, by the same rule.",
            "that repo's verdict is `local_only`. A repo that has a remote keeps every check",
            "For the project that line is “Saved on this computer only; no other copy was checked.”, "
            "which never claims no backup exists;",
            "or after a committed or remote-verified save with `handoff_ready: true` and "
            "`boundary: \"local_only\"`",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, out)
        for gone in ("backup elsewhere", "Git has no remote copy"):
            self.assertNotIn(gone, out)
        skill = guide("SKILL.md")
        self.assertIn("a project or vault with no remote configured records `local_only`, seen as "
                      "`boundary_local_only`", skill)
        self.assertIn("or a committed or remote-verified save with `handoff_ready: true` and "
                      "`boundary: \"local_only\"`", skill)

    def test_every_repo_gets_a_verdict_and_reads_fail_closed(self):
        # Review round 2, items 2 and 3, and the fail-closed sweep.
        out = guide("references/out.md")
        for phrase in (
            "The result's `verdicts` names each repo's verdict (`ok`, `local_only` or `refused`), and the "
            "combined status is `boundary_ok` only when every repo is `ok`, `boundary_local_only` (exit 0) "
            "when none is refused and at least one is `local_only`, and `boundary_refused` otherwise.",
            "A git read that fails stops the check with no verdict",
            "Missing means a successful read found it absent; a path that exists but cannot be read is not "
            "missing, so Out does not write over it and names it in `warnings` instead.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, out)

    def test_the_measure_example_is_labelled_as_the_ordinary_case(self):
        # Review round 2, item 5.
        out = guide("references/out.md")
        self.assertIn("The example below is the ordinary case, with both `TODO.md` and the session log "
                      "present; when either could not be created, use the adjusted selection from "
                      "[When the session log or TODO.md is missing](#out) instead:", out)
        self.assertIn("For the example above (both files present) it is:", out)


    def test_one_rule_maps_status_and_exit_code(self):
        # Review round 1, item 5: no sentence may map every exit 0 to passed.
        out = guide("references/out.md")
        for phrase in (
            "read from the status and exit code of that call's own result, both together:",
            "- `status: \"boundary_ok\"` with exit 0 → `passed`: the ✓ and the restart line.",
            "- `status: \"boundary_local_only\"` with exit 0 (every repo committed and clean, at least one "
            "with no Git remote configured) → `local_only`: no ✓,",
            "- Anything else (another status, a nonzero exit, a status not seen) → not ready:",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, out)
        for gone in ("exactly `passed` when it exited 0", "the verdict is `passed` only when"):
            with self.subTest(gone=gone):
                self.assertNotIn(gone, out)


    def test_the_lines_follow_the_verdicts(self):
        notes_line = "your notes are saved on this computer only; no other copy was checked"
        both = flat(view.render_closing(closing(verdicts={"project": "local_only", "notes": "local_only"}),
                                        NOW, 80, False, markdown=True))
        self.assertIn(LOCAL_LINE, both)
        self.assertIn(notes_line, both.lower())
        self.assertTrue(both.endswith(RESTART))
        # A committed project already on its remote, with a local-only vault:
        # no project line and no "push" line, since the check found HEAD there.
        mixed = flat(view.render_closing(closing(verdicts={"project": "ok", "notes": "local_only"}),
                                         NOW, 80, False, markdown=True))
        self.assertNotIn(LOCAL_LINE, mixed)
        self.assertIn(notes_line, mixed.lower())
        self.assertNotIn("push before", mixed)
        self.assertTrue(mixed.endswith(RESTART))

    def test_missing_or_incomplete_verdicts_withhold_the_restart(self):
        # Final cross-cutting review, item 4: without a complete per-repo result
        # a local-only save is not confirmed, and the box says what is missing.
        for verdicts in ("absent", None, "local_only", [], {}, {"notes": "local_only"},
                         {"project": "maybe"}, {"project": "local_only", "other": "ok"}):
            with self.subTest(verdicts=verdicts):
                summary = closing()
                if verdicts == "absent":
                    del summary["verdicts"]
                else:
                    summary["verdicts"] = verdicts
                for markdown in (False, True):
                    text = flat(view.render_closing(summary, NOW, 80, False, markdown=markdown))
                    self.assertNotIn(RESTART, text)
                    self.assertNotIn(LOCAL_LINE, text)
                    self.assertTrue(text.endswith("Keep this session open and record the boundary check's "
                                                  "per-repo verdicts before clearing context."))
                    if markdown:  # the terminal panel wraps long lines inside its border
                        self.assertIn("per-repo verdicts were not recorded (or lack the project's), so which "
                                      "repo is saved only on this computer is unknown and the save is not "
                                      "confirmed.", text)

    def test_verdicts_that_contradict_the_save_withhold_the_restart(self):
        for over in ({"saved": "remote-verified", "verdicts": {"project": "local_only"}},
                     {"verdicts": {"project": "local_only", "notes": "refused"}},
                     {"verdicts": {"project": "ok"}}):
            with self.subTest(over=over):
                text = flat(view.render_closing(closing(**over), NOW, 80, False, markdown=True))
                self.assertNotIn(RESTART, text)
                self.assertIn("per-repo verdicts do not match this save", text)

    def test_the_guide_passes_the_verdicts(self):
        out = guide("references/out.md")
        for phrase in (
            "Copy the check's `verdicts` object into the box as it reads",
            "the renderer picks the lines from it, not from `saved`",
            "vault.json counts as absent only when it does not exist; a directory, an unreadable file or "
            "anything other than a JSON object stops the check rather than skipping the vault.",
            "After every repo is checked, it reads vault.json and each repo's HEAD, remote names and "
            "settings and unsaved paths again, and any change refuses.",
            "Only remote-tracking refs this fetch refreshes count as holding the commit: those a configured "
            "remote's fetch refspec writes. A leftover ref from a removed remote, or one outside the "
            "refspec, proves nothing.",
            "Each remote is fetched by name. Kerd does not model every Git fetch rule: a remote with a "
            "negative fetch refspec (`^…`) or `skipDefaultUpdate` set makes the check refuse",
            "push and confirm by hand.”, and a refspec Git itself rejects stops the check with no verdict.",
            "Without a complete `verdicts` (missing, malformed or without the project's verdict) a "
            "local-only save is not confirmed: no restart line, and the box names the missing verdicts.",
            "(a detached HEAD is reported as no branch, not a failure)",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, out)


class MissingRecordsOutTests(unittest.TestCase):
    """Finding 4: Out creates the session log and TODO.md when they are missing."""

    def test_out_creates_and_names_them(self):
        out = guide("references/out.md")
        for phrase in (
            "**When the session log or TODO.md is missing.**",
            "Out creates what is missing: `kivna/sessions/<date>.md`",
            "a minimal `TODO.md` whose `## Now` section holds the open items Out saves",
            "(or the line “Nothing open.” when there are none, so the section is never empty)",
            "name them in the box's `this_session` in plain words",
            "If either cannot be created, say so in `warnings` with the reason",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, out)
        self.assertIn("A missing `kivna/sessions/<date>.md` or `TODO.md` (with a `## Now` section) is "
                      "created by Out and named in the box", guide("SKILL.md"))


    def test_when_they_cannot_be_created_the_reading_set_uses_what_exists(self):
        # Review round 1, item 1: the failure path, not only the happy one.
        out = guide("references/out.md")
        for phrase in (
            "The reading set and the `measure` call then name only records that exist:",
            "leave the missing file out of `--file` and `--section` rather than naming a path "
            "`measure` cannot read.",
            "Carry what it would have held into a record that does exist",
            "and measure again.",
            "When no existing record can carry them, so a fresh reader could not recover the open "
            "work and next action, set `handoff_ready: false` and name the gap in `next`.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, out)


class FirstArrivalTests(unittest.TestCase):
    """Finding 5: a project with no Kerd records gets one line, not an empty grid."""

    SUMMARY = {"project": "Tally", "phase": None, "where": None, "open_work": [], "recommendation": None,
               "last_session": None, "team": [], "documents": [], "warnings": [], "insight": None,
               "question": {"text": "Start a Conductor session?", "proposed": None},
               "base": ".", "restored": "yes", "restore_note": None, "first_arrival": True}

    def test_one_line_replaces_the_grid_and_the_question_still_ends_it(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = view.render_dashboard(dict(self.SUMMARY), NOW, 80, False, markdown=markdown)
                text = flat(out)
                self.assertIn(FIRST_LINE, text)
                self.assertTrue(text.rstrip("*").endswith("What do you want to work on?"))
                self.assertNotIn("Start a Conductor session?", out)
                for gone in ("PHASE", "NEXT", "TEAM", "No established pairing", "not recorded",
                             "No open work is recorded", "No recommendation"):
                    self.assertNotIn(gone, out)
                self.assertIn("TALLY", out)
                self.assertIn("SWITCH IN COMPLETE", out)

    def test_the_line_fits_the_width(self):
        out = view.render_dashboard(dict(self.SUMMARY), NOW, 40, False)
        self.assertTrue(all(view.columns(line) <= 40 for line in out.splitlines()))

    def test_false_or_absent_keeps_the_grid(self):
        for value in (False, None):
            with self.subTest(value=value):
                out = view.render_dashboard(dict(self.SUMMARY, first_arrival=value), NOW, 80, False,
                                            markdown=True)
                self.assertIn("| PROJECT | PHASE | NEXT |", out)
                self.assertNotIn(FIRST_LINE, flat(out))

    def test_the_skill_description_names_the_exception(self):
        # Review round 2, item 8.
        import re
        text = (SWITCH / "SKILL.md").read_text(encoding="utf-8")
        description = re.search(r'^description: "(.*)"$', text, re.M).group(1)
        self.assertIn("a project/phase/next/team grid (one plain line instead where Kerd has no records)",
                      description)
        self.assertLessEqual(len(description), 1024)

    def test_the_guide_says_when(self):
        text = guide("references/in.md")
        self.assertIn("set `first_arrival: true` and `restored: \"yes\"`", text)
        # Review round 1, items 7 and 8: the evidence, and the exception to "always render".
        for phrase in (
            "only when successful reads confirm that `CONTEXT.md`, `TODO.md` and `kivna/sessions/` "
            "are all absent and no work record is linked or known.",
            "A location that cannot be inspected (an unreadable folder, a failed read) is not absence: "
            "use `restored: \"partial\"` with the gap in `restore_note`, and never `first_arrival`.",
            "except on a first arrival (`first_arrival: true`), where the one plain line replaces them all;",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertIn("“Kerd has nothing saved here yet. Tell me what you want to work on and "
                      "Conductor will shape it with you.”", text)


class OwnerIsYouTests(unittest.TestCase):
    """Finding 10: the person at the keyboard is "You:", never taught a real name."""

    def test_no_real_name_in_the_examples(self):
        for rel in ("references/in.md", "references/out.md"):
            with self.subTest(rel=rel):
                text = guide(rel)
                self.assertNotIn("Anthony:", text)
                self.assertNotIn("Tony:", text)

    def test_owner_placeholders_say_you(self):
        text = guide("references/in.md")
        self.assertNotIn("<Person>", text)
        self.assertIn("“You: retire N stale pairings (<aliases or count>), set aside, recoverable”", text)
        self.assertIn("“You: look at the Codex <role> window", text)

    def test_the_rule_is_stated(self):
        text = guide("references/in.md")
        self.assertIn("The person at the keyboard is “You:”, not their name, nickname or account name.", text)
        self.assertIn("A named owner appears only when the records name someone else as that item's owner.",
                      text)
        self.assertIn("(“You: check the stats panel on the TV”)", text)


class InlineCodeTests(unittest.TestCase):
    """Finding 15: a command in a box value renders as code, not as \\` escapes."""

    def test_code_spans_pass_through(self):
        value = "Run `python3 tally.py export` for a dated file, `requests-YYYY-MM-DD.csv`."
        self.assertEqual(view.md(value), value)
        box = view.render_closing(closing(this_session=[value]), NOW, 80, False, markdown=True)
        self.assertIn(value, box)
        self.assertNotIn("\\`", box)

    def test_text_around_code_is_still_escaped(self):
        self.assertEqual(view.md("*bold* `a_b` [x]"), "\\*bold\\* `a_b` \\[x\\]")
        self.assertEqual(view.md("# Heading `x`"), "\\# Heading `x`")
        self.assertEqual(view.md("`x` # not a heading"), "`x` # not a heading")

    def test_unsafe_or_unmatched_backticks_stay_escaped(self):
        for value, expected in (("Keep ``` literal", "Keep \\`\\`\\` literal"),
                                ("a `b", "a \\`b"),
                                ("cells `a | b`", "cells \\`a \\| b\\`"),
                                ("empty `` here", "empty \\`\\` here")):
            with self.subTest(value=value):
                self.assertEqual(view.md(value), expected)

    def test_a_longer_fence_holds_a_backtick(self):
        self.assertEqual(view.md("use `` a`b `` here"), "use `` a`b `` here")

    def test_cli_closing_box_from_the_walkthrough(self):
        data = closing(this_session=["Tally can now save your request list as a spreadsheet file: run "
                                     "`python3 tally.py export` for a dated file, `requests-YYYY-MM-DD.csv`."])
        result = subprocess.run([sys.executable, str(SCRIPT), "--closing", "-", "--markdown"],
                                input=json.dumps(data), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("run `python3 tally.py export` for a dated file", result.stdout)
        self.assertNotIn("\\`", result.stdout)


class HandoverExampleTests(unittest.TestCase):
    """P2 review: model/effort evidence is for dispatched jobs, not inline work."""

    def test_model_effort_evidence_is_conditional(self):
        text = guide("references/in.md")
        self.assertIn("with current model/effort evidence only for jobs dispatched to contributors "
                      "(one task Conductor does itself gets one plain line instead)", text)
        self.assertNotIn("Shape, current model/effort evidence, owner", text)


class PhaseCarriesTests(unittest.TestCase):
    """Finding 16: Out's phase was only on its screen, and In's PHASE meant only
    the recommended item's rung, so the next arrival showed "not recorded"."""

    def test_out_writes_the_phase_and_in_reads_it(self):
        self.assertIn("write the same words into the start point's current section as one line, "
                      "`Phase: <phase>`, before the last commit", guide("references/out.md"))
        text = guide("references/in.md")
        self.assertIn("when the item has none, the `Phase:` line the start point records (Out writes it "
                      "there), and `null` only when neither exists", text)
        self.assertIn("or the start point's recorded `Phase:` line when the item has none", text)
        self.assertIn("a start point that cannot be read is a restoration gap (`restored: \"partial\"`), "
                      "not a missing phase", text)


if __name__ == "__main__":
    unittest.main()
