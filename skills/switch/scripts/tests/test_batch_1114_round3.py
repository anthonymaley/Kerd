"""Batch 1114, part 2: what the non-developer walkthrough on 0.196.0 found in Switch.

#1: In's managed-roll probe was a compound `git rev-parse … && …` the person could not judge.
#4: "Nothing actionable is open" sat above four open items, all the person's own.
#5: Out spoke git to a non-developer ("commit by name", "no Git remote is configured").
#12: RELEASED: "Nothing released" on a project with no release process.
#13: an ordinary risk reached ATTENTION.
#16: the measurement and read_args sat in CONTEXT.md among the person's lines.
#17: the first Out never said what Kerd's own files are.

Renderer and helper checks run the code; guide checks find the wording, not
that a model follows it.
"""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[4]
SWITCH = ROOT / "skills/switch"
SPEC = importlib.util.spec_from_file_location("where_we_are_round3", SWITCH / "scripts/where_we_are.py")
view = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(view)
STATUS = SWITCH / "scripts/roll_status.py"
NOW = "2026-11-14 18:00 EST"
FIRST_OUT = ("Kerd keeps its notes for next time in CONTEXT.md, TODO.md and the kivna/ folder; "
             "you can ignore them.")


def flat(text):
    return " ".join(text.split())


def guide(rel):
    return flat((SWITCH / rel).read_text(encoding="utf-8"))


def arrival(**over):
    summary = {"project": "Harbor Hours", "phase": "drafting", "where": "The brief is drafted.",
               "open_work": ["You: call the venue about the date.", "You: chase the FAQ answers."],
               "recommendation": None, "team": [], "question": None, "restored": "yes",
               "first_arrival": False}
    summary.update(over)
    return summary


def closing(**over):
    summary = {"project": "Harbor Hours", "branch": "main", "saved": "committed", "handoff_ready": True,
               "boundary": "local_only", "verdicts": {"project": "local_only"}, "phase": "Brief drafted",
               "released": None, "this_session": ["The launch brief is drafted."],
               "next": "You: call the venue.", "why": "The date gates the rest.", "next_in": [],
               "tree": "clean", "warnings": [], "host": "claude"}
    summary.update(over)
    return summary


class PersonOwnedWork(unittest.TestCase):
    """#4."""

    def test_a_list_with_no_recommendation_does_not_say_nothing_actionable(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = flat(view.render_dashboard(arrival(), NOW, 80, False, markdown=markdown))
                self.assertNotIn("Nothing actionable", out)
                self.assertNotIn("nothing actionable", out)
                self.assertIn("Nothing on the list can move yet", out)

    def test_in_recommends_the_persons_first_item(self):
        text = guide("references/in.md")
        self.assertIn("**Watching is not work that can move.**", text)
        self.assertIn("When every open item that can move is the person's own, recommend the first of "
                      "them plainly", text)
        self.assertIn("say “can move”, never “can be built” or “buildable”", text)
        self.assertNotIn("nothing in Now can be built", text)
        self.assertIn("when every open item that can move is theirs, recommend their first plainly",
                      guide("SKILL.md"))


class PlainWordsAtOut(unittest.TestCase):
    """#5."""

    def test_the_local_only_box_is_plain_and_claims_no_missing_backup(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = flat(view.render_closing(closing(), NOW, 80, False, markdown=markdown))
                self.assertIn("Saved on this computer only; no other copy was checked.", out)
                self.assertNotIn("remote", out.lower())
                self.assertNotIn("Committed", out)
                self.assertNotIn("backup", out.lower())

    def test_out_says_saved_not_committed(self):
        text = guide("references/out.md")
        self.assertIn("To the person, Out “saves”: it does not “commit by name”, and a project with no "
                      "remote is “saved on this computer only”, never “no remote”.", text)
        self.assertNotIn("saying which look like generated output", text)


class ReviewRound1(unittest.TestCase):
    """Fresh Codex review r1 of this batch: declined tracked changes, ignored files,
    the ignore rule, the local-only claim and the box's git words."""

    def test_a_declined_tracked_change_fails_visibly(self):
        text = guide("references/out.md")
        self.assertIn("A tracked file they want left out cannot be preserved (the helper refuses tracked "
                      "paths) and is never stashed: say plainly, before saving, that the save will be "
                      "marked incomplete because that change stays unsaved", text)
        self.assertIn("name it in the box's `tree`, so the boundary check refuses and the box shows it", text)

    def test_ignored_files_and_an_unreadable_inventory(self):
        text = guide("references/out.md")
        self.assertIn("Files the project already ignores are not in the question: the project chose to "
                      "ignore them.", text)
        self.assertIn("say the other files are unknown, never that there is nothing else", text)

    def test_the_ignore_rule_is_anchored_escaped_and_checked(self):
        text = guide("references/out.md")
        self.assertIn("(a leading `/`; `*`, `?`, `[`, `!`, `#` and trailing spaces escaped with `\\`)", text)
        self.assertIn("check with `git check-ignore -v -- <path>` that this rule, and no wider one, "
                      "matches it", text)
        self.assertIn("a tracked file never gets an ignore rule", text)
        self.assertNotIn("add its exact path to `.gitignore`", text)

    def test_the_local_only_line_claims_only_what_was_checked(self):
        for verdicts in ({"project": "local_only"}, {"project": "local_only", "notes": "local_only"}):
            with self.subTest(verdicts=verdicts):
                out = flat(view.render_closing(closing(verdicts=verdicts), NOW, 80, False, markdown=True))
                self.assertIn("Saved on this computer only; no other copy was checked.", out)
                self.assertNotIn("Kerd has no copy", out)
        self.assertIn("Your notes are saved on this computer only; no other copy was checked.",
                      flat(view.render_closing(closing(verdicts={"project": "local_only", "notes": "local_only"}),
                                               NOW, 80, False, markdown=True)))
        self.assertIn("“Saved on this computer only; no other copy was checked.”", guide("references/out.md"))

    def test_the_box_puts_plain_words_first(self):
        cases = ((dict(saved="remote-verified", boundary="passed", verdicts={"project": "ok"}),
                  "Saved and copied to your remote (pushed to main)"),
                 (dict(boundary="local_only", verdicts={"project": "ok"}, saved="committed"),
                  "Saved on this computer, not yet copied to your remote (committed, not pushed)"),
                 (dict(saved="committed", boundary=["No remote branch contains this commit."]),
                  "not yet confirmed on your remote (committed, not verified there)"),
                 (dict(saved="not-saved"), "Nothing was saved (nothing committed)"),
                 (dict(tree="report.csv"), "Unsaved changes in your project folder: report.csv"))
        for over, words in cases:
            for markdown in (False, True):
                with self.subTest(words=words, markdown=markdown):
                    # The terminal's attention panel draws a border inside wrapped lines.
                    out = flat(view.render_closing(closing(**over), NOW, 80, False,
                                                   markdown=markdown).replace("│", " "))
                    self.assertIn(words, out)
                    for old in ("Pushed to main", "Committed, not pushed", "Left in the working tree",
                                "Nothing was committed:", "committed on this machine"):
                        self.assertNotIn(old, out)


class ReleasedCell(unittest.TestCase):
    """#12: fail closed: only an explicit `releases: false` hides the cell."""

    def test_no_release_process_hides_the_cell(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = view.render_closing(closing(releases=False), NOW, 80, False, markdown=markdown)
                self.assertNotIn("RELEASED", out)
                self.assertNotIn("Nothing released", out)
        rows = [line for line in view.render_closing(closing(releases=False), NOW, 80, False,
                                                     markdown=True).splitlines() if line.startswith("|")]
        self.assertEqual(rows[0], "| PROJECT | SAVED | PHASE |")
        self.assertEqual([row.count("|") for row in rows], [4, 4, 4])

    def test_unknown_or_a_real_release_keeps_it(self):
        for over in ({}, {"releases": None}, {"releases": "no"}, {"releases": True},
                     {"releases": False, "released": "1.0.0"}):
            with self.subTest(over=over):
                out = view.render_closing(closing(**over), NOW, 80, False, markdown=True)
                self.assertIn("| PROJECT | SAVED | PHASE | RELEASED |", out)

    def test_out_names_the_rule(self):
        self.assertIn("`releases` is `false` only when successful reads show the project has no release "
                      "process", guide("references/out.md"))
        self.assertIn("A failed read or any doubt leaves it `null` and the cell shows as before.",
                      guide("references/out.md"))


class AttentionRisks(unittest.TestCase):
    """#13."""

    def test_ordinary_risks_stay_out_of_attention(self):
        self.assertIn("A risk the record does not mark urgent or imminent (“unanswered FAQ items could "
                      "make sales improvise”) stays in the sketchbook", guide("references/in.md"))


class KerdLinesInContext(unittest.TestCase):
    """#16: kept in CONTEXT.md, under a last heading for Kerd."""

    HEADING = "## For Kerd's next pickup (you can ignore this)"

    def test_out_names_the_heading(self):
        text = guide("references/out.md")
        self.assertIn("under its last heading, `" + self.HEADING + "`, which Out creates when missing "
                      "and keeps last", text)

    def test_graders_need_the_heading(self):
        sample = ("# Context\n\nThe brief is drafted.\n\n" + self.HEADING + "\n\n"
                  "Measured: 1,739 bytes, about 435 tokens.\n\nread_args: "
                  '["--record", "CONTEXT.md"]\n')
        bare = sample.replace(self.HEADING + "\n", "")
        for case in ("switch-out-clean", "switch-out-dirty-private", "switch-out-no-log-human"):
            for name in ("context-records-measurement.md", "context-saves-read-args.md"):
                with self.subTest(case=case, grader=name):
                    text = (ROOT / "evals" / case / "graders" / name).read_text(encoding="utf-8")
                    pattern = re.search(r"^pattern: '(.*)'$", text, re.M)[1]
                    flags = re.I if re.search(r"^flags: i$", text, re.M) else 0
                    self.assertRegex(sample, re.compile(pattern, flags))
                    self.assertNotRegex(bare, re.compile(pattern, flags))


class FirstOutLine(unittest.TestCase):
    """#17."""

    def test_only_a_first_out_says_it_once(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = flat(view.render_closing(closing(first_out=True), NOW, 80, False, markdown=markdown))
                self.assertEqual(out.count(FIRST_OUT), 1)
                for value in (None, False, "yes", 1):
                    later = flat(view.render_closing(closing(first_out=value), NOW, 80, False,
                                                     markdown=markdown))
                    self.assertNotIn("you can ignore them", later)

    def test_out_sets_it_from_a_successful_read(self):
        self.assertIn("`first_out` is `true` only when a successful read found no earlier session log "
                      "in `kivna/sessions/` before this Out", guide("references/out.md"))


class OneRollProbe(unittest.TestCase):
    """#1 (part): one helper call tells no run, a run and unknown apart."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="switch-round3-")
        self.repo = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.roll = Path(subprocess.run(["git", "-C", str(self.repo), "rev-parse", "--absolute-git-dir"],
                                        capture_output=True, text=True, check=True).stdout.strip()) / "roll"

    def tearDown(self):
        self.temp.cleanup()

    def status(self):
        return subprocess.run([sys.executable, str(STATUS), "--project", str(self.repo)],
                              capture_output=True, text=True)

    def test_no_record_is_exit_3_and_unreadable_is_not(self):
        result = self.status()
        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout, "")
        self.roll.mkdir(parents=True)
        (self.roll / "run.json").write_text("not-json", encoding="utf-8")
        self.assertEqual(self.status().returncode, 1)

    def test_the_chat_marker_is_reported_in_the_same_call(self):
        self.roll.mkdir(parents=True)
        (self.roll / "chat.json").write_text(json.dumps({"state": "waiting"}), encoding="utf-8")
        result = self.status()
        self.assertEqual(result.returncode, 3)
        self.assertIn("Chat roll marker: an unclaimed chat roll is waiting", result.stdout)
        (self.roll / "run.json").write_text(json.dumps({"status": "paused", "next_action": "Resume."}),
                                            encoding="utf-8")
        result = self.status()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Chat roll marker:", result.stdout)

    def test_in_uses_the_one_call(self):
        text = guide("references/in.md")
        self.assertIn("so In needs no `git rev-parse --git-path` probe first", text)
        self.assertIn("exit 3 means a successful read found none", text)
        self.assertNotIn("check whether `git rev-parse --git-path roll/run.json` names", text)
        self.assertIn("run `roll_status.py` once (exit 3 alone means no run", guide("SKILL.md"))


if __name__ == "__main__":
    unittest.main()
