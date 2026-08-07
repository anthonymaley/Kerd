#!/usr/bin/env python3
"""Render one work item's journey as a human-facing HTML page.

    python3 tools/diagram/gen_journey.py <slug> [--out PATH]

Every value is derived from disk — the product doc, the entry gates, the
contract spec, the gate records and git. Nothing is hand-maintained, so the
page cannot drift from the repo the way a written summary does.

Two things it does that a status page usually does not:

**It lists what is missing.** Each rung declares the artifacts it ought to
carry. Ones that do not exist are listed as open slots rather than omitted, so
a gap is visible from across the room and can be accepted or pushed back on
(Tony, 2026-08-07: "list when empty so we can accept that or push back").

**It says what it cannot show.** A field with no source on disk is named as
such rather than estimated. An honest hole is information; a plausible number
hides one.

Shape agreed 2026-08-05 over four live iterations, amended by annotation round
one on 2026-08-07 — see docs/design/shared-memory.md.
"""

import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# The funnel, in the language of the product rather than the machine.
#
# `expects` are the artifacts a rung ought to carry. They are NOT gate
# requirements — the gates refuse on a smaller, harder set. These are what a
# reader would expect to find, and listing the missing ones is the point:
# an absent evaluation matrix should be visible, not silently omitted.
# ---------------------------------------------------------------------------

STAGES = [
    ("frame", "Idea", "the problem named, and what winning would be", [
        ("The idea, drawn current-to-ideal", "journey-{slug}-current.svg", "drawn, not described"),
    ]),
    ("viability", "Validated", "the risks sized, the killer one answered", [
        ("What we considered", "matrix", "options compared against declared criteria"),
    ]),
    ("slice", "Scoped", "the smallest slice worth shipping", []),
    ("design", "Designed", "the solution drawn and agreed", [
        ("The design", "docs/design/{slug}.md", "how it works, in detail"),
        ("Architecture — how the parts connect", "docs/design/{slug}-architecture.svg",
         "high-level blocks and lines"),
        ("The proposal, drawn", "journey-{slug}-proposal.svg", "current versus new"),
    ]),
    ("contract", "Spec'd", "each piece written down precisely enough to hand over", []),
    ("build", "Built", "each piece made, and measured against its own spec", []),
    ("goal", "Proven", "the whole thing checked against what we said winning was", []),
    ("loop", "Live", "in use, and the machine can refuse a regression", []),
]

# The requirement vocabulary the gates emit, in plain English. The set is
# closed and small. An unmapped requirement falls through as raw text, which is
# visibly ugly on purpose — that is the signal the vocabulary grew.
PLAIN = [
    (r'^docs/product/\S+ — file exists$', "The idea is written down"),
    (r'^docs/product/\S+ — front matter route.*stage', "Tagged with how it enters and where it stands"),
    (r'^docs/product/\S+ — section "Value"$', "What winning looks like, stated in units"),
    (r'^docs/product/\S+ — section "Risk ledger" \((\d+) rows[^)]*\)$',
     lambda m: f"Every risk sized and evidenced — {m.group(1)} of them"),
    (r'^docs/product/\S+ — section "Risk ledger"$', "Every risk sized and evidenced"),
    (r'^docs/product/\S+ — section "Release slice"$', "The smallest valuable slice named"),
    (r'^docs/design/\S+ — file exists$', "The solution designed"),
    (r'^docs/gates/\S+ — design GO record.*$', "Design agreed, and signed off on the record"),
    (r'^docs/plans/\S+ — contract spec$', "The build contract written"),
    (r'^docs/plans/\S+ — section "Pieces" \((\d+) items\)$',
     lambda m: f"Broken into {m.group(1)} pieces, each with its own measure"),
    (r'^docs/plans/\S+ — section "Pieces"$', "Broken into pieces, each with its own measure"),
    (r'^docs/plans/\S+ — every Step carries \*\*Verify:\*\*$',
     "Every piece carries the check that proves it"),
    (r'^docs/plans/\S+ — "(.+?)" missing a "\*\*Verify:\*\*" line$',
     lambda m: f"No check written for: {m.group(1)}"),
    (r'^docs/plans/\S+ — zero unchecked boxes.*$', "Every piece built and checked off"),
    (r'^docs/gates/\S+ — goal record with section "Done condition".*$',
     "Proven against its done condition, on the record"),
    (r'^\.github/workflows/gate\.yml — file exists$', "The machine can refuse bad work"),
]

# Risk state → glyph. ○ meets · △ meets only with a countermeasure · × cannot
# meet. Deliberately the evaluation matrix's own vocabulary, so the system
# carries one symbol set rather than two competing ones.
GLYPH = {
    "countermeasure - permanent": ("ok", "○", "handled"),
    "countermeasure - temporary": ("warn", "△", "handled for now"),
    "accepted": ("ok", "○", "accepted"),
    "accepted unknown": ("warn", "△", "watching"),
    "fatal": ("bad", "×", "blocker"),
}


# The story an item tells at its head. Canonical library with the sections:
# docs/design/talk-formats.md. A product doc declares `story: <key>` in front
# matter; proposal is the default because every item framed so far is one.
STORIES = {
    "proposal": ("Proposal",
                 "This outline is used when a proposal is being made to improve the "
                 "condition as a result of reducing problems or gaining benefits not "
                 "currently available.",
                 ["Current Situation &amp; Background", "Problems &amp; Cause",
                  "Proposal &amp; Benefits"]),
    "compare": ("Compare &amp; Contrast",
                "This outline is used when showing a situation now versus after some "
                "change.",
                ["Current Situation", "New Situation"]),
    "discrepancy": ("Correcting Discrepancy from Standard",
                    "This outline is used when the current situation differs from an "
                    "established standard and countermeasure activity is in order.",
                    ["Current Situation", "Standard &amp; Discrepancy", "Countermeasure"]),
    "roadmap": ("Develop the Roadmap",
                "This outline is used when trends have been identified and analysed "
                "and a strategic direction is being decided.",
                ["Trends &amp; Analysis", "Strategic Direction"]),
    "illumination": ("Illumination of the Unknown",
                     "This outline is used when sharing information by starting from "
                     "what the reader already knows.",
                     ["Known", "Unknown"]),
    "educate": ("Educate to the Detail",
                "This outline is used when teaching detail that needs the bigger "
                "picture first.",
                ["Simplest", "Medium", "Detail"]),
    "problem": ("Problem Solving A3",
                "This outline is used for a perceived problem, worked to its point of "
                "cause and root cause before any countermeasure.",
                ["Happy path", "As-is — the gap, measured", "Point of cause",
                 "Root cause", "Countermeasure &amp; plan"]),
}


def plain(req):
    for pat, rep in PLAIN:
        m = re.match(pat, req)
        if m:
            return rep(m) if callable(rep) else rep
    return req


# ---------------------------------------------------------------------------
# Reading what is on disk
# ---------------------------------------------------------------------------

def run(*args):
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def md_text(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    s = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'\1', s)
    s = re.sub(r'`([^`]+)`', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()


def clip(s, n):
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0].rstrip(" ,;:—-") + "…"


def sections(text):
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r'^## (.+)$', line)
        if m:
            if cur:
                out[cur] = "\n".join(buf).strip()
            cur, buf = m.group(1).strip(), []
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).strip()
    return out


def read_product(slug):
    path = ROOT / "docs" / "product" / f"{slug}.md"
    if not path.exists():
        sys.exit(f"no product doc: docs/product/{slug}.md")
    text = path.read_text()
    title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), slug)
    story = "proposal"
    if text.startswith("---"):
        for line in text.split("---", 2)[1].splitlines():
            if line.lower().startswith("story:"):
                story = line.split(":", 1)[1].strip().lower()
    return {"title": title, "sec": sections(text), "text": text, "story": story}


def pitch(value_body):
    """Kept but unused since 2026-08-07: the drawing carries the statement, so
    the panel holds no prose. Retained because a story format without a drawing
    slot (roadmap, illumination) may still want a sentence — and because
    deleting it would hide that this was a decision rather than an oversight."""
    quote = []
    for l in value_body.splitlines():
        if l.startswith(">"):
            quote.append(l[1:].strip())
        elif quote:
            break
    src = " ".join(x for x in quote if x)
    if not src:
        out = []
        for line in value_body.splitlines():
            if not line.strip():
                if out:
                    break
                continue
            if line.startswith(("#", "-", "|", ">")):
                continue
            out.append(line.strip())
        src = " ".join(out)
    return clip(md_text(src), 300)


def pains(text):
    """The numbered problems, from the gap-list headings — already written, and
    already one line each."""
    return [md_text(m.group(1)) for m in re.finditer(r'^### Gap \d+ — (.+)$', text, re.M)]


def targets(value_body):
    out = []
    for line in value_body.splitlines():
        m = re.match(r'^- \*\*(.+?)\*\*\s*(.*)$', line.strip())
        if not m:
            continue
        claim = m.group(1).rstrip('.')
        if "→" not in claim:
            continue
        label, _, arrow = claim.partition(":")
        out.append({"label": md_text(label), "move": md_text(arrow)})
    return out


def risks(body):
    out = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|- :"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 8 or cells[0].lower() == "risk":
            continue
        cls, glyph, word = GLYPH.get(cells[5].lower(), ("bad", "×", "unhandled"))
        out.append({
            "title": clip(md_text(cells[0]), 110),
            "killer": cells[1].lower().startswith("y"),
            "impact": clip(md_text(cells[2]), 130),
            "likelihood": clip(md_text(cells[3]), 110),
            "counter": clip(md_text(cells[6]), 170) or "none — which is why it is open",
            "cls": cls, "glyph": glyph, "word": word,
        })
    out.sort(key=lambda r: (not r["killer"], {"bad": 0, "warn": 1, "ok": 2}[r["cls"]]))
    return out


def board(slug):
    raw = run("python3", "tools/diagram/progress.py", "--json")
    if not raw:
        sys.exit("progress.py --json produced nothing")
    for b in json.loads(raw)["board"]:
        if b["slug"] == slug:
            return b
    sys.exit(f"{slug} is not on the board")


def rung_dates(slug):
    out = {}
    for p in sorted((ROOT / "docs" / "gates").glob(f"*-{slug}-*.md")):
        m = re.match(r'^(\d{4}-\d{2}-\d{2})-' + re.escape(slug) + r'-(\w+)\.md$', p.name)
        if m:
            out[m.group(2)] = m.group(1)
    return out


def spec_pieces(slug):
    """The contract's own steps, each a measurable unit. This is the level Tony
    asked for (2026-08-07): "each step needs a measurable spec to be successful
    and to produce the tests we need to check"."""
    specs = sorted((ROOT / "docs" / "plans").glob(f"*-{slug}-spec.md"))
    if not specs:
        return []
    body = sections(specs[-1].read_text()).get("Pieces", "")
    out = []
    for line in body.splitlines():
        m = re.match(r'^- \[([ xX])\]\s*(.+)$', line.strip())
        if m:
            name = re.sub(r'^Step \d+\s*—\s*', '', md_text(m.group(2)))
            out.append({"done": m.group(1).lower() == "x", "name": clip(name, 120)})
    return out


def artefacts(have):
    out, seen = [], set()
    for item in have:
        m = re.match(r'^(\S+\.(?:md|py|yml|svg|excalidraw))\b', item)
        if not m:
            continue
        f = m.group(1)
        if "*" in f or f in seen or not (ROOT / f).exists():
            continue
        seen.add(f)
        out.append({"file": f, "name": Path(f).name})
    return out


def drawing(slug, kind):
    """Diagrams are made while pairing and committed like any other artifact —
    the excalidraw pipeline that already renders every flow in this repo. The
    page embeds the SVG if it is there and lists the slot if it is not; it never
    invents a picture."""
    p = ROOT / "docs" / "plans" / f"journey-{slug}-{kind}.svg"
    if not p.exists():
        return None
    return re.sub(r'<\?xml[^>]*\?>', '', p.read_text()).strip()


def stage_steps():
    """The numbered steps inside each stage. Defined once for the method, not
    per work item — the gates check a stage's outputs, this defines its work.
    A stage with no rungs written yet renders as an open slot, which is the
    honest state for seven of the eight (see docs/design/funnel-steps.md)."""
    path = ROOT / "docs" / "design" / "funnel-steps.md"
    if not path.exists():
        return {}
    out = {}
    for name, body in sections(path.read_text()).items():
        steps = []
        for line in body.splitlines():
            m = re.match(r'^\d+\.\s*`([^`]+)`\s*—\s*(.+)$', line.strip())
            if m:
                steps.append({"status": m.group(1).strip(), "text": md_text(m.group(2))})
        if steps:
            out[name] = steps
    return out


PILL = {"done": "ok", "open": "open", "in progress": "now", "not started": "todo"}


def expected_present(slug, spec):
    if spec is None:
        return False
    if spec == "matrix":
        return "Evaluation matrix" in (ROOT / "docs" / "product" / f"{slug}.md").read_text()
    path = spec.format(slug=slug)
    if not path.startswith("docs/"):
        path = f"docs/plans/{path}"
    return (ROOT / path).exists()


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def E(s):
    return html.escape(str(s), quote=False)


def render(slug):
    doc = read_product(slug)
    b = board(slug)
    dates = rung_dates(slug)
    value = doc["sec"].get("Value", "")
    tg = targets(value)
    rk = risks(doc["sec"].get("Risk ledger", ""))
    pieces = spec_pieces(slug)
    rungs = stage_steps()
    all_pains = pains(doc["text"])
    sha = run("git", "rev-parse", "--short", "HEAD")
    when = run("git", "log", "-1", "--format=%cd", "--date=format:%-d %B %Y, %H:%M")
    by_rung = {r["rung"]: r for r in b["rungs"]}
    labels = {s: l for s, l, _, _ in STAGES}
    reached = [s for s, _, _, _ in STAGES if by_rung.get(s, {}).get("state") == "built"]
    now = next((s for s, _, _, _ in STAGES if by_rung.get(s, {}).get("state") == "in-flight"), None)

    P = []
    A = P.append
    A('<!doctype html><html lang="en"><head><meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A(f'<title>{E(doc["title"])} — journey</title>{CSS}</head><body><div class="wrap">')

    A(f'<header><div class="eyebrow">Kerd · journey</div><h1>{E(doc["title"])}</h1>'
      f'<div class="derived">Drawn from the repo at <code>{E(sha)}</code> · {E(when)} · '
      f'read-only — this page changes nothing</div></header>')

    # ---- the story head. Which story is declared, not assumed ----------
    sname, outline, headings = STORIES.get(doc["story"], STORIES["proposal"])
    A(f'<section class="story"><h2>{sname}</h2><div class="storybox">')
    A(f'<p class="outline">{outline}</p><div class="a3">')
    # Pains spread across the middle panels; the last panel carries the pitch.
    per = max(1, len(all_pains) // max(1, len(headings)))
    for i, heading in enumerate(headings):
        if i:
            A('<div class="arrow">\u2192</div>')
        kind = ["current", "problem", "proposal", "d", "e"][i] if i < 5 else f"p{i}"
        A(f'<div class="panel"><h3>{heading}</h3>')
        d = drawing(slug, kind)
        A(f'<div class="draw">{d}</div>' if d else
          '<div class="slot blocking"><b>Not drawn — so this is not agreed.</b> '
          'The drawing is what forces alignment: if we do not agree on the picture '
          'we will not agree on the solution, and every agreement below this point '
          'is softer than it looks. Drawn while pairing, committed like any other '
          'diagram.</div>')
        chunk = all_pains[i * per:(i + 1) * per] if i < len(headings) - 1 else []
        if chunk:
            A('<ul class="pl">')
            for l in chunk[:3]:
                A(f'<li>{E(clip(l, 130))}</li>')
            A('</ul>')
        if i == len(headings) - 1:
            # No prose here. The drawing carries the statement — Tony 2026-08-07,
            # looking at a 300-char clip of the Value section trailing off
            # mid-sentence: "this can go i think, drawing replaces?". The target
            # numbers stay: they are the checkable version of the same claim.
            if tg:
                A('<div class="targets">')
                for t in tg[:3]:
                    A(f'<div class="target"><div class="num">{E(t["move"])}</div>'
                      f'<div class="cap">{E(clip(t["label"], 52))}</div></div>')
                A('</div>')
        A('</div>')
    A('</div></div></section>')

    # ---- risks ------------------------------------------------------------
    if rk:
        A('<section class="risks"><h2>Risks</h2><table class="rt"><thead><tr>'
          '<th></th><th>Risk</th><th>Impact</th><th>Likelihood</th>'
          '<th>Countermeasure</th></tr></thead><tbody>')
        for r in rk:
            k = ' <span class="killer">killer</span>' if r["killer"] else ""
            A(f'<tr class="{r["cls"]}"><td class="g"><span class="glyph">{r["glyph"]}</span>'
              f'<span class="gw">{E(r["word"])}</span></td>'
              f'<td class="rt-title">{E(r["title"])}{k}</td>'
              f'<td>{E(r["impact"])}</td><td>{E(r["likelihood"])}</td>'
              f'<td>{E(r["counter"])}</td></tr>')
        A('</tbody></table><div class="legend">○ handled · △ handled only by a '
          'countermeasure, or watched · × no countermeasure — a blocker</div></section>')

    # ---- tracker ----------------------------------------------------------
    A('<div class="funnel-label">The funnel</div><div class="minimap">')
    for s, label, _, _ in STAGES:
        st = by_rung.get(s, {}).get("state", "missing")
        cls = "done reached" if st == "built" else ("now reached" if st == "in-flight" else "")
        A(f'<div class="mm {cls}"><div class="dot"></div><div class="l">{E(label)}</div></div>')
    A('</div>')
    pos = f'At <b>{E(labels.get(now, now))}</b>' if now else "<b>Every rung reached</b>"
    A(f'<div class="mapnote">{pos} · {len(reached)} of {len(STAGES)} stages behind it · '
      f'entered the funnel at <b>{E(labels.get(b["enters_at"], b["enters_at"]))}</b></div>')

    # ---- the funnel is the spine -----------------------------------------
    # Current stage open, the rest folded behind one bar — the reader is here
    # to see where we are, not to scroll eight cards to find it.
    def stage_html(s, label, blurb, expects):
        r = by_rung.get(s, {})
        st = r.get("state", "missing")
        cls = {"built": "done", "in-flight": "now"}.get(st, "todo")
        word = {"built": "done", "in-flight": "in flight"}.get(st, "not started")
        H = [f'<div class="stage {cls}"><span class="lamp"></span><div class="head">'
             f'<h2>{E(label)}</h2><span class="status {cls}">{E(word)}</span>'
             + (f'<span class="when">{E(dates[s])}</span>' if s in dates else "") +
             f'</div><div class="card"><div class="blurb">{E(blurb)}</div>']

        # Every stage carries its own drawing. Tony 2026-08-07: "a diagram or
        # drawing can secure alignment before the next stage" — so an undrawn
        # stage is an unagreed stage, not merely an undocumented one.
        sd = drawing(slug, s)
        if sd:
            H.append(f'<div class="stagedraw">{sd}</div>')
        elif cls != "todo":
            H.append('<div class="slot blocking stageslot"><b>Not drawn — so this '
                     'stage is not agreed.</b> A drawing here is what secures '
                     'alignment before the next stage opens.</div>')

        # The steps — the work inside the stage.
        steps = rungs.get(label, [])
        if steps:
            H.append('<ul class="rungs">')
            for i, st_ in enumerate(steps, 1):
                pill = PILL.get(st_["status"], "todo")
                H.append(f'<li><span class="rn">Step {i}</span>'
                         f'<span class="rt">{E(st_["text"])}</span>'
                         f'<span class="pill {pill}">{E(st_["status"])}</span></li>')
            H.append('</ul>')
        else:
            H.append('<div class="norungs">Rungs not defined for this stage yet — '
                     'the gates check what it produces, not what it involves. '
                     'Defining them is queued.</div>')

        for it in r.get("need_items", []):
            H.append(f'<div class="blocker">× {E(plain(it))} — still needed</div>')
        for name, spec, note in expects:
            if not expected_present(slug, spec):
                H.append(f'<div class="openslot">· {E(name)} — {E(note)} '
                         f'<span class="nt">not there</span></div>')

        if s == "build" and pieces:
            n = sum(1 for x in pieces if x["done"])
            H.append(f'<div class="made"><h4>The pieces — {n} of {len(pieces)}, each '
                     f'measured against its own spec</h4><ul class="pieces">')
            for x in pieces:
                g, gl = ("ok", "○") if x["done"] else ("bad", "×")
                H.append(f'<li><span class="mark {g}">{gl}</span>'
                         f'<span class="what">{E(x["name"])}</span></li>')
            H.append('</ul></div>')

        made = artefacts(r.get("have_items", []))
        if made:
            H.append('<div class="made"><h4>What we created</h4><ul>')
            for a in made:
                H.append(f'<li><span class="what">{E(a["name"])}</span>'
                         f'<a class="open" href="../../{E(a["file"])}">open</a></li>')
            H.append('</ul></div>')
        H.append('</div></div>')
        return "".join(H)

    focus = now or (STAGES[-1][0] if not now else None)
    A('<div class="ladder">')
    A(stage_html(*next(x for x in STAGES if x[0] == focus)))
    A('</div>')
    others = [x for x in STAGES if x[0] != focus]
    if others:
        A('<details class="rest"><summary>All other stages</summary>'
          '<div class="ladder">')
        for x in others:
            A(stage_html(*x))
        A('</div></details>')

    A('<footer><h3>What this page cannot show yet, and why</h3><ul>')
    A('<li><b>How long each rung took.</b> Gate records are dated to the day and most '
      'journeys land two rungs on one date, so day resolution reads zero. Per-task '
      'start and end stamps began on 2026-08-06; too few yet for a comparison that '
      'would not mislead.</li>')
    A('<li><b>What it measured once in use.</b> Nothing on disk records post-ship '
      'measurement, so there is nothing to read.</li>')
    A('</ul><p class="foot">Everything else above is read from the repo at the commit '
      'named in the header. Nothing here is hand-maintained, so it cannot quietly go '
      'stale — but it also cannot show what was never written down, which is why the '
      'open slots are listed rather than hidden.</p></footer></div></body></html>')
    return "\n".join(P)


CSS = """<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--paper:#FBFAF7;--card:#FFF;--ink:#22312F;--ink-soft:#5C6B67;--hairline:#E4E7E4;
--moss:#3E7C4F;--moss-chip:#E3EFE6;--amber:#C98A2E;--amber-chip:#FBF0DC;
--red:#C6453F;--red-chip:#F8E4E2;--slate:#9AA5A1}
body{background:var(--paper);color:var(--ink);
font:16px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
padding:44px 24px 90px}
.wrap{max-width:1040px;margin:0 auto}
header{margin-bottom:34px}
.eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;
color:var(--ink-soft);font-weight:600;margin-bottom:10px}
h1{font-size:33px;line-height:1.18;letter-spacing:-.015em;max-width:22ch}
.derived{margin-top:12px;font-size:13px;color:var(--ink-soft)}
code{font:13px ui-monospace,SFMono-Regular,Menlo,monospace;background:#F1F0EC;
padding:1px 6px;border-radius:5px}
h2{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft);
font-weight:700;margin-bottom:13px}
section{margin-bottom:36px}

.story{margin-bottom:34px}
.storybox{background:var(--card);border:1px solid var(--hairline);border-radius:16px;
padding:22px 26px}
.outline{font-style:italic;font-size:15px;line-height:1.5;color:var(--ink-soft);
max-width:78ch;margin-bottom:20px}
.a3{display:flex;gap:10px;align-items:stretch;margin-bottom:0}
.a3 .panel{flex:1;min-width:0}
.arrow{align-self:center;color:var(--slate);font-size:20px;flex:none}
.panel h3{font-size:12px;font-weight:700;letter-spacing:.03em;color:var(--ink);
margin-bottom:9px}
.pl{margin-top:11px;padding-left:16px;display:grid;gap:6px}
.pl li{font-size:12.5px;line-height:1.4;color:var(--ink-soft)}
.pl li::marker{color:var(--red);font-weight:700}
.funnel-label{font-size:11px;letter-spacing:.14em;text-transform:uppercase;
color:var(--ink-soft);font-weight:700;margin-bottom:6px}
.rungs{list-style:none;display:grid;gap:0}
.rungs li{display:flex;align-items:center;gap:12px;padding:11px 0;
border-bottom:1px solid var(--hairline);flex-wrap:wrap}
.rungs li:last-child{border-bottom:none}
.rn{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
color:var(--slate);flex:none;width:56px}
.rt{flex:1;min-width:220px;font-size:14px;line-height:1.45}
.pill{font-size:10px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
padding:4px 11px;border-radius:999px;flex:none;margin-left:auto}
.pill.ok{background:var(--moss-chip);color:var(--moss)}
.pill.open{background:#DFF1EC;color:#1F6F62}
.pill.now{background:var(--amber-chip);color:#9A5A17}
.pill.todo{background:#EDEDEA;color:#77817D}
.norungs{font-size:13px;color:var(--slate);line-height:1.5;
border:1.5px dashed #D3D8D5;border-radius:10px;padding:13px 15px;background:#FCFCFB}
.blocker{margin-top:9px;font-size:13px;color:var(--red);line-height:1.45}
.openslot{margin-top:8px;font-size:13px;color:var(--slate);line-height:1.45}
.openslot .nt{font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.05em}
details.rest{margin-top:16px}
details.rest>summary{cursor:pointer;list-style:none;background:var(--card);
border:1px solid var(--hairline);border-radius:12px;padding:14px 20px;
font-size:11.5px;font-weight:700;letter-spacing:.11em;text-transform:uppercase;
color:var(--ink-soft);text-align:center}
details.rest>summary::-webkit-details-marker{display:none}
details.rest>summary:hover{border-color:var(--ink-soft)}
details.rest[open]>summary{margin-bottom:16px}
.panel{background:var(--card);border:1px solid var(--hairline);border-radius:16px;
padding:20px 24px}
.panel.proposal{border-color:#CFDDD3;background:linear-gradient(180deg,#FCFEFC,#FFF)}
.draw svg{width:100%;height:auto;display:block}
.slot{border:1.5px dashed #D3D8D5;border-radius:12px;padding:18px;font-size:13px;
color:var(--slate);line-height:1.5;background:#FCFCFB}
.slot.blocking{border-color:#E3A9A5;background:#FEF7F6;color:#8C5450}
.slot.blocking b{color:var(--red);display:block;margin-bottom:5px}
.stageslot{margin-bottom:13px;font-size:12.5px;padding:13px 16px}
.stagedraw{margin-bottom:14px;border:1px solid var(--hairline);border-radius:12px;
padding:14px;background:#FCFCFB}
.stagedraw svg{width:100%;height:auto;display:block}
.pains{margin-top:14px;padding-left:18px;display:grid;gap:7px}
.pains li{font-size:13.5px;line-height:1.45}
.pains li::marker{color:var(--red);font-weight:700}
.more{margin-top:9px;font-size:12.5px;color:var(--slate)}
.pitch{margin-top:14px;font-size:15px;line-height:1.5;max-width:52ch}
.targets{display:grid;gap:11px;margin-top:14px;padding-top:13px;
border-top:1px solid var(--hairline)}
.targets::before{content:"How we will know it worked";font-size:10px;font-weight:700;
letter-spacing:.09em;text-transform:uppercase;color:var(--slate)}
.target{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.target .num{font-size:15px;font-weight:700;color:var(--moss);
font-variant-numeric:tabular-nums;letter-spacing:-.01em;flex:none}
.target .cap{font-size:12.5px;color:var(--ink-soft);line-height:1.35}

.rt{width:100%;border-collapse:collapse;background:var(--card);
border:1px solid var(--hairline);border-radius:14px;overflow:hidden;font-size:13.5px}
.rt th{text-align:left;font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;
color:var(--ink-soft);padding:11px 14px;border-bottom:1px solid var(--hairline);
font-weight:700;background:#FAFAF8}
.rt td{padding:13px 14px;border-bottom:1px solid var(--hairline);vertical-align:top;
line-height:1.45;color:var(--ink-soft)}
.rt tr:last-child td{border-bottom:none}
.rt-title{color:var(--ink);font-weight:600;max-width:26ch}
.rt td.g{width:80px;white-space:nowrap}
.glyph{font-size:17px;font-weight:700;margin-right:5px}
.gw{font-size:10.5px;text-transform:uppercase;letter-spacing:.05em;font-weight:700}
tr.ok .glyph,tr.ok .gw{color:var(--moss)}
tr.warn .glyph,tr.warn .gw{color:#9A5A17}
tr.bad .glyph,tr.bad .gw{color:var(--red)}
.killer{font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
color:var(--red);background:var(--red-chip);padding:2px 7px;border-radius:999px;
white-space:nowrap}
.legend{margin-top:10px;font-size:12.5px;color:var(--slate)}

.minimap{display:flex;margin:34px 0 8px}
.mm{flex:1;text-align:center;position:relative}
.mm::before{content:"";position:absolute;top:7px;left:0;right:0;height:2px;background:var(--hairline)}
.mm:first-child::before{left:50%}
.mm:last-child::before{right:50%}
.mm.reached::before{background:var(--moss)}
.mm .dot{width:16px;height:16px;border-radius:50%;background:#FFF;
border:2px solid var(--hairline);margin:0 auto 7px;position:relative;z-index:1}
.mm.done .dot{background:var(--moss);border-color:var(--moss)}
.mm.now .dot{background:var(--amber);border-color:var(--amber)}
.mm .l{font-size:11px;color:var(--ink-soft);font-weight:600}
.mapnote{font-size:13.5px;color:var(--ink-soft);margin-bottom:30px}

.ladder{display:grid;gap:14px}
.stage{position:relative;padding-left:34px}
.lamp{position:absolute;left:0;top:6px;width:14px;height:14px;border-radius:50%;
background:#FFF;border:2px solid var(--hairline)}
.stage.done .lamp{background:var(--moss);border-color:var(--moss)}
.stage.now .lamp{background:var(--amber);border-color:var(--amber)}
.head{display:flex;gap:11px;align-items:center;flex-wrap:wrap}
.head h2{font-size:17px;letter-spacing:-.01em;text-transform:none;color:var(--ink);margin-bottom:0}
.status{font-size:11px;font-weight:700;padding:3px 10px;border-radius:999px;letter-spacing:.04em}
.status.done{background:var(--moss-chip);color:var(--moss)}
.status.now{background:var(--amber-chip);color:#9A5A17}
.status.todo{background:#F1F0EC;color:var(--slate)}
.when{font-size:12px;color:var(--ink-soft);font-variant-numeric:tabular-nums}
.stage .card{margin-top:11px;background:var(--card);border:1px solid var(--hairline);
border-radius:14px;padding:16px 20px}
.stage.todo .card{background:#FCFCFB;border-style:dashed}
.blurb{font-size:13px;color:var(--slate);margin-bottom:10px}
.steps,.pieces{list-style:none}
.steps li,.pieces li{display:flex;align-items:baseline;gap:10px;padding:6px 0;
border-bottom:1px solid var(--hairline);flex-wrap:wrap}
.steps li:last-child,.pieces li:last-child{border-bottom:none}
.mark{font-weight:700;width:15px;flex:none;text-align:center}
.mark.ok{color:var(--moss)}
.mark.bad{color:var(--red)}
.mark.open{color:var(--slate)}
.s-name{font-weight:600}
.s-name.todo,.s-name.open{font-weight:500;color:var(--ink-soft)}
.s-note{font-size:13px;color:var(--slate)}
.s-fact{margin-left:auto;font-size:11.5px;font-weight:600;color:var(--slate);white-space:nowrap}
.made{margin-top:12px;padding-top:11px;border-top:1px solid var(--hairline)}
.made h4{font-size:10.5px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
color:var(--ink-soft);margin-bottom:5px}
.made ul{list-style:none}
.made li{display:flex;gap:10px;align-items:baseline;padding:5px 0;
border-bottom:1px dashed var(--hairline)}
.made li:last-child{border-bottom:none}
.what{font-weight:600;font-size:14px}
.pieces .what{font-weight:500;font-size:13.5px;color:var(--ink-soft)}
a.open{font-size:11.5px;font-weight:600;color:var(--ink);text-decoration:none;
border:1px solid var(--hairline);border-radius:999px;padding:2px 10px;
white-space:nowrap;margin-left:auto}
a.open:hover{border-color:var(--ink-soft)}
a.open::after{content:" ↗";color:var(--ink-soft)}

footer{margin-top:50px;padding-top:22px;border-top:1px solid var(--hairline)}
footer h3{font-size:12px;letter-spacing:.12em;text-transform:uppercase;
color:var(--ink-soft);margin-bottom:11px}
footer ul{list-style:none;display:grid;gap:7px;max-width:80ch}
footer li{font-size:13.5px;color:var(--ink-soft);line-height:1.5;padding-left:15px;position:relative}
footer li::before{content:"—";position:absolute;left:0;color:var(--slate)}
footer li b{color:var(--ink)}
.foot{margin-top:15px;font-size:13px;color:var(--ink-soft);max-width:74ch;line-height:1.5}

@media (max-width:900px){.a3{flex-direction:column}.arrow{transform:rotate(90deg)}}
@media (max-width:700px){h1{font-size:26px}.mm .l{font-size:9px}.stage{padding-left:26px}
.rt,.rt tbody,.rt tr,.rt td{display:block}.rt thead{display:none}
.rt td{border-bottom:none;padding:4px 14px}
.rt tr{border-bottom:1px solid var(--hairline);padding:10px 0}}
</style>"""


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    slug = argv[1]
    out = ROOT / "docs" / "plans" / f"journey-{slug}.html"
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
    out.write_text(render(slug))
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv)
