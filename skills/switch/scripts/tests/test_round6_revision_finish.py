"""Switch In's handoff adds no exclusions of its own; the sitting-2 eval case is sound.

First-user round 6 (batch-1114, first-user-6.md, Proposal 2; sitting-2 reruns
2026-11-21): after Sam brought the product team's answers, 0 of 4 revisions of the
accepted brief ran Switch Out. Kerd's own records were left alone whenever Switch In's
handoff said "Edit launch-brief.md only"; the run whose handoff named them updated
them. These tests pin the wording in in.md and check the eval case
`evals/conductor-revision-out` is well formed and its graders tell a pass from the
round-6 endings. They check the words and patterns, not that a model follows them.
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


def quoted(value):
    """A single-quoted YAML scalar, as the graders write their patterns."""
    assert value.startswith("'") and value.endswith("'"), value
    return value[1:-1].replace("''", "'")


def grader(name):
    return front_matter(CASE / "graders" / f"{name}.md")[0]


def rx(name, key="pattern"):
    fields = grader(name)
    flags = re.I if fields.get("flags") == "i" else re.M if fields.get("flags") == "m" else 0
    return re.compile(quoted(fields[key]), flags)


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

    def test_scaffold_parses(self):
        result = subprocess.run(["bash", "-n", str(CASE / "scaffold.sh")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_prompt_is_sitting_twos_handoff_to_conductor(self):
        fields, body = front_matter(CASE / "prompt.md")
        self.assertIn("Skill", fields["allowed_tools"])
        self.assertTrue(body.strip().startswith("/kerd:conductor "))
        # The handoff limits the files; the eval checks that limit never limits Out.
        self.assertIn("Edit launch-brief.md only", body)
        self.assertNotIn("committed", body)

    def test_every_grader_has_a_type_weight_and_compiling_pattern(self):
        for path in sorted((CASE / "graders").glob("*.md")):
            with self.subTest(grader=path.name):
                fields, body = front_matter(path)
                self.assertIn(fields.get("type"), ("regex", "tool_used"))
                self.assertEqual(fields.get("weight"), "1")
                self.assertTrue(body.strip())
                for key in ("pattern", "input_match"):
                    if key in fields:
                        re.compile(quoted(fields[key]))

    def test_out_guide_grader_is_the_switch_out_cases_own(self):
        ours = rx("out-guide-read").pattern
        theirs = re.compile(quoted(front_matter(
            ROOT / "evals" / "switch-out-clean" / "graders" / "out-guide-read.md")[0]["pattern"])).pattern
        self.assertEqual(ours, theirs)


class GradersTellPassFromRound6(unittest.TestCase):
    def test_switch_out_skill_call(self):
        out = rx("switch-out-ran", "input_match")
        for call in ('{"skill":"kerd:switch","args":"out"}', '{"args": "out", "skill": "switch"}'):
            with self.subTest(call=call):
                self.assertTrue(out.search(call))
        for call in ('{"skill":"kerd:switch","args":"in"}', '{"skill":"kerd:conductor","args":"out"}',
                     '{"skill":"kerd:switch"}'):
            with self.subTest(call=call):
                self.assertFalse(out.search(call))

    def test_round6_endings_fail_and_outs_box_passes(self):
        put_down = rx("no-put-down-question")  # not_contains: a match is a slip
        closing = rx("ends-on-closing-line")
        asked = "That's updated.\n\n> 💬 **Put this down for today with /kerd:switch out?**"
        silent = "I didn't touch `TODO.md`. Your to-do list is yours, so say if you want it updated."
        box = ("**HARBOR HOURS · SAVED LOCALLY**\n\nRun /clear, then /kerd:switch in to pick up from here.")
        self.assertTrue(put_down.search(asked))
        self.assertFalse(closing.search(asked))
        self.assertFalse(closing.search(silent))
        self.assertFalse(put_down.search(box))
        self.assertTrue(closing.search(box))

    def test_brief_graders_start_from_the_scaffolds_brief(self):
        # The revision grader must fail on the untouched brief; the scope guard must pass on it.
        scaffold = (CASE / "scaffold.sh").read_text(encoding="utf-8")
        brief = scaffold[scaffold.index("cat > launch-brief.md <<'EOT'\n"):]
        brief = brief[brief.index("\n") + 1:brief.index("\nEOT\n")]
        self.assertFalse(rx("brief-revised").search(brief))
        self.assertTrue(rx("privacy-still-to-confirm").search(brief))

    def test_session_log_grader_skips_sitting_ones(self):
        log = rx("session-log-written")
        self.assertFalse(log.search("kivna/sessions/2026-11-20.md\nlaunch-brief.md"))
        self.assertTrue(log.search("launch-brief.md\nkivna/sessions/2026-11-21.md"))


if __name__ == "__main__":
    unittest.main()
