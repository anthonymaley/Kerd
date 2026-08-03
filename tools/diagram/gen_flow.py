#!/usr/bin/env python3
"""Per-stage flow diagrams — one file per function, generated from the same
interview data that fills the board's DETAIL map.

The board (gen_excalidraw.py) says WHAT each function must do. This says HOW one
stage runs: sequence, branches, the artifacts produced at each point, and where
the approvals sit. Arrows are used here and nowhere else — sequence is the whole
point of a flow, and containment cannot express order.

    python3 tools/diagram/gen_flow.py
"""
import json
import sys

sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from kit import Canvas, INK, RED, GREEN, BLUE, GREY, FAINT, mark_deltas
from to_svg import (to_svg, overflow_report, collision_report,
                    text_overlap_report)

c = Canvas()
X = 300
SP_X, SP_W = 660, 600          # the spine — the steps themselves
L_X = 300                       # left gutter — step number and kind
R_X = 1320                      # right gutter — artifacts, approvals, notes

# ── title ────────────────────────────────────────────────────────────────
c.txt("Frame the intent — stage flow", X, 80, 32)
c.txt("PRODUCT rung · function 1 of 5 · interviewed 2026-08-03\n"
      "sequence, branches, artifacts and approvals for ONE stage. the board says "
      "what it must do; this says how it runs.", X, 124, 15)
c.txt("DECISIONS are dashed  ·  ARTIFACTS are listed right", X, 172, 14, INK)
c.txt("RED — cost, or a route that leaves the stage / blocks it", X, 192, 14, RED)
c.txt("GREEN — Tony's input into the work: his annotations, his corrections",
      X, 212, 14, GREEN)
c.txt("BLUE — changed since you last marked this reviewed", X, 232, 14, BLUE)

y = 288


def step(n, kind, title, body, artifact="", note="", colour=INK, dashed=False,
         h=None):
    """One box on the spine, with its number/kind left and artifacts right."""
    global y
    # Box height follows the TITLE. The body renders below the box, so sizing
    # the box from body length just inflated the decision steps into tall
    # empty rectangles.
    bh = h or max(60, 30 + (title.count("\n") + 1) * 22)
    c.txt(f"{n}", L_X, y + 6, 26, colour)
    c.txt(kind, L_X + 44, y + 12, 13, colour)
    c.box(title, SP_X, y, SP_W, bh, stroke=colour,
          bg=GREY if not dashed and colour == INK else "transparent",
          size=14, dashed=dashed)
    if body:
        c.txt(body, SP_X + 18, y + bh + 8, 12, INK)
    if artifact:
        c.txt(artifact, R_X, y + 4, 12, colour)
    if note:
        c.txt(note, R_X, y + 4 + (artifact.count("\n") + 2) * 15, 12, RED)
    y += bh + (17 * (body.count("\n") + 1) + 22 if body else 26)
    return bh


def down(gap=34, colour=INK, dashed=False, label=""):
    """Arrow along the spine to the next step."""
    global y
    cx = SP_X + SP_W / 2
    c.arrow([(cx, y), (cx, y + gap)], stroke=colour, dashed=dashed)
    if label:
        c.txt(label, cx + 16, y + gap / 2 - 8, 12, colour)
    y += gap


# ── 1 ────────────────────────────────────────────────────────────────────
step("1", "IN", "Something arrives",
     "an idea · a product · a feature · an enhancement · a thought · a question ·\n"
     "a comparison to another product, competitor, company or repo ·\n"
     "an issue · a complaint",
     artifact="no artifact yet.\nthis is raw input.")
down()

# ── 2 ────────────────────────────────────────────────────────────────────
step("2", "CAPTURE", "Capture it properly",
     "an interview  ·  uploaded evidence  ·  or a whiteboard session.\n"
     "the mode is chosen to suit what arrived, not by default.",
     artifact="VISUAL: whiteboard\ncanvas, if that is the\nmode chosen")
down()

# ── 3 — triage ───────────────────────────────────────────────────────────
step("3", "DECISION", "TRIAGE — which route is this?",
     "the branch is here, and everything downstream depends on it.",
     artifact="the route, recorded.\nit is an output, not a\nprivate judgement.",
     dashed=True)

# three exits drawn as a fan
_fan_y = y
cx = SP_X + SP_W / 2
c.arrow([(cx, _fan_y), (cx, _fan_y + 26), (SP_X + 150, _fan_y + 26),
         (SP_X + 150, _fan_y + 56)])
c.arrow([(cx, _fan_y), (cx, _fan_y + 26), (SP_X + 450, _fan_y + 26),
         (SP_X + 450, _fan_y + 56)])
c.arrow([(cx, _fan_y), (cx, _fan_y + 26), (R_X + 130, _fan_y + 26),
         (R_X + 130, _fan_y + 56)], stroke=RED, dashed=True)
y = _fan_y + 56

c.box("NEW\nidea · feature · enhancement", SP_X, y, 290, 56, stroke=INK,
      bg=GREY, size=13)
c.box("PROBLEM\nissue · complaint · broken", SP_X + 310, y, 290, 56,
      stroke=INK, bg=GREY, size=13)
c.box("QUESTION\nabout the product", R_X, y, 260, 56, stroke=RED,
      size=13, dashed=True)
c.txt("LEAVES THIS STAGE.\nanswered from Hold product\ntruth — not framed as new\n"
      "work. framing a question as\na feature is how invented\nwork gets started.",
      R_X + 276, y + 2, 12, RED)
y += 86

# ── 4 — grounding, branch-dependent ──────────────────────────────────────
c.arrow([(SP_X + 145, y - 30), (SP_X + 145, y)])
c.arrow([(SP_X + 455, y - 30), (SP_X + 455, y)])
c.txt("4", L_X, y + 6, 26)
c.txt("GROUNDING\nread before\nyou produce\nANYTHING", L_X + 44, y + 12, 13)
c.box("competitor scan\n+ evidence of need\n\nthere may be no current\nsituation to read",
      SP_X, y, 290, 108, stroke=INK, size=13)
c.box("read the CURRENT situation\ncode · infra · product specs\nTHEN the gap analysis\n\n"
      "no proposal before the\npresent state is read",
      SP_X + 310, y, 290, 108, stroke=INK, size=13)
c.txt("this column is the entry\ngate's real job. inputs\narrive on their own —\n"
      "grounding is what gets\nskipped.", R_X, y + 4, 12, RED)
y += 138

# ── 5 — tool route ───────────────────────────────────────────────────────
c.arrow([(SP_X + 145, y - 30), (SP_X + 300, y - 30), (SP_X + 300, y)])
c.arrow([(SP_X + 455, y - 30), (SP_X + 300, y - 30), (SP_X + 300, y)])
step("5", "DECISION", "Does a tool's route match?",
     "a tool declares the route it serves. you invoke it ON MATCH — not because\n"
     "it exists, and not as an obligation.\n"
     "  SENSEI  — asserting a position · proving a gap or an idea with measurement ·\n"
     "            a complex problem needing point of cause and 5 whys.\n"
     "            TRIGGER: a problem that survived a few attempts to fix it.\n"
     "  otherwise — skip it. most work does not need it.",
     artifact="VISUAL: if sensei is\ninvoked, the pattern's\nown diagram, conforming\n"
              "to that pattern's rules,\nwith measurements.",
     note="BET: sensei is PROVEN —\nextensively used in\n~/toyota-sensei and other\n"
          "projects. what is untested\nis TRANSFER into Kerd.\nthe bet is the move,\n"
          "not the method.",
     dashed=True)
down()

# ── 6 — produce. TWO documents, not one shape ────────────────────────────
# Drawn as one converged box first. Tony's call: a new-idea doc and a problem
# doc do not have the same sections, so the branch that opened at triage stays
# open through output and only closes at acceptance.
c.arrow([(SP_X + 300, y), (SP_X + 300, y + 20), (SP_X + 145, y + 20),
         (SP_X + 145, y + 46)])
c.arrow([(SP_X + 300, y), (SP_X + 300, y + 20), (SP_X + 455, y + 20),
         (SP_X + 455, y + 46)])
y += 46
c.txt("6", L_X, y + 6, 26)
c.txt("OUT\ntwo documents,\nnot one shape\nwith optional\nsections", L_X + 44, y + 12, 13)
c.box("IDEA BRIEF", SP_X, y, 290, 40, stroke=INK, bg=GREY, size=13)
c.box("PROBLEM STATEMENT", SP_X + 310, y, 290, 40, stroke=INK, bg=GREY, size=13)
c.txt("what it is\n"
      "what it must become\n"
      "what gap it addresses\n"
      "how it compares to other\n"
      "  products / competitors\n"
      "its value\n"
      "a viability SIGNAL\n"
      "  — not a verdict\n"
      "the next stage's inputs",
      SP_X + 12, y + 50, 12)
c.txt("what is happening now\n"
      "  — read from code, infra,\n"
      "  product specs, not assumed\n"
      "what should be happening\n"
      "the gap between them, MEASURED\n"
      "point of cause, if the sensei\n"
      "  trigger fired at step 5\n"
      "the value of closing it\n"
      "the next stage's inputs",
      SP_X + 322, y + 50, 12)
c.txt(".md — machine-read,\nlong-read, measurable,\nhandoff-ready.\n\n"
      "VISUAL: a diagram of the\nidea, the interaction,\nthe flow.\n\n"
      "BOTH routes produce a doc\nAND a diagram. it is the\nSECTIONS that differ,\n"
      "not the artifact types.", R_X, y + 4, 12)
y += 210
c.arrow([(SP_X + 145, y - 22), (SP_X + 145, y - 8), (SP_X + 300, y - 8),
         (SP_X + 300, y + 20)])
c.arrow([(SP_X + 455, y - 22), (SP_X + 455, y - 8), (SP_X + 300, y - 8),
         (SP_X + 300, y + 20)])
y += 20
down()

# ── 7 — acceptance ───────────────────────────────────────────────────────
step("7", "APPROVAL", "Acceptance — TWO KEYS  (the routes converge here)",
     "MACHINE: the sections are present — WHICH sections depends on the route ·\n"
     "         the measurements are stated · the diagram conforms to the pattern\n"
     "         it claims · the next stage's declared inputs are all filled.\n"
     "HUMAN:   Tony says approve.\n"
     "neither key alone passes. shared machinery, route-specific checklist.",
     artifact="the approval itself is\nrecorded. an unnamed\napproval is how the\n"
              "design gate went missing.",
     dashed=True)

# fail loop back to 6
_fy = y
c.arrow([(SP_X, _fy - 96), (SP_X - 46, _fy - 96), (SP_X - 46, _fy - 250),
         (SP_X, _fy - 250)], stroke=RED, dashed=True)
c.txt("FAILS →\nback to\nproduce", SP_X - 132, _fy - 190, 12, RED)
down()

# ── 8 — unclosed risk ────────────────────────────────────────────────────
step("8", "OUT", "Anything that could not be closed",
     "every gap or risk left open is DOCUMENTED and CONFIRMED.\n"
     "carried is fine. silent is not.",
     artifact="written into the .md,\nnot held in the session.")
down()

# ── 9 — handoff ──────────────────────────────────────────────────────────
step("9", "HANDOFF", "→ Test viability  (PRODUCT, function 2)  — BOTH routes",
     "same destination for both. the KILLER ASSUMPTION differs; the test does not.\n"
     "  IDEA BRIEF        — is the need real, and can we win?\n"
     "  PROBLEM STATEMENT — is the cause correctly located, and is closing the\n"
     "                      gap worth what it costs?\n"
     "a problem statement going straight to DESIGN is the jump-to-countermeasure\n"
     "failure. the risk is HIGHEST on that route, so it is the last place to skip.",
     artifact="the next stage runs its\nOWN entry gate against\nwhat arrived here.\n\n"
              "carries a viability SIGNAL,\nnever a verdict.")

# ── footer ───────────────────────────────────────────────────────────────
c.txt("Settled: TRIAGE is a branch inside ONE function, not a fork between two. "
      "The routes diverge\nat grounding (4), stay apart through output (6), and "
      "rejoin at acceptance (7) — shared\nmachinery, route-specific checklist. Both "
      "hand off to the same place.\n\n"
      "Two things this stage still owes: the route-specific acceptance checklists "
      "are named but not\nwritten, and neither document has a declared home or "
      "naming rule — that is blocked on the\ncross-cutting \"Where the work is "
      "written down\", which is still drafted and unagreed.",
      X, y + 40, 15, RED)

# ── write ────────────────────────────────────────────────────────────────
# ── merge the open annotation queue back in ──────────────────────────────
# Annotations are a QUEUE, not an archive. Tony's comments are captured here,
# acted on, then DELETED — the substance moves into the diagram, the generator
# or a decision record, and the disposition is logged in annotations/log.md so
# nothing vanishes silently. Only unanswered comments should be in this file.
#
# This is also what fixes annotation drift: a preserved comment kept absolute
# position but not attachment, so it slid away from what it annotated whenever
# the layout reflowed. A comment that lives one cycle cannot drift.
#
# Ownership note: customData {gen: kerd} is NOT a reliable marker. Excalidraw
# propagates customData onto newly drawn elements, so Tony's own comments came
# back tagged as ours. Element ids fail too — they are reassigned on paste.
# What works is diffing the clipboard against the generated file by text.
import os
_ann = ("/Users/anthonymaley/Kerd/docs/plans/annotations/"
        "2026-08-03-frame-the-intent-tony.json")
if os.path.exists(_ann):
    _a = json.load(open(_ann))["elements"]
    for _e in _a:
        _e.setdefault("customData", {})["author"] = "tony"
        _e["index"] = "z" + str(len(c.els)).zfill(4)
        c.els.append(_e)
    print(f"merged {len(_a)} preserved annotation(s)")

out = "/Users/anthonymaley/Kerd/docs/plans/2026-08-03-frame-the-intent-flow.excalidraw"
_marked, _supp = mark_deltas(c.els, out)
if _marked or _supp:
    print(f"blue: {_marked} changed since last reviewed"
          + (f" ({_supp} kept red/green — those meanings outrank newness)"
             if _supp else ""))
else:
    print("blue: nothing marked (no reviewed snapshot yet — "
          "run mark_reviewed.py once you have read it)")

doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
       "elements": c.els,
       "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
       "files": {}}

json.dump(doc, open(out, "w"), indent=1)
print("wrote", out)
print(f"elements: {len(c.els)}")

svg_out = out.replace(".excalidraw", ".svg")
w, h = to_svg(c.els, svg_out)
print("wrote", svg_out, f"({w:.0f}x{h:.0f})")

for label, faults, fmt in (
        ("bound-text overflow", overflow_report(c.els),
         lambda f: f"{f[0][:52]:<52} text {f[1]}px > box {f[2]}px"),
        ("text/box collision", collision_report(c.els),
         lambda f: f"{f[0]:<46} at ({f[1]},{f[2]})"),
        ("text/text overlap", text_overlap_report(c.els),
         lambda f: f"{f[0]:<40} over {f[1]:<40} at ({f[2]},{f[3]})")):
    if faults:
        print(f"!! {len(faults)} {label}(s):")
        for f in faults:
            print("   " + fmt(f))
    else:
        print(f"no {label}s")
