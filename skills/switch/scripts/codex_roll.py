"""Fresh Codex workers with context observation over local app-server stdio.

No daemon, socket listener, transcript resume or existing TUI takeover.
"""

import json
import math
import os
from pathlib import Path
import queue
import signal
import subprocess
import threading
import time


class ProtocolError(RuntimeError):
    pass


def descendants(pid):
    """Snapshot child identities while the owned parent still exists (POSIX)."""
    result = subprocess.run(["ps", "-axo", "pid=,ppid=,lstart="], text=True, capture_output=True, check=True)
    rows = [line.split(maxsplit=2) for line in result.stdout.splitlines()]
    pending, found = {pid}, {}
    while pending:
        children = {int(p): stamp.strip() for p, parent, stamp in rows if int(parent) in pending}
        pending = set(children) - set(found)
        found.update(children)
    return found


def children_gone(identities):
    # Observe only; never kill a possibly re-used detached PID.
    for pid, stamp in identities.items():
        result = subprocess.run(["ps", "-p", str(pid), "-o", "lstart="], text=True, capture_output=True)
        if result.returncode not in {0, 1}:
            raise ProtocolError("Cannot inspect owned child after shutdown")
        if result.returncode == 0 and result.stdout.strip() == stamp.strip():
            return False
    return True


def group_gone(pid):
    try:
        os.killpg(pid, 0)
    except ProcessLookupError:
        return True
    except PermissionError:
        raise ProtocolError("Cannot inspect owned process group after shutdown") from None
    return False


def stop_owned_children(identities):
    """Stop only still-matching children captured before the owned parent exited."""
    for pid, stamp in identities.items():
        result = subprocess.run(["ps", "-p", str(pid), "-o", "lstart="], text=True, capture_output=True)
        if result.returncode not in {0, 1}:
            raise ProtocolError("Cannot verify owned child identity for shutdown")
        if result.returncode == 0 and result.stdout.strip() == stamp.strip():
            try:
                os.kill(int(pid), signal.SIGTERM)
            except ProcessLookupError:
                pass
            except PermissionError:
                raise ProtocolError("Cannot stop verified owned child; continuation remains blocked") from None


class ContextWatch:
    def __init__(self, fraction=0.65, test_tokens=None):
        if not math.isfinite(fraction) or not 0 < fraction < 0.9:
            raise ValueError("Context reserve must use a fraction between 0 and 0.9")
        if test_tokens is not None and (type(test_tokens) is not int or test_tokens <= 0):
            raise ValueError("Test trigger must be a positive token count")
        self.fraction, self.test_tokens = fraction, test_tokens
        self.readings = []
        self.trigger = None

    def observe(self, usage):
        last = usage.get("last", {})
        used, window = last.get("totalTokens"), usage.get("modelContextWindow")
        if type(used) is not int or used < 0:
            raise ProtocolError("Missing valid last-request context usage")
        if type(window) is not int or window <= 0:
            raise ProtocolError("Usable context window is unavailable; no guessed pressure threshold")
        threshold = min(int(window * self.fraction), self.test_tokens or window)
        reading = {"last": last, "model_context_window": window, "threshold": threshold}
        self.readings.append(reading)
        if self.trigger is None and used >= threshold:
            self.trigger = reading
            return True
        return False


class AppServer:
    def __init__(self, root, stderr, command=None):
        # Managed file/CLI jobs do not use desktop control. Its native helper can
        # outlive EOF. Disable the tool for this child only, never global settings;
        # some hosts still prewarm its helper, so verified cleanup remains required.
        self.proc = subprocess.Popen(command or ["codex", "app-server", "--stdio", "--disable", "computer_use"],
                                     cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=stderr, text=True, start_new_session=True)
        self.messages, self.counter = queue.Queue(), 0
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()

    def _read(self):
        try:
            for line in self.proc.stdout:
                self.messages.put(json.loads(line))
        except Exception as exc:
            self.messages.put(exc)
        finally:
            self.messages.put(None)

    def send(self, method, params, notification=False):
        message = {"method": method, "params": params}
        if not notification:
            self.counter += 1
            message["id"] = self.counter
        self.proc.stdin.write(json.dumps(message) + "\n")
        self.proc.stdin.flush()
        return message.get("id")

    def receive(self, timeout=0.25):
        try:
            message = self.messages.get(timeout=timeout)
        except queue.Empty:
            return {}
        if message is None:
            raise ProtocolError("App-server exited before the expected result")
        if isinstance(message, Exception):
            raise ProtocolError("Invalid app-server stream") from message
        if "method" in message and "id" in message:
            # This managed job cannot invent an answer or grant additional authority.
            self.proc.stdin.write(json.dumps({"id": message["id"], "error": {
                "code": -32601, "message": "Managed Roll cannot answer host approval or user-input requests"}}) + "\n")
            self.proc.stdin.flush()
            raise ProtocolError("Host requested a decision; stop for Conductor reassessment")
        return message


class AppServerBridge:
    """The narrow Bridge interface consumed by Roller; fresh calls only."""

    context_aware = True

    def __init__(self, project, transport, fraction=0.65, test_tokens=None):
        ContextWatch(fraction, test_tokens)
        self.transport, self.core = transport, transport.Bridge(project)
        self.root, self.state = self.core.root, self.core.state
        self.fraction, self.test_tokens = fraction, test_tokens
        self._held = None
        self._held_lock = None

    def close(self, alias):
        self.core.close(alias)

    def run(self, target, prompt, role, session, request_id, writable=False,
            model=None, effort=None, timeout=None, hold=False, checkpoint_requested=None,
            checkpoint_instruction=None):
        if self._held is not None:
            raise ProtocolError("This controller still owns a held source")
        lock = self.transport.exclusive(self.core.session_path(session).with_suffix(".lock"))
        lock.__enter__()
        try:
            self.core.ensure_resolved(session)
            return self._run(target, prompt, role, session, request_id, writable, model, effort, timeout, hold, checkpoint_requested, checkpoint_instruction)
        finally:
            if self._held is not None:
                self._held_lock = lock
            else:
                lock.__exit__(None, None, None)

    def inspect_held(self, timeout=10):
        """Probe the same live thread, without loading its turns or resuming it."""
        if self._held is None:
            raise ProtocolError("No held source owned by this controller")
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("Inspection timeout must be positive and finite")
        server, record, folder = self._held
        if record.get("phase") != "held":
            raise ProtocolError("Held source requires reassessment; a later idle reading cannot clear uncertainty")
        try:
            return self._inspect_held(timeout)
        except Exception as exc:
            record.update(phase="held_uncertain", hold_error=str(exc))
            self.transport.save(folder / "result.json", record)
            raise

    def _inspect_held(self, timeout):
        server, record, _ = self._held
        if server.proc.poll() is not None:
            raise ProtocolError("Held source exited unexpectedly; no destination may start")
        ident = server.send("thread/read", {"threadId": record["session_id"], "includeTurns": False})
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            message = server.receive()
            if message.get("id") == ident:
                thread = message.get("result", {}).get("thread", {})
                if ("error" in message or thread.get("id") != record["session_id"]
                        or thread.get("status", {}).get("type") != "idle"
                        or server.proc.poll() is not None):
                    raise ProtocolError("Held source is not the same loaded idle thread")
                return {"status": "held", "source_alive": True, "thread_status": "idle"}
            if message.get("method") in {"thread/compacted", "model/rerouted", "turn/started"}:
                raise ProtocolError("Unexpected activity while source was held")
        raise ProtocolError("Held source inspection timed out; retention is unproved")

    def held_result(self):
        if self._held is None:
            raise ProtocolError("No held source owned by this controller")
        return dict(self._held[1])

    def held_cancelled(self):
        if self._held is None:
            raise ProtocolError("No held source owned by this controller")
        return (self._held[2] / "cancel.json").exists()

    def release_held(self, *, abandon=False):
        """Explicit owned-child shutdown. Handoff callers must verify save first.

        No finalizer: save errors must not implicitly release the source. The
        synchronous controller must remain alive until release or explicit abandon.
        """
        if self._held is None:
            raise ProtocolError("No held source owned by this controller")
        server, record, folder = self._held
        if not abandon and record.get("phase") != "held":
            raise ProtocolError("Uncertain held source cannot be released as a successful handoff")
        record.update(status="cancelled" if abandon else "completed", phase="releasing")
        if abandon:
            record["provider_completed"] = False
        self._shutdown(server, record)
        record.update(finished_at=self.transport.now(), phase="abandoned" if abandon else "released")
        self.transport.save(folder / "result.json", record)
        if record.get("owned_children_gone") is True and not record.get("cleanup_error"):
            self._held = None
            self._held_lock.__exit__(None, None, None)
            self._held_lock = None
        return dict(record)

    def _run(self, target, prompt, role, session, request_id, writable=False,
             model=None, effort=None, timeout=None, hold=False, checkpoint_requested=None,
             checkpoint_instruction=None):
        if target != "codex" or not model or not effort:
            raise ValueError("Context-aware Roll currently requires an explicit Codex model/effort")
        if timeout is not None and (not math.isfinite(timeout) or timeout <= 0):
            raise ValueError("Optional timeout must be positive and finite")
        if self.core.session_path(session).exists():
            raise ProtocolError("Context-aware Roll requires a fresh alias, never session resume")
        folder = self.core.request_path(request_id)
        folder.mkdir(mode=0o700)
        record = {"request_id": request_id, "session": session, "target": target, "project": str(self.root),
                  "status": "running", "owner_pid": os.getpid(),
                  "started_at": self.transport.now(), "requested_model": model,
                  "requested_effort": effort, "session_id": None,
                  "authority": "project edits" if writable else "read only",
                  "route": "app-server-stdio", "context_test_trigger": self.test_tokens}
        self.transport.save(folder / "request.json", {"prompt": prompt, "role": role,
            "session": session, "target": target, "project": str(self.root),
            "writable": writable, "model": model, "effort": effort, "timeout": timeout})
        self.transport.save(folder / "result.json", record)
        watch, server = ContextWatch(self.fraction, self.test_tokens), None
        begun, interrupted = time.monotonic(), False
        pending, final_messages, active_turn = {}, {}, None
        completed, steer_pending = False, None
        stream = []

        def emit(status, **values):
            print(json.dumps({"status": status, **values}), flush=True)

        def request(method, params):
            ident = server.send(method, params)
            pending[ident] = method
            return ident

        def checkpoint(reason):
            nonlocal steer_pending
            if completed or record.get("checkpoint_requested"):
                return
            record["checkpoint_requested"] = reason
            steer_pending = request("turn/steer", {"threadId": record["session_id"], "expectedTurnId": active_turn,
                "input": [{"type": "text", "text": reason + ". " + (checkpoint_instruction or "Finish the current safe local operation; "
                "do not start another work package. Return the saved-place JSON now, retaining actual "
                "progress, decisions, evidence and failed attempts. Use continue if work remains, "
                "review only if genuinely ready. Do not launch any other job.")}]})

        try:
            with self.transport.shutdown_signals(), open(folder / "stderr.txt", "x") as stderr:
                os.chmod(folder / "stderr.txt", 0o600)
                server = AppServer(self.root, stderr)
                record["process_id"] = server.proc.pid
                self.transport.save(folder / "result.json", record)
                request("initialize", {"clientInfo": {"name": "kerd_roll", "version": "0.1"}})
                while not completed or steer_pending is not None:
                    if (folder / "cancel.json").exists() or (timeout and time.monotonic() - begun >= timeout):
                        interrupted = True
                        raise ProtocolError("Managed job cancelled or its optional timeout elapsed")
                    if active_turn and checkpoint_requested is not None and checkpoint_requested():
                        if not record.get("checkpoint_requested") and not completed:
                            emit("saving_place", reason="live Conductor request")
                            checkpoint("A safe checkpoint was requested by the live Conductor connection")
                    message = server.receive()
                    if not message:
                        continue
                    if "id" in message:
                        method = pending.pop(message["id"], None)
                        if method is None:
                            raise ProtocolError("Unexpected protocol response")
                        if "error" in message:
                            # A steer can race natural completion; only that completed turn is usable.
                            if method == "turn/steer" and completed:
                                steer_pending = None
                                record["steer_race"] = "turn already completed"
                                continue
                            raise ProtocolError(f"{method} failed: {message['error']}")
                        result = message["result"]
                        if method == "initialize":
                            server.send("initialized", {}, notification=True)
                            request("thread/start", {"cwd": str(self.root), "model": model,
                                    "approvalPolicy": "never", "sandbox": "workspace-write" if writable else "read-only",
                                    "config": {"web_search": "disabled", "features.computer_use": False}, "allowProviderModelFallback": False})
                        elif method == "thread/start":
                            sid = result["thread"]["id"]
                            record.update(session_id=sid, model=result.get("model"))
                            effective = result.get("sandbox", {})
                            if result.get("model") != model:
                                raise ProtocolError("Host did not select the requested model")
                            if Path(result.get("cwd", "")).resolve() != self.root:
                                raise ProtocolError("Host returned a different project")
                            expected_policy = "workspaceWrite" if writable else "readOnly"
                            if (result.get("approvalPolicy") != "never" or effective.get("type") != expected_policy
                                    or effective.get("networkAccess") not in {None, False}):
                                raise ProtocolError("Host returned unexpected effective authority")
                            roots = effective.get("writableRoots", [])
                            if any(Path(root).resolve() != self.root for root in roots):
                                raise ProtocolError("Host added writable roots outside the project")
                            self.transport.save(folder / "result.json", record)
                            request("turn/start", {"threadId": sid, "effort": effort,
                                    "input": [{"type": "text", "text": prompt}]})
                        elif method == "turn/start":
                            if active_turn is not None and result["turn"]["id"] != active_turn:
                                raise ProtocolError("Turn start response changed the owned turn")
                            active_turn = result["turn"]["id"]
                        elif method == "turn/steer":
                            if result.get("turnId") != active_turn:
                                raise ProtocolError("Steer response belongs to a different turn")
                            steer_pending = None
                            record["steer_accepted"] = True
                        continue
                    method, params = message.get("method"), message.get("params", {})
                    sid = record.get("session_id")
                    if sid is not None and params.get("threadId") not in {None, sid}:
                        raise ProtocolError("Received an event for a different thread")
                    if active_turn is not None and params.get("turnId") not in {None, active_turn}:
                        raise ProtocolError("Received an event for a different turn")
                    stream.append({"method": method})  # No reasoning or transcript content.
                    if method == "turn/started":
                        if active_turn is not None and params["turn"]["id"] != active_turn:
                            raise ProtocolError("A second turn cannot replace the owned turn")
                        active_turn = params["turn"]["id"]
                    elif method == "thread/tokenUsage/updated":
                        if params.get("turnId") != active_turn:
                            raise ProtocolError("Usage belongs to a different turn")
                        if watch.observe(params["tokenUsage"]) and not completed:
                            emit("saving_place", context_tokens=watch.trigger["last"]["totalTokens"],
                                 threshold=watch.trigger["threshold"], test_trigger=self.test_tokens is not None)
                            checkpoint("Roll requested from observed context usage")
                        record["usage"] = params["tokenUsage"].get("total")
                        record["context_readings"] = watch.readings
                        record["context_trigger"] = watch.trigger
                        self.transport.save(folder / "result.json", record)
                    elif method in {"item/started", "item/completed"}:
                        item = params.get("item", {})
                        if item.get("type") == "contextCompaction":
                            raise ProtocolError("Native compaction occurred; no no-compaction pass or automatic continuation")
                        if method == "item/completed" and item.get("type") == "agentMessage":
                            # Final answers only; an unknown or renamed phase is not
                            # one. Unphased items (older servers) are read.
                            if item.get("phase") in (None, "final_answer"):
                                final_messages[item["id"]] = item.get("text", "")
                        if method == "item/started" and item.get("type") in {"commandExecution", "fileChange"}:
                            emit("working", activity=item["type"])
                    elif method == "thread/compacted":
                        raise ProtocolError("Native compaction occurred; saved handoff needs reassessment")
                    elif method == "model/rerouted":
                        raise ProtocolError("Requested worker model was rerouted; reassess model suitability")
                    elif method == "turn/completed":
                        if params["turn"]["id"] != active_turn or params["turn"]["status"] != "completed":
                            raise ProtocolError("Worker turn did not finish successfully")
                        completed = True
                if not watch.readings:
                    raise ProtocolError("No context readings observed; context-aware continuation is unproved")
                if not final_messages or (len(final_messages) != 1 and not record.get("steer_accepted")):
                    raise ProtocolError("Expected one final saved-place response")
                # A late accepted steer may cause a corrected final message within this
                # same owned turn. Roller validates every candidate with the shared state
                # checker before saving the last; no lost evidence/failure accounting.
                candidates = list(final_messages.values())
                record.update(status="completed", provider_completed=True, reply=candidates[-1],
                              checkpoint_candidates=candidates)
                # Retain the complete contribution before releasing the source process.
                # It is not a validated place or clean shutdown yet. A dead driver can
                # inspect this exact receipt instead of guessing or replaying the job.
                self.transport.save(folder / "result.json", {**record, "status": "running", "phase": "checkpoint_saved"})
                saved = self.transport.read(folder / "result.json")
                if saved.get("checkpoint_candidates") != candidates:
                    raise ProtocolError("Source checkpoint failed read-back before release")
        except BaseException as exc:
            record.update(status="cancelled" if interrupted or isinstance(exc, KeyboardInterrupt) else "failed",
                          provider_completed=False, error=str(exc))
            if not isinstance(exc, (Exception, KeyboardInterrupt)):
                raise
        finally:
            if hold and server and record.get("status") == "completed":
                # Keep the existing transport's unresolved status and session lock.
                # A completed model turn is not a completed transport lifetime.
                record.update(status="running", phase="held", held_at=self.transport.now())
                self._held = (server, record, folder)
            else:
                if server:
                    self._shutdown(server, record)
                record["finished_at"] = self.transport.now()
            record.update(context_readings=watch.readings, context_trigger=watch.trigger, protocol_events=stream)
            self.transport.save(folder / "result.json", record)
            if record.get("session_id"):
                self.transport.save(self.core.session_path(session), {"target": target, "project": str(self.root),
                    "session": session, "session_id": record["session_id"], "closed": False, "last_request": request_id})
        return dict(record)

    def _shutdown(self, server, record):
        # Shared by ordinary Roll and explicit held-source release.
        owned_children = None
        try:
            owned_children = descendants(server.proc.pid)
            record["owned_children"] = owned_children
        except Exception as exc:
            record["cleanup_error"] = f"Cannot identify owned children: {exc}"
        try:
            server.proc.stdin.close()
            try:
                server.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.transport.Bridge.stop(server.proc)
                server.proc.wait(timeout=5)
            server.reader.join(timeout=2)
            if server.reader.is_alive():
                raise ProtocolError("Owned stream remains open after shutdown; possible detached writer")
            server.proc.stdout.close()
            if owned_children is None:
                raise ProtocolError("Owned child identity unavailable; parent stopped but continuation is uncertain")
            record["owned_child_count"] = len(owned_children)
            deadline = time.monotonic() + 3
            stopped_survivors = False
            while not (children_gone(owned_children) and group_gone(server.proc.pid)):
                if time.monotonic() >= deadline:
                    if stopped_survivors:
                        raise ProtocolError("Owned child or process group is still present; no fresh worker may start")
                    stop_owned_children(owned_children)
                    record["owned_survivor_shutdown_requested"] = True
                    stopped_survivors = True
                    deadline = time.monotonic() + 3
                time.sleep(0.05)
            record["owned_children_gone"] = True
        except Exception as exc:
            record.update(status="interrupted", cleanup_error=str(exc), provider_completed=False)
