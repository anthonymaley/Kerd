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


def bash_call(command, tid="toolu_1"):
    return {"type": "tool_use", "id": tid, "name": "Bash", "input": {"command": command}}


def tool_use(command, tid="toolu_1"):
    return json.dumps({"type": "assistant", "message": {"content": [bash_call(command, tid)]}},
                      separators=(",", ":"))


def tool_uses(*calls):
    """One assistant message carrying several Bash calls: (command, id) pairs."""
    return json.dumps({"type": "assistant", "message": {"content": [bash_call(c, t) for c, t in calls]}},
                      separators=(",", ":"))


def tool_result(output, tid="toolu_1"):
    return json.dumps({"type": "user", "message": {"content": [
        {"tool_use_id": tid, "type": "tool_result", "content": output, "is_error": False}]},
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
    check = "S=/p/switch/scripts; python3 $S/handoff.py --project /w boundary --preserve scratch.patch"
    ok = '{\n  "status": "boundary_ok",\n  "branch": "main"\n}'

    def run_trace(self, *later):
        return trace(tool_use("git push origin main"), tool_use(self.check), tool_result(self.ok), *later)

    def test_passed_last_passes(self):
        self.assertTrue(self.rx.search(self.run_trace(
            tool_use("python3 /p/switch/scripts/where_we_are.py --closing - --markdown"))))

    def test_save_then_boundary_in_one_command_passes(self):
        t = trace(tool_use("python3 $S/handoff.py --project . save --push --file a.md; echo \"exit $?\"; "
                           "python3 $S/handoff.py --project . boundary; echo \"exit $?\""),
                  tool_result('{"status": "saved_to_remote"}\nexit 0\n{"status": "boundary_ok"}\nexit 0'))
        self.assertTrue(self.rx.search(t))

    def test_helper_through_a_variable_passes(self):
        # Sonnet 5.5, 2026-10-06 eval: H=.../handoff.py, then `python3 $H --project . boundary`.
        t = trace(tool_use("H=/p/switch/scripts/handoff.py; python3 $H --project . save --push --file a.md; "
                           "echo \"exit $?\"; python3 $H --project . boundary; echo \"boundary exit $?\""),
                  tool_result('{"status": "saved_to_remote"}\nexit 0\n{"status": "boundary_ok"}'))
        self.assertTrue(self.rx.search(t))

    def test_real_command_shapes_pass(self):
        # Sonnet 5.5 evals, 2026-10-06: a new line before python3 (JSON's \\n is no word boundary for \\b),
        # 2>&1 with an output filter, and the helper held in a variable.
        for cmd in ("S=/p/scripts\npython3 $S/handoff.py --project . boundary --preserve scratch.patch 2>&1 "
                    "| grep -v -e xcrun -e DVT; echo exit=$?",
                    "S=/p/scripts/handoff.py\npython3 $S --project . boundary; echo \"boundary exit $?\"",
                    "python3 /p/scripts/handoff.py --project . boundary 2>&1 | tail -40"):
            with self.subTest(cmd=cmd):
                self.assertTrue(self.rx.search(trace(tool_use(cmd), tool_result(self.ok))))

    def test_output_cut_before_the_status_fails(self):
        # Same evals: `| tail -15` cut the status, the run never saw boundary_ok, and its box still said passed.
        t = trace(tool_use("python3 $S/scripts/handoff.py --project . boundary 2>&1 | tail -15"),
                  tool_result('  "branch": "main",\n  "clean": true\n}'))
        self.assertFalse(self.rx.search(t))

    def test_a_mutation_on_a_new_line_after_it_fails(self):
        self.assertFalse(self.rx.search(self.run_trace(tool_use("echo done\ngit push origin main"))))

    def test_a_mutation_on_a_new_line_in_the_same_command_fails(self):
        # codex-tui round 2: a lost backslash let one "statement" run past JSON's \n.
        t = trace(tool_use("python3 /p/handoff.py --project /w boundary\ngit push origin main"), tool_result(self.ok))
        self.assertFalse(self.rx.search(t))

    def test_the_result_is_the_boundary_calls_own(self):
        # codex-tui round 2: two calls in one message; results matched by tool ID, not position.
        old_record = tool_result('{"status": "boundary_ok"}', "toolu_old")
        failed = tool_result("Traceback: handoff.py failed", "toolu_b")
        t = trace(tool_uses(("cat /w/.boundary-log", "toolu_old"), (self.check, "toolu_b")), old_record, failed)
        self.assertFalse(self.rx.search(t))
        unrelated_first = trace(tool_uses(("git status --short", "toolu_s"), (self.check, "toolu_b")),
                                tool_result("", "toolu_s"), tool_result(self.ok, "toolu_b"))
        self.assertTrue(self.rx.search(unrelated_first))

    def test_quoted_git_options_do_not_hide_a_mutation(self):
        for later in ('git -C "/work/My Project" push origin main', 'git -c user.name="A User" commit -m x'):
            with self.subTest(later=later):
                self.assertFalse(self.rx.search(self.run_trace(tool_use(later))))

    def test_read_only_stash_and_tag_pass(self):
        for later in ("git stash list", "git stash show -p", "git tag --list", "git tag -l 'v*'", "git tag"):
            with self.subTest(later=later):
                self.assertTrue(self.rx.search(self.run_trace(tool_use(later))))

    def test_a_later_mutating_call_in_the_same_message_fails(self):
        # codex-tui round 3: boundary and push as separate calls in one assistant message.
        t = trace(tool_uses((self.check, "toolu_b"), ("git push origin main", "toolu_p")),
                  tool_result(self.ok, "toolu_b"), tool_result("", "toolu_p"))
        self.assertFalse(self.rx.search(t))

    def test_single_quoted_git_options_do_not_hide_a_mutation(self):
        self.assertFalse(self.rx.search(self.run_trace(tool_use("git -C '/work/My Project' push origin main"))))

    def test_newline_endings_and_echoes_pass(self):
        for cmd in (self.check + "\n", self.check + "\necho \"boundary exit $?\""):
            with self.subTest(cmd=cmd):
                self.assertTrue(self.rx.search(trace(tool_use(cmd), tool_result(self.ok))))

    def test_a_save_through_a_variable_after_it_fails(self):
        self.assertFalse(self.rx.search(self.run_trace(tool_use("python3 $H --project . save --push --file a.md"))))

    def test_read_only_git_after_it_passes(self):
        for later in ("git diff HEAD -- commit.md", "git config --get push.default", "git -C /w log --oneline -1",
                      "git status --short"):
            with self.subTest(later=later):
                self.assertTrue(self.rx.search(self.run_trace(tool_use(later))))

    def test_refused_fails(self):
        t = trace(tool_use(self.check), tool_result('{"status": "boundary_refused"}'))
        self.assertFalse(self.rx.search(t))

    def test_ok_then_a_later_refusal_fails(self):
        self.assertFalse(self.rx.search(self.run_trace(tool_use(self.check),
                                                       tool_result('{"status": "boundary_refused"}'))))

    def test_a_mutation_after_it_fails(self):
        for later in ("git -C /w commit -m x", "git push origin main", "git -c user.name=x commit -m y",
                      "git --no-pager tag v1", "python3 /p/handoff.py --project /w save --push CONTEXT.md"):
            with self.subTest(later=later):
                self.assertFalse(self.rx.search(self.run_trace(tool_use(later))))

    def test_a_mutation_in_the_same_command_fails(self):
        for cmd in (self.check + " && git -C /w commit -m x", self.check + "; git push origin main",
                    self.check + " && ./save.sh"):
            with self.subTest(cmd=cmd):
                self.assertFalse(self.rx.search(trace(tool_use(cmd), tool_result(self.ok))))

    def test_boundary_ok_from_another_command_fails(self):
        for cmd in ("cat /p/switch/scripts/handoff.py", "grep -n boundary_ok /p/switch/scripts/handoff.py"):
            with self.subTest(cmd=cmd):
                t = trace(tool_use(cmd), tool_result('result = {"status": "boundary_refused" if failures else "boundary_ok"}'))
                self.assertFalse(self.rx.search(t))

    def test_typed_but_not_run_fails(self):
        self.assertFalse(self.rx.search(trace(tool_use(self.check + " # boundary_ok"))))


class ConductorShellReadTests(unittest.TestCase):
    rx = re.compile(pattern("switch-in-clean", "conductor-not-shell-read"))

    def test_shell_reads_of_conductor_are_caught(self):
        for cmd in ("cat /p/skills/conductor/SKILL.md", "sed -n 1,40p /p/conductor/references/entry.md",
                    "grep -n Shape /p/conductor/references/journey.md",
                    "cd skills/conductor && cat SKILL.md", "ls\ncat /p/conductor/SKILL.md",
                    "rg -n Shape /p/conductor/SKILL.md\nrg --files .",
                    # Ordinary In has no reason to enter Conductor's folder: any cd into it counts.
                    "cd /p/conductor; cd references; cat journey.md", "cd /p/conductor/references && cat journey.md",
                    "cd skills/conductor; cd ../switch; cat SKILL.md", "cd /p/conductor; sed -n 1,20p references/entry.md"):
            with self.subTest(cmd=cmd):
                self.assertTrue(self.rx.search(tool_use(cmd)))

    def test_other_commands_are_not(self):
        for cmd in ("python3 /p/switch/scripts/where_we_are.py --summary - --markdown", "cat TODO.md",
                    "cat /p/switch/references/in.md", "rg --files /p/conductor/references/",
                    "grep -l Shape /p/conductor/references/*.md", "ls /p/conductor/references/"):
            with self.subTest(cmd=cmd):
                self.assertFalse(self.rx.search(tool_use(cmd)))


if __name__ == "__main__":
    unittest.main()
