#!/usr/bin/env python3
"""The register data model, redrawn after the 2026-08-08 schema study.

    python3 tools/diagram/gen_register_model.py

The first proposal was a seven-column markdown table. It was written by an
agent running in PARALLEL with the study of StrictDoc, ReqIF, Doorstop and
Sphinx-Needs, so it never saw a single finding from them. The producer caught
that — "did we actually learn from the study and alter our thinking into a
proposed model?" — and the answer was no.

This is the model with the findings actually folded in. Every claim marked
MEASURED was verified hands-on in a venv, not read from documentation.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from kit import Flow, INK, RED, GREEN, mark_deltas  # noqa: E402
from to_svg import (to_svg, overflow_report, collision_report,  # noqa: E402
                    text_overlap_report)

f = Flow("The register data model — after the schema study",
         "StrictDoc · ReqIF 1.2 · Doorstop 3.2 · Sphinx-Needs 8.3.0, all read "
         "as grammars and run hands-on\n"
         "the seven-column proposal never saw these findings — it was written "
         "in parallel with them")

# ── 1 — what we proposed before the study ────────────────────────────────
f.step("1", "BEFORE", "A markdown table with seven columns",
       "| ID | Category | State | Requirement | Depends | Superseded by | Source |\n"
       "\n"
       "one flat table. fields and links in the same row. the field set\n"
       "hardcoded in the checker. one rendering. a state is a label.\n"
       "\n"
       "every mature model surveyed rejects at least two of those choices.",
       artifact="the producer's own 15-field\nrow could not fit this\nshape either - which was\nthe tension nobody\nresolved.",
       colour=RED)
f.down()

# ── 2 — the model separates five things ──────────────────────────────────
f.step("2", "MODEL", "Five things, declared separately — not one table",
       "CATALOG      the field set, the twenty codes, the legal states,\n"
       "             the legal link types.  DECLARED ONCE, SHARED.\n"
       "             StrictDoc: [GRAMMAR] with IMPORT_FROM_FILE - one\n"
       "             schema file serving many documents.\n"
       "\n"
       "DISPOSITION  which categories this project owes, and its type.\n"
       "             already designed; this is the producer's G1.\n"
       "\n"
       "REGISTER     the requirement records themselves.\n"
       "\n"
       "RELATIONS    typed links. NOT a column. first-class objects.\n"
       "\n"
       "VIEWS        named field subsets, stored as DATA.",
       artifact="MEASURED: StrictDoc's\ndefault REQUIREMENT is\neight fields and NONE is\nmandatory. required-ness\nis a per-project\ndeclaration, not a vendor\nopinion. that is the\nwhole reason the catalog\nis separate from the\nregister.",
       colour=GREEN)
f.down()

# ── 3 — relations are objects ────────────────────────────────────────────
f.step("3", "RELATIONS", "A link is an object with a type — never a column",
       "ReqIF SpecRelation: TYPE, SOURCE and TARGET are ALL MANDATORY.\n"
       "a relation cannot be untyped. it is a first-class object beside\n"
       "the requirement, not an attribute of it.\n"
       "\n"
       "StrictDoc: ROLE must be REGISTERED IN THE GRAMMAR - 'ROLE:\n"
       "Refines' was refused until declared - and REVERSE_ROLE means one\n"
       "declaration gives BOTH reading directions.\n"
       "\n"
       "  depends-on / required-by      supersedes / superseded-by\n"
       "  satisfied-by / satisfies      verified-by / verifies\n"
       "  refines / refined-by\n"
       "\n"
       "the producer's single 'Trace Links:' field is four different\n"
       "relations in one bag. TECH-006 is a LINK TYPE, not a column.",
       artifact="this kills two columns\nfrom the seven: Depends\nand Superseded by both\nbecome links.\n\nand it gives supersession\na typed edge instead of a\nprose convention.",
       colour=GREEN)
f.down()

# ── 4 — views resolve fifteen-fields versus readability ──────────────────
f.step("4", "VIEWS", "One model, many renderings — the 15-vs-7 tension dissolves",
       "StrictDoc stores named VISIBLE_FIELDS sets as data. the model\n"
       "carries every field the producer's row names; a VIEW decides\n"
       "which of them a given surface shows.\n"
       "\n"
       "  card      ID · Category · State · Requirement       (the board)\n"
       "  table     + Depends · Source                        (the file)\n"
       "  full      every declared field                      (one record)\n"
       "  release   ID · Title · State · release              (planning)\n"
       "\n"
       "so the argument was never 15 versus 7. it was ONE MODEL versus\n"
       "ONE RENDERING, and we had conflated them.",
       artifact="UX-006 - 'avoid reading\nlots of text' - is a VIEW\nrequirement, not a schema\nrequirement. it was\nshrinking the model when\nit should have been\nchoosing a view.",
       colour=GREEN)
f.down()

# ── 5 — two holes the study opened ───────────────────────────────────────
f.step("5", "HOLES", "Two things the ratified design gets wrong",
       "FINAL IS UNFALSIFIABLE.  Doorstop's `reviewed` is a SHA256\n"
       "fingerprint of the item, not a label. MEASURED: editing one line\n"
       "of a requirement's text immediately reported 'unreviewed\n"
       "changes'. Kerd's `final` survives any later edit - so an approval\n"
       "cannot be told from one whose subject changed underneath it.\n"
       "  -> the record stores a hash of the statement at approval.\n"
       "     edit the statement and the state degrades, by construction.\n"
       "\n"
       "A STATE OWES NOTHING.  Sphinx-Needs attaches OBLIGATIONS to a\n"
       "state. MEASURED: 'a fun in status final must be verified_by at\n"
       "least one tst' produced a real refusal.\n"
       "  -> the producer's own G0-G8 gates already state the\n"
       "     obligations. In PROSE. this is their machine form.",
       artifact="SUSPECT LINKS follow from\nthe same fingerprint: a\nlink stores the target's\nstamp, so one edit marks\nits dependents for\nre-look. MEASURED: one\nedit flagged three\ndependents in two\ndocuments.\n\nDERIVED licenses an\norigin requirement to\nhave no parent - without\nit every BUS/STA/USR row\nreads as a broken trace.",
       colour=RED)
f.down()

# ── 6 — the surface already exists ───────────────────────────────────────
f.step("6", "SURFACE", "A mature tool already designed the markdown surface",
       "StrictDoc 0.27.1 ships a MARKDOWN backend whose default grammar\n"
       "is field-for-field identical to its .sdoc one:\n"
       "\n"
       "    ## <Title>\n"
       "    **UID**: FUN-001\n"
       "    **STATUS**: final\n"
       "\n"
       "    <the statement, a blank-line-separated block>\n"
       "\n"
       "short meta lines, long text as blocks. no pipes to escape, no\n"
       "column-width tyranny, and a statement can be a paragraph.\n"
       "\n"
       "DO NOT copy one thing: StrictDoc enforces FIELD ORDER. that is\n"
       "the single decision in the format actively hostile to a model\n"
       "editing a file.",
       artifact="the pipe problem is real\nand we hit it: the\nproposed schema declared\n\\| as the escape and the\nmatrix parser does not\nhonour it - an escaped\npipe split a row into\neight columns. a format\nrule nothing implements.\n\na block format has no\npipe problem at all.",
       colour=GREEN)
f.down()

# ── 7 — what this costs ──────────────────────────────────────────────────
f.step("7", "COST", "Named before the design, not discovered during it",
       "1. the register stops being one file. catalog, disposition,\n"
       "   register and relations are four declared things - which is\n"
       "   NFR-004 pressure ('not scatter artifacts') and must be\n"
       "   argued, not assumed. one directory, four files, is the\n"
       "   defensible reading.\n"
       "\n"
       "2. a block format is harder to scan raw than a table. the VIEW\n"
       "   answers it - but only once the board exists, and the board\n"
       "   is unbuilt.\n"
       "\n"
       "3. fingerprinted approval means a state can change without a\n"
       "   human acting. that is the point, and it will surprise\n"
       "   someone the first time it fires.",
       artifact="none of these is a\nblocker. all three are\nunqualified, which is the\ndangerous state - a named\nunsized risk reads as\nmanaged.",
       colour=RED)

out = os.path.join(REPO, "docs", "design", "register-model.excalidraw")
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
