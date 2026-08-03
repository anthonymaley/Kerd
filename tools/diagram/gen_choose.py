#!/usr/bin/env python3
"""Choose what matters next — a WORKING decision view, not a spec.

Tony could not name the axes in the abstract, which is fair: axes are easier to
judge against real items than to derive. So this renders the actual Kerd backlog
on a candidate pair and lets the picture argue for or against itself.

Axes (Tony, 2026-08-03): CONSEQUENCE x VALUE.

  CONSEQUENCE — what it costs us NOT to do this.
  VALUE       — what we gain by doing it. Already a declared quantity: Frame
                the intent states it, Test viability measures impact against
                it. Third caller for the same number, not a new measure.

EFFORT was the first cut and it was wrong. It is an INPUT measure sitting
beside an OUTCOME measure, which makes the grid incoherent — and it flattered
cheap work. Effort survives as a tiebreaker inside a cell, and as one of the
five slicing factors at Slice a release. It is not an axis.

Blocked items are drawn apart, because a dependency is a hard constraint (agreed
at Slice a release) and an unreachable item is not a candidate at all.

    python3 tools/diagram/gen_choose.py
"""
import json
import sys

sys.path.insert(0, "/Users/anthonymaley/Kerd/tools/diagram")
from kit import Canvas, INK, RED, GREY, FAINT
from to_svg import (to_svg, overflow_report, collision_report,
                    text_overlap_report)

c = Canvas()
X, Y = 300, 80

c.txt("Choose what matters next — the real backlog, on candidate axes", X, Y, 30)
c.txt("PRODUCT rung · function 5 · a working instance, not a specification\n"
      "the axes are a PROPOSAL. the point is to react to the picture, not to "
      "derive axes in the abstract.", X, Y + 42, 15)
c.txt("each item carries WHAT WE LOSE by not choosing it — the v0.68 rule "
      "(name the loss, or it disappears into the good news) applied to work.",
      X, Y + 88, 14, RED)

# ── banded rows, not a scatter ───────────────────────────────────────────
# First cut was a free scatter. It collided — loss labels overlapping each
# other and the frame — which is the noise problem itself, rendered. Bands are
# the same two axes with a structure you can scan: consequence groups the
# rows, effort orders within the group.
BX_, BY_, BW = X + 20, Y + 130, 1240
C_ITEM, C_EFF, C_LOSS = BX_ + 16, BX_ + 300, BX_ + 400

c.txt("WHAT WE WOULD LOSE BY NOT DOING IT", C_LOSS, BY_ - 22, 12)
c.txt("VALUE", C_EFF, BY_ - 22, 12)

BANDS = [
 ("HIGH CONSEQUENCE — these change what is possible, or block everything else",
  RED, [
   ("CI — nothing can refuse", "HIGH",
    "every rule stays a model choosing to comply. and /loop cannot run at all\n"
    "where nothing can refuse — so this GATES the loop, it does not just guard it."),
   ("Finish the requirements walk", "HIGH",
    "20 functions stay drafted; nothing downstream of them can start."),
   ("Run v0.66-v0.68 for real", "MED",
    "three releases stay unverified prompt text. verification, not new capability."),
   ("Repin leru + krutho x2 to current cache", "LOW",
    "one cache GC from breaking silently, in three repos.\n"
    "PURE HYGIENE — high consequence, no value. under EFFORT this looked like a\n"
    "cheap win; under VALUE it is revealed as maintenance."),
 ]),
 ("MEDIUM — worth doing, none of it urgent", INK, [
   ("The SPIKE — route one dead skill", "HIGH",
    "route-vs-rip stays a coin flip. HIGHEST VALUE in this band: it settles the\n"
    "fate of four dead skills with one cheap test."),
   ("Hook staleness check in tend", "MED",
    "the manual sweep only ever fixes the repo you happen to be looking at."),
   ("Settle the 'reachable' clause", "HIGH",
    "artifacts stay findable but not reached — today's unsolved one, and it\n"
    "blocks every artifact from being useful rather than merely stored."),
   ("Acceptance checklists (function 1 debt)", "MED",
    "the machine key cannot check route-specific sections without them."),
   ("Guard switch-in smoke test", "MED",
    "build-heavy repos flood a lean pickup with raw output."),
 ]),
 ("LOW — genuinely ignorable, and you can see what ignoring costs", INK, [
   ("Vault commit decision", "LOW", "contract and behaviour keep disagreeing."),
   ("CHANGELOG — revive or delete", "LOW",
    "stale at 0.14.0 while the repo is at 0.68.0."),
   ("Surface model-tiered delegation", "LOW", "open since v0.64.0."),
   ("Kerd.md MOC version field", "LOW", "says 0.31.0."),
 ]),
]

by = BY_
for title, colour, rows in BANDS:
    bh = 40 + len(rows) * 46
    c.rect(BX_, by, BW, bh, stroke=colour,
           dashed=(colour == RED))
    c.txt(title, BX_ + 16, by + 10, 14, colour)
    ry = by + 38
    for item, eff, loss in rows:
        c.box(item, C_ITEM, ry, 270, 32, stroke=colour,
              bg="transparent" if colour == RED else GREY, size=12)
        c.txt(eff, C_EFF, ry + 9, 12, colour)
        c.txt(loss, C_LOSS, ry + 2, 12, colour)
        ry += 46
    by += bh + 16

PW, BY = BW, by + 30

# ── blocked strip ────────────────────────────────────────────────────────
c.rect(X + 20, BY, PW, 118, stroke=RED, dashed=True)
c.txt("BLOCKED — not candidates at all. a dependency is a hard constraint, so "
      "these cannot be 'next' at any consequence.", X + 36, BY + 12, 14, RED)
for i, (lab, why) in enumerate((
        ("Dogfood sherpa on ~/Bree", "sherpa may be routed,\nreshaped or ripped"),
        ("Mode reconciliation", "same decision as sherpa"),
        ("skriv voice profile", "needs non-founder-genre\nsamples"))):
    c.box(lab, X + 40 + i * 400, BY + 40, 300, 30, stroke=RED, size=12)
    c.txt(why, X + 40 + i * 400, BY + 76, 11, RED)

# ── what the picture says ────────────────────────────────────────────────
c.txt("WHAT THIS PICTURE SAYS, that a ranked list did not:", X, BY + 130, 17, RED)
c.txt("· CI is HIGH on BOTH, and alone in that. it does not merely guard the "
      "work — /loop cannot run at all where\n"
      "  nothing can refuse, so it GATES the loop. nothing else on the board "
      "unblocks a whole capability.\n"
      "· 'Repin the three repos' is HIGH CONSEQUENCE, NO VALUE — pure hygiene. "
      "under the first cut (effort x consequence)\n"
      "  it read as a cheap win and rose. swapping effort for value demoted it "
      "correctly: it prevents harm, it adds nothing.\n"
      "· 'The SPIKE' rose for the same reason, in reverse — medium consequence, "
      "HIGH value, because one cheap test\n"
      "  settles the fate of four dead skills. effort had hidden that entirely.\n"
      "· the LOSS column is what makes the bottom band safe to ignore. you can "
      "see the cost of ignoring it.",
      X, BY + 160, 13)
c.txt("WHY EFFORT WAS WRONG: it is an INPUT measure sitting beside an OUTCOME "
      "measure, which makes the grid incoherent —\n"
      "and it systematically flatters cheap work. effort survives as a "
      "tiebreaker inside a cell, and as one of the five\n"
      "slicing factors at Slice a release. it is not an axis.",
      X, BY + 290, 14, RED)

out = "/Users/anthonymaley/Kerd/docs/plans/2026-08-03-choose-what-matters-view.excalidraw"
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
    print(f"!! {len(faults)} {label}(s): {faults[:4]}" if faults
          else f"no {label}s")
