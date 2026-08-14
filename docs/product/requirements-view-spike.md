---
route: spike
stage: findings
---

# Requirements view — Spike A findings

**The spike ran. It does not ship.** Whatever survives re-enters the ladder as
normal work. What exists is `tools/reqview/reqview.py` (Python standard library
only) and the page it writes to `output/requirements.html`.

**The question it answered:** can a generated HTML view over markdown we already
own deliver everything the producer's 08:16 list asks for, with paste-back
editing, and without acquiring a third-party runtime dependency?

**The answer: yes on capability, yes on dependency, and a qualified no on the
paste-back economics — which is the finding that matters.** Detail below.

---

## The kill criteria, each answered

### 1 — "Dependencies between requirements cannot be shown legibly." DID NOT HOLD.

The live set declares **ten dependency references across nine blocks**, and the
generator reproduces that count exactly — the same number the register's own
preamble claims, arrived at independently, which is the one cross-check
available.

Both directions render, and the derivation is visible as a derivation:

- Each card carries a three-column **dependency box**: `Traces to` (goal and law
  targets, laws tinted differently since they are excluded from coverage
  arithmetic), `Depends on` marked **stored**, and `Depended on by` marked
  **derived — not in the file**, on a tinted panel with a dashed rule so the two
  are never confused. The string `Depended on by` appears **39 times in the view
  and zero times in the register**; the reverse is computed on every render and
  written nowhere.
- A **dependency map** above the set gives one box per depended-upon requirement
  with its dependents listed under it — the "what breaks if I change this"
  question, answered by reading, not by running a report.
- Every reference is a chip that scrolls to its target and flashes it. Both
  directions are one click apart.
- An unresolved reference renders red and is reported. Rule 8 makes a dangling
  reference an error that stops the run; the generator reports rather than stops,
  because a spike that refuses to render teaches nothing.

Boxes, not a graph. That is also the honest reason this criterion failed to
kill: a *drawn* graph of 39 nodes would have needed a layout engine, and a
layout engine is where the dependency would have entered. Nested boxes and
two-way chips answer the same question and cost nothing.

### 2 — "The paste-back loop costs more effort than editing the markdown directly." HOLDS ON THE NARROW READING. Does not hold on the yardstick it was written against.

This is the one that needs the honest answer, so here is the arithmetic rather
than an impression.

**Counting producer actions for N text edits in one sitting:**

| | locate | change | commit the change | total |
|---|---|---|---|---|
| **The view** | 1 (search box) | 2 (toggle edit, type) + 1 (toggle done) | 3 fixed (copy, paste to model, regenerate + reload) | **4N + 3** |
| **The markdown file** | 1 (editor find) | 1 (type) | 1 fixed (save) | **2N + 1** |

- **One edit: 7 actions in the view against 3 in the file.**
- Ten edits: 43 against 21.

**On raw text editing the file wins, and it always will.** Nothing built here
changes that, and no future version will: an editor is already the cheapest
possible way to change text in a text file. Reported as a kill, not argued away.

Three things qualify it, and each is checkable:

1. **Two of the four per-edit actions are my design choice, not the loop's cost.**
   The edit/done toggle exists because I wanted a rendered reading view. Always-
   editable textareas remove both and bring the view to **2N + 3** — parity with
   the file plus a fixed two. The fixed three do not grow with N; the loop gets
   relatively cheaper with every edit in a sitting, which is exactly the "many
   requirments" case his 08:20 words name.
2. **The comparison is not like-for-like, and that is not a technicality.** Two
   of the five capabilities he asked for — **comments and attachments** — cannot
   be done in the markdown file at any action count, because there is nowhere to
   put them. The shape document is explicit that they live *beside* the record and
   never on it, and **no beside-space exists in this repository.** For those, the
   file's cost is not 2N + 1; it is undefined.
3. **The criterion's stated yardstick is his own** — *"i just mind overhead and
   overwork"* — which is about the job, not the keystroke. The job includes seeing
   which requirements break when one changes and seeing which are approved. The
   file supplies neither at any price.

**Verdict as I would report it to him: not killed, but only because the two
routes do different jobs. If the job is "change some words", use the file — the
view will never beat it. The view earns its place on the four things the file
cannot do at all.**

**And the loop is not closed.** The page emits the block in one click; **nothing
applies it.** A model applies it by hand, unverified. The applier is where the
real remaining cost sits and I did not build it — see the recommendation.

### 3 — "It cannot be built without a dependency of its own." DID NOT HOLD.

`tools/reqview/reqview.py` imports `hashlib`, `html`, `json`, `re`, `sys`,
`datetime`, `pathlib`. Nothing else, ever. The page has zero external references:
no CDN, no web font, no `fetch`, no `XMLHttpRequest`, no `@import`. Verified by
grep against the generated output, which returned nothing.

Two places where a dependency would normally be reached for, and what was done
instead:

- **SHA-256 in the browser**, so an edited requirement recomputes its fingerprint
  live. `crypto.subtle` is unavailable outside a secure context and `file://` is
  not reliably one across browsers. A compact SHA-256 is written into the page
  (~30 lines). Verified under node against the empty string and `"abc"`, and it
  reproduces published fingerprint vector 1 from the page's own code.
- **Markdown rendering.** A six-line inline renderer covers what the register's
  fields actually contain: bold, italic, backticks, open markers, and rule 6's
  reserved form. It is deliberately partial — no tables, no lists, no inline
  links — and would need widening, not replacing, if field content grows.

**Font:** the system UI stack (`-apple-system`, `Segoe UI`, `Roboto`, …). Legible,
no typeface opinion imposed, nothing to download.

---

## What the register broke, and what that says about the format

**A parse failure here is a finding about the format, not just a bug in my
parser.** Two real ones and two smaller.

### 1 — A bold field label that wraps across lines silently corrupts the field above it. R-0048.

R-0048 carries a note paragraph beginning:

```
**Reworked 2026-08-14 14:54, on the producer's authorised ruling, and its
dependency dropped in the same edit.**
```

The closing `**` is on the **second** line. A line-oriented parser — the obvious
implementation of rule 1, which describes fields as `bold label, full stop` — does
not see a boundary, and swallows the entire eight-line note into the preceding
field. That field is `Depends on`.

**The consequence was not cosmetic.** The note discusses R-0018 and R-0004 in
prose. Absorbed into `Depends on`, they became **declared dependencies**. The first
run reported *14 dependency links* and a **dangling reference from R-0048 to a
graveyard entry** — a fabricated rule 8 violation that looks exactly like a real
one. After the fix: 10 links, no dangling reference, matching the register's own
preamble.

**This is the format's problem, not mine.** The shape gives non-field bold
paragraphs — `**Reworked …**`, `**Re-pointed …**`, `**Unhomed by that kill …**` —
*the same form as a field label*. Nothing but a whitelist of known labels tells a
machine which is which, and a wrapped label defeats even the whitelist. The
register uses these notes deliberately and says so ("written as prose beside the
five required fields, not as a sixth field"), so they are not going away.

**Recommendation:** give a beside-the-fields note a form a machine can see —
a distinct prefix, or a rule that a field label never wraps.

### 2 — `## Findings` sits at heading level two, between the requirements and the graveyard.

Rule 13 says **nothing else sits at heading level two** and the graveyard is
**always last**. The register has three level-two sections and the graveyard is
third of three.

The damage is concrete: `## Findings` contains headings like `### 1 — Forty-six
requirements have no honest Why`, and `### 7 — The one thing to look at first`.
**A parser that treats every level-three heading under the register as a
requirement block reads seven findings as seven requirements.** Mine survives only
because it dispatches on the level-two section name and refuses to read anything
outside `## Requirements` and `## Graveyard`. That is the correct behaviour, and
it means the findings the producer wrote for himself are invisible to any
generated view.

**Recommendation:** either rule 13 gains a sanctioned third section, or the
findings move out of the register. Right now the file breaks its own frame.

### 3 — `Traces to` has a third legal value in practice.

R-0031 reads `**Traces to.** not yet traced — see Findings`. Rule 7 allows one or
more targets, or the declared `no parent, by design`. This is neither. The view
renders it as a warning tag rather than pretending it is a target — an honest
render of a value the format does not define.

### 4 — Small, and both already documented as deliberate.

- **No machine names anywhere.** Rule 4 says nobody hand-writes one and the
  checking tool inserts it; the tool has not run. The parser reads the comment
  when present and never demands it.
- **The `---` separators** sit inside the trailing field of each block, not
  between blocks in any structural sense. Stripped on parse. Worth knowing before
  anyone writes a second parser.

### And what did NOT break, which is worth recording

- **The fingerprint recipe is implementable from rule 9 alone.** Both published
  test vectors reproduce on the first attempt — including the discriminating
  derived-statement vector, which catches an implementation that strips the label
  wrongly or drops the `derived: ` prefix. The generator **refuses to render** if
  either vector fails, so a recipe drift is caught before a page is written.
- **All 39 live blocks carry all five required fields.** No omissions, no
  duplicated labels, no malformed approval lines.
- **All ten dependency references resolve.** The register's claim is true.
- **All 13 graveyard entries carry all six fields and a named kill authoriser.**
  Rule 10 is fully honoured.
- **State is computed and the answer is the honest one: 0 approved, 0
  invalidated, 39 never approved.** No status field was read, because there is
  none.

---

## What the view does, against his list

| His words | What the page does |
|---|---|
| *"see the requirments and their dependencies"* | Dependency map plus a per-card box showing stored and derived directions, chips both ways |
| *"interact with and edit the text"* | Statement, Why, Traces to and Depends on are editable in place; the fingerprint recomputes live and says which approval it would invalidate |
| *"see its status (for each requirment)"* | Computed from rule 9. Never / invalidated / approved, on every card |
| *"add comments perhaps for you to pick up or to record notes around the requirments"* | Comments beside each requirement, with an explicit **for the model to pick up** flag that survives into the handover block in capitals. His preposition — *around* — is honoured: nothing touches the fingerprint |
| *"add links or images perhaps as input"* | Links and images beside the requirement; images inlined as data URIs and carried into the handover |
| *(the graveyard)* | All 13, with **what was learned** promoted to the top of each entry in a white box, because that is the field that exists so a killed idea is not proposed again |

**Making an unapproved set look unapproved** was a stated constraint and it drove
the design: a hatched amber banner states *"Nothing in this set is approved"* above
the fold with the arithmetic beside it, every card carries a `NEVER APPROVED`
badge and a six-pixel amber left edge, and the counters render the never-approved
and invalidated tallies in the alarm colour while `0 approved` stays plain. The
set does not read as neutral. It reads as unfinished, which it is.

**Write-back is paste-back and the page never writes to disk.** The handover block
carries the register's SHA-256 **as it was when the page was rendered**, with an
instruction to refuse the paste if the file has moved since — which is R-0035's
requirement (*"a generated page carries the hash of the state it was rendered
from, so marks made against a stale view are refused rather than applied blind"*)
implemented rather than described. One edit, one comment and one attachment
produce a 47-line block. Copy is one click, with `execCommand` and
`navigator.clipboard` both attempted and a select-all fallback if a browser
blocks both.

---

## Verification, and what is NOT verified

**Verified:** both fingerprint vectors, in Python and again in the page's own
JavaScript under node; the parse against the real register with every count
cross-checked against the register's own claims; zero external references; every
JavaScript element lookup resolves to an id that exists; all 39 cards carry four
editable fields, three action buttons and a beside-space; the HTML closes every
tag it opens; the handover block generated end-to-end with a real edit, comment
and attachment.

**Not verified: the page has never been opened in a browser.** The Chrome
extension was not connected in this session and `file://` navigation was refused
by the tooling. Every interaction — click, edit, copy, `localStorage` on
`file://` — is **tested by code inspection and by executing the page's logic
under node, not by a human or an agent clicking it.** Tagged as *built, not yet
verified*. Someone should open it before any of this is believed.

---

## Would I build this properly? Yes — with five changes

**Yes.** No kill criterion held outright, the whole thing is 900 lines of standard
library, and it delivers four capabilities the markdown file cannot deliver at
any price. StrictDoc's 373 MB does not get to compete on this evidence.

What I would change, in the order I would do it:

1. **Build the applier, and build it first.** The paste-back loop is only half a
   loop: the page emits, nothing consumes. A second stdlib script that reads the
   handover block, refuses on hash mismatch, and rewrites the register turns one
   click plus a model turn into one click plus a command. **Until that exists, the
   loop's true cost is unmeasured, and everything above under-reports it.**
2. **Drop the edit/done toggle.** Always-editable fields halve the per-edit action
   count, from 4N + 3 to 2N + 3. It is the single cheapest change on this list.
3. **Give comments and attachments a real home in the repository.** They currently
   live in `localStorage` and die when the browser clears it. The shape mandates a
   beside-space and no beside-space exists — that is a gap in the format, not in
   the view, and it is the prerequisite for two of the five capabilities being
   real rather than demonstrated.
4. **Fix the two format defects before a second parser is written.** The wrapped
   bold label and the third level-two section both cost me a real bug; the first
   one fabricated a dependency and a rule 8 violation that looked entirely
   genuine. The next implementer will hit both.
5. **Take the direct-write-back decision consciously, because it collides with a
   constraint we set ourselves.** *"Works from disk with no server"* and *"writes
   directly to the file"* cannot both hold: direct write needs the File System
   Access API (Chrome only, and not on `file://`) or a local server. His 08:20
   words accept paste-back as the first step and name direct write-back as the
   target. **That target costs either a browser restriction or a process the
   producer has to start** — a decision, not an implementation detail, and it is
   the next thing to put in front of him.

**And the one thing not to change:** the file stays the only writable surface,
and the view stays disposable. Every tool in the 08-08 survey converged on that,
and nothing in this spike argued against it.
