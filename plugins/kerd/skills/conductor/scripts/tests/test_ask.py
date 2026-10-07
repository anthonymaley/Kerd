import importlib.util
import json
import os
import signal
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ask", ROOT / "ask.py")
ask = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ask)


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        commands = {p: [sys.executable, str(ROOT / "tests/fake_cli.py"), p] for p in ("codex", "claude")}
        self.bridge = ask.Bridge(self.project, commands)

    def run_job(self, provider="codex", prompt="Review this", **kwargs):
        return self.bridge.run(provider, prompt, kwargs.pop("role", "reviewer"),
                               kwargs.pop("session", provider), **kwargs)

    def test_project_subdirectory_resolves_without_copying_runner(self):
        nested = self.project / "docs" / "work"
        nested.mkdir(parents=True)
        bridge = ask.Bridge(nested, self.bridge.commands)
        result = bridge.run("codex", "Review", "reviewer", "nested")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(bridge.root, self.project)
        self.assertEqual(bridge.state, self.bridge.state)
        self.assertFalse((self.project / "tools").exists())
        self.assertFalse((self.project / "scripts").exists())

    def test_separate_git_directory_file_is_supported(self):
        project = self.project / "separate-project"
        metadata = self.project / "separate-metadata"
        subprocess.run(["git", "init", "-q", "--separate-git-dir", str(metadata),
                        str(project)], check=True)
        self.assertTrue((project / ".git").is_file())
        bridge = ask.Bridge(project, self.bridge.commands)
        result = bridge.run("claude", "Review", "reviewer", "separate")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(bridge.state, metadata / "cross-llm")
        self.assertEqual(subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=project, text=True), "")

    def test_packaged_cli_uses_explicit_project_from_foreign_cwd(self):
        result = self.run_job(request_id="portable")
        output = subprocess.run(
            [sys.executable, str(ROOT / "ask.py"), "--project", str(self.project),
             "status", "portable"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(output.returncode, 0, output.stderr)
        returned = json.loads(output.stdout)
        self.assertEqual(returned["project"], str(self.project))
        self.assertEqual(returned["reply"], result["reply"])
        self.assertEqual(returned["request_id"], "portable")

    def test_both_providers_capture_and_reuse_session_and_new_role(self):
        for provider in ("codex", "claude"):
            with self.subTest(provider=provider):
                first = self.run_job(provider)
                second = self.run_job(provider, role="different role")
                self.assertEqual(first["status"], "completed")
                self.assertEqual(first["session_id"], second["session_id"])
                self.assertIn("different role", second["reply"])
                self.assertNotEqual(first["request_id"], second["request_id"])

    def test_duplicate_request_returns_same_result_not_new_work(self):
        first = self.run_job(request_id="same")
        self.assertEqual(first, self.run_job(request_id="same"))
        with self.assertRaises(ValueError):
            self.run_job(prompt="different", request_id="same")

    def test_failure_and_incomplete_protocol_never_report_success(self):
        for provider in ("codex", "claude"):
            for prompt in ("FAIL", "BROKEN"):
                self.assertEqual(self.run_job(provider, prompt)["status"], "failed")

    def test_resume_cannot_silently_rebind(self):
        first = self.run_job()
        result = self.run_job(prompt="MISMATCH")
        self.assertEqual(result["status"], "failed")
        self.assertEqual(self.bridge.sessions()[0]["session_id"], first["session_id"])

    def test_provider_conflict_closed_session_and_traversal(self):
        self.run_job(session="shared")
        with self.assertRaises(ValueError):
            self.run_job("claude", session="shared")
        self.bridge.close("shared")
        with self.assertRaises(ValueError):
            self.run_job(session="shared")
        with self.assertRaises(ValueError):
            self.run_job(session="../../escape")
        with self.assertRaises(ValueError):
            self.run_job(request_id="../escape")

    def test_timeout_optional_and_local_logs_private(self):
        result = self.run_job(prompt="SLEEP", timeout=0.1)
        self.assertEqual(result["status"], "timed_out", result)
        request = self.bridge.request_path(result["request_id"])
        self.assertEqual((request / "events.jsonl").stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.run_job()["status"], "completed")

    def test_cancel_and_session_busy_but_other_session_can_run(self):
        output = []
        thread = threading.Thread(target=lambda: output.append(self.run_job(prompt="SLEEP", request_id="waiting")))
        thread.start()
        self.addCleanup(thread.join)
        deadline = time.monotonic() + 5
        while not (self.bridge.request_path("waiting") / "result.json").exists():
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.01)
        with self.assertRaises(ask.Busy):
            self.run_job()
        self.assertEqual(self.run_job(session="other")["status"], "completed")
        self.assertEqual(self.bridge.cancel("waiting")["status"], "cancellation_requested")
        thread.join(5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(output[0]["status"], "cancelled")
        self.assertEqual(self.bridge.wait("waiting"), output[0])

    def test_prompt_is_literal_stdin_not_shell(self):
        text = "$(touch should-not-exist); 'quoted'\nsecond line"
        result = self.run_job(prompt=text)
        self.assertIn(text, result["reply"])
        self.assertFalse((self.project / "should-not-exist").exists())

    def test_missing_executable_is_attributed_failure(self):
        self.bridge.commands["codex"] = ["/this-command-does-not-exist"]
        result = self.run_job()
        self.assertEqual(result["status"], "failed")
        self.assertEqual(self.bridge.status(result["request_id"])["status"], "failed")

    def test_state_is_inside_git_metadata_not_project_documents(self):
        self.run_job()
        status = subprocess.check_output(["git", "status", "--porcelain"], cwd=self.project, text=True)
        self.assertEqual(status, "")
        self.assertTrue(str(self.bridge.state).startswith(str(self.project / ".git")))

    def test_conflicting_ids_within_one_provider_response_do_not_bind(self):
        result = self.run_job("claude", "CONFLICT")
        self.assertEqual(result["status"], "failed")
        self.assertIn("Conflicting session IDs", result["provider_error"])
        self.assertEqual(self.bridge.sessions(), [])

    def test_abandoned_submission_recovers_without_rerunning(self):
        first = self.run_job(request_id="template")
        spec = ask.read(self.bridge.request_path(first["request_id"]) / "request.json")
        orphan = self.bridge.request_path("orphan")
        orphan.mkdir()
        ask.save(orphan / "request.json", spec)
        result = self.run_job(request_id="orphan")
        self.assertEqual(result["status"], "failed")
        self.assertEqual(self.bridge.status("orphan"), result)
        self.assertFalse((orphan / "events.jsonl").exists())
        self.assertEqual(self.run_job()["status"], "completed")

    def test_empty_reserved_request_reports_uncertainty_without_launch(self):
        self.bridge.request_path("empty").mkdir()
        result = self.run_job(request_id="empty")
        self.assertEqual(result["status"], "unknown")
        self.assertEqual(result, self.bridge.status("empty"))
        self.assertEqual(self.bridge.sessions(), [])

    def test_timeout_kills_descendant_after_leader_exits(self):
        started = time.monotonic()
        result = self.run_job(prompt="DESCENDANT", timeout=0.5)
        self.assertEqual(result["status"], "timed_out")
        self.assertLess(time.monotonic() - started, 7)
        output = (self.bridge.request_path(result["request_id"]) / "events.jsonl").read_text()
        self.assertIn("child-ready", output)
        self.assertEqual(self.run_job()["status"], "completed")

    def test_explicit_cancel_kills_ready_descendant_group(self):
        output = []
        thread = threading.Thread(target=lambda: output.append(self.run_job(prompt="DESCENDANT", request_id="descendant")))
        thread.start()
        self.addCleanup(thread.join, 5)
        ready = self.project / "fixture-child.json"
        deadline = time.monotonic() + 5
        while not ready.exists():
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.01)
        group = json.loads(ready.read_text())["group"]
        def cleanup_group():
            try:
                os.killpg(group, signal.SIGKILL)
            except ProcessLookupError:
                pass
        self.addCleanup(cleanup_group)
        self.bridge.cancel("descendant")
        thread.join(7)
        self.assertFalse(thread.is_alive())
        self.assertEqual(output[0]["status"], "cancelled")
        deadline = time.monotonic() + 2
        while True:
            try:
                os.killpg(group, 0)
            except ProcessLookupError:
                break
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.02)

    def test_background_returns_and_retains_session_lock_and_result(self):
        started = time.monotonic()
        accepted = self.run_job(prompt="SLEEP", request_id="background", background=True)
        worker = accepted["owner_pid"]
        self.addCleanup(os.waitpid, worker, 0)
        self.assertEqual(accepted["status"], "starting")
        self.assertLess(time.monotonic() - started, 1)
        with self.assertRaises(ask.Busy):
            self.run_job()
        deadline = time.monotonic() + 7
        while True:
            result = self.bridge.status("background")
            if result["status"] not in ("starting", "running"):
                break
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.05)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(self.run_job()["session_id"], result["session_id"])

    def test_wait_timeout_leaves_background_work_running_and_result_retrievable(self):
        for provider in ("codex", "claude"):
            with self.subTest(provider=provider):
                request_id = "wait-" + provider
                accepted = self.run_job(provider, "SLEEP", request_id=request_id, background=True)
                self.addCleanup(os.waitpid, accepted["owner_pid"], 0)
                progress = self.bridge.wait(request_id, timeout=0.05)
                self.assertIn(progress["status"], ("starting", "running"))
                self.assertFalse((self.bridge.request_path(request_id) / "cancel.json").exists())
                with self.assertRaises(ask.Busy):
                    self.run_job(provider)
                result = self.bridge.wait(request_id, timeout=7)
                self.assertEqual(result["status"], "completed")
                self.assertEqual(result["request_id"], request_id)
                self.assertEqual(result["target"], provider)
                self.assertEqual(result, self.bridge.status(request_id))
                self.assertEqual(result, self.bridge.wait(request_id, timeout=0))

    def test_wait_returns_failure_and_uncertainty_without_retry(self):
        failed = self.run_job(prompt="FAIL", request_id="failed")
        self.assertEqual(self.bridge.wait("failed"), failed)
        self.bridge.request_path("uncertain").mkdir()
        self.assertEqual(self.bridge.wait("uncertain")["status"], "unknown")
        self.assertFalse((self.bridge.request_path("uncertain") / "events.jsonl").exists())
        with self.assertRaisesRegex(ValueError, "Unknown request"):
            self.bridge.wait("absent")

    def test_wait_validates_timeout_and_cli_returns_retained_result(self):
        result = self.run_job(request_id="retained")
        for timeout in (-1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                self.bridge.wait("retained", timeout)
        completed = subprocess.run(
            [sys.executable, str(ROOT / "ask.py"), "--project", str(self.project),
             "wait", "retained", "--timeout", "0"],
            capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(completed.stdout), result)

    def test_abandoned_background_start_returns_failure_without_launch(self):
        first = self.run_job(request_id="template")
        request = self.bridge.request_path("abandoned-start")
        request.mkdir()
        ask.save(request / "request.json", ask.read(self.bridge.request_path("template") / "request.json"))
        ask.save(request / "result.json", {**first, "request_id": "abandoned-start",
                                          "status": "starting", "owner_pid": os.getpid()})
        result = self.bridge.wait("abandoned-start", timeout=0)
        self.assertEqual(result["status"], "failed")
        self.assertIn("before provider launch", result["error"])
        self.assertFalse((request / "events.jsonl").exists())
        self.assertEqual(self.run_job()["status"], "completed")

    def start_signal_fixture(self, request_id):
        ready = self.project / "fixture-child.json"
        if ready.exists():
            ready.unlink()
        script = (
            f"import sys; sys.path.insert(0, {str(ROOT)!r}); from ask import Bridge; "
            f"Bridge({str(self.project)!r}, {{'codex': [{sys.executable!r}, "
            f"{str(ROOT / 'tests/fake_cli.py')!r}, 'codex']}}).run("
            f"'codex', 'DESCENDANT', 'tester', 'codex', request_id={request_id!r})"
        )
        runner = subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, text=True)
        def cleanup_runner():
            if runner.poll() is None:
                runner.kill()
            runner.communicate(timeout=5)
        self.addCleanup(cleanup_runner)
        deadline = time.monotonic() + 5
        while not ready.exists():
            self.assertIsNone(runner.poll())
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.01)
        group = json.loads(ready.read_text())["group"]
        def cleanup_group():
            try:
                os.killpg(group, signal.SIGKILL)
            except ProcessLookupError:
                pass
        self.addCleanup(cleanup_group)
        return runner, group

    def test_normal_termination_cleans_provider_group_and_allows_reuse(self):
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            with self.subTest(signal=sig):
                request_id = "signal-" + str(sig)
                runner, group = self.start_signal_fixture(request_id)
                runner.send_signal(sig)
                time.sleep(0.1)  # cleanup is waiting for the resistant descendant
                runner.send_signal(signal.SIGTERM)
                runner.send_signal(signal.SIGINT)
                runner.communicate(timeout=8)
                self.assertEqual(self.bridge.status(request_id)["status"], "cancelled")
                deadline = time.monotonic() + 2
                while True:
                    try:
                        os.killpg(group, 0)
                    except ProcessLookupError:
                        break
                    self.assertLess(time.monotonic(), deadline)
                    time.sleep(0.02)
                self.assertEqual(self.run_job()["status"], "completed")

    def test_uncatchable_runner_death_blocks_session_reuse_and_close(self):
        self.run_job()  # bind a native session before the interrupted request
        runner, group = self.start_signal_fixture("killed-runner")
        runner.kill()
        runner.communicate(timeout=5)
        os.killpg(group, 0)  # deliberately still alive; cleanup owns this fixture
        self.assertEqual(self.bridge.status("killed-runner")["status"], "interrupted")
        self.assertEqual(self.bridge.cancel("killed-runner")["status"], "interrupted")
        with self.assertRaisesRegex(ask.Busy, "unresolved outcome"):
            self.run_job()
        with self.assertRaises(ask.Busy):
            self.bridge.close("codex")
        with self.assertRaisesRegex(ask.Busy, "group is still present"):
            self.bridge.resolve("killed-runner")
        self.assertEqual(self.run_job(session="other")["status"], "completed")
        os.killpg(group, signal.SIGKILL)  # only this test's deliberately orphaned fixture
        deadline = time.monotonic() + 3
        while True:
            try:
                os.killpg(group, 0)
            except ProcessLookupError:
                break
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.02)
        resolved = self.bridge.resolve("killed-runner")
        self.assertEqual(resolved["status"], "abandoned")
        self.assertIn("outcome not proven", resolved["error"])
        self.assertEqual(self.run_job()["status"], "completed")

    def test_signal_handlers_are_restored_and_run_timeout_is_finite(self):
        previous = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)}
        self.run_job()
        self.assertEqual(previous, {sig: signal.getsignal(sig) for sig in previous})
        for timeout in (float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                self.run_job(timeout=timeout)

    def test_resolve_refuses_unrecorded_provider_and_completed_work(self):
        first = self.run_job(request_id="complete")
        with self.assertRaises(ValueError):
            self.bridge.resolve("complete")
        path = self.bridge.request_path("unrecorded")
        path.mkdir()
        ask.save(path / "request.json", ask.read(self.bridge.request_path("complete") / "request.json"))
        ask.save(path / "result.json", {"request_id": "unrecorded", "status": "running", "session": "codex"})
        with self.assertRaisesRegex(ValueError, "group was not recorded"):
            self.bridge.resolve("unrecorded")
        self.assertEqual(ask.read(path / "result.json")["status"], "running")

    def test_interrupt_during_startup_is_saved_without_launch(self):
        with mock.patch.object(self.bridge, "command", side_effect=KeyboardInterrupt):
            result = self.run_job(request_id="startup-interrupt")
        self.assertEqual(result["status"], "cancelled")
        self.assertNotIn("process_id", result)
        self.assertEqual(self.run_job()["status"], "completed")

    def test_resolve_permission_denial_is_conservative_busy(self):
        result = self.run_job(request_id="permission")
        result["status"] = "running"
        ask.save(self.bridge.request_path("permission") / "result.json", result)
        with mock.patch.object(ask.os, "killpg", side_effect=PermissionError):
            with self.assertRaisesRegex(ask.Busy, "cannot be inspected"):
                self.bridge.resolve("permission")
        self.assertEqual(ask.read(self.bridge.request_path("permission") / "result.json")["status"], "running")

    def test_interruption_inside_process_creation_preserves_uncertainty(self):
        with mock.patch.object(ask.subprocess, "Popen", side_effect=KeyboardInterrupt):
            result = self.run_job(request_id="launch-interrupt")
        self.assertEqual(result["status"], "interrupted")
        with self.assertRaises(ask.Busy):
            self.run_job()
        with self.assertRaises(ValueError):
            self.bridge.resolve("launch-interrupt")

    def test_detached_output_pipe_does_not_hang_cleanup(self):
        output = []
        thread = threading.Thread(target=lambda: output.append(self.run_job(prompt="DETACHED", request_id="detached")))
        thread.start()
        self.addCleanup(thread.join, 5)
        ready = self.project / "fixture-detached.json"
        deadline = time.monotonic() + 5
        while not ready.exists():
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.01)
        group = json.loads(ready.read_text())["group"]
        def cleanup_detached_fixture():
            try:
                os.killpg(group, signal.SIGKILL)
            except ProcessLookupError:
                pass
        self.addCleanup(cleanup_detached_fixture)
        self.bridge.cancel("detached")
        thread.join(5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(output[0]["status"], "cancelled")
        self.assertIn("detached descendants", output[0]["cleanup_warning"])

    def test_cleanup_permission_failure_is_saved_and_blocks_reuse(self):
        created = []
        real_popen = ask.subprocess.Popen
        def capture(*args, **kwargs):
            proc = real_popen(*args, **kwargs)
            created.append(proc)
            return proc
        try:
            with mock.patch.object(ask.subprocess, "Popen", side_effect=capture), mock.patch.object(self.bridge, "stop", side_effect=PermissionError("fixture denial")):
                result = self.run_job(prompt="SLEEP", timeout=0.01)
            self.assertEqual(result["status"], "interrupted")
            self.assertEqual(self.bridge.status(result["request_id"])["status"], "interrupted")
            self.assertIn("fixture denial", result["cleanup_error"])
            with self.assertRaises(ask.Busy):
                self.run_job()
        finally:
            for proc in created:
                if proc.poll() is None:
                    os.killpg(proc.pid, signal.SIGKILL)
                proc.wait(timeout=5)

    def test_stop_rechecks_denied_probe_until_group_confirmed_gone(self):
        proc = mock.Mock(pid=99999999)
        with mock.patch.object(ask.os, "killpg", side_effect=[
            None, PermissionError("transient probe denial"), ProcessLookupError(),
        ]) as killpg, mock.patch.object(ask.time, "sleep"), mock.patch.object(
            ask.time, "monotonic", side_effect=[0, 0, 1]
        ):
            self.bridge.stop(proc)
        self.assertEqual(killpg.call_args_list, [
            mock.call(proc.pid, signal.SIGTERM), mock.call(proc.pid, 0), mock.call(proc.pid, 0),
        ])
        proc.wait.assert_called_once()

    def test_stop_keeps_denial_uncertain_without_confirmed_disappearance(self):
        for later_probe in (PermissionError("still denied"), None):
            with self.subTest(later_probe=later_probe):
                proc = mock.Mock(pid=99999999)
                proc.communicate.return_value = ("", "")
                record = {"status": "timed_out"}
                with mock.patch.object(ask.os, "killpg", side_effect=[
                    None, PermissionError("probe denied"), later_probe,
                ]) as killpg, mock.patch.object(ask.time, "sleep"), mock.patch.object(
                    ask.time, "monotonic", side_effect=[0, 0, 1, 4]
                ):
                    self.bridge.stop_and_collect(proc, record)
                self.assertEqual(record["status"], "interrupted")
                self.assertIn("denied", record["cleanup_error"])
                self.assertEqual(killpg.call_args_list, [
                    mock.call(proc.pid, signal.SIGTERM), mock.call(proc.pid, 0), mock.call(proc.pid, 0),
                ])
                proc.wait.assert_not_called()

    def test_stop_does_not_retry_a_denied_termination_signal(self):
        proc = mock.Mock(pid=99999999)
        with mock.patch.object(ask.os, "killpg", side_effect=PermissionError("TERM denied")) as killpg:
            with self.assertRaises(PermissionError):
                self.bridge.stop(proc)
        killpg.assert_called_once_with(proc.pid, signal.SIGTERM)
        proc.wait.assert_not_called()

    def test_interrupted_background_parent_does_not_finalize_child_result(self):
        real_fork = ask.os.fork
        children = []
        def interrupted_fork():
            child = real_fork()
            if child:
                children.append(child)
                raise KeyboardInterrupt  # parent interrupted before the PID assignment
            return child
        with mock.patch.object(ask.os, "fork", side_effect=interrupted_fork):
            with self.assertRaises(KeyboardInterrupt):
                self.run_job(prompt="SLEEP", request_id="parent-interrupted", background=True)
        self.addCleanup(os.waitpid, children[0], 0)
        result = self.bridge.wait("parent-interrupted", timeout=7)
        self.assertEqual(result["status"], "completed")
        self.assertTrue((self.bridge.request_path("parent-interrupted") / "events.jsonl").exists())

    def test_session_mismatch_cannot_erase_cleanup_uncertainty(self):
        first = self.run_job()
        proc = mock.Mock(pid=99999999, returncode=None)
        proc.communicate.side_effect = [
            subprocess.TimeoutExpired("fixture", 0.2),
            (json.dumps({"type": "thread.started", "thread_id": "different-session"}), ""),
        ]
        with mock.patch.object(ask.subprocess, "Popen", return_value=proc), mock.patch.object(self.bridge, "stop", side_effect=PermissionError("fixture denial")):
            result = self.run_job(request_id="mismatch-and-cleanup", timeout=1e-9)
        self.assertEqual(result["status"], "interrupted")
        self.assertIn("fixture denial", result["cleanup_error"])
        self.assertEqual(self.bridge.sessions()[0]["session_id"], first["session_id"])
        with self.assertRaises(ask.Busy):
            self.run_job()


if __name__ == "__main__":
    unittest.main()
