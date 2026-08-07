#!/usr/bin/env python3
"""Render one work item's journey as a human-facing HTML page.

    python3 tools/diagram/gen_journey.py <slug> [--out PATH]

Every value on the page is derived from disk — the product doc, the entry
gates, the gate records and git. Nothing is hand-maintained, so the page
cannot drift from the repo the way a written summary does.

Where a field has no source on disk the page SAYS SO rather than estimating.
That is deliberate: an honest hole is information (it shows what capture is
missing), and a plausible number is not.

The shape is the one agreed on 2026-08-05 over four live iterations
(docs/plans/2026-08-05-journey-view-mock.html): the idea as the title, the
story at the top, the ladder below, what we created per rung.
"""

import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# The ladder, in the language of the product rather than the machine.
# ---------------------------------------------------------------------------

STAGES = [
    ("frame", "Idea", "the problem named, and what winning would be"),
    ("viability", "Validated", "the risks sized, the killer one answered"),
    ("slice", "Scoped", "the smallest slice worth shipping"),
    ("design", "Designed", "the solution drawn and agreed"),
    ("contract", "Spec'd", "the build written down precisely enough to hand over"),
    ("build", "Built", "each piece made and proved"),
    ("goal", "Proven", "the whole thing checked against what we said winning was"),
    ("loop", "Live", "in use, and the machine can refuse a regression"),
]

# The full requirement vocabulary the gates emit, in plain English. Collected
# by sweeping every rung of every slug — the set is closed and small, so a
# lookup is honest here rather than a guess. An unmapped requirement falls
# through to its raw text, which is visibly ugly on purpose: it is the signal
# that the vocabulary grew and this table did not.
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
     lambda m: f"The build broken into {m.group(1)} pieces"),
    (r'^docs/plans/\S+ — section "Pieces"$', "The build broken into pieces"),
    (r'^docs/plans/\S+ — every Step carries \*\*Verify:\*\*$',
     "Every piece carries a way to prove it worked"),
    (r'^docs/plans/\S+ — "(.+?)" missing a "\*\*Verify:\*\*" line$',
     lambda m: f"No way to prove it worked: {m.group(1)}"),
    (r'^docs/plans/\S+ — zero unchecked boxes.*$', "Every piece built and checked off"),
    (r'^docs/gates/\S+ — goal record with section "Done condition".*$',
     "Proven against its done condition, on the record"),
    (r'^\.github/workflows/gate\.yml — file exists$', "The machine can refuse bad work"),
]

# Risk state → traffic light. The five states are the closed set the gates
# enforce; "no countermeasure" is not among them because a risk without one is
# a blocker by standing decision, which is what red means here.
LIGHTS = {
    "countermeasure - permanent": ("green", "handled"),
    "countermeasure - temporary": ("amber", "handled for now"),
    "accepted": ("green", "accepted"),
    "accepted unknown": ("amber", "watching"),
    "fatal": ("red", "blocker"),
}


def plain(req):
    """Machine requirement → product language."""
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
    """Strip inline markdown. The product doc is written for a reader who sees
    the source; this page is for one who does not, so bold stars and backticks
    are noise rather than emphasis."""
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    s = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'\1', s)
    s = re.sub(r'`([^`]+)`', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    return re.sub(r'\s+', ' ', s).strip()


def clip(s, n):
    """Truncate on a word boundary — a cut mid-word reads as corruption."""
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0].rstrip(" ,;:—-") + "…"


def sections(text):
    """Split markdown into {heading: body} for level-2 headings."""
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
    fm = {}
    if text.startswith("---"):
        head = text.split("---", 2)[1]
        for line in head.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return {"path": path, "title": title, "front": fm, "sec": sections(text), "text": text}


def why(value_body):
    """The requirement in the words it was given in — the quoted block if there
    is one, else the opening paragraph. This is the field whose absence cost an
    hour on 2026-08-07: the record held the mechanism and dropped the purpose."""
    quote = [l[1:].strip() for l in value_body.splitlines() if l.startswith(">")]
    if quote:
        # keep only the first quoted block
        out = []
        for l in quote:
            if not l and out:
                break
            if l:
                out.append(l)
        return md_text(" ".join(out))
    para = []
    for line in value_body.splitlines():
        if not line.strip():
            if para:
                break
            continue
        if line.startswith(("#", "-", "|")):
            continue
        para.append(line.strip())
    return md_text(" ".join(para))


def targets(value_body):
    """`- **name: X → Y.** note` lines under "Value, in units"."""
    out = []
    for line in value_body.splitlines():
        m = re.match(r'^- \*\*(.+?)\*\*\s*(.*)$', line.strip())
        if not m:
            continue
        claim, note = m.group(1).rstrip('.'), m.group(2)
        if "→" not in claim and "->" not in claim:
            continue
        label, _, arrow = claim.partition(":")
        out.append({"label": md_text(label), "move": md_text(arrow), "note": md_text(note)})
    return out


def risks(body):
    """The eight-column ledger. Non-table lines are skipped rather than parsed —
    the gates' own parser treats every line as a row, which is a known trap."""
    out = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|- :"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 8 or cells[0].lower() == "risk":
            continue
        state = cells[5].lower()
        colour, word = LIGHTS.get(state, ("red", "unhandled"))
        out.append({
            "risk": md_text(cells[0]), "killer": cells[1].lower().startswith("y"),
            "impact": cells[2], "likelihood": cells[3],
            "state": cells[5], "counter": md_text(cells[6]) or "— none —",
            "trigger": md_text(cells[7]), "colour": colour, "word": word,
        })
    out.sort(key=lambda r: (not r["killer"], r["colour"] != "red"))
    return out


def ruled_out(body):
    """Each entry opens `**What**` and gives its reason after an em-dash. The
    lead-in may carry a parenthetical before the dash, so the split is on the
    first em-dash rather than on the bold run ending."""
    out = []
    for para in body.split("\n\n"):
        para = para.strip().replace("\n", " ")
        m = re.match(r'^\*\*(.+?)\*\*(.*)$', para)
        if not m:
            continue
        what, rest = m.group(1), m.group(2)
        why_ = rest.split("—", 1)[1] if "—" in rest else rest
        out.append({"what": md_text(what), "why": clip(md_text(why_), 240)})
    return out


def board(slug):
    raw = run("python3", "tools/diagram/progress.py", "--json")
    if not raw:
        sys.exit("progress.py --json produced nothing")
    data = json.loads(raw)
    for b in data["board"]:
        if b["slug"] == slug:
            return b
    sys.exit(f"{slug} is not on the board")


def rung_dates(slug):
    """Gate records are dated in their filename. Day granularity is all they
    carry — 6 of 7 completed journeys land design and goal on one date, so
    this cannot support a duration comparison. Named, not hidden."""
    out = {}
    for p in sorted((ROOT / "docs" / "gates").glob(f"*-{slug}-*.md")):
        m = re.match(r'^(\d{4}-\d{2}-\d{2})-' + re.escape(slug) + r'-(\w+)\.md$', p.name)
        if m:
            out[m.group(2)] = m.group(1)
    return out


def artefacts(slug, rung, have):
    """What we created at this rung — the real files, with a link."""
    out, seen = [], set()
    for item in have:
        m = re.match(r'^(\S+\.(?:md|py|yml|excalidraw))\b', item)
        if not m:
            continue
        f = m.group(1)
        if "*" in f or f in seen:
            continue
        seen.add(f)
        if (ROOT / f).exists():
            out.append({"file": f, "name": Path(f).name})
    return out


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def E(s):
    # quote=False: these are text nodes, and escaping apostrophes turns
    # "Spec'd" into "Spec&#x27;d" on the page. The only attribute use is a
    # repo-relative path from a disk glob, which cannot carry a quote.
    return html.escape(str(s), quote=False)


def render(slug):
    doc = read_product(slug)
    b = board(slug)
    dates = rung_dates(slug)
    value = doc["sec"].get("Value", "")
    the_why = why(value)
    tg = targets(value)
    rk = risks(doc["sec"].get("Risk ledger", ""))
    ro = ruled_out(doc["sec"].get("What we ruled out", ""))
    sha = run("git", "rev-parse", "--short", "HEAD")
    when = run("git", "log", "-1", "--format=%cd", "--date=format:%-d %B %Y, %H:%M")

    by_rung = {r["rung"]: r for r in b["rungs"]}
    reached = [s for s, _, _ in STAGES if by_rung.get(s, {}).get("state") == "built"]
    now = next((s for s, _, _ in STAGES if by_rung.get(s, {}).get("state") == "in-flight"), None)

    P = []
    A = P.append

    A(f'<!doctype html><html lang="en"><head><meta charset="utf-8">')
    A(f'<meta name="viewport" content="width=device-width, initial-scale=1">')
    A(f'<title>{E(doc["title"])} — journey</title>{CSS}</head><body><div class="wrap">')

    # ---- header -----------------------------------------------------------
    A('<header><div class="eyebrow">Kerd · journey</div>')
    A(f'<h1>{E(doc["title"])}</h1>')
    A(f'<div class="derived">Drawn from the repo at <code>{E(sha)}</code> · '
      f'{E(when)} · read-only — this page changes nothing</div></header>')

    # ---- why (gap 11: the purpose, next to the thing, permanently) --------
    if the_why:
        A('<section class="whybox"><h2>Why this exists</h2>')
        A(f'<blockquote>{E(the_why)}</blockquote>')
        A('<div class="src">Straight from the frame — this is the requirement in '
          'the words it was given in, not a retelling.</div></section>')

    # ---- what winning looks like -----------------------------------------
    if tg:
        A('<section class="results"><h2>What winning looks like</h2><div class="grid">')
        for t in tg:
            A(f'<div class="res"><div class="num">{E(t["move"])}</div>'
              f'<div class="cap">{E(t["label"])}</div></div>')
        A('</div></section>')

    # ---- risks, as lights -------------------------------------------------
    if rk:
        A('<section class="risks"><h2>Risks</h2><div class="rl">')
        for r in rk:
            k = ' <span class="killer">killer</span>' if r["killer"] else ""
            A(f'<div class="risk {r["colour"]}"><div class="rhead">'
              f'<span class="lightword">{E(r["word"])}</span>{k}</div>'
              f'<div class="rtext">{E(r["risk"])}</div>'
              f'<div class="rcm"><b>What we do about it:</b> {E(r["counter"])}</div>'
              f'<div class="rtr"><b>Revisit when:</b> {E(r["trigger"])}</div></div>')
        A('</div></section>')

    # ---- minimap ----------------------------------------------------------
    A('<div class="minimap">')
    for s, label, _ in STAGES:
        st = by_rung.get(s, {}).get("state", "missing")
        cls = "done reached" if st == "built" else ("now reached" if st == "in-flight" else "")
        A(f'<div class="mm {cls}"><div class="dot"></div><div class="l">{E(label)}</div></div>')
    A('</div>')
    labels = {s: label for s, label, _ in STAGES}
    pos = f'At <b>{E(labels.get(now, now))}</b>' if now else "Every rung reached"
    A(f'<div class="mapnote">{pos} · {len(reached)} of {len(STAGES)} rungs behind it · '
      f'entered the ladder at <b>{E(labels.get(b["enters_at"], b["enters_at"]))}</b></div>')

    # ---- the ladder -------------------------------------------------------
    A('<div class="ladder">')
    seen_have = set()
    for s, label, blurb in STAGES:
        r = by_rung.get(s, {})
        st = r.get("state", "missing")
        cls = {"built": "done", "in-flight": "now"}.get(st, "todo")
        word = {"built": "done", "in-flight": "in flight"}.get(st, "not started")
        when_s = dates.get(s, "")
        A(f'<div class="stage {cls}"><span class="lamp"></span><div class="head">'
          f'<h2>{E(label)}</h2><span class="status {cls}">{E(word)}</span>'
          + (f'<span class="when">{E(when_s)}</span>' if when_s else "") +
          f'</div><div class="card"><div class="blurb">{E(blurb)}</div><ul class="steps">')
        # The gates report cumulatively — every rung repeats every earlier
        # rung's requirements. Rendered literally that reads as eight identical
        # stages. What a rung MEANS is what it added over the one before it.
        fresh = [it for it in r.get("have_items", []) if it not in seen_have]
        seen_have.update(r.get("have_items", []))
        for it in fresh:
            A(f'<li><span class="mark done">✓</span><span class="s-name">{E(plain(it))}</span></li>')
        for it in r.get("need_items", []):
            A(f'<li><span class="mark todo">○</span><span class="s-name todo">{E(plain(it))}</span>'
              f'<span class="s-fact">still needed</span></li>')
        if not fresh and not r.get("need_items"):
            A('<li><span class="mark done">✓</span><span class="s-name">'
              'Nothing had to be on disk to start — this is where work enters</span></li>')
        A('</ul>')
        made = artefacts(slug, s, r.get("have_items", []))
        if made:
            A('<div class="made"><h4>What we created</h4><ul>')
            for a in made:
                A(f'<li><span class="what">{E(a["name"])}</span>'
                  f'<a class="open" href="../../{E(a["file"])}">open</a></li>')
            A('</ul></div>')
        A('</div></div>')
    A('</div>')

    # ---- what we ruled out ------------------------------------------------
    if ro:
        A('<section class="ruled"><h2>What we considered and threw away</h2><ul>')
        for r in ro:
            A(f'<li><span class="what">{E(r["what"])}</span>'
              f'<span class="why">{E(r["why"][:260])}</span></li>')
        A('</ul></section>')

    # ---- honest holes -----------------------------------------------------
    A('<footer><h3>What this page cannot show yet, and why</h3><ul>')
    A('<li><b>How long each rung took.</b> Gate records are dated to the day, and '
      'most journeys land two rungs on one date — so day resolution reads zero. '
      'Per-task start/end stamps started being written on 2026-08-06; there are '
      'few enough that a comparison would mislead.</li>')
    A('<li><b>The drawn current-situation and proposal panels.</b> Agreed in the '
      'mock, and a drawing has no source on disk to derive from. It needs a '
      'declared home before this page can carry it.</li>')
    A('<li><b>What it measured once in use.</b> No artifact records post-ship '
      'measurement, so there is nothing to read.</li>')
    A('<li><b>An evaluation matrix of what we considered.</b> The machinery is '
      'built and CI-enforced and holds zero matrices, so there is nothing to '
      'render.</li>')
    A('</ul><p class="foot">Every other value above is derived from the repo at the '
      'commit named in the header. Nothing on this page is hand-maintained, so it '
      'cannot quietly go stale — but it also cannot show what was never '
      'written down.</p></footer>')

    A('</div></body></html>')
    return "\n".join(P)


CSS = """<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
--paper:#FBFAF7;--card:#FFF;--ink:#22312F;--ink-soft:#5C6B67;--hairline:#E4E7E4;
--moss:#3E7C4F;--moss-chip:#E3EFE6;--amber:#C98A2E;--amber-chip:#FBF0DC;
--red:#C6453F;--red-chip:#F8E4E2;--slate:#8C9793;
}
body{background:var(--paper);color:var(--ink);
font:16px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;
padding:44px 24px 90px}
.wrap{max-width:980px;margin:0 auto}
header{margin-bottom:38px}
.eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;
color:var(--ink-soft);font-weight:600;margin-bottom:10px}
h1{font-size:33px;line-height:1.18;letter-spacing:-.015em;max-width:22ch}
.derived{margin-top:12px;font-size:13px;color:var(--ink-soft)}
code{font:13px ui-monospace,SFMono-Regular,Menlo,monospace;background:#F1F0EC;
padding:1px 6px;border-radius:5px}
h2{font-size:12px;letter-spacing:.12em;text-transform:uppercase;
color:var(--ink-soft);font-weight:700;margin-bottom:14px}
section{margin-bottom:38px}

.whybox{background:var(--card);border:1px solid var(--hairline);
border-left:4px solid var(--moss);border-radius:14px;padding:22px 26px}
.whybox blockquote{font-size:19px;line-height:1.5;max-width:62ch}
.whybox .src{margin-top:12px;font-size:13px;color:var(--ink-soft)}

.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}
.res{background:var(--card);border:1px solid var(--hairline);border-radius:14px;
padding:18px 20px}
.res .num{font-size:23px;font-weight:700;letter-spacing:-.02em;color:var(--moss);
font-variant-numeric:tabular-nums}
.res .cap{margin-top:5px;font-size:13px;color:var(--ink-soft);line-height:1.4}

.rl{display:grid;gap:12px}
.risk{background:var(--card);border:1px solid var(--hairline);border-radius:14px;
padding:16px 20px;border-left:5px solid var(--slate)}
.risk.green{border-left-color:var(--moss)}
.risk.amber{border-left-color:var(--amber)}
.risk.red{border-left-color:var(--red)}
.rhead{display:flex;gap:9px;align-items:center;margin-bottom:7px}
.lightword{font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
padding:3px 10px;border-radius:999px}
.risk.green .lightword{background:var(--moss-chip);color:var(--moss)}
.risk.amber .lightword{background:var(--amber-chip);color:#9A5A17}
.risk.red .lightword{background:var(--red-chip);color:var(--red)}
.killer{font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
color:var(--red)}
.rtext{font-weight:600;line-height:1.45;max-width:78ch}
.rcm,.rtr{margin-top:7px;font-size:13.5px;color:var(--ink-soft);line-height:1.45;max-width:82ch}
.rcm b,.rtr b{color:var(--ink)}

.minimap{display:flex;gap:0;align-items:flex-start;margin:34px 0 8px}
.mm{flex:1;text-align:center;position:relative}
.mm::before{content:"";position:absolute;top:7px;left:0;right:0;height:2px;
background:var(--hairline)}
.mm:first-child::before{left:50%}
.mm:last-child::before{right:50%}
.mm.reached::before{background:var(--moss)}
.mm .dot{width:16px;height:16px;border-radius:50%;background:#FFF;
border:2px solid var(--hairline);margin:0 auto 7px;position:relative;z-index:1}
.mm.done .dot{background:var(--moss);border-color:var(--moss)}
.mm.now .dot{background:var(--amber);border-color:var(--amber)}
.mm .l{font-size:11px;color:var(--ink-soft);font-weight:600}
.mapnote{font-size:13.5px;color:var(--ink-soft);margin-bottom:34px}

.ladder{display:grid;gap:16px}
.stage{position:relative;padding-left:34px}
.lamp{position:absolute;left:0;top:6px;width:14px;height:14px;border-radius:50%;
background:#FFF;border:2px solid var(--hairline)}
.stage.done .lamp{background:var(--moss);border-color:var(--moss)}
.stage.now .lamp{background:var(--amber);border-color:var(--amber)}
.head{display:flex;gap:11px;align-items:center;flex-wrap:wrap}
.head h2{font-size:17px;letter-spacing:-.01em;text-transform:none;color:var(--ink);
margin-bottom:0}
.status{font-size:11px;font-weight:700;padding:3px 10px;border-radius:999px;
letter-spacing:.05em}
.status.done{background:var(--moss-chip);color:var(--moss)}
.status.now{background:var(--amber-chip);color:#9A5A17}
.status.todo{background:#F1F0EC;color:var(--slate)}
.when{font-size:12px;color:var(--ink-soft);font-variant-numeric:tabular-nums}
.stage .card{margin-top:11px;background:var(--card);border:1px solid var(--hairline);
border-radius:14px;padding:17px 21px}
.stage.todo .card{background:#FCFCFB;border-style:dashed}
.blurb{font-size:13.5px;color:var(--ink-soft);margin-bottom:11px}
.steps{list-style:none}
.steps li{display:flex;align-items:baseline;gap:11px;padding:6px 0;
border-bottom:1px solid var(--hairline);flex-wrap:wrap}
.steps li:last-child{border-bottom:none}
.mark{font-weight:700;width:16px;flex:none;text-align:center}
.mark.done{color:var(--moss)}
.mark.todo{color:var(--slate)}
.s-name{font-weight:600}
.s-name.todo{font-weight:500;color:var(--ink-soft)}
.s-fact{margin-left:auto;font-size:12px;font-weight:600;color:var(--slate);white-space:nowrap}
.made{margin-top:13px}
.made h4{font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
color:var(--ink-soft);margin-bottom:4px}
.made ul{list-style:none}
.made li{display:flex;gap:10px;align-items:baseline;padding:5px 0;
border-bottom:1px dashed var(--hairline)}
.made li:last-child{border-bottom:none}
.made .what{font-weight:600;font-size:14px}
a.open{font-size:11.5px;font-weight:600;color:var(--ink);text-decoration:none;
border:1px solid var(--hairline);border-radius:999px;padding:2px 10px;
white-space:nowrap;margin-left:auto}
a.open:hover{border-color:var(--ink-soft)}
a.open::after{content:" ↗";color:var(--ink-soft)}

.ruled ul{list-style:none;display:grid;gap:9px}
.ruled li{background:var(--card);border:1px solid var(--hairline);border-radius:12px;
padding:13px 18px}
.ruled .what{font-weight:700;display:block;margin-bottom:3px}
.ruled .why{font-size:13.5px;color:var(--ink-soft);line-height:1.45}

footer{margin-top:54px;padding-top:24px;border-top:1px solid var(--hairline)}
footer h3{font-size:12px;letter-spacing:.12em;text-transform:uppercase;
color:var(--ink-soft);margin-bottom:12px}
footer ul{list-style:none;display:grid;gap:8px;max-width:80ch}
footer li{font-size:13.5px;color:var(--ink-soft);line-height:1.5;
padding-left:16px;position:relative}
footer li::before{content:"—";position:absolute;left:0;color:var(--slate)}
footer li b{color:var(--ink)}
.foot{margin-top:16px;font-size:13px;color:var(--ink-soft);max-width:72ch;line-height:1.5}

@media (max-width:700px){
h1{font-size:26px}
.mm .l{font-size:9px}
.stage{padding-left:26px}
.s-fact,a.open{margin-left:27px}
}
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
