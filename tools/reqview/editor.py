#!/usr/bin/env python3
"""The register's edit surface — a local process, not a server.

    python3 tools/reqview/editor.py          # then open http://localhost:8765

WHY THIS EXISTS. Reading happened in a rendered page, editing in a markdown
editor, and sealing in a terminal: three surfaces for one job, and the producer
had to hold the mapping between them. This is one window.

WHY A LOCAL PROCESS. A `file://` page cannot write to disk — the File System
Access API requires https or http://localhost, and Firefox and Safari ship no
pickers at all. Verified 2026-08-15 rather than assumed. So a page that saves
what you type needs a process behind it. It is stdlib-only, binds to loopback,
and stops when you close it.

THE TWO ZONES, which is what makes this small. A DRAFT carries no machinery:
edit freely, nothing is hashed, nothing refuses. The fingerprint engages at ONE
moment — approval — and once per requirement, ever. Applying agreement
machinery to things nobody has agreed to was the whole source of the weight.

THE FIVE OPERATIONS, and no others:

    edit title        the heading handle   — rule 3 puts it OUTSIDE the
                                             fingerprint, so it is always free
    edit description  **Statement.**       — inside the fingerprint
    edit / add Why    **Why.**             — inside the fingerprint
    approve           **Approval.**        — the only computing moment
    mark for discussion  a `> **Note —` blockquote — outside the fingerprint,
                                             so marking never un-approves

There is deliberately NO kill button. Rule 10: a model may propose a kill and
may never record one, and a graveyard entry owes `what was learned` — which is
the field that stops a dead idea being re-proposed. Marking `kill?` opens that
conversation; it does not perform it.

DISCUSSION NOTES ARE PERMANENT — ruled by Tony 2026-08-15: "trail is good".
The page adds them and cannot clear them, and that is the design rather than a
gap. A note records that a question was asked and, once the Why answers it,
that it was settled — which is the same reason a graveyard entry keeps `what
was learned`. Clearing them would leave a register that looks like nobody ever
doubted anything. Removing one is a deliberate edit in the file.

THE SAFETY PROPERTY. Every write is applied to the markdown, re-parsed with the
same parser the view and the audit use, and rolled back if the result does not
parse. The file on disk is never left in a state the tooling cannot read.
"""
import http.server
import json
import os
import re
import socketserver
import sys
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import reqview                                                   # noqa: E402

PORT = int(os.environ.get("REQVIEW_PORT", "8765"))
REGISTER = reqview.REGISTER

FIELD_LABELS = {"statement": "Statement", "why": "Why"}
DISCUSS_KINDS = {"kill": "Discuss: kill?", "explain": "Discuss: explain"}


# --------------------------------------------------------------------------
# block surgery — every edit is scoped to one block and re-parsed after
# --------------------------------------------------------------------------

# One definition, in reqview — the single-parser rule applies to locating a
# block just as much as to reading one.
block_span = reqview.block_span


def set_field(block, label, value):
    """Replace a field's whole paragraph. The label may carry a modifier —
    `**Statement (derived).**` — and the modifier is preserved: dropping it
    would silently un-mark a derivation, which rule 12 exists to make visible."""
    pat = re.compile(r"(\*\*" + label + r"(?:\s*\([^)]*\))?\.\*\*)(.*?)(?=\n\n|\n---|\Z)",
                     re.S)
    m = pat.search(block)
    if not m:
        return None
    return block[:m.start()] + m.group(1) + " " + value.strip() + block[m.end():]


def set_handle(block, handle):
    """The heading handle. Rule 3: outside the fingerprint, reworded freely."""
    return re.sub(r"(^\n?### R-\d{4} — )(.*)$",
                  lambda m: m.group(1) + handle.strip(),
                  block, count=1, flags=re.M)


def add_note(block, label, comment):
    """Append a note after the fields. Notes are outside the fingerprint, so a
    discussion mark never disturbs an approval."""
    body = ("> **Note — %s** %s" % (label, comment.strip())).rstrip()
    body = "\n".join(l if l.startswith(">") else "> " + l for l in body.split("\n"))
    stripped = block.rstrip()
    if stripped.endswith("---"):
        stripped = stripped[:-3].rstrip()
        return stripped + "\n\n" + body + "\n\n---\n"
    return stripped + "\n\n" + body + "\n"


def apply_edit(text, ref, op, payload):
    span = block_span(text, ref)
    if not span:
        return None, "no block %s" % ref
    a, b = span
    block = text[a:b]

    if op == "title":
        block = set_handle(block, payload["value"])
    elif op in ("statement", "why"):
        block = set_field(block, FIELD_LABELS[op], payload["value"])
        if block is None:
            return None, "no %s field on %s" % (op, ref)
    elif op == "approve":
        block = set_field(block, "Approval", payload["value"])
        if block is None:
            return None, "no approval field on %s" % ref
    elif op == "discuss":
        kind = DISCUSS_KINDS.get(payload.get("kind"))
        if not kind:
            return None, "unknown discussion kind"
        block = add_note(block, kind, payload.get("comment", ""))
    else:
        return None, "unknown operation %r" % op
    return text[:a] + block + text[b:], None


def write_checked(new_text):
    """Parse before writing. A file the tooling cannot read is worse than a
    rejected edit, so the rejection is what happens."""
    refusals = []
    reqview.parse(new_text, refusals)
    if refusals:
        first = refusals[0]
        return "the edit would break the register: %s — %s" % (
            first["where"], first["why"].split(".")[0])
    REGISTER.write_text(new_text, encoding="utf-8")
    return None


# --------------------------------------------------------------------------
# model for the page
# --------------------------------------------------------------------------

def snapshot():
    text = REGISTER.read_text(encoding="utf-8")
    refusals = []
    _, blocks, _ = reqview.parse(text, refusals)
    recs, graves, _ = reqview.build(blocks, refusals)
    out = []
    for r in recs:
        out.append({
            "ref": r["ref"], "handle": r["handle"],
            "statement": r["statement"], "why": r["why"],
            "traces": r["traces"], "depends": r["depends"],
            "state": r["state"], "fp": r["fp"],
            "approver": r["approver"], "approved_on": r["approved_on"],
            "derived": r["derived"],
            "why_missing": bool(reqview.PLACEHOLDER_WHY.search(r["why"])),
            "notes": r["notes"],
        })
    return {"requirements": out, "graveyard": len(graves),
            "refusals": [{"where": x["where"], "why": x["why"]} for x in refusals]}


# --------------------------------------------------------------------------
# the page
# --------------------------------------------------------------------------

PAGE = r"""<!doctype html><html><head><meta charset="utf-8">
<title>Requirements — edit</title>
<style>
:root{--ink:#1c1c1c;--bg:#faf9f7;--card:#fff;--line:#e3e0da;--muted:#6b6660;
--draft:#b8860b;--agreed:#2e7d32;--flag:#b3261e;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
header{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);
padding:14px 24px;display:flex;gap:18px;align-items:baseline;z-index:9}
h1{font-size:16px;margin:0;font-weight:600}
.count{color:var(--muted);font-size:13px}
main{max-width:900px;margin:0 auto;padding:24px}
.rq{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--draft);
border-radius:6px;padding:16px 18px;margin:0 0 16px}
.rq.agreed{border-left-color:var(--agreed)}
.rq.flagged{border-left-color:var(--flag)}
.hd{display:flex;gap:10px;align-items:baseline;margin-bottom:10px}
.ref{font:600 13px ui-monospace,Menlo,monospace;color:var(--muted)}
.zone{margin-left:auto;font-size:11px;text-transform:uppercase;letter-spacing:.08em;
color:var(--draft)}
.agreed .zone{color:var(--agreed)}
.lbl{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);
margin:12px 0 4px}
[contenteditable]{outline:none;border:1px solid transparent;border-radius:4px;
padding:5px 7px;margin:-5px -7px;white-space:pre-wrap}
[contenteditable]:hover{border-color:var(--line)}
[contenteditable]:focus{border-color:#7aa7d9;background:#fbfdff}
.title{font-weight:600;font-size:15px}
.missing{color:#a3968a;font-style:italic}
.meta{font-size:12px;color:var(--muted);margin-top:12px;
display:flex;gap:14px;flex-wrap:wrap;align-items:center}
button{font:inherit;font-size:12px;padding:5px 12px;border:1px solid var(--line);
background:#fff;border-radius:5px;cursor:pointer}
button:hover{border-color:#999}
button.go{border-color:var(--agreed);color:var(--agreed)}
button.flag{border-color:var(--flag);color:var(--flag)}
button[disabled]{opacity:.4;cursor:not-allowed}
.fp{font:12px ui-monospace,Menlo,monospace;color:var(--muted)}
.note{background:#fff8e6;border-left:3px solid var(--draft);padding:7px 11px;
margin-top:10px;font-size:13px;border-radius:0 4px 4px 0}
.note.kill{background:#fdeceb;border-left-color:var(--flag)}
#toast{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);
background:#1c1c1c;color:#fff;padding:9px 16px;border-radius:6px;font-size:13px;
opacity:0;transition:opacity .18s;pointer-events:none;max-width:80vw}
#toast.show{opacity:1}
#toast.bad{background:var(--flag)}
.saved{color:var(--agreed)}
@media(prefers-color-scheme:dark){:root{--ink:#e8e6e3;--bg:#17181a;--card:#1f2124;
--line:#33363b;--muted:#9a958e}[contenteditable]:focus{background:#20262e}
.note{background:#2a2416}.note.kill{background:#2c1b1a}}
</style></head><body>
<header><h1>Requirements</h1><span class="count" id="count"></span>
<span class="count" id="hint">edit inline · blur to save</span></header>
<main id="list"></main><div id="toast"></div>
<script>
let DATA=null;
const $=s=>document.querySelector(s);
function toast(m,bad){const t=$('#toast');t.textContent=m;
t.className='show'+(bad?' bad':'');setTimeout(()=>t.className='',bad?4200:1500);}
async function load(){const r=await fetch('/api/register');DATA=await r.json();render();}
async function send(ref,op,payload){
  const r=await fetch('/api/edit',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify(Object.assign({ref:ref,op:op},payload))});
  const j=await r.json();
  if(!j.ok){toast(j.error,true);await load();return false;}
  await load();return true;}
function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
function render(){
  const live=DATA.requirements;
  const agreed=live.filter(r=>r.state==='approved').length;
  const flagged=live.filter(r=>r.notes.some(n=>/^Discuss/.test(n.label))).length;
  $('#count').textContent=live.length+' live · '+agreed+' agreed · '
    +(live.length-agreed)+' draft'+(flagged?' · '+flagged+' flagged':'');
  $('#list').innerHTML=live.map(card).join('');
  bind();}
function card(r){
  const isAgreed=r.state==='approved';
  const flagged=r.notes.some(n=>/^Discuss/.test(n.label));
  const cls='rq'+(isAgreed?' agreed':'')+(flagged?' flagged':'');
  const zone=isAgreed?'agreed':(r.state==='invalidated'?'changed since approval':'draft');
  const notes=r.notes.map(n=>'<div class="note'+(/kill/.test(n.label)?' kill':'')
    +'"><b>'+esc(n.label)+'</b> '+esc(n.text)+'</div>').join('');
  return '<article class="'+cls+'" data-ref="'+r.ref+'">'
   +'<div class="hd"><span class="ref">'+r.ref+'</span>'
   +'<span class="title" contenteditable data-op="title">'+esc(r.handle)+'</span>'
   +'<span class="zone">'+zone+'</span></div>'
   +'<div class="lbl">Description'+(r.derived?' (derived)':'')+'</div>'
   +'<div contenteditable data-op="statement">'+esc(r.statement)+'</div>'
   +'<div class="lbl">Why</div>'
   +'<div contenteditable data-op="why" class="'+(r.why_missing?'missing':'')+'">'
   +esc(r.why)+'</div>'
   +notes
   +'<div class="meta">'
   +(isAgreed
      ? '<span class="fp">'+esc(r.approver)+' · '+esc(r.approved_on)+' · fp:'+r.fp+'</span>'
      : '<button class="go" data-act="approve"'+(r.why_missing?' disabled title="the Why is still blank"':'')
        +'>Approve</button>')
   +'<button data-act="explain">Needs explanation</button>'
   +'<button class="flag" data-act="kill">Possible kill</button>'
   +'</div></article>';}
function bind(){
  document.querySelectorAll('[contenteditable]').forEach(el=>{
    el.dataset.orig=el.textContent;
    el.addEventListener('blur',async()=>{
      const v=el.textContent.trim();
      if(v===el.dataset.orig.trim())return;
      const ref=el.closest('.rq').dataset.ref;
      if(await send(ref,el.dataset.op,{value:v}))toast('saved '+ref);});
    el.addEventListener('keydown',e=>{
      if(e.key==='Escape'){el.textContent=el.dataset.orig;el.blur();}
      if(e.key==='Enter'&&el.dataset.op==='title'){e.preventDefault();el.blur();}});});
  document.querySelectorAll('button[data-act]').forEach(b=>{
    b.addEventListener('click',async()=>{
      const ref=b.closest('.rq').dataset.ref, act=b.dataset.act;
      if(act==='approve'){
        if(!confirm('Approve '+ref+'?\n\nThis fingerprints the description, the Why '
          +'and the links as they read now.'))return;
        await send(ref,'approve',{});toast('approved '+ref);return;}
      const c=prompt(act==='kill'?'Why might this be killed?':'What needs explaining?');
      if(c===null)return;
      await send(ref,'discuss',{kind:act,comment:c});toast('flagged '+ref);});});}
load();
</script></body></html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        raw = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, PAGE, "text/html")
        if self.path == "/api/register":
            return self._send(200, json.dumps(snapshot()))
        self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path != "/api/edit":
            return self._send(404, json.dumps({"error": "not found"}))
        n = int(self.headers.get("Content-Length", "0"))
        try:
            req = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception as e:
            return self._send(400, json.dumps({"ok": False, "error": str(e)}))

        ref, op = req.get("ref"), req.get("op")
        text = REGISTER.read_text(encoding="utf-8")
        payload = dict(req)
        if op == "approve":
            import datetime
            payload["value"] = "Tony, %s" % datetime.date.today().isoformat()

        new_text, err = apply_edit(text, ref, op, payload)
        if err:
            return self._send(200, json.dumps({"ok": False, "error": err}))
        err = write_checked(new_text)
        if err:
            return self._send(200, json.dumps({"ok": False, "error": err}))
        if op == "approve":
            reqview.seal(quiet=False)
        self._send(200, json.dumps({"ok": True}))

    def log_message(self, *a):
        pass


def main():
    # Every print flushes. A buffered start-up message means the terminal looks
    # empty while the process is in fact running, which is indistinguishable
    # from "it didn't start" — and that is exactly how this first failed.
    def say(m=""):
        print(m, flush=True)

    if not REGISTER.exists():
        say("No register at %s" % REGISTER)
        return 1

    socketserver.TCPServer.allow_reuse_address = True
    # Loopback only. Nothing here should be reachable from another machine.
    httpd, port = None, None
    for cand in range(PORT, PORT + 10):
        try:
            httpd = socketserver.TCPServer(("127.0.0.1", cand), Handler)
            port = cand
            break
        except OSError as e:
            say("port %d is busy (%s) — trying %d" % (cand, e.strerror or e, cand + 1))
    if httpd is None:
        say("Could not bind any port in %d-%d. Set REQVIEW_PORT to a free one."
            % (PORT, PORT + 9))
        return 1

    url = "http://localhost:%d" % port
    say()
    say("  editing  %s" % REGISTER)
    say("  OPEN     %s" % url)
    say("  stop     ctrl-c")
    say()
    opened = False
    try:
        opened = webbrowser.open(url)
    except Exception as e:
        say("  (could not launch a browser automatically: %s)" % e)
    if not opened:
        say("  No browser opened automatically — paste the URL above into one.")
        say()
    try:
        with httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        say("\nstopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
