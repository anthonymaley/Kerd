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


def run(*args, session=None, codex=None):
    env = {k: v for k, v in os.environ.items() if k not in needs.SESSION_ENV}
    if session:
        env["CLAUDE_CODE_SESSION_ID"] = session
    if codex:
        env["CODEX_THREAD_ID"] = codex
    return subprocess.run(["python3", str(NEEDS), *args], capture_output=True, text=True, env=env)


def show(d, session=""):
    return run("show", "--project", d, "--session=" + session).stdout


class NeedsTest(unittest.TestCase):
    def test_set_show_clear(self):
        d = repo()
        self.assertEqual(show(d, "s1"), "")
        self.assertEqual(run("set", "--project", d, "  Release   0.205.0 \n", session="s1").returncode, 0)
        self.assertEqual(show(d, "s1"), "Release 0.205.0\n")
        self.assertTrue(os.path.exists(os.path.join(d, ".git", "kerd", "needs-you", needs.session_file("s1"))))
        self.assertEqual(run("clear", "--project", d, session="s1").returncode, 0)
        self.assertEqual(show(d, "s1"), "")
        self.assertEqual(run("clear", "--project", d, session="s1").returncode, 0)

    def test_show_is_session_scoped(self):
        d = repo()
        run("set", "--project", d, "from A", session="a")
        run("set", "--project", d, "from B", session="b")
        self.assertEqual(show(d, "a"), "from A\n")
        self.assertEqual(show(d, "b"), "from B\n")
        self.assertEqual(show(d, ""), "")
        self.assertEqual(show(d, "c"), "")
        run("clear", "--project", d, session="a")
        self.assertEqual(show(d, "b"), "from B\n")

    def test_set_refuses_without_session_id(self):
        d = repo()
        r = run("set", "--project", d, "q")
        self.assertEqual(r.returncode, 2)
        self.assertIn("no session id", r.stderr)
        self.assertFalse(os.path.exists(os.path.join(d, ".git", "kerd")))
        self.assertEqual(run("clear", "--project", d).returncode, 2)

    def test_codex_thread_id_used(self):
        d = repo()
        run("set", "--project", d, "codex q", codex="thr1")
        self.assertEqual(show(d, "thr1"), "codex q\n")

    def test_ids_never_collide(self):
        d = repo()
        h = needs.session_file("a/b")
        for sid, text in (("a/b", "one"), ("ab", "two"), ("a.b", "three"), (h, "four")):
            run("set", "--project", d, text, session=sid)
        for sid, text in (("a/b", "one"), ("ab", "two"), ("a.b", "three"), (h, "four")):
            self.assertEqual(show(d, sid), text + "\n")
        self.assertEqual(len(os.listdir(os.path.join(d, ".git", "kerd", "needs-you"))), 4)
        self.assertEqual(len(h), 32)

    def test_no_pruning_of_old_open_questions(self):
        d = repo()
        run("set", "--project", d, "old", session="old")
        f = os.path.join(d, ".git", "kerd", "needs-you", needs.session_file("old"))
        t = os.path.getmtime(f) - 90 * 24 * 3600
        os.utime(f, (t, t))
        run("set", "--project", d, "new", session="new")
        self.assertEqual(show(d, "old"), "old\n")

    def test_status_json_file_with_newline_in_path(self):
        d = repo()
        odd = os.path.join(d, "sub\nfolder")
        os.makedirs(odd)
        subprocess.run(["git", "init", "-q", odd], check=True)
        run("set", "--project", odd, "odd q", session="s1")
        f = os.path.join(d, "status.json")
        Path(f).write_text(json.dumps({"workspace": {"current_dir": odd}, "session_id": "s1"}))
        r = run("show", "--line", "--status-json", f)
        self.assertEqual(r.stdout, "💬 Needs you: odd q\n")
        Path(f).write_text("not json")
        self.assertEqual(run("show", "--line", "--status-json", f).stdout, "")

    def test_legacy_single_file_ignored_then_replaced(self):
        d = repo()
        os.makedirs(os.path.join(d, ".git", "kerd"))
        legacy = Path(d, ".git", "kerd", "needs-you")
        legacy.write_text("legacy q\n")
        self.assertEqual(show(d, "s"), "")
        self.assertEqual(run("set", "--project", d, "mine", session="s").returncode, 0)
        self.assertEqual(show(d, "s"), "mine\n")

    def test_control_characters_stripped(self):
        d = repo()
        run("set", "--project", d, "a\x1b[31mred\x1b[0m\x07 b\x9bc\x01d", session="s")
        self.assertEqual(show(d, "s"), "ared bcd\n")

    def test_worktree_gitdir_file(self):
        d = repo()
        wt = tempfile.mkdtemp()
        gd = os.path.join(d, ".git", "worktrees", "w")
        os.makedirs(gd)
        Path(wt, ".git").write_text("gitdir: " + gd + "\n")
        run("set", "--project", wt, "wt q", session="s")
        self.assertTrue(os.path.exists(os.path.join(gd, "kerd", "needs-you", needs.session_file("s"))))

    def test_asks_only_contiguous_table_and_case(self):
        text = "## NOW\n\n### Asks\n\n" + HEAD + "| a | First | | | | | | |\n\nstray\n| b | Not mine | | | | | | |\n"
        self.assertEqual(needs.asks_questions(text), ["First"])

    def test_label_trimmed_to_limit(self):
        d = repo()
        run("set", "--project", d, "x" * 200, session="s")
        self.assertEqual(len(show(d, "s").strip()), needs.LABEL_MAX)

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
        run("set", "--project", d, "Pick a name", session="s")
        self.assertEqual(show(d, "s"), "Pick a name\nShip it\n")
        self.assertEqual(show(d, ""), "Ship it\n")
        self.assertEqual(show(d, "other"), "Ship it\n")

    def test_line_format(self):
        self.assertEqual(needs.line([]), "")
        self.assertEqual(needs.line(["a", "b"]), "💬 Needs you: a · b")
        self.assertEqual(needs.line(["a", "b", "c", "d"]), "💬 Needs you: a · b +2")

    def test_missing_project_never_crashes(self):
        r = run("show", "--project", "/nonexistent/zzz", "--session=s")
        self.assertEqual((r.returncode, r.stdout), (0, ""))
        self.assertEqual(run("clear", "--project", "/nonexistent/zzz", session="s").returncode, 0)


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
        run("set", "--project", d, "Release 0.205.0", session="sess1")
        out = self.sl(json.dumps({"workspace": {"current_dir": d}, "session_id": "sess1"}), "echo INNER")
        self.assertRegex(out, r"^\d\d:\d\d · 💬 Needs you: Release 0\.205\.0 · INNER\n$")

    def test_other_sessions_question_not_shown(self):
        d = repo()
        run("set", "--project", d, "Release 0.205.0", session="sess1")
        out = self.sl(json.dumps({"cwd": d, "session_id": "sess2"}))
        self.assertRegex(out, r"^\d\d:\d\d\n$")

    def test_nul_byte_input_is_quiet_and_forwarded(self):
        d = repo()
        out_file = os.path.join(d, "got")
        payload = b'{"cwd":"/x"}\x00\x01tail\n\n'
        r = subprocess.run(["bash", str(STATUSLINE), "cat > " + out_file], input=payload, capture_output=True)
        self.assertEqual(r.stderr, b"")
        self.assertRegex(r.stdout.decode(), r"^\d\d:\d\d\n$")
        self.assertEqual(Path(out_file).read_bytes(), payload)

    def test_newline_in_cwd_still_finds_question(self):
        d = repo()
        odd = os.path.join(d, "a\nb")
        os.makedirs(odd)
        subprocess.run(["git", "init", "-q", odd], check=True)
        run("set", "--project", odd, "odd q", session="s9")
        out = self.sl(json.dumps({"cwd": odd, "session_id": "s9"}))
        self.assertRegex(out, r"💬 Needs you: odd q\n$")

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
