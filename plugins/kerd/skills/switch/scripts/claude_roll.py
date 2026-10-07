"""Fresh Claude workers with context observation over stream-json stdio.

One `claude -p` process per run. A fixed bootstrap turn proves the effective
authority and reports the context window before any work is sent; the work turn
is then watched from its own usage and asked for its saved place at a tool
boundary. No resume, retained source, live control or compaction.
"""

import json
import math
import os
from pathlib import Path
import queue
import subprocess
import threading
import time

import codex_roll
from codex_roll import DEFAULT_CHECKPOINT_INSTRUCTION, ContextWatch, ProtocolError


ROUTE = "claude-stream-json"
BOOTSTRAP = "Reply READY and nothing else. Do not use any tools."
READ_TOOLS = frozenset({"Read", "Glob", "Grep"})
WRITE_TOOLS = frozenset({"Edit", "Write"})
CHECKPOINT_REASON = "Roll requested from observed context usage"
STEER_RACE = "turn completed before a tool boundary"
USAGE_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
HOOK_SUBTYPES = frozenset({"hook_started", "hook_progress", "hook_response"})
RECORDED_SUBTYPES = frozenset({"commands_changed", "thinking_tokens", "task_started",
                               "task_notification", "api_retry"})
DRAIN_SUBTYPES = HOOK_SUBTYPES | {"commands_changed"}
EOF = object()


def leader_start(pid):
    """The owned leader's start time, recorded so a reused PID is never mistaken for it."""
    result = subprocess.run(["ps", "-p", str(pid), "-o", "lstart="], text=True, capture_output=True)
    stamp = result.stdout.strip() if result.returncode == 0 else ""
    if not stamp:
        raise ProtocolError("Cannot record the owned Claude process start time; identity is unproved")
    return stamp


def owner_of(event):
    """None for the main conversation, the parent tool use id for a subagent; anything else stops."""
    if "parent_tool_use_id" not in event:
        raise ProtocolError("Claude event lacks parent_tool_use_id; conversation ownership is unproved")
    parent = event["parent_tool_use_id"]
    if parent is None or (isinstance(parent, str) and parent):
        return parent
    raise ProtocolError("Claude event has an invalid parent_tool_use_id; conversation ownership is unproved")


def _blocks_continuation(value):
    if isinstance(value, dict):
        if value.get("decision") == "block" or value.get("continue") is False:
            return True
        return any(_blocks_continuation(item) for item in value.values())
    if isinstance(value, list):
        return any(_blocks_continuation(item) for item in value)
    return False


def hook_ok(event, sid):
    """A hook event belongs to this session, succeeded, and asks nothing to block or stop."""
    if not isinstance(sid, str) or not sid or event.get("session_id") != sid:
        return False
    if event.get("subtype") == "hook_response":
        code = event.get("exit_code")
        if event.get("outcome") != "success" or type(code) is not int or code != 0:
            return False
    output = event.get("output")
    if output is None:
        return True
    if not isinstance(output, str):
        return False
    try:
        values = [json.loads(output)]
    except ValueError:
        # JSON Lines; plain text lines are allowed and skipped.
        values = []
        for line in output.splitlines():
            try:
                values.append(json.loads(line))
            except ValueError:
                continue
    return not any(_blocks_continuation(value) for value in values)


class ClaudeStream:
    """An owned `claude -p` stream-json process; parsed stdout lines arrive on a queue."""

    def __init__(self, root, stderr, command):
        self.proc = subprocess.Popen(command, cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=stderr, text=True, start_new_session=True)
        self.messages = queue.Queue()
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()

    def _read(self):
        try:
            for line in self.proc.stdout:
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise ProtocolError("Claude stream line is not a JSON object")
                self.messages.put(event)
        except Exception as exc:
            self.messages.put(exc)
        finally:
            self.messages.put(None)

    def send(self, text):
        self.proc.stdin.write(json.dumps({"type": "user", "message": {"role": "user", "content": text}}) + "\n")
        self.proc.stdin.flush()

    def receive(self, timeout=0.25):
        """An event, None when nothing arrived in time, or EOF when the stream ended."""
        try:
            message = self.messages.get(timeout=timeout)
        except queue.Empty:
            return None
        if message is None:
            return EOF
        if isinstance(message, Exception):
            raise ProtocolError("Invalid Claude stream: a line is not a JSON object") from message
        return message


class ClaudeStreamBridge:
    """The narrow Bridge interface consumed by Roller; fresh calls only, no held source."""

    context_aware = True
    STARTUP_TIMEOUT = 60
    DRAIN_TIMEOUT = 10

    def __init__(self, project, transport, fraction=0.65, test_tokens=None):
        ContextWatch(fraction, test_tokens)
        self.transport, self.core = transport, transport.Bridge(project)
        self.root, self.state = self.core.root, self.core.state
        self.fraction, self.test_tokens = fraction, test_tokens

    def close(self, alias):
        self.core.close(alias)

    def run(self, target, prompt, role, session, request_id, writable=False,
            model=None, effort=None, timeout=None, hold=False, checkpoint_requested=None,
            checkpoint_instruction=None):
        with self.transport.exclusive(self.core.session_path(session).with_suffix(".lock")):
            self.core.ensure_resolved(session)
            return self._run(target, prompt, role, session, request_id, writable, model, effort,
                             timeout, hold, checkpoint_requested, checkpoint_instruction)

    def _run(self, target, prompt, role, session, request_id, writable, model, effort,
             timeout, hold, checkpoint_requested, checkpoint_instruction):
        if target != "claude" or not model or not effort:
            raise ValueError("Context-aware Claude Roll requires target claude with an explicit model/effort")
        if hold or checkpoint_requested is not None:
            raise ProtocolError("Claude context-aware Roll has no retainable source or live control in v1")
        if timeout is not None and (not math.isfinite(timeout) or timeout <= 0):
            raise ValueError("Optional timeout must be positive and finite")
        if self.core.session_path(session).exists():
            raise ProtocolError("Context-aware Roll requires a fresh alias, never session resume")
        folder = self.core.request_path(request_id)
        folder.mkdir(mode=0o700)
        record = {"request_id": request_id, "session": session, "target": target, "project": str(self.root),
                  "status": "running", "owner_pid": os.getpid(),
                  "started_at": self.transport.now(), "requested_model": model,
                  "requested_effort": effort, "session_id": None, "model": None,
                  "authority": "project edits" if writable else "read only",
                  "route": ROUTE, "context_test_trigger": self.test_tokens,
                  "provider_completed": False, "context_window": None, "bootstrap_tokens": None,
                  "steer_race": None, "num_turns": None, "estimated_cost_usd": None}
        self.transport.save(folder / "request.json", {"prompt": prompt, "role": role,
            "session": session, "target": target, "project": str(self.root),
            "writable": writable, "model": model, "effort": effort, "timeout": timeout})
        self.transport.save(folder / "result.json", record)
        tools = READ_TOOLS | (WRITE_TOOLS if writable else frozenset())
        command = self.core.command("claude", None, writable, model, effort) + ["--input-format", "stream-json"]
        watch, server = ContextWatch(self.fraction, self.test_tokens), None
        begun, interrupted = time.monotonic(), False
        stream = []
        reference, early_sessions = None, []
        owned_children, snapshotted = None, False

        def emit(status, **values):
            print(json.dumps({"status": status, **values}), flush=True)

        def save():
            self.transport.save(folder / "result.json", record)

        def next_event(deadline=None, eof_ok=False):
            """The next event; None once `deadline` passes. EOF stops the run unless `eof_ok`."""
            nonlocal interrupted
            while True:
                if (folder / "cancel.json").exists() or (timeout and time.monotonic() - begun >= timeout):
                    interrupted = True
                    raise ProtocolError("Managed job cancelled or its optional timeout elapsed")
                if deadline is not None and time.monotonic() >= deadline:
                    return None
                message = server.receive()
                if message is None:
                    continue
                if message is EOF:
                    if eof_ok:
                        return EOF
                    raise ProtocolError("Claude exited before the expected result")
                if not isinstance(message, dict):
                    raise ProtocolError("Claude stream line is not a JSON object")
                # Protocol labels only; never reasoning, tool or transcript content.
                stream.append({key: message.get(key) if isinstance(message.get(key), str) else None
                               for key in ("type", "subtype")})
                return message

        def check_session(event):
            if "session_id" not in event:
                return
            if reference is None:
                early_sessions.append(event["session_id"])  # checked against the first init
            elif event["session_id"] != reference["session_id"]:
                raise ProtocolError("Received a Claude event for a different session")

        def check_hook(event):
            sid = reference["session_id"] if reference is not None else event.get("session_id")
            if not hook_ok(event, sid):
                raise ProtocolError("A hook failed, blocked, stopped continuation or belongs to another session")

        def screen(event):
            """All-phase event rules. Returns init/assistant/user/result, or None when recorded only."""
            check_session(event)
            kind = event.get("type")
            if kind == "system":
                subtype = event.get("subtype")
                if subtype == "init":
                    return "init"
                if subtype in HOOK_SUBTYPES:
                    check_hook(event)
                    return None
                if subtype in RECORDED_SUBTYPES:
                    return None
                if subtype == "compact_boundary":
                    raise ProtocolError("Native compaction occurred; no automatic continuation")
                if subtype == "permission_denied":
                    raise ProtocolError("Claude reported a permission denial; stop for Conductor reassessment")
                raise ProtocolError("Unexpected Claude system event; stop for reassessment")
            if kind == "rate_limit_event":
                return None
            if kind in {"assistant", "user", "result"}:
                return kind
            raise ProtocolError("Unexpected Claude stream event type")

        def authority(event):
            sid, cwd, mode = event.get("session_id"), event.get("cwd"), event.get("permissionMode")
            seen, chosen = event.get("tools"), event.get("model")
            if not isinstance(sid, str) or not sid:
                raise ProtocolError("Claude init has no session identity")
            if not isinstance(cwd, str) or Path(cwd).resolve() != self.root:
                raise ProtocolError("Claude init reports a different project")
            if mode != "dontAsk":
                raise ProtocolError("Claude init reports unexpected permission mode")
            if (not isinstance(seen, list) or any(not isinstance(tool, str) for tool in seen)
                    or set(seen) != tools):
                raise ProtocolError("Claude init tools differ from the requested set")
            if not isinstance(chosen, str) or not chosen:
                raise ProtocolError("Claude init has no model; no guessed window")
            return {"session_id": sid, "cwd": cwd, "permissionMode": mode,
                    "tools": frozenset(seen), "model": chosen}

        def repeated_init(event):
            # init repeats per input; a repeat may confirm but never change authority.
            if authority(event) != reference:
                raise ProtocolError("Claude init changed within the owned run; authority is unproved")

        def main_message(event):
            """The validated main-conversation message, or None for a subagent event."""
            if owner_of(event) is not None:
                return None
            message = event.get("message")
            if not isinstance(message, dict) or not isinstance(message.get("id"), str):
                raise ProtocolError("Main assistant event lacks a message identity")
            usage = message.get("usage")
            if not isinstance(usage, dict) or any(type(usage.get(key)) is not int or usage[key] < 0
                                                  for key in USAGE_KEYS):
                raise ProtocolError("Missing valid last-request context usage")
            content = message.get("content")
            if not isinstance(content, list) or any(not isinstance(block, dict) for block in content):
                raise ProtocolError("Main assistant event has malformed content")
            return message

        def reading(message, seen):
            """(message id, used tokens, whether this id is new or its usage changed)."""
            used = sum(message["usage"][key] for key in USAGE_KEYS)
            ident = message["id"]
            changed = seen.get(ident) != used
            seen[ident] = used
            return ident, used, changed

        def check_result(event):
            if event.get("subtype") != "success" or event.get("is_error") is not False:
                raise ProtocolError("Claude turn did not finish successfully")
            queued = event.get("queued_turn_count")
            if type(queued) is not int or queued != 0:
                raise ProtocolError("Claude result reports a queued extra turn")
            if event.get("permission_denials") != []:
                raise ProtocolError("Claude result reports permission denials")
            if event.get("session_id") != reference["session_id"]:
                raise ProtocolError("Claude result belongs to a different session")

        try:
            with self.transport.shutdown_signals(), open(folder / "stderr.txt", "x") as stderr:
                os.chmod(folder / "stderr.txt", 0o600)
                server = ClaudeStream(self.root, stderr, command)
                record["process_id"] = server.proc.pid
                save()
                record["process_start"] = leader_start(server.proc.pid)
                save()

                # Phase 1: bootstrap. Authority and window are proved before any work is sent.
                server.send(BOOTSTRAP)
                deadline = time.monotonic() + self.STARTUP_TIMEOUT
                seen = {}
                while True:
                    event = next_event(deadline if reference is None else None)
                    if event is None:
                        raise ProtocolError("Claude init did not arrive within the startup deadline")
                    kind = screen(event)
                    if kind == "init":
                        if reference is not None:
                            repeated_init(event)
                            continue
                        current = authority(event)
                        if any(sid != current["session_id"] for sid in early_sessions):
                            raise ProtocolError("Received a Claude event for a different session")
                        reference = current
                        record.update(session_id=current["session_id"], model=current["model"])
                        save()
                        continue
                    if kind is None:
                        continue
                    if reference is None:
                        raise ProtocolError("Claude content arrived before a validated init")
                    if kind == "user":
                        owner_of(event)
                        raise ProtocolError("Unexpected user event in the bootstrap turn")
                    if kind == "assistant":
                        message = main_message(event)
                        if message is None:
                            continue
                        if any(block.get("type") not in {"text", "thinking"} for block in message["content"]):
                            raise ProtocolError("Bootstrap turn used a tool or unexpected content; authority is unproved")
                        record["bootstrap_tokens"] = reading(message, seen)[1]
                        continue
                    check_result(event)
                    turns = event.get("num_turns")
                    if type(turns) is not int or turns != 1:
                        raise ProtocolError("Bootstrap result reports more than one turn")
                    model_usage = event.get("modelUsage")
                    entry = model_usage.get(reference["model"]) if isinstance(model_usage, dict) else None
                    window = entry.get("contextWindow") if isinstance(entry, dict) else None
                    if type(window) is not int or window <= 0:
                        raise ProtocolError("No usable context window for the initialized model; no guessed window")
                    record["context_window"] = window
                    save()
                    break

                # Phase 2: work, watched from its own usage.
                server.send(prompt)
                deadline = time.monotonic() + self.STARTUP_TIMEOUT
                work_init, seen, outstanding = False, {}, set()
                latched = sent = False
                while True:
                    event = next_event(None if work_init else deadline)
                    if event is None:
                        raise ProtocolError("Claude work init did not arrive within the startup deadline")
                    kind = screen(event)
                    if kind == "init":
                        if work_init:
                            repeated_init(event)
                        elif authority(event) != reference:
                            raise ProtocolError("Claude work init differs from the bootstrap init; authority is unproved")
                        work_init = True
                        continue
                    if kind is None:
                        continue
                    if not work_init:
                        raise ProtocolError("Claude content arrived before the work init")
                    if kind == "user":
                        if owner_of(event) is not None:
                            continue  # a subagent's own tool results; no Task tool is granted
                        message = event.get("message")
                        content = message.get("content") if isinstance(message, dict) else None
                        if not isinstance(content, list) or not content:
                            raise ProtocolError("Main user event is not a tool result; stop for reassessment")
                        for block in content:
                            ident = block.get("tool_use_id") if isinstance(block, dict) else None
                            if (not isinstance(block, dict) or block.get("type") != "tool_result"
                                    or not isinstance(ident, str) or not ident or ident not in outstanding):
                                raise ProtocolError("Main user event is not a result for an outstanding tool use")
                            outstanding.remove(ident)
                        continue
                    if kind == "assistant":
                        message = main_message(event)
                        if message is None:
                            continue  # subagent usage is not the worker's context
                        ident, used, changed = reading(message, seen)
                        if changed:
                            if watch.observe_tokens(used, window, {"message_id": ident, "used": used}):
                                emit("saving_place", context_tokens=used, threshold=watch.trigger["threshold"],
                                     test_trigger=self.test_tokens is not None)
                                latched = True
                            record.update(context_readings=watch.readings, context_trigger=watch.trigger)
                            save()
                        for block in message["content"]:
                            if block.get("type") == "tool_use":
                                if not isinstance(block.get("id"), str) or not block["id"]:
                                    raise ProtocolError("Main tool use has no identity")
                                outstanding.add(block["id"])
                        if latched and not sent and outstanding:
                            # The probe proved injection at the next tool boundary only.
                            server.send(CHECKPOINT_REASON + ". " + (checkpoint_instruction or DEFAULT_CHECKPOINT_INSTRUCTION))
                            sent = True
                            record["checkpoint_requested"] = CHECKPOINT_REASON
                            save()
                        continue
                    if latched and not sent:
                        record["steer_race"] = STEER_RACE
                    check_result(event)
                    text = event.get("result")
                    if not isinstance(text, str) or not text:
                        raise ProtocolError("Claude result has no final reply")
                    cost = event.get("total_cost_usd")
                    record.update(num_turns=event.get("num_turns"),
                                  estimated_cost_usd=cost if type(cost) in (int, float) and math.isfinite(cost) else None)
                    break
                if not watch.readings:
                    raise ProtocolError("No context readings observed; context-aware continuation is unproved")

                # Owned identities first, while the owned parent certainly exists, so the
                # receipt carries them for an inspected recovery after controller loss.
                owned_children, snapshotted = codex_roll.snapshot_owned(server, record), True
                if owned_children is None or record.get("cleanup_error"):
                    raise ProtocolError("Owned child identity unavailable; no checkpoint receipt")

                # Provisional receipt before any cleanup; never promotable by itself.
                record.update(provider_completed=True, reply=text, checkpoint_candidates=[text])
                # As persisted: JSON turns integer PID keys in owned_children into strings.
                receipt = json.loads(json.dumps({**record, "status": "running", "phase": "checkpoint_saved"}))
                self.transport.save(folder / "result.json", receipt)
                saved = self.transport.read(folder / "result.json")
                if saved != receipt or json.dumps(saved, sort_keys=True) != json.dumps(receipt, sort_keys=True):
                    raise ProtocolError("Source checkpoint failed read-back before release")

                # Drain.
                server.proc.stdin.close()
                deadline = time.monotonic() + self.DRAIN_TIMEOUT
                while True:
                    event = next_event(deadline, eof_ok=True)
                    if event is None:
                        raise ProtocolError("Claude stream did not reach EOF after input closed")
                    if event is EOF:
                        break
                    check_session(event)
                    if event.get("type") != "system" or event.get("subtype") not in DRAIN_SUBTYPES:
                        raise ProtocolError("Unexpected Claude event after the final result; no promotion")
                    if event.get("subtype") in HOOK_SUBTYPES:
                        check_hook(event)
                record["status"] = "completed"
        except BaseException as exc:
            record.update(status="cancelled" if interrupted or isinstance(exc, KeyboardInterrupt) else "failed",
                          provider_completed=False, error=str(exc))
            if not isinstance(exc, (Exception, KeyboardInterrupt)):
                raise
        finally:
            if server:
                if snapshotted:
                    codex_roll.finish_owned(self.transport, server, record, owned_children)
                else:
                    codex_roll.shutdown_owned(self.transport, server, record)
                if record.get("status") == "completed" and (record.get("owned_children_gone") is not True
                                                            or record.get("cleanup_error")):
                    record.update(status="interrupted", provider_completed=False)
            record["finished_at"] = self.transport.now()
            record.update(context_readings=watch.readings, context_trigger=watch.trigger, protocol_events=stream)
            self.transport.save(folder / "result.json", record)
            if record.get("session_id"):
                self.transport.save(self.core.session_path(session), {"target": target, "project": str(self.root),
                    "session": session, "session_id": record["session_id"], "closed": False, "last_request": request_id})
        return dict(record)
