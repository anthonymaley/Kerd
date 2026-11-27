import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
NEEDS = ROOT / "needs.py"
STATUSLINE = REPO / "hooks" / "statusline.sh"
spec = importlib.util.spec_from_file_location("needs", NEEDS)
needs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(needs)

HEAD = "| Ask id | Question | Default | Why | Blocks | Kind | Asked | Answer where |\n|---|---|---|---|---|---|---|---|\n"


def todo(*questions):
    rows = "".join(f"| a{i} | {q} | d | w | b | k | t | here |\n" for i, q in enumerate(questions))
    return f"# TODO\n\n## Now\n\n### Queue\n\n| x |\n\n### Asks\n\n{HEAD}{rows}\n## Backlog\n\n| z | Other thing | q |\n"


def repo():
    d = tempfile.mkdtemp()
    subprocess.run(["git", "init", "-q", d], check=True)
    return d


def run(*args, session=None):
    env = {k: v for k, v in os.environ.items() if k not in needs.SESSION_ENV}
    if session:
        env["CLAUDE_CODE_SESSION_ID"] = session
    return subprocess.run(["python3", str(NEEDS), *args], capture_output=True, text=True, env=env)


class NeedsTest(unittest.TestCase):
    def test_set_show_clear(self):
        d = repo()
        self.assertEqual(run("show", "--project", d).stdout, "")
        self.assertEqual(run("set", "--project", d, "  Release   0.205.0 \n").returncode, 0)
        self.assertEqual(run("show", "--project", d).stdout, "Release 0.205.0\n")
        self.assertTrue(os.path.exists(os.path.join(d, ".git", "kerd", "needs-you", "default")))
        self.assertEqual(run("clear", "--project", d).returncode, 0)
        self.assertEqual(run("show", "--project", d).stdout, "")
        self.assertEqual(run("clear", "--project", d).returncode, 0)

    def test_sessions_are_separate(self):
        d = repo()
        run("set", "--project", d, "from A", session="a/../1")
        run("set", "--project", d, "from B", session="b")
        self.assertEqual(run("show", "--project", d).stdout, "from A\nfrom B\n")
        self.assertTrue(os.path.exists(os.path.join(d, ".git", "kerd", "needs-you", "a1")))
        run("clear", "--project", d, session="a/../1")
        self.assertEqual(run("show", "--project", d).stdout, "from B\n")

    def test_old_files_ignored_and_legacy_file_read(self):
        d = repo()
        run("set", "--project", d, "old one", session="a")
        f = os.path.join(d, ".git", "kerd", "needs-you", "a")
        t = os.path.getmtime(f) - 8 * 24 * 3600
        os.utime(f, (t, t))
        self.assertEqual(run("show", "--project", d).stdout, "")
        d2 = repo()
        os.makedirs(os.path.join(d2, ".git", "kerd"))
        Path(d2, ".git", "kerd", "needs-you").write_text("legacy q\n")
        self.assertEqual(run("show", "--project", d2).stdout, "legacy q\n")
        run("set", "--project", d2, "mine", session="s")
        self.assertEqual(run("show", "--project", d2).stdout, "legacy q\nmine\n")

    def test_control_characters_stripped(self):
        d = repo()
        run("set", "--project", d, "a\x1b[31mred\x1b[0m\x07 b\x9bc\x01d", session="s")
        self.assertEqual(run("show", "--project", d).stdout, "ared bcd\n")

    def test_worktree_gitdir_file(self):
        d = repo()
        wt = tempfile.mkdtemp()
        gd = os.path.join(d, ".git", "worktrees", "w")
        os.makedirs(gd)
        Path(wt, ".git").write_text("gitdir: " + gd + "\n")
        run("set", "--project", wt, "wt q")
        self.assertTrue(os.path.exists(os.path.join(gd, "kerd", "needs-you", "default")))

    def test_asks_only_contiguous_table_and_case(self):
        text = "## NOW\n\n### Asks\n\n" + HEAD + "| a | First | | | | | | |\n\nstray\n| b | Not mine | | | | | | |\n"
        self.assertEqual(needs.asks_questions(text), ["First"])

    def test_label_trimmed_to_limit(self):
        d = repo()
        run("set", "--project", d, "x" * 200)
        self.assertEqual(len(run("show", "--project", d).stdout.strip()), needs.LABEL_MAX)

    def test_asks_table_rows(self):
        qs = needs.asks_questions(todo("Push release 0.205.0 to the remote now please ok", "[Merge it](http://x)"))
        self.assertEqual(qs, ["Push release 0.205.0 to the remote", "Merge it"])

    def test_asks_ignores_backlog_and_empty(self):
        self.assertEqual(needs.asks_questions(todo()), [])
        self.assertEqual(needs.asks_questions(""), [])
        self.assertEqual(needs.asks_questions("## Backlog\n### Asks\n" + HEAD + "| a | Q | | | | | | |\n"), [])

    def test_combined_label_and_asks(self):
        d = repo()
        Path(d, "TODO.md").write_text(todo("Ship it"))
        run("set", "--project", d, "Pick a name")
        self.assertEqual(run("show", "--project", d).stdout, "Pick a name\nShip it\n")

    def test_line_format(self):
        self.assertEqual(needs.line([]), "")
        self.assertEqual(needs.line(["a", "b"]), "💬 Needs you: a · b")
        self.assertEqual(needs.line(["a", "b", "c", "d"]), "💬 Needs you: a · b +2")

    def test_missing_project_never_crashes(self):
        r = run("show", "--project", "/nonexistent/zzz")
        self.assertEqual((r.returncode, r.stdout), (0, ""))
        self.assertEqual(run("clear", "--project", "/nonexistent/zzz").returncode, 0)


class StatuslineTest(unittest.TestCase):
    def sl(self, payload, *args):
        env = dict(os.environ)
        return subprocess.run(["bash", str(STATUSLINE), *args], input=payload, capture_output=True,
                              text=True, env=env).stdout

    def test_quiet_when_nothing_waits(self):
        d = repo()
        out = self.sl(json.dumps({"workspace": {"current_dir": d}}))
        self.assertRegex(out, r"^\d\d:\d\d\n$")

    def test_segment_after_clock_and_inner_kept(self):
        d = repo()
        run("set", "--project", d, "Release 0.205.0")
        out = self.sl(json.dumps({"workspace": {"current_dir": d}}), "echo INNER")
        self.assertRegex(out, r"^\d\d:\d\d · 💬 Needs you: Release 0\.205\.0 · INNER\n$")

    def test_cwd_fallback_and_asks(self):
        d = repo()
        Path(d, "TODO.md").write_text(todo("One", "Two", "Three"))
        out = self.sl(json.dumps({"cwd": d}))
        self.assertRegex(out, r"💬 Needs you: One · Two \+1\n$")

    def test_inner_output_without_needs_and_bad_json(self):
        self.assertRegex(self.sl("{}", "echo INNER"), r"^\d\d:\d\d · INNER\n$")
        self.assertRegex(self.sl("not json", "echo INNER"), r"^\d\d:\d\d · INNER\n$")

    def test_inner_receives_stdin_bytes(self):
        d = repo()
        out_file = os.path.join(d, "got")
        for tail in (b"\n\n", b"", b"\n"):
            payload = json.dumps({"cwd": d}).encode() + tail
            subprocess.run(["bash", str(STATUSLINE), "cat > " + out_file], input=payload, capture_output=True)
            self.assertEqual(Path(out_file).read_bytes(), payload)

    def test_inner_receives_stdin(self):
        d = repo()
        payload = json.dumps({"cwd": d})
        out = self.sl(payload, "python3 -c 'import sys,json;print(json.load(sys.stdin)[\"cwd\"])'")
        self.assertIn(d, out)


if __name__ == "__main__":
    unittest.main()
