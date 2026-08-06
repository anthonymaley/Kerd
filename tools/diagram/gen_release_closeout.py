#!/usr/bin/env python3
"""Release-closeout — every release checks its own story. Design package.

    python3 tools/diagram/gen_release_closeout.py

Draws docs/design/release-closeout.md for the design conversation: the
never-prompted toll, the triggered pass, the charter split, the 21-edit
map, the measurements, and the named out-of-scope.
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

f = Flow("Release-closeout — every release checks its own story · design package",
         "slice 1 of docs/product/release-closeout.md\n"
         "slainte re-founded as the triggered pass; tend wired at the two moments it's needed.")

# ── 1 — now ──────────────────────────────────────────────────────────────
f.step("1", "NOW", "The judgment layer waits to be remembered - and never runs",
       "slainte usage: ZERO ('i never use it... im not prompted and\n"
       "forget' - Tony, interviewed). its .slainte target list still\n"
       "audits a CHANGELOG dead since 0.14.0. meanwhile five goal\n"
       "gates produced five layer-4 blocks - every one a stale-\n"
       "narrative gap found AFTER shipping. CI refuses the mechanical\n"
       "layer; nothing sweeps the story.",
       artifact="slainte's dormant release\narea already specs the\n"
                "judgment layer (rule 7) -\nnever triggered once.",
       colour=RED)
f.down()

# ── 2 — the change ───────────────────────────────────────────────────────
f.step("2", "CHANGE", "Triggered, fixing, restrained - never remembered",
       "a conductor task whose commit bumps the version fields IS a\n"
       "release; close-out runs the pass BEFORE the boundary: tend's\n"
       "drift check + slainte's narrative sweep of the repo surfaces\n"
       "(README + What's New, playbook, capability lists, touched\n"
       "living docs). findings become FIXES - work commits under the\n"
       "verification gate, skriv's audit on the prose. orient offers\n"
       "tend on a bare repo. standalone slainte/tend stay invocable.",
       artifact="restraint is reported:\nanything judged deliberate-\n"
                "not-drift is NAMED as left\nuntouched - the killer\n"
                "risk's countermeasure.",
       colour=GREEN)
f.down()

# ── 3 — the mechanism ────────────────────────────────────────────────────
f.step("3", "MECHANISM", "One release definition, two invokes, a charter split",
       "triggers = the version-field diff (CI's R1 set, reused) OR a\n"
       "goal record landing (feature closed as complete) - one release\n"
       "definition, two firing moments. conductor INVOKES /kerd:tend and\n"
       "/kerd:slainte (the invoke pattern's 3rd + 4th uses; zero\n"
       "re-description, same law as v0.84.0). charter split: CI owns\n"
       "mechanical (R1-R3, AU1-6 - slainte's duplicated rules 1/2/5\n"
       "prune to a pointer); the pass owns narrative (rule 7's family:\n"
       "README claims vs SKILL behaviour, What's New honesty,\n"
       "state-contract truth, skill counts, hook template).",
       artifact="the .slainte config DIES -\ntargets derive from the\n"
                "repo; the on-demand area\naudits survive config-less.")
f.down()

# ── 4 — edit map ─────────────────────────────────────────────────────────
f.step("4", "EDIT MAP", "21 edits, six files + a deletion - concept-swept",
       "slainte SKILL.md RE-FOUNDED (6): identity, config section\n"
       "deleted, release-pass charter, pruned rules, derived targets.\n"
       "tend (5): .slainte leaves required-files/scaffold/report,\n"
       "joins the deprecated-patterns list with offered deletion.\n"
       "conductor (2): orient bare-repo wire; close-out release wire\n"
       "as step 6, boundary renumbers 6->7, marker stays last.\n"
       "state-contract (2 rows) - playbook (1) - README (slainte\n"
       "section + What's New v0.85.0 cap-five) - kerd-map one-liner +\n"
       "regen - git rm .slainte - version 0.85.0 (3 fields).",
       artifact="sweep ran by CONCEPT per\nthe newest playbook gotcha:\n"
                "read-only / never-fixes /\n.slainte / audit-targets\n"
                "phrasings, sections read\nwhole.")
f.down()

# ── 5 — proof ────────────────────────────────────────────────────────────
f.step("5", "PROOF", "Six measurement families, each a named command",
       "config dead: git ls-files .slainte empty; zero refs in\n"
       "slainte; tend refs = deprecated rows only (count derived at\n"
       "contract). read-only identity dead: zero hits in slainte +\n"
       "state-contract. wires exist once each; conductor contains NO\n"
       "slainte check descriptions (single-definition law). charter\n"
       "split written: CI-owns pointer >= 1, 'Version sync' as kept\n"
       "rule = 0. skriv wire >= 1. map one-liner new + pair regen'd.",
       artifact="honest limit, NAMED: the\ntrigger is prompt-layer -\n"
                "a skipped pass is today's\nstatus quo; CI graduation\n"
                "sits behind the accepted\nrisk's review trigger.\n"
                "rigor mvp: measured =\ngreps/diffs; waived-by-name\n"
                "= first triggered pass at\nthe next real release.")
f.down()

# ── 6 — out of scope ─────────────────────────────────────────────────────
f.step("6", "SCOPE", "Out of scope, named (composer keys on the frame)",
       "EXTERNAL/DECLARED SURFACES (websites, SDK docs, portals,\n"
       "marketplace beyond this repo): slice 2, own mechanism.\n"
       "CI GRADUATION (What's-New-untouched refusal): review trigger.\n"
       "KIVNA SCAFFOLD VERDICT: Backlog archaeology, untouched.\n"
       "SKRIV SKILL.md: untouched - called, not changed.\n"
       "SWITCH: untouched entirely - the pass runs before the\n"
       "boundary; the boundary contract stays v0.84.0's.",
       artifact="options not close - marks\nsuffice, no matrix.",
       colour=GREEN, dashed=True)

# Tony's font call 2026-08-04: the package reads in Nunito (6).
for _e in f.els:
    if _e["type"] == "text":
        _e["fontFamily"] = 6

out = os.path.join(REPO, "docs", "design", "release-closeout.excalidraw")
_ann = os.path.join(REPO, "docs", "plans", "annotations",
                    "release-closeout-tony.json")
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
