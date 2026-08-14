# Shape test — five requirements written in the draft shape

**What this file is.** A test of `docs/design/requirement-shape.md`, written by an
agent given exactly two inputs: that document and `docs/kerd-goals.md`. Nothing
else in the repo was read — no existing register, no prior art, no catalog. The
point of that constraint is to find out whether the shape is writable by someone
who has the format and the goals and nothing else.

**These requirements are not proposed for approval.** They are real — each derives
from an approved goal or law — but they exist here to stress the format. The
findings section below is the actual deliverable.

**Nothing here is approved.** The shape says approval is a fingerprint Tony
records; no fingerprint is recorded for any entry below, so by the shape's own
logic none of them is approved.

---

## Notation used in this file — INVENTED, see Finding 1

The shape document describes six elements in prose and never shows a requirement.
Every syntactic choice below is mine:

```
### <reference> — <short handle>
<!-- machine: <hidden machine name> -->

**Statement.** …
**Why.** …
**Traces to.** …            (or: **No parent, by design.** …)
**Depends on.** …           (or: **Depends on.** none)
**Approval.** …
```

The short handle after the reference is also mine. The shape says the reference
is "the name he says out loud" and is deliberately meaning-free — which leaves a
requirement with no human-readable name at all. A file of `ST-0001 … ST-0005`
headings is unreadable top-to-bottom, and the shape's own settled decision is
that the set is **a document you read top to bottom**. So I added a handle. It is
outside the fingerprint, on the same logic that keeps the reference outside.

---

## 1 — The plain one

### ST-0001 — spec lives in the user's repo
<!-- machine: 019f3c2a-7d41-7b0e-9a55-1c8f0b6e4d22 -->

**Statement.** Kerd shall write the agreed spec for a work item to a file inside
the repository that holds the work item.

**Why.** Law 1 makes the repository the boundary of a project, and Tony ruled on
it directly rather than as a preference: *"the way i work, every project has its
own repo, its non negotiable."* A spec held anywhere else — a central Kerd store,
a vault, a service — puts the agreement outside the boundary the producer treats
as absolute, and separates the spec from the git history that the shape document
already relies on for versioning.

**Traces to.** Law 1.

**Depends on.** none.

**Approval.** Not approved — no fingerprint recorded.

---

## 2 — The one with real dependencies

### ST-0002 — done is checked against the spec, difference by difference
<!-- machine: 019f3c2a-7d41-7b0e-9a55-2f10c3a75e88 -->

**Statement.** Before Kerd reports a work item as done, it shall compare the built
artifact against the agreed spec and report each difference it finds as a separate
item.

**Why.** G6's design input, his words: *"we have a spec and the measurement of
done is clear, should not look different or behave differt fromt he agreed
spec"*. The goal note sharpens what that demands — the check runs *while it runs*:
*"design UI/UX etc needs to be part of the pre build and measurable by the model
during build"*. Reporting differences one at a time rather than as a verdict is
G5 applied to the check itself (*"show the work"*) and is what makes a failed
check something the producer can act on instead of a rejection to argue with.

**Traces to.** G6.

**Depends on.** ST-0001. There is nothing to compare an artifact against until
the agreed spec exists in a known location in the same repository.

**Approval.** Not approved — no fingerprint recorded.

> **Reverse links, derived, not stored** (shown here because the shape says the
> reverse *"is what answers his change-of-mind question"* — I am showing what a
> reader would need to see, not storing it):
> ST-0001 is depended on by ST-0002. G6 is traced to by ST-0002.
>
> The shape does not say where a derived reverse is *displayed* in a document-
> shaped register. See Finding 4.

---

## 3 — The one that cannot be finished yet

### ST-0003 — how a fine tune moves through the process
<!-- machine: 019f3c2a-7d41-7b0e-9a55-3a72d90f16b4 -->

**Statement.** A change classified as fine tuning shall reach a landed spec update
by **[TBD-1: whether fine tuning is a dedicated path of its own, or a rapid
traversal of the normal path]**, and shall in either case land its change in the
governing spec with the approval of the role that owns it.

**Why.** G3's design input names the class and the guard in his words: *"the
process should allow and recognize and understand for small changes without
breaking the process or cirumventing it… but also not let these small changes
break the design spec or the archtecure or requirments without agreed change"*.
The goals then state plainly that the shape of the path is unchosen: *"Two
candidate designs are floated in his words and **neither is chosen**: a dedicated
process for fine tuning, or rapid traversal of the normal path from first step to
last. That choice is design work."* It is listed again as open question 1 in the
goals. The second half of the statement is not open — G3's guard and Law 2 both
bind whichever path is picked — so the hole is scoped to the mechanism, not to
the obligation.

**Traces to.** G3.

**Depends on.** none.

**Approval.** **Cannot be approved while TBD-1 is open.** The shape: *"a statement
with an open marker cannot be approved — because approving a hole would
fingerprint a question as if it were an answer."*

**Open markers in this file: 1 of the 3 allowed across the whole set.** I cannot
verify the budget — see Finding 3.

---

## 4 — The dead one

## Graveyard

**Structure of this section is INVENTED.** The shape says a graveyard is needed
and names its two purposes and one constraint; it specifies no fields, no
location, and no entry format. See Finding 2, which is the worst finding in this
file.

### ST-0004 — DEAD — effort threshold below which the spec need not change

**Killed:** 2026-08-14, by the plain text of Law 2 in the approved goals. Not
killed by a test; killed by analysis.

**Statement as it was proposed.** Kerd shall define an effort threshold, and a
change falling below it shall land without an update to its governing spec,
design, or requirement.

**Why it was proposed.** It follows directly from the pressure G3 names — *"i dont
mind robust, i just mind overhead and overwork"* and *"Hey, can we change the font
on the screen?… It doesn't take us one hour to go through a process"*. A threshold
is the obvious, cheap way to honour that, and it is the design a reader arrives at
independently from G3 alone.

**Why it is dead.** The goals rule it out by name, and rule out the reasoning that
produces it. Tony: *"but doesnt have to be huge process"* — and the goals record
what that does **not** mean:

> The model's straw-man was that enforcing this on trivia manufactures the
> overhead G3 exists to prevent — so there must be a threshold below which the law
> does not apply. **There isn't one. The law is absolute; the ceremony is
> proportionate.**

And the reason the threshold is not merely unnecessary but harmful:

> That distinction is what keeps Law 2 from decaying into "significant changes
> only" — a judgement call, and therefore a hole.

**What was learned, so the next proposer does not re-derive it.** The instinct
behind this requirement is correct and the mechanism is wrong. When cost pressure
argues for an exemption, the dial to reach for is **the ceremony**, not **whether
the document stays true**. Any future requirement that proposes scaling process by
size must be checked against that split before it is written. G3 question 2 —
*"Does the change go against the spec, design, or requirements?"* — is the
sanctioned discriminator, and it is about *direction*, not *size*; a size
threshold is a different mechanism wearing the same clothes.

**Supersedes / superseded by.** Not superseded. Killed outright. The live
requirement covering this territory is ST-0003, which reaches the same speed by
proportionate approval rather than by exemption.

**Reference is retained forever.** ST-0004 will never be reused (ISO 29148
never-reuse, adopted in element 1). This entry is what makes that observable.

---

## 5 — The hard case

**Why I picked this one.** It is the requirement where the shape's own writing
rules and the never-summarise law point in opposite directions, and where the
goals forbid the usual escape hatch. G1's second design input was typed into the
goals file by Tony himself. It is (a) non-functional, (b) about a *cumulative*
property no single step exhibits, (c) unmeasurable **by ruling** — the goals
explicitly reject metrics: *"these are not measurement, these are inouts to design
to avoid what those g1-g8 from happening, they cant be measured"* — and (d)
phrased in a totality word the shape's adopted word list bans. Any one of those
would stress the format. Together they are the worst case I can construct from
real material.

### ST-0005 — the process does not accumulate into a burden
<!-- machine: 019f3c2a-7d41-7b0e-9a55-4c9d2e6b80f1 -->

**Statement.** Kerd shall present the producer with a single running view of the
whole process — the stages passed, the stage in hand, the stages remaining, and
what each remaining stage will ask of him — and shall not require an approval from
him at a stage whose inputs are already agreed.

**Why.** Tony's design input, verbatim and his, added directly into the goals file
2026-08-13 18:30: *"a user never feels overwhelmed by the process"*. The goals then
say precisely what makes this different from G4: *"A process that is clear at every
point and exhausting in aggregate fails G1 even though no single gate failed."*
Since the failure is cumulative, it cannot be prevented at any single gate; the
only things a requirement can bind are the producer's *visibility of the whole* and
the *total count of demands made on him*. Those two are what the statement above
binds, and they are my derivation, not his words — his words are the failure to be
prevented, quoted above. The supporting inputs are G5's *"show the work, show the
state, show the tools being used"* and G3's *"a stage whose inputs are already
clear passes instantly."*

**Traces to.** G1.

**Depends on.** none.

**Approval.** Not approved — no fingerprint recorded.

**Flagged for the producer:** the statement above is a construction, not a
transcription. If the derivation from *"a user never feels overwhelmed"* to *"one
running view, and no approval at an already-agreed stage"* is wrong, the statement
is wrong and the Why still holds. This is the case where the Why is load-bearing
and the statement is the derived part — the reverse of the usual reading. See
Finding 6.

---

# Findings — where the format did not tell me what to do

Ranked by damage if left unfixed. Damage means: how wrong the register gets, how
soon, and whether it is recoverable.

---

## Finding 1 — SEVERE. There is no concrete form. The shape is six arguments, not a template.

**What I was trying to write.** The first requirement. Any requirement.

**What the format says.** It describes six elements in careful prose — *"### 3.
Statement — what must be true / The requirement itself, in his words or agreed
words, one or two sentences"* — and argues each one against a one-field floor with
ADOPTED/ADAPTED/BUILT provenance. It never shows a requirement. There is a
straw-man section and an open-questions section; neither contains an example. The
closest it comes is *"Requirements are blocks in a file you can read top to
bottom."*

**What was missing.** Everything between "six elements" and a file on disk. No
field labels. No ordering of elements within a block. No heading level. No
statement of whether the reference is a heading or a field. No delimiter between
requirements. No indication whether the elements are markdown, YAML frontmatter,
HTML comments, or a table. The document settles the *container* question (a
document, decided 2026-08-14 09:32) and then does not say what a block inside that
document looks like.

**What I did.** Invented the entire notation, documented at the top of this file:
`### <reference> — <handle>` as the block heading, bolded field labels in a fixed
order, `---` between blocks, an HTML comment for the machine name. I also invented
the short handle, which is a seventh thing on the record.

**Damage if unfixed.** Two people writing against this document produce two
incompatible registers, and neither is wrong. Every downstream tool — the
fingerprint checker, the link validator, the reverse-link deriver, the open-marker
counter — needs to parse this, and none of them can be specified until the form
is. This is the finding that blocks everything else: five of the nine findings
below are downstream of it.

**Note on why this may be invisible from inside.** The document says *"it is the
corner we already stand in… The register is already a document with requirements
as blocks in reading order."* If a form already exists in the repo, the shape
document inherits it silently. To a reader who has the shape and not the register
— which is the case this test was constructed to simulate — that inheritance is
invisible and the form is simply absent.

---

## Finding 2 — SEVERE. The graveyard entry was not writable from the format. I built it.

**What I was trying to write.** Requirement 4, the dead one.

**What the format says.** In the straw-man, answered by Tony: *"we need a
graveyard so we dont add them again and learn from them"*. It then gives two
purposes — *"stop a dead requirement being proposed again, and keep what was
learned from killing it"* — one constraint — *"a dead requirement keeps its
reference forever"* — two named failure modes — retrieval-at-proposal-time, and
*"Capture must be a **byproduct**"* — and closes with: *"**Still to design:** where
it lives, and what makes it readable at proposal time rather than at archaeology
time."* The container section adds: *"**Deliberately still open:** … how the
graveyard sits relative to it."*

**What was missing.** A dead requirement has no specified shape at all. Concretely,
I could not determine, and had to decide: whether a graveyard entry keeps the six
elements or has its own set; whether a dead requirement keeps its Why or gains a
second one; whether "why it is dead" is a field or prose; whether the links
survive death (does ST-0004 still trace to G3? I dropped the trace, on the
reasoning that a dead requirement serving a live goal would corrupt any coverage
count — that reasoning is mine); whether "superseded by" is a link role, given
that element 5 defines exactly two roles and this is a third; whether the killing
date and killing authority are recorded, given that the shape cut History as a
field and cut Status entirely; and where the graveyard physically sits relative
to the live document.

**What I did.** Invented a seven-part entry: killed-when-and-by-what, statement as
proposed, why it was proposed, why it is dead (with the quotes that killed it),
what was learned, supersedes/superseded-by, reference-retained. I put it under a
`## Graveyard` heading in the same file. Every part of that is mine.

**Damage if unfixed.** Higher than it looks, for a reason the format itself
supplies. It names the failure mode — *"a discipline-dependent log is high impact
+ high likelihood + no countermeasure = dead"* — and then leaves the graveyard as
a discipline-dependent log, because with no specified entry shape, killing a
requirement well requires the killer to invent a good entry in the moment. The
format diagnoses the disease and does not take the cure. The learning payload is
also the part most likely to be dropped under time pressure, and it is the part
the format says is the actual point.

**One thing that did work.** The never-reuse doctrine paid off exactly as the
format predicts — *"The graveyard *is* what makes never-reuse observable"*. That
line was directly actionable and I acted on it without inventing anything.

---

## Finding 3 — SEVERE. The reference cannot be minted correctly by a first-time writer, and the rules for it conflict.

**What I was trying to write.** The identifier on ST-0001.

**What the format says.** *"Once assigned, the identification is unique — it is
never changed (even if the identified requirement changes) nor is it reused (even
if the identified requirement is deleted)"*, and the scale lesson: *"every scheme
that encoded meaning in the identifier eventually had the meaning change. So the
reference carries no claim that can go stale — it is a number, not a description."*
It also says references should be *"sequential"*.

**What was missing, in three separate ways.**

*Uniqueness has no register.* Never-reuse is a property of an allocation, and the
format never says where the allocation lives or how a writer finds the next free
number. It mentions "51 requirements" and "46 requirements with no parent" in
passing, so numbers are clearly already taken — I have no way to know which, and
under this test's constraint no way to look. Any number I pick may collide, and a
collision under a never-reuse doctrine is unrecoverable by renumbering, because
renumbering is the thing the doctrine forbids.

*"Sequential" and "meaning-free" are in tension.* A sequence position is
information — it says "I was created 40th", which is exactly a claim that a later
insertion or a re-import can make false, and it is the same class of thing the
scale lesson indicts. The format asserts both properties in the same paragraph
without noticing.

*I violated the rule I was given, knowingly.* I prefixed with `ST-` for "shape
test", which encodes meaning in the identifier — precisely what the format
forbids, and what it recommends re-minting the existing references to eliminate.
I did it because the alternative was to guess into a live allocation. That is a
worse outcome than a flagged violation, but it means this file's references are
not conformant and must not be merged into a real register as they stand.

**What I did.** `ST-0001` through `ST-0005`, sequential within this file, flagged
non-conformant here.

**Damage if unfixed.** Reference collision in a scheme whose central promise is
that references never move. The failure is silent at write time and permanent
once committed.

**Related, same root.** The open-marker budget is *"at most three open across the
whole set"* — a set-level constraint that no writer of a single requirement can
check without reading the whole set. I used one marker and stated that I could not
verify the budget. If two are already open elsewhere, I have breached a cap
without any way of knowing it. A cap needs a counter, and the format specifies the
cap and not the counter.

---

## Finding 4 — HIGH. The two machine-only elements are unwritable by hand, and the document decision makes that a contradiction.

**What I was trying to write.** Element 2, the hidden machine name, on every block.

**What the format says.** *"A second identifier, minted by the tooling, never
shown, never spoken."* And separately, settled: *"the file is the only writable
surface, which is the one thing every tool in the survey agreed on."*

**What was missing.** Those two statements collide. If the file is the only
writable surface, the machine name must be *in the file* — and then it is shown,
to anyone reading the file top to bottom, which the same document says is how the
register is read. The format never says who mints it when a human adds a
requirement by typing into a markdown file, which is the only mechanism the
document currently provides. Nor does it say the format of the value.

**What I did.** Put a UUIDv7-shaped value in an HTML comment on each live
requirement, so it is in the file and invisible in a rendered view. I minted the
values myself, which is exactly what *"minted by the tooling"* says should not
happen. I omitted it entirely on the graveyard entry, on a guess that a dead
record no longer needs move-versus-delete detection — a guess I cannot defend and
which may be backwards, since a graveyard entry is precisely a record that has
*moved*.

**The same problem, worse, on element 6.** The fingerprint is described by its
semantics — *"records a fingerprint of the statement, the Why, and the links as
they read at that moment"* — and never by its recipe. No hash algorithm, no
canonicalisation (is whitespace significant? is the field label part of the
input? are the links hashed as text or as resolved references?), no storage
location, no format. Two conformant implementations will disagree, and disagreement
means spurious mass un-approval — which the format already flags as the one real
migration cost. More basically: the format defines what *approved* means and never
defines what *unapproved* looks like on the page. I invented `**Approval.** Not
approved — no fingerprint recorded`, i.e. absence-means-unapproved. That is a
reasonable default and it is mine.

**Damage if unfixed.** Every record carries two fields that no writer can produce
correctly, and one of them is the field the whole approval mechanism rests on.

---

## Finding 5 — HIGH. The plain-language word list and the never-summarise law contradict each other, and the format gives no precedence rule.

**What I was trying to write.** ST-0005, the hard case.

**What the format says.** In element 3: *"no superlatives, no vague pronouns, no
'and/or', no 'if possible' loopholes, no 'all / always / never' totality words"*,
adopted as normative and shown as help at the field. In element 4: the Why *"holds
them verbatim, marked as his, never paraphrased"* — his law, *"never sumarize
memories or requirments or achievements etc"*.

**Where they collide.** Tony's design input for G1 is *"a user never feels
overwhelmed by the process"*. That is a totality word ("never"), a vague subject
("a user"), and a subjective predicate ("feels overwhelmed") — three violations of
the adopted word list in eight words. The verbatim law says I may not touch it.
The word list says the statement may not contain it.

The format does resolve the *location* — verbatim words live in the Why, and the
word list is attached to the Statement — so on a literal reading there is no
conflict. But that resolution has a consequence the format does not acknowledge:
**it means the requirement's binding content and its authoritative wording are
never the same text.** The statement is always a derived construction whenever the
producer's own words break the style rules, and his words break them often, because
he writes like a person and the word list is written for specification prose. Under
G7 that derivation is the exact operation the never-summarise law exists to
forbid — I did not summarise, but I did *interpret*, and the format has no name for
that act and no gate on it.

**What I did.** Wrote a constructed statement, kept his words whole in the Why, and
added a **Flagged for the producer** note saying the statement is a derivation and
naming what would be wrong if the derivation is wrong. The flag is my invention.
The format has no mechanism for "this statement is inferred from the Why rather
than taken from it", and after Finding 6 I think it needs one.

**Damage if unfixed.** Silent interpretation of the producer's words, presented in
the same shape as transcription, on exactly the requirements that matter most —
the non-functional ones where his words are all there is.

**A second collision inside the same rule.** *"'shall' binds, 'should' is a goal
and is not a requirement."* Applied strictly, requirements derived from G-goals
are awkward: the source is stated as an aspiration and the requirement must be
stated as a binding. That translation is a judgement call made once per
requirement, and the format offers no worked example of doing it well. My ST-0005
statement is my best attempt and I am not confident in it.

---

## Finding 6 — HIGH. I could not reliably tell what belongs in the Statement versus the Why.

**Direct answer to the question asked: no, not reliably.** The boundary held for
ST-0001 and ST-0002 and broke on ST-0003 and ST-0005.

**What the format says.** Statement: *"what must be true… one or two sentences"*.
Why: *"the reason the requirement exists"*, and the sanctioned home for
everything that must not live in the statement — *"All assumptions made regarding a
requirement shall be documented and validated in one of the requirement's
attributes (e.g., rationale)"* — with the test *"can we delete this yet?"*

**Where the line failed.**

*Scope.* ST-0002 says differences are reported *"as a separate item"*. Is
per-item reporting part of what must be true, or is it the reason the check is
useful? I put it in the statement and justified it in the Why. Both readings are
defensible and the format does not decide it. Generally: any requirement whose
statement includes a *manner* has this ambiguity, and most non-trivial
requirements include a manner.

*Constraint versus reason.* ST-0003's second clause — the change still lands in
the spec with the owner's approval — is G3's guard. A guard is a constraint on
what must be true, so it belongs in the statement; it is also the reason the fast
path is safe, so it belongs in the Why. I put it in both, in different words,
which is duplication the format does not sanction and which will drift.

*Inversion.* ST-0005 is the real break. The Why contains the authoritative,
producer-authored, never-to-be-paraphrased content; the statement is my
construction from it. That is the reverse of the assumed relationship, where the
statement is the load-bearing part and the Why supports it. The fingerprint covers
both, so this is not an approval hole — but every human and machine reading
convention in the document ("the statement is the requirement") is upside down for
this record, and the format has no way to say so. Hence my invented flag.

**Damage if unfixed.** Inconsistent placement across the register, which corrupts
anything that reads statements as the requirement — coverage counts, the writing
checker, and any generated view.

---

## Finding 7 — MEDIUM. The open-marker rules are partly actionable, and the missing parts are the ones a writer hits first.

**Direct answer: about half.** Three things worked with no invention. Three things
I had to decide.

**Actionable as written.** (a) That a marker is legal at all — *"A statement may
carry an open marker… rather than a silent guess"* — is clear and was directly
usable. (b) The approval consequence is unambiguous and I applied it verbatim:
*"a statement with an open marker cannot be approved."* (c) The purpose is clear
enough to judge a candidate against, so I could confirm that G3's undecided path
is a genuine hole rather than a manufactured one.

**Not actionable.** *Syntax.* The document shows two different forms in two places
— its own prose example *"to be decided: which accounts this covers"* and Spec
Kit's *"[NEEDS CLARIFICATION]"* — and adopts neither. I invented `[TBD-1: …]`.
Since the cap is a count, the marker must be machine-countable, so its syntax is
load-bearing, not cosmetic.

*Identity.* A cap of three implies counting, and counting across a document
implies markers are distinguishable. I numbered mine `TBD-1`. Whether numbering is
per-file, per-register, or per-requirement is unspecified, and it interacts with
the reference-allocation problem in Finding 3 in the same way.

*Granularity.* Is the cap on markers or on requirements-carrying-markers? A
statement with two holes — mine nearly had two — is one requirement and two
markers. I read it as markers, since that is the stricter reading and the Spec Kit
source counts markers.

*Location.* Element 3 attaches markers to the statement. Nothing says whether a
Why may carry one. ST-0005's Why contains a genuinely unresolved question (is my
derivation right?) which I expressed as an unmarked prose flag rather than a
marker, precisely because I could not tell whether that was legal, and because
making it a marker would have consumed budget.

**Damage if unfixed.** Bounded — the important rule (no approval over a hole) works
today. But the cap is unenforceable without syntax, and an unenforceable cap is the
thing the format itself calls *"the worst of both worlds: it looks like a contract
and isn't one."*

---

## Finding 8 — MEDIUM. `traces to` has no cardinality, and no rule for tracing to a law.

**What I was trying to write.** ST-0001's trace.

**What the format says.** *"**traces to** — the goal or law this requirement
serves."* Singular noun; nothing about multiples. The no-parent marker is
specified for the zero case.

**What was missing.** ST-0001 serves Law 1 primarily and G6 secondarily. ST-0002
serves G6 and draws real content from G5. ST-0005 traces to G1 and leans on G5 and
G3. I recorded one parent each and buried the others in prose, on the guess that
the singular noun is deliberate and that a single parent keeps coverage countable.
That guess is invisible to any future coverage computation — the secondary
relationships are now unqueryable prose, which is exactly the class of loss the
links element exists to prevent.

Separately: the format lists laws and goals as equivalent trace targets, but the
goals file says laws *"are obeyed, not achieved"*. A requirement tracing to an
obeyed law is a different relationship from one tracing to an achieved goal — the
first is a constraint the requirement must not violate, the second is an outcome
it contributes to. Coverage arithmetic over the two mixed together will not mean
anything. The format does not distinguish them.

**Damage if unfixed.** Coverage becomes uncountable or wrong, in a system whose
own outward straw-man already concedes *"Coverage is asserted, not computed."*

---

## Finding 9 — MEDIUM. The derived reverse is specified as a computation and not as a place.

**What I was trying to write.** The reverse of ST-0002's dependency, so that a
reader of ST-0001 can see what breaks if ST-0001 changes.

**What the format says.** The storage rule is unambiguous and I followed it
without difficulty — one end stored, reverse derived, *"never maintained by
hand"*. Its purpose is explicit: *"'what depends on this?' is the reverse
direction, computed."*

**What was missing.** The set is now settled as a *document* — *"the file is the
only writable surface"* and *"the HTML view is generated from the document and
stays disposable"*. So the derived reverse cannot be written into the document
(it is derived) and, in a plain-markdown register read top to bottom, is therefore
invisible at exactly the moment it is needed: when someone is reading ST-0001 and
considering changing it. The format's answer is the generated HTML view — but the
document decision also says the document is what you read.

**What I did.** Wrote the reverses into an explicitly-labelled blockquote under
ST-0002, marked as shown-not-stored. This is a hand-maintained copy of a derived
fact, which the format forbids in the same sentence that motivates it. I did it
anyway to make the test legible, and it is a finding rather than a solution.

**Damage if unfixed.** Tony's stated need — *"change requirement x and the impact
can be measured and planned"* — is served only when he is looking at the generated
view, and the register's own settled decision is that the document is the artifact.
Bounded, because the computation is well-specified; the gap is delivery, not
mechanism.

---

## Finding 10 — LOW, and it may be a strength. The Why is where the real work happens, and the format under-sells it.

Writing five of these, the Why took roughly three times the effort of the
statement and carries most of the value in four of the five. The format's own
outward straw-man says it would defend the required Why least hard — *"a required
field that gets filled with a perfunctory sentence is worse than an optional one
filled when it matters"*. My experience of writing against it is the opposite: the
Why is the only element that made me go back to the goals and check, and it is the
element that caught ST-0004 being dead. Recorded as a data point against the
format's own doubt, not as a finding of absence.

**The one gap inside it.** The format says his words are *"marked as his"* and
never says how. I used italics plus attribution plus a date where I had one,
copying the style of the goals file. A machine that needs to distinguish quoted
producer words from model prose — which the never-summarise law will eventually
require — cannot do it from italics.

---

# Verdict

**Does the format hold up in practice? The reasoning holds up; the format does
not yet exist.**

The six elements are the right six, and I want to be precise about that because
the rest of this is critical. Every element earned its place while I was writing:
the reference was needed to point at ST-0001 from ST-0002; the Why caught a dead
requirement; the links were the only part of the shape that produced no ambiguity
at all in the roles-and-storage rule; the fingerprint's replacement of a status
field is correct and I never once missed a status. The provenance discipline
(ADOPTED/ADAPTED/BUILT) is the strongest thing in the document and made it possible
for me to tell which rules were load-bearing and which were choices.

But `requirement-shape.md` is a **design rationale**, not a **specification**. It
argues six elements against a floor of one and wins the argument; it never says
what a requirement looks like. Of the ten findings, six (1, 2, 3, 4, 7, 10) are
some version of "the property is stated, the form that carries it is not". I
invented a notation, a handle field, a graveyard entry structure, a reference
prefix that knowingly violates the format's own rule, marker syntax, marker
numbering, machine-name values and placement, an unapproved representation, a
derivation flag, and a display convention for derived reverses. That is eleven
inventions in five requirements. The document's honesty about *its own* inventions
is exemplary — BUILT is *"flagged loudly"* — and none of that discipline reaches
the person who has to write in the shape.

**The single change that would most improve it: add one fully worked example
requirement, in exact final form, and make it normative.** Not prose describing a
requirement — a real one, in the file format, with all six elements filled, a real
fingerprint value, a real machine name, a real open marker, a real link in each
role, and a dead twin in the graveyard beside it. That one addition closes Findings
1, 2, 4, 7 and 10 outright and makes 3, 6 and 9 answerable questions instead of
guesses. It also costs nothing the document does not already owe, since every
choice it would have to make is a choice someone has to make before anything can
be built.

**If a second change were allowed**, it would be to specify where the reference
allocation lives (Finding 3), because that is the only finding whose damage is
unrecoverable once committed.

---

*Written 2026-08-14 by an agent with access to `docs/design/requirement-shape.md`
and `docs/kerd-goals.md` only. Not approved. Not proposed for the register.*
