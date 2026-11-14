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


def reap_child(pid, seconds=10):
    """Bounded replacement for a blocking os.waitpid(pid, 0) in cleanup: poll with
    WNOHANG until the deadline, then SIGTERM, then SIGKILL, reaping each time; if the
    child still cannot be reaped, fail loudly instead of hanging the suite."""
    def reaped(within):
        deadline = time.monotonic() + within
        while True:
            try:
                done, _ = os.waitpid(pid, os.WNOHANG)
            except ChildProcessError:  # already reaped elsewhere
                return True
            if done:
                return True
            if time.monotonic() >= deadline:
                return False
            time.sleep(0.02)
    if reaped(seconds):
        return
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.kill(pid, sig)
        except ProcessLookupError:
            pass
        if reaped(2):
            raise AssertionError(f"child {pid} outlived {seconds} s and was stopped with {sig.name}")
    raise AssertionError(f"child {pid} could not be reaped after SIGKILL")


class ReadinessGatedClock:
    """Stands in for ask's `time` module: `monotonic` holds still until the fixture
    child's readiness file holds complete JSON, then runs at real speed from there.
    The hold is capped (20 s real time) so a broken fixture fails instead of hanging."""

    def __init__(self, ready, cap=20.0):
        self.ready = ready
        self.start = time.monotonic()
        self.cap = cap
        self.ready_at = None

    def monotonic(self):
        now = time.monotonic()
        if self.ready_at is None:
            try:
                json.loads(self.ready.read_text())["group"]
                self.ready_at = now
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                if now - self.start < self.cap:
                    return self.start
                self.ready_at = self.start
        return self.start + (now - self.ready_at)

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)


class TestDeadline(AssertionError):
    pass


class TransportTests(unittest.TestCase):
    # One real-time deadline per test, set before anything can block and cleared after
    # every other cleanup (addCleanup runs last-registered first), so a hang in a test or
    # its cleanup fails with a clear message instead of stalling the suite. SIGALRM is
    # delivered to the main thread only, where unittest runs the test; job threads keep
    # their own bounds. Forked children do not inherit the pending alarm.
    TEST_DEADLINE = 90

    def arm_deadline(self, seconds):
        if threading.current_thread() is not threading.main_thread():
            return
        message = f"{self.id()} exceeded its {seconds} s real-time deadline"
        fired = []
        def expired(signum, frame):
            fired.append(True)
            raise TestDeadline(message)
        previous = signal.signal(signal.SIGALRM, expired)
        signal.setitimer(signal.ITIMER_REAL, seconds)
        def disarm():
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous)
            # ask.run turns an exception inside a job into a "failed" result after
            # stopping the provider group, so the raise above can be absorbed; the
            # deadline still fails the test here.
            if fired:
                raise TestDeadline(message)
        self.addCleanup(disarm)

    def setUp(self):
        self.arm_deadline(self.TEST_DEADLINE)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.project)], check=True, timeout=30)
        commands = {p: [sys.executable, str(ROOT / "tests/fake_cli.py"), p] for p in ("codex", "claude")}
        self.bridge = ask.Bridge(self.project, commands)

    def wait_for_group(self, ready, runner=None):
        # The fixture child's write_text is not atomic: wait for a complete file, not just its name.
        deadline = time.monotonic() + 5
        while True:
            try:
                return json.loads(ready.read_text())["group"]
            except (FileNotFoundError, json.JSONDecodeError):
                if runner is not None:
                    self.assertIsNone(runner.poll())
                self.assertLess(time.monotonic(), deadline)
                time.sleep(0.01)

    def wait_for_group_gone(self, group, seconds):
        # macOS can deny the existence probe while a killed group is reaped; as in
        # ask.stop(), denial is not disappearance: keep polling within the deadline.
        deadline = time.monotonic() + seconds
        while True:
            try:
                os.killpg(group, 0)
            except ProcessLookupError:
                return
            except PermissionError:
                pass
            self.assertLess(time.monotonic(), deadline, "process group still present")
            time.sleep(0.02)

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
                        str(project)], check=True, timeout=30)
        self.assertTrue((project / ".git").is_file())
        bridge = ask.Bridge(project, self.bridge.commands)
        result = bridge.run("claude", "Review", "reviewer", "separate")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(bridge.state, metadata / "cross-llm")
        self.assertEqual(subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=project, text=True, timeout=30), "")

    def test_packaged_cli_uses_explicit_project_from_foreign_cwd(self):
        result = self.run_job(request_id="portable")
        output = subprocess.run(
            [sys.executable, str(ROOT / "ask.py"), "--project", str(self.project),
             "status", "portable"], cwd=ROOT, capture_output=True, text=True, timeout=30)
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
        thread = self.start_job_thread(output, "waiting", prompt="SLEEP")
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
        status = subprocess.check_output(["git", "status", "--porcelain"], cwd=self.project, text=True, timeout=30)
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

    def start_job_thread(self, output, request_id, ready=None, **kwargs):
        """Start a synchronous job on a daemon thread, with its cleanup registered before
        the test waits on anything. The job carries its own timeout (20 s unless given),
        so it ends even if cancellation never reaches it. At cleanup the fixture child's
        group is killed; if the thread is still alive, the leader's group (its pid,
        recorded in result.json at launch) is killed too, the thread gets a 5 s join, and
        a thread that survives fails the test loudly rather than holding up exit."""
        kwargs.setdefault("timeout", 20)
        thread = threading.Thread(
            target=lambda: output.append(self.run_job(request_id=request_id, **kwargs)), daemon=True)

        def kill(group):
            try:
                os.killpg(group, signal.SIGKILL)
            except ProcessLookupError:
                pass
            except PermissionError:  # macOS denies while reaping; a live group still fails here
                self.wait_for_group_gone(group, 3)

        def cleanup():
            for group in (self.recorded_groups_from_ready(ready) if ready is not None else ()):
                kill(group)
            if thread.is_alive():
                for group in self.recorded_groups(request_id, ready):
                    kill(group)
                thread.join(5)
            if thread.is_alive():
                raise AssertionError(f"job thread {request_id!r} survived cleanup")

        self.addCleanup(cleanup)
        thread.start()
        return thread

    def run_bounded(self, seconds, groups, **kwargs):
        """Run a synchronous job on a daemon thread under a real-time deadline.

        `groups` returns the process groups the job may have started; on a missed
        deadline or an exception every one of them is SIGKILLed, then the thread is
        joined, and the test fails instead of blocking the suite."""
        returned, failed = [], []

        def job():
            try:
                returned.append(self.run_job(**kwargs))
            except BaseException as exc:  # surfaced on the test thread below
                failed.append(exc)

        def kill_groups():
            for group in groups():
                try:
                    os.killpg(group, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass

        runner = threading.Thread(target=job, daemon=True)
        runner.start()
        runner.join(seconds)
        if runner.is_alive() or failed:
            kill_groups()
            runner.join(5)
            if failed:
                raise failed[0]
            self.fail(f"run_job did not return within {seconds} s real time")
        return returned[0]

    def recorded_groups(self, request_id, ready=None):
        """Process groups for a request: the leader's pid from result.json (ask starts
        the leader in a new session, so its pid is the group ID), recorded as soon as
        it launches, and the fixture child's own group when its readiness file exists."""
        groups = set()
        record = ask.read(self.bridge.request_path(request_id) / "result.json") or {}
        if isinstance(record.get("process_id"), int):
            groups.add(record["process_id"])
        if ready is not None:
            try:
                groups.add(json.loads(ready.read_text())["group"])
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                pass
        return groups

    def test_timeout_kills_descendant_after_leader_exits(self):
        # Under machine load the fixture child once took longer than the 0.5 s timeout
        # to start, so the kill came before "child-ready" (1 of 1,277, 2026-11-13). The
        # job's clock now holds still until the child has printed "child-ready" (it
        # writes fixture-child.json after the print), so the 0.5 s timeout always fires
        # on a live, SIGTERM-ignoring descendant, and the 7 s bound runs from there.
        # run_job is synchronous, so both jobs here run under a real-time deadline: a
        # hang fails the test after killing every group the job started, found from the
        # leader's recorded pid even when the child never became ready. 30 s covers the
        # clock's 20 s hold cap, the 0.5 s timeout, ask's 3 s grace and 1 s collection.
        ready = self.project / "fixture-child.json"
        clock = ReadinessGatedClock(ready)
        groups = lambda: self.recorded_groups("timeout-descendant", ready)
        # After a normal return, clean up only the child's own group (still alive only if
        # the kill failed); a reaped leader's pid is not killed, as it may be reused.
        self.addCleanup(lambda: [self._kill_quietly(g) for g in self.recorded_groups_from_ready(ready)])
        with mock.patch.object(ask, "time", clock):
            result = self.run_bounded(30, groups, prompt="DESCENDANT", timeout=0.5,
                                      request_id="timeout-descendant")
        self.assertEqual(result["status"], "timed_out")
        self.assertIsNotNone(clock.ready_at, "the descendant never became ready")
        output = (self.bridge.request_path(result["request_id"]) / "events.jsonl").read_text()
        self.assertIn("child-ready", output)
        # The bound covers the whole kill: the group must be gone within 7 s of readiness,
        # so the group wait gets only what remains of that budget.
        remaining = 7 - (time.monotonic() - clock.ready_at)
        self.assertGreater(remaining, 0)
        self.wait_for_group_gone(json.loads(ready.read_text())["group"], remaining)
        self.assertLess(time.monotonic() - clock.ready_at, 7)
        follow = self.run_bounded(15, lambda: self.recorded_groups("timeout-follow-up"),
                                  request_id="timeout-follow-up")
        self.assertEqual(follow["status"], "completed")

    @staticmethod
    def recorded_groups_from_ready(ready):
        try:
            return {json.loads(ready.read_text())["group"]}
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return set()

    @staticmethod
    def _kill_quietly(group):
        try:
            os.killpg(group, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass

    def test_explicit_cancel_kills_ready_descendant_group(self):
        output = []
        ready = self.project / "fixture-child.json"
        thread = self.start_job_thread(output, "descendant", ready, prompt="DESCENDANT")
        group = self.wait_for_group(ready)
        self.bridge.cancel("descendant")
        thread.join(7)
        self.assertFalse(thread.is_alive())
        self.assertEqual(output[0]["status"], "cancelled")
        self.wait_for_group_gone(group, 2)

    def test_background_returns_and_retains_session_lock_and_result(self):
        started = time.monotonic()
        accepted = self.run_job(prompt="SLEEP", request_id="background", background=True)
        worker = accepted["owner_pid"]
        self.addCleanup(reap_child, worker)
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
                self.addCleanup(reap_child, accepted["owner_pid"])
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
            capture_output=True, text=True, check=True, timeout=30)
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
        # Registered before the readiness wait, so a fixture that never becomes ready is
        # still cleaned up: the child's group from its file, and, while the runner is still
        # alive, the leader's group from result.json (a reaped leader's pid may be reused).
        def cleanup_group():
            groups = (self.recorded_groups(request_id, ready) if runner.poll() is None
                      else self.recorded_groups_from_ready(ready))
            for group in groups:
                try:
                    os.killpg(group, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                except PermissionError:  # macOS denies while reaping; a live group still fails here
                    self.wait_for_group_gone(group, 3)
        self.addCleanup(cleanup_group)
        group = self.wait_for_group(ready, runner)
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
                self.wait_for_group_gone(group, 2)
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
        self.wait_for_group_gone(group, 3)
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
        ready = self.project / "fixture-detached.json"
        thread = self.start_job_thread(output, "detached", ready, prompt="DETACHED")
        group = self.wait_for_group(ready)
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
        self.addCleanup(reap_child, children[0])
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
