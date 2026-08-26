#!/usr/bin/env python3
"""Project types — one declaration or three? Design conversation input.

    python3 tools/diagram/gen_project_types.py

Draws the collision found on 2026-08-07 while framing
docs/product/requirements-project-type-templates.md: `route`, `Rigor level`
and the proposed `Project Type` are three declarations with overlapping
legal sets, two of them already machine-enforced. Then the second
collision underneath it: the file's nine gates (G0-G8) against Kerd's
seven rungs.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from kit import Flow, INK, RED, GREEN, mark_deltas  # noqa: E402
from to_svg import (to_svg, overflow_report, collision_report,  # noqa: E402
                    text_overlap_report)
import json  # noqa: E402

f = Flow("Project types — one declaration, or three?",
         "input to the design conversation for "
         "docs/product/requirements-project-type-templates.md\n"
         "found 2026-08-07: the new declaration overlaps two that "
         "already refuse.")

# ── 1 — now ──────────────────────────────────────────────────────────────
f.step("1", "NOW", "Three declarations, and 'spike' is in all three",
       "route         = new | problem | spike\n"
       "                front matter, kit.py:28, gate-checked per rung\n"
       "Rigor level   = spike | mvp | production-v1\n"
       "                ## Scope, kit.py:49, AU6-checked\n"
       "Project Type  = Ideation | Spike | MVP | Pilot | Full Release |\n"
       "                Maintenance | Security Review | Experiment |\n"
       "                Hotfix | Migration | Platform | Compliance |\n"
       "                Beta | Decommission | Internal Tooling  (15)\n"
       "\n"
       "a spike would declare spike THREE times, in three places,\n"
       "against three different legal sets.",
       artifact="two of the three already\nREFUSE. route and Rigor\n"
                "level are machine-checked\ntoday across 20 slugs.\n"
                "Project Type is the\nproducer's, and unbuilt.",
       colour=RED)
f.down()

# ── 2 — what each one actually controls ──────────────────────────────────
f.step("2", "READ", "They are not the same thing — but one contains the rest",
       "route          which rungs apply; spike licenses a bypass\n"
       "Rigor level    how much proof the release slice owes\n"
       "Project Type   required / conditional / n-a per category,\n"
       "               PLUS the gates that type must pass,\n"
       "               PLUS the floors it cannot go below\n"
       "\n"
       "Project Type carries strictly more than either. a type of\n"
       "'Spike' already implies route: spike and Rigor level: spike -\n"
       "it cannot mean anything else.",
       artifact="the overlap is not a\nnaming clash. it is one\n"
                "decision currently taken\nin three places, which is\n"
                "three chances to disagree.")
f.down()

# ── 3 — the change ───────────────────────────────────────────────────────
f.step("3", "CHANGE", "One declaration replaces two — a subtraction",
       "declared ONCE, at G0 intake:      Project Type: MVP\n"
       "\n"
       "derived, never declared again:\n"
       "   route         Spike -> spike · Ideation -> spike ·\n"
       "                 Maintenance/Hotfix -> problem · rest -> new\n"
       "   Rigor level   Spike -> spike · MVP/Pilot/Beta -> mvp ·\n"
       "                 Full Release/Migration/Platform/Compliance\n"
       "                 -> production-v1\n"
       "\n"
       "two legal sets die. one arrives. the system gets SMALLER.",
       artifact="reads as an addition on\nfirst look and is the\n"
                "opposite. derived-from-\ndisk applies: a value the\n"
                "machine can compute is\nnever asked for twice.",
       colour=GREEN)
f.down()

# ── 4 — the second collision ─────────────────────────────────────────────
f.step("4", "COLLISION", "Nine gates against seven rungs — they do not align",
       "G0 intake qualified          ~ frame\n"
       "G1 disposition declared        - NO RUNG\n"
       "G2 spec approved             ~ handoff\n"
       "G3 design approved           = design\n"
       "G4 build complete            = loop\n"
       "G5 verification passed       ~ loop  (the loop's own exit)\n"
       "G6 security / privacy          - NO RUNG\n"
       "G7 launch readiness            - NO RUNG\n"
       "G8 post-launch evidence      - NO RUNG (after ready-to-release)\n"
       "                               - viability and scope have NO GATE",
       artifact="G8 is the clean fit. loop\n/ Live was left empty in\n"
                "funnel-steps.md because\nno steps could be found.\n"
                "category POST gave it\nvocabulary; G8 gives it\na gate.",
       colour=RED)
f.down()

# ── 5 — what it costs ────────────────────────────────────────────────────
f.step("5", "COST", "Named before the design, not discovered during it",
       "1. 20 slugs already carry route + Rigor level. a merge is\n"
       "   cross-cutting and owes the standing grep sweep.\n"
       "2. retrofit is FORBIDDEN by standing rule - so how does an\n"
       "   existing slug acquire a type? forward-only leaves 20\n"
       "   items typeless, and the derivation above cannot run\n"
       "   backwards without inventing intent.\n"
       "3. G6 security has no home in Kerd AT ALL. the hard stop\n"
       "   'no production exposure without G6' is currently\n"
       "   inexpressible - not failing, inexpressible.",
       artifact="none of the three is a\nblocker yet. all three\n"
                "are unqualified, which is\nthe dangerous state - a\n"
                "named unsized risk reads\nas managed.",
       colour=RED)

out = os.path.join(REPO, "docs", "plans", "project-types.excalidraw")
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
