#!/usr/bin/env python3
"""Progress HTML — design package diagram.

    python3 tools/diagram/gen_progress_html.py

Draws docs/design/progress-html.md for the design conversation: the one
file you open, the page anatomy, the grown write path, the freshness
anchor's self-reference catch, determinism, proof, and named scope.
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

f = Flow("Progress HTML — the view you open · design package",
         "slice 1 of docs/product/progress-html.md — born from the expert-user\n"
         "pass: 'where are we?' becomes opening a file.")
SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

# ── 1 — now vs the change ────────────────────────────────────────────────
f.step("1", "NOW", "Terminal table, static SVG, drill-down by command",
       "'really manual and hard to consume quickly' (Tony, at the\n"
       "push-wiring goal gate). detail on demand = more terminal commands.",
       artifact="the expert-user pass\nfound this - the machinery\n"
                "was sound, the human pull\nsurface was not.",
       colour=RED)
f.down()

f.step("2", "CHANGE", "docs/plans/progress.html — committed, self-contained",
       "open it cold over file:// -> board at a glance, every goal strip,\n"
       "click a goal -> its pieces + per-rung named have/need, verbatim\n"
       "from the gate kit. read-only. zero external requests.",
       artifact="inline CSS + vanilla JS +\nmodel and gate detail as an\n"
                "inlined JSON block. system\nfont stack. nothing polls,\n"
                "nothing mutates.")
f.down()

# ── 3 — the write path grows ─────────────────────────────────────────────
f.step("3", "MECHANISM", "write_pair becomes write_surfaces(model, canvas, dir)",
       "ONE serializer of ALL committed view surfaces: .excalidraw, .svg,\n"
       "and now progress.html. render and stale both write through it;\n"
       "the byte-compare set becomes a TRIO. FIX_LINE grows to add the\n"
       "third file; F12's spelled literal updated with it.")
_y = f.y
f.box("no new CI step\nthe existing seventh step covers the trio -\nstale compares whatever write_surfaces writes",
      SP_X, _y, 380, 70, stroke=INK, bg=GREY, size=13)
f.txt("amends push-wiring's design\ndoc: 'both files' becomes\n"
      "'all three' when this ships\n(named cross-doc impact).",
      R_X, _y + 2, 12)
f.y = _y + 96
f.down()

# ── 4 — the catch ────────────────────────────────────────────────────────
f.step("4", "CATCH", "The freshness anchor must not be HEAD",
       "the page names what it reflects - but the commit that STORES the\n"
       "page moves HEAD, so a HEAD stamp re-stales every fresh compare:\n"
       "permanent deadlock. same killer class as push-wiring's probe.",
       artifact="")
_y = f.y
f.box("ANCHOR = MODEL-DERIVED, so it converges by construction:\n"
      "newest landed-piece commit (sha + subject, from trailer evidence)\n"
      "+ a state fingerprint (md5 of the canonical model JSON).\n"
      "both change exactly when the picture changes; render-only\n"
      "commits change neither. no timestamps, no HEAD, no randomness.",
      SP_X, _y, 600, 110, stroke=RED, size=13)
f.y = _y + 136
f.down()

# ── 5 — determinism ──────────────────────────────────────────────────────
f.step("5", "EVIDENCE", "Why the byte-compare stays safe",
       "same discipline that proved the pair: sorted iteration, values\n"
       "derived only from model + gate detail, no time, no random.\n"
       "fixture F14 asserts two consecutive generations byte-identical.",
       dashed=True)
f.down()

# ── 6 — proof ────────────────────────────────────────────────────────────
f.step("6", "PROOF", "Fixtures + the cold open",
       "F14 determinism · F11-F13 amended to the trio (converged 0 /\n"
       "drifted 1 all three named, new fix line as spelled literal /\n"
       "missing 1) · both-ways demonstration at ship · then the\n"
       "expert-user pass: Tony opens the committed page cold over\n"
       "file:// and answers 'where are we?' with zero terminal.",
       artifact="the three stage-1\nmeasurements, ANSWERED:\n\n"
                "actions -> open one file.\ndetail -> in the page,\n"
                "one click. trust -> the\nfreshness line + the trio\n"
                "compare in CI step 7.")
f.down()

# ── 7 — scope ────────────────────────────────────────────────────────────
f.step("7", "SCOPE", "Out of scope, named (composer key on the frame)",
       "live refresh / watch mode - any server - any control that\n"
       "mutates - replacing the SVG or terminal surfaces.\n"
       "each returns only through its own frame.",
       colour=GREEN, dashed=True)

# Tony's standing font call (2026-08-04): design packages read in Nunito.
for _e in f.els:
    if _e["type"] == "text":
        _e["fontFamily"] = 6

out = os.path.join(REPO, "docs", "design", "progress-html.excalidraw")
_ann = os.path.join(REPO, "docs", "plans", "annotations",
                    "progress-html-tony.json")
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
