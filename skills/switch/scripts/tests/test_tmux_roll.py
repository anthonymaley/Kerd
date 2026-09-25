"""tmux_roll.py: the chat roll saves under the owner lock, restarts only the recorded pane,
never types into Claude, and picks up only when every check holds."""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import roll  # noqa: E402
import tmux_roll  # noqa: E402

MODEL = "claude-opus-5-5[1m]"
ENV = {"TMUX": "/tmp/tmux-501/default,4013,0", "TMUX_PANE": "%4", "CLAUDE_CODE_SESSION_ID": "old-sid"}
T0 = 1_790_000_000.0


class Result:
    def __init__(self, returncode=0, stdout=""):
        self.returncode, self.stdout = returncode, stdout


class FakeTmux:
    """Records tmux calls; answers `display` with the given pane and PID."""
    def __init__(self, pane="%4", pane_pid=100, respawn_rc=0):
        self.calls, self.pane, self.pane_pid, self.respawn_rc = [], pane, pane_pid, respawn_rc

    def __call__(self, argv, **_):
        self.calls.append(argv)
        if "display" in argv:
            return Result(0, f"{self.pane} {self.pane_pid}\n") if self.pane else Result(1, "")
        if "respawn-pane" in argv:
            return Result(self.respawn_rc)
        return Result(0)


class ChatRollTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        for args in (["init", "-q", "-b", "main"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            subprocess.run(["git", *args], cwd=self.root, check=True)
        (self.root / "docs/work/w").mkdir(parents=True)
        self.record = "docs/work/w/work.md"
        (self.root / self.record).write_text("next: build step 2\n")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "start"], cwd=self.root, check=True)
        self.chat = tmux_roll.Chat(self.root)
        self.parents = {500: 200, 200: 100, 100: 1}   # claude 500 -> shell 200 -> pane 100

    def tearDown(self):
        self.tmp.cleanup()

    def parent(self, pid):
        return self.parents.get(pid)

    def save(self, env=ENV, now=T0, **kw):
        return self.chat.out(self.record, "build step 2", "Build on concert/x; no push", MODEL, 500_000,
                             env=env, now=now, claude_pid=kw.pop("claude_pid", 500), **kw)

    def relaunch(self, tmux, alive=lambda pid: False):
        return self.chat.relaunch(delay=0, run=tmux, alive=alive, parent=self.parent,
                                  sleep=lambda s: None, shell="/bin/zsh")

    # out ------------------------------------------------------------------------------------------
    def test_out_writes_marker_with_verbatim_approval(self):
        data = self.save()
        on_disk = json.loads(self.chat.marker.read_text())
        self.assertEqual(on_disk, data)
        self.assertEqual(data["approval_boundary"], "Build on concert/x; no push")
        self.assertEqual((data["pane"], data["tmux_socket"], data["relaunch"]), ("%4", "/tmp/tmux-501/default", "pending"))

    def test_out_outside_tmux_is_manual_and_needs_no_pane(self):
        data = self.save(env={"CLAUDE_CODE_SESSION_ID": "s"}, claude_pid=None)
        self.assertEqual((data["relaunch"], data["pane"]), ("manual", None))

    def test_out_refuses_in_tmux_without_finding_claude(self):
        with self.assertRaisesRegex(roll.RollError, "Claude process"):
            self.save(claude_pid=None)
        self.assertFalse(self.chat.marker.exists())

    def test_out_refuses_when_managed_roll_record_exists(self):
        (self.chat.local / "run.json").write_text('{"status": "review"}')
        with self.assertRaisesRegex(roll.RollError, "managed Roll"):
            self.save()

    def test_out_refuses_second_marker(self):
        self.save()
        with self.assertRaisesRegex(roll.RollError, "already exists"):
            self.save()

    def test_out_refuses_while_owner_lock_held(self):
        fd = os.open(self.chat.local / "owner.lock", os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(self.chat.transport.Busy):
                self.save()
        finally:
            os.close(fd)

    # loop guard -----------------------------------------------------------------------------------
    def roll_once(self, now):
        self.save(now=now)
        self.chat.set_marker(relaunch="exited")
        return self.chat.claim("new", MODEL, now=now + 10, alive=lambda p: False, sleep=lambda s: None)

    def progress(self, n):
        (self.root / self.record).write_text(f"step {n}\n")

    def test_no_progress_since_last_roll_refuses(self):
        self.roll_once(T0)
        with self.assertRaisesRegex(roll.RollError, "No progress"):
            self.save(now=T0 + 60)

    def test_three_rolls_in_a_row_then_stop(self):
        for n in range(3):
            self.progress(n)
            self.assertEqual(self.roll_once(T0 + n * 100)["chain"], n + 1)
        self.progress(9)
        with self.assertRaisesRegex(roll.RollError, "3 rolls in a row"):
            self.save(now=T0 + 400)

    def test_chain_resets_after_a_quiet_window(self):
        self.roll_once(T0)
        self.progress(1)
        self.assertEqual(self.save(now=T0 + 10 + tmux_roll.CHAIN_WINDOW + 1)["chain"], 1)

    # relaunch -------------------------------------------------------------------------------------
    def test_relaunch_restarts_only_recorded_pane_with_same_model_and_no_typing(self):
        self.save()
        tmux = FakeTmux()
        self.assertEqual(self.relaunch(tmux), "exited")
        verbs = [c[3] for c in tmux.calls]
        self.assertEqual(verbs, ["display", "respawn-pane"])
        self.assertNotIn("send-keys", [w for c in tmux.calls for w in c])
        respawn = tmux.calls[1]
        self.assertEqual(respawn[:4], ["tmux", "-S", "/tmp/tmux-501/default", "respawn-pane"])
        self.assertEqual(respawn[respawn.index("-t") + 1], "%4")
        self.assertIn("claude --model 'claude-opus-5-5[1m]' -- '/kerd:switch roll in'", respawn[-1])
        self.assertEqual(json.loads(self.chat.marker.read_text())["relaunch"], "exited")

    def test_relaunch_refuses_missing_pane(self):
        self.save()
        tmux = FakeTmux(pane=None)
        self.assertEqual(self.relaunch(tmux), "refused")
        self.assertEqual(len(tmux.calls), 1)

    def test_relaunch_refuses_pane_not_running_recorded_claude(self):
        self.save()
        tmux = FakeTmux(pane_pid=999)
        self.assertEqual(self.relaunch(tmux), "refused")
        self.assertNotIn("respawn-pane", [w for c in tmux.calls for w in c])
        self.assertIn("no longer runs", json.loads(self.chat.marker.read_text())["relaunch"])

    def test_relaunch_does_nothing_after_cancel(self):
        self.save()
        self.chat.cancel(now=T0 + 1)
        tmux = FakeTmux()
        self.assertEqual(self.relaunch(tmux), "withdrawn")
        self.assertEqual(tmux.calls, [])
        self.assertTrue(list(self.chat.local.glob("chat-roll-cancelled-*.json")))

    def test_relaunch_reports_old_pid_still_alive(self):
        self.save()
        self.assertEqual(self.relaunch(FakeTmux(), alive=lambda p: True), "pid-alive")

    def test_start_relaunch_hands_job_to_tmux_without_shell_variables(self):
        data = self.save()
        tmux = FakeTmux()
        tmux_roll.start_relaunch(self.root, data, run=tmux)
        argv = tmux.calls[0]
        self.assertEqual(argv[:5], ["tmux", "-S", "/tmp/tmux-501/default", "run-shell", "-b"])
        self.assertNotIn("$", argv[-1])

    # in -------------------------------------------------------------------------------------------
    def claim(self, model=MODEL, now=T0 + 10, alive=lambda p: False):
        return self.chat.claim("new-sid", model, now=now, alive=alive, sleep=lambda s: None, wait=0)

    def test_claim_after_exit_succeeds_once(self):
        self.save()
        self.chat.set_marker(relaunch="exited")
        data = self.claim()
        self.assertEqual((data["next_action"], data["claimed_by"]), ("build step 2", "new-sid"))
        self.assertFalse(self.chat.marker.exists())
        self.assertTrue((self.chat.local / "chat-roll-claimed-new-sid.json").exists())
        with self.assertRaisesRegex(roll.RollError, "missing or already claimed"):
            self.claim()

    def refused(self, reason, **kw):
        with self.assertRaisesRegex(roll.RollError, reason):
            self.claim(**kw)
        self.assertFalse(self.chat.marker.exists())
        self.assertTrue(list(self.chat.local.glob("chat-roll-refused-*.json")))

    def test_claim_refuses_unconfirmed_exit(self):
        self.save()
        self.refused("did not confirm")

    def test_claim_refuses_stale_marker(self):
        self.save()
        self.chat.set_marker(relaunch="exited")
        self.refused("older than 30 minutes", now=T0 + tmux_roll.MAX_AGE + 1)

    def test_claim_refuses_moved_head(self):
        self.save()
        self.chat.set_marker(relaunch="exited")
        subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "moved"], cwd=self.root, check=True)
        self.refused("commit changed")

    def test_claim_refuses_edited_sketchbook(self):
        self.save()
        self.chat.set_marker(relaunch="exited")
        (self.root / self.record).write_text("edited\n")
        self.refused("sketchbook changed")

    def test_claim_refuses_other_model(self):
        self.save()
        self.chat.set_marker(relaunch="exited")
        self.refused("runs claude-sonnet-5", model="claude-sonnet-5")

    def test_manual_claim_refuses_while_old_session_alive(self):
        self.save(env={"CLAUDE_CODE_SESSION_ID": "s"}, claude_pid=4242)
        self.refused("still running", alive=lambda p: True)

    def test_manual_claim_succeeds_once_old_session_gone(self):
        self.save(env={"CLAUDE_CODE_SESSION_ID": "s"}, claude_pid=4242)
        self.assertEqual(self.claim(alive=lambda p: False)["state"], "claimed")

    # helpers --------------------------------------------------------------------------------------
    def test_find_claude_walks_up_to_the_cli(self):
        commands = {300: "/bin/zsh -c python3 tmux_roll.py out", 200: "zsh", 150: "claude --model x", 1: "launchd"}
        parents = {300: 200, 200: 150, 150: 1}
        self.assertEqual(tmux_roll.find_claude(300, parents.get, commands.get), 150)
        self.assertIsNone(tmux_roll.find_claude(300, {300: 200, 200: 1}.get, commands.get))


if __name__ == "__main__":
    unittest.main()
