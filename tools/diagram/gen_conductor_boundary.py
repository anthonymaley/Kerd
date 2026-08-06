#!/usr/bin/env python3
"""Conductor-boundary — the close-out runs the boundary. Design package.

    python3 tools/diagram/gen_conductor_boundary.py

Draws docs/design/conductor-boundary.md for the design conversation:
the no-decision handoff ask, the invoke-is-literal mechanism, the
17-edit map across five files, the measurements, and the named
out-of-scope.
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

f = Flow("Conductor-boundary — the close-out runs the boundary · design package",
         "slice 1 of docs/product/conductor-boundary.md\n"
         "one act closes a conducted session; every close names what's next.")

# ── 1 — now ──────────────────────────────────────────────────────────────
f.step("1", "NOW", "The close ends with an ask carrying no decision",
       "conductor close-out finishes its five steps, then STOPS and\n"
       "tells the human: 'run /kerd:switch out'. observed tonight\n"
       "(2026-08-06): the ask carried nothing to decide - the boundary\n"
       "was mechanical, the wait was pure friction. after the boundary\n"
       "the session sits quiet though TODO names the next pick.",
       artifact="three briefs in one evening,\nall the same theme: the\n"
                "session should flow further\nbetween the human keys.",
       colour=RED)
f.down()

# ── 2 — the change ───────────────────────────────────────────────────────
f.step("2", "CHANGE", "Close-out invokes the boundary; every close names what's next",
       "conductor close-out gains step 6: INVOKE /kerd:switch out (the\n"
       "Skill tool - literal, proven: switch-in already chains into\n"
       "conductor the same way, observed twice tonight). the handoff\n"
       "ask dies. at each task's verified commit, one line names the\n"
       "next pick (plan step mid-spec; TODO Now/Backlog top after).\n"
       "the banner ends: 'Free context: type /clear, then switch in'.",
       artifact="suggestion, never a loop:\nstarting the pick stays a\n"
                "human reply. Tony's key:\n'without building a loop\nor hook'.",
       colour=GREEN)
f.down()

# ── 3 — the mechanism ────────────────────────────────────────────────────
f.step("3", "MECHANISM", "Invoke is literal - the killer risk dissolves structurally",
       "the frame's killer risk: two prompt-layer descriptions of the\n"
       "boundary drifting apart (best-evidenced failure class - the\n"
       "v0.83.0 goal block). dissolved, not mitigated: conductor holds\n"
       "ONE instruction to call /kerd:switch out and ZERO descriptions\n"
       "of the flow. banner additions live in SWITCH's template, so\n"
       "both callers get them. switch out cannot tell who called it.",
       artifact="one definition, two callers:\nstandalone /kerd:switch out\n"
                "(Tony's key: usable without\nconductor) + conductor's\nclose-out.")
f.down()

# ── 4 — edit map ─────────────────────────────────────────────────────────
f.step("4", "EDIT MAP", "17 edits, five files + version - swept, not predicted",
       "conductor SKILL.md (5): close-out intro rewrite, new step 6\n"
       "invoke, handoff paragraph DELETED, execute next-pick paragraph,\n"
       "principles bullet -> 'closes the session it conducted'.\n"
       "switch SKILL.md (3): single-definition ownership paragraph,\n"
       "second-caller line, banner + /clear ritual line.\n"
       "state-contract (4 rows): two-caller owner rows; git row was\n"
       "STALE since v0.67 (work commits) - fixed honestly here.\n"
       "README (3): conductor section, layers paragraph, What's New\n"
       "v0.84.0 cap-five. playbook (1): role line. version: 0.84.0.",
       artifact="design-time cross-cutting\ngrep DONE (the standing\n"
                "obligation): 8 truth sites;\nplaybook v0.26.0 entry left\n"
                "as dated history, named.")
f.down()

# ── 5 — proof ────────────────────────────────────────────────────────────
f.step("5", "PROOF", "Six measurements, each a named command",
       "handoff ask 1 -> 0: grep 'tell the user to run' = 0.\n"
       "single definition: no switch step-headings in conductor = 0;\n"
       "invoke line names /kerd:switch out >= 1.\n"
       "banner lines once, in switch: /clear grep = 1 there, 0 in\n"
       "conductor. Switch In byte-identical (vault-unhook proof shape).\n"
       "Switch Out step-heading list unchanged bar banner body.\n"
       "next-pick naming present in execute phase.",
       artifact="honest limit, NAMED: skill\ntext is prompt-layer - the\n"
                "invoke is an instruction,\nnot a refuser. rigor mvp:\n"
                "measured = greps + diffs;\nwaived-by-name = first live\n"
                "conducted boundary, next\nsession log.")
f.down()

# ── 6 — out of scope ─────────────────────────────────────────────────────
f.step("6", "SCOPE", "Out of scope, named (composer keys on the frame)",
       "/CLEAR AUTOMATION: CLI built-in wall confirmed - banner offers,\n"
       "human types.\n"
       "LOOPS / HOOKS / SCHEDULING: suggestion only, permanent\n"
       "countermeasure in the ledger.\n"
       "LIGHT/LOW + AUTO-SIZING: separate Backlog item, untouched.\n"
       "STOP-HOOK FIX: adjacent Backlog High, untouched.\n"
       "SCAFFOLD/TEND FIRST-RUN WIRING: captured to the tend/slainte\n"
       "review brief.",
       artifact="options not close - marks\nsuffice, no matrix.",
       colour=GREEN, dashed=True)

# Tony's font call 2026-08-04: the package reads in Nunito (6).
for _e in f.els:
    if _e["type"] == "text":
        _e["fontFamily"] = 6

out = os.path.join(REPO, "docs", "design", "conductor-boundary.excalidraw")
_ann = os.path.join(REPO, "docs", "plans", "annotations",
                    "conductor-boundary-tony.json")
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
