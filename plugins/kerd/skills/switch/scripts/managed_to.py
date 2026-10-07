"""Synchronous managed-source handoff, not arbitrary interactive-session takeover.

The caller owns the bridge and must remain alive through recovery or explicitly
abandon. Save failures return to that caller without closing the held source.
"""
import handoff
import roll
import json
import subprocess


class ManagedTo:
    def __init__(self, bridge, branch, place, previous, files, message, protected=None,
                 cancelled=None, allow_unchanged=False):
        self.bridge, self.root = bridge, bridge.root
        self.branch, self.place, self.previous = branch, place, previous
        self.files, self.message = list(files), message
        self.protected = dict(protected or {})
        self.receipt = None
        self.error = None
        self.result = None
        self.cancelled = cancelled or (lambda: False)
        self.allow_unchanged = allow_unchanged
        if place not in self.files or place in self.protected:
            raise ValueError("Saved place must be an assigned output, not a protected input")
        handoff.relative_file(self.root, place)

    def save_and_release(self):
        """Retry only after the caller has diagnosed and repaired the failed save.

        No implicit retries, new model turn, source shutdown on save failure, or
        destination dispatch. Cancelling is an explicit abandonment, not success.
        """
        if self.receipt is not None:
            raise handoff.HandoffError("This handoff is already released")
        try:
            result = self.bridge.held_result()
            if (result.get("status") != "running" or result.get("phase") != "held"
                    or not result.get("provider_completed") or self.bridge.held_cancelled() or self.cancelled()):
                raise handoff.HandoffError("Source is not available for handoff; inspect or explicitly abandon")
            self.bridge.inspect_held()
            state = self.previous
            for candidate in result.get("checkpoint_candidates") or [result["reply"]]:
                parsed = roll.parse_reply(candidate)
                if parsed != state:
                    state = roll.check_state(parsed, self.root, state)
            if state == self.previous and not self.allow_unchanged:
                raise handoff.HandoffError("No changed working place to hand off")
            if state["status"] != "continue":
                raise handoff.HandoffError("Managed To requires a valid unfinished working place")
            for name, content in self.protected.items():
                path = self.root / handoff.relative_file(self.root, name)
                if path.read_bytes() != content:
                    raise handoff.HandoffError("Protected input changed; no source release")
            self.bridge.transport.save(self.root / handoff.relative_file(self.root, self.place), state)
            def verify_commit(commit):
                def blob(name):
                    path = handoff.relative_file(self.root, name)
                    return subprocess.check_output(["git", "-C", str(self.root), "show", f"{commit}:{path}"], stderr=subprocess.PIPE)
                stored = roll.check_state(json.loads(blob(self.place)), self.root)
                if stored != state or any(blob(name) != value for name, value in self.protected.items()):
                    raise handoff.HandoffError("Committed handoff or agreement differs from validated work; source retained")
                for name in state["evidence"]:
                    blob(name)
                if self.cancelled() or self.bridge.held_cancelled():
                    raise handoff.HandoffError("Cancellation requested before push; source not released")
            saved = handoff.publish(self.root, self.branch, self.files, self.message, push=True, verify_commit=verify_commit)
            if saved.get("status") != "saved_to_remote":
                raise handoff.HandoffError("Remote save is not verified")
            self.bridge.inspect_held()
            if self.bridge.held_cancelled() or self.cancelled():
                raise handoff.HandoffError("Cancellation requested; saved but source not released")
            released = self.bridge.release_held()
            if (released.get("status") != "completed" or released.get("cleanup_error")
                    or released.get("owned_children_gone") is not True or not roll.group_gone(released)):
                raise handoff.HandoffError("Source shutdown is uncertain; destination must not start")
            self.result = released
            self.receipt = dict(saved, source_session_exited=True,
                note="Remote save and owned-source exit verified; destination execution is a separate step")
            self.error = None
            return dict(self.receipt)
        except Exception as exc:
            self.error = str(exc)
            raise

    def prepare_destination(self, root, files=(), sections=()):
        if self.cancelled():
            raise handoff.HandoffError("Caller cancelled; no destination preparation")
        if self.receipt is None or self.result is None or not roll.group_gone(self.result):
            raise handoff.HandoffError("No verified save and source release; destination must not start")
        if root.resolve() == self.root.resolve():
            raise handoff.HandoffError("Destination must be a separate checkout")
        packet = handoff.prepare(root, self.branch, self.place, files, sections, sync=True,
                                 expected_commit=self.receipt["commit"])
        if self.cancelled():
            raise handoff.HandoffError("Caller cancelled during pickup; no destination execution")
        if packet["commit"] != self.receipt["commit"]:
            raise handoff.HandoffError("Destination revision differs from the saved handoff")
        return packet
