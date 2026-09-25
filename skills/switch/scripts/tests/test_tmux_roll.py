"""tmux_roll.py: the chat roll saves under the owner lock, restarts only the recorded pane,
never types into Claude, and picks up only when every check holds."""
import fcntl
import json
import shlex
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
CLAUDE = {"pid": 500, "start": "Thu Sep 24 21:00:00 2026"}


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

    def save(self, env=ENV, now=T0, claude=CLAUDE, command="claude --model x", tmux_env=None, **kw):
        return self.chat.out(self.record, "build step 2", "Build on concert/x; no push", MODEL, 500_000,
                             claude, command, env=env, now=now,
                             tmux_env={} if tmux_env is None else tmux_env, **kw)

    def exited(self):
        self.chat.update(json.loads(self.chat.marker.read_text())["roll_id"], relaunch="exited")

    def relaunch(self, tmux, alive=True, gone_after=True, roll_id=None, now=T0 + 5):
        """alive: the recorded Claude runs at the check; gone_after: it is gone once the pane restarts."""
        state = {"restarted": False}
        def present(pid):
            return not ((state["restarted"] and gone_after) or not alive)
        def start(pid):
            return CLAUDE["start"]
        def run(argv, **kw):
            if "respawn-pane" in argv:
                state["restarted"] = True
            return tmux(argv, **kw)
        roll_id = roll_id or json.loads(self.chat.marker.read_text())["roll_id"]
        return self.chat.relaunch(roll_id, delay=0, run=run, start=start, parent=self.parent,
                                  sleep=lambda s: None, shell="/bin/zsh", now=now, present=present)

    # out ------------------------------------------------------------------------------------------
    def test_out_writes_marker_with_verbatim_approval(self):
        data = self.save()
        on_disk = json.loads(self.chat.marker.read_text())
        self.assertEqual(on_disk, data)
        self.assertEqual(data["approval_boundary"], "Build on concert/x; no push")
        self.assertEqual((data["pane"], data["tmux_socket"], data["relaunch"]), ("%4", "/tmp/tmux-501/default", "pending"))

    def test_out_outside_tmux_is_manual_and_needs_no_pane(self):
        data = self.save(env={"CLAUDE_CODE_SESSION_ID": "s"})
        self.assertEqual((data["relaunch"], data["pane"]), ("manual", None))

    def test_out_refuses_without_identifying_claude_in_or_out_of_tmux(self):
        for env in (ENV, {"CLAUDE_CODE_SESSION_ID": "s"}):
            with self.subTest(tmux="TMUX" in env):
                with self.assertRaisesRegex(roll.RollError, "Claude process"):
                    self.save(env=env, claude=None)
        self.assertFalse(self.chat.marker.exists())

    def test_out_refuses_without_session_id(self):
        with self.assertRaisesRegex(roll.RollError, "session's ID"):
            self.save(env={"TMUX": ENV["TMUX"], "TMUX_PANE": "%4"})

    def test_out_refuses_session_started_with_other_launch_options(self):
        for command in ("claude --permission-mode plan", "/usr/local/bin/claude --model x --add-dir /y",
                        "node /opt/claude --allowedTools=Read"):
            with self.subTest(command=command):
                with self.assertRaisesRegex(roll.RollError, "restart would drop"):
                    self.save(command=command)
        self.assertFalse(self.chat.marker.exists())

    def test_launch_restriction_allows_model_and_a_prompt(self):
        for command in ("claude", "claude --model claude-opus-5-5[1m]", "claude --model=x",
                        "claude --model x -- /kerd:switch roll in", "claude fix the typo"):
            with self.subTest(command=command):
                self.assertIsNone(tmux_roll.launch_restriction(command))

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
        self.exited()
        return self.chat.claim("new", MODEL, now=now + 10, start=lambda p: None, present=lambda p: False,
                               sleep=lambda s: None)

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
        with self.assertRaisesRegex(roll.RollError, "3 rolls in a row already"):
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
        roll_id = self.save()["roll_id"]
        self.chat.cancel(now=T0 + 1)
        tmux = FakeTmux()
        self.assertEqual(self.relaunch(tmux, roll_id=roll_id), "withdrawn")
        self.assertEqual(tmux.calls, [])
        self.assertTrue(list(self.chat.local.glob("chat-roll-cancelled-*.json")))

    def test_relaunch_reports_old_pid_still_alive(self):
        self.save()
        self.assertEqual(self.relaunch(FakeTmux(), gone_after=False), "pid-alive")

    def test_relaunch_refuses_when_recorded_claude_already_gone_or_pid_reused(self):
        self.save()
        tmux = FakeTmux()
        self.assertEqual(self.relaunch(tmux, alive=False), "refused")
        self.assertEqual(tmux.calls, [])

    def test_relaunch_rechecks_checkpoint_before_restarting(self):
        self.save()
        (self.root / self.record).write_text("edited after the save\n")
        tmux = FakeTmux()
        self.assertEqual(self.relaunch(tmux), "refused")
        self.assertEqual(tmux.calls, [])
        self.assertIn("sketchbook changed", json.loads(self.chat.marker.read_text())["relaunch"])

    def test_relaunch_ignores_another_rolls_id(self):
        self.save()
        tmux = FakeTmux()
        self.assertEqual(self.relaunch(tmux, roll_id="not-this-roll"), "withdrawn")
        self.assertEqual(tmux.calls, [])

    def test_cancel_after_restart_began_is_too_late(self):
        self.save()
        roll_id = json.loads(self.chat.marker.read_text())["roll_id"]
        seen = {}
        def tmux(argv, **kw):
            if "respawn-pane" in argv:
                with self.assertRaisesRegex(roll.RollError, "Too late"):
                    self.chat.cancel(now=T0 + 6)
                seen["tried"] = True
            return FakeTmux()(argv, **kw)
        self.assertEqual(self.relaunch(tmux, roll_id=roll_id), "exited")
        self.assertTrue(seen["tried"])

    def test_old_relaunch_cannot_update_a_newer_roll(self):
        self.save()
        old = json.loads(self.chat.marker.read_text())["roll_id"]
        self.chat.cancel(now=T0 + 1)
        self.progress(2)
        self.save(now=T0 + 2)
        self.assertIsNone(self.chat.update(old, relaunch="exited"))
        self.assertEqual(json.loads(self.chat.marker.read_text())["relaunch"], "pending")

    def test_start_relaunch_hands_job_to_tmux_without_shell_variables(self):
        data = self.save()
        tmux = FakeTmux()
        tmux_roll.start_relaunch(self.root, data, run=tmux)
        argv = tmux.calls[0]
        self.assertEqual(argv[:5], ["tmux", "-S", "/tmp/tmux-501/default", "run-shell", "-b"])
        self.assertNotIn("$", argv[-1])

    def test_relaunch_command_parses_with_the_real_parser(self):
        words = shlex.split(tmux_roll.relaunch_command(self.root, "abc123"))
        args = tmux_roll.build_parser().parse_args(words[2:])
        self.assertEqual((args.command, args.project, args.roll_id), ("relaunch", str(self.root), "abc123"))

    # in -------------------------------------------------------------------------------------------
    def claim(self, model=MODEL, now=T0 + 10, alive=False, session="new-sid", present=None, start=None):
        present = present or (lambda p: alive)
        start = start or (lambda p: CLAUDE["start"])
        return self.chat.claim(session, model, now=now, start=start, present=present,
                               sleep=lambda s: None, wait=0)

    def test_claim_after_exit_succeeds_once(self):
        self.save()
        self.exited()
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
        self.chat.update(json.loads(self.chat.marker.read_text())["roll_id"], relaunch="pid-alive")
        self.refused("did not confirm")

    def test_claim_refuses_stale_marker(self):
        self.save()
        self.exited()
        self.refused("older than 30 minutes", now=T0 + tmux_roll.MAX_AGE + 1)

    def test_claim_refuses_moved_head(self):
        self.save()
        self.exited()
        subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "moved"], cwd=self.root, check=True)
        self.refused("commit changed")

    def test_claim_refuses_edited_sketchbook(self):
        self.save()
        self.exited()
        (self.root / self.record).write_text("edited\n")
        self.refused("sketchbook changed")

    def test_claim_refuses_other_model(self):
        self.save()
        self.exited()
        self.refused("runs claude-sonnet-5", model="claude-sonnet-5")

    def test_manual_claim_refuses_while_old_session_alive(self):
        self.save(env={"CLAUDE_CODE_SESSION_ID": "s"})
        self.refused("still running", alive=True)

    def test_unreadable_process_is_unknown_not_gone(self):
        self.save(env={"CLAUDE_CODE_SESSION_ID": "s"})
        self.refused("cannot be shown to be closed", present=lambda p: True, start=lambda p: None)

    def test_process_state_is_three_valued(self):
        self.assertEqual(tmux_roll.process_state(CLAUDE, lambda p: CLAUDE["start"], lambda p: True), "alive")
        self.assertEqual(tmux_roll.process_state(CLAUDE, lambda p: "Fri Sep 25 01:00:00 2026", lambda p: True), "gone")
        self.assertEqual(tmux_roll.process_state(CLAUDE, lambda p: None, lambda p: False), "gone")
        self.assertEqual(tmux_roll.process_state(CLAUDE, lambda p: None, lambda p: True), "unknown")
        self.assertEqual(tmux_roll.process_state(CLAUDE, lambda p: None, lambda p: None), "unknown")
        self.assertEqual(tmux_roll.process_state(None), "unknown")

    def test_relaunch_reports_unknown_exit_as_unknown(self):
        self.save()
        roll_id = json.loads(self.chat.marker.read_text())["roll_id"]
        calls = {"n": 0}
        def start(pid):
            calls["n"] += 1
            return CLAUDE["start"] if calls["n"] == 1 else None
        result = self.chat.relaunch(roll_id, delay=0, run=FakeTmux(), start=start, parent=self.parent,
                                    sleep=lambda s: None, shell="/bin/zsh", now=T0 + 5, present=lambda p: True)
        self.assertEqual(result, "exit-unknown")
        self.refused("did not confirm")

    def test_claim_leaves_a_restart_in_progress_alone(self):
        self.save()
        for state in ("pending", "respawning"):
            with self.subTest(state=state):
                self.chat.update(json.loads(self.chat.marker.read_text())["roll_id"], relaunch=state)
                with self.assertRaisesRegex(roll.RollError, "still in progress"):
                    self.claim()
                self.assertTrue(self.chat.marker.exists())

    def test_prompt_dashes_cannot_hide_a_launch_option(self):
        self.assertEqual(tmux_roll.launch_restriction('claude Explain -- usage --permission-mode plan'),
                         "--permission-mode")
        self.assertIsNone(tmux_roll.launch_restriction("claude --model m --effort high -- /kerd:switch roll in"))

    def test_session_env_the_tmux_server_lacks_refuses(self):
        env = {**ENV, "CLAUDE_CONFIG_DIR": "/Users/x/.claude-work", "CLAUDE_EFFORT": "high", "CLAUDE_PID": "500"}
        with self.assertRaisesRegex(roll.RollError, "CLAUDE_CONFIG_DIR"):
            self.save(env=env)
        self.assertEqual(self.save(env=env, tmux_env={"CLAUDE_CONFIG_DIR": "/Users/x/.claude-work"})["effort"], "high")

    def test_unreadable_tmux_environment_refuses(self):
        with self.assertRaisesRegex(roll.RollError, "tmux server's environment"):
            self.chat.out(self.record, "n", "a", MODEL, 1, CLAUDE, "claude", env=ENV, now=T0, tmux_env=None)

    def test_relaunch_carries_effort(self):
        env = {**ENV, "CLAUDE_EFFORT": "high"}
        self.save(env=env)
        tmux = FakeTmux()
        self.relaunch(tmux)
        self.assertIn("--effort high --", [c for c in tmux.calls if "respawn-pane" in c][0][-1])

    def test_manual_claim_refuses_unidentified_predecessor(self):
        self.save(env={"CLAUDE_CODE_SESSION_ID": "s"})
        data = json.loads(self.chat.marker.read_text())
        data["claude"] = {"pid": 500, "start": ""}
        self.chat.marker.write_text(json.dumps(data))
        self.refused("cannot be shown to be closed")

    def test_claim_needs_this_sessions_id(self):
        self.save()
        self.exited()
        with self.assertRaisesRegex(roll.RollError, "session's ID"):
            self.claim(session=None)
        self.assertTrue(self.chat.marker.exists())

    def test_manual_claim_succeeds_once_old_session_gone(self):
        self.save(env={"CLAUDE_CODE_SESSION_ID": "s"})
        self.assertEqual(self.claim(alive=False)["state"], "claimed")

    # helpers --------------------------------------------------------------------------------------
    def test_find_claude_walks_up_to_the_cli(self):
        commands = {300: "/bin/zsh -c python3 tmux_roll.py out", 200: "zsh", 150: "claude --model x", 1: "launchd"}
        parents = {300: 200, 200: 150, 150: 1}
        self.assertEqual(tmux_roll.find_claude(300, parents.get, commands.get), 150)
        self.assertIsNone(tmux_roll.find_claude(300, {300: 200, 200: 1}.get, commands.get))


if __name__ == "__main__":
    unittest.main()
