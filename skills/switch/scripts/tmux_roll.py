#!/usr/bin/env python3
"""Roll a Claude Conductor chat into a fresh session in the same tmux pane.

out       Save the roll note under roll/owner.lock and, inside tmux, hand the relaunch to the
          tmux server. Outside tmux, print the one line to run instead.
relaunch  (run by tmux) After a short wait, re-check everything under the lock, commit to the
          restart, then restart the recorded pane into `claude --model <same> -- "/kerd:switch roll in"`.
in        Claim the note for this session, or refuse, stop and say why.
cancel    Withdraw the note; refused once the restart has begun.

Nothing is typed into a running Claude. The note is relaunch state, never committed:
$(git rev-parse --git-path roll)/chat.json. The handoff record (the work's sketchbook) is the
project-local file; a roll grants no approval beyond the one it copies from there. Claude only:
a session started with launch options other than --model/--effort, or with Claude or Anthropic
environment settings the tmux server does not share, is not rolled automatically.
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
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent))
import roll  # noqa: E402

MAX_AGE = 30 * 60        # a note older than this is stale
CHAIN_WINDOW = 6 * 3600  # rolls closer together than this count as consecutive
MAX_CHAIN = 3
# Set by Claude Code for its own children, not by the person; a restart sets them afresh.
PER_PROCESS = {"CLAUDECODE", "CLAUDE_PID", "CLAUDE_EFFORT", "CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_ROOT",
               "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_EXECPATH", "CLAUDE_CODE_SESSION_ID",
               "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_SSE_PORT",
               "CLAUDE_CODE_MESSAGING_SOCKET", "CLAUDE_CODE_MESSAGING_TOKEN"}
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


def ps(field, pid):
    return subprocess.run(["ps", "-o", f"{field}=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()


def exists(pid):
    """True, False, or None when it cannot be told."""
    try:
        os.kill(int(pid), 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except (ValueError, TypeError, OSError):
        return None
    return True


def parent_of(pid):
    out = ps("ppid", pid)
    return int(out) if out.isdigit() else None


def command_of(pid):
    return ps("command", pid)


def start_of(pid):
    """Process start time, or None when it cannot be read; with the PID it identifies a
    process across PID reuse."""
    done = subprocess.run(["ps", "-o", "lstart=", "-p", str(pid)], capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 and done.stdout.strip() else None


def identity(pid, start=start_of):
    begun = start(pid) if pid else None
    return {"pid": pid, "start": begun} if begun else None


def process_state(ident, start=start_of, present=exists):
    """'alive' (the exact recorded process), 'gone' (absent, or its PID reused), or 'unknown'."""
    if not ident or not ident.get("start"):
        return "unknown"
    there = present(ident["pid"])
    if there is False:
        return "gone"
    if there is None:
        return "unknown"
    begun = start(ident["pid"])
    if begun is None:
        return "unknown"
    return "alive" if begun == ident["start"] else "gone"


def find_claude(begin, parent=parent_of, command=command_of, depth=10):
    """Nearest ancestor whose command is the Claude CLI; None if there is none."""
    pid = begin
    for _ in range(depth):
        if not pid or pid <= 1:
            return None
        words = command(pid).split()
        if words and any(Path(w).name == "claude" for w in words[:2]):
            return pid
        pid = parent(pid)
    return None


def launch_restriction(command):
    """The first launch option other than --model/--effort, which a restart would drop; None
    if none. `ps` loses argument boundaries, so every word is scanned, `--` included: a prompt
    word that looks like an option refuses too, which only means rolling by hand."""
    words = command.split()
    at = next((i for i, w in enumerate(words[:2]) if Path(w).name == "claude"), None)
    if at is None:
        return "not a claude command"
    rest = iter(words[at + 1:])
    for word in rest:
        if word in {"--model", "--effort"}:
            next(rest, None)
        elif word == "--" or word.startswith(("--model=", "--effort=")):
            continue
        elif word.startswith("-"):
            return word
    return None


def env_restriction(session_env, tmux_env):
    """Claude or Anthropic settings in this session that the tmux server's environment does not
    carry identically; the restarted pane would lose them. Names only, never values."""
    return sorted(k for k, v in session_env.items()
                  if (k.startswith(("CLAUDE", "ANTHROPIC")) and k not in PER_PROCESS
                      and tmux_env.get(k) != v))


def tmux_global_env(socket, run=subprocess.run):
    done = run(["tmux", "-S", socket, "show-environment", "-g"], capture_output=True, text=True)
    if done.returncode != 0:
        return None
    pairs = (line.split("=", 1) for line in done.stdout.splitlines() if "=" in line and not line.startswith("-"))
    return {k: v for k, v in pairs}


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
            raise roll.RollError("Roll note did not read back")

    def update(self, roll_id, **fields):
        """Change this exact roll's note; None if it was cancelled, claimed or replaced."""
        with self.locked():
            data = self.read(self.marker)
            if not data or data.get("roll_id") != roll_id:
                return None
            data.update(fields)
            self.write(data)
            return data

    def checkpoint_problem(self, data, now):
        """Why the saved place no longer matches the checkout; None when it does."""
        if now - data.get("created_at", 0) > MAX_AGE:
            return "The roll note is older than 30 minutes"
        if data.get("project") != str(self.project):
            return "The roll note belongs to another project"
        if data.get("branch") != git(self.project, "branch", "--show-current"):
            return "The branch changed since the roll was saved"
        if data.get("head") != git(self.project, "rev-parse", "HEAD"):
            return "The commit changed since the roll was saved"
        try:
            if sha256(roll.project_file(self.project, data["handoff_record"])) != data.get("handoff_sha256"):
                return "The sketchbook changed since the roll was saved"
        except (roll.RollError, OSError, KeyError):
            return "The sketchbook named in the roll is missing"
        return None

    # --- out ---------------------------------------------------------------------------------
    def out(self, handoff_record, next_action, approval, model, threshold_tokens, claude,
            claude_command, session=None, env=None, now=None, tmux_env=None):
        """claude is the source session's process identity {pid, start}; required everywhere."""
        env = os.environ if env is None else env
        now = time.time() if now is None else now
        record = roll.project_file(self.project, handoff_record)
        for label, value in (("next action", next_action), ("approval boundary", approval), ("model", model)):
            if not value or not value.strip():
                raise roll.RollError(f"A roll needs its {label}")
        session = session or env.get("CLAUDE_CODE_SESSION_ID")
        if not session:
            raise roll.RollError("This session's ID is not available; not rolling")
        if not claude:
            raise roll.RollError("Could not identify this session's Claude process; not rolling")
        restriction = launch_restriction(claude_command or "")
        if restriction:
            raise roll.RollError(f"This session was started with {restriction}, which a restart would drop; "
                                 "roll by hand (Switch Out, then a fresh session)")
        in_tmux = bool(env.get("TMUX") and env.get("TMUX_PANE"))
        if in_tmux:
            if tmux_env is None:
                raise roll.RollError("Could not read the tmux server's environment; not restarting blind")
            names = env_restriction(env, tmux_env)
            if names:
                raise roll.RollError(f"This session has {', '.join(names)} set, which the restarted pane "
                                     "would not carry; roll by hand (Switch Out, then a fresh session)")
        with self.locked():
            if (self.local / "run.json").exists():
                raise roll.RollError("A managed Roll record exists here; the chat roll does not take it over")
            if self.marker.exists():
                raise roll.RollError("A roll note already exists; inspect or cancel it")
            head, digest = git(self.project, "rev-parse", "HEAD"), sha256(record)
            last = self.read(self.last)
            chain = 1
            if last and now - last.get("at", 0) < CHAIN_WINDOW:
                if last.get("head") == head and last.get("record_sha256") == digest:
                    raise roll.RollError("No progress since the last roll (same commit, same sketchbook); not rolling again")
                chain = last.get("chain", 0) + 1
                if chain > MAX_CHAIN:
                    raise roll.RollError(f"{MAX_CHAIN} rolls in a row already; stopping for the person")
            data = {
                "roll_id": uuid.uuid4().hex,
                "project": str(self.project), "branch": git(self.project, "branch", "--show-current"),
                "head": head, "handoff_record": handoff_record, "handoff_sha256": digest,
                "next_action": next_action.strip(), "approval_boundary": approval.strip(),
                "from_session": session, "claude": claude,
                "pane": env.get("TMUX_PANE") if in_tmux else None,
                "tmux_socket": env["TMUX"].split(",")[0] if in_tmux else None,
                "model": model.strip(), "effort": env.get("CLAUDE_EFFORT") or None,
                "threshold_tokens": threshold_tokens, "chain": chain,
                "created_at": now, "state": "saved", "relaunch": "pending" if in_tmux else "manual",
            }
            self.write(data)
        return data

    # --- relaunch (runs under the tmux server) ------------------------------------------------
    def relaunch(self, roll_id, delay=5.0, run=subprocess.run, start=start_of, parent=parent_of,
                 sleep=time.sleep, shell=None, now=None, present=exists):
        sleep(delay)
        with self.locked():
            data = self.read(self.marker)
            if (not data or data.get("roll_id") != roll_id or data.get("state") != "saved"
                    or data.get("relaunch") != "pending"):
                return "withdrawn"
            problem = self.checkpoint_problem(data, time.time() if now is None else now)
            if not problem:
                state = process_state(data["claude"], start, present)
                if state != "alive":
                    problem = f"the recorded Claude is {state}, not running"
            if not problem:
                tmux = ["tmux", "-S", data["tmux_socket"]]
                probe = run([*tmux, "display", "-p", "-t", data["pane"], "#{pane_id} #{pane_pid}"],
                            capture_output=True, text=True)
                words = probe.stdout.split()
                if probe.returncode != 0 or len(words) != 2 or words[0] != data["pane"]:
                    problem = "the pane is not on the recorded tmux server"
                elif not descends_from(data["claude"]["pid"], int(words[1]), parent):
                    problem = "the pane no longer runs the recorded Claude"
            if problem:
                data["relaunch"] = f"refused: {problem}"
                self.write(data)
                return "refused"
            data["relaunch"] = "respawning"   # the point of no return: cancel now reports too late
            self.write(data)
        shell = shell or os.environ.get("SHELL") or "/bin/zsh"
        effort = f"--effort {shlex.quote(data['effort'])} " if data.get("effort") else ""
        fresh = (f"claude --model {shlex.quote(data['model'])} {effort}-- {shlex.quote('/kerd:switch roll in')}; "
                 f"exec {shlex.quote(shell)} -l")
        done = run([*tmux, "respawn-pane", "-k", "-t", data["pane"], "-c", data["project"], fresh],
                   capture_output=True, text=True)
        if done.returncode != 0:
            self.update(roll_id, relaunch="refused: respawn-pane failed")
            return "refused"
        state = "unknown"
        for _ in range(20):
            state = process_state(data["claude"], start, present)
            if state == "gone":
                self.update(roll_id, relaunch="exited")
                return "exited"
            sleep(0.5)
        outcome = "pid-alive" if state == "alive" else "exit-unknown"
        self.update(roll_id, relaunch=outcome)
        return outcome

    # --- in -------------------------------------------------------------------------------------
    def claim(self, session, model, now=None, start=start_of, sleep=time.sleep, wait=15.0, present=exists):
        if not session:
            raise roll.RollError("This session's ID is not available; cannot claim the roll")
        data = self.read(self.marker)
        waited = 0.0
        while data and data.get("relaunch") in {"pending", "respawning"} and waited < wait:
            sleep(0.5)
            waited += 0.5
            data = self.read(self.marker)
        with self.locked():
            data = self.read(self.marker)
            if data is None:
                raise roll.RollError("No roll to pick up: the note is missing or already claimed")
            if data.get("relaunch") in {"pending", "respawning"}:
                raise roll.RollError("The restart is still in progress; the note stays until it resolves")
            now = time.time() if now is None else now
            reason = self.refusal(data, model, now, start, present)
            if reason:
                data.update(state="refused", refusal=reason)
                (self.local / f"chat-roll-refused-{stamp(now)}.json").write_text(json.dumps(data, indent=2))
                self.marker.unlink()
                raise roll.RollError(reason)
            safe = "".join(c for c in session if c.isalnum() or c == "-")
            target = self.local / f"chat-roll-claimed-{safe}.json"
            os.rename(self.marker, target)
            data.update(state="claimed", claimed_by=session, claimed_at=now)
            target.write_text(json.dumps(data, indent=2))
            self.last.write_text(json.dumps({"head": data["head"], "record_sha256": data["handoff_sha256"],
                                             "chain": data["chain"], "at": now}))
        return data

    def refusal(self, data, model, now, start, present):
        problem = self.checkpoint_problem(data, now)
        if problem:
            return problem
        if data.get("model") != model:
            return f"This session runs {model}, the roll was saved on {data.get('model')}"
        state = data.get("relaunch")
        if state == "manual":
            state = process_state(data.get("claude"), start, present)
            if state == "alive":
                return "The previous Claude session is still running; close it first"
            if state != "gone":
                return "The previous session cannot be shown to be closed"
        elif state != "exited":
            return f"The relaunch did not confirm the old session ended ({state})"
        return None

    def cancel(self, now=None):
        now = time.time() if now is None else now
        with self.locked():
            data = self.read(self.marker)
            if data is None:
                raise roll.RollError("No unclaimed roll to cancel")
            if data.get("relaunch") in {"respawning", "exited", "pid-alive", "exit-unknown"}:
                raise roll.RollError("Too late to cancel: the pane restart has already begun")
            data.update(state="cancelled")
            (self.local / f"chat-roll-cancelled-{stamp(now)}.json").write_text(json.dumps(data, indent=2))
            self.marker.unlink()
        return data


def relaunch_command(project, roll_id):
    """The job tmux runs. No shell variables: Claude's permission check stops them."""
    return (f"{shlex.quote(sys.executable)} {shlex.quote(str(Path(__file__).resolve()))} "
            f"--project {shlex.quote(str(project))} relaunch --roll-id {shlex.quote(roll_id)}")


def start_relaunch(project, data, run=subprocess.run):
    """Hand the relaunch to the tmux server so it outlives this Claude."""
    return run(["tmux", "-S", data["tmux_socket"], "run-shell", "-b", relaunch_command(project, data["roll_id"])],
               capture_output=True, text=True)


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    out = sub.add_parser("out")
    out.add_argument("--handoff-record", required=True, help="Project-relative sketchbook, written last")
    out.add_argument("--next-action", required=True)
    out.add_argument("--approval", required=True, help="The approval boundary, verbatim from the sketchbook")
    out.add_argument("--model", required=True, help="This session's model ID, e.g. claude-opus-5-5[1m]")
    out.add_argument("--threshold-tokens", type=int, required=True)
    again = sub.add_parser("relaunch")
    again.add_argument("--roll-id", required=True)
    inn = sub.add_parser("in")
    inn.add_argument("--model", required=True, help="This session's model ID")
    sub.add_parser("cancel")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        chat = Chat(args.project)
        if args.command == "out":
            env_pid = os.environ.get("CLAUDE_PID", "")
            pid = int(env_pid) if env_pid.isdigit() else find_claude(os.getppid())
            socket = os.environ.get("TMUX", "").split(",")[0]
            data = chat.out(args.handoff_record, args.next_action, args.approval, args.model,
                            args.threshold_tokens, identity(pid), command_of(pid) if pid else "",
                            tmux_env=tmux_global_env(socket) if socket else None)
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
            print(chat.relaunch(args.roll_id))
        elif args.command == "in":
            data = chat.claim(os.environ.get("CLAUDE_CODE_SESSION_ID"), args.model)
            print(json.dumps({k: data[k] for k in ("handoff_record", "next_action", "approval_boundary", "chain")}, indent=2))
            print(f"Rolled: Kerd {kerd_version()}, continuing {data['next_action']}")
        else:
            chat.cancel()
            print("Roll cancelled; the note is kept as chat-roll-cancelled-….json")
    except (roll.RollError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Roll stopped: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
