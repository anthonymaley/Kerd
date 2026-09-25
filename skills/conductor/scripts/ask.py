#!/usr/bin/env python3
"""Repo-local CLI request transport. No SDK, service, inbox or workflow engine."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
import uuid


def now():
    return datetime.now(timezone.utc).isoformat()


def name(value):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", value):
        raise ValueError("Names must contain 1–80 letters, digits, hyphens or underscores")
    return value


def read(path):
    return json.loads(path.read_text()) if path.exists() else None


def save(path, value):
    """Atomic, private local metadata; never rewrite another request's record."""
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=".writing-")
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


class Busy(Exception):
    pass


@contextmanager
def shutdown_signals():
    """Route normal CLI termination through request cleanup, then restore host handlers."""
    previous = {}
    def interrupt(signum, frame):
        # A second termination signal must not interrupt process-group cleanup.
        for sig in previous:
            signal.signal(sig, signal.SIG_IGN)
        raise KeyboardInterrupt
    if threading.current_thread() is threading.main_thread():
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            previous[sig] = signal.getsignal(sig)
            signal.signal(sig, interrupt)
    try:
        yield
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


@contextmanager
def exclusive(path):
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Busy("This named session already has an active request") from None
        yield fd
    finally:
        os.close(fd)


def parse_events(provider, output):
    result = {"session_id": None, "reply": "", "usage": None,
              "model": None, "files_reported": [], "provider_error": None,
              "provider_completed": False}
    session_ids = set()
    for line in output.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        if provider == "codex":
            if event.get("type") == "thread.started":
                result["session_id"] = event.get("thread_id")
                if result["session_id"]:
                    session_ids.add(result["session_id"])
            if event.get("type") == "item.completed":
                item = event.get("item", {})
                if item.get("type") == "agent_message":
                    result["reply"] = item.get("text", "")
                if item.get("type") == "file_change":
                    result["files_reported"].extend(c.get("path") for c in item.get("changes", [])
                                                     if c.get("path"))
            if event.get("type") == "turn.completed":
                result["provider_completed"] = True
                result["usage"] = event.get("usage")
            if event.get("type") == "turn.failed":
                result["provider_error"] = event.get("error", event)
        else:
            if event.get("session_id") and event.get("type") in ("system", "result") and not event.get("parent_tool_use_id"):
                result["session_id"] = event["session_id"]
                session_ids.add(event["session_id"])
            if event.get("type") == "system" and event.get("subtype") == "init":
                result["model"] = event.get("model")
            if event.get("type") == "result":
                result["provider_completed"] = True
                result["reply"] = event.get("result", "")
                result["usage"] = event.get("usage")
                result["estimated_cost_usd"] = event.get("total_cost_usd")
                if event.get("is_error") or event.get("subtype") != "success":
                    result["provider_error"] = event.get("errors") or event.get("result") or event
    if len(session_ids) > 1:
        result.update(session_id=None, provider_error="Conflicting session IDs within provider response")
    return result


class Bridge:
    def __init__(self, project=".", commands=None):
        project = Path(project).resolve()
        self.root = Path(subprocess.check_output(
            ["git", "-C", str(project), "rev-parse", "--show-toplevel"], text=True).strip()).resolve()
        git_dir = Path(subprocess.check_output(
            ["git", "-C", str(self.root), "rev-parse", "--absolute-git-dir"], text=True).strip())
        self.state = git_dir / "cross-llm"
        for folder in (self.state, self.state / "sessions", self.state / "requests"):
            folder.mkdir(mode=0o700, exist_ok=True)
        self.commands = commands or {"codex": ["codex"], "claude": ["claude"]}

    def session_path(self, session):
        return self.state / "sessions" / (name(session) + ".json")

    def request_path(self, request_id):
        return self.state / "requests" / name(request_id)

    def sessions(self):
        return [read(p) for p in sorted((self.state / "sessions").glob("*.json"))]

    def status(self, request_id):
        result_path = self.request_path(request_id) / "result.json"
        record = read(result_path)
        if record is None:
            spec = read(self.request_path(request_id) / "request.json")
            if spec is None:
                if self.request_path(request_id).is_dir():
                    return {"request_id": request_id, "project": str(self.root), "status": "unknown",
                            "error": "Request metadata incomplete; launch state uncertain, not retried"}
                raise ValueError("Unknown request")
            provisional = {"request_id": request_id, "session": spec["session"],
                           "target": spec["target"], "project": spec["project"]}
            try:
                with exclusive(self.session_path(spec["session"]).with_suffix(".lock")):
                    record = read(result_path)
                    if record is None:
                        record = {**provisional, "status": "failed",
                                  "error": "Submission ended before provider launch; not retried"}
                        save(result_path, record)
            except Busy:
                return {**provisional, "status": "starting"}
        if record["status"] == "starting":
            try:
                with exclusive(self.session_path(record["session"]).with_suffix(".lock")):
                    record = read(result_path)
                    if record["status"] == "starting":
                        # The child saves running before it launches any provider.
                        record.update(status="failed", finished_at=now(),
                                      error="Launcher stopped before provider launch; not retried")
                        save(result_path, record)
            except Busy:
                pass
        if record["status"] == "running":
            try:
                os.kill(record["owner_pid"], 0)
            except ProcessLookupError:
                return {**record, "status": "interrupted", "error": "Runner exited; provider state uncertain. Session reuse blocked; inspect native work. No automatic retry or PID-based kill."}
        return record

    def ensure_resolved(self, session):
        """Call while holding the session lock; durable uncertainty survives runner death."""
        for spec_path in (self.state / "requests").glob("*/request.json"):
            spec = read(spec_path)
            if spec.get("session") != session:
                continue
            record = read(spec_path.parent / "result.json")
            if record is None or record.get("status") in ("starting", "running", "interrupted", "unknown"):
                raise Busy(f"Prior request {spec_path.parent.name} has an unresolved outcome; inspect its status before reusing or closing this session")

    def wait(self, request_id, timeout=None):
        """Retrieve a final result, or current state when the caller stops waiting.

        This timeout affects only retrieval; it never cancels or resubmits work.
        """
        if timeout is not None and (not math.isfinite(timeout) or timeout < 0):
            raise ValueError("An optional wait timeout must be finite and nonnegative")
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            record = self.status(request_id)
            if record["status"] not in ("starting", "running"):
                return record
            remaining = None if deadline is None else deadline - time.monotonic()
            if remaining is not None and remaining <= 0:
                return record
            time.sleep(0.1 if remaining is None else min(0.1, remaining))

    def cancel(self, request_id):
        record = self.status(request_id)
        if record["status"] in ("starting", "running"):
            save(self.request_path(request_id) / "cancel.json", {"requested_at": now()})
            return {"request_id": request_id, "status": "cancellation_requested"}
        return record

    def resolve(self, request_id):
        """Explicitly retire an uncertain result only after its recorded group is gone."""
        request_path = self.request_path(request_id)
        spec = read(request_path / "request.json")
        if not spec:
            raise ValueError("Request has no session metadata; cannot safely resolve")
        with exclusive(self.session_path(spec["session"]).with_suffix(".lock")):
            record = read(request_path / "result.json")
            if not record or record.get("status") not in ("running", "interrupted", "unknown"):
                raise ValueError("Only an interrupted or uncertain launched request can be resolved")
            group = record.get("process_id")
            if not isinstance(group, int) or group <= 1:
                raise ValueError("Provider group was not recorded; inspect native work, cannot safely resolve")
            try:
                os.killpg(group, 0)  # existence probe, never a termination signal
            except ProcessLookupError:
                pass
            except PermissionError:
                raise Busy("Recorded provider group cannot be inspected; cannot safely resolve") from None
            else:
                raise Busy("Recorded provider group is still present; cannot resolve or reuse this session")
            record.update(status="abandoned", resolved_at=now(),
                          error="Caller resolved uncertain work after recorded provider group disappeared; outcome not proven")
            save(request_path / "result.json", record)
            return record

    def close(self, session):
        path = self.session_path(session)
        with exclusive(path.with_suffix(".lock")):
            self.ensure_resolved(session)
            record = read(path)
            if not record:
                raise ValueError("Unknown session")
            record.update(closed=True, closed_at=now())
            save(path, record)
            return record

    def command(self, target, sid, writable, model, effort):
        args = list(self.commands[target])
        if target == "codex":
            args += ["exec", "--json", "--color", "never", "--sandbox",
                     "workspace-write" if writable else "read-only", "-c", 'approval_policy="never"']
            if model:
                args += ["--model", model]
            if effort:
                args += ["-c", "model_reasoning_effort=" + json.dumps(effort)]
            if sid:
                args += ["resume", sid]
            args += ["-"]
        else:
            allowed = "Read,Glob,Grep,Edit,Write" if writable else "Read,Glob,Grep"
            args += ["-p", "--output-format", "stream-json", "--verbose",
                     "--permission-mode", "dontAsk", "--permission-prompts", "none",
                     "--tools", allowed, "--allowedTools", allowed, "--strict-mcp-config"]
            if model:
                args += ["--model", model]
            if effort:
                args += ["--effort", effort]
            if sid:
                args += ["--resume", sid]
        return args

    def run(self, target, prompt, role, session, request_id=None, writable=False,
            model=None, effort=None, timeout=None, background=False):
        if target not in self.commands:
            raise ValueError("Target must be codex or claude")
        if not prompt.strip() or not role.strip():
            raise ValueError("A task and caller-supplied role are required")
        if timeout is not None and (not math.isfinite(timeout) or timeout <= 0):
            raise ValueError("An optional timeout must be finite and positive")
        session_path = self.session_path(session)
        request_id = name(request_id or str(uuid.uuid4()))
        request_dir = self.request_path(request_id)
        spec = dict(target=target, prompt=prompt, role=role, session=session,
                    project=str(self.root), writable=writable, model=model, effort=effort, timeout=timeout)
        if request_dir.exists():
            saved = read(request_dir / "request.json")
            if saved is not None and saved != spec:
                raise ValueError("Request ID already belongs to a different job")
            return self.status(request_id)
        with shutdown_signals(), exclusive(session_path.with_suffix(".lock")) as lock_fd:
            self.ensure_resolved(session)
            existing = read(session_path)
            if existing and (existing["target"] != target or existing["project"] != str(self.root)):
                raise ValueError("Session belongs to a different provider or project")
            if existing and existing.get("closed"):
                raise ValueError("Session is closed; choose a new name")
            sid = existing.get("session_id") if existing else None
            try:
                request_dir.mkdir(mode=0o700)
            except FileExistsError:
                raise Busy("Request ID is already being submitted") from None
            save(request_dir / "request.json", spec)
            record = {"request_id": request_id, "session": session, "target": target,
                      "project": str(self.root), "status": "starting" if background else "running", "owner_pid": os.getpid(),
                      "started_at": now(), "session_id": sid, "requested_model": model,
                      "requested_effort": effort, "authority": "project edits" if writable else "read only"}
            proc = None
            output = errors = ""
            background_child = False
            launch_attempted = False
            fork_attempted = False
            child = None
            try:
                save(request_dir / "result.json", record)
                if background:
                    # The child inherits the held session lock; no queue or launch gap.
                    fork_attempted = True
                    child = os.fork()
                    if child:
                        return {**record, "owner_pid": child}
                    background_child = True
                    os.setsid()
                    quiet = os.open(os.devnull, os.O_RDWR)
                    for descriptor in (0, 1, 2):
                        os.dup2(quiet, descriptor)
                    if quiet > 2:
                        os.close(quiet)
                    record.update(status="running", owner_pid=os.getpid())
                    save(request_dir / "result.json", record)
                authority = ("You may create or edit task files within this project. Do not commit or publish."
                             if writable else
                             "Read-only contribution: inspect relevant project files using available read-only tools "
                             "or inspection commands. Do not change files, run write-producing tests/builds, "
                             "install anything, access the network, commit or publish.")
                task = (f"Current request: {request_id}\nProject: {self.root}\n"
                        f"Caller-supplied role for THIS request: {role}\n"
                        f"Authority: {authority}\nDo not dispatch other agents or access unrelated material.\n"
                        "Return your contribution, evidence, relevant file paths and any limitations.\n\n"
                        f"Task:\n{prompt}\n")
                args = self.command(target, sid, writable, model, effort)
                if (request_dir / "cancel.json").exists():
                    raise KeyboardInterrupt
                launch_attempted = True
                proc = subprocess.Popen(args, cwd=self.root, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        text=True, start_new_session=True)
                record["process_id"] = proc.pid
                save(request_dir / "result.json", record)
                begun = time.monotonic()
                last_progress = begun
                first = True
                while True:
                    try:
                        output, errors = proc.communicate(task if first else None, timeout=0.2)
                        break
                    except subprocess.TimeoutExpired as pending:
                        first = False
                        if time.monotonic() - last_progress >= 2:
                            partial = pending.output or b""
                            if isinstance(partial, bytes):
                                partial = partial.decode("utf-8", errors="replace")
                            progress = parse_events(target, partial)
                            record.update(session_id=progress["session_id"] or sid,
                                          model=progress["model"], updated_at=now(),
                                          provider_output_bytes=len(partial.encode("utf-8")))
                            save(request_dir / "result.json", record)
                            last_progress = time.monotonic()
                        cancelled = (request_dir / "cancel.json").exists()
                        expired = timeout is not None and time.monotonic() - begun >= timeout
                        if cancelled or expired:
                            record["status"] = "cancelled" if cancelled else "timed_out"
                            output, errors = self.stop_and_collect(proc, record)
                            break
                parsed = parse_events(target, output)
                record.update(parsed, exit_code=proc.returncode)
                returned_sid = parsed["session_id"]
                if sid and returned_sid and sid != returned_sid and not record.get("cleanup_error"):
                    record.update(status="failed", error="Provider changed the requested session; not rebound")
                elif record["status"] == "running":
                    ok = proc.returncode == 0 and parsed["provider_completed"] and not parsed["provider_error"] and returned_sid
                    record["status"] = "completed" if ok else "failed"
                    if not ok:
                        record["error"] = parsed["provider_error"] or "Provider exited without a successful, attributed result"
                if returned_sid and (not sid or returned_sid == sid):
                    save(session_path, {"target": target, "project": str(self.root), "session": session,
                                        "session_id": returned_sid, "closed": False, "last_request": request_id})
            except KeyboardInterrupt:
                if fork_attempted and not background_child:
                    # The child may already own this request, even if fork was interrupted
                    # before returning its PID. The parent must never finalize its result.
                    raise
                if proc:
                    output, errors = self.stop_and_collect(proc, record)
                if launch_attempted and proc is None:
                    record.update(status="interrupted", error="Interrupted during provider launch; process identity unknown, inspect native work before recovery")
                elif not record.get("cleanup_error"):
                    record.update(status="cancelled", error="Caller interrupted the request")
            except Exception as exc:
                if child:
                    raise
                if proc:
                    output, errors = self.stop_and_collect(proc, record)
                if not record.get("cleanup_error"):
                    record.update(status="failed", error=str(exc))
            record["finished_at"] = now()
            # Provider events are local troubleshooting evidence, not proof of task quality.
            for filename, content in (("events.jsonl", output), ("stderr.txt", errors)):
                fd = os.open(request_dir / filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(fd, "w") as stream:
                    stream.write(content)
            if background_child:
                # os._exit() below skips the with-block's cleanup, so the fork-inherited
                # session lock would otherwise only be released by the kernel during process
                # teardown, after this result is already visible to callers polling status().
                # Release it explicitly first so "completed" never appears while still locked.
                # Unlock rather than close: the with-block's own close still owns the fd.
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            save(request_dir / "result.json", record)
            if background_child:
                os._exit(0 if record["status"] == "completed" else 1)
            return record

    def stop_and_collect(self, proc, record):
        try:
            self.stop(proc)
        except OSError as exc:
            record.update(status="interrupted", cleanup_error=str(exc),
                          error="Process cleanup could not be confirmed; session reuse blocked")
        return self.collect_stopped(proc, record)

    @staticmethod
    def collect_stopped(proc, record):
        try:
            return proc.communicate(timeout=1)
        except subprocess.TimeoutExpired as pending:
            record["cleanup_warning"] = "Output pipe stayed open after group cleanup; detached descendants may survive. Stopped collecting output."
            for stream in (proc.stdin, proc.stdout, proc.stderr):
                if stream:
                    stream.close()
            def decoded(value):
                return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value or ""
            return decoded(pending.output), decoded(pending.stderr)

    @staticmethod
    def stop(proc):
        # The group can outlive its leader and hold inherited pipes open.
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            proc.wait()
            return
        deadline = time.monotonic() + 3
        denied_probe = None
        while time.monotonic() < deadline:
            proc.poll()  # reap an exited leader while checking its whole group
            try:
                os.killpg(proc.pid, 0)
            except ProcessLookupError:
                proc.wait()
                return
            except PermissionError as exc:
                # A macOS exit-time probe can be denied briefly. Retry only
                # observation within the existing grace period: denial is not
                # disappearance, nor permission to send another signal.
                denied_probe = exc
            time.sleep(0.05)
        if denied_probe is not None:
            raise denied_probe
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".")
    sub = parser.add_subparsers(dest="action", required=True)
    run = sub.add_parser("run", help="Run a caller-defined job and return its result")
    run.add_argument("--target", choices=["codex", "claude"], required=True)
    run.add_argument("--session", required=True, help="Local name; created on first use, reused thereafter")
    run.add_argument("--role", required=True)
    run.add_argument("--prompt-file", help="Read task from file; otherwise stdin")
    run.add_argument("--request-id", help="Optional stable id; duplicate submission does not rerun")
    run.add_argument("--write", action="store_true", help="Permit task file edits within the project")
    run.add_argument("--model")
    run.add_argument("--effort")
    run.add_argument("--timeout", type=float, help="Optional seconds; no timeout by default")
    run.add_argument("--background", action="store_true", help="Return immediately while a local child executes the request")
    sub.add_parser("sessions")
    for action in ("status", "cancel", "resolve"):
        command = sub.add_parser(action)
        command.add_argument("request_id")
    wait = sub.add_parser("wait", help="Wait for a retained result without cancelling work")
    wait.add_argument("request_id")
    wait.add_argument("--timeout", type=float,
                      help="Optional seconds to wait; 0 retrieves immediately; does not cancel work")
    sub.add_parser("close").add_argument("session")
    args = parser.parse_args()
    try:
        bridge = Bridge(args.project)
        if args.action == "run":
            prompt = Path(args.prompt_file).read_text() if args.prompt_file else sys.stdin.read()
            result = bridge.run(args.target, prompt, args.role, args.session, args.request_id,
                                args.write, args.model, args.effort, args.timeout, args.background)
        elif args.action == "sessions":
            result = bridge.sessions()
        elif args.action == "close":
            result = bridge.close(args.session)
        elif args.action == "wait":
            result = bridge.wait(args.request_id, args.timeout)
        else:
            result = getattr(bridge, args.action)(args.request_id)
        print(json.dumps(result, indent=2))
        return 0 if not isinstance(result, dict) or result.get("status") in (None, "starting", "running", "completed", "cancellation_requested") else 1
    except (ValueError, Busy, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "busy" if isinstance(exc, Busy) else "error", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
