#!/usr/bin/env python3
"""Test 4: could Jev predict, from the review request alone, whether Codex or Claude
would block it? Marks were set by reading each reply's verdict (blocked = a change was
required before the guarded step; cleared = none; excluded = not a review verdict).
Requests live in .git/kerd-agent/requests (local only); results keep ids and scores only."""
import json, sys, time
from pathlib import Path
from run_trial import api_key, ask
HERE = Path(__file__).resolve().parent
raw = json.load(open(sys.argv[1]))
marks = sys.argv[2]
assert len(marks) == len(raw), (len(marks), len(raw))
key = api_key(); out = []
for x, m in zip(raw, marks):
    if m == "X": continue
    body = {"model": "jev-latest",
            "state": "A request sent to an independent reviewer of a software change:\n\n" + x["prompt"][:6000],
            "questions": {"blocks": {"type": "noul",
                "instructions": "A careful independent reviewer, checking this change against the repository, would require at least one correction before it proceeds."}}}
    t0 = time.monotonic(); r = ask(key, body)
    out.append({"request": x["file"], "role": x["role"], "blocked": m == "B",
                "prompt_chars": len(x["prompt"]), "ms": round((time.monotonic()-t0)*1000), "response": r})
    print(len(out), "error" if "error" in r else "ok", flush=True)
(HERE / "review_results.json").write_text(json.dumps(out, indent=1))
