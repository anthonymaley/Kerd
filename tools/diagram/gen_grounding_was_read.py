#!/usr/bin/env python3
"""Grounding-was-read — declarations + the reachability audit. Design package.

    python3 tools/diagram/gen_grounding_was_read.py

Draws docs/design/grounding-was-read.md for the design conversation: the
prose-and-luck status quo, the declared reading list, the granularity
decision, the AU5 mechanism and refusal text, why optional beats required,
the proof plan, and the named out-of-scope.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from kit import Flow, INK, RED, GREEN, GREY, mark_deltas  # noqa: E402
from to_svg import (to_svg, overflow_report, collision_report,  # noqa: E402
                    text_overlap_report)

f = Flow("Grounding-was-read — declarations + the reachability audit · design package",
         "slice 1 of docs/product/grounding-was-read.md\n"
         "lost becomes a red light; whether reading happened stays slice 2.")
SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

# ── 1 — now ──────────────────────────────────────────────────────────────
f.step("1", "NOW", "Grounding today: prose, memory, luck",
       "what must be read before producing lives in walk detail and in\n"
       "heads. skipped reading leaves no trace - the 6 Jul design doc held\n"
       "1 Aug's answer, well-named, on disk, unread.",
       artifact="honest finding at design\ntime: A8's sketched landing\n"
                "site does NOT exist -\ncheck_rung is inline code,\n"
                "there is no kit.GATES table\nto hold a grounding slot.\n"
                "a static home would be\ninvented, not filled.",
       colour=RED)
f.down()

# ── 2 — the change ───────────────────────────────────────────────────────
f.step("2", "CHANGE", "The product doc declares its reading list",
       "docs/product/<slug>.md gains an OPTIONAL section:\n"
       "## Grounding\n"
       "- <ref> — <why>   (ref = path or glob from repo root)\n"
       "the audit gains AU5: every declared ref resolves on disk, or the\n"
       "push goes red naming the doc and the broken reference.",
       artifact="lost is a checkable state.\n\n"
                "slice 1 checks RESOLUTION\nonly. whether the reading\n"
                "happened is slice 2\n(receipts - priced in the\n"
                "product ledger).")
f.down()

# ── 3 — the granularity decision ─────────────────────────────────────────
f.step("3", "DECISION", "Where declarations live — marks, not a matrix",
       "static per-rung table: X - cannot name what THIS work touches;\n"
       "duplicates the gate's existing existence checks; invents a data\n"
       "structure ahead of need.\n"
       "per-item ## Grounding: O - carries the actual payload (the\n"
       "6-Jul class: related living docs, standing decisions).\n"
       "hybrid: deferred - slice 2's rung-scoped receipts may want a\n"
       "static floor; an extension point, not a debt.",
       artifact="options are not close, so\nmarks suffice - the design\n"
                "instrument's own rule:\nscores only when close,\n"
                "weights only when criteria\ndiffer.")
f.down()

# ── 4 — AU5 mechanism ────────────────────────────────────────────────────
f.step("4", "MECHANISM", "AU5 — parse and refusal, verbatim",
       "for every docs/product/*.md: find_section('Grounding') ->\n"
       "absent = vacuous pass (declaring is opting in). per '- ' line:\n"
       "split on the FIRST ' — '; resolve exact path, or glob with >=1\n"
       "match, against the repo root.")
_y = f.y
f.box("CLEAN\nevery declared ref resolves\naudit stays: audit: clean",
      SP_X, _y, 250, 84, stroke=INK, bg=GREY, size=13)
f.box("PROBLEMS, named verbatim:\n"
      "grounding reference does not resolve: <ref>\n"
      "grounding line malformed: <line>",
      SP_X + 270, _y, 340, 84, stroke=RED, size=13)
f.txt("rides gate.py audit =\nCI step two. rot is caught\n"
      "at the push that causes it,\nnever archaeologically.",
      R_X, _y + 96, 12)
f.y = _y + 150
f.down()

# ── 5 — why optional ─────────────────────────────────────────────────────
f.step("5", "EDGE", "Why optional, not required",
       "retrofitting twelve product docs with invented reading lists\n"
       "would manufacture exactly the hollow declarations the frame's\n"
       "killer risk names. grounding grows per new work; the audit\n"
       "enforces honesty about what WAS declared.",
       artifact="residual, named (accepted,\nper the frame): an absent\n"
                "section means no\nreachability guarantee for\nthat work item.",
       dashed=True)
f.down()

# ── 6 — proof ────────────────────────────────────────────────────────────
f.step("6", "PROOF", "Fixtures + dogfood + the measurement answered",
       "kit.selftest gains four temp-tree cases: resolving (exact +\n"
       "glob) -> clean · broken ref -> named verbatim · malformed line\n"
       "-> named · absent section -> vacuous pass.\n"
       "at ship: both-ways demonstration on the real tree (0.70.0\n"
       "pattern). dogfood: this item's OWN product doc gains its\n"
       "## Grounding section in the build.",
       artifact="the stage-1 measurement,\nANSWERED:\n\n"
                "broken grounding refs at a\npushed tip -> 0: AU5 inside\n"
                "gate.py audit at every tip.\n\nCI STAYS SEVEN STEPS.")
f.down()

# ── 7 — out of scope ─────────────────────────────────────────────────────
f.step("7", "SCOPE", "Out of scope, named (composer key on the frame)",
       "READ-RECEIPTS at gates: slice 2, carrying the hollow-stamping\n"
       "row and the retrieval-not-comprehension claim.\n"
       "RUNG-SCOPED grounding + any static floor: slice 2's extension\n"
       "point, taken only if receipts need it.\n"
       "ORPHAN REPORT (artifacts no grounding names): unframed.\n"
       "COMPREHENSION PROOFS: never, per the ledger's third row.",
       artifact="", colour=GREEN, dashed=True)

# Tony's font call 2026-08-04: the package reads in Nunito (6), not the
# hand-drawn Excalifont the kit defaults to.
for _e in f.els:
    if _e["type"] == "text":
        _e["fontFamily"] = 6

out = os.path.join(REPO, "docs", "design", "grounding-was-read.excalidraw")
_ann = os.path.join(REPO, "docs", "plans", "annotations",
                    "grounding-was-read-tony.json")
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
