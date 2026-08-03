#!/usr/bin/env python3
"""Test viability — stage flow. PRODUCT rung, function 2 of 5.

Layout comes from kit.Flow, shared with every other stage, so a fix to step
spacing or the legend lands on all of them rather than the one being edited.

    python3 tools/diagram/gen_flow_viability.py
"""
import json
import os
import sys

sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from kit import Flow, INK, RED, GREEN, BLUE, GREY, mark_deltas
from to_svg import (to_svg, overflow_report, collision_report,
                    text_overlap_report)

f = Flow("Test viability — stage flow",
         "PRODUCT rung · function 2 of 5 · interviewed 2026-08-03\n"
         "receives a viability SIGNAL from framing and turns it into a verdict. "
         "the killer assumption differs by route; the test does not.")

SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

# ── 1 ────────────────────────────────────────────────────────────────────
f.step("1", "IN", "What arrives from framing",
       "the idea brief OR the problem statement · its killer assumption ·\n"
       "and a viability SIGNAL — never a verdict. testing it is this rung's job.\n"
       "  IDEA     — is the need real, and can we win?\n"
       "  PROBLEM  — is the cause correctly located, and is closing the gap\n"
       "             worth what it costs?",
       artifact="the VALUE statement comes\nwith it. that number is\n"
                "what 'fatal' is measured\nagainst later.")
f.down()

# ── 2 — the correction ───────────────────────────────────────────────────
f.step("2", "GROUNDING", "Sort what is already on the table",
       "risks are NOT unnamed. that was a drafted claim, and it was wrong.",
       artifact="", note="")
_y = f.y
f.box("UNMITIGATED\nnamed, understood,\nnothing done", SP_X, _y, 190, 76,
      stroke=INK, bg=GREY, size=12)
f.box("UNQUALIFIED\nnamed, NOT sized —\nwe do not know how bad", SP_X + 205, _y,
      190, 76, stroke=RED, size=12)
f.box("ACCEPTED UNKNOWN\nknown gap, taken on\ndeliberately", SP_X + 410, _y,
      190, 76, stroke=INK, bg=GREY, size=12)
f.txt("UNQUALIFIED is the dangerous one, and it is\n"
      "dangerous because it does not look dangerous.\n"
      "a named, unsized risk READS AS MANAGED — it has\n"
      "a name, it is written down, it looks handled.\n"
      "the failure mode is not silence. it is false comfort.",
      R_X, _y + 2, 12, RED)
f.y = _y + 106
f.down()

# ── 3 — triage ───────────────────────────────────────────────────────────
f.step("3", "DECISION", "Cheap estimate — could this one be fatal?",
       "two passes, or 'risk-driven, not menu-driven' quietly becomes a full\n"
       "risk register. estimate first, spend evidence second.\n"
       "  could plausibly cross the line  → gather evidence (step 4)\n"
       "  clearly cannot                  → not this rung's problem",
       artifact="the triage itself is\nrecorded. what you chose\n"
                "NOT to investigate is\npart of the output.",
       dashed=True)
f.down()

# ── 4 — evidence ─────────────────────────────────────────────────────────
f.step("4", "GROUNDING", "EVIDENCE — what qualifies a risk",
       "whichever is cheaper AND would actually change the decision:\n"
       "  A TEST      — run something. empirical.\n"
       "  AN ANALYSIS — prove it from what is already known. also evidence,\n"
       "                and usually the cheapest. not everything needs\n"
       "                an experiment.\n"
       "without evidence you cannot dispose of a risk — only feel better\n"
       "about it.",
       artifact="the evidence is an\nartifact, not a memory.\n"
                "a qualified risk POINTS\nAT what qualified it.")
f.down()

# ── 5 — measure ──────────────────────────────────────────────────────────
_y = f.y
f.txt("5", L_X, _y + 6, 26)
f.txt("MEASURE\nqualified =\nproven AND\nmeasured", L_X + 44, _y + 12, 13)
f.box("IMPACT\nmeasured, in the units\nVALUE was stated in", SP_X, _y, 290, 76,
      stroke=INK, bg=GREY, size=13)
f.box("LIKELIHOOD\nseparately. never folded\ninto the impact number",
      SP_X + 310, _y, 290, 76, stroke=INK, bg=GREY, size=13)
f.txt("DO NOT MULTIPLY THEM.\n"
      "expected value is the wrong maths for a bet you\n"
      "take once — a 5% chance of ending the thing is\n"
      "not 5% of the damage. you do not get to average\n"
      "across a single non-repeated outcome.\n\n"
      "FATAL = impact >= the VALUE framing declared,\n"
      "at ANY likelihood. likelihood sets the RESPONSE,\n"
      "not the classification.",
      R_X, _y + 2, 12, RED)
f.y = _y + 136
f.down()

# ── 6 — countermeasure, and the blocker default ──────────────────────────
f.step("6", "DECISION", "Is there a countermeasure?",
       "a countermeasure is a HYPOTHESIS — 'I believe X will address Y because\n"
       "Z' — so it must state what it is expected to do, or nothing can check\n"
       "later whether it worked.",
       artifact="", dashed=True)
_y = f.y
cx = SP_X + SP_W / 2
f.arrow([(cx, _y), (cx, _y + 22), (SP_X + 100, _y + 22), (SP_X + 100, _y + 48)])
f.arrow([(cx, _y), (cx, _y + 22), (SP_X + 320, _y + 22), (SP_X + 320, _y + 48)])
f.arrow([(cx, _y), (cx, _y + 22), (SP_X + 520, _y + 22), (SP_X + 520, _y + 48)],
        stroke=RED)
_y += 48
f.box("PERMANENT\nroot cause addressed", SP_X, _y, 200, 60, stroke=INK,
      bg=GREY, size=12)
f.box("TEMPORARY\ncontained, not cured", SP_X + 215, _y, 200, 60, stroke=INK,
      bg=GREY, size=12)
f.box("NONE\n= BLOCKER", SP_X + 430, _y, 170, 60, stroke=RED, size=13)
f.txt("A RISK WITHOUT A COUNTERMEASURE IS A BLOCKER.\n"
      "that is the DEFAULT — so silence stops the work\n"
      "instead of passing it, which is the whole point.\n\n"
      "a blocker clears ONE way: an explicit act of\n"
      "acceptance. who, when, on what basis. an\n"
      "ACCEPTED UNKNOWN is a blocker accepted without\n"
      "even knowing its size — allowed, never by default.",
      R_X, _y - 30, 12, RED)
f.txt("carries the CONDITION that brings it back.\n"
      "an unmarked temporary countermeasure is a\n"
      "permanent one by neglect.",
      SP_X + 215, _y + 66, 12, RED)
f.y = _y + 118
f.down()

# ── 7 — acceptance ───────────────────────────────────────────────────────
f.step("7", "APPROVAL", "Acceptance — TWO KEYS",
       "MACHINE: nothing merely NAMED. every risk proven, measured and given a\n"
       "         likelihood, or an explicit accepted unknown. impact and value\n"
       "         in comparable units. every countermeasure states its expected\n"
       "         effect. every TEMPORARY one carries its return condition.\n"
       "         NO BLOCKER LEFT UNACCEPTED.\n"
       "HUMAN:   Tony accepts each blocker BY NAME — including the unknowns and\n"
       "         any low-likelihood fatal. rounding a small probability to zero\n"
       "         silently is exactly what this gate exists to stop.",
       artifact="the acceptance is the\nartifact. 'we discussed\n"
                "it' is not an acceptance.",
       dashed=True)
f.down()

# ── 8 — verdict ──────────────────────────────────────────────────────────
_y = f.y
f.txt("8", L_X, _y + 6, 26)
f.txt("OUT\nthe verdict", L_X + 44, _y + 12, 13)
f.box("PROCEED\nno unaccepted\nblocker remains", SP_X, _y, 190, 68, stroke=INK,
      bg=GREY, size=12)
f.box("RESHAPE\nchange the thing so\nthe fatal risk is not", SP_X + 205, _y,
      190, 68, stroke=INK, bg=GREY, size=12)
f.box("DEAD\nhigh impact\n+ high likelihood\n+ no countermeasure",
      SP_X + 410, _y, 190, 68, stroke=RED, size=12)
f.txt("HIGH IMPACT + HIGH LIKELIHOOD + NO COUNTERMEASURE\n"
      "= DEAD PROJECT. not a kill you choose — a state you\n"
      "recognise. the thing is already dead; the only\n"
      "question is how long before someone says so.\n\n"
      "THIS IS THE LIMIT ON ACCEPTANCE. every other blocker\n"
      "can be accepted by name. this one cannot, or\n"
      "'accept by name' becomes an escape hatch for\n"
      "anything. the only moves left are RESHAPE — change\n"
      "the thing so the risk is no longer fatal — or KILL.\n\n"
      "a kill here is a SUCCESS: it is the cheapest place\n"
      "the thing can die.",
      R_X, _y + 2, 12, RED)
f.y = _y + 208
f.down()

# ── 9 — handoff ──────────────────────────────────────────────────────────
f.step("9", "HANDOFF", "→ Shape the solution  (DESIGN)",
       "carries the surviving risks and their countermeasures forward. design\n"
       "builds AROUND them — a countermeasure is a constraint on the shape,\n"
       "not a note in a document nobody opens.",
       artifact="the next rung runs its\nOWN entry gate against\nwhat arrived here.")

# ── open on this stage ───────────────────────────────────────────────────
f.txt("OPEN on this stage — accepted risks age, and nothing brings them back.\n"
      "A TEMPORARY countermeasure is self-expiring: it carries its own return "
      "condition, so that class is answered.\n"
      "The other two are not. An ACCEPTED UNKNOWN was accepted because evidence "
      "was too expensive — evidence gets\ncheaper. A LOW-LIKELIHOOD FATAL was "
      "accepted at one moment's odds — odds move. Today both are permanent by\n"
      "default, which is the same shape as the design doc that held the answer "
      "and went unread: right when decided,\nand nothing brings it back.",
      X, f.y + 40, 15, RED)

# ── write ────────────────────────────────────────────────────────────────
out = ("/Users/anthonymaley/Kerd/docs/plans/"
       "2026-08-03-test-viability-flow.excalidraw")

_ann = ("/Users/anthonymaley/Kerd/docs/plans/annotations/"
        "2026-08-03-test-viability-tony.json")
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
