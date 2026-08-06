#!/usr/bin/env python3
"""Vault-unhook — the vault becomes opt-in everywhere. Design package.

    python3 tools/diagram/gen_vault_unhook.py

Draws docs/design/vault-unhook.md for the design conversation: the
zero-reader toll, the opt-in-everywhere change, the coverage table
(every vault artifact's fate), the four-file edit map, the renumber
decision, the proof plan, and the named out-of-scope.
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

f = Flow("Vault-unhook — the vault becomes opt-in everywhere · design package",
         "slice 1 of docs/product/vault-unhook.md\n"
         "the boundary stops paying for pages nobody reads; the deliberate path stays whole.")
SP_X, SP_W, L_X, R_X, X = f.SP_X, f.SP_W, f.L_X, f.R_X, f.X

# ── 1 — now ──────────────────────────────────────────────────────────────
f.step("1", "NOW", "The boundary pays a toll nobody collects",
       "every full switch-out writes the vault - Status, Weekly, domain\n"
       "files - real tokens, every boundary, every project. readers:\n"
       "ZERO. no human opens Obsidian (all three users, interviewed\n"
       "2026-08-06); no machine reads it (write-only by design). one\n"
       "user hit session limits MID-switch-out paying this bill.",
       artifact="the insurance is already\ndelivered twice: immutable\n"
                "kivna/sessions/ logs +\ngit history of every\nCONTEXT.md version.",
       colour=RED)
f.down()

# ── 2 — the change ───────────────────────────────────────────────────────
f.step("2", "CHANGE", "Opt-in everywhere, deliberate path untouched",
       "switch-out: vault step DELETED (all modes collapse on the vault\n"
       "axis). tend: a missing vault is a legitimate opt-out, one info\n"
       "line, never a warning. kivna save: THE one way vault pages get\n"
       "written - invoked on purpose at natural breakpoints.\n"
       "nothing in any existing vault is deleted or moved.",
       artifact="the switch-IN path is not\nedited AT ALL - the killer\n"
                "feature (fresh session,\nswitch in, one second ago)\n"
                "is out of bounds by\nconstruction.")
f.down()

# ── 3 — coverage ─────────────────────────────────────────────────────────
f.step("3", "COVERAGE", "Every vault artifact's fate — nothing dies silently",
       "Status.md -> duplicated in repo (CONTEXT + newest log).\n"
       "Weekly.md -> re-curation of repo records; deliberate save.\n"
       "MOC -> static index; deliberate save.\n"
       "domain files (Architecture, Playbook, guides) -> human-curated\n"
       "re-statements; vault-only prose kept via deliberate save.\n"
       "people/ -> VAULT-ONLY, the genuine residue - untouched, writable.\n"
       "client/engagement/research slots -> vault-only where they exist.",
       artifact="the killer risk's\ncountermeasure IS this\ntable. the one truly\n"
                "vault-only class (people/,\ncurated prose) keeps its\nfull write path.")
f.down()

# ── 4 — edit map ─────────────────────────────────────────────────────────
f.step("4", "EDITS", "Four files, one principle",
       "switch SKILL.md (the bulk): step 4 deleted + renumber; modifier\n"
       "table drops the Vault row; description, intro, usage, triage,\n"
       "fallback all drop vault language; banner gains ONE conditional\n"
       "line when vault.json exists ('vault not written - on-demand').\n"
       "kivna SKILL.md: ONE sentence added (save is deliberate; switch\n"
       "no longer calls it). tend SKILL.md: Cat-3 missing-vault nag ->\n"
       "info line; present vault keeps every check. vault-spec: opt-in\n"
       "sentence in Ownership. plus README x3 sections, v0.83.0.",
       artifact="kivna's touch is minimal\nBY DESIGN - the kivna\n"
                "verdict review (Backlog)\nshould meet an unmodified\nsurface.")
f.down()

# ── 5 — decision ─────────────────────────────────────────────────────────
f.step("5", "DECISION", "Delete-and-renumber beats a tombstone step",
       "delete + renumber: O - the skill reads clean to a new user;\n"
       "living docs describe what IS, git archives what was.\n"
       "tombstone 'step 4 (removed)': X - a numbered hole documents\n"
       "history, not behavior.\n"
       "cost, named: one playbook gotcha cites 'step 5' - a dated\n"
       "incident record, left as archaeology.",
       artifact="options not close - marks\nsuffice, no matrix.")
f.down()

# ── 6 — proof ────────────────────────────────────────────────────────────
f.step("6", "PROOF", "Three diff-scoped measurements + the honest limit",
       "writes per boundary 1 -> 0: the deletion itself; grep lands at\n"
       "exactly two deliberate-path pointers.\n"
       "on-demand unchanged: kivna diff = one added sentence, zero\n"
       "removals.\n"
       "killer feature byte-for-byte: ZERO diff hunks inside ## Switch\n"
       "In - any hunk there is a build refusal.\n"
       "plus: full suite (no tool edits), release sweep R1-R3.",
       artifact="honest limit, NAMED: skill\ntext is prompt-layer - no\n"
                "runtime refuser observes a\nsession's tool calls.\n"
                "rigor mvp disposition:\nmeasured = 3 diff checks +\n"
                "sweep; waived-by-name =\nlive-boundary observation\n"
                "(first real switch-out,\nnext session log).")
f.down()

# ── 7 — out of scope ─────────────────────────────────────────────────────
f.step("7", "SCOPE", "Out of scope, named (composer key on the frame)",
       "BOUNDARY AUTO-SIZING (light/low die): Backlog, own slice -\n"
       "the modifier table's shape is left alone bar the vault row.\n"
       "CYCLE AUTOMATION (out -> clear -> in): Backlog High, own frame.\n"
       "KIVNA VERDICT (import/export/scaffold archaeology): Backlog.\n"
       "VAULT DELETION OR MIGRATION: never in this slice.\n"
       "SCHEDULED SAVES: only if the stale-insurance trigger fires.",
       artifact="", colour=GREEN, dashed=True)

# Tony's font call 2026-08-04: the package reads in Nunito (6).
for _e in f.els:
    if _e["type"] == "text":
        _e["fontFamily"] = 6

out = os.path.join(REPO, "docs", "design", "vault-unhook.excalidraw")
_ann = os.path.join(REPO, "docs", "plans", "annotations",
                    "vault-unhook-tony.json")
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
