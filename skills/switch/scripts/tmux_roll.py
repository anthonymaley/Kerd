#!/usr/bin/env python3
"""Roll the Conductor chat into a fresh session in the same tmux pane.

out       Save the roll marker under roll/owner.lock and, inside tmux, start the relaunch as a
          tmux background job. Outside tmux, print the one line to run instead.
relaunch  (run by tmux) After a short wait, check the pane still runs the recorded Claude, then
          restart the pane into `claude --model <same> -- "/kerd:switch roll in"`.
in        Claim the marker for this session, or refuse, stop and say why.
cancel    Withdraw an unclaimed marker before the relaunch fires.

Nothing is typed into a running Claude. The marker is relaunch state, never committed:
$(git rev-parse --git-path roll)/chat.json. The handoff record (the work's sketchbook) is the
project-local file; a roll grants no approval beyond the one it copies from there.
"""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import roll  # noqa: E402

MAX_AGE = 30 * 60        # a marker older than this is stale
CHAIN_WINDOW = 6 * 3600  # rolls closer together than this count as consecutive
MAX_CHAIN = 3
PACKAGE = Path(__file__).resolve().parents[3]


def git(project, *args):
    return subprocess.run(["git", *args], cwd=project, capture_output=True, text=True,
                          check=True).stdout.strip()


def roll_dir(project):
    path = Path(git(project, "rev-parse", "--git-path", "roll"))
    path = path if path.is_absolute() else Path(project) / path
    path.mkdir(parents=True, exist_ok=True)
    return path


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stamp(now):
    return datetime.fromtimestamp(now).strftime("%Y%m%dT%H%M%S")


def kerd_version():
    try:
        return json.loads((PACKAGE / ".claude-plugin/plugin.json").read_text())["version"]
    except (OSError, ValueError, KeyError):
        return "version not read"


def pid_alive(pid):
    try:
        os.kill(int(pid), 0)
    except (ProcessLookupError, ValueError, TypeError):
        return False
    except PermissionError:
        return True
    return True


def parent_of(pid):
    out = subprocess.run(["ps", "-o", "ppid=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return int(out) if out.isdigit() else None


def command_of(pid):
    return subprocess.run(["ps", "-o", "command=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()


def find_claude(start, parent=parent_of, command=command_of, depth=10):
    """Nearest ancestor whose command is the Claude CLI; None if there is none."""
    pid = start
    for _ in range(depth):
        if not pid or pid <= 1:
            return None
        words = command(pid).split()
        if words and any(Path(w).name == "claude" for w in words[:2]):
            return pid
        pid = parent(pid)
    return None


def descends_from(pid, ancestor, parent=parent_of, depth=10):
    for _ in range(depth):
        if pid == ancestor:
            return True
        if not pid or pid <= 1:
            return False
        pid = parent(pid)
    return False


class Chat:
    def __init__(self, project, transport=None):
        self.project = Path(project).resolve()
        self.local = roll_dir(self.project)
        self.marker = self.local / "chat.json"
        self.last = self.local / "chat-last.json"
        self.transport = transport or roll.connection()

    def locked(self):
        return self.transport.exclusive(self.local / "owner.lock")

    def read(self, path):
        return json.loads(path.read_text()) if path.is_file() else None

    def write(self, data):
        tmp = self.marker.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        os.replace(tmp, self.marker)
        if self.read(self.marker) != data:
            raise roll.RollError("Roll marker did not read back")

    def set_marker(self, **fields):
        """Relaunch progress. A claimed, refused or cancelled marker is left alone."""
        with self.locked():
            data = self.read(self.marker)
            if data is None:
                return None
            data.update(fields)
            self.write(data)
            return data

    # --- out ---------------------------------------------------------------------------------
    def out(self, handoff_record, next_action, approval, model, threshold_tokens,
            session=None, env=None, now=None, claude_pid=None):
        env = os.environ if env is None else env
        now = time.time() if now is None else now
        record = roll.project_file(self.project, handoff_record)
        for label, value in (("next action", next_action), ("approval boundary", approval), ("model", model)):
            if not value or not value.strip():
                raise roll.RollError(f"A roll needs its {label}")
        with self.locked():
            if (self.local / "run.json").exists():
                raise roll.RollError("A managed Roll record exists here; the chat roll does not take it over")
            if self.marker.exists():
                raise roll.RollError("An unclaimed chat roll marker already exists; inspect or cancel it")
            head, digest = git(self.project, "rev-parse", "HEAD"), sha256(record)
            last = self.read(self.last)
            chain = 1
            if last and now - last.get("at", 0) < CHAIN_WINDOW:
                if last.get("head") == head and last.get("record_sha256") == digest:
                    raise roll.RollError("No progress since the last roll (same commit, same sketchbook); not rolling again")
                chain = last.get("chain", 0) + 1
                if chain > MAX_CHAIN:
                    raise roll.RollError(f"{MAX_CHAIN} rolls in a row; stopping for the person")
            in_tmux = bool(env.get("TMUX") and env.get("TMUX_PANE"))
            data = {
                "project": str(self.project), "branch": git(self.project, "branch", "--show-current"),
                "head": head, "handoff_record": handoff_record, "handoff_sha256": digest,
                "next_action": next_action.strip(), "approval_boundary": approval.strip(),
                "from_session": session or env.get("CLAUDE_CODE_SESSION_ID"),
                "claude_pid": claude_pid, "pane": env.get("TMUX_PANE") if in_tmux else None,
                "tmux_socket": env["TMUX"].split(",")[0] if in_tmux else None,
                "model": model.strip(), "threshold_tokens": threshold_tokens, "chain": chain,
                "created_at": now, "state": "saved", "relaunch": "pending" if in_tmux else "manual",
            }
            if in_tmux and not claude_pid:
                raise roll.RollError("Could not find this session's Claude process; not restarting a pane blind")
            self.write(data)
        return data

    # --- relaunch (runs under the tmux server) ------------------------------------------------
    def relaunch(self, delay=5.0, run=subprocess.run, alive=pid_alive, parent=parent_of,
                 sleep=time.sleep, shell=None):
        sleep(delay)
        data = self.read(self.marker)
        if not data or data.get("state") != "saved" or data.get("relaunch") != "pending":
            return "withdrawn"
        tmux = ["tmux", "-S", data["tmux_socket"]]
        probe = run([*tmux, "display", "-p", "-t", data["pane"], "#{pane_id} #{pane_pid}"],
                    capture_output=True, text=True)
        words = probe.stdout.split()
        if probe.returncode != 0 or len(words) != 2 or words[0] != data["pane"]:
            self.set_marker(relaunch="refused: pane not found on the recorded tmux server")
            return "refused"
        if not descends_from(data["claude_pid"], int(words[1]), parent):
            self.set_marker(relaunch="refused: the pane no longer runs the recorded Claude")
            return "refused"
        shell = shell or os.environ.get("SHELL") or "/bin/zsh"
        fresh = (f"claude --model {shlex.quote(data['model'])} -- {shlex.quote('/kerd:switch roll in')}; "
                 f"exec {shlex.quote(shell)} -l")
        self.set_marker(relaunch="respawning")
        done = run([*tmux, "respawn-pane", "-k", "-t", data["pane"], "-c", data["project"], fresh],
                   capture_output=True, text=True)
        if done.returncode != 0:
            self.set_marker(relaunch="refused: respawn-pane failed")
            return "refused"
        for _ in range(20):
            if not alive(data["claude_pid"]):
                self.set_marker(relaunch="exited")
                return "exited"
            sleep(0.5)
        self.set_marker(relaunch="pid-alive")
        return "pid-alive"

    # --- in -------------------------------------------------------------------------------------
    def claim(self, session, model, now=None, alive=pid_alive, sleep=time.sleep, wait=15.0):
        data = self.read(self.marker)
        waited = 0.0
        while data and data.get("relaunch") in {"pending", "respawning"} and waited < wait:
            sleep(0.5)
            waited += 0.5
            data = self.read(self.marker)
        with self.locked():
            data = self.read(self.marker)
            if data is None:
                raise roll.RollError("No roll to pick up: the marker is missing or already claimed")
            now = time.time() if now is None else now
            reason = self.refusal(data, model, now, alive)
            if reason:
                data.update(state="refused", refusal=reason)
                target = self.local / f"chat-roll-refused-{stamp(now)}.json"
                target.write_text(json.dumps(data, indent=2))
                self.marker.unlink()
                raise roll.RollError(reason)
            safe = "".join(c for c in (session or "unknown") if c.isalnum() or c == "-")
            target = self.local / f"chat-roll-claimed-{safe}.json"
            os.rename(self.marker, target)
            data.update(state="claimed", claimed_by=session, claimed_at=now)
            target.write_text(json.dumps(data, indent=2))
            (self.last).write_text(json.dumps({"head": data["head"], "record_sha256": data["handoff_sha256"],
                                               "chain": data["chain"], "at": now}))
        return data

    def refusal(self, data, model, now, alive):
        if now - data.get("created_at", 0) > MAX_AGE:
            return "The roll marker is older than 30 minutes"
        if data.get("project") != str(self.project):
            return "The roll marker belongs to another project"
        if data.get("branch") != git(self.project, "branch", "--show-current"):
            return "The branch changed since the roll was saved"
        if data.get("head") != git(self.project, "rev-parse", "HEAD"):
            return "The commit changed since the roll was saved"
        try:
            if sha256(roll.project_file(self.project, data["handoff_record"])) != data.get("handoff_sha256"):
                return "The sketchbook changed since the roll was saved"
        except (roll.RollError, OSError):
            return "The sketchbook named in the roll is missing"
        if data.get("model") != model:
            return f"This session runs {model}, the roll was saved on {data.get('model')}"
        state = data.get("relaunch")
        if state == "manual":
            if data.get("claude_pid") and alive(data["claude_pid"]):
                return "The previous Claude session is still running; close it first"
        elif state != "exited":
            return f"The relaunch did not confirm the old session ended ({state})"
        return None

    def cancel(self, now=None):
        now = time.time() if now is None else now
        with self.locked():
            data = self.read(self.marker)
            if data is None:
                raise roll.RollError("No unclaimed roll to cancel")
            data.update(state="cancelled")
            (self.local / f"chat-roll-cancelled-{stamp(now)}.json").write_text(json.dumps(data, indent=2))
            self.marker.unlink()
        return data


def start_relaunch(project, data, run=subprocess.run):
    """Hand the relaunch to the tmux server so it outlives this Claude. No shell variables."""
    job = f"{shlex.quote(sys.executable)} {shlex.quote(str(Path(__file__).resolve()))} relaunch --project {shlex.quote(str(project))}"
    return run(["tmux", "-S", data["tmux_socket"], "run-shell", "-b", job], capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    out = sub.add_parser("out")
    out.add_argument("--handoff-record", required=True, help="Project-relative sketchbook, written last")
    out.add_argument("--next-action", required=True)
    out.add_argument("--approval", required=True, help="The approval boundary, verbatim from the sketchbook")
    out.add_argument("--model", required=True, help="This session's model ID, e.g. claude-opus-5-5[1m]")
    out.add_argument("--threshold-tokens", type=int, required=True)
    sub.add_parser("relaunch")
    inn = sub.add_parser("in")
    inn.add_argument("--model", required=True, help="This session's model ID")
    sub.add_parser("cancel")
    args = parser.parse_args()
    try:
        chat = Chat(args.project)
        if args.command == "out":
            data = chat.out(args.handoff_record, args.next_action, args.approval, args.model,
                            args.threshold_tokens, claude_pid=find_claude(os.getppid()))
            if data["relaunch"] == "manual":
                print("Saved. This terminal is not tmux, so it cannot restart itself. Close this session, then run:")
                print(f"  claude --model {shlex.quote(data['model'])} -- \"/kerd:switch roll in\"")
                return 0
            started = start_relaunch(chat.project, data)
            if started.returncode != 0:
                chat.cancel()
                raise roll.RollError("tmux did not accept the relaunch job; the roll is cancelled")
            print(f"Rolling: saved at {data['next_action']}; restarting this pane.")
        elif args.command == "relaunch":
            print(chat.relaunch())
        elif args.command == "in":
            data = chat.claim(os.environ.get("CLAUDE_CODE_SESSION_ID"), args.model)
            print(json.dumps({k: data[k] for k in ("handoff_record", "next_action", "approval_boundary", "chain")}, indent=2))
            print(f"Rolled: Kerd {kerd_version()}, continuing {data['next_action']}")
        else:
            chat.cancel()
            print("Roll cancelled; the marker is kept as chat-roll-cancelled-….json")
    except (roll.RollError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Roll stopped: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
