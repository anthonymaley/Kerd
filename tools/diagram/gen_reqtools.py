#!/usr/bin/env python3
"""Architecture overviews for the requirements-register build-vs-adopt matrix.

    python3 tools/diagram/gen_reqtools.py

One overview per option, because `tools/design/kit.py` requires every row of a
matrix's `## Options` table to cite an architecture overview that EXISTS on
disk — "the drawn overview is a matrix requirement, not decoration".

Each overview answers the same four questions in the same order, so the six can
be read against each other rather than each on its own terms:

    1  STORE      where a requirement actually lives
    2  INSTALL    what every consuming project must have, measured
    3  GENERATED  what appears that was not written by hand
    4  VERDICT    against the producer's three MUST criteria

Every number here was measured by the 2026-08-07 evaluation workflows — hands-on
installs in throwaway venvs, not read off a README. The sources are recorded in
docs/design/requirements-traceability.md.
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

# The producer's three MUST criteria, stated 2026-08-07 23:41.
MUSTS = "TECH-008 the same files  ·  NFR-004 no scatter  ·  TECH-007 git + Claude Code native"

OPTIONS = [
    {
        "slug": "build",
        "title": "BUILD — the register is a markdown table Kerd already knows how to check",
        "sub": "one file in the consuming project's own repo; AU7/AU8 ride the existing audit",
        "store": ("docs/requirements/register.md   one markdown table, one row per requirement\n"
                  "docs/requirements/categories.md the twenty-category disposition\n"
                  "\n"
                  "plain text. the project's own git repo. no index, no database,\n"
                  "no shadow copy, no sync step. a model reads and WRITES a\n"
                  "requirement with Read/Edit — no tool invocation in the capture path."),
        "store_art": "measured: a 117-line\nchecker + 11 fixtures\npassed first run against\nthe real kit.py.",
        "store_colour": INK,
        "install": ("nothing.\n"
                    "\n"
                    "tools/ is 10,112 lines of stdlib-only Python across 35 files\n"
                    "with no dependency manifest of any kind. AU7/AU8 add no\n"
                    "CI step — they ride gate.py audit, on the AU5/AU6 precedent."),
        "install_art": "the only option that\nimposes nothing on a\nconsuming project.",
        "install_colour": INK,
        "gen": ("the progress board and the journey pages, which already exist.\n"
                "progress_kit.derive() counts len(gates_kit.audit(root)) today, so\n"
                "a new check appears on the board for free.\n"
                "\n"
                "NOT delivered, and this is categorical rather than incremental:\n"
                "no write-back UI · no PDF · no ReqIF · no baselines · no\n"
                "concurrency story beyond merge conflicts."),
        "gen_art": "every page in tools/ is\nread-only by design and\nsays so on its face.",
        "gen_colour": RED,
        "verdict": ("TECH-008  met BY CONSTRUCTION, not by policy — the register IS\n"
                    "          the file, so there is nothing to keep in sync.\n"
                    "NFR-004   one location, two files.\n"
                    "TECH-007  plain markdown in the project's repo."),
        "verdict_art": "the bar the five external\noptions have to beat.",
        "verdict_colour": GREEN,
    },
    {
        "slug": "strictdoc",
        "title": "STRICTDOC — .sdoc files, a real validator, and a web UI that writes back",
        "sub": "Apache-2.0 · v0.27.1 · 40 releases in 12 months · the only option with verified write-back",
        "store": (".sdoc files — plain text, human-readable, byte-for-byte round-trip\n"
                  "verified. its own format, not the project's existing markdown\n"
                  "(markdown support exists and is not the primary path).\n"
                  "\n"
                  "write-back is REAL and was tested, not read: an edit POSTed to the\n"
                  "server changed the file on disk, every other line byte-identical,\n"
                  "git diff two clean lines, with optimistic concurrency control."),
        "store_art": "the one capability no\nother option has, and it\nworks.",
        "store_colour": GREEN,
        "install": ("87 distributions.  373 MB.\n"
                    "\n"
                    "pandas · plotly · numpy · selenium · lxml. strictdoc itself is\n"
                    "18 MB of that. every consuming project owes all of it, because\n"
                    "TECH-001 puts the state in the user's repo, so the tool runs there."),
        "install_art": "against a repo whose\nposture is stdlib Python\nplus POSIX shell, with\nzero runtime deps.",
        "install_colour": RED,
        "gen": ("HTML · JSON · Excel · ReqIF · markdown · rst · doxygen · spdx —\n"
                "all real, all working, zero extra setup.\n"
                "\n"
                "PDF is NOT among them. --formats=html2pdf fails with 'HTML2PDF\n"
                "feature is not enabled': experimental, behind a flag, needs\n"
                "Chrome + chromedriver."),
        "gen_art": "export breadth is the\nbest of the six by a\nwide margin.",
        "gen_colour": INK,
        "verdict": ("NO RELEASES. no milestones, no board, no grouping — confirmed by\n"
                    "three independent checks. StrictDoc's own development plan says\n"
                    "its milestones are 'maintained as GitHub milestones'.\n"
                    "\n"
                    "THE AUTHORS LEAVE THEIR OWN TOOL FOR THE THING WE WANT IT FOR."),
        "verdict_art": "a RELEASE field plus\n--filter-nodes was tried:\nJSON export ignores the\nfilter, and the query\nlanguage has no equality\noperator, so v1.0 also\nmatches v1.0.1.",
        "verdict_colour": RED,
    },
    {
        "slug": "doorstop",
        "title": "DOORSTOP — one file per requirement, and referential integrity that actually refuses",
        "sub": "LGPLv3 · v3.2 · the closest external fit, killed by arithmetic rather than opinion",
        "store": ("one DIRECTORY per document, one FILE per requirement, one\n"
                  ".doorstop.yml per directory. the UID is not inside the file —\n"
                  "it IS the filename.\n"
                  "\n"
                  "item format is YAML, or markdown with YAML frontmatter. a\n"
                  "stdlib-only Python script parsed every field with PyYAML NOT\n"
                  "installed, so there is genuinely no lock-in."),
        "store_art": "the markdown itemformat\nis the idea worth\nstealing: frontmatter +\nbody is exactly 'read by\na person, parsed by a\ntool'.",
        "store_colour": INK,
        "install": ("15 transitive distributions.  28 MB.\n"
                    "\n"
                    "bottle · requests · openpyxl · PyYAML · plantuml-markdown.\n"
                    "requires Python >=3.10,<3.15 — a ceiling a consuming project\n"
                    "does not control."),
        "install_art": "the lightest of the five\nexternal options, and\nstill not nothing.",
        "install_colour": RED,
        "gen": ("published HTML; nothing generated needs committing.\n"
                "\n"
                "but plain `doorstop` MUTATES the source files — alphabetises keys\n"
                "and injects SHA256 fingerprints — so CI must pass -F. and the web\n"
                "server is read-only bar one number-reservation POST."),
        "gen_art": "no release, board,\nmilestone or grouping\nconcept exists — grep\nconfirmed.",
        "gen_colour": RED,
        "verdict": ("NFR-004  FAILS ON ARITHMETIC. 4 documents + 5 requirements already\n"
                    "         cost 13 tracked files. 20 categories + 31 requirements is\n"
                    "         ~65 files across 20 directories, against one register.\n"
                    "TECH-008 half-pass — not a parallel STORE, but a parallel LAYOUT:\n"
                    "         it cannot annotate docs/product/<slug>.md."),
        "verdict_art": "the scatter is intrinsic.\nfile-per-item is HOW it\nearns clean diffs; it\ncannot be configured\naway.\n\nand values are unvalidated\n— state: BANANA passed.",
        "verdict_colour": RED,
    },
    {
        "slug": "sphinxneeds",
        "title": "SPHINX-NEEDS — the best data model of the six, inside a documentation build",
        "sub": "MIT · v8.3.0 · validation that genuinely refuses · and 4.6 MB of vendored JavaScript",
        "store": ("requirements live as DIRECTIVES INSIDE prose documents, in RST\n"
                  "or markdown-via-MyST.\n"
                  "\n"
                  "the decisive test: Kerd's real 14 product docs were copied into a\n"
                  "Sphinx tree and built. Sphinx first refused outright for lack of a\n"
                  "master document; given one, it discovered ZERO needs."),
        "store_art": "adoption means rewriting\nevery existing product\ndoc into directive\nsyntax.",
        "store_colour": RED,
        "install": ("30 distributions / 118 MB — or 35 / 122 MB with MyST for markdown.\n"
                    "\n"
                    "its own diagrams need non-Python binaries: Java + plantuml.jar,\n"
                    "or Graphviz. absent them, needflow bakes 'Error: PlantUML is not\n"
                    "available!' into the PUBLISHED HTML rather than failing the build."),
        "install_art": "a silent-corruption mode\nin the artifact a human\nis meant to read.",
        "install_colour": RED,
        "gen": ("three requirements produced a 5.0 MB, 73-FILE build output.\n"
                "4.6 MB of it is vendored JavaScript the extension ships:\n"
                "DataTables · JSZip · pdfmake · and a Flash .swf.\n"
                "\n"
                "actual content: 48 KB."),
        "gen_art": "to share the HTML you\ncommit that tree, or\nstand up hosting.",
        "gen_colour": RED,
        "verdict": ("what it DOES do, and no other external option does as well:\n"
                    "UX-001 IDs · a five-state enum · custom dependency field ·\n"
                    "req-to-req links with automatic backlinks · needtable filtering.\n"
                    "and its validation REFUSES — malformed ID, bogus status and\n"
                    "dangling dependency all rejected; sphinx-build -W exits 1."),
        "verdict_art": "it would score O on the\ndoctrine criterion where\nKerd's own four hooks\nscore X.\n\nneeds.json is a BUILD\nARTIFACT — a derived\nsecond copy, which is the\nparallel store TECH-008\nforbids.",
        "verdict_colour": RED,
    },
    {
        "slug": "openfasttrace",
        "title": "OPENFASTTRACE — a tracer with a fixed ID grammar the producer's format cannot enter",
        "sub": "GPL-3.0 · v4.9.0 released the same day it was evaluated · and a JVM",
        "store": ("nothing. OFT stores no requirements — it READS markdown you already\n"
                  "have and reports coverage. 'OFT is a requirement tracing tool.'\n"
                  "\n"
                  "it defines a native authoring syntax, so it is a SCHEMA plus a\n"
                  "LINKER over your files — which makes it a COMPETING schema for\n"
                  "the same docs/product/*.md that Kerd already owns."),
        "store_art": "register vs tracer: this\nis a tracer. it never\nanswers where a\nrequirement lives.",
        "store_colour": RED,
        "install": ("Java 17+, verified three ways: the README, the 4.9.0 JAR's\n"
                    "MANIFEST.MF (Java-Version: 17), and the class-file header\n"
                    "(major=61). no JVM exists on this machine.\n"
                    "\n"
                    "ships as a .jar only — no brew, no pip, no npm, no docker,\n"
                    "no native image. grep over the README returned zero hits."),
        "install_art": "the largest install\nburden of the six, and\nthe only one that is not\na Python package.",
        "install_colour": RED,
        "gen": ("plain text · HTML · an aspec XML report carrying id, version,\n"
                "status, sourcefile, sourceline, coverage and dependencies —\n"
                "parseable by stdlib xml.etree, with CI exit codes 0/1/2.\n"
                "\n"
                "no UI · no write-back · no release or board concept."),
        "gen_art": "the XML report is good\nand a stdlib script can\nread it.",
        "gen_colour": INK,
        "verdict": ("ID GRAMMAR IS FIXED: artifacttype~name~revision, and names must\n"
                    "start with a unicode letter. FUN-001 and UX-001 are NOT\n"
                    "EXPRESSIBLE AT ALL. even FUN~001~1 is illegal.\n"
                    "\n"
                    "lifecycle is a closed set of four — draft, proposed, approved,\n"
                    "rejected — with no extension point. Depends exists but is INERT:\n"
                    "the docs say it 'has no effect on the coverage'."),
        "verdict_art": "worth stealing anyway:\nwriting an OFT tag costs\nnothing — # [impl->dsn~x~1]\nis a plain comment. only\nCHECKING needs the JVM,\nso Kerd could adopt the\nconvention and write its\nown stdlib checker.",
        "verdict_colour": RED,
    },
    {
        "slug": "reqflow",
        "title": "REQFLOW — no macOS install path exists, and a requirement is whatever a regex matched",
        "sub": "GPLv2+ · last release 2019-03-11 · three commits in 2025",
        "store": ("nothing, and there is no schema. the entire data model is\n"
                  "struct Requirement { id; seqnum; parentDocument; covers;\n"
                  "coveredBy; text; }.\n"
                  "\n"
                  "a requirement exists only where a PCRE regex matched inside a\n"
                  "scanned document. the ID is an opaque matched string."),
        "store_art": "no category taxonomy.\nno lifecycle states —\nthe only status in the\ntool is 'U' for\nuncovered.",
        "store_colour": RED,
        "install": ("THERE IS NO MACOS INSTALL PATH.\n"
                    "\n"
                    "brew search -> not found. pip3 index -> no distribution. every\n"
                    "release ships Windows .exe only; configure.ac's *darwin* case is\n"
                    "empty. macOS means an autotools compile against libzip, libxml2,\n"
                    "poppler-cpp — and libpcreposix from PCRE1, whose Homebrew formula\n"
                    "Homebrew itself marks deprecated: unmaintained."),
        "install_art": "this would be Kerd's\nfirst native-compiled\ndependency. that is a\ncategory change in what\na consuming project must\nown.",
        "install_colour": RED,
        "gen": ("text · CSV · HTML. the HTML claim is true and verified in source.\n"
                "\n"
                "the only machine-readable export is CSV — the export enum is\n"
                "literally { REQ_X_TXT, REQ_X_CSV }. no JSON, no XML."),
        "gen_art": "enough to diff a coverage\nmatrix in CI. not enough\nto round-trip a register.",
        "gen_colour": RED,
        "verdict": ("markdown is handled only by the unknown-extension fallthrough to\n"
                    "plain text — no notion of headings, frontmatter, tables or lists.\n"
                    "\n"
                    "no UI, no write-back, no board. report-only, one-way. it cannot\n"
                    "be the place a requirement's state changes, which is most of\n"
                    "what a register does."),
        "verdict_art": "a plausible tool for a\nteam already tracing\nrequirements through Word\nand PDF deliverables.\nnot a dependency Kerd can\nask an arbitrary project\nto install.",
        "verdict_colour": RED,
    },
]


def draw(opt):
    f = Flow(opt["title"], opt["sub"] + "\n" + MUSTS)
    f.step("1", "STORE", "Where a requirement actually lives",
           opt["store"], artifact=opt["store_art"], colour=opt["store_colour"])
    f.down()
    f.step("2", "INSTALL", "What every consuming project must have — measured, not read",
           opt["install"], artifact=opt["install_art"],
           colour=opt["install_colour"])
    f.down()
    f.step("3", "GENERATED", "What appears that nobody wrote by hand",
           opt["gen"], artifact=opt["gen_art"], colour=opt["gen_colour"])
    f.down()
    f.step("4", "VERDICT", "Against the producer's three MUST criteria",
           opt["verdict"], artifact=opt["verdict_art"],
           colour=opt["verdict_colour"])

    out = os.path.join(REPO, "docs", "design", f"reqtools-{opt['slug']}.excalidraw")
    mark_deltas(f.els, out)
    json.dump({"type": "excalidraw", "version": 2,
               "source": "https://excalidraw.com", "elements": f.els,
               "appState": {"gridSize": None,
                            "viewBackgroundColor": "#ffffff"},
               "files": {}}, open(out, "w"), indent=1)
    svg = out.replace(".excalidraw", ".svg")
    w, h = to_svg(f.els, svg)
    faults = []
    for label, found in (("overflow", overflow_report(f.els)),
                         ("collision", collision_report(f.els)),
                         ("text overlap", text_overlap_report(f.els))):
        if found:
            faults.append(f"{len(found)} {label}")
    status = " | ".join(faults) if faults else "layout clean"
    print(f"wrote {os.path.relpath(svg, REPO)} ({w:.0f}x{h:.0f}) — {status}")
    return len(faults)


if __name__ == "__main__":
    bad = sum(draw(o) for o in OPTIONS)
    print(f"\n{len(OPTIONS)} overviews written; "
          f"{'all layouts clean' if not bad else f'{bad} layout fault(s)'}")
