"""Batch 1114, part 3: the walkthrough rerun on 0.197.0 (first-user-4).

Row 1: chained commands (`roll_status.py; echo; ls …`) left prompts after python3 and git were allowed.
Row 14: with no README the arrival was headed "PROJECT" though notes.md had a title.
Row 5 / new 3: "no other copy was checked" read as a skipped check, and ATTENTION repeated it.
New 2: Out told the person its token measurement.
New 6: "you can ignore them" was said twice, by the model and by the renderer.

Renderer checks run the code; guide checks find the wording, not that a model follows it.
"""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[4]
SWITCH = ROOT / "skills/switch"
SPEC = importlib.util.spec_from_file_location("where_we_are_round4", SWITCH / "scripts/where_we_are.py")
view = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(view)
NOW = "2026-11-14 21:00 EST"


def flat(text):
    return " ".join(text.split())


def guide(rel):
    text = (SWITCH / rel).read_text(encoding="utf-8")
    if rel == "references/in.md":
        text += "\n" + (SWITCH / "references/in-detail.md").read_text(encoding="utf-8")
    return flat(text)


def closing(**over):
    summary = {"project": "Harbor Hours", "branch": "main", "saved": "committed", "handoff_ready": True,
               "boundary": "local_only", "verdicts": {"project": "local_only"}, "phase": "Brief drafted",
               "released": None, "releases": False, "this_session": ["The launch brief is drafted."],
               "next": "You: ask the product team.", "why": "Their answers finish the brief.",
               "next_in": [], "tree": "clean", "warnings": [], "host": "claude"}
    summary.update(over)
    return summary


class OnePlainCommand(unittest.TestCase):
    """Row 1."""

    def test_each_guide_says_one_plain_call(self):
        for rel in ("references/in.md", "references/out.md"):
            with self.subTest(rel=rel):
                text = guide(rel)
                self.assertIn("Each command is one plain call: one helper or git command on its own, with "
                              "absolute paths", text)
                self.assertIn("never `cd … &&`, `; echo`, `| head` or another command chained on", text)
                self.assertIn("edit prose with the host's file-edit tool, never `python3 - <<EOF`", text)
        self.assertIn("Each command is one plain call with absolute paths: no `cd … &&`, `; echo` or "
                      "`| head` chained on", guide("SKILL.md"))


class ProjectNameWithoutReadme(unittest.TestCase):
    """Row 14."""

    def test_the_notes_file_heading_comes_before_the_folder_name(self):
        text = " ".join(guide("references/in.md").split())
        # Round 5 replaced "the first `.md` file there by name" with a root notes.md; see round5 tests.
        self.assertIn("with no README, or a README with no heading, the first heading of a `notes.md` at its "
                      "root", text)
        self.assertIn("else the folder name; and when that name is itself a placeholder word (`project`, "
                      "`app`, `work`), “Your project”.", text)
        self.assertIn("Never the literal word “project” on its own", text)
        self.assertIn("else the folder name (“Your project” for a placeholder name)", guide("SKILL.md"))


class LocalOnlySaidOnce(unittest.TestCase):
    """Row 5 / new 3."""

    def test_the_cell_says_it_and_attention_does_not(self):
        for markdown in (False, True):
            with self.subTest(markdown=markdown):
                out = view.render_closing(closing(), NOW, 80, False, markdown=markdown)
                self.assertEqual(flat(out).count("Saved on this computer only."), 1)
                self.assertNotIn("ATTENTION", out)
                self.assertNotIn("checked", out)
                self.assertNotIn("remote", out.lower())
        rows = [line for line in view.render_closing(closing(), NOW, 80, False, markdown=True).splitlines()
                if line.startswith("|")]
        self.assertEqual(rows[2], "| Harbor Hours | Saved on this computer only. | Brief drafted |")

    def test_docs_quote_the_same_line(self):
        for rel in ("docs/guide/getting-started.md", "README.md"):
            with self.subTest(rel=rel):
                text = flat((ROOT / rel).read_text(encoding="utf-8"))
                self.assertIn("“Saved on this computer only”".replace("“", '"').replace("”", '"'), text)
                self.assertNotIn("no other copy was checked", text)
                self.assertNotIn("no Git remote is configured\"", text)


class OutKeepsItsPlumbing(unittest.TestCase):
    """New 2 and new 6."""

    def test_the_measurement_stays_in_the_record(self):
        self.assertIn("The measurement is for the record only: never tell the person the token or byte "
                      "figures, the target or the reading set's size.", guide("references/out.md"))

    def test_the_first_out_line_is_the_renderers(self):
        self.assertIn("The renderer writes that line: do not say it in `this_session` or anywhere else.",
                      guide("references/out.md"))


class SketchbookHeaderKeptCurrent(unittest.TestCase):
    """Row 18: "Drafting the brief itself is not yet approved" survived two approvals."""

    def test_out_rewrites_a_resolved_header_line(self):
        self.assertIn("When what it adds resolves a header or position line (stage, what is or is not yet "
                      "approved) or a field marked pending or asked, rewrite that line too, never only "
                      "append below it", guide("references/out.md"))


if __name__ == "__main__":
    unittest.main()
