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
# A bold lead label may WRAP ACROSS LINES in this register — e.g. R-0048's
# "**Reworked …, and its\ndependency dropped in the same edit.**". Matching only
# within one line silently absorbs the whole note into the preceding field, which
# put a graveyard reference into R-0048's `Depends on`. Match across the segment.
BOLD_LEAD_RE = re.compile(r"^\*\*(.+?)\*\*", re.S)
LABEL_WINDOW = 6  # lines a wrapped bold label may span
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


def parse(text):
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
    notes_about_format = []
    preamble = ""
    section_names = []

    for name, start, end in sections:
        section_names.append(name)
        body = lines[start:end]
        if name == "(preamble)":
            preamble = "\n".join(body).strip()
            continue
        low = name.lower()
        is_reqs = low == "requirements"
        is_grave = low == "graveyard"
        if not (is_reqs or is_grave):
            notes_about_format.append(
                "Level-two section `## %s` sits between the requirements heading and "
                "the graveyard. Rule 13 says nothing else sits at heading level two, "
                "and the graveyard is always last. Parsed as prose, not requirements — "
                "but a naive parser would read its `### 1 — …` headings as requirement "
                "blocks." % name)
            continue

        # split into ### blocks
        idxs = [i for i, l in enumerate(body) if HEAD3_RE.match(l)]
        for n, i in enumerate(idxs):
            j = idxs[n + 1] if n + 1 < len(idxs) else len(body)
            chunk = body[i:j]
            head = HEAD3_RE.match(chunk[0]).group(1).strip()
            parts = [p.strip() for p in head.split("—")]
            ref = parts[0] if parts else head
            dead = len(parts) > 1 and parts[1].upper() == "DEAD"
            handle = parts[2] if dead and len(parts) > 2 else (
                parts[1] if len(parts) > 1 else "")
            if not REF_RE.fullmatch(ref):
                notes_about_format.append(
                    "Heading `%s` in `## %s` is not `### R-nnnn — handle`; skipped."
                    % (head, name))
                continue
            if is_grave and not dead:
                notes_about_format.append(
                    "%s sits in the graveyard without the `— DEAD` marker rule 10 "
                    "requires." % ref)
            if is_reqs and dead:
                notes_about_format.append(
                    "%s is marked DEAD but sits in the live set." % ref)

            b = Block(ref, handle, dead or is_grave, name)
            b.raw = "\n".join(chunk).strip()

            rest = chunk[1:]
            # machine comment on the line directly under the heading
            for l in rest[:2]:
                m = MACHINE_RE.match(l.strip())
                if m:
                    b.machine = m.group(1)
                    break

            # field boundaries: a bold-lead line whose previous line is blank
            bounds = []
            for k, l in enumerate(rest):
                if not l.startswith("**"):
                    continue
                if k > 0 and rest[k - 1].strip():
                    continue
                window = "\n".join(rest[k:k + LABEL_WINDOW])
                m = BOLD_LEAD_RE.match(window)
                if m:
                    label = " ".join(m.group(1).split()).rstrip(".").strip()
                    if "\n" in m.group(1):
                        notes_about_format.append(
                            "%s has a bold field label that wraps across lines "
                            "(`%s…`). A line-oriented parser absorbs the whole "
                            "paragraph into the field above it." % (ref, label[:44]))
                    bounds.append((k, label))
            for n2, (k, label) in enumerate(bounds):
                k2 = bounds[n2 + 1][0] if n2 + 1 < len(bounds) else len(rest)
                seg = "\n".join(rest[k:k2])
                seg = BOLD_LEAD_RE.sub("", seg, count=1).lstrip()
                val = "\n".join(x for x in seg.split("\n")
                                if x.strip() != "---").strip()
                norm = label.lower().rstrip(".").strip()
                derived = False
                if norm.startswith("statement") and "(derived)" in norm:
                    norm, derived = "statement", True
                known = DEAD_LABELS if b.dead else LIVE_LABELS
                if norm in known:
                    if norm in b.fields:
                        notes_about_format.append(
                            "%s carries two `%s` fields." % (b.ref, label))
                    b.fields[norm] = val
                    if derived:
                        b.derived = True
                else:
                    b.notes.append((label, val))
            blocks.append(b)

    return preamble, blocks, notes_about_format, section_names


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

def build(blocks, notes_about_format):
    live = [b for b in blocks if not b.dead]
    dead = [b for b in blocks if b.dead]
    live_refs = {b.ref for b in live}
    all_refs = {b.ref for b in blocks}

    seen = set()
    for b in blocks:
        if b.ref in seen:
            notes_about_format.append("Duplicate reference %s." % b.ref)
        seen.add(b.ref)

    recs = []
    for b in live:
        missing = [l for l in LIVE_LABELS if l not in b.fields]
        for l in missing:
            notes_about_format.append(
                "%s has no `%s` field. Rule 1 requires all five on every live block; "
                "an absent field is written `none`, never omitted." % (b.ref, l))
        stmt = b.fields.get("statement", "")
        why = b.fields.get("why", "")
        traces = b.fields.get("traces to", "")
        depends = b.fields.get("depends on", "")
        approval = b.fields.get("approval", "")
        fp_now = fingerprint(stmt, why, traces, depends, b.derived)

        deps, dangling = [], []
        if depends.strip().lower() not in ("none", ""):
            for r in REF_RE.findall(depends):
                deps.append(r)
                if r not in live_refs:
                    dangling.append(r)
            if not deps:
                notes_about_format.append(
                    "%s `Depends on` is neither `none` nor a list of references: %r. "
                    "Rule 8 allows only those two." % (b.ref, depends[:70]))
        for r in dangling:
            notes_about_format.append(
                "%s depends on %s, which is not in the live set%s. Rule 8 makes an "
                "unresolved reference an error that stops the run."
                % (b.ref, r, " (it is in the graveyard)" if r in all_refs else ""))

        traces_list = [t.strip() for t in traces.split(",") if t.strip()]
        untraced = traces.strip().lower().startswith("not yet traced")

        a = approval.strip()
        m = APPROVED_RE.match(a.split("\n")[0].strip())
        if m:
            state = "approved" if m.group(3) == fp_now else "invalidated"
            recorded_fp, approver, approved_on = m.group(3), m.group(1), m.group(2)
        else:
            if not a.lower().startswith("none"):
                notes_about_format.append(
                    "%s `Approval` is neither `none…` nor `<name>, <date> · fp:<12 hex>`: "
                    "%r." % (b.ref, a[:70]))
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
        missing = [l for l in DEAD_LABELS if l not in b.fields]
        for l in missing:
            notes_about_format.append(
                "Graveyard %s has no `%s` field (rule 10 requires six)." % (b.ref, l))
        killed = b.fields.get("killed", "")
        if "authorised by" not in killed.lower() and "authorized by" not in killed.lower():
            notes_about_format.append(
                "Graveyard %s names no kill authoriser. Rule 10 makes it required."
                % b.ref)
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


def render(preamble, recs, graves, notes, register_hash, source_path, goals):
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

    notes_html = "".join("<li>%s</li>" % inline(n).replace("<p>", "").replace("</p>", "")
                         for n in notes) or "<li>Nothing.</li>"

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
            .replace("__NOTES__", notes_html)
            .replace("__NNOTES__", str(len(notes))))


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
    <div class="count"><b>__NNOTES__</b>format notes</div>
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

<h2>What this view found in the format</h2>
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

    if not REGISTER.exists():
        print("No register at %s" % REGISTER)
        return 1
    raw = REGISTER.read_bytes()
    register_hash = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8")

    preamble, blocks, notes, sections = parse(text)
    recs, graves, _ = build(blocks, notes)

    goals = {}
    if GOALS.exists():
        goals = parse_goals(GOALS.read_text(encoding="utf-8"))
    if not goals:
        notes.append(
            "No goals or laws could be read from `%s`, so every `Traces to` target "
            "renders as a bare identifier. A rendering built for a human must "
            "resolve a reference to its name."
            % (GOALS.relative_to(ROOT) if GOALS.exists() else "docs/kerd-goals.md"))
    else:
        cited = {" ".join(t.split()) for r in recs if not r["untraced"]
                 for t in r["traces_list"]}
        for c in sorted(cited):
            if c not in goals:
                notes.append(
                    "`Traces to` names `%s`, which is neither a goal nor a law in "
                    "`docs/kerd-goals.md`. It renders unresolved." % c)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page = render(preamble, recs, graves, notes, register_hash,
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
    print("  format notes        %d" % len(notes))
    for n in notes:
        print("      - %s" % n)
    print("  wrote %s (%d KB)" % (OUTPUT, len(page.encode("utf-8")) // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
