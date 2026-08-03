#!/usr/bin/env python3
"""What we ruled out, and why — cross-cutting flow.

    python3 tools/diagram/gen_flow_ruledout.py
"""
import json
import os
import sys

sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from kit import Flow, INK, RED, GREY, mark_deltas
from to_svg import (to_svg, overflow_report, collision_report,
                    text_overlap_report)

f = Flow("What we ruled out, and why — flow",
         "CROSS-CUTTING · added 2026-08-03\n"
         "four functions independently demanded this output and none had a home "
         "for it. not a graveyard — an INPUT, read in grounding.")
SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

f.step("1", "IN", "An option is eliminated — at any rung",
       "a rejected approach and a failed fix are THE SAME THING. one was\n"
       "eliminated by an analysis, the other by a test — and those are the same\n"
       "kind of evidence differing in cost, as agreed at Test viability.\n"
       "splitting them was smuggling back a distinction already dissolved.",
       artifact="the four callers:\n"
                "  gaps that could not be\n  closed (Frame the intent)\n"
                "  accepted unknowns and\n  blockers (Test viability)\n"
                "  work we discounted\n  (Slice a release)\n"
                "  what was deliberately\n  not built (from cutting\n"
                "  Hold product truth)")
f.down()

f.step("2", "DECISION", "Was it ever a CANDIDATE?",
       "did someone believe it would work, for a reason?\n"
       "  YES  → its elimination is information. record it.\n"
       "  NO   → a slip is not an option. a mistyped variable was never a\n"
       "         candidate, so its failure says nothing.",
       artifact="this filter is what makes\nthe volume survivable.\n"
                "most failed fixes are\nslips, not eliminated\n"
                "concepts — so the real\nvolume is far below\n"
                "'every fix that failed'.",
       dashed=True)
f.down()

f.step("3", "OUT", "ONE entry per CONCEPT — never per attempt",
       "what was tried or considered  ·  why it was eliminated  ·  the evidence\n"
       "(a test OR an analysis)  ·  and the CONDITION that would bring it back.",
       artifact="NOT the code.\nNOT the diff.\nNOT the error output.\n\n"
                "concepts outlive codebases.\n'caching at the edge did\n"
                "not help, the miss rate\nwas already low' stays true\n"
                "after a rewrite. a diff\ndoes not.\n\n"
                "many failed attempts at\none idea are ONE entry.")
f.down()

# ── 4 — capture, and the risk that decides whether this exists ───────────
f.step("4", "DECISION", "How does it get captured?",
       "capture MUST be a byproduct of work already happening — never a\n"
       "separate act of discipline.\n"
       "  BUILD-LEVEL  — a failed verify IS the record. conductor already runs\n"
       "                 a verify per step and hands back after three failures.\n"
       "  DESIGN-LEVEL — hand-written. rare enough to afford it.",
       artifact="", note="", dashed=True)
_y = f.y
f.txt("RUN THROUGH TEST VIABILITY'S OWN MACHINERY:\n\n"
      "  RISK         the record is not maintained at volume\n"
      "  IMPACT       high — a stale 'already tried' list is WORSE\n"
      "               than none. it answers confidently and wrongly.\n"
      "               that is the exact argument that killed\n"
      "               Hold product truth.\n"
      "  LIKELIHOOD   high — the standard fate of any log needing\n"
      "               discipline to maintain.\n"
      "  COUNTERMEASURE   none, at first pass.\n\n"
      "  = HIGH IMPACT + HIGH LIKELIHOOD + NO COUNTERMEASURE\n"
      "  = DEAD PROJECT, by the rule set an hour earlier.\n\n"
      "so BYPRODUCT CAPTURE is not an optimisation. it is the\n"
      "condition of this artifact existing at all.",
      SP_X + 14, _y + 6, 12, RED)
f.y = _y + 250
f.down()

f.step("5", "READ", "Consumed in GROUNDING, by everything that proposes",
       "this is the whole point, and it is why the artifact is an input rather\n"
       "than a graveyard. a rung cannot start without reading what was already\n"
       "ruled out — which is what stops a dead option being re-proposed and\n"
       "re-argued from scratch months later.",
       artifact="SECOND CALLER for the\ngrounding column, and a\n"
                "partial answer to the\nreachability clause open\n"
                "since this morning:\n\n"
                "it gets read because a\nrung CANNOT START without\n"
                "it — not because someone\nremembers to.")
f.down()

f.step("6", "RETURN", "The condition that brings an entry back",
       "written at the moment of elimination, because that is the only moment\n"
       "anyone knows what would change the answer.\n"
       "'discounted because X' ages exactly like an accepted risk and a\n"
       "temporary countermeasure — the constraint that killed it may lift.",
       artifact="THIRD thing today with a\nreturn condition: a\n"
                "temporary countermeasure,\nan accepted risk, and now\n"
                "an eliminated option.\n\n"
                "three is enough to suspect\na general rule rather than\n"
                "three coincidences.")

out = ("/Users/anthonymaley/Kerd/docs/plans/"
       "2026-08-03-what-we-ruled-out-flow.excalidraw")
_ann = ("/Users/anthonymaley/Kerd/docs/plans/annotations/"
        "2026-08-03-what-we-ruled-out-tony.json")
if os.path.exists(_ann):
    for _e in json.load(open(_ann))["elements"]:
        _e.setdefault("customData", {})["author"] = "tony"
        _e["index"] = "z" + str(len(f.els)).zfill(4)
        f.els.append(_e)

mark_deltas(f.els, out)
json.dump({"type": "excalidraw", "version": 2,
           "source": "https://excalidraw.com", "elements": f.els,
           "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
           "files": {}}, open(out, "w"), indent=1)
print("wrote", out, f"| elements: {len(f.els)}")
w, h = to_svg(f.els, out.replace(".excalidraw", ".svg"))
print(f"svg {w:.0f}x{h:.0f}")
for label, faults in (("bound-text overflow", overflow_report(f.els)),
                      ("text/box collision", collision_report(f.els)),
                      ("text/text overlap", text_overlap_report(f.els))):
    print(f"!! {len(faults)} {label}(s): {faults[:3]}" if faults
          else f"no {label}s")
