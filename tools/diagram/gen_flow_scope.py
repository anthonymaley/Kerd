#!/usr/bin/env python3
"""Slice a release · Set the goal — stage flow. PRODUCT rung, function 4 of 4.

    python3 tools/diagram/gen_flow_scope.py
"""
import json
import os
import sys

sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from kit import Flow, INK, RED, GREY, mark_deltas
from to_svg import (to_svg, overflow_report, collision_report,
                    text_overlap_report)

f = Flow("Slice a release · Set the goal — stage flow",
         "PRODUCT rung · function 4 · interviewed 2026-08-03\n"
         "a release is a GROUPING, not a time axis. the DONE condition is "
         "assembled from upstream declarations, never authored at the end.")
SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

f.step("1", "IN", "What arrives",
       "what is already built · the framed and viability-tested candidates ·\n"
       "their QUALIFIED risks with countermeasures attached · and the record\n"
       "of what was already ruled out.",
       artifact="risk arrives PRE-CHEWED.\ndo not re-assess it here.\n\n"
                "a feature carrying a\nTEMPORARY countermeasure is\n"
                "a different slicing\ncandidate from one carrying\na permanent fix.")
f.down()

# ── 2 — the five factors, which do not work alike ────────────────────────
f.step("2", "GROUNDING", "What actually decides the grouping",
       "five factors, and lumping them together is the mistake — they act on\n"
       "the grouping in three different ways.")
_y = f.y
f.box("DEPENDENCY\nHARD CONSTRAINT\n\nB cannot ship before A\nif B needs A.\nno trade-off exists.",
      SP_X, _y, 190, 110, stroke=RED, size=12)
f.box("USER COMPREHENSION\nCEILING\n\nhow much change can be\nabsorbed AT ONCE.\ncaps the size.",
      SP_X + 205, _y, 190, 110, stroke=RED, size=12)
f.box("EFFORT · RISK ·\nOPPORTUNITY\nTRADE-OFFS\n\nshape the grouping\namong what is left.\nthey do not forbid.",
      SP_X + 410, _y, 190, 110, stroke=INK, bg=GREY, size=12)
f.txt("THE CEILING IS THE UNUSUAL ONE.\n"
      "almost everything sizes a release by what is READY —\n"
      "a bound from the producing side. this is a bound from\n"
      "the RECEIVING side: a release can be too big even when\n"
      "everything in it is finished.\n\n"
      "it is why 'we shipped everything we had' is a real\n"
      "failure mode and not a joke.",
      R_X, _y + 2, 12, RED)
f.y = _y + 140
f.down()

f.step("3", "OUT", "THE GROUPING",
       "what is in · what is deferred · and why this cut rather than another.\n"
       "dependencies eliminate the impossible groupings, the ceiling caps the\n"
       "size, the trade-offs choose among what is left.",
       artifact="NOT A SCHEDULE.\ntime may be attached\nlater, or never.\n\n"
                "MVP / v1 / v1.2 are\nORDERED, not scheduled.\n"
                "conflating the two turns\na grouping decision into\na deadline argument.")
f.down()

# ── 4 — assemble DONE ────────────────────────────────────────────────────
f.step("4", "GROUNDING", "Walk the upstream declarations",
       "the DONE condition is ASSEMBLED, never authored. you do not write a\n"
       "wish list at the end — you walk what each rung already declared.",
       artifact="this is why the draft\nwas circular. 'specific\n"
                "enough to terminate a\nloop' is true EXACTLY\n"
                "when every item points\nat a declaration that\nexists.")
f.down()

_y = f.y
f.txt("5", L_X, _y + 6, 26)
f.txt("OUT\nthe DONE\ncondition", L_X + 44, _y + 12, 13)
f.box("DONE  =  every item a conformance check against a DECLARATION",
      SP_X, _y, SP_W, 44, stroke=INK, bg=GREY, size=13)
f.txt("met the feature spec          <-  the contract\n"
      "met the product spec          <-  the idea brief\n"
      "goal of the function met      <-  the goal set here\n"
      "looks EXACTLY like design     <-  design, approved before build\n"
      "tests pass                    <-  every proof layer declared by\n"
      "                                  Decide what proves it —\n"
      "                                  INCLUDING user testing\n"
      "documentation complete        <-  DERIVED, not declared: every\n"
      "                                  declaration covered — feature,\n"
      "                                  product and problem specs, the\n"
      "                                  changes and fixes implemented,\n"
      "                                  the solution diagrams, and what\n"
      "                                  we ruled out",
      SP_X + 14, _y + 56, 12)
f.txt("TWO ORPHANS RESOLVED WITHOUT NEW FUNCTIONS.\n"
      "'user testing passed' and 'documentation is\n"
      "complete' had no upstream declaration when\n"
      "this started. user testing turned out to be a\n"
      "proof LAYER nobody had listed; documentation\n"
      "turned out to be DERIVED rather than declared.",
      R_X, _y + 56, 12, RED)
f.y = _y + 290
f.down()

f.step("6", "DECISION", "Does every DONE item point at a declaration that EXISTS?",
       "if it does not, it cannot be checked — so it passes by ASSERTION.\n"
       "that is the unqualified-risk failure in another costume: it looks\n"
       "handled because it is written down.\n"
       "  fix it one of two ways: remove the item, or go and get the\n"
       "  declaration made upstream. never leave it unbacked.",
       artifact="", dashed=True)
f.down()

f.step("7", "APPROVAL", "Acceptance — TWO KEYS",
       "MACHINE: every DONE item points at an existing declaration ·\n"
       "         dependencies satisfied by the ordering ·\n"
       "         the slice is within the comprehension ceiling.\n"
       "HUMAN:   Tony approves the grouping — what is in, what is deferred,\n"
       "         and why this cut rather than another.",
       artifact="the deferral is part of\nthe output, not the\n"
                "residue. what did NOT\nmake the cut goes to\nWhat we ruled out.",
       dashed=True)
f.down()

f.step("8", "HANDOFF", "→ Choose what matters next, then the loop",
       "the DONE condition is what /loop terminates on. a loop with a vague\n"
       "DONE condition is the one that runs forever — which is why the\n"
       "assembly rule above is load-bearing rather than tidy.",
       artifact="/loop MUST NOT run where\nnothing can refuse.\n"
                "still true, still unfixed —\n0 CI workflows, every repo.")

out = ("/Users/anthonymaley/Kerd/docs/plans/"
       "2026-08-03-slice-a-release-flow.excalidraw")
_ann = out.replace("-flow.excalidraw", "-tony.json").replace(
    "docs/plans/", "docs/plans/annotations/")
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
