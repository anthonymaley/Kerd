# Shape test 2 — five requirements written in the normative form

**This is a test artifact, not the register.** Nothing here is allocated,
approved, or binding. The references below are **not allocations** — see
finding 2. No block here is approved, because approval belongs to the producer
and cannot be written by a model.

**Written from exactly two sources:** `docs/design/requirement-shape.md` (the
format under test) and `docs/kerd-goals.md` (the approved goals and four laws).
Nothing else was read.

**Every place I had to invent something is marked inline like this:**
`<!-- INVENTION n: … -->`, and each is written up in the findings section at
the end.

<!-- INVENTION 1: the format defines a requirement BLOCK and a `## Graveyard`
     heading. It defines no document frame — no title, no preamble, no heading
     under which live blocks sit, no ordering rule. The title, this preamble,
     the `## Requirements` heading below, and the decision to order blocks by
     ascending reference are all mine. -->

---

## Requirements

### R-0901 — a change names the document it updates

**Statement.** A change that Kerd lands shall record the identity of the spec, design document, or requirement that the change updates.

**Why.** Law 2 is stated absolutely: *"so each change should result in a chnage to spec or design or requirement"*, with the scaling dial placed on ceremony rather than on truth — *"but doesnt have to be huge process"*. A change that lands without naming its governing document leaves the law unobservable: nobody can tell afterwards whether the document was updated or merely assumed to be still true, which is the silent drift Law 2 exists to prevent.

**Traces to.** Law 2

**Depends on.** none

**Approval.** none — test artifact, never submitted

<!-- INVENTION 2 (reference band): rule 2 mints "the highest number present
     anywhere in the document — live blocks and graveyard together — plus one",
     and calls the document plus graveyard "the allocation register". This file
     is not that document, and I am forbidden from reading the register, so I
     cannot mint a conformant reference. I chose the R-09xx band and labelled
     the whole file as non-allocating, mirroring the format document's own
     handling of its illustrative examples. -->

<!-- INVENTION 3 (machine name omitted): rule 1 says the machine-name comment
     "sits in an HTML comment on the line directly under the heading" and that
     absence must be written, never implied. Rule 4 says "Nobody hand-writes
     one: a writer adds a block without the comment, and the checking tool
     mints and inserts it on its next run." These cannot both be followed. I
     followed rule 4 and omitted the comment from every block. -->

---

### R-0902 — a change is classified before it is worked

**Statement.** Kerd shall classify a proposed change as fine tuning or not fine tuning before the change is worked, by putting to it the five classification questions recorded in G3, and shall classify a change that contradicts its governing spec, design document, or requirement as not fine tuning.

**Why.** G3 asks for the class by name and for the recognition of it: *"the process should allow and recognize and understand for small changes without breaking the process or cirumventing it"*. Tony supplied the classifier as questions rather than as a size threshold — *"have we already built the item and are looking to change it? does the change go agaist the spec or design or requirment? how much effort or impact is the change, how critical is the chage, are users blocked or having poor experience?"* — and the goals name question 2 as the discriminator, which is why the second clause of the statement binds separately rather than being left to judgement. The trace to Law 2 is a constraint link, not a coverage claim: classification never exempts a change from landing in its governing document.

**Traces to.** G3, Law 2

**Depends on.** R-0901

**Approval.** none — test artifact, never submitted

---

### R-0903 — who approves the document update a fine tune carries

**Statement.** The update to a spec, design document, or requirement carried by a change classified as fine tuning shall be approved by [OPEN-R-0903-1: whether the role that made the classification may also approve the update it carries, or whether that approval must come from an authority that did not make the classification], and shall in either case be approved before the change is landed.

**Why.** G3 assigns the approval to the agent roles — *"the composer or conductor roles (if we keep them) should have the approval"* — and then leaves the separation of authorities explicitly unresolved in the goals' own straw-man: *"this puts classification and approval in the same hands. If the conductor decides a change is a fine tune and also approves its spec update, the producer is out of the loop for a class of changes the conductor itself defines — and the cheap path is the one the model is under standing pressure to pick. Nothing here yet separates those two authorities."* That is the open marker above, and it is a real hole in the approved goals rather than a doubt of mine. What is not open is the timing: G3's guard — *"imagine for g3 if the design spec designer saw his font being changed without his approval....."* — binds whichever way the authority question is settled, so the second clause is stated, not marked.

**Traces to.** G3

**Depends on.** R-0902

**Approval.** none — blocked by [OPEN-R-0903-1]

---

### R-0904 — the producer can see how much process is left

**Statement (derived).** Kerd shall be able to state, at any point in a work item's journey, how many producer decisions the remainder of that journey requires, and shall present that number with each request for a producer decision.

**Why.** G1 carries a second design input added by Tony directly into the goals file: *"a user never feels overwhelmed by the process"*. The goals distinguish it from G4 precisely on aggregate versus instance — a process can be clear at every point and exhausting in total — and Tony ruled that design inputs of this kind cannot be measured after the fact: *"these are not measurement, these are inouts to design to avoid what those g1-g8 from happening, they cant be measured."* His words are therefore the authority here and the statement above is our derivation of one countermeasure from them: making the remaining weight visible before it is spent, so accumulation is a thing the producer sees coming rather than a thing he discovers by being worn down. It is marked derived because approving this block is approving that derivation, not his sentence. The secondary trace to G5 is genuine and not decorative — *"show the work, show the state, show the tools being used"* and *"Where are we in the journey? What's happening next?"* — the same count answers both, which is why it is a second target rather than prose.

**Traces to.** G1, G5

**Depends on.** none

**Approval.** none — test artifact, never submitted

<!-- Why this is my hard case: G1's second design input is the one place in the
     approved goals where the source is (a) verbatim producer words, (b) ruled
     unmeasurable by the producer himself, (c) about the process in aggregate
     rather than about any artifact a build produces, and (d) in breach of the
     adopted word list three ways in eight words. It therefore loads four of
     the format's mechanisms at once — the derived-statement flag, the
     precedence rule, rule 11's "rejectable against" test, and the goal/law
     coverage split. See findings 4 and 5. -->

---

## Graveyard

### R-0905 — DEAD — hand a subagent a summary of the requirements its step touches

**Killed.** 2026-08-14, by the plain text of G7's design input in the approved goals. Killed by analysis, not by a test.

**Statement as proposed.** Kerd shall supply a subagent working a step with a summary of the requirements that step touches, in place of the requirement text, so that a cheaper model can work the step without exceeding what it can hold.

**Why it was proposed.** It follows directly from G7's own grounding — *"make sure we're not wasting tokens by using the correct model and using the correct effort"* — and from G3's pressure against overhead, *"i dont mind robust, i just mind overhead and overwork"*. Summarising is the obvious lever: it is the cheapest way to make a small model fit a large register, and a reader arrives at it independently from G7's first half alone.

**Why it is dead.** G7's design input rules it out by name: *"never sumarize memories or requirments or achievements etc"*, and the goals gloss why it is the specific trap here — *"Summarising is the default way a model economises, and it is exactly how a requirement quietly becomes a paraphrase of a requirement."* It is harmful rather than merely wasteful because it also breaks G2: *"we shoudl ensure the spec has those memory items in the work"*, so a subagent handed a paraphrase is put back in exactly the position where guessing is available to it — the position G2 exists to make unreachable.

**What was learned.** When token cost argues for compression, the dial to reach for is **which** requirements are carried into a step, never **whether** they are carried whole. Selection is legitimate economy; summarisation is fidelity loss wearing economy's clothes. Any future requirement that reduces the volume of a record rather than the number of records is checked against that split before it is written.

**Superseded by.** nothing — killed outright.

---

## Findings — where the format did not tell me what to do

Ranked by damage if left unfixed. **Hard count of distinct pieces of notation,
structure, or convention I had to invent: 3.** They are marked inline above as
INVENTION 1–3. Everything else below is an ambiguity, a collision, or a
latent defect that did not force me to invent anything to finish the file — I
have kept those out of the count deliberately so the number stays comparable.

### 1 — A reference cannot be minted outside the register document. (Highest damage.)

**Trying to write:** the reference on the first block.

**The format says** (rule 2): *"the next reference is the highest number present
anywhere in the document — live blocks and graveyard together — plus one. The
document plus its graveyard* is *the allocation register."*

**What is missing:** the rule is total — it defines minting only for a writer
who is editing the allocation document itself. Anyone writing requirements
anywhere else (a proposal, a design doc, a test like this one, a branch that
has not merged) has no conformant way to name what they wrote. The format
document has the same problem and solved it the same way I did: it emitted
R-0101–0103 and labelled them illustrative twice, then listed "the example
references could be mistaken for allocations" as an exposure it created. That
is not a fix, it is a warning label on a defect.

**What I did:** INVENTION 2 — took the R-09xx band and banner-labelled the file
as non-allocating.

**Why it ranks first:** it is the only finding here that can put a wrong,
permanent, never-reusable identifier into a register under a doctrine that
forbids ever changing one. Every other finding costs a rewrite; this one costs
an identity.

### 2 — Rule 1 and rule 4 give opposite instructions about the machine name.

**Trying to write:** the HTML comment under each heading.

**The format says** (rule 1): *"The machine name sits in an HTML comment on the
line directly under the heading… a field that does not apply says so explicitly
(`none`), it is never omitted. Absence must be written, not implied."* And
(rule 4): *"Nobody hand-writes one: a writer adds a block without the comment,
and the checking tool mints and inserts it on its next run."*

**What is missing:** which of the two a human writer follows. Rule 1's
requiredness plus its worked example (every example block carries a comment)
reads as "write one"; rule 4 reads as "never write one". They cannot both hold
for the same writer at the same moment.

**What I did:** INVENTION 3 — followed rule 4, omitted every comment. I believe
this is the intended reading, but "I believe" is the problem: the format let me
choose.

**Damage:** moderate, and self-limiting once the checking tool exists — but the
tool does not exist, so today every block in the register is in an
unresolvable state with respect to its own format.

### 3 — The word list collides with the absoluteness of the laws, and the precedence rule does not reach the collision.

**Trying to write:** R-0901's statement, which derives from a law the goals call
absolute.

**The format says:** the word list bans *"no 'all / always / never' totality
words"*, and it governs the Statement — that part is ruled and settled:
*"the word list governs the Statement; quoted words inside the Why are never
linted."*

**What is missing:** the settled precedence rule resolves the word list against
**his quoted words**. It does not resolve the word list against **the content of
the laws**, which is a different collision in our own prose. Law 2 is absolute
by ruling — *"The law is absolute; the ceremony is proportionate"* — and G3's
goals text says the alternative *"decay[s] into 'significant changes only' — a
judgement call, and therefore a hole."* A statement deriving from an absolute
law has to say the law applies to every change, and the natural word for that
is banned. Writing the weaker word is exactly the decay the goals name.

**What I did:** wrote *"A change that Kerd lands shall…"*, using an indefinite
subject to carry universal quantification without a totality word. That is a
standard specification-writing technique and it works, but nothing in the
format teaches it, and a writer who does not know it will either break the word
list or weaken the law. **I did not count this as an invention** — it is a
sentence construction, not a piece of notation or structure added to the
document. It is a documentation gap, not a hole I had to fill with new
machinery.

**Damage:** high in aggregate, low per instance. It will produce quietly weaker
statements over time, which is precisely the failure that is hardest to detect
by review.

### 4 — Rule 11's Statement/Why test is reliable everywhere except where the source is unmeasurable, which is where I most needed it.

**Trying to write:** R-0904, from G1's *"a user never feels overwhelmed by the
process"*.

**The format says** (rule 11): *"the Statement is what a build can be* rejected
against *— if a clause could cause a difference report, it is statement
content, including manner… The Why explains, evidences, and never restates a
binding clause in other words."*

**Verdict, honestly: the test worked on four of my five blocks and I did not
hesitate once.** On R-0901, R-0902, R-0903 and R-0905 the line was obvious, and
the "never restate a binding clause" half is a genuinely good rule — it stopped
me repeating G3's guard in R-0903's Why, which is the drift it is built to
prevent.

**Where it fails:** the goals contain design inputs the producer ruled cannot be
measured — *"they cant be measured"*. Rule 11 asks what a build can be rejected
against; if nothing can, then by rule 11 **there is no statement content at
all**, and the requirement cannot exist in this format. The format's answer is
the derived-statement flag, which marks *that* a derivation happened but says
nothing about whether the derivation is faithful or whether a different
countermeasure would serve the same words equally well. I picked one
countermeasure out of several available ones and flagged it. A reviewer
approving R-0904 is approving my choice among unstated alternatives, with the
alternatives nowhere on the page.

**What I did:** used `**Statement (derived).**`, and put the honest weakness in
an HTML comment beside the block rather than in the Why — because rule 11 bans
it from the Why and rule 5 bans it from being a marker.

**Damage:** high on exactly the requirements that matter most — the ones
carrying his design inputs, which are the reason the goals file exists.

### 5 — The derived flag has an undefined interaction with the fingerprint recipe.

**The format says** (rule 9): *"strip each bold label and its full stop"*.
(Rule 12): the label becomes `**Statement (derived).**`

**What is missing:** whether "the bold label" means the whole of
`**Statement (derived).**` or only `**Statement.**`, leaving a stray
`(derived)` at the head of the hashed text. The two readings produce different
fingerprints for identical content. The format itself names this class of
defect as its own worst exposure: *"two implementations that disagree on any
detail of the recipe silently disagree on what is approved."* There is exactly
one published test vector and it is a non-derived block, so the vector cannot
discriminate between the readings.

**What I did:** nothing — no block here is approved, so I never had to choose.
This is latent, not encountered.

**Damage:** high the day a derived statement is approved; zero until then.
Cheap to fix now (one sentence and a second test vector), expensive later
(re-approval).

### 6 — The open-marker cap has no defined scope outside the register.

**The format says** (rule 5): *"The cap is at most three markers — counting
markers, not requirements — across the live set; the graveyard never counts."*

**Verdict: the rules were actionable, including the cap, with one gap.** Syntax,
numbering, the statement-only restriction, the forced approval line, and the
"a doubt about a Why is not a marker" exclusion all told me exactly what to do,
and I used them without hesitation — the exclusion in particular stopped me
turning my doubt about R-0904 into a marker, which is the rule working.

**The gap:** "the live set" is undefined for a document that is not the
register. Do this file's markers count against the register's three? If yes, a
test file can exhaust the producer's budget. If no, the cap is trivially
evadable by writing requirements in a second file. I used one marker, so the
question was academic in practice, but it is not academic in principle.

**What I did:** wrote one marker and assumed the strict reading (that it would
count). I did not count this as an invention because the assumption changed
nothing I wrote.

**Damage:** low now, moderate the moment "one document or several" is decided —
the format already flags that the minting rule assumes one document; the cap
assumes it too, and that second dependency is not currently written down.

### 7 — Graveyard writability, and one genuinely missing field.

**Verdict: yes, the graveyard entry was writable from the format alone**, and it
was the *easiest* block in this file to write. Rule 10 names all six fields, the
worked example shows the exact shape, the `— DEAD` heading modifier is
specified, links-drop-on-death is specified, machine-name-stays is specified,
and `nothing — killed outright` is given as a literal. Naming **What was
learned** as a field rather than a discipline is the thing that made it work:
I filled in a form instead of remembering to be thoughtful, which is exactly
the byproduct-capture argument the format makes for itself. It holds.

**The one gap:** a graveyard entry has no approval line and no equivalent, so
**nothing records who authorised the kill**. `**Killed.**` records the date and
what killed it (a test or an analysis) but not who agreed. Under a format whose
whole approval theory is that a fingerprint proves what was agreed, killing a
requirement — which is a change to the set, and therefore a change that Law 2
and G1 both reach — is the one act with no approval mechanism at all. I killed
R-0905 on my own authority as a model, and the format gave me no field in which
to disclose that. I disclosed it in the file banner instead.

**Damage:** moderate. It is a hole in the approval theory rather than in the
notation, and it is cheap to close.

### 8 — His-words marking and the trace rules were followable without incident.

Recording the negatives, since a format test that only reports failures is
itself miscalibrated:

- **Rule 6 (reserved form for his words)** was unambiguous and I used it
  throughout. Knowing that attributed italic quotation means verbatim producer
  words and nothing else made the Why sections easy to write and, I expect,
  easy to check mechanically.
- **Rule 7 (traces)** gave me cardinality, the comma separator, the goal/law
  coverage split, and the instruction that a genuine secondary source is a
  second target rather than prose. R-0902 (`G3, Law 2`) and R-0904 (`G1, G5`)
  both landed without a decision to make. The coverage split is a good rule and
  I would not have derived it.
- **Rule 8 (depends on)** was trivial and correct.
- **The fingerprint recipe is exactly followable.** I implemented it from the
  text alone — four fields in order, labels stripped, whitespace collapsed,
  newline-joined, SHA-256, first twelve hex — and reproduced the published
  vector `cf543030e4e7` on the first attempt with no guessing. That is the
  single strongest part of this format, and finding 5 is the only crack in it.

### 9 — Note on the forbidden file, since the brief asked.

I did not read `docs/requirements/shape-test.md` or any of the other named
files. The temptation was real and specific at exactly one moment: choosing the
hard case in requirement 5, where I caught myself reasoning about what an
earlier run would *probably* have picked in order to avoid it — which is a
weaker version of the same contamination. I resolved it by picking on the
merits and writing down why in an HTML comment beside R-0904, so the choice is
auditable rather than asserted. Worth flagging as a property of this test
design: "do not pick what they picked" is itself an instruction that invites
modelling the other run.

---

## Verdict

**Yes, this format holds up in practice.** I wrote five real requirements,
including a dependency chain, an open-markered block, a derived statement, and
a graveyard entry, and I invented **three** things to do it — a document frame,
a reference band, and a resolution of one internal contradiction. Two of those
three are artifacts of writing *outside* the register rather than defects in
the block format itself. The block format — six fields, fixed order, fixed
delimiters, reserved quotation form, exact fingerprint recipe — did what a
normative form is supposed to do: it stopped me making decisions.

The parts I expected to be hardest were not. The graveyard entry was the
easiest block in the file. The fingerprint recipe reproduced its own test
vector on the first attempt. The Statement/Why boundary held on four blocks out
of five without a moment's hesitation.

**The single change that would most improve it: define reference minting for a
writer who is not editing the register.** Everything else in this findings list
costs a rewrite. This one costs an identity, under a doctrine that forbids ever
changing one — and the format document has already sprung the trap on itself
once, emitting three illustrative references and then listing "the example
references could be mistaken for allocations" as a known exposure with a
warning label for a countermeasure. A minting rule that only works inside one
file is not yet a minting rule; it is the happy path of one.
