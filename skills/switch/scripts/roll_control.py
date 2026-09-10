"""A live command channel for the existing Roll owner. No inbox or service."""
import json
from pathlib import Path
import queue
import sys
import threading

import handoff
from managed_to import ManagedTo


class ControlEnded(RuntimeError):
    pass


class LiveControl:
    def __init__(self, stream=None, emit=None):
        self.stream = stream if stream is not None else sys.stdin
        self.emit = emit or self._emit
        self.commands = queue.Queue()
        self.pending = None
        self.reader = None
        self.released_result = None
        self.checkpoint_requested = threading.Event()
        self.stopping = threading.Event()

    @staticmethod
    def _emit(value):
        sys.stdout.write(json.dumps({"control": True, **value}) + "\n")
        sys.stdout.flush()

    def start(self):
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()
        self.emit({"status": "connected", "note": "Commands apply at a safe worker boundary"})

    def _read(self):
        try:
            for line in self.stream:
                try:
                    command = json.loads(line)
                    if not isinstance(command, dict) or command.get("action") not in {"to", "retry", "abandon", "status"}:
                        raise ValueError("Expected to, retry, abandon or status")
                    allowed = {"action", "branch", "destination", "message", "files", "pickup"} if command["action"] == "to" else {"action"}
                    if set(command) - allowed:
                        raise ValueError("Unexpected command fields; no authority inferred")
                    if command["action"] == "to":
                        if command.get("pickup", "local") not in {"local", "on_destination"}:
                            raise ValueError("Pickup must be local or on_destination")
                        for key in ("branch", "destination", "message"):
                            if not isinstance(command.get(key), str) or not command[key].strip():
                                raise ValueError("Handoff needs branch, destination and message")
                        if command.get("pickup") == "on_destination" and not Path(command["destination"]).is_absolute():
                            raise ValueError("Other-device pickup needs its explicit absolute project path")
                        if (not isinstance(command.get("files"), list) or not command["files"]
                                or any(not isinstance(value, str) for value in command["files"])):
                            raise ValueError("Handoff needs an explicit file list")
                    if command["action"] == "abandon":
                        self.stopping.set()
                    self.commands.put(command)
                    if command["action"] in {"to", "abandon"}:
                        self.checkpoint_requested.set()
                    self.emit({"status": "received", "action": command["action"]})
                except (ValueError, TypeError) as exc:
                    self.emit({"status": "rejected", "error": str(exc)})
        finally:
            self.stopping.set()
            self.commands.put({"action": "disconnected"})
            self.checkpoint_requested.set()

    def _next(self, wait=False):
        try:
            return self.commands.get() if wait else self.commands.get_nowait()
        except queue.Empty:
            return None

    def boundary(self):
        self.ensure_connected()
        while (command := self._next()) is not None:
            action = command["action"]
            if action in {"abandon", "disconnected"}:
                raise ControlEnded("Caller abandoned the managed run" if action == "abandon" else "Control channel closed")
            if action == "to":
                if self.pending is None:
                    self.pending = command
                    self.emit({"status": "handoff_pending", "note": "Actual owned worker reached its boundary"})
                else:
                    self.emit({"status": "rejected", "error": "A handoff is already pending"})
            elif action == "status":
                self.emit({"status": "held", "handoff_pending": self.pending is not None})
            else:
                self.emit({"status": "rejected", "error": "No failed save to retry"})
        return self.pending

    def ensure_connected(self):
        if self.stopping.is_set():
            raise ControlEnded("Caller abandoned or disconnected from this managed run")

    def wait_for_recovery(self, error, retry=True):
        self.emit({"status": "source_held", "error": str(error), "retry_available": retry,
                   "note": "No destination started; Conductor must inspect before retry or abandon"})
        while True:
            self.ensure_connected()
            command = self._next(wait=True)
            action = command["action"]
            if action in {"abandon", "disconnected"}:
                raise ControlEnded("Caller abandoned the managed run" if action == "abandon" else "Control channel closed")
            if action == "retry" and retry:
                return
            if action == "status":
                self.emit({"status": "source_held", "error": str(error), "retry_available": retry})
            else:
                self.emit({"status": "rejected", "error": "Inspect this held source; only the stated recovery is available"})

    def handoff(self, roller, previous, agreement_bytes, record):
        command = self.pending
        if command is None:
            return None
        elsewhere = command.get("pickup") == "on_destination"
        # A foreign path belongs to that device; do not resolve or probe it here.
        dest = Path(command["destination"]) if elsewhere else Path(command["destination"]).resolve()
        transfer = None
        while True:
            try:
                self.ensure_connected()
                # Refuse bad targets before saving or releasing the source. No clone,
                # checkout selection or remote identity is inferred from a task name.
                if not elsewhere:
                    if dest == roller.root or handoff.root_for(dest) != dest:
                        raise handoff.HandoffError("Destination must be a separate existing repository root")
                    handoff.require_branch(dest, command["branch"])
                    if handoff.git(dest, "status", "--porcelain"):
                        raise handoff.HandoffError("Destination has local changes")
                    if handoff.git(dest, "remote", "get-url", "origin") != handoff.git(roller.root, "remote", "get-url", "origin"):
                        raise handoff.HandoffError("Source and destination origin differ; reconcile before handoff")
                if transfer is None:
                    transfer = ManagedTo(roller.bridge, command["branch"], str(roller.place.relative_to(roller.root)),
                        previous, command["files"], command["message"],
                        {str(roller.agreement.relative_to(roller.root)): agreement_bytes},
                        cancelled=self.stopping.is_set, allow_unchanged=True)
                self.emit({"status": "saving"})
                receipt = transfer.save_and_release()
                self.released_result = transfer.result
                record["handoff"] = {"destination": str(dest), "receipt": receipt}
                roller.transport.save(roller.ledger, record)
                self.emit({"status": "source_released", "commit": receipt["commit"]})
                break
            except Exception as exc:
                if isinstance(exc, ControlEnded):
                    raise
                # Once release is uncertain, this is not another save retry.
                can_retry = (roller.bridge._held is not None
                             and roller.bridge.held_result().get("phase") == "held")
                if can_retry:
                    try:
                        roller.bridge.inspect_held()
                    except Exception:
                        can_retry = False
                record.setdefault("handoff_failures", []).append({"at": roller.transport.now(), "error": str(exc)})
                record.update(status="uncertain", next_action="Inspect the failed handoff; source ownership retained")
                roller.transport.save(roller.ledger, record)
                self.wait_for_recovery(exc, retry=can_retry)
        self.ensure_connected()
        if elsewhere:
            self.emit({"status": "awaiting_destination", "commit": receipt["commit"],
                       "note": "Source released; destination has not been inspected, prepared or started"})
            return {"destination": str(dest), "receipt": receipt, "pickup": "on_destination",
                    "origin": handoff.git(roller.root, "remote", "get-url", "origin"),
                    "agreement": str(roller.agreement.relative_to(roller.root)),
                    "place": str(roller.place.relative_to(roller.root))}
        try:
            packet = transfer.prepare_destination(dest, files=[str(roller.agreement.relative_to(roller.root))])
        except Exception as exc:
            raise RuntimeError(f"Source released, but destination pickup failed; no destination started: {exc}") from exc
        self.ensure_connected()
        self.emit({"status": "destination_prepared", "commit": packet["commit"]})
        return {"destination": str(dest), "receipt": receipt, "packet": packet}
