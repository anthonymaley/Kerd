"""Batch 1114: what the second first-user run and the 2026-11-13 weekly review left in Switch.

N4: a first arrival was headed "PROJECT" because the caller passed the folder name.
N6 / #24: Out committed generated files without naming them, or could leave them unmentioned.
Weekly review: Out saved a next step naming README sections that did not exist.

Guide checks find the wording, not that a model follows it. The measure checks run
the helper the guide now points Out at, to show it fails closed.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[4]
SWITCH = ROOT / "skills/switch"
SCRIPT = SWITCH / "scripts" / "handoff.py"
SPEC = importlib.util.spec_from_file_location("handoff_batch_1114", SCRIPT)
handoff = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(handoff)


def guide(rel):
    return " ".join((SWITCH / rel).read_text(encoding="utf-8").split())


class ProjectDisplayName(unittest.TestCase):
    """N4."""

    def test_in_takes_the_readme_heading_before_the_folder_name(self):
        self.assertIn("`project` is the project already restored, by its display name: the text of "
                      "the first heading in its `README.md` when there is one (markup removed), else "
                      "the folder name", guide("references/in.md"))
        self.assertIn("PROJECT is the README's first heading, else the folder name", guide("SKILL.md"))


class OutSaveScope(unittest.TestCase):
    """N6 / #24."""

    def test_untracked_files_are_named_once_in_a_speech_bubble(self):
        text = guide("references/out.md")
        self.assertIn("files the sitting created or changed and left uncommitted, tracked or untracked", text)
        self.assertIn("Never leave one unmentioned either. Ask it once, in Kerd's speech-bubble form", text)
        self.assertIn("`> 💬 **These files of yours changed and aren't saved yet: tally.py, and "
                      "requests-2026-11-14.csv, which the export made. Which should I save too?**`", text)
        self.assertIn("not asked about again. A tracked file they want left out cannot be preserved", text)
        self.assertIn("should never be saved, add one anchored, escaped rule for exactly its path to "
                      "`.gitignore`", text)

    def test_skill_reminder_matches(self):
        self.assertIn("other files the sitting created or changed and left uncommitted, untracked ones too",
                      guide("SKILL.md"))
        self.assertIn("in one speech-bubble question that leaves none unmentioned", guide("SKILL.md"))


class NextStepTargetsExist(unittest.TestCase):
    """Weekly review 2026-11-13: confirm a named file or section exists before saving it."""

    def test_out_checks_with_measure_and_fails_closed(self):
        text = guide("references/out.md")
        self.assertIn("confirm that every file or section the next step names as already there", text)
        self.assertIn("Only `status: \"measured\"` with exit 0 confirms them.", text)
        self.assertIn("a check that could not run or be read is not \"exists\"", text)
        self.assertIn("confirmed by `measure` first; a blocked check is not \"exists\"", guide("SKILL.md"))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="switch-batch-1114-")
        self.root = Path(self.temp.name).resolve()
        for args in (["init", "-q"], ["config", "user.email", "t@example.com"], ["config", "user.name", "T"]):
            subprocess.run(["git", "-C", str(self.root), *args], check=True, capture_output=True)
        (self.root / "CONTEXT.md").write_text("# Context\n\nNext: edit README Usage.\n", encoding="utf-8")
        (self.root / "README.md").write_text("# Tally\n\n## Usage\n\nRun it.\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "init"], check=True, capture_output=True)

    def tearDown(self):
        self.temp.cleanup()

    def run_measure(self, *extra):
        return subprocess.run([sys.executable, str(SCRIPT), "--project", str(self.root), "measure",
                               "--record", "CONTEXT.md", *extra], capture_output=True, text=True)

    def test_a_real_section_is_confirmed(self):
        result = self.run_measure("--section", "README.md", "## Usage")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "measured")

    def test_a_missing_section_or_file_blocks(self):
        for extra in (["--section", "README.md", "## Install"], ["--file", "docs/missing.md"]):
            with self.subTest(extra=extra):
                result = self.run_measure(*extra)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stderr)["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
