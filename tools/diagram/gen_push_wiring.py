#!/usr/bin/env python3
"""Push wiring — the staleness refuser. Design package diagram.

    python3 tools/diagram/gen_push_wiring.py

Draws docs/design/push-wiring.md for the design conversation: the ship
flow now vs under the gate, the stale check, the CI wiring (and the
shallow-checkout defect caught at design time), the determinism evidence,
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

f = Flow("Push wiring — the staleness refuser · design package",
         "the ladder's first passenger · slice 1 of docs/product/push-wiring.md\n"
         "forgetting the refresh becomes a refusal, not a drift.")
SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

# ── 1 — now vs the change ────────────────────────────────────────────────
f.step("1", "NOW", "The ship flow today",
       "commit work (Piece: trailer) -> push. the render refreshes only when\n"
       "someone remembers, in a later commit, maybe a later push.",
       artifact="measured 2026-08-04:\ntwo manual rounds in one\n"
                "session; between them the\ncommitted render MISSTATES\n"
                "position (mode-cut strip:\n'9 landed' after all 11).",
       colour=RED)
f.down()

f.step("2", "CHANGE", "The ship flow under the gate",
       "commit -> refresh -> commit the render pair -> ONE push.\n"
       "CI step 7 byte-compares fresh vs committed at every pushed tip;\n"
       "different = refused, and the message carries the exact fix.",
       artifact="named cost (ledger row 3,\nRED): a per-piece push is\n"
                "now a two-commit pair; a\nforgotten refresh costs one\n"
                "extra local round.\n\n"
                "a push touching nothing the\nrender reads compares equal\n"
                "and passes untouched.")
f.down()

# ── 3 — the stale check mechanism ────────────────────────────────────────
f.step("3", "MECHANISM", "progress.py stale — check-only, mutates nothing",
       "render the pair to a TEMP dir (never the working tree) ->\n"
       "byte-compare each against docs/plans/progress.{excalidraw,svg}\n"
       "on disk. in CI, disk IS the pushed tip; locally the answer is\n"
       "'would CI refuse this tree?'. both files compared - a hand-edited\n"
       "SVG is drift too.")
_y = f.y
f.box("EXIT 0\nboth identical\nprints: render current",
      SP_X, _y, 250, 84, stroke=INK, bg=GREY, size=13)
f.box("EXIT 1\nany difference, or either file missing\nnames each file + the fix VERBATIM:\nrun the renderer, add the pair, commit",
      SP_X + 270, _y, 330, 84, stroke=RED, size=13)
f.txt("convergence: render-only\ncommits carry NO trailer,\n"
      "so refresh divergence stops\nat depth 1 (probed 2026-08-04,\n"
      "md5 pair identical).",
      R_X, _y + 2, 12)
f.y = _y + 110
f.down()

# ── 4 — CI wiring + the caught defect ────────────────────────────────────
f.step("4", "CI", "Seventh step — and a defect caught at design time",
       "gate.yml gains: 'Progress render current' -> python3\n"
       "tools/diagram/progress.py stale, after Matrix audit.",
       artifact="")
_y = f.y
f.box("DEFECT FOUND: actions/checkout@v4 defaults to DEPTH 1.\n"
      "the renderer derives landed pieces from git log trailers -\n"
      "a shallow checkout sees ONE commit, derives an emptier model,\n"
      "and refuses EVERY push. the fix ships with this slice:\n"
      "checkout gains fetch-depth: 0.",
      SP_X, _y, 600, 110, stroke=RED, size=13)
f.txt("same bug class as the 0.71.1\nabsolute-REPO refusal: local\n"
      "verifies pass in an environment\nCI doesn't have. the progress\n"
      "selftest never noticed - its\nfixtures build their own trees.",
      R_X, _y + 2, 12, RED)
f.y = _y + 136
f.down()

# ── 5 — determinism evidence ─────────────────────────────────────────────
f.step("5", "EVIDENCE", "Why an exact byte-compare is safe",
       "read from the toolkit 2026-08-04: ids counter-based, seeds\n"
       "arithmetic (10000 + n*7) · no random, no time/date anywhere ·\n"
       "every output-feeding glob sorted() · REPO root-independent since\n"
       "0.71.1 · SVG text metrics are pure arithmetic, no font query.",
       artifact="RESIDUAL, named: Mac vs\nLinux byte-identity is\n"
                "UNPROVEN until the first CI\nrun - the ship run IS the\n"
                "proof. if it ever diverges:\nnormalise before compare,\n"
                "never weaken to a semantic\ndiff.",
       dashed=True)
f.down()

# ── 6 — proof plan ───────────────────────────────────────────────────────
f.step("6", "PROOF", "Fixtures + the both-ways demonstration",
       "selftest gains three temp-tree fixtures: converged -> 0 ·\n"
       "drifted (source changed after render) -> 1 naming both files,\n"
       "fix line asserted VERBATIM · missing pair -> 1.\n"
       "at ship, refusal demonstrated both ways on the real tree\n"
       "(planted stale render -> 1; refreshed pair -> 0), the 0.70.0\n"
       "pattern.",
       artifact="the two stage-1 measurements,\nANSWERED:\n\n"
                "staleness at a push tip -> 0:\nCI refuses any differing tip.\n\n"
                "remember-steps -> 0: nothing\nremembered - forgetting yields\n"
                "a refusal carrying the fix\n(fixture-checked).")
f.down()

# ── 7 — out of scope ─────────────────────────────────────────────────────
f.step("7", "SCOPE", "Out of scope, named (composer key on the frame)",
       "AUTO-PUSH of the refreshed render (hook or CI-side commit): the\n"
       "ledger's accepted unknown stands untested - review trigger fires\n"
       "if any slice proposes CI write-back.\n"
       "GATE.PY rendering have/need through the progress view: a later\n"
       "slice.",
       artifact="", colour=GREEN, dashed=True)

# Tony's font call 2026-08-04: the package reads in Nunito (6), not the
# hand-drawn Excalifont the kit defaults to.
for _e in f.els:
    if _e["type"] == "text":
        _e["fontFamily"] = 6

out = os.path.join(REPO, "docs", "design", "push-wiring.excalidraw")
_ann = os.path.join(REPO, "docs", "plans", "annotations",
                    "push-wiring-tony.json")
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
