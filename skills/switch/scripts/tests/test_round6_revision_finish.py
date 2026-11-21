"""Switch In's handoff adds no exclusions of its own; the sitting-2 eval case is sound.

First-user round 6 (batch-1114, first-user-6.md, Proposal 2; sitting-2 reruns
2026-11-21): after Sam brought the product team's answers, 0 of 4 revisions of the
accepted brief ran Switch Out. Kerd's own records were left alone whenever Switch In's
handoff said "Edit launch-brief.md only"; the run whose handoff named them updated
them. These tests pin the wording in in.md and check the eval case
`evals/conductor-revision-out` is well formed and its graders tell a pass from the
round-6 endings. They check the words and patterns, not that a model follows them.

Codex review of the first cut (Hold, five findings): the revised brief is the
person's own file, so Out must ask before saving it and the single-turn case ends
on that question, not the closing box; the session account may be a new sitting
heading in the day's existing log; each requested fact and both unanswered
questions are checked; any --push through the helper counts as a push.
Review r2: regex cannot judge meaning, so the brief's facts, the save question and the
session account are model-graded rubrics (`type: llm`); regex stays for the mechanical
checks, whose tests below include the slips they must catch.
"""
from pathlib import Path
import json
import os
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[4]
IN = ROOT / "skills" / "switch" / "references" / "in.md"
CASE = ROOT / "evals" / "conductor-revision-out"

HANDOFF_RULE = (
    "Carry only the exclusions the person stated. Never add your own (“edit X only”, "
    "“nothing committed”): Kerd's own records and the closing save are part of every sitting."
)


def flat(text):
    return " ".join(text.split())


def front_matter(path):
    """Front matter as a flat dict; one level of nesting becomes `parent.key`."""
    text = path.read_text(encoding="utf-8")
    head = text.split("---\n", 2)
    if len(head) < 3 or head[0] != "":
        raise AssertionError(f"{path.name}: no front matter")
    fields, parent = {}, None
    for line in head[1].splitlines():
        key, _, value = line.strip().partition(":")
        value = value.strip()
        if line.startswith("  ") and parent:
            fields[f"{parent}.{key}"] = value
        else:
            fields[key] = value
            parent = key if value == "" else None
    return fields, head[2]


def quoted(value):
    """A single-quoted YAML scalar, as the graders write their patterns."""
    assert value.startswith("'") and value.endswith("'"), value
    return value[1:-1].replace("''", "'")


def rx(name, key="pattern"):
    fields = front_matter(CASE / "graders" / f"{name}.md")[0]
    flags = re.I if fields.get("flags") == "i" else 0
    return re.compile(quoted(fields[key]), flags)


def bash(command):
    """A Bash call's input as the graders' input_match sees it (compact JSON)."""
    return json.dumps({"command": command, "description": "x"}, separators=(",", ":"))


def call(name, **inputs):
    """One tool_use as it sits in the trace."""
    return json.dumps({"type": "tool_use", "id": "toolu_1", "name": name, "input": inputs},
                      separators=(",", ":"), ensure_ascii=False)


def scaffold_file(name):
    scaffold = (CASE / "scaffold.sh").read_text(encoding="utf-8")
    body = scaffold[scaffold.index(f"cat > {name} <<'EOT'\n"):]
    return body[body.index("\n") + 1:body.index("\nEOT\n") + 1]


BRIEF = scaffold_file("launch-brief.md")
LOG = scaffold_file("kivna/sessions/2026-11-20.md")


class HandoffCarriesOnlyStatedExclusions(unittest.TestCase):
    def test_rule_is_in_enter_conductor_once(self):
        text = IN.read_text(encoding="utf-8")
        section = text[text.index("### Enter Conductor from the answer"):
                       text.index("### Welcome back: the screen summary")]
        self.assertEqual(flat(section).count(HANDOFF_RULE), 1)
        self.assertEqual(flat(text).count(HANDOFF_RULE), 1)


class EvalCaseShape(unittest.TestCase):
    def test_case_names_its_folder_and_scaffold(self):
        case = (CASE / "case.yaml").read_text(encoding="utf-8")
        self.assertIn('schema_version: "1.1"', case)
        self.assertIn("name: conductor-revision-out", case)
        self.assertIn("scaffold_script: scaffold.sh", case)
        self.assertTrue(os.access(CASE / "scaffold.sh", os.X_OK))

    def test_scaffold_parses_and_adds_no_remote(self):
        result = subprocess.run(["bash", "-n", str(CASE / "scaffold.sh")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("git remote add", (CASE / "scaffold.sh").read_text(encoding="utf-8"))

    def test_prompt_is_sitting_twos_handoff_to_conductor(self):
        fields, body = front_matter(CASE / "prompt.md")
        self.assertIn("Skill", fields["allowed_tools"])
        self.assertTrue(body.strip().startswith("/kerd:conductor "))
        # The handoff limits the files; the eval checks that limit never limits Out.
        self.assertIn("Edit launch-brief.md only", body)
        self.assertNotIn("committed", body)

    def test_every_grader_has_a_type_weight_and_compiling_patterns(self):
        for path in sorted((CASE / "graders").glob("*.md")):
            with self.subTest(grader=path.name):
                fields, body = front_matter(path)
                self.assertIn(fields.get("type"), ("regex", "tool_used", "llm"))
                if fields["type"] == "llm":
                    self.assertIn("focus", fields)
                    self.assertIn("PASS", body)
                    self.assertIn("FAIL", body)
                self.assertEqual(fields.get("weight"), "1")
                self.assertTrue(body.strip())
                for key in ("pattern", "input_match", "before.input_match", "after.input_match"):
                    if key in fields:
                        re.compile(quoted(fields[key]))

    def test_the_closing_box_is_not_required_in_a_single_turn(self):
        self.assertFalse((CASE / "graders" / "ends-on-closing-line.md").exists())

    def test_out_graders_match_their_sources(self):
        theirs = front_matter(ROOT / "evals" / "switch-out-clean" / "graders" / "out-guide-read.md")[0]
        self.assertEqual(rx("out-guide-read").pattern, quoted(theirs["pattern"]))

    def test_meaning_is_model_graded(self):
        # Review r2: these judge meaning, so they are rubrics, never regex.
        for name, focus in (("brief-answers-in", "{source: file, path: launch-brief.md}"),
                            ("brief-open-questions-kept", "{source: file, path: launch-brief.md}"),
                            ("asks-which-files-to-save", "last_message"),
                            ("sitting-account-written", "trace")):
            with self.subTest(grader=name):
                fields, _ = front_matter(CASE / "graders" / f"{name}.md")
                self.assertEqual(fields["type"], "llm")
                self.assertEqual(fields["focus"], focus)
        for gone in ("brief-fact-browser", "brief-fact-apps", "brief-fact-no-account",
                     "brief-account-mark-removed", "brief-fact-date-confirmed",
                     "privacy-still-to-confirm", "pricing-still-to-confirm",
                     "ends-on-save-question-naming-brief", "session-log-written"):
            with self.subTest(gone=gone):
                self.assertFalse((CASE / "graders" / f"{gone}.md").exists())


class RubricsStateTheExactChecks(unittest.TestCase):
    def rubric(self, name):
        return flat(front_matter(CASE / "graders" / f"{name}.md")[1])

    def test_brief_answers(self):
        text = self.rubric("brief-answers-in")
        for check in ("works in any phone browser", "iPhone and Android apps are available at launch",
                      "volunteers need no account, and the coordinator sends them a link",
                      "no longer carries a \"To confirm\" mark", "stated as 10 February (2027) and confirmed",
                      "not called tentative", "PASS only if all five hold", "does not work in a browser"):
            with self.subTest(check=check):
                self.assertIn(check, text)

    def test_open_questions(self):
        text = self.rubric("brief-open-questions-kept")
        for check in ("privacy and security question", "price after 25 volunteers",
                      "PASS only if both are still marked \"To confirm\""):
            with self.subTest(check=check):
                self.assertIn(check, text)
        # Both start open in the scaffold's brief, so "still" is true of the start state.
        self.assertRegex(BRIEF, r"private and secure\?\*\*\n\*\*\[To confirm\.\]\*\*")
        self.assertRegex(BRIEF, r"\$19 a month\. \*\*\[To confirm")

    def test_save_question(self):
        text = self.rubric("asks-which-files-to-save")
        for check in ("final question asks the person which of their changed files to save",
                      "names the launch brief", "does not claim the brief is already saved",
                      "\"Put this down for today?\""):
            with self.subTest(check=check):
                self.assertIn(check, text)

    def test_sitting_account(self):
        text = self.rubric("sitting-account-written")
        for check in ("a new dated log file under kivna/sessions/ other than 2026-11-20.md",
                      "a new \"## \" sitting heading added to 2026-11-20.md followed by that account",
                      "only the earlier sitting's existing account was reworded"):
            with self.subTest(check=check):
                self.assertIn(check, text)
        # The rubric names sitting 1's heading as it is in the scaffold.
        self.assertIn("## Sitting: Harbor Hours launch brief", LOG)


class OutAfterTheRevision(unittest.TestCase):
    rx = rx("out-after-revision")
    OUT = call("Skill", skill="kerd:switch", args="out")

    def test_edit_or_write_on_the_brief_then_out_passes(self):
        for change in (call("Edit", file_path="/w/launch-brief.md", old_string="a", new_string="b"),
                       call("Write", file_path="/w/launch-brief.md", content="# Brief\n")):
            with self.subTest(change=change[:40]):
                self.assertTrue(self.rx.search(change + "\n" + self.OUT))
        self.assertTrue(self.rx.search(call("Edit", file_path="/w/launch-brief.md", old_string="a",
                                            new_string="b") + "\n" + call("Skill", args="out", skill="switch")))

    def test_out_first_or_another_file_or_another_skill_fails(self):
        edit = call("Edit", file_path="/w/launch-brief.md", old_string="a", new_string="b")
        self.assertFalse(self.rx.search(self.OUT + "\n" + edit))
        self.assertFalse(self.rx.search(call("Edit", file_path="/w/notes.md", old_string="a",
                                             new_string="b") + "\n" + self.OUT))
        self.assertFalse(self.rx.search(edit + "\n" + call("Skill", skill="kerd:switch", args="in")))
        self.assertFalse(self.rx.search(call("Read", file_path="/w/launch-brief.md") + "\n" + self.OUT))


class OutStartsUnaskedAndAsksAboutTheBrief(unittest.TestCase):
    QUESTION = ("> 💬 **These files of yours changed and aren't saved yet: launch-brief.md. "
                "Should I save it too?**")
    PLAIN = "> 💬 **The launch brief changed and isn't saved yet. Should I save it too?**"
    PUT_DOWN = "That's updated.\n\n> 💬 **Put this down for today with /kerd:switch out?**"
    SILENT = "I didn't touch `TODO.md`. Your to-do list is yours, so say if you want it updated."
    BOX = "**HARBOR HOURS · SAVED LOCALLY**\n\nRun /clear, then /kerd:switch in to pick up from here."

    def test_switch_out_skill_call(self):
        out = rx("switch-out-ran", "input_match")
        for given in ('{"skill":"kerd:switch","args":"out"}', '{"args": "out", "skill": "switch"}'):
            with self.subTest(call=given):
                self.assertTrue(out.search(given))
        for given in ('{"skill":"kerd:switch","args":"in"}', '{"skill":"kerd:conductor","args":"out"}',
                      '{"skill":"kerd:switch"}'):
            with self.subTest(call=given):
                self.assertFalse(out.search(given))

    def test_no_box_before_the_answer(self):
        box = rx("no-closing-box")  # not_contains: a match is a slip
        self.assertTrue(box.search(self.BOX))
        self.assertTrue(box.search("**HARBOR HOURS · SESSION SAVED ✓**"))
        self.assertFalse(box.search(self.QUESTION))

    def test_round6_put_down_ending_is_a_slip(self):
        put_down = rx("no-put-down-question")
        self.assertTrue(put_down.search(self.PUT_DOWN))
        self.assertFalse(put_down.search(self.QUESTION))

    def test_brief_is_not_saved_before_the_answer(self):
        saved = rx("brief-not-saved-unasked", "input_match")  # max 0: a match is a slip
        for cmd in ("python3 /s/handoff.py --project /p save --file launch-brief.md --file TODO.md",
                    "git -C /p add launch-brief.md", "git -C /p commit -m x -- launch-brief.md",
                    # Review r2: broad staging sweeps the brief in without naming it.
                    "git -C /p add -A", "git add .", "git -C /p add --all", "git add -u",
                    "git -C /p add . && git -C /p commit -m x", "git commit -a -m x",
                    "git -C /p commit -am x", "git commit --all -m x",
                    "python3 /s/handoff.py --project /p save --push --file CONTEXT.md"):
            with self.subTest(cmd=cmd):
                self.assertTrue(saved.search(bash(cmd)))
        for cmd in ("git -C /p status --short", "git -C /p diff -- launch-brief.md",
                    "python3 /s/handoff.py --project /p save --file CONTEXT.md --file TODO.md",
                    "git -C /p add CONTEXT.md TODO.md kivna/sessions/2026-11-21.md",
                    "git -C /p add ./CONTEXT.md", "git -C /p commit -m x -- CONTEXT.md",
                    "git -C /p commit --amend --no-edit", "git -C /p log --all --oneline"):
            with self.subTest(cmd=cmd):
                self.assertFalse(saved.search(bash(cmd)))


class NothingPushed(unittest.TestCase):
    rx = rx("nothing-pushed", "input_match")  # max 0: a match is a slip

    def test_pushes_are_caught(self):
        for cmd in ("git push", "git -C /p push origin main",
                    "python3 /s/handoff.py --project /p save --push --file CONTEXT.md",
                    "python3 $H --project /p save --file CONTEXT.md --push",
                    "H=/s/handoff.py; python3 $H --project . save --push --file a.md"):
            with self.subTest(cmd=cmd):
                self.assertTrue(self.rx.search(bash(cmd)))

    def test_local_saves_and_reads_are_not(self):
        for cmd in ("git config --get push.default", "git -C /p remote",
                    "python3 /s/handoff.py --project /p save --file CONTEXT.md"):
            with self.subTest(cmd=cmd):
                self.assertFalse(self.rx.search(bash(cmd)))

    def test_an_added_remote_is_caught(self):
        added = rx("no-remote-added")  # not_contains: a match is a slip
        self.assertTrue(added.search('[core]\n\tbare = false\n[remote "origin"]\n\turl = /x\n'))
        self.assertFalse(added.search("[core]\n\tbare = false\n[user]\n\tname = Sam Rivera\n"))


if __name__ == "__main__":
    unittest.main()
