#!/usr/bin/env python3
"""BUILD rung — stage flow. Two functions + a rung-wide property.

Layout comes from kit.Flow, shared with every other stage, so a fix to step
spacing or the legend lands on all of them rather than the one being edited.

    python3 tools/diagram/gen_flow_build.py
"""
import json
import os
import sys

sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from kit import Flow, INK, RED, GREEN, BLUE, GREY, mark_deltas
from to_svg import (to_svg, overflow_report, collision_report,
                    text_overlap_report)

f = Flow("BUILD — stage flow",
         "BUILD rung · two functions + a rung-wide property · interviewed "
         "2026-08-03\nBuild a piece · Prove it (the loop) → Prove the whole · "
         "Goal gate (where the human re-enters).")

SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

# ── 1 ────────────────────────────────────────────────────────────────────
f.step("1", "IN", "One piece of the work order",
       "under the two-tier rule: the exact spec — scope, the why, its own\n"
       "check — plus access to related materials. AND NO MORE. a builder\n"
       "holding the whole file re-derives intent from it; a builder holding\n"
       "one self-contained piece builds that piece.",
       artifact="the piece arrived with\nits check already written\n"
                "— a piece without one was\nnever handable at all.")
f.down()

# ── 2 — build + measure (the loop) ───────────────────────────────────────
f.step("2", "BUILD +\nMEASURE", "Checked against ALL RELEVANT specs",
       "the piece's own criteria PLUS everything its change touches —\n"
       "relevance scoped by the overseer, who holds all truth. tests match\n"
       "the acceptance criteria / goal the work order carries.",
       artifact="'relevant' is what covers\ncollateral: neighbouring\n"
                "terrain is relevant by\nconstruction.",
       note="the measured failure this guards: a\n"
            "deletion range that swallowed three\n"
            "helpers while passing every check\n"
            "written for the piece itself.")
f.down()

# ── 3 — per-piece verdict ────────────────────────────────────────────────
f.step("3", "DECISION", "Piece done — or the overseer's problem",
       "no human key per piece. a failing piece is re-dispatched, re-scored,\n"
       "or stopped BY THE ROLES — the human hears nothing unless a gap no\n"
       "agent role can answer becomes a BLOCKER (the escalation contract).\n"
       "pieces loop here until every piece has landed.",
       artifact="on-demand COLD EYES may\nbe ordered early for a\n"
                "risky piece — one carrying\na countermeasure, or\ntouching fatal terrain.",
       dashed=True)
f.down(gap=48, label="every piece landed")

# ── 4 — cold review ──────────────────────────────────────────────────────
f.step("4", "COLD\nEYES", "The whole change, reviewed unanchored",
       "the reviewing eyes see ONLY the work order and the change — no build\n"
       "context, no session memory. the builder's own context is what blinds\n"
       "it. once per goal, never routinely per piece.",
       artifact="verdict CAN BLOCK.\nadvice is not a check.",
       note="the flaw class this catches is a gap in\n"
            "the DECLARED TRUTH itself — 'never\n"
            "contacts your server' failed no check,\n"
            "because nothing declared it. those gaps\n"
            "live at ASSEMBLY, not per piece.")
f.down()

# ── 5 — conformance ──────────────────────────────────────────────────────
f.step("5", "CONFORM", "Every declared layer — never one verdict",
       "code · logic · architecture · pixel vs the approved design · the\n"
       "product measurements from stage 1. each layer reports its own\n"
       "conformance; a single green tick is how gaps hide.",
       artifact="this is where every\nupstream declaration\ncomes home to be checked.")
_y = f.y
f.txt("RUNG-WIDE PROPERTY: every gate on this rung must be able\n"
      "to BLOCK from OUTSIDE the model. advisory output is not a\n"
      "check. this is what makes the escalation contract\n"
      "trustworthy: the human can only afford to hear nothing\n"
      "if nothing bad can pass silently.",
      R_X, _y - 8, 12, RED)
f.y = _y + 78
f.down()

# ── 6 — the expert-user pass ─────────────────────────────────────────────
f.step("6", "APPROVAL", "GOAL ACHIEVED — the expert-user pass",
       "MACHINE: every declared layer conforms, per layer.\n"
       "HUMAN:   Tony uses the OUTPUT ITSELF — the app feature, the\n"
       "         performance, the document, the diagram, whatever it finally\n"
       "         is — checked as the EXPERT USER, not as a reader of reports.",
       artifact="Tony, 2026-08-03: 'im\nchecking it as the\nexpert user.'",
       dashed=True,
       note="this is the report the escalation\n"
            "contract promised. the human re-enters\n"
            "HERE, and nowhere earlier short of an\n"
            "unanswerable blocker.")

# ── open on this stage ───────────────────────────────────────────────────
f.txt("OPEN on this stage — the property has no instance: nothing today can refuse "
      "from outside the model.\nCI on ~/3of3 is the first concrete build item (MVP "
      "sequence). Until it exists, every gate on this page\nis prompt-layer — the "
      "escalation contract is written but not enforceable.",
      X, f.y + 40, 15, RED)

# ── write ────────────────────────────────────────────────────────────────
out = ("/Users/anthonymaley/Kerd/docs/plans/"
       "2026-08-03-build-flow.excalidraw")

_ann = ("/Users/anthonymaley/Kerd/docs/plans/annotations/"
        "2026-08-03-build-tony.json")
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
