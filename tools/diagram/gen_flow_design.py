#!/usr/bin/env python3
"""Design the solution — stage flow. DESIGN rung, the whole rung (4 folded to 1).

Layout comes from kit.Flow, shared with every other stage, so a fix to step
spacing or the legend lands on all of them rather than the one being edited.

    python3 tools/diagram/gen_flow_design.py
"""
import json
import os
import sys

sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from kit import Flow, INK, RED, GREEN, BLUE, GREY, mark_deltas
from to_svg import (to_svg, overflow_report, collision_report,
                    text_overlap_report)

f = Flow("Design the solution — stage flow",
         "DESIGN rung · one function, one conversation, one package · interviewed "
         "2026-08-03\nthe four-way split (shape / agree / prove / interface) was "
         "Claude's decomposition of the brainstorming checklist, never Tony's shape.")

SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

# ── 1 ────────────────────────────────────────────────────────────────────
f.step("1", "IN", "What arrives from stage 1",
       "the intent document — idea brief or problem statement — WITH its\n"
       "MEASUREMENTS. those numbers are what the package must answer, and what\n"
       "post-build conformance will measure against.\n"
       "the QUALIFIED risks, countermeasures attached, from Test viability.",
       artifact="a countermeasure is a\nCONSTRAINT on the shape —\n"
                "design builds around it,\nnot a note nobody opens.")
f.down()

# ── 2 — grounding ────────────────────────────────────────────────────────
f.step("2", "GROUNDING", "Read before proposing anything",
       "inputs arrive on their own. grounding is what gets skipped.",
       artifact="", note="")
_y = f.y
f.box("WHAT WE\nRULED OUT\nno dead option\nre-pitched", SP_X, _y, 142, 90,
      stroke=INK, bg=GREY, size=11)
f.box("THE ACTUAL\nCODE\nnot summaries", SP_X + 152, _y, 142, 90,
      stroke=INK, bg=GREY, size=11)
f.box("STANDING\nDECISIONS\nsettled ground not\nre-litigated", SP_X + 304, _y,
      142, 90, stroke=INK, bg=GREY, size=11)
f.box("LIVING DESIGN\nDOCS it touches\nwhy neighbours\nhave their shape", SP_X + 456, _y,
      142, 90, stroke=INK, bg=GREY, size=11)
f.txt("the last two were added from measured failures, not\n"
      "theory: the 08-02 session trusted a stale code comment\n"
      "twice while the design doc holding the answer went\n"
      "unread. code cannot tell you WHY a neighbouring piece\n"
      "is shaped the way it is. this is reachability's second\n"
      "caller — a rung that cannot start without reading these\n"
      "is what makes them reachable.",
      R_X, _y + 2, 12, RED)
f.y = _y + 120
f.down()

# ── 3 — the conversation ─────────────────────────────────────────────────
f.step("3", "THE\nCONVERSATION", "At least TWO approaches, then choose",
       "options on CONSTANT AXES, costs marked, bets named — resolved in ONE\n"
       "message, not a sequence of clarifications. the choosing happens here,\n"
       "in the conversation, not in a separate function.",
       artifact="what was NOT chosen goes\nto the ruled-out record —\n"
                "capture as a byproduct,\nnot a separate task.",
       note="today's server (5.0.6, read not summarized):\n"
            "prose sections, approval PER SECTION ·\n"
            "'multiple choice preferred' · agreed in prose.\n"
            "the 2-3 approaches part earned its keep.")
f.down()

# ── 4 — the package ──────────────────────────────────────────────────────
f.step("4", "OUT", "ONE PACKAGE",
       "detailed specs · architecture plans · testing strategy · solution\n"
       "diagrams · flow diagrams · visualizations for AS MANY ASPECTS AS WE CAN.\n"
       "testing strategy is IN the package: test bias per layer, every seam\n"
       "needing a contract test named. the interface is one of the drawn aspects.\n"
       "(?) interface values a machine can check — tokens, hex, spacing, states.",
       artifact="LIVES AT docs/design/\n<slug>.md + .excalidraw —\n"
                "living, undated, same slug\nas the product doc.")
f.down()

# ── 5 — approval ─────────────────────────────────────────────────────────
f.step("5", "APPROVAL", "GO — two keys, neither sufficient alone",
       "HUMAN:   every aspect Tony cares about is DRAWN, he has reviewed the\n"
       "         drawings, and NOTHING IS LEFT TO ANNOTATE.\n"
       "MACHINE: every measurement stage 1 declared has a NAMED ANSWER in the\n"
       "         package — point at where the design delivers it. nothing\n"
       "         declared upstream goes unaddressed. the MEASURING itself is\n"
       "         post-build conformance, not here.",
       artifact="GO writes a dated gate\nrecord: docs/gates/\n"
                "<date>-<slug>-design.md —\nimmutable, diffable.",
       dashed=True)
f.down()

# ── 6 — handoff ──────────────────────────────────────────────────────────
f.step("6", "HANDOFF", "→ Write the contract  (CONTRACT)",
       "the approved package is what the orchestrator writes the score FROM.\n"
       "approval happened HERE — the contract rung never re-derives or\n"
       "re-approves the design.",
       artifact="the next rung runs its\nOWN entry gate against\nwhat arrived here.",
       note="TODAY THIS IS BROKEN: brainstorming's terminal\n"
            "state is 'invoking writing-plans' — the working\n"
            "half exits into the half conductor superseded in\n"
            "July (0 artifacts since 17 Jul). and its spec lands\n"
            "in docs/superpowers/specs/, a third filing home.")

# ── open on this stage ───────────────────────────────────────────────────
f.txt("OPEN on this stage — the (?) on machine-checkable interface values is drafted, "
      "not read from evidence.\nAnd the disposition of superpowers brainstorming itself "
      "(rewire its exit? replace it? route it per the\ntool-declares-route rule?) is a "
      "DESIGN-rung decision for the Kerd redesign, deliberately not made here —\n"
      "this walk declares what the function must do, not which tool serves it.",
      X, f.y + 40, 15, RED)

# ── write ────────────────────────────────────────────────────────────────
out = ("/Users/anthonymaley/Kerd/docs/plans/"
       "2026-08-03-design-the-solution-flow.excalidraw")

_ann = ("/Users/anthonymaley/Kerd/docs/plans/annotations/"
        "2026-08-03-design-the-solution-tony.json")
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
