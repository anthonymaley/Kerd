"""Batch 1114, round 5: the walkthrough rerun on released 0.197.0 (first-user-5).

New 1: the first arrival was headed "QUOTES FROM THE PILOT": the name came from the first `.md` by name.
New 6: each Out made a temp file with mktemp, wrote it and removed it: three prompts.
New 2: RELEASED came back on a launch brief: `releases` was passed without the four reads.
New 5: "keep the technical stuff out of my way" was never saved, so a fresh session said "Conductor · Shape".

Guide checks find the wording, not that a model follows it.
"""
from pathlib import Path
import unittest

SWITCH = Path(__file__).resolve().parents[2]


def guide(rel):
    return " ".join((SWITCH / rel).read_text(encoding="utf-8").split())


class ProjectNameNeverByAlphabet(unittest.TestCase):
    """New 1."""

    def test_in_names_notes_md_and_refuses_alphabetical_order(self):
        text = guide("references/in.md")
        self.assertNotIn("the first `.md` file there by name", text)
        self.assertNotIn("main notes file", text)
        self.assertIn("the first heading of a `notes.md` at its root (any case: `Notes.md`, `NOTES.md`) "
                      "when there is one; else the folder name", text)
        self.assertIn("Never a file picked by alphabetical order", text)

    def test_skill_md_says_the_same(self):
        text = guide("SKILL.md")
        self.assertNotIn("main notes file", text)
        self.assertIn("PROJECT is the README's first heading, else the first heading of a root `notes.md` "
                      "(any case), else the folder name (“Your project” for a placeholder name), never a "
                      "file picked by alphabetical order", text)


class OutInputsOnStdin(unittest.TestCase):
    """New 6."""

    def test_out_pipes_carry_phrases(self):
        text = guide("references/out.md")
        self.assertIn("**Pipe them on stdin**", text)
        self.assertIn("printf '%s\\n' 'first finding' 'second finding' | python3", text)
        self.assertIn("--carry-file -", text)
        self.assertIn("Do not make a temporary file for them", text)
        self.assertIn("Only where a host cannot pipe at all, make the file with `mktemp`, remove it after "
                      "the call, and say so in that turn", text)

    def test_in_and_skill_md_agree(self):
        self.assertIn("Every Switch input that accepts `-` goes on stdin, never through a temporary file",
                      guide("references/in.md"))
        self.assertIn("runs with the phrases piped to `--carry-file -` (no temporary file;", guide("SKILL.md"))

    def test_the_instruction_is_true_of_the_scripts(self):
        handoff = (SWITCH / "scripts/handoff.py").read_text(encoding="utf-8")
        view = (SWITCH / "scripts/where_we_are.py").read_text(encoding="utf-8")
        self.assertIn('if value == "-":', handoff)
        self.assertIn('sys.stdin.read() if args.closing == "-"', view)
        self.assertIn('sys.stdin.read() if args.summary == "-"', view)


class ReleasesChecksComeFirst(unittest.TestCase):
    """New 2."""

    def test_four_reads_before_the_box_and_a_default(self):
        text = guide("references/out.md")
        self.assertIn("**`releases` comes from four reads, made before filling the box.**", text)
        for read in ("`git tag --list` succeeds and prints nothing",
                     "no `CHANGELOG*` or release-notes file at the root",
                     "no version field the project bumps",
                     "no record (CONTEXT.md, TODO.md, the session logs) mentions a release"):
            self.assertIn(read, text)
        self.assertIn("With the reads not made, pass `null`, never `false` and never a guess", text)
        self.assertIn("`releases` is set only after the guide's four reads (not made: `null`)", guide("SKILL.md"))


class TechnicalDetailPreferenceCarried(unittest.TestCase):
    """New 5."""

    def test_out_saves_it_in_their_words_dated(self):
        text = guide("references/out.md")
        self.assertIn("save it in CONTEXT.md's governing lines", text)
        self.assertIn("in their own words and dated, as one line: "
                      "`Person's preference (2026-11-14): “keep the technical stuff out of my way”.`", text)

    def test_in_passes_it_to_conductor(self):
        self.assertIn("and any saved preference about technical detail (CONTEXT.md's "
                      "`Person's preference (<date>): “…”` line), quoted in the person's words",
                      guide("references/in.md"))


if __name__ == "__main__":
    unittest.main()
