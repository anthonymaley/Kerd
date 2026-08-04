#!/usr/bin/env python3
"""CROSS-CUTTING — constraints, not steps. Walked 2026-08-04.

No arrows between panels: these are not a sequence, they are constraints on
how EVERY function behaves. Numbers are for annotation reference only.

    python3 tools/diagram/gen_flow_crosscutting.py
"""
import json
import os
import sys

sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from kit import Flow, INK, RED, GREEN, BLUE, GREY, mark_deltas
from to_svg import (to_svg, overflow_report, collision_report,
                    text_overlap_report)

f = Flow("CROSS-CUTTING — constraints, not steps",
         "five functions walked 2026-08-04 · no order implied — each binds "
         "EVERY function on the board\nplus two system-wide properties and "
         "the closed reachable clause.")

SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X
GAP = 30

# ── 1 — how we talk ──────────────────────────────────────────────────────
f.step("1", "TALK", "How we talk to each other",
       "one question, drilled, carrying the findings it depends on — clear,\n"
       "visual, obvious: no rambling, no ambiguity, no noise. a DECISION\n"
       "question carries five things in the simplest terms: what it is · why\n"
       "it matters · the gap · what we win · what we lose. non-simple\n"
       "questions use the A3 storylines; a whiteboard diagram is a legitimate\n"
       "question form. FACTS are never asked — they die at a lower rung\n"
       "(code, docs, history). POSITIONS are never guessed — one source, the\n"
       "human. and STRAW-MAN YOURSELF FIRST: 'is that really true?'",
       artifact="speech bubble + border\nmarks a question needing\n"
                "the human's answer.",
       note="must BIND from outside the model —\n"
            "five written statements did not bind;\n"
            "the one rule that holds today is held\n"
            "by a hook firing on every prompt.")
f.y += GAP

# ── 2 — the entry gate ───────────────────────────────────────────────────
f.step("2", "GATE", "Do we have what we need?",
       "checks the DECLARED inputs of the rung about to start — mechanical:\n"
       "declarations exist on disk or they don't — and names exactly what is\n"
       "missing. the refusal is not its own mechanism: it rides the LADDER\n"
       "as a question the spec cannot answer. renders via Show where we are,\n"
       "never a view of its own. honours a declared SPIKE as the one\n"
       "licensed bypass.",
       artifact="the gates in series ARE\nthe routing — work enters\n"
                "at the lowest rung whose\ninputs all exist.")
f.y += GAP

# ── 3 — show where we are ────────────────────────────────────────────────
f.step("3", "VIEW", "Show where we are",
       "PUSHED at every stage close and end of task; PULLABLE at any time.\n"
       "have / need / progress for one rung AND the whole board — never\n"
       "prose. LIVENESS during a long task: landed · in flight · remaining\n"
       "at piece granularity, updated at every piece boundary, derived from\n"
       "disk — motion vs hang without asking, never self-reported.",
       artifact="the push is a REPORT,\nnever an ask — it costs\n"
                "the human nothing.",
       note="gate-close copy = dated RECORD\n"
            "(docs/gates/); the any-time view is\n"
            "living. the date split's third caller.")
f.y += GAP

# ── 4 — size work to a model ─────────────────────────────────────────────
f.step("4", "SIZE", "Size work to a model",
       "every dispatching function declares tier + effort + why — sized\n"
       "AFTER the work is written, never before; never the top tier for\n"
       "difficulty alone. wrong sizes surface to NO human: caught by the\n"
       "piece's own failing check, re-sized and re-dispatched by the roles.",
       artifact="the declaration makes\nthe ladder's 'lowest\n"
                "role' computable.")
f.y += GAP

# ── 5 — external tools ───────────────────────────────────────────────────
f.step("5", "TOOLS", "Stay in control of external tools",
       "a tool is staffed like a PLAYER. the driving role decides which\n"
       "tools are needed; every invocation carries a bounded contract — do\n"
       "this, don't do that, return in this shape, to the CALLER. the tool\n"
       "never names the next step. what is NOT adopted is named before\n"
       "invocation. KILL authority over a rogue task — control from outside\n"
       "the tool.",
       artifact="the measured failure:\nbrainstorming captured\n"
                "the plan phase and\nnever came back.")

# ── the properties ───────────────────────────────────────────────────────
f.txt("SYSTEM-WIDE PROPERTY — THE ROLE LADDER: every blocker, question and "
      "refusal anywhere rides ONE\nladder — answered at the lowest role with "
      "the knowledge AND the authority, escalated only on genuine\n"
      "inability; the human is the last rung. three callers surfaced it: the "
      "contract's escalation, the loop's\nquestions, the gate's refusals.",
      X, f.y + 40, 15, RED)
f.txt("REACHABLE — CLOSED 2026-08-04: an artifact is reachable when at least "
      "one function's declared\ngrounding names it, enforced by the entry "
      "gate. lost is a CHECKABLE state — an artifact in no\ngrounding list "
      "is lost by declaration. naming solves findability; grounding solves "
      "reachability.",
      X, f.y + 130, 15, RED)

# ── write ────────────────────────────────────────────────────────────────
out = ("/Users/anthonymaley/Kerd/docs/plans/"
       "2026-08-04-crosscutting-flow.excalidraw")

_ann = ("/Users/anthonymaley/Kerd/docs/plans/annotations/"
        "2026-08-04-crosscutting-tony.json")
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
