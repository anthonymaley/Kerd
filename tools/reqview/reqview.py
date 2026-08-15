#!/usr/bin/env python3
"""reqview — SPIKE. Generate a self-contained HTML view over a requirements register.

Standard library only. No third-party imports, ever. No network access.

    python3 tools/reqview/reqview.py

Reads   docs/requirements/register-v2.md
Writes  output/requirements.html   (one file, everything inlined)

The view is disposable. The markdown file is the only writable surface: the page
never writes to disk, it emits a paste-back block the producer copies out.

State is COMPUTED from the fingerprint recipe in docs/design/requirement-shape.md
rule 9. There is no status field in the register and this tool never invents one.

STRICT. Rule 14: ambiguity is refused, never guessed. Everything this parser
meets is classified by an exact shape — a field label, a note blockquote, a
separator, a machine comment — and anything it cannot classify stops the run
with the block and the text named. It never picks the likely reading and it
never writes a page from a guess. That rule is not decoration: this file's
first version guessed, and its guesses were plausible — a wrapped bold note
absorbed into a `Depends on` fabricated four dependencies and a dangling
reference, and a comma inside prose in a `Traces to` produced the trace target
"and the migration will not." A plausible wrong answer is worse than an error,
because an error is seen.
"""

import hashlib
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "docs" / "requirements" / "register-v2.md"
GOALS = ROOT / "docs" / "kerd-goals.md"
OUTPUT = ROOT / "output" / "requirements.html"

LIVE_LABELS = ["statement", "why", "traces to", "depends on", "approval"]
DEAD_LABELS = [
    "killed",
    "statement as proposed",
    "why it was proposed",
    "why it is dead",
    "what was learned",
    "superseded by",
]
FP_FIELDS = ["statement", "why", "traces to", "depends on"]

REF_RE = re.compile(r"\bR-\d{4}\b")
# Rule 1, as a shape rather than a habit. A field label is bold text opening a
# paragraph AND CLOSING ON ITS OWN FIRST LINE — a label never wraps. A note is a
# blockquote: every line begins with ">", so no wrap can make a note line look
# like a field line. Between them there is no reading left to guess at.
FIELD_LABEL_RE = re.compile(r"^\*\*([^*\n]+)\*\*")
NOTE_LEAD_RE = re.compile(r"^>\s\*\*Note\s+—\s+")
HEAD3_RE = re.compile(r"^###\s+(.*)$")
HEAD2_RE = re.compile(r"^##\s+(.*)$")
# A goal or law reference. Never rendered bare in this view: the producer's rule
# is name the behaviour, never the identifier — "you say AU7 but how do i know
# what that is?". The reference stays so he can say it out loud; the name travels
# with it, and both jump to the goal or law itself at the foot of the page.
GOALLAW_RE = re.compile(r"\bLaw\s+([1-9])\b|\bG([1-8])\b")
GOALHEAD_RE = re.compile(r"^#{2,3}\s+(G[1-8]|Law\s+[1-9])\s+—\s+(.*?)\s*$")
MACHINE_RE = re.compile(r"^<!--\s*machine:\s*([0-9a-fA-F-]+)\s*-->\s*$")
APPROVED_RE = re.compile(r"^(.+?),\s*(\S+)\s*·\s*fp:([0-9a-f]{12})\s*$")
NONE_RE = re.compile(r"^none(\s+—\s+.+)?$", re.S)          # rule 9's only prose
TARGET_RE = re.compile(r"^(G[1-8]|Law\s[1-9]|R-\d{4})$")   # rule 7's targets
SEP = ", "                                                 # rule 7, exactly
# Whole-field sentinels — matched against the ENTIRE field before a comma is
# ever looked at, which is how `no parent, by design` survives having one in it.
TRACE_SENTINELS = {"no parent, by design", "not yet traced"}


def refuse(refusals, where, what, why):
    """Rule 14. Record what could not be classified; the run stops on any of these."""
    refusals.append({"where": where, "what": what, "why": why})


# What the strict parser actually checks. Every one of these refuses the render
# when it fails, so a page that exists has passed all of them — which is why the
# page lists them as checks rather than as findings to be forgiven.
CHECKS = [
    "**The document frame** (rule 13) — a preamble, then `## Requirements`, then "
    "`## Graveyard` last, and nothing at heading level two between them.",
    "**Every heading** (rules 1, 10) — `### R-nnnn — handle`, with `— DEAD` in the "
    "graveyard and nowhere else.",
    "**Every paragraph inside every block** (rule 1) — a field, a `> **Note — …**` "
    "blockquote, the machine comment, or the `---` separator. A bold lead that does "
    "not close on its own line is refused rather than absorbed into the field above.",
    "**The five fields** (rule 1) — all present, each once, in order, with notes "
    "after them; six on a graveyard entry.",
    "**`Traces to`** (rule 7) — references separated by a comma and a single space, "
    "or a whole-field sentinel matched before any comma is looked at. No prose.",
    "**`Depends on`** (rule 8) — `R-nnnn` references or `none`, every one resolving "
    "into the live set.",
    "**The approval line** (rule 9) — `none`, `none — <reason>`, or "
    "`<name>, <date> · fp:<12 hex>`, and the state computed from the recipe, never "
    "read from a field.",
    "**References** (rules 2, 13) — none reused, both sections in ascending order.",
    "**Every kill** (rule 10) — a named authoriser on every graveyard entry.",
    "**The fingerprint recipe itself** (rule 9) — both published test vectors "
    "reproduced before anything is read.",
]


# --------------------------------------------------------------------------
# fingerprint — rule 9, verified against both published test vectors
# --------------------------------------------------------------------------

def fingerprint(statement, why, traces, depends, derived):
    """Rule 9. Labels are already stripped by the parser (whole, modifier included).
    A derived statement is prefixed `derived: ` so flipping the flag un-approves."""
    stmt = ("derived: " + statement) if derived else statement
    parts = [stmt, why, traces, depends]
    joined = "\n".join(" ".join(p.split()) for p in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]


def selftest():
    """The two vectors published in docs/design/requirement-shape.md rule 9.
    The second discriminates a label-stripping / derived-prefix bug."""
    v1 = fingerprint(
        "Kerd shall write the agreed spec for a work item to a file inside the "
        "repository that holds the work item.",
        'Law 1 makes the repository the boundary of a project, and Tony ruled on it '
        'directly: *"the way i work, every project has its own repo, its non '
        'negotiable."* A spec held anywhere else puts the agreement outside the '
        'boundary he treats as absolute, and separates it from the repository '
        'history that approval and change detection rely on.',
        "Law 1", "none", False)
    v2 = fingerprint(
        "Kerd shall state, at each request for a producer decision, how many "
        "producer decisions the remainder of the work item's journey requires, and "
        "shall present that count with the request.",
        'Tony added this input to the goals himself: *"a user never feels overwhelmed '
        'by the process"* — and ruled inputs of this kind unmeasurable: *"these are '
        'not measurement, these are inouts to design to avoid what those g1-g8 from '
        'happening, they cant be measured."* His words are the authority; the '
        'statement is our derivation of one countermeasure from them — the weight of '
        'what remains is shown before it is spent, so accumulation is seen coming '
        'rather than discovered. Approving this block approves that derivation.',
        "G1, G5", "none", True)
    return [("vector 1 (plain)", v1, "cf543030e4e7", v1 == "cf543030e4e7"),
            ("vector 2 (derived)", v2, "e45b7b2d80a2", v2 == "e45b7b2d80a2")]


_FIXTURE_FIELDS = (
    "\n**Statement.** The thing shall do the thing\n"
    "\n**Why.** Not yet written.\n"
    "\n**Traces to.** G1\n"
    "\n**Depends on.** none\n"
    "\n**Approval.** none\n\n---\n")


def _fixture_doc(live="", grave=""):
    return ("# Requirements — fixture\n\npreamble\n\n"
            "## Requirements\n" + live + "\n## Graveyard\n" + grave)


def parser_selftest():
    """Heading-parse fixtures. Both hazards below were reported open at the
    2026-08-14 boundary; one was real and silent, one was already closed. They
    are pinned here so neither can return unnoticed."""
    out = []

    def head_case(name, live, grave, want):
        r = []
        _, blocks, _ = parse(_fixture_doc(live, grave), r)
        got = [(b.ref, b.handle, b.dead) for b in blocks]
        out.append((name, repr(got), repr(want), got == want))

    # HAZARD 1 — an em dash inside a handle. Splitting on every em dash
    # truncated the handle and refused nothing.
    head_case("em dash in a live handle",
              "\n### R-0001 — a handle — with an em dash\n" + _FIXTURE_FIELDS, "",
              [("R-0001", "a handle — with an em dash", False)])
    head_case("em dash in a dead handle",
              "", "\n### R-0002 — DEAD — a handle — with an em dash\n" + _FIXTURE_FIELDS,
              [("R-0002", "a handle — with an em dash", True)])
    # `DEAD` is an exact segment, never a prefix: a live handle may open with it.
    head_case("live handle opening with the word DEAD",
              "\n### R-0003 — DEAD links are refused\n" + _FIXTURE_FIELDS, "",
              [("R-0003", "DEAD links are refused", False)])

    # HAZARD 2 — findings.md concatenated back on to the register. Its numbered
    # `### 1 — ...` headings mimic block headings. Verified: they are refused,
    # never filed as requirements.
    r = []
    _, blocks, _ = parse(
        _fixture_doc("\n### R-0001 — live one\n" + _FIXTURE_FIELDS)
        + "\n### 1 — Forty-six requirements have no honest Why\n\nprose\n"
          "\n### 3 — No statement wording was changed\n\nprose\n", r)
    filed = [b.ref for b in blocks]
    out.append(("numbered findings headings refused",
                "filed=%r refusals=%d" % (filed, len(r)),
                "filed=['R-0001'] refusals=2",
                filed == ["R-0001"] and len(r) == 2))
    return out


# --------------------------------------------------------------------------
# parser
# --------------------------------------------------------------------------

class Block:
    def __init__(self, ref, handle, dead, section):
        self.ref = ref
        self.handle = handle
        self.dead = dead
        self.section = section
        self.machine = None
        self.fields = {}          # normalised label -> text
        self.derived = False      # Statement (derived)
        self.notes = []           # (label, text) — bold paragraphs that are not fields
        self.raw = ""


def paragraphs(chunk):
    """Blank-line separated paragraphs, each with the line number it started on.
    The paragraph is the unit of classification: a field, a note, a separator, a
    machine comment. There is no fifth thing, and rule 14 says so out loud."""
    out, cur, at = [], [], 0
    for i, line in enumerate(chunk):
        if line.strip() == "":
            if cur:
                out.append((at, cur))
                cur = []
        else:
            if not cur:
                at = i
            cur.append(line)
    if cur:
        out.append((at, cur))
    return out


def parse(text, refusals):
    """Rule 13's frame, rule 1's block, rules 7-9's field values. Strict."""
    lines = text.split("\n")
    sections = []             # (name, start, end)
    cur_name, cur_start = "(preamble)", 0
    for i, line in enumerate(lines):
        m = HEAD2_RE.match(line)
        if m:
            sections.append((cur_name, cur_start, i))
            cur_name, cur_start = m.group(1).strip(), i + 1
    sections.append((cur_name, cur_start, len(lines)))

    blocks = []
    preamble = ""
    section_names = [s[0] for s in sections]

    # ---- rule 13: the frame. Exactly three sections, graveyard last. ----
    expected = ["(preamble)", "Requirements", "Graveyard"]
    if section_names != expected:
        refuse(refusals, "the document frame",
               " → ".join("`## %s`" % s for s in section_names),
               "Rule 13: the register is a title and preamble, then `## Requirements`, "
               "then `## Graveyard` last, and nothing else sits at heading level two. "
               "A section between the two is refused rather than parsed as prose — its "
               "sub-headings are close enough to `### R-nnnn — handle` that a heading-"
               "driven reader files them as requirements. Analysis about the set lives "
               "in its own file beside the register.")
        return preamble, blocks, section_names

    for name, start, end in sections:
        body = lines[start:end]
        if name == "(preamble)":
            preamble = "\n".join(body).strip()
            continue
        is_grave = name == "Graveyard"

        idxs = [i for i, l in enumerate(body) if HEAD3_RE.match(l)]
        for n, i in enumerate(idxs):
            j = idxs[n + 1] if n + 1 < len(idxs) else len(body)
            chunk = body[i:j]
            head = HEAD3_RE.match(chunk[0]).group(1).strip()
            where = "`## %s` heading `%s`" % (name, head[:60])
            # The separator is POSITIONAL, never "every em dash in the line".
            # A handle may contain em dashes; splitting on all of them silently
            # truncated it and refused nothing — a plausible wrong answer, the
            # exact class rule 14 exists to stop. One split takes the reference,
            # a second takes `DEAD` only when that is the whole segment, and
            # everything after belongs to the handle intact.
            parts = [p.strip() for p in head.split("—", 1)]
            ref = parts[0] if parts else head
            rest = parts[1] if len(parts) > 1 else ""
            dead = False
            if rest.upper().startswith("DEAD"):
                tail = [p.strip() for p in rest.split("—", 1)]
                if tail[0].upper() == "DEAD":       # exact segment, not a prefix:
                    dead = True                     # a handle may start "DEAD ..."
                    rest = tail[1] if len(tail) > 1 else ""
            handle = rest
            if not REF_RE.fullmatch(ref) or not handle:
                refuse(refusals, where, head,
                       "Rule 1: a block heading is `### R-nnnn — handle`, or "
                       "`### R-nnnn — DEAD — handle` in the graveyard. This is neither, "
                       "and what it names cannot be decided by guessing.")
                continue
            if is_grave != dead:
                refuse(refusals, ref, head,
                       "Rule 10: a graveyard entry carries `— DEAD` and a live block "
                       "does not. This one contradicts the section it sits in.")
                continue

            b = Block(ref, handle, dead, name)
            b.raw = "\n".join(chunk).strip()
            known = DEAD_LABELS if b.dead else LIVE_LABELS
            order, seen_note = [], False

            for at, para in paragraphs(chunk[1:]):
                first, whole = para[0], "\n".join(para)
                stripped = whole.strip()

                if stripped == "---":
                    continue                                    # block separator
                if MACHINE_RE.match(first.strip()) and len(para) == 1:
                    b.machine = MACHINE_RE.match(first.strip()).group(1)
                    continue                                    # rule 4

                if first.startswith(">"):                        # rule 1: a note
                    if not all(l.startswith(">") for l in para):
                        refuse(refusals, ref, first[:70],
                               "Rule 1: every line of a note carries `>`. A note that "
                               "drops it mid-paragraph re-opens the exact crack this "
                               "marker closes.")
                        continue
                    if not NOTE_LEAD_RE.match(first):
                        refuse(refusals, ref, first[:70],
                               "Rule 1: a note opens `> **Note — …**`. A blockquote "
                               "without the marker is not classifiable as a note.")
                        continue
                    raw = "\n".join(re.sub(r"^>\s?", "", l) for l in para).strip()
                    mt = re.match(r"^\*\*Note\s+—\s+(.+?)\*\*", raw, re.S)
                    if not mt:
                        refuse(refusals, ref, first[:70],
                               "Rule 1: a note's `> **Note — …**` marker never closes. "
                               "Where the title ends and the note begins is not "
                               "something a parser may decide.")
                        continue
                    label = " ".join(mt.group(1).split()).rstrip(".:").strip()
                    b.notes.append((label, raw[mt.end():].strip()))
                    seen_note = True
                    continue

                if not first.startswith("**"):
                    refuse(refusals, ref, first[:70],
                           "Rule 1: a paragraph inside a block is a field (bold label), "
                           "a note (`> **Note — …**`), the machine comment, or the `---` "
                           "separator. This is none of the four.")
                    continue

                m = FIELD_LABEL_RE.match(first)
                if not m:
                    refuse(refusals, ref, first[:70],
                           "Rule 1: a field label is bold text that opens the paragraph "
                           "and closes on its own first line — a label never wraps. This "
                           "bold lead does not close on its line, which is precisely how "
                           "a note was once read as a field and absorbed into the field "
                           "above it. If it is a note, mark it `> **Note — …**`.")
                    continue
                label = " ".join(m.group(1).split()).rstrip(".").strip()
                norm = label.lower()
                derived = False
                if norm.startswith("statement") and "(derived)" in norm:
                    norm, derived = "statement", True
                if norm not in known:
                    refuse(refusals, ref, label[:70],
                           "Rule 1: the bold-label form is reserved to the %s labels a "
                           "%s block carries. A note in that form is indistinguishable "
                           "from a field — write it `> **Note — …**`."
                           % (len(known), "graveyard" if b.dead else "live"))
                    continue
                if norm in b.fields:
                    refuse(refusals, ref, label[:70],
                           "Rule 1: this block carries two `%s` fields. Which one binds "
                           "is not a question a parser may answer." % label)
                    continue
                if seen_note:
                    refuse(refusals, ref, label[:70],
                           "Rule 1: notes come last. A field after a note leaves the "
                           "field region non-contiguous.")
                val = "\n".join(para[0:])
                val = FIELD_LABEL_RE.sub("", val, count=1).strip()
                b.fields[norm] = val
                order.append(norm)
                if derived:
                    b.derived = True

            missing = [l for l in known if l not in b.fields]
            if missing:
                refuse(refusals, ref, ", ".join("`%s`" % x for x in missing),
                       "Rule 1: all %s fields are required on every %s block — a field "
                       "that does not apply is written `none`, never omitted."
                       % (len(known), "graveyard" if b.dead else "live"))
            elif order != known:
                refuse(refusals, ref, " → ".join(order),
                       "Rule 1: the fields appear in a fixed order (%s)."
                       % ", ".join(known))
            blocks.append(b)

    return preamble, blocks, section_names


def check_values(b, refusals):
    """Rules 7, 8 and 9 — the structured fields. References and sentinels only."""
    if b.dead:
        return [], []

    traces_raw = " ".join(b.fields.get("traces to", "").split())
    depends_raw = " ".join(b.fields.get("depends on", "").split())
    approval = b.fields.get("approval", "").strip()

    traces = []
    if traces_raw not in TRACE_SENTINELS:
        for t in traces_raw.split(","):
            t = t.strip()
            if TARGET_RE.match(t):
                traces.append(t)
            else:
                refuse(refusals, b.ref, "`Traces to` → %r" % t[:60],
                       "Rule 7: `Traces to` carries references separated by `%s` — "
                       "`Gn`, `Law n`, `R-nnnn` — or a whole-field sentinel (%s). "
                       "Prose here splits on its own commas and yields targets that "
                       "look real; the explanation belongs in the Why."
                       % (SEP, ", ".join("`%s`" % s for s in sorted(TRACE_SENTINELS))))
                traces = []
                break
        if traces and traces_raw != SEP.join(traces):
            refuse(refusals, b.ref, "`Traces to` → %r" % traces_raw[:60],
                   "Rule 7: the separator is a comma and a single space, exactly.")

    deps = []
    if depends_raw != "none":
        for d in depends_raw.split(","):
            d = d.strip()
            if REF_RE.fullmatch(d):
                deps.append(d)
            else:
                refuse(refusals, b.ref, "`Depends on` → %r" % d[:60],
                       "Rule 8: `Depends on` carries `R-nnnn` references separated by "
                       "`%s`, or the sentinel `none`. Never prose." % SEP)
                deps = []
                break
        if deps and depends_raw != SEP.join(deps):
            refuse(refusals, b.ref, "`Depends on` → %r" % depends_raw[:60],
                   "Rule 8: the separator is a comma and a single space, exactly.")

    if not (APPROVED_RE.match(" ".join(approval.split())) or NONE_RE.match(approval)):
        refuse(refusals, b.ref, "`Approval` → %r" % approval[:60],
               "Rule 9: the approval line is `none`, `none — <reason>`, or "
               "`<name>, <date> · fp:<12 hex>` and nothing else.")

    return traces, deps


def parse_goals(text):
    """Pull the eight goals and four laws out of docs/kerd-goals.md.

    Names are taken verbatim from the headings — never paraphrased and never
    shortened. The body is the goal's own opening prose, stopping at the
    `Grounded in:` roll-up, so a reference has something real to land on
    without dragging the whole goals file into the view.
    """
    lines = text.split("\n")
    heads = []
    for i, line in enumerate(lines):
        m = GOALHEAD_RE.match(line)
        if m:
            heads.append((i, " ".join(m.group(1).split()), m.group(2).strip()))
    out = {}
    for n, (i, ref, name) in enumerate(heads):
        j = len(lines)
        for k in range(i + 1, len(lines)):
            if lines[k].startswith("## ") or lines[k].startswith("### "):
                j = k
                break
        body = "\n".join(lines[i + 1:j]).strip()
        paras, kept = [p.strip() for p in body.split("\n\n") if p.strip()], []
        for p in paras:
            if p.startswith("**Grounded in") or p.startswith("---"):
                break
            kept.append(p)
            if len(kept) == 2:
                break
        out[ref] = {"ref": ref, "name": name, "body": "\n\n".join(kept),
                    "anchor": ref.replace(" ", "-"),
                    "kind": "law" if ref.startswith("Law") else "goal"}
    return out


# --------------------------------------------------------------------------
# cross-references — every mention of anything is a jump
# --------------------------------------------------------------------------

# Populated once per render. Keyed by reference; a live requirement, a dead one,
# and a goal or law each get a different-looking link, because a reader following
# a reference must know what kind of thing they are about to land on.
LINKS = {"live": {}, "dead": {}, "goals": {}}


def linkify(t):
    """Turn every reference in already-escaped HTML into a jump.

    Applied last, over rendered HTML rather than raw text, so it also catches
    references inside code spans and bold notes. Nothing this touches produces
    an attribute containing a reference, so it cannot corrupt earlier markup.
    """
    def ref_sub(m):
        r = m.group(0)
        if r in LINKS["live"]:
            return ('<a class="xref" href="#%s" data-goto="%s" title="%s">%s</a>'
                    % (r, r, html.escape("%s — %s" % (r, LINKS["live"][r]), quote=True), r))
        if r in LINKS["dead"]:
            return ('<a class="xref dead" href="#%s" data-goto="%s" title="%s">'
                    '%s<span class="skull">&#8224;</span></a>'
                    % (r, r, html.escape("DEAD — %s — %s" % (r, LINKS["dead"][r]), quote=True), r))
        return ('<span class="xref missing" title="Not in this register — '
                'neither live nor in the graveyard">%s</span>' % r)

    def goal_sub(m):
        ref = " ".join(m.group(0).split())
        g = LINKS["goals"].get(ref)
        if not g:
            return m.group(0)
        return ('<a class="xgoal %s" href="#%s" data-goto="%s" title="%s">%s</a>'
                % (g["kind"], g["anchor"], g["anchor"],
                   html.escape("%s — %s" % (ref, g["name"]), quote=True), m.group(0)))

    return GOALLAW_RE.sub(goal_sub, REF_RE.sub(ref_sub, t))


def goal_tag(t):
    """A `Traces to` target, rendered with its name beside it. This is the field
    the producer reads 39 times, so the name is inline here rather than on hover:
    `G4` alone asks him to hold eight numbers in his head."""
    ref = " ".join(t.split())
    g = LINKS["goals"].get(ref)
    if not g:
        return '<span class="tag warn">%s</span>' % html.escape(t)
    return ('<a class="tag %s" href="#%s" data-goto="%s" title="%s">'
            '<b>%s</b> <span class="gname">%s</span></a>'
            % (g["kind"], g["anchor"], g["anchor"],
               html.escape("%s — %s" % (ref, g["name"]), quote=True),
               html.escape(ref), html.escape(g["name"])))


# --------------------------------------------------------------------------
# model
# --------------------------------------------------------------------------

def build(blocks, refusals):
    live = [b for b in blocks if not b.dead]
    dead = [b for b in blocks if b.dead]
    live_refs = {b.ref for b in live}
    all_refs = {b.ref for b in blocks}

    seen = set()
    for b in blocks:
        if b.ref in seen:
            refuse(refusals, b.ref, b.ref,
                   "Rule 2: a reference is never reused. Two blocks carry this one, and "
                   "which of them a dependency names cannot be decided by guessing.")
        seen.add(b.ref)

    order = [b.ref for b in live]
    if order != sorted(order):
        refuse(refusals, "`## Requirements`", " ".join(order[:8]) + " …",
               "Rule 13: blocks appear in ascending reference order.")
    gorder = [b.ref for b in dead]
    if gorder != sorted(gorder):
        refuse(refusals, "`## Graveyard`", " ".join(gorder[:8]) + " …",
               "Rule 13: blocks appear in ascending reference order in both sections.")

    recs = []
    for b in live:
        traces_list, deps = check_values(b, refusals)
        stmt = b.fields.get("statement", "")
        why = b.fields.get("why", "")
        traces = b.fields.get("traces to", "")
        depends = b.fields.get("depends on", "")
        approval = b.fields.get("approval", "")
        fp_now = fingerprint(stmt, why, traces, depends, b.derived)

        dangling = [r for r in deps if r not in live_refs]
        for r in dangling:
            refuse(refusals, b.ref, "`Depends on` → %s" % r,
                   "Rule 8: an unresolved reference is an error that stops the run. %s "
                   "is not in the live set%s."
                   % (r, " — it is in the graveyard" if r in all_refs else ""))

        untraced = " ".join(traces.split()) == "not yet traced"

        a = approval.strip()
        m = APPROVED_RE.match(a.split("\n")[0].strip())
        if m:
            state = "approved" if m.group(3) == fp_now else "invalidated"
            recorded_fp, approver, approved_on = m.group(3), m.group(1), m.group(2)
        else:
            state = "never"
            recorded_fp = approver = approved_on = None

        open_markers = re.findall(r"\[OPEN-[^\]]+\]", stmt)

        recs.append({
            "ref": b.ref, "handle": b.handle, "machine": b.machine,
            "statement": stmt, "why": why, "traces": traces, "depends": depends,
            "approval": approval, "derived": b.derived,
            "traces_list": traces_list, "untraced": untraced,
            "deps": deps, "dangling": dangling,
            "fp": fp_now, "state": state, "recorded_fp": recorded_fp,
            "approver": approver, "approved_on": approved_on,
            "open_markers": open_markers,
            "notes": [{"label": l, "text": t} for l, t in b.notes],
        })

    by_ref = {r["ref"]: r for r in recs}
    for r in recs:
        r["dependents"] = sorted(
            o["ref"] for o in recs if r["ref"] in o["deps"])

    graves = []
    for b in dead:
        killed = b.fields.get("killed", "")
        if "authorised by" not in killed.lower() and "authorized by" not in killed.lower():
            refuse(refusals, b.ref, "`Killed` → %r" % " ".join(killed.split())[:60],
                   "Rule 10: a kill lands with a named authoriser or the entry is "
                   "refused. A model may propose a kill; it may not record one.")
        graves.append({
            "ref": b.ref, "handle": b.handle, "machine": b.machine,
            "killed": killed,
            "statement": b.fields.get("statement as proposed", ""),
            "why_proposed": b.fields.get("why it was proposed", ""),
            "why_dead": b.fields.get("why it is dead", ""),
            "learned": b.fields.get("what was learned", ""),
            "superseded": b.fields.get("superseded by", ""),
            "notes": [{"label": l, "text": t} for l, t in b.notes],
        })

    return recs, graves, by_ref


# --------------------------------------------------------------------------
# render helpers
# --------------------------------------------------------------------------

def inline(text):
    """Minimal inline markdown -> HTML. Escapes first; nothing is executed.
    Rule 6's reserved form (attributed italic double-quotation) is marked so the
    producer's verbatim words are visually distinct from ours."""
    t = html.escape(text)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[(OPEN-[^\]]+)\]", r'<span class="open">[\1]</span>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t, flags=re.S)
    t = re.sub(r"\*(&quot;.+?&quot;)\*", r'<em class="his">\1</em>', t, flags=re.S)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t, flags=re.S)
    t = linkify(t)
    paras = [p.strip() for p in t.split("\n\n") if p.strip()]
    return "".join("<p>%s</p>" % p.replace("\n", " ") for p in paras)


def flat(text, limit=520):
    """Inline markdown with no cross-references — for the hover preview, which is
    a look, not a place to click from. Trimmed so a preview never becomes a wall."""
    t = html.escape(text)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t, flags=re.S)
    t = re.sub(r"\*(&quot;.+?&quot;)\*", r'<em class="his">\1</em>', t, flags=re.S)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t, flags=re.S)
    paras, out, used = [p.strip() for p in t.split("\n\n") if p.strip()], [], 0
    for p in paras:
        p = p.replace("\n", " ")
        if used and used + len(p) > limit:
            out.append("<p class=\"muted\">…</p>")
            break
        out.append("<p>%s</p>" % p)
        used += len(p)
    return "".join(out)


def chip(ref, cls="", named=True):
    """A dependency chip. Two rules ride on it. A chip pointing into the graveyard
    is drawn dead, so a reader knows before clicking that they are about to land
    on something killed. And the handle rides alongside the reference — a bare
    `R-0008` asks the reader to hold thirty-nine numbers in his head, which is the
    same complaint the bare `G4` earned."""
    dead = ref in LINKS["dead"]
    handle = LINKS["dead"].get(ref) or LINKS["live"].get(ref) or "not in the register"
    if dead:
        cls = (cls + " dead").strip()
        title = html.escape("DEAD — %s — %s" % (ref, handle), quote=True)
        label = '%s<span class="skull">&#8224;</span>' % ref
    else:
        title = html.escape("%s — %s" % (ref, handle), quote=True)
        label = ref
    name = ('<span class="cname">%s</span>' % html.escape(handle)) if named else ""
    return ('<a class="chip %s" href="#%s" data-goto="%s" title="%s">%s%s</a>'
            % (cls, ref, ref, title, label, name))


STATE_LABEL = {
    "never": "NEVER APPROVED",
    "invalidated": "APPROVAL INVALIDATED",
    "approved": "APPROVED",
}


def render(preamble, recs, graves, checks, register_hash, source_path, goals):
    LINKS["live"] = {r["ref"]: r["handle"] for r in recs}
    LINKS["dead"] = {g["ref"]: g["handle"] for g in graves}
    LINKS["goals"] = goals

    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    n_live, n_dead = len(recs), len(graves)
    n_approved = sum(1 for r in recs if r["state"] == "approved")
    n_inval = sum(1 for r in recs if r["state"] == "invalidated")
    n_never = sum(1 for r in recs if r["state"] == "never")
    n_deps = sum(1 for r in recs if r["deps"])
    n_edges = sum(len(r["deps"]) for r in recs)
    n_open = sum(len(r["open_markers"]) for r in recs)

    # ---- dependency map: only requirements that participate ----
    parts = []
    targets = sorted({d for r in recs for d in r["deps"]})
    for t in targets:
        dependents = sorted(r["ref"] for r in recs if t in r["deps"])
        title = next((r["handle"] for r in recs if r["ref"] == t), "")
        alive = any(r["ref"] == t for r in recs)
        parts.append(
            '<div class="mapbox%s"><div class="maphead">%s <span class="maphandle">%s</span>%s</div>'
            '<div class="maparrow">← needed by</div><div class="mapdeps">%s</div></div>'
            % ("" if alive else " missing", chip(t, named=False), html.escape(title),
               "" if alive else ' <span class="badge bad">NOT IN LIVE SET</span>',
               "".join(chip(d) for d in dependents)))
    depmap = "".join(parts) or '<p class="muted">No dependencies declared.</p>'

    # ---- requirement cards ----
    cards = []
    for r in recs:
        st = r["state"]
        deps_html = "".join(
            chip(d, "bad" if d in r["dangling"] else "") for d in r["deps"]) \
            or '<span class="muted">none</span>'
        rev_html = "".join(chip(d) for d in r["dependents"]) \
            or '<span class="muted">nothing depends on this</span>'
        traces_html = "".join(goal_tag(t) for t in r["traces_list"]) \
            if not r["untraced"] else \
            '<span class="tag warn">not yet traced</span>'
        notes_html = "".join(
            '<div class="note"><div class="notelabel">%s</div>%s</div>'
            % (html.escape(n["label"]), inline(n["text"])) for n in r["notes"])
        fpline = ('recorded fp:%s · now %s' % (r["recorded_fp"], r["fp"])
                  if r["recorded_fp"] else 'fingerprint now <b>%s</b> — none recorded' % r["fp"])

        cards.append("""
<article class="card state-{st}" id="{ref}" data-ref="{ref}" data-state="{st}"
         data-deps="{ndeps}" data-search="{search}">
  <header class="cardhead">
    <div class="hleft"><span class="ref">{ref}</span>
      <span class="handle">{handle}</span></div>
    <div class="hright"><span class="badge {st}">{label}</span></div>
  </header>
  <div class="fp" title="Computed from the fingerprint recipe, never read from a field">{fpline}</div>
  <div class="fields">
    <div class="field" data-field="statement">
      <div class="flabel">Statement{dmark}</div>
      <div class="fview">{statement}</div>
      <textarea class="fedit" hidden>{statement_raw}</textarea>
    </div>
    <div class="field" data-field="why">
      <div class="flabel">Why</div>
      <div class="fview">{why}</div>
      <textarea class="fedit" hidden>{why_raw}</textarea>
    </div>
    <div class="linkbox">
      <div class="linkcol">
        <div class="flabel">Traces to</div>
        <div class="fview taglist">{traces}</div>
        <textarea class="fedit" hidden data-field="traces to">{traces_raw}</textarea>
      </div>
      <div class="linkcol">
        <div class="flabel">Depends on <span class="src">stored</span></div>
        <div class="fview chips">{deps}</div>
        <textarea class="fedit" hidden data-field="depends on">{depends_raw}</textarea>
      </div>
      <div class="linkcol derivedcol">
        <div class="flabel">Depended on by <span class="src derived">derived — not in the file</span></div>
        <div class="fview chips">{rev}</div>
      </div>
    </div>
    <div class="field approval">
      <div class="flabel">Approval <span class="src">as written</span></div>
      <div class="fview">{approval}</div>
    </div>
    {notes}
  </div>
  <div class="cardtools">
    <button data-act="edit">Edit text</button>
    <button data-act="comment">Add comment</button>
    <button data-act="attach">Add link or image</button>
    <span class="dirty" hidden>● changed</span>
  </div>
  <div class="beside"></div>
</article>""".format(
            ref=r["ref"], st=st, label=STATE_LABEL[st],
            ndeps=len(r["deps"]),
            handle=html.escape(r["handle"]),
            search=html.escape((r["ref"] + " " + r["handle"] + " " + r["statement"]).lower()[:600], quote=True),
            fpline=fpline,
            dmark=' <span class="src">derived</span>' if r["derived"] else "",
            statement=inline(r["statement"]), statement_raw=html.escape(r["statement"]),
            why=inline(r["why"]), why_raw=html.escape(r["why"]),
            traces=traces_html, traces_raw=html.escape(r["traces"]),
            deps=deps_html, depends_raw=html.escape(r["depends"]),
            rev=rev_html,
            approval=inline(r["approval"]),
            notes=notes_html))

    # ---- graveyard ----
    gcards = []
    for g in graves:
        gcards.append("""
<article class="grave" id="{ref}" data-search="{search}">
  <header class="cardhead">
    <div class="hleft"><span class="ref">{ref}</span>
      <span class="badge dead">DEAD</span>
      <span class="handle">{handle}</span></div>
  </header>
  <div class="fields">
    <div class="field learned">
      <div class="flabel">What was learned <span class="src">read this before proposing again</span></div>
      <div class="fview">{learned}</div>
    </div>
    <div class="gcols">
      <div><div class="flabel">Killed</div>{killed}</div>
      <div><div class="flabel">Superseded by</div>{superseded}</div>
    </div>
    <details><summary>Statement as proposed, why it was proposed, why it is dead</summary>
      <div class="flabel">Statement as proposed</div>{statement}
      <div class="flabel">Why it was proposed</div>{why_proposed}
      <div class="flabel">Why it is dead</div>{why_dead}
    </details>
  </div>
</article>""".format(
            ref=g["ref"], handle=html.escape(g["handle"]),
            search=html.escape((g["ref"] + " " + g["handle"] + " " + g["learned"]).lower()[:600], quote=True),
            learned=inline(g["learned"]), killed=inline(g["killed"]),
            superseded=inline(g["superseded"]), statement=inline(g["statement"]),
            why_proposed=inline(g["why_proposed"]), why_dead=inline(g["why_dead"])))

    # ---- the goals and laws, so a reference has somewhere to land ----
    def gkey(g):
        return (0 if g["kind"] == "goal" else 1, g["ref"])

    used = set()
    for r in recs:
        for t in r["traces_list"]:
            used.add(" ".join(t.split()))
    gcardsg = []
    for g in sorted(goals.values(), key=gkey):
        cited = sorted(r["ref"] for r in recs
                       if any(" ".join(t.split()) == g["ref"] for t in r["traces_list"]))
        gcardsg.append(
            '<article class="goalcard %s" id="%s">'
            '<header class="cardhead"><div class="hleft">'
            '<span class="ref">%s</span><span class="handle">%s</span></div>'
            '<div class="hright"><span class="badge %s">%s</span></div></header>'
            '<div class="fview">%s</div>'
            '<div class="citedby"><span class="flabel">Traced to by</span>%s</div>'
            '</article>'
            % (g["kind"], g["anchor"], html.escape(g["ref"]), html.escape(g["name"]),
               g["kind"], "LAW — OBEYED, NOT ACHIEVED" if g["kind"] == "law" else "GOAL",
               inline(g["body"]),
               "".join(chip(c) for c in cited) or
               '<span class="muted">nothing traces to this</span>'))
    goals_html = "".join(gcardsg) or '<p class="muted">The goals file was not readable.</p>'

    # Every check below refused the render if it failed, so a page that exists is
    # a page that passed all of them. The list is the checking, shown — not a
    # backlog of things the reader is expected to forgive.
    checks_html = "".join(
        "<li><b>PASSED</b> %s</li>" % inline(c).replace("<p>", "").replace("</p>", "")
        for c in checks)

    # ---- hover previews: know without going ----
    # A reader following a dependency chain should rarely have to leave the block
    # they are reading. The click is for when you want to go there; this is for
    # when you only want to know. Three kinds, three different things to show.
    peek = {}
    for r in recs:
        peek[r["ref"]] = {
            "kind": "live", "ref": r["ref"], "title": r["handle"],
            "badge": STATE_LABEL[r["state"]], "bcls": r["state"],
            "body": flat(r["statement"]),
            "foot": ("depends on %s" % ", ".join(r["deps"]) if r["deps"] else "depends on nothing")
                    + " · " + ("needed by %s" % ", ".join(r["dependents"])
                               if r["dependents"] else "nothing needs it"),
        }
    for g in graves:
        peek[g["ref"]] = {
            "kind": "dead", "ref": g["ref"], "title": g["handle"],
            "badge": "DEAD", "bcls": "dead",
            "body": flat(g["killed"], 340) + '<div class="peeklabel">Statement as proposed</div>'
                    + flat(g["statement"], 300),
            "foot": "superseded by: " + " ".join(g["superseded"].split())[:150],
        }
    for g in goals.values():
        peek[g["anchor"]] = {
            "kind": g["kind"], "ref": g["ref"], "title": g["name"],
            "badge": "LAW" if g["kind"] == "law" else "GOAL", "bcls": g["kind"],
            "body": flat(g["body"], 620), "foot": "from docs/kerd-goals.md",
        }

    data = {
        "peek": peek,
        "generated": now,
        "source": source_path,
        "register_sha256": register_hash,
        "refs": [r["ref"] for r in recs],
        "live": {r["ref"]: r["handle"] for r in recs},
        "dead": {g["ref"]: g["handle"] for g in graves},
        "goals": {k: {"name": v["name"], "anchor": v["anchor"], "kind": v["kind"]}
                  for k, v in goals.items()},
        "fields": {r["ref"]: {"statement": r["statement"], "why": r["why"],
                              "traces to": r["traces"], "depends on": r["depends"],
                              "derived": r["derived"], "fp": r["fp"]}
                   for r in recs},
    }

    return (HTML
            .replace("__DATA__", json.dumps(data))
            .replace("__GENERATED__", html.escape(now))
            .replace("__SOURCE__", html.escape(source_path))
            .replace("__HASH__", register_hash[:16])
            .replace("__NLIVE__", str(n_live))
            .replace("__NDEAD__", str(n_dead))
            .replace("__NAPPROVED__", str(n_approved))
            .replace("__NINVAL__", str(n_inval))
            .replace("__NNEVER__", str(n_never))
            .replace("__NDEPS__", str(n_deps))
            .replace("__NEDGES__", str(n_edges))
            .replace("__NOPEN__", str(n_open))
            .replace("__DEPMAP__", depmap)
            .replace("__CARDS__", "".join(cards))
            .replace("__GRAVES__", "".join(gcards))
            .replace("__GOALS__", goals_html)
            .replace("__NGOALS__", str(sum(1 for g in goals.values() if g["kind"] == "goal")))
            .replace("__NLAWS__", str(sum(1 for g in goals.values() if g["kind"] == "law")))
            .replace("__NOTES__", checks_html)
            .replace("__NNOTES__", str(len(checks))))


# --------------------------------------------------------------------------
# the page
# --------------------------------------------------------------------------

HTML = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Requirements — Kerd</title>
<style>
:root{
  --ink:#1b1b1b; --dim:#5d5d5d; --faint:#8a8a8a;
  --paper:#f7f6f3; --box:#ffffff; --line:#d8d5cd;
  --unapproved:#b3541e; --unapproved-bg:#fdf1e7;
  --inval:#8a1c1c; --ok:#1f6f3d;
  --derive:#2a5f8f; --derive-bg:#eaf1f8;
  --dead:#6a6a6a; --dead-bg:#f0efeb;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  font-size:16px; line-height:1.55;
}
.wrap{max-width:1060px;margin:0 auto;padding:0 20px 120px}
h1{font-size:26px;margin:0 0 4px}
h2{font-size:19px;margin:44px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--line)}
p{margin:0 0 10px}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.9em;
  background:#eeece6;padding:1px 4px;border-radius:3px}
.muted{color:var(--faint)}
.src{font-size:11px;font-weight:400;color:var(--faint);text-transform:none;letter-spacing:0}
.src.derived{color:var(--derive)}

/* ---------- the honest banner ---------- */
header.top{background:var(--box);border-bottom:1px solid var(--line);padding:18px 0 0}
.topinner{max-width:1060px;margin:0 auto;padding:0 20px}
.sub{color:var(--dim);font-size:13px;margin-bottom:14px}
.verdict{
  background:var(--unapproved-bg); border:2px solid var(--unapproved);
  border-radius:6px; padding:14px 16px; margin-bottom:14px;
  background-image:repeating-linear-gradient(45deg,rgba(179,84,30,.05) 0 10px,transparent 10px 20px);
}
.verdict b{color:var(--unapproved);font-size:17px;display:block;margin-bottom:4px}
.verdict span{font-size:13px;color:var(--dim)}
.counts{display:flex;flex-wrap:wrap;gap:8px;padding-bottom:14px}
.count{background:var(--paper);border:1px solid var(--line);border-radius:5px;
  padding:6px 10px;font-size:13px}
.count b{font-size:17px;display:block;line-height:1.2}
.count.warn b{color:var(--unapproved)}
.bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;
  padding:10px 0;border-top:1px solid var(--line);position:sticky;top:0;
  background:var(--box);z-index:20}
input[type=search]{flex:1;min-width:180px;padding:7px 10px;border:1px solid var(--line);
  border-radius:5px;font:inherit;font-size:14px;background:var(--paper)}
button{font:inherit;font-size:13px;padding:6px 11px;border:1px solid var(--line);
  background:var(--paper);border-radius:5px;cursor:pointer;color:var(--ink)}
button:hover{background:#ece9e2}
button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
button.primary{background:var(--unapproved);color:#fff;border-color:var(--unapproved);font-weight:600}
button.primary:hover{background:#96461a}

/* ---------- boxes ---------- */
.card,.grave{background:var(--box);border:1px solid var(--line);border-radius:7px;
  margin:0 0 14px;padding:14px 16px}
.card.state-never{border-left:6px solid var(--unapproved);background:var(--box)}
.card.state-invalidated{border-left:6px solid var(--inval)}
.card.state-approved{border-left:6px solid var(--ok)}
/* ---- arriving somewhere: the landed-on block says so, loudly and briefly ---- */
@keyframes land{
  0%{box-shadow:0 0 0 6px rgba(42,95,143,.32);background:#e6f0f9}
  70%{box-shadow:0 0 0 6px rgba(42,95,143,.20)}
  100%{box-shadow:0 0 0 6px rgba(42,95,143,0)}
}
.hit{outline:3px solid var(--derive);outline-offset:3px;animation:land 1.8s ease-out;
  scroll-margin-top:120px;position:relative}
.hit::before{content:"you jumped here";position:absolute;top:-11px;left:12px;
  background:var(--derive);color:#fff;font-size:10px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;padding:2px 7px;border-radius:3px}
.card,.grave,.goalcard{scroll-margin-top:120px}
@media (prefers-reduced-motion:reduce){.hit{animation:none}}
.cardhead{display:flex;justify-content:space-between;gap:12px;align-items:baseline;
  flex-wrap:wrap;margin-bottom:8px}
.hleft{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.ref{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-weight:700;font-size:15px}
.handle{font-size:15px;color:var(--dim)}
.badge{font-size:11px;font-weight:700;letter-spacing:.05em;padding:3px 8px;border-radius:4px;
  border:1px solid}
.badge.never{background:var(--unapproved-bg);color:var(--unapproved);border-color:var(--unapproved)}
.badge.invalidated{background:#fbecec;color:var(--inval);border-color:var(--inval)}
.badge.approved{background:#e9f5ed;color:var(--ok);border-color:var(--ok)}
.badge.dead{background:var(--dead-bg);color:var(--dead);border-color:#c5c2ba}
.badge.bad{background:#fbecec;color:var(--inval);border-color:var(--inval)}
.fp{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:11px;
  color:var(--faint);margin-bottom:10px}
.flabel{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--faint);margin:12px 0 4px}
.field:first-child .flabel{margin-top:0}
.fview{font-size:15px}
.fview p{margin:0 0 8px}
.fview p:last-child{margin-bottom:0}
em.his{font-style:italic;background:#fff6d9;box-shadow:inset 0 -1px 0 #e7d089;padding:0 2px}
.open{background:#fdf1e7;border:1px dashed var(--unapproved);color:var(--unapproved);
  padding:0 3px;border-radius:3px}
textarea.fedit{width:100%;min-height:92px;font:inherit;font-size:14px;padding:9px;
  border:2px solid var(--derive);border-radius:5px;background:#fff;line-height:1.5}

/* ---------- the dependency box ---------- */
.linkbox{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px;
  border:1px solid var(--line);border-radius:6px;padding:10px 12px;background:#fbfaf7}
.linkcol{min-width:0}
.derivedcol{background:var(--derive-bg);margin:-10px -12px -10px 0;padding:10px 12px;
  border-left:1px dashed var(--derive);border-radius:0 6px 6px 0}
.chips{display:flex;flex-wrap:wrap;gap:5px}
.chip{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12px;
  text-decoration:none;color:var(--ink);background:#fff;border:1px solid var(--line);
  border-radius:4px;padding:2px 7px}
.chip:hover{background:var(--ink);color:#fff}
.chip .cname{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  color:var(--dim);margin-left:6px;font-size:12px}
.chip:hover .cname{color:#e6e6e6}
.chip.dead .cname{color:#8f8c85}
.chip.bad{border-color:var(--inval);color:var(--inval)}
/* a chip or reference pointing into the graveyard is drawn dead BEFORE it is clicked */
.chip.dead,.xref.dead{background:var(--dead-bg);border-color:#c5c2ba;color:var(--dead);
  text-decoration:line-through;text-decoration-color:#b0ada5}
.chip.dead:hover,.xref.dead:hover{background:var(--dead);color:#fff;text-decoration:line-through}
.skull{text-decoration:none;display:inline-block;margin-left:2px;font-size:.85em;vertical-align:super}

/* ---- every reference in prose is a jump ---- */
.xref{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;
  color:var(--derive);text-decoration:none;border-bottom:1px solid rgba(42,95,143,.4);
  padding:0 1px;border-radius:2px}
.xref:hover{background:var(--derive);color:#fff;border-bottom-color:transparent}
.xref.missing{color:var(--inval);border-bottom:1px dashed var(--inval);cursor:help}
.xgoal{color:#5a4a12;text-decoration:none;border-bottom:1px dotted #b09a4a;
  background:#fbf6e6;padding:0 2px;border-radius:2px;cursor:help}
.xgoal:hover{background:#8a6d1a;color:#fff;border-bottom-color:transparent}

.taglist{display:flex;flex-wrap:wrap;gap:5px}
.tag{font-size:12px;background:#eef0ea;border:1px solid var(--line);border-radius:4px;padding:2px 7px}
a.tag{text-decoration:none;color:var(--ink);display:inline-flex;gap:5px;align-items:baseline}
a.tag:hover{background:var(--ink);color:#fff;border-color:var(--ink)}
a.tag .gname{font-size:11.5px;color:var(--dim)}
a.tag:hover .gname{color:#e6e6e6}
.tag.law{background:#e8ecf3}
.tag.warn{background:var(--unapproved-bg);border-color:var(--unapproved);color:var(--unapproved)}

/* ---- the goals and laws, at the foot of the page ---- */
.goalcard{background:var(--box);border:1px solid var(--line);border-left:6px solid #b09a4a;
  border-radius:7px;margin:0 0 14px;padding:14px 16px}
.goalcard.law{border-left-color:var(--derive)}
.goalcard .fview{font-size:14.5px;color:var(--dim)}
.badge.goal{background:#fbf6e6;color:#5a4a12;border-color:#b09a4a}
.badge.law{background:var(--derive-bg);color:var(--derive);border-color:var(--derive)}
.citedby{margin-top:10px;padding-top:8px;border-top:1px solid var(--line);
  display:flex;gap:5px;align-items:baseline;flex-wrap:wrap}
.citedby .flabel{margin:0 4px 0 0}
.note{border-left:3px solid var(--line);padding:6px 0 6px 10px;margin-top:12px;
  font-size:14px;color:var(--dim)}
.notelabel{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  color:var(--faint);margin-bottom:3px}
.approval .fview{font-size:14px;color:var(--dim)}
.cardtools{display:flex;gap:8px;margin-top:14px;padding-top:10px;border-top:1px solid var(--line);
  flex-wrap:wrap;align-items:center}
.dirty{font-size:12px;color:var(--derive);font-weight:600}

/* ---------- beside the requirement ---------- */
.beside:empty{display:none}
.beside{margin-top:10px;display:flex;flex-direction:column;gap:8px}
.item{background:var(--derive-bg);border:1px solid #c3d5e6;border-radius:5px;padding:8px 10px;
  font-size:14px;position:relative}
.item .kind{font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--derive);margin-bottom:3px}
.item.formodel{background:#fff6d9;border-color:#e7d089}
.item.formodel .kind{color:#8a6d1a}
.item img{max-width:100%;border-radius:4px;margin-top:6px;display:block;border:1px solid var(--line)}
.item a{color:var(--derive);word-break:break-all}
.item .rm{position:absolute;top:6px;right:6px;padding:1px 7px;font-size:12px}
.composer{background:#fff;border:2px solid var(--derive);border-radius:6px;padding:10px}
.composer textarea{width:100%;min-height:70px;font:inherit;font-size:14px;padding:8px;
  border:1px solid var(--line);border-radius:4px}
.composer input[type=text]{width:100%;font:inherit;font-size:14px;padding:7px;
  border:1px solid var(--line);border-radius:4px;margin-bottom:6px}
.composer .row{display:flex;gap:8px;align-items:center;margin-top:8px;flex-wrap:wrap}
label.chk{font-size:13px;display:flex;gap:5px;align-items:center;cursor:pointer}

/* ---------- map ---------- */
.map{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}
.mapbox{background:var(--box);border:1px solid var(--line);border-left:5px solid var(--derive);
  border-radius:6px;padding:10px 12px}
.mapbox.missing{border-left-color:var(--inval)}
.maphead{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-weight:700;font-size:14px}
.maphandle{font-family:inherit;font-weight:400;color:var(--dim);font-size:13px}
.maparrow{font-size:11px;color:var(--faint);margin:6px 0 4px;text-transform:uppercase;letter-spacing:.06em}
.mapdeps{display:flex;flex-wrap:wrap;gap:5px}

/* ---------- graveyard ---------- */
.grave{background:var(--dead-bg);border-left:6px solid #b8b5ad}
.grave .learned{background:#fff;border:1px solid var(--line);border-radius:5px;padding:10px 12px}
.gcols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;font-size:14px;color:var(--dim)}
details{margin-top:12px}
summary{cursor:pointer;font-size:13px;color:var(--derive)}
.findings li{margin-bottom:6px;font-size:14px}

/* ---------- the hover preview: a look, not a journey ---------- */
#peek{position:fixed;z-index:60;max-width:440px;width:max-content;
  background:var(--box);border:1px solid var(--ink);border-left:6px solid var(--derive);
  border-radius:7px;padding:11px 13px;box-shadow:0 8px 26px rgba(0,0,0,.18);
  font-size:13.5px;line-height:1.5;pointer-events:none}
#peek.dead{border-left-color:var(--dead);background:var(--dead-bg)}
#peek.goal{border-left-color:#b09a4a}
#peek.law{border-left-color:var(--derive)}
#peek .peekhead{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;margin-bottom:7px}
#peek .peekref{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-weight:700;font-size:13px}
#peek .peektitle{color:var(--dim)}
#peek p{margin:0 0 6px}
#peek p:last-child{margin-bottom:0}
#peek .peeklabel{font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  color:var(--faint);margin:8px 0 3px}
#peek .peekfoot{margin-top:8px;padding-top:6px;border-top:1px solid var(--line);
  font-size:11.5px;color:var(--faint)}
#peek .peekgo{font-size:11px;color:var(--derive);font-weight:600}

/* ---------- handover ---------- */
.dock{position:fixed;left:0;right:0;bottom:0;background:var(--box);
  border-top:2px solid var(--unapproved);padding:10px 20px;z-index:40;
  box-shadow:0 -4px 14px rgba(0,0,0,.07)}
.dockinner{max-width:1060px;margin:0 auto;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.dockinner .grow{flex:1;font-size:13px;color:var(--dim)}
.panel{position:fixed;inset:5% 5% 5% 5%;background:var(--box);border:2px solid var(--ink);
  border-radius:8px;z-index:50;display:flex;flex-direction:column;padding:14px}
.panel textarea{flex:1;width:100%;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:12px;padding:10px;border:1px solid var(--line);border-radius:5px;line-height:1.5}
.panel .row{display:flex;gap:8px;align-items:center;margin-bottom:10px;flex-wrap:wrap}
[hidden]{display:none !important}
@media (max-width:760px){.linkbox{grid-template-columns:1fr}.derivedcol{margin:0;border-left:none;
  border-top:1px dashed var(--derive);border-radius:0 0 6px 6px}.gcols{grid-template-columns:1fr}}
</style>
</head><body>

<header class="top"><div class="topinner">
  <h1>Requirements &mdash; Kerd</h1>
  <div class="sub">Generated __GENERATED__ from <code>__SOURCE__</code> &middot;
    register sha256 <code>__HASH__…</code> &middot;
    <b>this page is a view. The markdown file is the only writable surface.</b></div>

  <div class="verdict">
    <b>Nothing in this set is approved.</b>
    <span>__NNEVER__ of __NLIVE__ live requirements have never been approved,
    __NINVAL__ have an approval invalidated by a later edit, __NAPPROVED__ are approved.
    Every state on this page is <b>computed from the fingerprint recipe</b> (shape rule 9)
    over Statement, Why, Traces to and Depends on. The register has no status field and
    this view invents none.</span>
  </div>

  <div class="counts">
    <div class="count"><b>__NLIVE__</b>live</div>
    <div class="count warn"><b>__NNEVER__</b>never approved</div>
    <div class="count warn"><b>__NINVAL__</b>invalidated</div>
    <div class="count"><b>__NAPPROVED__</b>approved</div>
    <div class="count"><b>__NDEPS__</b>with dependencies</div>
    <div class="count"><b>__NEDGES__</b>dependency links</div>
    <div class="count"><b>__NOPEN__</b>open markers</div>
    <div class="count"><b>__NDEAD__</b>in the graveyard</div>
    <div class="count"><b>__NNOTES__</b>format checks passed</div>
  </div>

  <div class="bar">
    <input type="search" id="q" placeholder="Search reference, handle or statement…">
    <button data-filter="all" class="on">All</button>
    <button data-filter="never">Unapproved</button>
    <button data-filter="deps">Has dependencies</button>
    <button data-filter="changed">Changed by me</button>
    <button id="jumpgrave">Graveyard</button>
    <button id="jumpgoals">Goals &amp; laws</button>
  </div>
</div></header>

<div class="wrap">

<h2>Dependency map &mdash; stored one way, reverse derived</h2>
<p class="muted">Each requirement stores only what it <b>depends on</b>. The
&ldquo;needed by&rdquo; direction below and on every card is computed here and is never
written into the file &mdash; a hand-written reverse is a copy that drifts.</p>
<div class="map">__DEPMAP__</div>

<h2>Requirements &mdash; __NLIVE__ live</h2>
<div id="cards">__CARDS__</div>

<h2 id="graveyard">Graveyard &mdash; __NDEAD__ dead, and what each one taught</h2>
<p class="muted">Read <b>what was learned</b> before proposing anything in this
territory. That is the field's whole purpose: a killed idea is not proposed again.</p>
<div id="graves">__GRAVES__</div>

<h2 id="goals">What the set serves &mdash; __NGOALS__ goals and __NLAWS__ laws</h2>
<p class="muted">Every <b>Traces to</b> target on this page carries its name, and every
<code>G</code><i>n</i> or <code>Law </code><i>n</i> anywhere in the prose above jumps here.
Names and text are quoted from <code>docs/kerd-goals.md</code>, unshortened. The goals sit
at the foot of the page on purpose &mdash; a reader arrives to read requirements.</p>
<div id="goalcards">__GOALS__</div>

<h2>What this view checked in the format</h2>
<p class="muted">Rule 14: <b>ambiguity is refused, never guessed.</b> Each check
below stops the render when it fails, naming the block and the text it could not
classify &mdash; so this page existing is the result. Nothing here is a warning
the reader is asked to live with.</p>
<ul class="findings">__NOTES__</ul>

</div>

<div class="dock"><div class="dockinner">
  <span class="grow" id="dockmsg">No changes yet. Edits, comments and attachments
    accumulate here and leave as one block.</span>
  <button id="clear">Discard all</button>
  <button class="primary" id="handover">Copy handover block</button>
</div></div>

<div id="peek" hidden></div>

<div class="panel" id="panel" hidden>
  <div class="row">
    <b>Handover block</b>
    <span class="muted" id="panelmsg">Copied to the clipboard. Paste it to the model.</span>
    <span style="flex:1"></span>
    <button class="primary" id="recopy">Copy again</button>
    <button id="closepanel">Close</button>
  </div>
  <textarea id="out" spellcheck="false"></textarea>
</div>

<script>
"use strict";
const DATA = __DATA__;

/* ---- SHA-256, written here so the page needs no crypto.subtle and no library.
   Lets an edited requirement recompute its fingerprint live, offline, on file://. ---- */
function sha256(str){
  const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
  0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
  0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
  0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
  0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
  0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
  0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
  0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  let H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
  const bytes=new TextEncoder().encode(str);
  const l=bytes.length, withOne=l+1, padded=withOne+((56-withOne%64)+64)%64, total=padded+8;
  const m=new Uint8Array(total); m.set(bytes); m[l]=0x80;
  const bits=l*8; const dv=new DataView(m.buffer);
  dv.setUint32(total-8, Math.floor(bits/0x100000000)); dv.setUint32(total-4, bits>>>0);
  const w=new Uint32Array(64);
  const rr=(x,n)=>(x>>>n)|(x<<(32-n));
  for(let i=0;i<total;i+=64){
    for(let t=0;t<16;t++) w[t]=dv.getUint32(i+t*4);
    for(let t=16;t<64;t++){
      const s0=rr(w[t-15],7)^rr(w[t-15],18)^(w[t-15]>>>3);
      const s1=rr(w[t-2],17)^rr(w[t-2],19)^(w[t-2]>>>10);
      w[t]=(w[t-16]+s0+w[t-7]+s1)>>>0;
    }
    let [a,b,c,d,e,f,g,h]=H;
    for(let t=0;t<64;t++){
      const S1=rr(e,6)^rr(e,11)^rr(e,25), ch=(e&f)^(~e&g);
      const t1=(h+S1+ch+K[t]+w[t])>>>0;
      const S0=rr(a,2)^rr(a,13)^rr(a,22), maj=(a&b)^(a&c)^(b&c);
      const t2=(S0+maj)>>>0;
      h=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0;
    }
    H=[H[0]+a,H[1]+b,H[2]+c,H[3]+d,H[4]+e,H[5]+f,H[6]+g,H[7]+h].map(x=>x>>>0);
  }
  return H.map(x=>x.toString(16).padStart(8,"0")).join("");
}
const collapse = s => s.trim().replace(/\s+/g," ");
function fingerprint(f){
  const stmt = (f.derived ? "derived: " : "") + f["statement"];
  return sha256([stmt,f["why"],f["traces to"],f["depends on"]].map(collapse).join("\n")).slice(0,12);
}

/* ---- state: everything the producer does accumulates here ---- */
const KEY = "reqview:"+DATA.register_sha256.slice(0,12);
let S = {edits:{}, comments:[], attachments:[]};
try{ const raw=localStorage.getItem(KEY); if(raw) S=JSON.parse(raw); }catch(e){}
function save(){ try{ localStorage.setItem(KEY, JSON.stringify(S)); }catch(e){} }

const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const esc=s=>s.replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
/* Same cross-reference rule as the generator: every reference is a jump, a dead
   one looks dead before it is clicked, and a goal or law never travels bare. */
function linkify(x){
  x=x.replace(/\bR-\d{4}\b/g,r=>{
    if(DATA.live[r]!==undefined)
      return '<a class="xref" href="#'+r+'" data-goto="'+r+'" title="'+esc(r+" — "+DATA.live[r])+'">'+r+'</a>';
    if(DATA.dead[r]!==undefined)
      return '<a class="xref dead" href="#'+r+'" data-goto="'+r+'" title="'+esc("DEAD — "+r+" — "+DATA.dead[r])+
             '">'+r+'<span class="skull">†</span></a>';
    return '<span class="xref missing" title="Not in this register">'+r+'</span>';
  });
  x=x.replace(/\bLaw\s+[1-9]\b|\bG[1-8]\b/g,m=>{
    const k=m.replace(/\s+/," "), g=DATA.goals[k];
    if(!g) return m;
    return '<a class="xgoal '+g.kind+'" href="#'+g.anchor+'" data-goto="'+g.anchor+
           '" title="'+esc(k+" — "+g.name)+'">'+m+'</a>';
  });
  return x;
}
function goalTag(t){
  const k=t.replace(/\s+/g," ").trim(), g=DATA.goals[k];
  if(!g) return '<span class="tag warn">'+esc(t)+'</span>';
  return '<a class="tag '+g.kind+'" href="#'+g.anchor+'" data-goto="'+g.anchor+'" title="'+
    esc(k+" — "+g.name)+'"><b>'+esc(k)+'</b> <span class="gname">'+esc(g.name)+'</span></a>';
}
function md(t){
  let x=esc(t);
  x=x.replace(/`([^`]+)`/g,"<code>$1</code>");
  x=x.replace(/\[(OPEN-[^\]]+)\]/g,'<span class="open">[$1]</span>');
  x=x.replace(/\*\*([\s\S]+?)\*\*/g,"<strong>$1</strong>");
  x=x.replace(/\*(&quot;[\s\S]+?&quot;)\*/g,'<em class="his">$1</em>');
  x=x.replace(/\*([\s\S]+?)\*/g,"<em>$1</em>");
  x=linkify(x);
  return x.split(/\n\n+/).filter(p=>p.trim()).map(p=>"<p>"+p.replace(/\n/g," ")+"</p>").join("");
}
function count(){
  return Object.keys(S.edits).reduce((n,r)=>n+Object.keys(S.edits[r]).length,0)
       + S.comments.length + S.attachments.length;
}
function refresh(){
  const n=count();
  $("#dockmsg").textContent = n===0
    ? "No changes yet. Edits, comments and attachments accumulate here and leave as one block."
    : n+" change"+(n===1?"":"s")+" pending — "
      + Object.keys(S.edits).length+" requirement(s) edited, "
      + S.comments.length+" comment(s), "+S.attachments.length+" attachment(s). "
      + "One click copies them all out.";
  $$(".card").forEach(c=>{
    const r=c.dataset.ref, has=!!(S.edits[r]&&Object.keys(S.edits[r]).length);
    $(".dirty",c).hidden=!has;
    c.dataset.changed = has ? "1":"0";
  });
  if(typeof dropTitles==="function") dropTitles(document);
  save();
}

/* ---- render the beside-space (comments, links, images) ---- */
function renderBeside(ref){
  const card=document.getElementById(ref); if(!card) return;
  const box=$(".beside",card);
  const keep=$(".composer",box);
  box.innerHTML="";
  S.comments.filter(c=>c.ref===ref).forEach(c=>{
    const d=document.createElement("div");
    d.className="item"+(c.forModel?" formodel":"");
    d.innerHTML='<button class="rm">remove</button><div class="kind">'
      +(c.forModel?"comment — for the model to pick up":"note — around this requirement")
      +' · '+esc(c.at)+'</div>'+md(c.text);
    $(".rm",d).onclick=()=>{S.comments.splice(S.comments.indexOf(c),1);renderBeside(ref);refresh();};
    box.appendChild(d);
  });
  S.attachments.filter(a=>a.ref===ref).forEach(a=>{
    const d=document.createElement("div"); d.className="item";
    let body = a.kind==="image"
      ? '<div>'+esc(a.title||a.name)+'</div><img src="'+a.data+'" alt="'+esc(a.title||a.name)+'">'
      : '<div>'+esc(a.title||"")+'</div><a href="'+esc(a.url)+'" target="_blank" rel="noopener">'+esc(a.url)+'</a>';
    d.innerHTML='<button class="rm">remove</button><div class="kind">'
      +(a.kind==="image"?"image — input":"link — input")+' · '+esc(a.at)+'</div>'+body;
    $(".rm",d).onclick=()=>{S.attachments.splice(S.attachments.indexOf(a),1);renderBeside(ref);refresh();};
    box.appendChild(d);
  });
  if(keep) box.appendChild(keep);
}

/* ---- editing ---- */
function toggleEdit(card){
  const ref=card.dataset.ref, on=card.dataset.editing==="1";
  $$(".field,.linkcol",card).forEach(f=>{
    const ta=$("textarea.fedit",f), v=$(".fview",f);
    if(!ta) return;
    ta.hidden=on; if(v) v.hidden=!on;
  });
  card.dataset.editing = on?"0":"1";
  $('[data-act=edit]',card).textContent = on ? "Edit text" : "Done editing";
  if(on) applyEdits(card, ref);
}
function fieldName(f){
  return f.dataset.field || $("textarea.fedit",f).dataset.field;
}
function applyEdits(card, ref){
  const f = Object.assign({}, DATA.fields[ref]);
  $$(".field,.linkcol",card).forEach(el=>{
    const ta=$("textarea.fedit",el); if(!ta) return;
    const name=fieldName(el), val=ta.value;
    const orig=DATA.fields[ref][name];
    if(collapse(val)!==collapse(orig)){
      S.edits[ref]=S.edits[ref]||{};
      S.edits[ref][name]={was:orig, now:val};
    } else if(S.edits[ref]){ delete S.edits[ref][name]; }
    f[name]=val;
    const v=$(".fview",el);
    if(name==="depends on"){
      const refs=(val.match(/R-\d{4}/g)||[]);
      v.innerHTML = refs.length ? refs.map(r=>{
        const dead=DATA.dead[r]!==undefined;
        const h = dead ? DATA.dead[r]
                : (DATA.live[r]!==undefined?DATA.live[r]:"not in the register");
        const title = (dead?"DEAD — ":"")+r+" — "+h;
        return '<a class="chip'+(dead?" dead":"")+'" href="#'+r+'" data-goto="'+r+
               '" title="'+esc(title)+'">'+r+(dead?'<span class="skull">†</span>':'')+
               '<span class="cname">'+esc(h)+'</span></a>';
      }).join("") : '<span class="muted">none</span>';
    } else if(name==="traces to"){
      v.innerHTML = val.split(",").map(t=>t.trim()).filter(Boolean).map(goalTag).join("");
    } else { v.innerHTML = md(val); }
  });
  if(S.edits[ref] && !Object.keys(S.edits[ref]).length) delete S.edits[ref];
  const now=fingerprint(f);
  const fpEl=$(".fp",card);
  fpEl.innerHTML = now===DATA.fields[ref].fp
    ? fpEl.dataset.orig || fpEl.innerHTML
    : "fingerprint was <b>"+DATA.fields[ref].fp+"</b> → now <b>"+now+
      "</b> — any approval over the old text no longer holds";
  refresh();
}

/* ---- composers ---- */
function composer(card, kind){
  const ref=card.dataset.ref, box=$(".beside",card);
  const old=$(".composer",box); if(old) old.remove();
  const c=document.createElement("div"); c.className="composer";
  if(kind==="comment"){
    c.innerHTML='<textarea placeholder="A comment or a note around '+ref+
      '. Markdown is fine."></textarea>'+
      '<div class="row"><label class="chk"><input type="checkbox" checked> '+
      'for the model to pick up</label><span style="flex:1"></span>'+
      '<button class="primary">Add comment</button><button class="cancel">Cancel</button></div>';
    $("button.primary",c).onclick=()=>{
      const t=$("textarea",c).value.trim(); if(!t) return;
      S.comments.push({ref, text:t, forModel:$("input",c).checked,
        at:new Date().toISOString().slice(0,16).replace("T"," ")});
      c.remove(); renderBeside(ref); refresh();
    };
  } else {
    c.innerHTML='<input type="text" class="t" placeholder="Title or caption (optional)">'+
      '<input type="text" class="u" placeholder="https://… paste a link">'+
      '<div class="row"><label class="chk">or an image: <input type="file" accept="image/*"></label>'+
      '<span style="flex:1"></span><button class="primary">Attach</button>'+
      '<button class="cancel">Cancel</button></div>'+
      '<div class="muted" style="font-size:12px;margin-top:6px">Images are inlined into the '+
      'page and into the handover block as data URIs. Large images make a large block.</div>';
    $("button.primary",c).onclick=()=>{
      const title=$(".t",c).value.trim(), url=$(".u",c).value.trim();
      const file=$("input[type=file]",c).files[0];
      const at=new Date().toISOString().slice(0,16).replace("T"," ");
      if(file){
        const fr=new FileReader();
        fr.onload=()=>{S.attachments.push({ref,kind:"image",name:file.name,title,
          data:fr.result,bytes:file.size,at}); c.remove(); renderBeside(ref); refresh();};
        fr.readAsDataURL(file);
      } else if(url){
        S.attachments.push({ref,kind:"link",url,title,at});
        c.remove(); renderBeside(ref); refresh();
      }
    };
  }
  $("button.cancel",c).onclick=()=>c.remove();
  box.appendChild(c);
  const first=$("textarea",c)||$("input",c); if(first) first.focus();
}

/* ---- the handover block: one action out ---- */
function handover(){
  const L=[];
  L.push("# Requirements handover — paste-back");
  L.push("");
  L.push("- register: `"+DATA.source+"`");
  L.push("- register sha256 at render time: `"+DATA.register_sha256+"`");
  L.push("- view generated: "+DATA.generated);
  L.push("- handed over: "+new Date().toISOString().slice(0,16).replace("T"," "));
  L.push("");
  L.push("> Apply only if the register still hashes to the value above. If it does not,");
  L.push("> the view was stale — refuse and regenerate rather than applying blind.");
  L.push("");
  const refs=Object.keys(S.edits).sort();
  L.push("## Edits — "+refs.length+" requirement(s)");
  L.push("");
  if(!refs.length) L.push("_none_");
  refs.forEach(r=>{
    L.push("### "+r);
    const f=Object.assign({},DATA.fields[r]);
    Object.keys(S.edits[r]).forEach(k=>{
      f[k]=S.edits[r][k].now;
      L.push("");
      L.push("**"+k+"** — was:");
      L.push("");
      L.push("```");L.push(S.edits[r][k].was);L.push("```");
      L.push("");
      L.push("**"+k+"** — now:");
      L.push("");
      L.push("```");L.push(S.edits[r][k].now);L.push("```");
    });
    L.push("");
    L.push("fingerprint "+DATA.fields[r].fp+" → "+fingerprint(f)+
      " (any approval over the old text is invalidated)");
    L.push("");
  });
  L.push("");
  L.push("## Comments — "+S.comments.length);
  L.push("");
  if(!S.comments.length) L.push("_none_");
  S.comments.forEach(c=>{
    L.push("### "+c.ref+" — "+(c.forModel?"FOR THE MODEL TO PICK UP":"note")+" · "+c.at);
    L.push("");L.push(c.text);L.push("");
  });
  L.push("");
  L.push("## Attachments — "+S.attachments.length);
  L.push("");
  if(!S.attachments.length) L.push("_none_");
  S.attachments.forEach(a=>{
    L.push("### "+a.ref+" — "+a.kind+" · "+a.at);
    if(a.title) L.push("");L.push(a.title||"");
    L.push("");
    if(a.kind==="link") L.push("- url: "+a.url);
    else { L.push("- image: `"+a.name+"` ("+a.bytes+" bytes), inlined below as a data URI");
           L.push("");L.push("```");L.push(a.data);L.push("```"); }
    L.push("");
  });
  L.push("");
  L.push("_Comments and attachments live beside the requirement and never touch its");
  L.push("fingerprint. Only the edits above change approval state._");
  return L.join("\n");
}
function copyOut(){
  const text=handover();
  $("#out").value=text;
  $("#panel").hidden=false;
  const ta=$("#out"); ta.focus(); ta.select();
  let ok=false;
  try{ ok=document.execCommand("copy"); }catch(e){}
  if(!ok && navigator.clipboard){
    navigator.clipboard.writeText(text).then(()=>{
      $("#panelmsg").textContent="Copied to the clipboard. Paste it to the model.";
    }).catch(()=>{ $("#panelmsg").textContent="Select all and copy — the browser blocked the clipboard."; });
  } else {
    $("#panelmsg").textContent = ok
      ? "Copied to the clipboard. Paste it to the model."
      : "Select all and copy — the browser blocked the clipboard.";
  }
}

/* ---- wiring ---- */
/* Landing on the target has to be unmistakable: nothing worse than jumping and
   then having to hunt. A target hidden by the current filter or search is
   revealed first, otherwise the jump silently does nothing. */
let hitTimer=null;
function goTo(id){
  const t=document.getElementById(id);
  if(!t) return false;
  if(typeof hidePeek==="function") hidePeek();
  if(t.hidden){ $("#q").value=""; $$("button[data-filter]").forEach(x=>
      x.classList.toggle("on", x.dataset.filter==="all")); applyFilter("all"); }
  $$(".hit").forEach(x=>x.classList.remove("hit"));
  t.scrollIntoView({behavior:"smooth",block:"center"});
  /* restart the animation even when the same target is hit twice in a row */
  void t.offsetWidth; t.classList.add("hit");
  clearTimeout(hitTimer); hitTimer=setTimeout(()=>t.classList.remove("hit"),2600);
  history.replaceState(null,"","#"+id);
  return true;
}
document.addEventListener("click",e=>{
  const g=e.target.closest("[data-goto]");
  if(g){ e.preventDefault(); goTo(g.dataset.goto); return; }
  const b=e.target.closest("button[data-act]");
  if(b){ const card=b.closest(".card");
    if(b.dataset.act==="edit") toggleEdit(card);
    else composer(card, b.dataset.act==="comment"?"comment":"attach");
  }
});
$$("button[data-filter]").forEach(b=>b.onclick=()=>{
  $$("button[data-filter]").forEach(x=>x.classList.remove("on"));
  b.classList.add("on"); applyFilter(b.dataset.filter);
});
let FILTER="all";
function applyFilter(f){
  if(f) FILTER=f;
  const q=$("#q").value.trim().toLowerCase();
  $$(".card").forEach(c=>{
    let show=true;
    if(FILTER==="never") show = c.dataset.state!=="approved";
    if(FILTER==="deps") show = c.dataset.deps!=="0";
    if(FILTER==="changed") show = c.dataset.changed==="1";
    if(show && q) show = c.dataset.search.includes(q);
    c.hidden=!show;
  });
  $$(".grave").forEach(g=>{ g.hidden = !!q && !g.dataset.search.includes(q); });
}
$("#q").oninput=()=>applyFilter();
$("#jumpgrave").onclick=()=>document.getElementById("graveyard").scrollIntoView({behavior:"smooth"});
$("#jumpgoals").onclick=()=>document.getElementById("goals").scrollIntoView({behavior:"smooth"});
window.addEventListener("hashchange",()=>{ if(location.hash) goTo(location.hash.slice(1)); });
$("#handover").onclick=copyOut;
$("#recopy").onclick=copyOut;
$("#closepanel").onclick=()=>$("#panel").hidden=true;
$("#clear").onclick=()=>{ if(confirm("Discard every pending edit, comment and attachment?")){
  S={edits:{},comments:[],attachments:[]}; save(); location.reload(); } };

/* ---- hover preview ----------------------------------------------------
   Hover to know, click to go. Two ways this becomes an irritation instead of a
   help, both guarded: it must not fire as the pointer crosses a link (hence the
   delay), and it must not cover the block being read (hence the placement, which
   never overlaps the link's own line and prefers the side with room).
   Keyboard focus opens it with no delay; touch users get nothing from hover,
   which is exactly why the click-through exists as well. ---------------------*/
const PEEK=$("#peek"); let peekT=null, peekFor=null;
function peekHTML(p){
  return '<div class="peekhead"><span class="peekref">'+esc(p.ref)+'</span>'+
    '<span class="badge '+p.bcls+'">'+esc(p.badge)+'</span>'+
    '<span class="peektitle">'+esc(p.title)+'</span></div>'+
    p.body+
    '<div class="peekfoot">'+esc(p.foot)+' &middot; <span class="peekgo">click to jump</span></div>';
}
function showPeek(el){
  const p=DATA.peek[el.dataset.goto]; if(!p) return;
  peekFor=el;
  PEEK.className=p.kind==="live"?"":p.kind;
  PEEK.innerHTML=peekHTML(p);
  PEEK.hidden=false;
  PEEK.style.left="0px"; PEEK.style.top="0px";       /* measure unclamped */
  const r=el.getBoundingClientRect(), b=PEEK.getBoundingClientRect();
  const vw=innerWidth, vh=innerHeight, gap=10;
  /* vertical: below the link's line if it fits, otherwise above it — never over it */
  let top = r.bottom+gap;
  if(top+b.height > vh-8) top = (r.top-gap-b.height >= 8) ? r.top-gap-b.height
                               : Math.max(8, vh-8-b.height);
  let left = r.left;
  if(left+b.width > vw-12) left = Math.max(12, vw-12-b.width);
  PEEK.style.left=Math.round(left)+"px"; PEEK.style.top=Math.round(top)+"px";
}
function hidePeek(){ clearTimeout(peekT); peekT=null; peekFor=null; PEEK.hidden=true; }
document.addEventListener("mouseover",e=>{
  const a=e.target.closest("[data-goto]");
  if(!a||!DATA.peek[a.dataset.goto]){ if(peekFor) hidePeek(); return; }
  if(a===peekFor) return;
  clearTimeout(peekT);
  peekT=setTimeout(()=>showPeek(a),330);
});
document.addEventListener("mouseout",e=>{
  const a=e.target.closest("[data-goto]");
  if(a && a===peekFor && !a.contains(e.relatedTarget)) hidePeek();
  else if(a) clearTimeout(peekT);
});
document.addEventListener("focusin",e=>{
  const a=e.target.closest && e.target.closest("[data-goto]");
  if(a && DATA.peek[a.dataset.goto]) showPeek(a); else if(peekFor) hidePeek();
});
document.addEventListener("focusout",()=>{ if(peekFor) hidePeek(); });
document.addEventListener("keydown",e=>{ if(e.key==="Escape") hidePeek(); });
addEventListener("scroll",()=>{ if(peekFor) hidePeek(); },{passive:true});
/* the native tooltip would fight the preview; it stays only where JS is absent */
function dropTitles(root){ $$("[data-goto][title]",root).forEach(a=>{
  a.dataset.title=a.title; a.removeAttribute("title"); }); }
dropTitles(document);

/* restore anything already pending */
$$(".fp").forEach(f=>f.dataset.orig=f.innerHTML);
Object.keys(S.edits).forEach(ref=>{
  const card=document.getElementById(ref); if(!card){ delete S.edits[ref]; return; }
  $$(".field,.linkcol",card).forEach(el=>{
    const ta=$("textarea.fedit",el); if(!ta) return;
    const n=fieldName(el); if(S.edits[ref][n]) ta.value=S.edits[ref][n].now;
  });
  applyEdits(card, ref);
});
DATA.refs.forEach(renderBeside);
refresh();
/* arriving with a hash already in the URL gets the same landing treatment */
if(location.hash) setTimeout(()=>goTo(location.hash.slice(1)),60);
</script>
</body></html>
"""


# --------------------------------------------------------------------------

def main():
    print("reqview — spike. Standard library only; no network.")
    ok = True
    for name, got, want, good in selftest():
        print("  fingerprint %-20s %s  %s" % (name, got, "OK" if good else "FAIL want " + want))
        ok = ok and good
    if not ok:
        print("Fingerprint recipe does not reproduce the published vectors. Refusing to render.")
        return 1

    for name, got, want, good in parser_selftest():
        print("  parser      %-34s %s" % (name, "OK" if good else "FAIL\n     got  %s\n     want %s" % (got, want)))
        ok = ok and good
    if not ok:
        print("Heading parse does not match its fixtures. Refusing to render.")
        return 1

    if not REGISTER.exists():
        print("No register at %s" % REGISTER)
        return 1
    raw = REGISTER.read_bytes()
    register_hash = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8")

    refusals = []
    preamble, blocks, sections = parse(text, refusals)
    recs, graves, _ = build(blocks, refusals)

    goals = {}
    if GOALS.exists():
        goals = parse_goals(GOALS.read_text(encoding="utf-8"))
    if not goals:
        refuse(refusals, "docs/kerd-goals.md", "no goals or laws could be read",
               "Rule 7: a human-facing view names the behaviour, never the identifier. "
               "Without the goals file every `Traces to` target would render as a bare "
               "reference, which is a defect in the view — so it is not rendered.")
    else:
        cited = {" ".join(t.split()) for r in recs if not r["untraced"]
                 for t in r["traces_list"]}
        for c in sorted(cited):
            if c not in goals and not REF_RE.fullmatch(c):
                refuse(refusals, "`Traces to`", c,
                       "Rule 7: the target is neither a goal nor a law in "
                       "`docs/kerd-goals.md`. An unresolved reference is an error that "
                       "stops the run, not something to render unnamed.")

    if refusals:
        print()
        print("REFUSED — %d thing%s in the register could not be classified."
              % (len(refusals), "" if len(refusals) == 1 else "s"))
        print("Rule 14: ambiguity is refused, never guessed. No page was written.")
        for r in refusals:
            print()
            print("  %s" % r["where"])
            print("    text   %s" % r["what"])
            print("    why    %s" % r["why"])
        return 2

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page = render(preamble, recs, graves, CHECKS, register_hash,
                  str(REGISTER.relative_to(ROOT)), goals)
    OUTPUT.write_text(page, encoding="utf-8")

    print("  sections            %s" % ", ".join(repr(s) for s in sections))
    print("  live                %d" % len(recs))
    print("  graveyard           %d" % len(graves))
    print("  dependency links    %d" % sum(len(r["deps"]) for r in recs))
    print("  goals + laws        %d goals, %d laws"
          % (sum(1 for g in goals.values() if g["kind"] == "goal"),
             sum(1 for g in goals.values() if g["kind"] == "law")))
    print("  clickable jumps     %d" % page.count("data-goto="))
    print("  approved            %d" % sum(1 for r in recs if r["state"] == "approved"))
    print("  invalidated         %d" % sum(1 for r in recs if r["state"] == "invalidated"))
    print("  never approved      %d" % sum(1 for r in recs if r["state"] == "never"))
    print("  format checks       %d passed, 0 refusals" % len(CHECKS))
    for c in CHECKS:
        print("      ok  %s" % c)
    print("  wrote %s (%d KB)" % (OUTPUT, len(page.encode("utf-8")) // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
