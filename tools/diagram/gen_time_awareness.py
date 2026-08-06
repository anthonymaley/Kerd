#!/usr/bin/env python3
"""Time-awareness — the machine consults a clock. Design package.

    python3 tools/diagram/gen_time_awareness.py

Draws docs/design/time-awareness.md for the design conversation: the
clock-blind failures, the same-turn rule, the four capture mechanisms,
the edit map, the measurements, and the named out-of-scope.
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

f = Flow("Time-awareness — the machine consults a clock · design package",
         "slice 1 of docs/product/time-awareness.md\n"
         "honest actuals first; estimates wait for the journey view.")

# ── 1 — now ──────────────────────────────────────────────────────────────
f.step("1", "NOW", "The model cannot tell time - two wrong-by-hours labels in one day",
       "'late-evening sitting' written at midday; a TODO item dated\n"
       "itself 'midnight' without checking. every honest time so far\n"
       "exists because a hand ran date. git already timestamps every\n"
       "commit - rung LANDINGS are boundable today; missing: start\n"
       "times, in-session moments, the human's clock, and the model\n"
       "consulting one while writing prose.",
       colour=RED)
f.down()

# ── 2 — the aim ──────────────────────────────────────────────────────────
f.step("2", "AIM", "Tony's framing at approval: actuals calibrate estimates",
       "task start + task end = duration; accumulated durations =\n"
       "the base that makes effort estimates for future tasks\n"
       "accurate instead of guessed. slice 1 captures HONEST ACTUALS\n"
       "only - estimates themselves are the parked journey view's\n"
       "slice when it wakes (its named prerequisite: time data needs\n"
       "an on-disk home).",
       colour=GREEN)
f.down()

# ── 3 — the rule ─────────────────────────────────────────────────────────
f.step("3", "RULE", "The same-turn rule - one definition, in the state contract",
       "a wall-clock time is written ONLY in a turn that ran date and\n"
       "read its output; a remembered or inferred time is never\n"
       "written (the killer risk: a plausible false time in an\n"
       "immutable record poisons the calibration base). definition\n"
       "lives ONCE in docs/state-contract.md; switch + conductor carry\n"
       "one-line pointers (single-definition law, v0.84.0 precedent).\n"
       "machine layer checks presence/format only - time HONESTY is\n"
       "the declared limit (retrieval-not-comprehension class).")
f.down()

# ── 4 — the mechanisms ───────────────────────────────────────────────────
f.step("4", "CAPTURE", "Four mechanisms - no new write moments invented",
       "MARKER STAMP: conductor writes 'conductor: <phase> @ date' -\n"
       "the execute stamp IS task start. all 4 .active-modes readers\n"
       "are prefix-greps (swept, proven safe); stop.sh echoes the\n"
       "stamp to the human free.\n"
       "TASK END: the work commit's git timestamp - already exact.\n"
       "SITTING RANGES: headings get real (HH:MM-HH:MM TZ); per-task\n"
       "line at boundary: started (marker) / landed (git).\n"
       "CLOCK LINE: new gate records carry **Clock:** under the title\n"
       "- documented in tools/gates/README.md, NOT validated (the\n"
       "accepted risk holds the CI graduation), goal records first.")
f.down()

# ── 5 — the statusline ───────────────────────────────────────────────────
f.step("5", "HUMAN", "hooks/statusline.sh - composes, never claims the slot",
       "prints HH:MM; with an argument naming an existing statusline\n"
       "command, prints 'HH:MM . <its output>' forwarding stdin (the\n"
       "context JSON). the slot may be occupied - THIS machine runs\n"
       "scorched-earth's burn-rate wrapper, the live example. wiring\n"
       "machine-local + opt-in, absolute paths (hook-path gotcha):\n"
       "free slot -> point statusLine at the script; occupied ->\n"
       "pass the current command as the argument. the model never\n"
       "sees the statusline - the frame's accepted limit.")
f.down()

# ── 6 — edit map ─────────────────────────────────────────────────────────
f.step("6", "EDITS", "Six files - sweep run at design time",
       "1 hooks/statusline.sh NEW (chainable segment)\n"
       "2 skills/conductor/SKILL.md - stamped marker format +\n"
       "  close-out per-task range line + same-turn pointer\n"
       "3 skills/switch/SKILL.md - sitting heading range, per-task\n"
       "  lines, banner close time + same-turn pointer\n"
       "4 docs/state-contract.md - the rule's single definition\n"
       "5 tools/gates/README.md - Clock row (optional, unvalidated)\n"
       "6 README.md - statusline wiring beside the hooks\n"
       "UNTOUCHED, NAMED: docs/gates/* (no retrofits) . AU rules .\n"
       "spec templates (per-step stamps excluded) .\n"
       "hooks.template.json (statusline is not a hook event).")
f.down()

# ── 7 — measurements ─────────────────────────────────────────────────────
f.step("7", "MEASURE", "Stage-1 measurements - each with a named answer",
       "standalone: echo '{}' | statusline.sh matches ^HH:MM$ .\n"
       "chained: stub cmd -> 'HH:MM . STUB' . marker: grep\n"
       "'^conductor: execute @ ' = 1 AND all four hook scripts exit 0\n"
       "against a stamped file . single definition: 'same-turn'\n"
       "defined once (state-contract), pointed >=1 in each skill .\n"
       "Clock row grep = 1 AND git diff docs/gates/ empty . board\n"
       "byte-compare: gate.py route identical for all existing slugs.",
       colour=GREEN)

out = os.path.join(REPO, "docs", "design", "time-awareness.excalidraw")
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
