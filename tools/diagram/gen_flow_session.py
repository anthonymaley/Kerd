#!/usr/bin/env python3
"""SESSION rung — stage flow. One function + a rung-wide property.

4 -> 1 under interview (2026-08-04): Drive to done survives; Open/close ·
Hold state dissolved into the property, Route to the altitude into the entry
gates, Keep context optimal into construction.

    python3 tools/diagram/gen_flow_session.py
"""
import json
import os
import sys

sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from kit import Flow, INK, RED, GREEN, BLUE, GREY, mark_deltas
from to_svg import (to_svg, overflow_report, collision_report,
                    text_overlap_report)

f = Flow("SESSION — stage flow",
         "SESSION rung · one function + a rung-wide property · interviewed "
         "2026-08-04\n4 → 1: Drive to done (the loop) survives — the other "
         "three dissolved: property, entry gates, construction.")

SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

# ── 1 — entry: the gates route ───────────────────────────────────────────
f.step("1", "IN", "The work order, already on disk",
       "a cut release with its DONE condition — every piece carrying its\n"
       "own check, measurements declared, risks qualified. entered through\n"
       "the GATES: work enters at the LOWEST rung whose declared inputs all\n"
       "exist; missing inputs push work UP, never through. nothing passes\n"
       "a gate on assertion.",
       artifact="the one licensed bypass\nis a SPIKE — declared up\n"
                "front, cheap, built for a\nkill-or-keep decision.",
       note="'just build it' is the anti-pattern\n"
            "for MVP work: measurable results, a\n"
            "spec reliably built against, risks\n"
            "recorded. a spike that wants to\n"
            "become real re-enters via the gates.")
f.down()

# ── 2 — the loop ─────────────────────────────────────────────────────────
f.step("2", "LOOP", "Next unblocked item → build and prove → repeat",
       "unattended. each piece runs BUILD's machinery on exactly its slice\n"
       "(two-tier access) and commits as it verifies. the driver holds\n"
       "nothing — state lives on disk — so it cuts and resumes fresh\n"
       "between pieces whenever conditions degrade. cutting costs nothing:\n"
       "cut liberally, even per piece.",
       artifact="no degradation detector\nneeded — the missing\n"
                "signal dissolved rather\nthan found.")
_y = f.y
f.txt("RUNG-WIDE PROPERTY: state lives in the DECLARED\n"
      "ARTIFACTS, never in the session. anything worth keeping\n"
      "is written the moment it exists. a session may die at\n"
      "any instant — the loss is bounded to the in-flight\n"
      "piece, redone from its spec.",
      R_X, _y - 8, 12, RED)
f.y = _y + 78
f.down()

# ── 3 — the escalation ladder ────────────────────────────────────────────
f.step("3", "DECISION", "A question the spec cannot answer",
       "answered at the LOWEST role with the knowledge AND the authority\n"
       "to answer it. escalates only on genuine inability — the intent-\n"
       "holding role may adjust within its declared power. the human is\n"
       "LAST, and hears only what no agent role can decide.",
       artifact="while an answer waits on\nthe human, nothing is\n"
                "built the answer could\ninvalidate — park vs stop\n"
                "is the driving role's call.",
       dashed=True,
       note="fills the escalation contract's\n"
            "middle: the ladder of roles that\n"
            "must fail before the human hears\n"
            "anything.")
f.down(gap=48, label="answered — the loop continues")

# ── 4 — the stops ────────────────────────────────────────────────────────
f.step("4", "STOP", "Two stops, nothing else",
       "GOAL ACHIEVED — hands to Prove the whole · Goal gate, where the\n"
       "expert-user pass is the report the escalation contract promised.\n"
       "or a HUMAN-LEVEL BLOCKER — pause, wait. a degraded session is not\n"
       "a stop: cut between pieces and resume.",
       dashed=True)

# ── open on this stage ───────────────────────────────────────────────────
f.txt("OPEN on this stage — the loop MUST NOT run at all where nothing can "
      "refuse: unattended requires\nevery gate able to BLOCK from outside the "
      "model. today: 0 CI, 0 hooks, every repo. CI (MVP\nsequence) is the "
      "precondition — until it exists this page describes a loop that may "
      "not be\nswitched on.",
      X, f.y + 40, 15, RED)

# ── write ────────────────────────────────────────────────────────────────
out = ("/Users/anthonymaley/Kerd/docs/plans/"
       "2026-08-04-session-flow.excalidraw")

_ann = ("/Users/anthonymaley/Kerd/docs/plans/annotations/"
        "2026-08-04-session-tony.json")
if os.path.exists(_ann):
    _a = json.load(open(_ann))["elements"]
    for _e in _a:
        _e.setdefault("customData", {})["author"] = "tony"
        _e["index"] = "z" + str(len(f.els)).zfill(4)
        f.els.append(_e)
    print(f"merged {len(_a)} preserved annotation(s)")

_marked, _supp = mark_deltas(f.els, out)
print(f"blue: {_marked} changed since last reviewed"
      if _marked or _supp else "blue: no reviewed snapshot yet")

doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
       "elements": f.els,
       "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
       "files": {}}
json.dump(doc, open(out, "w"), indent=1)
print("wrote", out)
print(f"elements: {len(f.els)}")

svg_out = out.replace(".excalidraw", ".svg")
w, h = to_svg(f.els, svg_out)
print("wrote", svg_out, f"({w:.0f}x{h:.0f})")

for label, faults, fmt in (
        ("bound-text overflow", overflow_report(f.els),
         lambda z: f"{z[0][:52]:<52} text {z[1]}px > box {z[2]}px"),
        ("text/box collision", collision_report(f.els),
         lambda z: f"{z[0]:<46} at ({z[1]},{z[2]})"),
        ("text/text overlap", text_overlap_report(f.els),
         lambda z: f"{z[0]:<40} over {z[1]:<40} at ({z[2]},{z[3]})")):
    if faults:
        print(f"!! {len(faults)} {label}(s):")
        for z in faults:
            print("   " + fmt(z))
    else:
        print(f"no {label}s")
