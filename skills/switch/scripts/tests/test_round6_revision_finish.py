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


def revised(brief=BRIEF):
    """The brief as the request asks: four answers in, their marks gone, the rest open."""
    out = brief.replace("**Launch:** February 2027 (10 February is tentative)",
                        "**Launch:** 10 February 2027")
    out = out.replace("February 2027. **[To confirm: the 10 February date is tentative, so use "
                      "\"February\" in anything external until it's firm.]**", "10 February 2027.")
    out = out.replace("1. Confirm the launch date (10 February is tentative).\n", "")
    out = out.replace("**[To confirm.]** Not covered in our notes.\n\n**What support",
                      "No. Volunteers don't need an account: the coordinator sends them a link.\n\n"
                      "**What support", 1)
    out = out.replace("**Who is it for?**", "**What do volunteers use?**\nIt works in any phone "
                      "browser, and there are iPhone and Android apps at launch.\n\n**Who is it for?**")
    assert out.count("browser") == 1 and "tentative" not in out, "sample brief drifted"
    return out


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
                self.assertIn(fields.get("type"), ("regex", "tool_used", "tool_order"))
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
        order = front_matter(CASE / "graders" / "out-after-revision.md")[0]
        self.assertEqual(order["before.tool"], "Edit")
        self.assertEqual(order["after.tool"], "Skill")
        self.assertEqual(quoted(order["after.input_match"]), rx("switch-out-ran", "input_match").pattern)


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

    def test_ends_on_the_save_question_naming_the_brief(self):
        ask = rx("ends-on-save-question-naming-brief")
        self.assertTrue(ask.search("Found: the brief has the answers.\n\n" + self.QUESTION))
        self.assertTrue(ask.search(self.PLAIN))
        for ending in (self.PUT_DOWN, self.SILENT, self.BOX,
                       "> 💬 **These files changed: notes.md. Should I save them too?**"):
            with self.subTest(ending=ending):
                self.assertFalse(ask.search(ending))

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
                    "git -C /p add launch-brief.md", "git -C /p commit -m x -- launch-brief.md"):
            with self.subTest(cmd=cmd):
                self.assertTrue(saved.search(bash(cmd)))
        for cmd in ("git -C /p status --short", "git -C /p diff -- launch-brief.md",
                    "python3 /s/handoff.py --project /p save --file CONTEXT.md --file TODO.md"):
            with self.subTest(cmd=cmd):
                self.assertFalse(saved.search(bash(cmd)))


class SessionAccountEitherWay(unittest.TestCase):
    rx = rx("session-log-written")

    def test_a_new_dated_log_passes(self):
        self.assertTrue(self.rx.search(call("Write", file_path="/w/kivna/sessions/2026-11-21.md",
                                            content="# 2026-11-21\n\n## Sitting: brief answers\n")))

    def test_a_new_sitting_heading_in_the_days_log_passes(self):
        last = "- Nothing was sent, shared or published.\n"
        self.assertTrue(self.rx.search(call(
            "Edit", file_path="/w/kivna/sessions/2026-11-20.md", old_string=last,
            new_string=last + "\n## Sitting: brief updated with the product team's answers\n\n- x\n")))
        self.assertTrue(self.rx.search(call(
            "Write", file_path="/w/kivna/sessions/2026-11-20.md",
            content=LOG + "\n## Sitting: brief updated with the product team's answers\n")))

    def test_rewording_sitting_ones_account_fails(self):
        self.assertFalse(self.rx.search(call(
            "Edit", file_path="/w/kivna/sessions/2026-11-20.md",
            old_string="- Nothing was sent, shared or published.",
            new_string="- Nothing was sent, shared or published yet.")))
        self.assertFalse(self.rx.search(call("Write", file_path="/w/kivna/sessions/2026-11-20.md",
                                             content=LOG)))

    def test_other_files_fail(self):
        self.assertFalse(self.rx.search(call("Write", file_path="/w/docs/work/launch-brief/work.md",
                                             content="# x\n\n## Now\n")))


class BriefFactsAndOpenQuestions(unittest.TestCase):
    FACTS = ("brief-fact-browser", "brief-fact-apps", "brief-fact-no-account",
             "brief-account-mark-removed", "brief-fact-date-confirmed")
    OPEN = ("privacy-still-to-confirm", "pricing-still-to-confirm")

    def test_untouched_brief_fails_every_fact_and_keeps_both_questions_open(self):
        for name in self.FACTS:
            with self.subTest(grader=name):
                self.assertFalse(rx(name).search(BRIEF))
        for name in self.OPEN:
            with self.subTest(grader=name):
                self.assertTrue(rx(name).search(BRIEF))

    def test_the_requested_revision_passes_every_grader(self):
        brief = revised()
        for name in self.FACTS + self.OPEN:
            with self.subTest(grader=name):
                self.assertTrue(rx(name).search(brief))

    def test_closing_an_unanswered_question_fails(self):
        brief = revised()
        no_privacy = brief.replace("**[To confirm.]** Our notes don't cover how data is stored",
                                   "Our notes don't cover how data is stored")
        self.assertNotEqual(no_privacy, brief)
        self.assertFalse(rx("privacy-still-to-confirm").search(no_privacy))
        no_pricing = brief.replace(" **[To confirm: whether $19 is a flat monthly price or depends "
                                   "on the number of volunteers.]**", "")
        self.assertNotEqual(no_pricing, brief)
        self.assertFalse(rx("pricing-still-to-confirm").search(no_pricing))

    def test_a_date_still_called_tentative_fails(self):
        self.assertFalse(rx("brief-fact-date-confirmed").search(revised() + "\n10 February is tentative.\n"))


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
