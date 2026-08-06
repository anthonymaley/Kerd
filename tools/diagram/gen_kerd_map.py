#!/usr/bin/env python3
"""Kerd as a whole — the living system map.

    python3 tools/diagram/gen_kerd_map.py

One page: the nine skills and their jobs, the ladder
the work climbs, and the machinery that refuses from outside the model.
Living doc — regenerate on structural change; blue deltas vs the last
mark_reviewed baseline.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from kit import Canvas, INK, RED, GREEN, GREY, mark_deltas  # noqa: E402
from to_svg import (to_svg, overflow_report, collision_report,  # noqa: E402
                    text_overlap_report)

c = Canvas()
X0 = 300

# ── title + legend ───────────────────────────────────────────────────────
c.txt("Kerd — the whole system, current state (v0.87.0)", X0, 80, 30)
c.txt("skills are what you invoke · the ladder is what work climbs · "
      "the machinery refuses from outside the model",
      X0, 122, 14)
c.txt("RED (dashed) — dying or under review as a cut candidate", X0, 150, 12, RED)
c.txt("GREEN — Tony's keys live here", X0, 168, 12, GREEN)
c.txt("grey — machinery, not skills: nothing to install, push-to-main = released",
      X0 + 260, 168, 12)

# ── band 1: the nine skills ───────────────────────────────────────────────
c.txt("THE NINE SKILLS — invoked as /kerd:<name>, loaded from the installed plugin version",
      X0, 196, 16)

BW, BH, GAP = 270, 96, 20
row1_y, row2_y = 246, 362
cluster = [
    ("SESSION FLOW", X0, [
        ("switch", "the boundary: pull, handoff,\nsession-state commit;\nreads 3 files, writes 3 kinds", INK),
        ("conductor", "the performance: orient, plan,\nexecute, close; four roles —\nyou compose, players execute", INK),
        ("pair", "partner-mode toggle (hook):\nrapid back-and-forth,\none speech-bubble question", INK),
    ]),
    ("KNOWLEDGE", X0 + (BW + GAP) * 3 + 40, [
        ("kivna", "the vault interface:\nhuman-first knowledge base,\non-demand since v0.83.0", INK),
        ("skriv", "human voice for prose:\naudit, fix, or write —\nnever code or commits", INK),
    ]),
]
cluster2 = [
    ("HEALTH", X0, [
        ("tend", "converge repo structure\nto current conventions;\nnever commits", INK),
        ("slainte", "release close-out pass: triggered\nat version bumps + goal records,\nfixes doc drift, restraint reported", INK),
    ]),
    ("QUALIFY & DISCOVER", X0 + (BW + GAP) * 3 + 40, [
        ("interrogate", "UNDER REVIEW - the ledger\nSTANDARD is load-bearing;\ndoes the skill earn its place?", RED),
        ("lorg", "UNDER REVIEW - cut candidate:\nclaude plugin manages now;\ngap analysis never exercised", RED),
    ]),
]
for label, x0, skills in cluster:
    c.txt(label + "   ", x0, row1_y - 18, 12)
    for i, (name, job, col) in enumerate(skills):
        x = x0 + i * (BW + GAP)
        c.box(f"{name}", x, row1_y, BW, 26, stroke=col, size=14,
              bg=GREY if col is INK else "transparent")
        c.txt(job, x + 10, row1_y + 32, 12, col)
for label, x0, skills in cluster2:
    c.txt(label + "   ", x0, row2_y - 18, 12)
    for i, (name, job, col) in enumerate(skills):
        x = x0 + i * (BW + GAP)
        c.box(f"{name}", x, row2_y, BW, 26, stroke=col, size=14,
              bg=GREY if col is INK else "transparent",
              dashed=(col is RED))
        c.txt(job, x + 10, row2_y + 32, 12, col)

c.txt("cut and gone (dead solutions stay dead): capturerequirements v0.73 · "
      "sherpa v0.74 · mode + all eleven modes/ v0.75",
      X0, 474, 12, RED)

# ── band 2: the ladder ───────────────────────────────────────────────────
lad_y = 534
c.txt("THE LADDER — every work item climbs it; gates route by what exists on disk",
      X0, lad_y - 26, 16)
RUNGS = ["frame", "viability", "slice", "design", "contract", "build",
         "goal", "loop"]
LW, LH, LG = 118, 40, 24
for i, r in enumerate(RUNGS):
    x = X0 + i * (LW + LG)
    c.box(r, x, lad_y, LW, LH, size=14)
    if i:
        c.arrow([[x - LG + 2, lad_y + LH / 2], [x - 2, lad_y + LH / 2]])
c.txt("human keys (GREEN): frame value + slice · design GO on the canvas · "
      "the expert-user pass at goal — everything else is machine-checked",
      X0, lad_y + LH + 12, 12, GREEN)
c.txt("records: docs/product/<slug>.md (living) · docs/gates/<date>-<slug>-<rung>.md "
      "(immutable) · docs/plans/<date>-<slug>-spec.md (the contract)",
      X0, lad_y + LH + 32, 12)

# ── band 3: the machinery ────────────────────────────────────────────────
mach_y = 678
c.txt("THE MACHINERY — refuses from outside the model, on every push; "
      "not skills, not installed, released by push-to-main",
      X0, mach_y - 26, 16)
MW, MH = 270, 110
mach = [
    ("tools/gates", "router + refuser:\ngate table per rung,\naudit AU1-AU6,\nrelease rules R1-R3"),
    ("tools/diagram", "progress board derived\nfrom disk + the stale\nrefuser (5 catches) +\ndesign canvas kit"),
    ("tools/design", "evaluation matrix\nchecker: declared\ncriteria, scored basis,\narithmetic recomputed"),
    ("CI - seven steps", "gate selftest · audit ·\nrelease · progress selftest\n· matrix selftest · matrix\naudit · render current"),
]
for i, (name, job) in enumerate(mach):
    x = X0 + i * (MW + GAP)
    c.box(name, x, mach_y, MW, 26, size=14, bg=GREY)
    c.txt(job, x + 10, mach_y + 32, 12)

c.txt("the skills advise and structure; the machinery is what can say no. "
      "rigor level (AU6) is the newest refusal: every Release slice declares "
      "spike / mvp / production-v1.",
      X0, mach_y + MH + 22, 12)

# Tony's font call 2026-08-04: packages read in Nunito (6).
for _e in c.els:
    if _e["type"] == "text":
        _e["fontFamily"] = 6

out = os.path.join(REPO, "docs", "design", "kerd-map.excalidraw")
mark_deltas(c.els, out)
json.dump({"type": "excalidraw", "version": 2,
           "source": "https://excalidraw.com", "elements": c.els,
           "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
           "files": {}}, open(out, "w"), indent=1)
print("wrote", out, f"| elements: {len(c.els)}")
w, h = to_svg(c.els, out.replace(".excalidraw", ".svg"))
print(f"svg {w:.0f}x{h:.0f}")
for label, faults in (("bound-text overflow", overflow_report(c.els)),
                      ("text/box collision", collision_report(c.els)),
                      ("text/text overlap", text_overlap_report(c.els))):
    print(f"!! {len(faults)} {label}(s): {faults[:3]}" if faults
          else f"no {label}s")
