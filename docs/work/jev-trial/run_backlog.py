#!/usr/bin/env python3
"""Test 1: Jev judges the 73 Backlog rows of the 2026-09-12 closure review.

Truth is that review's verdict (an Opus 5 player; its done and dead rows were then
closed at that day's Switch Out). State is the row's opening words plus the evidence
the review recorded. Writes backlog_results.json beside this file.
"""
import json, re, sys, time
from pathlib import Path
from run_trial import api_key, ask

HERE = Path(__file__).resolve().parent
SRC = HERE.parents[1] / "work/model-ready-work/trials/2026-09-12-conductor-session-closure-review.md"
VERDICTS = {
    "done": "The work the row asks for has been completed; the evidence shows it exists.",
    "dead": "The row no longer applies: its target was removed, replaced or made moot.",
    "open": "The work is still needed and not yet done.",
    "unsure": "The evidence is not enough to tell whether it is done, dead or open.",
}

rows = []
for line in SRC.read_text().splitlines():
    m = re.match(r"^\| (\d+) \| (.*?) \| (.*?) \| (.*?) \| (.*) \|$", line)
    if m:
        n, row, group, verdict, ev = m.groups()
        rows.append({"id": int(n), "row": row, "group": group,
                     "truth": verdict.strip("* ").lower(), "evidence": ev})
assert len(rows) == 73, len(rows)
key = api_key()
out = []
for r in rows:
    body = {"model": "jev-latest",
            "state": f"A backlog row from a software project (opening words): {r['row']}\nArea: {r['group']}\n\nWhat a reviewer found when checking it against the repository:\n{r['evidence']}",
            "questions": {"verdict": {"type": "choice",
                                      "instructions": "Given what the reviewer found, what should happen to this backlog row?",
                                      "criteria": VERDICTS}}}
    t0 = time.monotonic(); resp = ask(key, body)
    out.append({**r, "ms": round((time.monotonic() - t0) * 1000), "response": resp})
    print(r["id"], "error" if "error" in resp else "ok", flush=True)
(HERE / "backlog_results.json").write_text(json.dumps(out, indent=1))
