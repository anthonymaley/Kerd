"""Switch's trace graders tell a pass from a slip.
codex-tui (2026-10-06 11:51) found the old graders matched command names: a
`head` slice of a guide passed, a refused or early boundary check passed, and a
shell read of Conductor went unseen. Two one-run probes the same evening showed
the eval trace records each tool's output in order (Bash and Read alike), so the
graders now read outputs. These tests run each pattern over made-up trace lines
in the probes' shape, and check the guides still carry the anchors they match.
"""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[4]
EVALS = ROOT / "evals"
IN_CASES = ("switch-in-clean", "switch-in-dirty-private", "switch-in-no-log-human")
OUT_CASES = ("switch-out-clean", "switch-out-dirty-private", "switch-out-no-log-human")


def pattern(case, grader):
    text = (EVALS / case / "graders" / f"{grader}.md").read_text(encoding="utf-8")
    line = next(l for l in text.splitlines() if l.startswith("pattern: '"))
    return line[len("pattern: '"):-1].replace("''", "'")


def tool_use(command):
    return json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Bash", "input": {"command": command}}]}}, separators=(",", ":"))


def tool_result(output):
    return json.dumps({"type": "user", "message": {"content": [
        {"tool_use_id": "t", "type": "tool_result", "content": output, "is_error": False}]},
        "tool_use_result": {"stdout": output}}, separators=(",", ":"))


def trace(*lines):
    return "\n".join(lines)


def last_line(rel):
    return [l for l in (ROOT / rel).read_text(encoding="utf-8").splitlines() if l.strip()][-1]


class GraderCopiesTests(unittest.TestCase):
    def test_each_grader_is_identical_across_its_cases(self):
        for cases, grader in ((IN_CASES, "in-guide-read"), (IN_CASES, "conductor-not-shell-read"),
                              (OUT_CASES, "out-guide-read"), (OUT_CASES, "boundary-passed-last")):
            texts = {(EVALS / c / "graders" / f"{grader}.md").read_text(encoding="utf-8") for c in cases}
            with self.subTest(grader=grader):
                self.assertEqual(len(texts), 1)

    def test_old_boundary_grader_is_gone(self):
        for case in OUT_CASES:
            self.assertFalse((EVALS / case / "graders" / "boundary-ran.md").exists())


class GuideReadTests(unittest.TestCase):
    GUIDES = (("switch-in-clean", "in-guide-read", "skills/switch/references/in.md",
               "# In: useful context", "make the banner complete."),
              ("switch-out-clean", "out-guide-read", "skills/switch/references/out.md",
               "# Out: clean boundaries", "Without `--sync` it is local-only."))

    def test_anchors_are_the_guides_first_heading_and_last_sentence(self):
        for _, _, rel, heading, sentence in self.GUIDES:
            with self.subTest(rel=rel):
                first = (ROOT / rel).read_text(encoding="utf-8").splitlines()[0]
                self.assertEqual(first, heading)
                self.assertTrue(last_line(rel).endswith(sentence))

    def test_whole_read_passes_and_slice_fails(self):
        for case, grader, rel, heading, sentence in self.GUIDES:
            rx = re.compile(pattern(case, grader))
            whole = f"1\t{heading}\n2\t\n3\tbody\n400\t{sentence}\n"
            with self.subTest(rel=rel, read="whole"):
                self.assertTrue(rx.search(trace(tool_use(f"cat {rel}"), tool_result(whole))))
            with self.subTest(rel=rel, read="two chunks"):
                self.assertTrue(rx.search(trace(tool_result(f"{heading}\nbody"), tool_result(f"more\n{sentence}"))))
            with self.subTest(rel=rel, read="head slice"):
                self.assertFalse(rx.search(trace(tool_use(f"head -40 {rel}"), tool_result(f"{heading}\nbody"))))
            with self.subTest(rel=rel, read="named in a command only"):
                self.assertFalse(rx.search(trace(tool_use(f"echo '{heading} {sentence}'"))))


class BoundaryTests(unittest.TestCase):
    rx = re.compile(pattern("switch-out-clean", "boundary-passed-last"))
    check = "python3 /p/switch/scripts/handoff.py --project /w boundary --preserve scratch.patch"

    def test_passed_last_passes(self):
        t = trace(tool_use("git push origin main"), tool_use("python3 /p/handoff.py --project /w save --push a.md"),
                  tool_use(self.check), tool_result('{\n  "status": "boundary_ok",\n  "branch": "main"\n}'),
                  tool_use("python3 /p/switch/scripts/where_we_are.py --closing - --markdown"))
        self.assertTrue(self.rx.search(t))

    def test_refused_fails(self):
        t = trace(tool_use(self.check), tool_result('{"status": "boundary_refused"}'))
        self.assertFalse(self.rx.search(t))

    def test_a_save_after_it_fails(self):
        for later in ("git -C /w commit -m x", "git push origin main",
                      "python3 /p/handoff.py --project /w save --push CONTEXT.md"):
            with self.subTest(later=later):
                t = trace(tool_use(self.check), tool_result('{"status": "boundary_ok"}'), tool_use(later))
                self.assertFalse(self.rx.search(t))

    def test_typed_but_not_run_fails(self):
        self.assertFalse(self.rx.search(trace(tool_use(self.check + " # boundary_ok"))))


class ConductorShellReadTests(unittest.TestCase):
    rx = re.compile(pattern("switch-in-clean", "conductor-not-shell-read"))

    def test_shell_reads_of_conductor_are_caught(self):
        for cmd in ("cat /p/skills/conductor/SKILL.md", "sed -n 1,40p /p/conductor/references/entry.md",
                    "grep -n Shape /p/conductor/references/journey.md"):
            with self.subTest(cmd=cmd):
                self.assertTrue(self.rx.search(tool_use(cmd)))

    def test_other_commands_are_not(self):
        for cmd in ("python3 /p/switch/scripts/where_we_are.py --summary - --markdown", "cat TODO.md",
                    "cat /p/switch/references/in.md"):
            with self.subTest(cmd=cmd):
                self.assertFalse(self.rx.search(tool_use(cmd)))


if __name__ == "__main__":
    unittest.main()
