# What a requirement looks like

**Status: AWAITING TONY'S REVIEW AND APPROVAL — BLOCKING.** Nothing may be
built against this shape until he has worked through it. Approval here is a
gate, not a status to record and move past: the process demands the answer, it
does not note its absence and continue — his rule, *"the process demand
approval or push back until approval"*.

**What changed since the last draft:** the first version was written from his
words alone, before any research existed. He stopped it himself: *"dont just
take 'he asked for them' as fact that is the best way."* The Law 4 research has
now run — standards, docs-as-code tools, enterprise tools, and AI-vendor
practice — and this rewrite is drafted against that evidence. Several decisions
were taken along the way and are treated as settled here: **approval is a
fingerprint, not a declared status, and the fingerprint covers the statement
and the links** (*"no point doing half of the fingerprint"*); **there is no
lifecycle or status field on a requirement**; **which release a requirement is
in lives on the release, never on the requirement**; **the plain-language
writing rules are adopted, shown as help where the writing happens**; and
**Jira is ruled out**.

**What changed 2026-08-14, second pass:** a fresh agent wrote five real
requirements using only this document and the goals, and its verdict was that
the reasoning holds and the format did not exist. This document now opens
with a **normative form** — the exact thing to write, shown before it is
argued — a resolution of each of the test's ten findings, and one precedence
proposal awaiting Tony's ruling. The reasoning below is unchanged.

**The bar this draft is held to:** across everything surveyed, the mandatory
minimum anywhere is **one field**. The most modern, most industry-negotiated
specification requires a title and nothing else; the exchange standard beneath
the big tools requires nothing at all. The old draft carried nine fields. Every
element below therefore argues for its place against a floor of one, and each
is labelled with which Law 4 step produced it — **ADOPTED** (taken from a named
source largely as-is), **ADAPTED** (taken and changed, with the change named),
or **BUILT** (no prior art exists; we are inventing, and that is flagged
loudly).

---

## The normative form — what a requirement looks like on the page

**Added 2026-08-14, after the writing test.** A fresh agent was given this
document and the goals and asked to write five real requirements. Its verdict,
verbatim: *"the reasoning holds up; the format does not yet exist."* It had to
invent eleven pieces of notation to write five requirements. Everything in this
section exists to make that never happen again. **This section is normative:
where it and the reasoning below seem to differ, this section is what you
write; the reasoning below is why.**

The form is shown before it is argued, because a writer needs the form and a
reader can take the arguments on trust until they want them.

### Two live requirements and one dead one, in exact final form

The blocks are shown fenced so that heading levels and delimiters are
unambiguous. **The references and content are illustrative — nothing below is
in the register, and these numbers are not allocations.** The fingerprint on
the first block is a genuinely computed value under the recipe given after the
examples, so an implementer can test against it.

```markdown
### R-0101 — spec lives in the work's repo
<!-- machine: 01a000da-8cb2-7a8c-812e-e2df8a27e480 -->

**Statement.** Kerd shall write the agreed spec for a work item to a file inside the repository that holds the work item.

**Why.** Law 1 makes the repository the boundary of a project, and Tony ruled on it directly: *"the way i work, every project has its own repo, its non negotiable."* A spec held anywhere else puts the agreement outside the boundary he treats as absolute, and separates it from the repository history that approval and change detection rely on.

**Traces to.** Law 1

**Depends on.** none

**Approval.** Tony, 2026-08-14 · fp:cf543030e4e7

---

### R-0102 — how a fine tune lands
<!-- machine: 01a000da-8cb2-7e00-8e72-10c058360c22 -->

**Statement.** A change classified as fine tuning shall reach a landed spec update by [OPEN-R-0102-1: whether fine tuning is a dedicated path of its own, or a rapid traversal of the normal path], and shall in either case land its change in the governing spec with the approval of the role that owns it.

**Why.** G3 names the class and the guard in his words: *"the process should allow and recognize and understand for small changes without breaking the process or cirumventing it… but also not let these small changes break the design spec or the archtecure or requirments without agreed change"*. The shape of the path is recorded in the goals as unchosen — that is the open marker above. The second half of the statement is not open: the guard binds whichever path is picked.

**Traces to.** G3

**Depends on.** R-0101

**Approval.** none — blocked by [OPEN-R-0102-1]
```

And the dead twin, in the graveyard at the end of the same document:

```markdown
## Graveyard

### R-0103 — DEAD — effort threshold below which the spec need not change
<!-- machine: 01a000da-8cb2-7e68-b8b5-dbc9a74f54ac -->

**Killed.** 2026-08-14, by the plain text of Law 2 in the approved goals. Killed by analysis, not by a test.

**Statement as proposed.** Kerd shall define an effort threshold, and a change falling below it shall land without an update to its governing spec, design, or requirement.

**Why it was proposed.** It follows directly from the pressure G3 names — *"i dont mind robust, i just mind overhead and overwork"* — and it is the design a reader arrives at independently from G3 alone.

**Why it is dead.** The goals rule it out by name: *"The law is absolute; the ceremony is proportionate."* And the reason it is harmful rather than merely unnecessary: a threshold decays Law 2 into *"significant changes only"* — a judgement call, and therefore a hole.

**What was learned.** When cost pressure argues for an exemption, the dial to reach for is the ceremony, never whether the document stays true. Any future requirement that scales process by size is checked against that split before it is written.

**Superseded by.** nothing — killed outright. The live requirement covering this territory is R-0102, which reaches the same speed by proportionate approval rather than by exemption.
```

**What the generated view adds that the file never carries:** under the first
requirement it shows *depended on by R-0102*, and it warns that editing the
first requirement invalidates the second's approval. Both are computed from
the stored direction. Neither is ever written into the document — a
hand-written reverse is a copy that drifts.

### The rules, stated flat

1. **A requirement is a level-three heading block.** Heading:
   `### <reference> — <handle>`. Blocks are separated by a `---` line. The
   machine name sits in an HTML comment on the line directly under the
   heading. Then the five labelled lines, bold label, full stop, one blank
   line between fields, always in this order: **Statement**, **Why**,
   **Traces to**, **Depends on**, **Approval**. All five are required on
   every live requirement — a field that does not apply says so explicitly
   (`none`), it is never omitted. Absence must be written, not implied.

2. **The reference** is `R-` plus a four-digit number: opaque, permanent,
   never changed, never reused. The uniform `R-` prefix carries no meaning —
   every requirement wears the same one; it exists only so a reference is
   findable by search. **Minting:** the next reference is the highest number
   present anywhere in the document — live blocks and graveyard together —
   plus one. The document plus its graveyard *is* the allocation register;
   that is what makes never-reuse observable. The checking tool refuses a
   duplicate. On "sequential" versus "meaning-free": creation order is the
   one fact about a requirement that can never change, so a sequence number
   is the one encoding that can never go stale. That is why sequence
   survives the scale lesson and category prefixes do not.

3. **The handle** is a short human name after the reference. It is
   notation, not a seventh element: it is outside the fingerprint, may be
   reworded at any time without touching identity or approval, and carries
   meaning deliberately — which is exactly why it is not the reference. It
   exists because the set is a document read top to bottom, and a page of
   bare `R-0101 … R-0105` headings is unreadable, which fails the reading
   the document decision was chosen for. The writing test added this out of
   necessity; it is adopted.

4. **The machine name** is a UUIDv7 in an HTML comment. "Hidden" means
   never rendered, never spoken, never typed by a person — not absent from
   the file. It must be in the file, because the file is the only writable
   surface; the HTML comment is invisible in every rendered view, which is
   the honest reconciliation of those two rules. **Nobody hand-writes one:**
   a writer adds a block without the comment, and the checking tool mints
   and inserts it on its next run. That is capture as a byproduct — the
   discipline-free mechanism this document already demands for the
   graveyard. A dead requirement keeps its machine name: a graveyard entry
   is precisely a record that has moved, which is the case the machine name
   exists to track.

5. **Open markers** are written `[OPEN-<reference>-<n>: the question]`,
   numbered per requirement, and are legal **in the Statement only**. The
   cap is at most three markers — counting markers, not requirements —
   across the live set; the graveyard never counts. A block with any open
   marker carries `**Approval.** none — blocked by [OPEN-…]`. A doubt about
   a Why is not a marker: it is either a comment beside the record, or the
   derived-statement flag below. The cap is countable by search precisely
   because the syntax is fixed; until the checking tool exists the cap is a
   convention, and an unenforced cap is the *looks like a contract and
   isn't one* failure — so the counter is part of the tool's first duty,
   not a later nicety.

6. **His words, in the Why**, are marked by one reserved form: an italic
   quotation with attribution — `Tony: *"…"*`, or *"…"* directly following
   his name and a date. **Inside the register, italic double-quoted text is
   verbatim producer words and nothing else may use that form.** Machines
   and readers distinguish his words from ours by form, not by judgement.

7. **Traces to** takes one or more targets, comma-separated, or the
   declared `no parent, by design`. A trace to a goal counts toward
   coverage; a trace to a law is a constraint link and is excluded from
   coverage arithmetic — laws are obeyed, not achieved, and counting the
   two together would make coverage mean nothing. A secondary source a
   requirement genuinely serves is a second target, not buried prose:
   prose is unqueryable, which is the loss the links element exists to
   prevent.

8. **Depends on** takes references only, or `none`. A reference that does
   not resolve is an error that stops the run — already settled; restated
   here because it is the writer's rule too.

9. **The approval line** is either `none` (with an optional reason after a
   dash) or `Tony, <date> · fp:<12 hex characters>`. **The fingerprint
   recipe:** take the text of Statement, Why, Traces to and Depends on, in
   that order; strip each bold label and its full stop; trim each field and
   collapse every internal whitespace run to a single space; join the four
   with single newline characters; hash the UTF-8 bytes with SHA-256;
   record the first twelve hex characters. The value on the first example
   above is computed by exactly this recipe and can be used as a test
   vector. A recorded fingerprint that no longer matches means **not
   approved** — that state is computed and reported by the tool, never
   written into the file. Collapsing whitespace is deliberate: a
   formatting-only edit must not un-approve a requirement; the recipe, not
   the file bytes, is the contract, and every implementation must share it
   exactly.

10. **A graveyard entry** replaces the five live fields with six:
    **Killed** (date, and what killed it — a test or an analysis),
    **Statement as proposed**, **Why it was proposed**, **Why it is dead**
    (carrying the words that killed it, verbatim under the same reserved
    form), **What was learned** (the payload — written so the next
    proposer does not re-derive the dead idea), and **Superseded by** (a
    reference, or `nothing — killed outright`). The heading gains `— DEAD`
    between reference and handle. The machine name stays. **The links are
    dropped on death:** a dead requirement tracing to a live goal would
    corrupt every coverage count. The graveyard lives under a `## Graveyard`
    heading at the end of the same document, so anyone proposing into the
    register scans past it — or the tool does — before a new requirement
    lands. The formerly open question of where the graveyard sits is
    thereby closed with the cheapest answer that makes it readable at
    proposal time; moving it later costs a cut and a paste, not a
    migration.

11. **The statement/Why boundary, decided by one test:** the Statement is
    what a build can be *rejected against* — if a clause could cause a
    difference report, it is statement content, including manner ("as a
    separate item" binds). The Why explains, evidences, and never restates
    a binding clause in other words — a guard stated in the statement is
    referenced from the Why, not repeated, because a repeat in different
    words is two texts that will drift.

12. **The derived-statement flag — DECIDED 2026-08-14 11:53**, together with
    the precedence rule below. When a statement is constructed from his words
    rather than transcribed — which happens whenever his words carry the
    requirement but are not specification prose — the label becomes
    `**Statement (derived).**` The flag says: the Why holds the authority
    here, the statement is our derivation of it, and approving this block
    is approving the derivation. Without the flag, interpretation is
    presented in the same clothes as transcription, on exactly the
    requirements where his words are all there is.

**Cost of this section, stated plainly:** the existing register's blocks do
not yet match this form and must be converged once — a mechanical pass, but a
real one. And every existing approval re-fingerprints under this recipe,
which lands on top of the migration cost already flagged for widening the
fingerprint: the two re-approval passes should be scheduled as one, so his
time is spent once, not twice.

---

## Precedence between the word list and his verbatim words — DECIDED 2026-08-14 11:53

The writing test found a genuine collision, not a gap. The adopted word list
bans totality words and vague subjects; the never-summarise law carries his
words verbatim; and his words break the word list often, because he writes
like a person and the list is written for specification prose. His G1 input —
*"a user never feels overwhelmed by the process"* — breaks it three ways in
eight words, and may not be touched.

**The proposed rule: the word list governs the Statement and never touches
quoted words inside the Why.** The statement is ours to write well, so the
linter binds it. His words are evidence, not prose under review — a linter
that flags them is asking to edit the witness. Tested against the collision
above: his sentence lives whole in the Why, the statement derives a checkable
obligation from it, and the derived-statement flag (rule 12) marks that the
derivation happened — so the act the never-summarise law worries about,
interpretation wearing transcription's clothes, is named on the page instead
of hidden.

**RULED BY TONY, 2026-08-14 11:53 — "agree".** The rule is settled and binding:
**the word list governs the Statement; quoted words inside the Why are never
linted.**

It was escalated rather than decided by the model because it settles which of
two of his own rules yields where they meet. That is the shape of question that
belongs to him, and this is what the escalation was for.

**What follows from it, so nobody re-derives it:** the writing help appears at
the Statement field and nowhere else. A quoted passage in the Why is evidence,
and evidence is not edited to read better. Where a statement is derived from
his words rather than being his words, the derivation is marked on the page —
so interpretation can never wear transcription's clothes, which is the exact
thing the never-summarise law exists to prevent.

---

## The shape — six elements

Two of the six exist for the machine and Tony never fills them in or reads
them. He writes three things: what must be true, why, and what it connects to.

### 1. Reference — the name he says out loud

A short identifier for speaking about a requirement — his ask, verbatim:
*"Reference numbers"*. Without it a requirement cannot be pointed at in
conversation, in a release list, or in an impact question, so it earns its
place against the one-field floor immediately.

**ADOPTED from ISO 29148**, whose doctrine is verbatim: *"Once assigned, the
identification is unique — it is never changed (even if the identified
requirement changes) nor is it reused (even if the identified requirement is
deleted)."* Every long-lived numbering scheme in the survey — architecture
decision records, Python proposals, internet standards — follows exactly this:
sequential, permanent, deliberately meaning-free. The survey's scale lesson:
*every scheme that encoded meaning in the identifier eventually had the meaning
change.* So the reference carries no claim that can go stale — it is a number,
not a description.

### 2. A hidden machine name — the twin he never sees

A second identifier, minted by the tooling, never shown, never spoken. Its one
job: when a requirement is edited *and* moved in the same change, the machine
can still tell "this is the same requirement, changed" from "that one was
deleted and a new one appeared".

**ADOPTED from StrictDoc**, whose documentation states that without it the tool
*"cannot reliably determine whether a node has been modified or relocated."*
The research flagged this as a **day-one trap: adopt it late and the fidelity
of every comparison is permanently degraded**, because history before the
adoption can never be reconstructed. That trap is the entire argument for
carrying it now, while the register is small — and it is the honest cost too:
every record carries a field that serves nobody in the room, purely so the
future machine can answer "what changed" truthfully. Against a one-field floor,
this survives only because omitting it is irreversible and including it costs
Tony nothing to maintain.

### 3. Statement — what must be true

The requirement itself, in his words or agreed words, one or two sentences.
This is the one element the floor itself demands — the modern specification's
single mandatory field is precisely this.

**ADOPTED from the OSLC floor**, and it carries two disciplines with it:

- **The writing help, at the field.** The ISO 29148 plain-language rules —
  no superlatives, no vague pronouns, no "and/or", no "if possible" loopholes,
  no "all / always / never" totality words; 'shall' binds, 'should' is a goal
  and is not a requirement — appear **as help where the statement is written**,
  not as a verdict afterwards. **ADOPTED** as a word list (it is normative in
  the standard and measured to work — 59% precision at 82% recall when built as
  an automated checker), **ADAPTED** in placement: every surveyed system runs
  it as a check after the writing; his call is better — *"we should have that
  as a help or listed under the field"* — because help at the field prevents
  the defect instead of reporting it, and the rule is visible at the moment it
  applies rather than discoverable by tripping over it.

- **A tracked hole is allowed, and capped.** A statement may carry an open
  marker — "to be decided: which accounts this covers" — rather than a silent
  guess. **ADAPTED from ISO 29148 and Spec Kit together.** The standard makes
  these markers first-class and closable: the set *"cannot be considered
  complete until all the TBx designated requirements have been resolved"* — so
  "none open" is a gate an approval can insist on. Spec Kit adds the part the
  standard lacks, a budget: *"LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers
  total."* Adapted by combining the two: markers are legal, **at most three
  open across the whole set**, and a statement with an open marker cannot be
  approved — because approving a hole would fingerprint a question as if it
  were an answer. This is the same refusal-to-guess as G2, given a mechanism.

### 4. Why — the reason, carrying his verbatim words

One element doing two jobs the old draft split. It holds the reason the
requirement exists, and where his own words are the reason, **it holds them
verbatim, marked as his, never paraphrased** — his law: *"never sumarize
memories or requirments or achievements etc"*.

**ADAPTED from ISO 29148's rationale attribute.** The standard makes rationale
the sanctioned home for everything that must not live in the statement — *"All
assumptions made regarding a requirement shall be documented and validated in
one of the requirement's attributes (e.g., rationale)"* — and the research
named it *the only attribute that reliably pays for itself*, because it is the
one that answers **"can we delete this yet?"** A statement says what must be
true; only the rationale says whether the reason still holds. The adaptation is
ours: the standard's rationale is prose anybody writes; ours is required, and
where the producer's words exist they are carried whole under the
never-summarise law. That fusion has no exact precedent, but each half does, so
this is adaptation, not invention.

The decision-record tradition supplies the confirming evidence from the other
direction: its practitioners found the real payload of a decision record is the
context and the rejected alternatives, *not* the decision — the decision is
visible in the artifact; the reasoning is visible nowhere else.

### 5. Links — what it serves and what it needs

Two connections, each stored in one direction only, with the reverse derived:

- **traces to** — the goal or law this requirement serves. Law 2 applied to
  requirements: one that traces to nothing does not belong —
- **unless it says so on purpose.** A requirement may declare **"no parent, by
  design"** instead of a trace. **ADOPTED from Doorstop's `derived` marker** —
  *"this has no parent, on purpose"* — which exempts an item from
  must-link-upward checking. This matters concretely: this repo holds 46
  requirements with no parent and has been treating every one as a defect. Some
  are — and some originate rather than refine, and the marker is what lets a
  checker tell the two apart instead of drowning real findings in false ones.
- **depends on** — other requirements this one needs. His ask, verbatim: *"no
  simple way for me to see the requirments and their dependencies"*.

**ADOPTED — the storage rule is the strongest convergence in the whole
survey:** all five docs-as-code tools store a link at exactly one end and
derive the reverse, because two stored ends means two records to keep
consistent and a conflict every time they touch. A link naming a requirement
that does not exist is an error that stops the run — also unanimous. The
derived reverse is not decoration: it is what answers his change-of-mind
question — *"change requirement x and the impact can be measured and planned"*
— because "what depends on this?" is the reverse direction, computed, never
maintained by hand.

**Links are inside the approval fingerprint** — settled: change what a
requirement depends on and its approval is invalidated exactly as if the words
had changed.

### 6. The approval mark — a fingerprint, not a signature

When Tony approves a requirement, the system records a fingerprint of the
**statement, the Why, and the links** as they read at that moment. The
requirement is approved for exactly as long as its current fingerprint matches
the recorded one. Change a word, a reason, or a link and the approval is
automatically no longer valid — nobody maintains a status, nobody forgets to
downgrade one, and an approval can never quietly apply to words it was not given
for.

**ADOPTED from Doorstop**, which fingerprints an item's content and reports
*"unreviewed changes"* on any mismatch — and which deliberately excludes
housekeeping details so metadata edits do not nag. **ADAPTED by his own
ruling:** Doorstop's fingerprint covers what its project chooses; ours covers
**the statement, the Why and the links, always** — *"no point doing half of the
fingerprint."*

**The Why was added to the fingerprint by Tony, 2026-08-14 09:32**, correcting a
choice the composer had made silently. Its reasoning was that a reason can gain
detail without un-saying the agreement; the correction is that **a reason can
also change what a statement means**, and if it can, an approval must not
survive an edit to it. This is his own "no point doing half of the fingerprint"
applied one element further. The composer had flagged the omission itself: *"I
applied his ruling narrowly where I could have asked."*

**What stays outside the fingerprint, deliberately:** the reference, the hidden
machine name, and everything beside the requirement — comments, notes,
attachments. Commenting must never invalidate an approval; that is unanimous
across the surveyed territory, and it is the reason those things live beside a
requirement rather than in it.

This element replaces the entire status question. What the old draft tried to
hold in a status field — is it agreed? — is computed here instead. And the
strongest finding in the standards research backs the removal: **no standard in
the territory defines a status on the requirement at all.** Two independent
enterprise vendors converged on the same shape — the *review* has a lifecycle,
the requirement does not. Approval is an event that happens *to* a requirement,
never a field carried *by* one. The two tools that did ship a status field
shipped it unenforced, which the research called *"the worst of both worlds: it
looks like a contract and isn't one."*

---

## The set is a DOCUMENT — decided 2026-08-14 09:32

The research called this a trilemma where every corner bleeds, and the earlier
draft never chose one. **Tony chose the document corner.**

**Requirements are blocks in a file you can read top to bottom.** Reading order
is meaningful and costs nothing to keep. Git carries the history. The HTML view
is generated *from* the document and stays disposable — the file is the only
writable surface, which is the one thing every tool in the survey agreed on.

**Why this corner, on the evidence:**

- **The document's known cost is rebuild speed, and it is nowhere near us.**
  StrictDoc reaches a ten-second page load at 100 documents of 100–400 nodes
  each. We have 51 requirements.
- **The database corner buys clean merges under many authors — we have one
  human and one agent.** It charges for that benefit by making you re-encode
  reading order as a field, which is precisely Doorstop's densest bug cluster.
  We would pay the cost and collect almost none of the benefit.
- **The graph corner has no reviewable narrative at all**, which fails his
  stated need outright: *"no simple way for me to see the requirments and their
  dependencies"*.

**And it is the corner we already stand in.** The register is already a document
with requirements as blocks in reading order. This confirms rather than
migrates — no conversion, no re-keying, no lost history.

**What it commits us to, stated plainly:** merge conflicts here are prose
conflicts, not field conflicts. Reordering is free. Anything that needs to
query across requirements is computed by reading the document, not by asking a
database — which is affordable at this scale and would not be at ten thousand.

**Deliberately still open:** whether it is *one* document or several, and how
the graveyard sits relative to it. Both are cheap to decide later and expensive
to guess at now.

---

## Beside the requirement, never on it

Three things the old draft put on the record that belong next to it. None of
these is an element of the shape.

**Comments and notes.** His ask stands in full: *"to add comments perhaps for
you to pick up or to record notes around the requirments"* — note his own
preposition, **around**. **ADOPTED as a discipline — it is unanimous across
the territory:** discussion lives outside the record everywhere (proposals
mandate a discussion address; decision processes keep debate in the thread and
record only a link), and the enterprise finding is the sharp version:
**comments are not field values, so commenting must never version the
requirement.** A comment on our shape must never disturb the fingerprint — a
question about a requirement must not un-approve it. So comments live beside
the record, addressable to it by its reference, and the model reads them there.

**Attachments — links and images.** His ask: *"add links or images perhaps as
input"*. **This is the one place we are on our own, and it is flagged loudly:
attachments on a requirement appear in NO surveyed system.** Not the standards,
not the tools, not the vendors. So nothing here can be justified by prior art
— only on its own terms, which are his words above. The honest reading of his
words is *input* — material that informs a requirement, not part of one. So
attachments live in the same beside-space as comments, referenced from the Why
element when one is load-bearing. What is **BUILT** is only the beside-space
itself, and it is the smallest thing that honours the ask; putting attachments
*on* the record would be building something no one in the territory has ever
needed, on no evidence.

**History.** Cut as a field entirely — see the cut list. The record's history
is the version history the repository already keeps; the research's line:
*"Git commits already give you immutable snapshots that span every file at
once — which is precisely the thing DOORS makes hard and expensive."* One
signal from the standard survives the cut, derived rather than stored: ISO
29148 values a version count as a **volatility sensor** — *"a requirement that
has a lot of change could indicate a problem or risk to the project."* That
number is computable from the repository history whenever wanted; storing it
per-record buys nothing.

---

## Considered and decided — the research's remaining offers

**Declared coverage — a requirement naming which artifact kinds must cover it.
Not now, on Jama's own arithmetic.** OpenFastTrace lets a requirement declare
"an architecture piece and a test must cover me", and completeness becomes
computed rather than asserted — genuinely the best coverage mechanism surveyed.
But it presupposes a settled set of downstream artifact kinds, and ours are not
settled — design and test artifacts do not yet exist as first-class things to
point at. The research's reason Jama is overkill applies word for word:
*"its central mechanism is schema enforcement across item types, and that
mechanism only pays when many people are producing items under a methodology
nobody can hold in their head. Two people hold the methodology in their
heads."* Declared coverage returns for consideration the day the downstream
artifact kinds exist. Deferred with that named return condition, not refused.

**Relationship rules — declaring which link shapes are required between which
kinds of thing.** Same verdict, same reason, same return condition. The idea is
worth keeping verbatim — coverage becomes *"a schema violation you can draw,
not a report you run"* — and it needs more than one kind of thing to relate.

**Two ranking dimensions — stability, and necessity as essential / conditional
/ optional.** Not now. IEEE 830's point stands — *priority is not one number*
— but nothing in the interview or the goals asks for ranking, and the pre-reset
schema had already deferred priority with the right return condition: it
returns when a release artifact exists to consume it. Adding two ranking fields
to a shape held to a floor of one, with no consumer, fails the bar twice.

**Set-level quality — five questions asked of the whole set, once.** Taken —
but as a discipline, not an element. ISO 29148 keeps two separate quality
lists: characteristics of a requirement, and characteristics of the *set*
(complete? consistent? feasible? — asked of the collection). Putting set
quality on each row is a category error; the survey's phrasing: *quality is a
property of the collection, checked once, not a question asked of every row.*
So the five set questions become a review checklist run against the whole
register at approval moments. **ADOPTED**, and it costs the shape nothing —
which is exactly why it belongs.

---

## What was cut from the nine-field draft, and why

| Old field | Verdict |
|---|---|
| **Reference** | **Kept** — element 1, now with the never-changed, never-reused doctrine attached. |
| **Statement** | **Kept** — element 3, now carrying the writing help and the capped open-markers. |
| **Status** (`DRAFT · ACCEPTED · FINAL v1.0 · v1.2`) | **Cut, by settled decision.** Approval is computed from the fingerprint; selection lives on the release. Both facts the field tried to hold — is it agreed, is it going forward — now cannot go stale, because nobody maintains them. The old draft itself had already flagged this field *"unresolved and not to be treated as settled."* What the cut does **not** yet carry is his versions want — see the straw-man. |
| **Traces to** | **Kept, merged** into element 5 — with the "no parent, by design" marker added. |
| **Depends on** | **Kept, merged** into element 5 — one-directional, reverse derived, inside the fingerprint. |
| **Source words** | **Kept, merged** into element 4. His verbatim words are now *inside* the Why, marked as his — the never-summarise law binds exactly as before; what changed is that the reason and the words carrying it are one element instead of two. |
| **Notes & comments** | **Cut from the record, honoured beside it.** Unanimous across the territory: commenting must never version the requirement. His ask is met in full — the location moved, the capability did not. |
| **Attachments** | **Cut from the record, honoured beside it.** No surveyed system has this on a requirement; the beside-space is the smallest honest answer to *"add links or images perhaps as input"*. |
| **History** | **Cut.** The repository already keeps immutable history of every change to every record at once; a per-record history field re-implements it worse and goes stale. The volatility signal the standard wanted from it is derived on demand instead. |

Nine fields in; six elements out, two of which are machine-only. The three
things Tony actually writes: what must be true, why, what it connects to.

---

## Against the schema written before the reset

The repo already carries a full requirement schema, written on 8 August —
twenty categories, five states, five link roles, hash-approved statements. The
agreed method was to draft fresh, then compare non-destructively and keep what
survives on merit. This is that comparison. **Nothing here deletes anything;
these are recommendations.**

**What it already got right, and this draft keeps:**

- **The approval fingerprint, with the source named.** It borrowed Doorstop's
  mechanism a week before the research independently recommended it, and named
  where it came from. Element 6 is the same mechanism — with one real change,
  below.
- **Refusal on divergence, never a silent rewrite.** Its rule — *"a red check
  is a question the producer answers; a silent downgrade is a decision made for
  them"* — is exactly right and is carried forward whole.
- **Typed links with registered reverses, and an unknown link target refused.**
  The research's unanimous convergence, already implemented.
- **The suspect-link stamp** — a link carrying a fingerprint of its target as
  it read when the link was made, so editing a requirement flags every
  dependent for a re-look. This is Doorstop's second staleness signal,
  independent of the first, and it directly serves *"the impact can be measured
  and planned"*. **Recommend keeping it**; the new draft's links element is
  compatible with it.
- **The no-parent allowance** — it already lets origin requirements stand
  without a parent. The fresh draft arrived at the same marker from the
  research independently, which is the comparison working as intended.
- **Views** — its insight that a fifteen-field argument was *"one model
  against one rendering"* survives untouched: how much of a requirement any
  surface shows is a rendering decision, not a shape decision.

**What it has that this shape drops (recommended, not deleted):**

- **The five-state lifecycle.** Overtaken by the settled decision: no status
  field. What each state *owed* was the valuable part, and the obligations
  survive as computed facts — "final owes a matching fingerprint" simply *is*
  element 6. The two states with no computed home — superseded, dropped — are
  raised in the straw-man rather than silently lost.
- **The required twenty-category field, and the category living inside the
  reference itself.** The research's scale lesson cuts against it: *every
  scheme that encoded meaning in the identifier eventually had the meaning
  change* — and a reference whose prefix names a category is meaning in the
  identifier. The old schema's own tag system already carries what the single
  bucket destroys. Recommend the categories become tags entirely and the
  reference goes opaque — flagged as a recommendation with a real cost: every
  existing reference would be re-minted, which is exactly the kind of identity
  change the doctrine forbids doing twice. This deserves its own decision.
- **A required free-text Source field.** Absorbed by element 4 — the Why
  carries the verbatim words themselves, which is stronger than pointing at
  where they live.

**What this adds that it lacks:** the hidden machine name (its day-one trap is
already half-sprung — adopting it now limits the damage rather than avoiding
it); the writing help at the statement; capped open-markers with "none open"
as an approval gate; a required Why; and the widened fingerprint. **The
widening carries the one real migration cost in this document, stated
plainly:** the existing fingerprints cover the statement only. The moment the
recipe grows to include links, **every one of the 51 approved requirements
diverges at once and is refused until re-approved** — and re-approval is the
producer's own work by definition, because nobody else's approval means
anything. That is a real cost in his time, flagged before it is scheduled, not
after.

---

## Findings resolved — the writing test's ten findings, each answered

The writing test produced ten findings. Each is dispositioned here as
**SETTLED** (the normative form answers it) or **PROPOSED** (a decision only
the producer can take, flagged and waiting). The test's own severity ranking
is kept.

**1 — No concrete form existed. SETTLED.** The normative form section is the
answer: field labels, order, requiredness, delimiters, heading level, and a
worked example with a computed fingerprint. The test's short handle is
adopted (rule 3), with the reasoning stated: the set is a document read top
to bottom, and meaning-free headings alone make it unreadable — the handle
carries the meaning and stays outside the fingerprint so it can go stale
harmlessly.

**2 — The graveyard entry was unwritable. SETTLED.** A dead requirement now
has a six-field entry shape (rule 10), shown rather than described, with the
learning payload as a named field so capturing it is filling in a form, not
inventing one under time pressure — the countermeasure to the
discipline-dependent-log failure this document itself diagnosed. Location is
closed: end of the same document. Links drop on death; the machine name
stays.

**3 — The reference could not be minted, and its rules conflicted. SETTLED.**
Minting is defined (rule 2): highest number across live blocks and graveyard,
plus one — the document plus graveyard is the allocation register, which is
exactly what makes never-reuse observable. The sequential/meaning-free
tension is resolved rather than denied: creation order is the one fact that
cannot change, so it is the one encoding that cannot go stale. The test
file's prefixed references are non-conformant by its own admission and are
never merged. The open-marker budget got its counter for the same root
cause: fixed syntax makes the cap countable (rule 5). What this does **not**
decide: re-minting the existing register's references to the opaque form was
already flagged as its own decision with a real cost, and it stays his.

**4 — The two machine elements were unwritable, and the fingerprint had no
recipe. SETTLED.** "Hidden" is reconciled with "the file is the only
writable surface": in the file, inside an HTML comment, invisible in every
rendered view, minted by the tool as a byproduct — never by a person (rule
4). The fingerprint has an exact recipe with a computed test vector (rule
9), and the unapproved state has a written form: `**Approval.** none` —
absence is stated, never implied. The test's guess that a dead record drops
its machine name is reversed, for the reason the test itself suspected: a
graveyard entry is precisely a record that has moved.

**5 — The word list and the never-summarise law collide. SETTLED — Tony
ruled 2026-08-14 11:53.** This was a contradiction between two of his own
rules, so the precedence was his to set, and it was escalated rather than
decided. **The linter governs the Statement and never touches quoted words
inside the Why** — his words are evidence, and evidence is not edited to
read better. It carries the derived-statement flag with it, which names the
act of interpretation the collision forces. Full reasoning in its own
section above.

**6 — The Statement/Why boundary was unreliable. SETTLED, with one edge
riding on finding 5.** The boundary test is rule 11: statement content is
what a build can be rejected against, manner included; the Why explains and
never restates a binding clause. The inversion case — where his words in the
Why are the authority and the statement is derived — is exactly what the
derived-statement flag marks, so its final shape lands with his ruling on
finding 5.

**7 — The open-marker rules were half actionable. SETTLED.** Syntax,
identity, granularity and location are all fixed in rule 5: bracketed
markers numbered per requirement, statement only, cap of three counted as
markers across the live set. The stricter reading of the cap is kept
deliberately. A doubt about a Why is not a marker — it is a comment beside
the record or the derived-statement flag.

**8 — Traces had no cardinality and no law/goal distinction. SETTLED.**
One or more targets (rule 7); secondary sources are targets, not prose.
Goal traces count toward coverage; law traces are constraint links excluded
from coverage arithmetic, because laws are obeyed, not achieved, and mixing
the two makes the number meaningless.

**9 — The derived reverse had no place to appear. SETTLED, with the cost
named.** The reverse lives in the generated view and in an on-demand impact
report, never in the document (rules preamble). The cost is real and
accepted: reading the raw file alone does not show what depends on a
requirement — the impact question is answered at change time, by the tool,
which is when it is actually asked.

**10 — His words had no machine-detectable marking. SETTLED.** One reserved
form (rule 6): inside the register, attributed italic quotation is verbatim
producer words and nothing else may use that form. The test's observation
that the Why is where the real work happens is recorded as evidence *for*
the required Why, against this document's own earlier doubt — the Why is the
element that caught a dead requirement.

**The score: eight settled, two riding on one ruling.** Findings 5 and 6's
edge both land with the same decision — the precedence rule and its
derived-statement flag — which is therefore the single thing awaiting him
from this pass.

---

## Straw-man

Law 3, both passes.

### Inward — what is wrong or missing in what I wrote

**~~The versions are not carried.~~ CLOSED by Tony, 2026-08-14 09:26:** *"we
already discounted the FINAL 1.0 etc - ignore, we use fingerprint and
lifecycle."*

**Named version numbers are dropped entirely.** They were part of an
off-the-cuff answer he later withdrew as unresearched, and nothing replaces
them: the fingerprint answers *"has this changed since we agreed it?"*, and
that is the question versions were being asked to answer.

**"Lifecycle" here means the DERIVED progression, not a restored field** — the
model's reading, recorded so it is checkable rather than assumed: approval comes
from the fingerprint, and where a requirement has reached comes from **what
links to it** (a design cites it, so it is designed; a test cites it, so it is
tested). Nothing is stored and nothing is maintained. This is consistent with
the settled decision that there is no lifecycle field, and with his own
correction that *"lifecycle is a better way vs status"* — a progression rather
than a flag. **If he meant a stored field, this reading is wrong and an element
is missing.**

*The shape therefore stands at six elements.*

**~~"Superseded" and "dropped" have no home.~~ ANSWERED by Tony, 2026-08-14
09:28:** *"we need a graveyard so we dont add them again and learn from them"*

**Two purposes, and they are different:** stop a dead requirement being proposed
again, and keep what was learned from killing it. The second is the ADR finding
in another form — the payload is the reasoning, not the verdict.

**This is the first decision made about the SET rather than about a
requirement**, which matters because the set still has no shape (see the
omission pass below).

**It has roots in this repo already, verified rather than recalled:** a standing
decision of 2026-08-03 — *"'What we ruled out, and why' is its own artifact…
A rejected approach and a failed fix are the **same thing** — an option
eliminated, one by analysis and one by a test. The unit is the **concept**, not
the attempt and not the code"* — plus an `## Archive` section already sitting
empty in the register, and a `dropped` state in the old schema that required a
reason.

**Two failure modes are already named by that same decision, and they are the
whole design problem:**

1. *"Read in GROUNDING by everything that proposes, which makes it **an input
   rather than a graveyard**."* A graveyard that is not read **at the moment
   someone proposes something** cannot stop a re-add. Storage is not the
   mechanism; retrieval at the right moment is.
2. *"Capture must be a **byproduct** — a discipline-dependent log is high impact
   + high likelihood + no countermeasure = dead."* If killing a requirement
   requires someone to remember to write the reason down, the graveyard will be
   empty exactly when it matters.

**And the reference number resolves itself:** 29148's never-reuse rule is
already adopted, so a dead requirement keeps its reference forever. The
graveyard *is* what makes never-reuse observable — the number is visibly taken,
by a thing you can read.

**~~Still to design:~~ CLOSED by the normative form, 2026-08-14:** it lives
under a graveyard heading at the end of the same document, its entry is a
six-field form shown in exact final form, and the learning payload is a named
field rather than a discipline — see rule 10 and finding 2.

**Superseded and dropped, before this ruling:** The old schema could say "this
requirement was replaced by that one" and "this was deliberately abandoned,
with the reason". With no status field, this draft cannot say either. The
research called recorded rejection *"the single most underrated feature in the
whole territory"* — and I cut the only mechanism that recorded it without
building a replacement. A deleted requirement and a rejected one currently look
identical: gone.

**~~The Why sits outside the fingerprint, and I chose that silently.~~
CLOSED by Tony, 2026-08-14 09:32 — the Why is inside the fingerprint; his
correction is recorded in the approval-mark element.** The original
admission stands below as the record of the failure mode. His
ruling named the statement and the links. I left the Why out on the logic that
the reason can gain detail without un-saying the agreement — but a rationale
edit *can* change what a statement means, and if it can, an approval survives
an edit that mattered. I applied his ruling narrowly where I could have asked.

**The beside-space is a word.** Comments and attachments "live beside the
record" — where? Read when? His ask was *"for you to pick up"*: a beside-space
the model never reads at the moments that matter fails the ask while
appearing to honour it. This is the same defect as the old draft's History
field — a load-bearing element that is currently a name.

**The omission pass — walking his words forward:** *"Reference numbers"* —
carried. *"see the requirments and their dependencies"* — carried. *"change
requirement x and the impact can be measured and planned"* — carried by the
derived reverse plus the suspect stamp. *"add comments… for you to pick up"* —
carried in name only, see above. *"never sumarize"* — carried. What **nothing
carries**: who approved (the fingerprint proves *what* was approved — the
approval line now writes his name and a date beside it, though how that line
is itself verified remains undesigned); ~~and the *set* has no shape at
all~~ — **CLOSED in two steps:** Tony chose the document corner (2026-08-14
09:32), and the normative form now shows what a block inside that document
looks like.

### What the normative form newly breaks — added 2026-08-14, the same pass inward

The form section fixed the writing test's findings and created its own
exposures. Named here so they are findable, not discovered:

- **The example references could be mistaken for allocations.** Three
  reference numbers now appear in this document that are not in the register.
  They are labelled illustrative twice, but a copy-paste into the register
  would plant a collision under a never-reuse doctrine. The checking tool's
  duplicate refusal is the countermeasure; until it exists, the label is.
- **The minting rule assumes one document.** "Highest number across live and
  graveyard, plus one" works because everything is in one file. The
  deliberately open question of one-document-versus-several now has a cost
  attached: splitting the set re-opens reference allocation, which must then
  find a new home before the split lands.
- **The cap has syntax but still no counter.** The marker cap is countable
  now and counted by nothing. Until the checking tool runs, the cap is
  exactly the unenforced contract this document warns about — that is why
  the counter is named as the tool's first duty, and it is still a promise.
- **The fingerprint recipe, not the file, is now the contract.** Whitespace
  collapsing means two implementations that disagree on any detail of the
  recipe silently disagree on what is approved. The computed test vector in
  the example is the countermeasure; one vector is thin, and a real test
  suite around the recipe is owed before a second implementation exists.
- **The handle is meaning on the record.** It will go stale, by design, and
  the design's answer — rename freely, nothing breaks — is only true while
  every tool treats the heading after the reference as decoration. A tool
  that ever parses the handle inherits the staleness the reference was built
  to avoid.

### Outward — where this falls short of the territory

**Six against a floor of one.** I have argued each element, but the honest
comparison is stark: the most negotiated specification in the field ships one
mandatory field, and I ship six, two of which serve no human. Every argument
above could be an instance of exactly the over-carrying the floor exists to
indict. The two I would defend least hard under attack: the hidden machine
name (its value is real but arrives only at a scale and edit-pattern this
register may never reach) and the required Why (the standard makes rationale
an example attribute, not a mandate — requiring it is our escalation, and a
required field that gets filled with a perfunctory sentence is worse than an
optional one filled when it matters).

**Approved-versus-built is not distinguishable, and the territory says that
exact collapse is a documented failure.** PEP keeps Accepted and Final apart
because implementation lags approval — and implementation *always* lags
approval. The decision-record tradition collapsed the two, and that collapse
is precisely its documented drift failure: decided, divergently implemented,
no record. This shape can say "agreed" and cannot say "built" — the links that
would compute "built" (satisfied-by, verified-by) exist in the old schema only
as a deferred future slice. Until they exist, we have adopted the ADR failure
mode with open eyes.

**Coverage is asserted, not computed.** OpenFastTrace computes completeness
from declarations; we deferred that with a return condition. Fair — but until
the condition fires, "every goal is covered by requirements" is a sentence
somebody says, which is the class of claim this whole system exists to
eliminate.

**The habituation evidence is not answered by anything in this shape.** The
research's sharpest finding for us: approval quality decays structurally —
measured, worsening over time — and *presentation does not create scrutiny*.
The fingerprint makes an approval precise; nothing here makes it *attentive*.
Capping what one approval may contain, logging approvals queryably, requiring
the approver to produce something beyond a yes — all structural
countermeasures the evidence recommends, none present here. This shape makes
false approval recoverable, not rarer.

---

## Open questions

Things I could not settle from his words or the evidence, and would have had
to invent. Each is a real decision awaiting him, not a doubt.

1. **What carries the named versions?** "FINAL v1.0 → v1.2" — release-side
   membership at a moment, a name minted at approval, or something else. The
   change-of-mind requirement hangs on this.
2. ~~**Where do superseded and rejected requirements go?**~~ **CLOSED,
   2026-08-14:** the graveyard, at the end of the same document, with the
   entry form shown in the normative form section — a durable record, its
   reference retained, superseded-by as a named field.
3. ~~**Is the Why inside the fingerprint?**~~ **CLOSED by Tony, 2026-08-14
   09:32:** yes — his correction is recorded in the approval-mark element,
   and the fingerprint recipe hashes it.
4. **What is the container** — partly closed: Tony chose the document
   (2026-08-14 09:32) and the normative form defines the block. **Still
   open: one document or several** — and the minting rule now attaches a
   cost to splitting, named in the straw-man.
5. **Does the writing help ever refuse, or only advise?** Still open — and
   now paired with the precedence proposal awaiting his ruling: whatever the
   help does, the proposal is that it does it to the Statement only and
   never to his quoted words.
6. **Where exactly is the beside-space, and at which moments does the model
   read it?** His *"for you to pick up"* is a reading obligation, not just a
   storage location.
7. **The precedence rule and the derived-statement flag — proposed, his
   ruling needed.** The one decision this pass explicitly leaves for him;
   the proposal and its reasoning have their own section after the normative
   form.
