#!/usr/bin/env python3
"""Rigor level — the declared level + the refusal. Design package.

    python3 tools/diagram/gen_rigor_level.py

Draws docs/design/rigor-level.md for the design conversation: the
never-asked status quo, the one-line declaration, the two settled forks
(where it lives; uniform + honest retrofit), the AU6 mechanism and gate
row with refusal text, the proof plan, and the named out-of-scope.
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

f = Flow("Rigor level — the declared level + the refusal · design package",
         "slice 1 of docs/product/rigor-level.md\n"
         "the rigor question is asked by construction; what a level requires stays slice 2.")
SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

# ── 1 — now ──────────────────────────────────────────────────────────────
f.step("1", "NOW", "Rigor today: never asked",
       "DONE assembles only what upstream declared - an undeclared rigor\n"
       "class fails nothing. it is not waived, not failed, just never\n"
       "asked. zero product docs declare any measurement level; security\n"
       "has never been asked once, and nothing went red.",
       artifact="honest finding at design\ntime: grandfathering-for-\n"
                "free was REFUTED here -\nboard_for re-derives route\n"
                "for EVERY slug per render,\nso a new gate row is\n"
                "retroactive in effect.",
       colour=RED)
f.down()

# ── 2 — the change ───────────────────────────────────────────────────────
f.step("2", "CHANGE", "The Release slice declares its level, one line",
       "docs/product/<slug>.md ## Release slice gains one line:\n"
       "Rigor level: mvp\n"
       "legal set: spike · mvp · production-v1 - RIGOR_LEVELS tuple in\n"
       "tools/gates/kit.py, canonical write-down in tools/gates/README.md\n"
       "(the route/stage precedent). exactly one line per slice.",
       artifact="in slice 1 the value is\nDATA. what a level\n"
                "REQUIRES (the catalog,\nthe disposition table)\n"
                "arrives with slice 2.\ndeclaring is the forcing\nfunction.")
f.down()

# ── 3 — decision: where it lives ─────────────────────────────────────────
f.step("3", "DECISION", "Where the declaration lives — marks, not a matrix",
       "line in ## Release slice: O - matches the keyed frame ('declared\n"
       "in the Release slice definition'); nothing invented.\n"
       "front-matter key: X - a third key breaks the route/stage\n"
       "both-or-nothing pair.\n"
       "new ## Rigor section: X - empty until slice 2; RESERVED as the\n"
       "disposition table's home, nothing built for it now.",
       artifact="options are not close, so\nmarks suffice - scores\n"
                "only when close, weights\nonly when criteria differ.")
f.down()

# ── 4 — decision: uniform + honest retrofit ──────────────────────────────
f.step("4", "DECISION", "Uniform rule, honest retrofit — the frame amendment",
       "exempt list in kit: X - board says 'never asked' about three done\n"
       "journeys forever; a special case that only shrinks.\n"
       "audit-only, no gate row: X - nothing refuses a new slice; the\n"
       "forcing function loses its teeth.\n"
       "honest retrofit: O - one falsifiable line each, landing in the\n"
       "SAME COMMIT as the rule; no tip ever has one without the other.",
       artifact="Tony's key 2026-08-05:\na level is one falsifiable\n"
                "value - it cannot be\nhollow the way a\n"
                "reconstructed reading\nlist can.\n\n"
                "proposed, annotate if\ndishonest: all four mvp\n"
                "(push-wiring, grounding-\nwas-read, progress-html,\n"
                "rigor-level).",
       colour=GREEN)
f.down()

# ── 5 — mechanism ────────────────────────────────────────────────────────
f.step("5", "MECHANISM", "AU6 + the design-rung row — refusals verbatim",
       "for every docs/product/*.md: a Rigor level line OUTSIDE Release\n"
       "slice -> named. section present -> exactly one legal line inside.\n"
       "no Release slice section -> vacuous (framed docs, spikes).\n"
       "design rung gains the matching need row - same kit function,\n"
       "two call sites, one parser.")
_y = f.y
f.box("CLEAN\nevery Release slice declares\na legal level\naudit stays: audit: clean",
      SP_X, _y, 250, 96, stroke=INK, bg=GREY, size=13)
f.box("PROBLEMS, named verbatim:\n"
      "Release slice missing 'Rigor level: <...>' line\n"
      "illegal rigor level '<v>' (legal: spike, mvp, production-v1)\n"
      "duplicate Rigor level lines (want exactly one)",
      SP_X + 270, _y, 460, 96, stroke=RED, size=13)
f.txt("rides gate.py audit =\nCI step two. silence is\n"
      "caught at the push that\nships it. CI STAYS SEVEN\nSTEPS.",
      R_X, _y + 108, 12)
f.y = _y + 168
f.down()

# ── 6 — proof ────────────────────────────────────────────────────────────
f.step("6", "PROOF", "Fixtures + dogfood + the measurements answered",
       "selftest gains six temp-tree cases (18 -> 24): legal -> clean ·\n"
       "missing -> named verbatim · illegal -> named · duplicate -> named\n"
       "· misplaced -> named · no section -> vacuous.\n"
       "at ship: both-ways demo on the real tree (strip a retrofit line\n"
       "-> exit 1 naming it; restore -> clean). dogfood: this item's OWN\n"
       "Release slice declares its level in the same commit.",
       artifact="stage-1 measurements,\nANSWERED:\n\n"
                "undeclared level at a tip\n-> AU6 red within one CI\nrun, fix named.\n\n"
                "three done journeys'\nboard render -> unchanged:\n"
                "same-commit retrofit,\nroute pre/post identical,\n"
                "stale harness byte-compare.")
f.down()

# ── 7 — out of scope ─────────────────────────────────────────────────────
f.step("7", "SCOPE", "Out of scope, named (composer key on the frame)",
       "CATALOG + disposition table: slice 2 - the legal-set home\n"
       "migrates from kit constant to catalog when it exists.\n"
       "MEASURED CLASSES as CI checks: slice 3.\n"
       "route: spike FOLD into the rigor axis: unframed, untouched -\n"
       "a spike doc without a Release slice passes AU6 vacuously.\n"
       "LEVEL SEMANTICS: slice 1 refuses silence and illegality,\n"
       "never judges fit.",
       artifact="", colour=GREEN, dashed=True)

# Tony's font call 2026-08-04: the package reads in Nunito (6), not the
# hand-drawn Excalifont the kit defaults to.
for _e in f.els:
    if _e["type"] == "text":
        _e["fontFamily"] = 6

out = os.path.join(REPO, "docs", "design", "rigor-level.excalidraw")
_ann = os.path.join(REPO, "docs", "plans", "annotations",
                    "rigor-level-tony.json")
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
