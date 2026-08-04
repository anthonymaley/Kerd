#!/usr/bin/env python3
"""Write the contract · Size and assign — stage flow. CONTRACT rung, complete.

Layout comes from kit.Flow, shared with every other stage, so a fix to step
spacing or the legend lands on all of them rather than the one being edited.

    python3 tools/diagram/gen_flow_contract.py
"""
import json
import os
import sys

sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from kit import Flow, INK, RED, GREEN, BLUE, GREY, mark_deltas
from to_svg import (to_svg, overflow_report, collision_report,
                    text_overlap_report)

f = Flow("Write the contract · Size and assign — stage flow",
         "CONTRACT rung · interviewed 2026-08-03\n"
         "the agreed design becomes a written work order a builder who was "
         "never in the room can build from.")

SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

# ── 1 ────────────────────────────────────────────────────────────────────
f.step("1", "IN", "The GO'd design package — INTACT",
       "full specs, documents, diagrams, measurements, plans, UX design,\n"
       "systems. nothing summarized on the way in: the contract is written\n"
       "FROM upstream truth, not from a digest of it.\n"
       "the qualified risks ride with it — a countermeasure is a constraint\n"
       "the work order must build around.",
       artifact="design's GO already\nhappened. this rung never\n"
                "re-derives or re-approves\nthe design.")
f.down()

# ── 2 — grounding ────────────────────────────────────────────────────────
f.step("2", "GROUNDING", "Read before writing the order",
       "the TERRAIN the work will change — actual code, read not summarized.\n"
       "the order must name exact paths, signatures and values, and it\n"
       "cannot do that from memory.\n"
       "WHAT WE RULED OUT — a contract proposes implementation choices.\n"
       "STANDING DECISIONS — the conventions a work order cannot violate.",
       artifact="same grounding law as\ndesign: inputs arrive on\n"
                "their own, grounding is\nwhat gets skipped.")
f.down()

# ── 3 — the order ────────────────────────────────────────────────────────
f.step("3", "THE ORDER", "Written so a stranger can build it",
       "implementable by a builder who NEVER SAW THE REASONING. every piece\n"
       "carries its exact scope, the why behind any non-obvious choice, and\n"
       "ITS OWN CHECK — a piece without a check cannot be handed to anyone.",
       artifact="the why travels IN the\npiece. a builder who\n"
                "re-derives intent drifts,\nconfidently.")
f.down()

# ── 4 — size and assign ──────────────────────────────────────────────────
f.step("4", "SIZE +\nASSIGN", "After the piece is written — never before",
       "a tag assigned during planning measures how hard the piece FELT to\n"
       "plan, not what judgment survived being written down. write the piece\n"
       "in full, then read it and ask what decision is still left in it.",
       artifact="what stays with the\noverseer after honest\n"
                "tagging is small —\nand that is correct.")
_y = f.y
f.box("the OVERSEER\nholds ALL upstream truth", SP_X, _y, 290, 64,
      stroke=INK, bg=GREY, size=13)
f.box("a BUILDER\nexact spec + related\nmaterials — AND NO MORE", SP_X + 310,
      _y, 290, 64, stroke=INK, bg=GREY, size=13)
f.txt("TWO-TIER ACCESS, BY ROLE. the tier is the requirement —\n"
      "not a token-saving trick. a builder holding the whole\n"
      "file re-derives intent from it; a builder holding one\n"
      "self-contained piece builds that piece.",
      R_X, _y + 2, 12, RED)
f.y = _y + 94
f.down()

# ── 5 — acceptance ───────────────────────────────────────────────────────
f.step("5", "APPROVAL", "Machine key ALONE — no human gate here",
       "every piece is MEASURABLE against an upstream declaration: the design\n"
       "package, the measurements, the countermeasures. provided that\n"
       "measuring is real, the human reads nothing at this rung.\n"
       "a piece NOTHING upstream declared cannot be measured, so it cannot\n"
       "pass by assertion — it is a PUSH-BACK to design.",
       artifact="Tony, 2026-08-03: 'i dont\nneed to approve contract\n"
                "if we can measure it meets\noutput of other stages.'",
       dashed=True,
       note="the DONE-assembled rule applied to the\n"
            "contract itself. this REMOVES today's\n"
            "per-spec human approval when the\n"
            "machine key holds.")
f.down()

# ── 6 — handoff + escalation ─────────────────────────────────────────────
f.step("6", "HANDOFF", "→ Execute a unit  (BUILD)",
       "pieces flow to builders under the two-tier rule. the ESCALATION\n"
       "CONTRACT governs everything downstream: the human hears ONLY of a\n"
       "gap no agent role can answer that is a BLOCKER — the blocker-\n"
       "acceptance path from Test viability. otherwise the next report is\n"
       "GOAL ACHIEVED.",
       artifact="the next rung runs its\nOWN entry gate against\nwhat arrived here.",
       note="stricter than today: score corrections\n"
            "are currently surfaced to the human\n"
            "before being made. under this rule they\n"
            "are not — only role-unanswerable\n"
            "blockers reach him.")

# ── open on this stage ───────────────────────────────────────────────────
f.txt("OPEN on this stage — the delegation half of the machinery that serves this "
      "function has never fired:\nthe score-writing call and sized builders exist as "
      "one disk-write trial (9:1 compression, tags assigned\ncorrectly), not as a "
      "session that built something. The first real delegated build is the test of\n"
      "everything on this page.",
      X, f.y + 40, 15, RED)

# ── write ────────────────────────────────────────────────────────────────
out = ("/Users/anthonymaley/Kerd/docs/plans/"
       "2026-08-03-write-the-contract-flow.excalidraw")

_ann = ("/Users/anthonymaley/Kerd/docs/plans/annotations/"
        "2026-08-03-write-the-contract-tony.json")
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
