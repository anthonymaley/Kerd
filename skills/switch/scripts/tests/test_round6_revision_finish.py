"""Switch In's handoff adds no exclusions of its own; the sitting-2 eval case is sound.

First-user round 6 (batch-1114, first-user-6.md, Proposal 2; sitting-2 reruns
2026-11-21): after Sam brought the product team's answers, 0 of 4 revisions of the
accepted brief ran Switch Out. Kerd's own records were left alone whenever Switch In's
handoff said "Edit launch-brief.md only"; the run whose handoff named them updated
them. These tests pin the wording in in.md and check the eval case
`evals/conductor-revision-out` is well formed.

Three Codex review rounds on the case's regex graders each found another edge case, so
every grader except a trivial non-empty check is now a model-judged rubric
(`type: llm`). These tests can only check that each rubric states its criteria; how
the judge applies them is shown only by a real `claude plugin eval` run (the case's
README says so).
"""
from pathlib import Path
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
RUBRICS = {
    "brief-answers-in": "{source: file, path: launch-brief.md}",
    "brief-open-questions-kept": "{source: file, path: launch-brief.md}",
    "asks-which-files-to-save": "last_message",
    "brief-not-saved-unasked": "trace",
    "out-after-revision": "trace",
    "out-guide-read": "trace",
    "sitting-account-written": "trace",
}


def flat(text):
    return " ".join(text.split())


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    head = text.split("---\n", 2)
    if len(head) < 3 or head[0] != "":
        raise AssertionError(f"{path.name}: no front matter")
    fields = {}
    for line in head[1].splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, head[2]


def rubric(name):
    return flat(front_matter(CASE / "graders" / f"{name}.md")[1])


def scaffold_file(name):
    scaffold = (CASE / "scaffold.sh").read_text(encoding="utf-8")
    body = scaffold[scaffold.index(f"cat > {name} <<'EOT'\n"):]
    return body[body.index("\n") + 1:body.index("\nEOT\n") + 1]


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

    def test_graders_are_rubrics_but_one_non_empty_check(self):
        names = sorted(p.stem for p in (CASE / "graders").glob("*.md"))
        self.assertEqual(names, sorted([*RUBRICS, "reply-not-empty"]))
        for name, focus in RUBRICS.items():
            with self.subTest(grader=name):
                fields, body = front_matter(CASE / "graders" / f"{name}.md")
                self.assertEqual(fields["type"], "llm")
                self.assertEqual(fields["weight"], "1")
                self.assertEqual(fields["focus"], focus)
                self.assertIn("PASS", body)
                self.assertIn("FAIL", body)
        fields, _ = front_matter(CASE / "graders" / "reply-not-empty.md")
        self.assertEqual((fields["type"], fields["target"]), ("regex", "last_message"))
        self.assertEqual(fields["pattern"], "'^[\\s\\S]{300,}$'")
        re.compile(fields["pattern"][1:-1])

    def test_readme_says_what_the_tests_cannot_prove(self):
        readme = flat((CASE / "README.md").read_text(encoding="utf-8"))
        self.assertIn("can only check that each rubric states its criteria", readme)
        self.assertIn("Only a real `claude plugin eval` run of this case can show how the judge "
                      "behaves, and none has been recorded yet.", readme)
        self.assertIn("`context.history_file`", readme)


class RubricsStateEachCriterion(unittest.TestCase):
    def assert_states(self, name, *checks):
        text = rubric(name)
        for check in checks:
            with self.subTest(grader=name, check=check):
                self.assertIn(check, text)

    def test_brief_answers(self):
        self.assert_states(
            "brief-answers-in", "works in any phone browser",
            "iPhone and Android apps are available at launch",
            "volunteers need no account, and the coordinator sends them a link",
            "no longer carries a \"To confirm\" mark", "stated as 10 February (2027) and confirmed",
            "not called tentative anywhere in the brief",
            "nothing anywhere else may still say the opposite of these answers",
            "the \"Open items\" list must not still call the date tentative",
            "PASS only if all five hold and nothing elsewhere contradicts them",
            "\"does not work in a browser\"")

    def test_every_other_open_item_stays_open(self):
        self.assert_states(
            "brief-open-questions-kept", "privacy and security question", "price after 25 volunteers",
            "What the grant report contains", "Shift scheduling", "What support is available",
            "Permission to quote the four pilot coordinators", "\"Probably not the right fit\"",
            "The pilot year", "PASS only if all eight are still marked or listed as unconfirmed",
            "nothing elsewhere in the brief states any of them as a confirmed fact")

    def test_the_open_items_are_the_scaffolds_own(self):
        # The rubric lists every unconfirmed item the scaffold's brief marks, so each
        # anchor below must be in that brief.
        brief = scaffold_file("launch-brief.md")
        for anchor in ("**[To confirm: whether $19 is a flat monthly price",
                       "**[To confirm: exactly what's in the report",
                       "**[To confirm: that scheduling isn't in the launch",
                       "**Is our volunteers' information private and secure?**\n**[To confirm.]**",
                       "**What support is available?**\n**[To confirm.]**",
                       "**[Quotes: confirm permission before use.]**",
                       "**Probably not the right fit (our suggestion, please confirm):**",
                       "7. Confirm the pilot year."):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, brief)
        # "[To confirm" appears 8 times: the Status line's legend, the five open FAQ items
        # above (price, grant report, scheduling, privacy, support) and the two answered
        # ones (account, launch date). A ninth would be an item the rubric does not list.
        self.assertEqual(brief.count("[To confirm"), 8)

    def test_save_question(self):
        self.assert_states(
            "asks-which-files-to-save",
            "final question asks the person which of their changed files to save",
            "names the launch brief", "does not claim the brief is already saved",
            "\"Put this down for today?\"", "SESSION SAVED or SAVED LOCALLY")

    def test_brief_not_saved_before_the_answer(self):
        self.assert_states(
            "brief-not-saved-unasked", "every command in it comes before their answer",
            "could stage, commit or push launch-brief.md", "`git add -A`", "`git add .`",
            "`git add :/`", "`git add '*'`", "`git commit -a`", "any `--push` or `git push`",
            "`git remote add`", "`git add -- kivna/sessions/2026-11-21.md CONTEXT.md TODO.md`")

    def test_out_after_a_successful_change(self):
        self.assert_states(
            "out-after-revision", "whose tool result is not an error",
            "whatever the path's spelling", "whatever the order of the call's fields",
            "the skill is switch (kerd:switch) and its arguments start Out",
            "followed later in the trace by event 2", "every change to it failed or errored")

    def test_out_guide_read_in_full(self):
        self.assert_states(
            "out-guide-read", "\"# Out: clean boundaries\"", "\"Without `--sync` it is local-only.\"",
            "read only in part")
        # The anchors are the guide's own first heading and last sentence.
        guide = (ROOT / "skills" / "switch" / "references" / "out.md").read_text(encoding="utf-8")
        self.assertEqual(guide.splitlines()[0], "# Out: clean boundaries")
        self.assertTrue(guide.rstrip().endswith("Without `--sync` it is local-only."))

    def test_sitting_account(self):
        self.assert_states(
            "sitting-account-written", "whose tool result is a success (not an error)",
            "a new dated log file under kivna/sessions/ other than 2026-11-20.md",
            "a new \"## \" sitting heading added to 2026-11-20.md followed by that account",
            "Substantive means the new text says what this sitting did",
            "more than a heading, a date or a placeholder",
            "only the earlier sitting's existing account was reworded")
        self.assertIn("## Sitting: Harbor Hours launch brief", scaffold_file("kivna/sessions/2026-11-20.md"))


if __name__ == "__main__":
    unittest.main()
