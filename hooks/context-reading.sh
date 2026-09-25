#!/bin/bash
# Kerd context reading (UserPromptSubmit and PostToolUse)
# Tells the session how many tokens its last request carried, read from its
# own transcript: the last main-conversation reply's input + cache tokens, the
# formula Claude Code's status line uses for context usage. It reports a
# token count only: these hook inputs carry no window size, so no capacity or
# percentage is claimed.
#   $1 = prompt : each prompt once an earlier main-conversation reply has
#                 usage to count, plain-text stdout (added to context);
#                 silent before the first reply of a fresh conversation.
#   $1 = tool   : after tool calls, at most every 5 minutes or 50,000 tokens,
#                 as PostToolUse additionalContext; the transcript is read at
#                 most once a minute.
# Read-only on the transcript. Writes one small throttle file per session
# under $TMPDIR; if it cannot, it stays silent rather than repeat itself. Also
# records the event's permission mode beside it (<session>.mode) for the chat roll.
# Silent on any failure: a hook must go quiet, never crash.
set -uo pipefail

mode="${1:-prompt}"
command -v python3 >/dev/null 2>&1 || exit 0

# The hook event arrives on stdin and goes straight to Python on stdin: a large
# tool event must never pass through the environment or an argument list.
read -r -d '' KERD_PY <<'PY'
import json, os, sys, time

mode = sys.argv[1]
try:
    hook = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if not isinstance(hook, dict) or hook.get("agent_id"):   # subagents: stay quiet
    sys.exit(0)
path, sid = hook.get("transcript_path"), hook.get("session_id")
if not path or not sid or not os.path.isfile(path):
    sys.exit(0)

state_dir = os.path.join(os.environ.get("TMPDIR") or "/tmp", "kerd-context")
state = os.path.join(state_dir, "".join(c for c in sid if c.isalnum() or c == "-"))
now = int(time.time())
# The current permission mode, as the host reports it on this event, for Switch's chat roll:
# it restarts the session with the mode in force when it rolled. Written on every event,
# unthrottled; a failure only means the roll refuses.
if hook.get("permission_mode"):
    try:
        import tempfile
        os.makedirs(state_dir, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=state_dir, prefix=".mode-")   # one per hook: they can run at once
        with os.fdopen(fd, "w") as f:
            json.dump({"mode": hook["permission_mode"], "at": time.time()}, f)
        os.replace(tmp, state + ".mode")
    except Exception:
        pass
reported_at, reported_tokens, scanned_at = 0, 0, 0
try:
    fields = [int(x) for x in open(state).read().split()[:3]]
    reported_at, reported_tokens = fields[0], fields[1]
    scanned_at = fields[2] if len(fields) > 2 else fields[0]
except Exception:
    pass
if mode == "tool" and now - scanned_at < 60:    # read the transcript at most once a minute
    sys.exit(0)

def last_reading(path):
    # The last reply sits near the end; widen the tail only if one huge
    # trailing record hides it.
    with open(path, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        for span in (4_000_000, 32_000_000):
            f.seek(max(0, size - span))
            for raw in reversed(f.read().splitlines()):
                try:
                    entry = json.loads(raw)
                except Exception:
                    continue
                if entry.get("type") != "assistant" or entry.get("isSidechain"):
                    continue
                usage = (entry.get("message") or {}).get("usage")
                if usage:
                    return sum(int(usage.get(k) or 0) for k in
                               ("input_tokens", "cache_read_input_tokens",
                                "cache_creation_input_tokens"))
            if span >= size:
                break
    return None

tokens = last_reading(path)
if not tokens:
    sys.exit(0)

report = mode != "tool" or now - reported_at >= 300 or tokens - reported_tokens >= 50_000
if report:
    reported_at, reported_tokens = now, tokens
try:
    os.makedirs(state_dir, exist_ok=True)
    with open(state, "w") as f:
        f.write(f"{reported_at} {reported_tokens} {now}\n")
except Exception:
    if mode == "tool":      # no throttle memory: stay silent rather than repeat
        sys.exit(0)
if not report:
    sys.exit(0)

line = (f"Context: {tokens:,} tokens in the last request "
        f"(Kerd reading, {time.strftime('%H:%M')}).")
if mode == "tool":
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PostToolUse", "additionalContext": line}}))
else:
    print(line)
PY

python3 -c "$KERD_PY" "$mode" 2>/dev/null || true
exit 0
