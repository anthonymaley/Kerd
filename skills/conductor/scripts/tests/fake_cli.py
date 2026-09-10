"""Deterministic subprocess fixture. Never calls a model."""
import json
import subprocess
import sys
import time
import uuid

provider = sys.argv[1]
args = sys.argv[2:]
prompt = sys.stdin.read()
if "DETACHED" in prompt:
    child = subprocess.Popen([sys.executable, "-c", "import os,time,json,pathlib; pathlib.Path('fixture-detached.json').write_text(json.dumps({'group':os.getpgrp()})); print('detached-ready',flush=True); time.sleep(30)"], start_new_session=True)
    time.sleep(30)
if "DESCENDANT" in prompt:
    child = subprocess.Popen([sys.executable, "-c", "import os,signal,time,json,pathlib; signal.signal(signal.SIGTERM, signal.SIG_IGN); pathlib.Path('fixture-child.json').write_text(json.dumps({'group':os.getpgrp()})); print('child-ready', flush=True); time.sleep(30)"])
    time.sleep(30)
sid = str(uuid.uuid4())
if provider == "codex" and "resume" in args:
    sid = args[args.index("resume") + 1]
if provider == "claude" and "--resume" in args:
    sid = args[args.index("--resume") + 1]
if "MISMATCH" in prompt:
    sid = str(uuid.uuid4())
if "SLEEP" in prompt:
    time.sleep(2)
if "BROKEN" in prompt:
    print("not JSON")
    sys.exit(0)
if provider == "codex":
    print(json.dumps({"type": "thread.started", "thread_id": sid}))
    print(json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": prompt}}))
    print(json.dumps({"type": "turn.failed", "error": {"message": "fixture failure"}} if "FAIL" in prompt
                     else {"type": "turn.completed", "usage": {"output_tokens": 4}}))
else:
    print(json.dumps({"type": "system", "subtype": "init", "session_id": sid, "model": "fixture"}))
    if "CONFLICT" in prompt:
        sid = str(uuid.uuid4())
    print(json.dumps({"type": "result", "session_id": sid, "result": prompt,
                      "subtype": "error_fixture" if "FAIL" in prompt else "success",
                      "is_error": "FAIL" in prompt, "usage": {"output_tokens": 4}}))
