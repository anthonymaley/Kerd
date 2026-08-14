# What a requirement looks like

**Status: AWAITING TONY'S REVIEW AND APPROVAL — BLOCKING.** Nothing may be
built against this shape until he has worked through it. Approval here is a
gate, not a status to record and move past: the process demands the answer, it
does not note its absence and continue — his rule, *"the process demand
approval or push back until approval…"*.

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
argued — and a resolution of each of that test's ten findings. The precedence
collision it surfaced has since been **ruled by Tony** (*"agree"*, 2026-08-14
11:53) and is settled.

**What changed 2026-08-14, third pass:** the form was re-tested by a second
fresh agent barred from the first test's output. It held — inventions fell
from eleven to three, and the fingerprint recipe reproduced its published
vector from the text alone — and it surfaced five gaps at the edges of the
block: minting outside the register, the document frame, a machine-name
contradiction, the unrecorded kill authoriser, and a label-stripping crack in
the fingerprint recipe. All five are closed in the rules, with a second
computed test vector chosen to discriminate the fingerprint fix. The
reasoning below is unchanged.

**What changed 2026-08-14, fourth pass — the fidelity audit:** every citation
was checked against its declared source. The research citations verified
exactly; six producer citations did not, because his words had been captured
into working files instead of the interview — now consolidated there,
verbatim, with times, and re-cited here against it. Approved proposals are no
longer dressed as stated positions (his 09:32 "yes" and 11:53 "agree"
answered proposals he did not author); the exemplar's open marker moved off a
question he had already ruled (fine tunes: *"fine tunes move the way
everything else does, just faster, assuming they dont break the specs
etc."*); one invented attribution and one truncated quote are corrected; and
the exemplar no longer breaks its own reserved-form rule. Both published
fingerprint vectors survive unchanged.

**What changed 2026-08-14, fifth pass — the parsing test:** the form had been
validated twice by having fresh agents **write** in it, and audited twice for
fidelity. It had never been **read** by a machine. The first parser written
against it — the view generator at `tools/reqview/reqview.py` — found three
defects in an afternoon that two writing tests and two fidelity audits all
missed, and the three are one design fault: **prose inside a structured field
is indistinguishable from structure.** A bold in-place note that wrapped
across lines wore exactly the clothes of a field label and was absorbed into
the `Depends on` above it, fabricating four dependencies and a dangling
reference that read as entirely genuine; a comma inside prose in a
`Traces to` became a delimiter and produced *"and the migration will not."* as
a trace target; and a `## Findings` section sat between the requirements and
the graveyard, breaking rule 13's own ordering, its numbered sub-headings
mimicking requirement blocks. **Writing and parsing are different tests**, and
the format had only ever sat the first one. Three rules close the fault — a
structured field carries references and never prose (rules 7, 8, 9), a note is
a blockquote and can never wear a field label's clothes (rule 1), the
graveyard is last and nothing sits between it and the requirements (rule 13) —
under a principle this repo already holds elsewhere, now stated on its own as
rule 14: **ambiguity is refused, never guessed.** All three defects produced
*plausible* wrong answers, which is worse than an error. Both published
fingerprint vectors survive unchanged.

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
in the register, and these numbers are not allocations.** That is not just a
label: under rule 2, a number outside the register names nothing, and filing
refuses a block that arrives with a pre-written number — so these examples
cannot collide with anything even if copied. The fingerprints on the first
and third blocks are genuinely computed values under the recipe given after
the examples; the third is chosen specifically so that an implementation
which strips labels wrongly, or drops the derived prefix, fails against it.

**And one thing must be unmistakable: the approval lines and the kill
authoriser inside these blocks are fabricated by the model to show the
form.** Tony has approved nothing and authorised no kill on this page — a
model-written approval is a contradiction in terms under this document's own
theory. The approval line sits outside the fingerprint, so the fabrication
costs the test vectors nothing; a real approval is his to record and only
his.

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

**Statement.** A change classified as fine tuning shall move along the same path as every other change, faster; shall land only if it does not break the governing spec, design document, or requirements; and in a borderline case its classification shall be made by [OPEN-R-0102-1: who makes the fine-tuning call when a change is borderline, given that role approval was later ruled to be operational help rather than authority over the agreements].

**Why.** His ruling of 2026-08-13 22:39 closed the shape of the path: *"fine tunes move the way everything else does, just faster, assuming they dont break the specs etc."* Not a separate process — the same path, faster, on condition the specs hold; the second clause of the statement binds that condition. What remains genuinely unstated is the borderline call: the goals record names it open ("who makes that call when it is borderline" — the record's phrasing, not his), and the same 22:39 rulings reread role approval as operational help rather than authority over the agreements, so the earlier answer no longer covers it. That is the open marker.

**Traces to.** G3

**Depends on.** R-0101

**Approval.** none — blocked by [OPEN-R-0102-1]

---

### R-0104 — the producer sees the weight of what remains
<!-- machine: 01a0010a-8a08-7baf-8c50-742a3ab20b6f -->

**Statement (derived).** Kerd shall state, at each request for a producer decision, how many producer decisions the remainder of the work item's journey requires, and shall present that count with the request.

**Why.** Tony added this input to the goals himself: *"a user never feels overwhelmed by the process"* — and ruled inputs of this kind unmeasurable: *"these are not measurement, these are inouts to design to avoid what those g1-g8 from happening, they cant be measured."* His words are the authority; the statement is our derivation of one countermeasure from them — the weight of what remains is shown before it is spent, so accumulation is seen coming rather than discovered. Approving this block approves that derivation.

**Traces to.** G1, G5

**Depends on.** none

**Approval.** Tony, 2026-08-14 · fp:e45b7b2d80a2
```

The third block is the discriminating test vector: its statement is derived,
so under rule 9 the hashed statement line begins `derived: `. An
implementation that strips only the plain label (leaving `(derived)` in the
text), or strips the whole label but forgets the prefix, produces a different
value — one vector that only proves the easy case is a vector that hides
this class of bug.

And the dead twin, in the graveyard at the end of the same document:

```markdown
## Graveyard

### R-0103 — DEAD — effort threshold below which the spec need not change
<!-- machine: 01a000da-8cb2-7e68-b8b5-dbc9a74f54ac -->

**Killed.** 2026-08-14, by analysis against the plain text of Law 2 in the approved goals — not by a test. Kill authorised by Tony.

**Statement as proposed.** Kerd shall define an effort threshold, and a change falling below it shall land without an update to its governing spec, design, or requirement.

**Why it was proposed.** It follows directly from the pressure G3 names — *"i dont mind robust, i just mind overhead and overwork"* — and it is the design a reader arrives at independently from G3 alone.

**Why it is dead.** His words behind the ruling: *"so each change should result in a chnage to spec or design or requirement"*, and immediately after, *"but doesnt have to be huge process"*. The goals record draws the line in its own words, not his: "The law is absolute; the ceremony is proportionate" — and names why a threshold is harmful rather than merely unnecessary: it decays Law 2 into "significant changes only", a judgement call, and therefore a hole.

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
   machine name, when present, sits in an HTML comment on the line directly
   under the heading — and a freshly hand-written block legitimately lacks
   it until the checking tool's next run, which is the one sanctioned
   absence in the form: rule 4 says who writes it, and it is never a
   person. Then the five labelled lines, bold label, full stop, one blank
   line between fields, always in this order: **Statement**, **Why**,
   **Traces to**, **Depends on**, **Approval**. All five are required on
   every live requirement — a field that does not apply says so explicitly
   (`none`), it is never omitted. The absence-must-be-written rule governs
   the five labelled fields; it never obliges a person to write the machine
   comment, which would break rule 4.

   **The bold-label form is reserved to fields, and a note is a blockquote.**
   Inside a requirement block, a paragraph whose first line opens with `**` is
   a field label — one of the five above, or one of the six a graveyard entry
   carries (rule 10) — and nothing else may take that form. An **in-place
   note** — a rework, a re-pointing, an amendment, anything a person needs to
   record beside the fields — is written as a markdown blockquote:

   ```markdown
   > **Note — Reworked 2026-08-14 14:54, on the producer's authorised ruling.**
   > The statement read *(verbatim, as migrated)*: "…". The twelve-type list is
   > dead; the distinction inside it is what the ruling kept, so this block is
   > reworked rather than killed and its reference is unchanged.
   ```

   The collision is closed by mechanism, not by care. A field line begins with
   `*`; a note line begins with `>`; and **every** line of a note carries the
   `>`, so a note that wraps across five lines is five note lines, and no wrap
   can produce a line that reads as a field. That is the exact failure this
   closes: an in-place note whose bold lead wrapped across two lines was read
   as a field label, and the paragraph under it was absorbed into the
   `Depends on` above, fabricating four dependencies and a dangling reference
   that looked entirely genuine. **Notes come last, after all five fields**,
   so the field region is contiguous and in order. A note is outside the
   fingerprint, exactly as a comment beside the record is — recording a rework
   must not un-approve anything. Outside a block — the register's preamble, a
   section's own introduction — there are no fields to collide with, and prose
   is prose.

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

   **Outside the register, references do not exist.** A number becomes a
   reference only by being present in the register; written anywhere else —
   a draft, a proposal, a branch that has not merged, a test — `R-` plus
   digits is the name of nothing. A writer drafting elsewhere therefore
   never mints: a draft block carries a **draft mark** in place of the
   reference — `R-@<handle>`, for example `R-@spec-in-repo` — and draft
   blocks point at each other by their draft marks. **Minting happens at
   filing, and only there:** when a draft lands in the register, the tool
   assigns the next number by the rule above and rewrites every draft mark
   that points at the block. **Filing refuses a block that arrives with a
   pre-written number** — the filer's tool assigns, always, so a collision
   cannot be typed into existence. A draft that is never filed consumed
   nothing: its draft mark was never a reference, so there is nothing to
   retire and no number is burned. This is the same shape as the machine
   name — identity is minted by the tool at the boundary, never composed by
   hand — and it is why the illustrative numbers in this document are
   harmless by mechanism rather than by warning label.

3. **The handle** is a short human name after the reference. It is
   notation, not a seventh element: it is outside the fingerprint, may be
   reworded at any time without touching identity or approval, and carries
   meaning deliberately — which is exactly why it is not the reference. It
   exists because the set is a **document read top to bottom**: a page of
   bare `R-0101 … R-0105` headings is unreadable, which fails the reading
   the document decision was chosen for. A database can leave the headings
   meaningless because nobody scans a database; a document cannot. The
   writing test added this out of necessity; it is adopted.

   **What a handle is for — and the test.** A reader scanning the headings
   must know what each block is *about* without reading its statement. So:
   cover the statement, read the heading alone, and ask what the
   requirement says. If the answer is "something about X" rather than a
   thing you could act on, the handle has failed and is rewritten. A handle
   that would be equally true of a dozen other blocks is not a handle.

   **What a handle must do.** Say the thing the requirement says, in the
   requirement's own terms, compressed — the rule itself rather than its
   subject. Roughly three to eight words. Lower case, no full stop, no em
   dash (the heading uses em dashes as delimiters). A noun phrase or a
   short clause, whichever states the point more directly.

   **What a handle must not do.** Three failures, all of them seen in this
   register's migration, where thirty-nine handles were invented with no
   standard to write them against:

   - **Do not describe the category of thing.** Naming the *kind* of rule
     and withholding the rule is the commonest failure and the emptiest.
   - **Do not restate the reference or the section.** "a requirement about
     dependencies" tells a reader only what they can already see.
   - **Do not truncate the statement.** A handle clipped mid-clause reads
     as a broken sentence rather than a name. Compress the point; never
     chop the words.

   **A good one and a bad one, both real.** Good: `R-0009 — the cross takes
   no modifier`. It is the rule itself in five words, and a reader who
   reads only that heading already knows what the block binds. Bad, and
   rewritten under this rule: `R-0005 — work is distinguished on one axis`
   announced that there was one axis and withheld which one, when the
   statement says exactly which — so it became `R-0005 — ships a change, or
   produces a finding`. Same length, and the second one says the thing.

   **A graveyard entry carries a handle under the same rule.** The `— DEAD`
   marker carries the death, so the handle stays a statement of what the
   block *said*, never of the fact that it died.

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
   not a later nicety. **The live set is defined:** the blocks under the
   register's requirements heading (rule 13), and nothing else. Markers in
   a draft count for nothing — a draft's markers are questions in a draft,
   not holes in the set — and the cap cannot be evaded through drafts,
   because the cap is enforced **at filing**: a block whose markers would
   push the live set past three is refused until a marker somewhere is
   closed.

6. **His words, in the Why**, are marked by one reserved form: an italic
   quotation with attribution — `Tony: *"…"*`, or *"…"* directly following
   his name and a date. **Inside the register, italic double-quoted text is
   verbatim producer words and nothing else may use that form.** Machines
   and readers distinguish his words from ours by form, not by judgement.

7. **Traces to** carries **references and nothing else — never prose.** The
   separator is defined exactly: **a comma followed by a single space**, and
   nothing else separates targets. A target is `G<n>`, `Law <n>`, or a
   requirement reference `R-nnnn`; anything that is not one of those three is
   not a target. Three **whole-field sentinels** are declared, and each is
   matched against the *entire* field before a comma is ever looked at —
   which is precisely why the comma inside the first one is not a separator:
   `no parent, by design` (there is no parent, deliberately);
   `not yet traced` (no trace has been established, and none will be
   invented to fill the space); and, on `Depends on`, `none`.

   **If a link needs explaining, the explanation goes in the Why**, which is
   where reasons already live. A structured field is read by a machine; a
   sentence in it is a delimiter waiting to happen. It happened: a `Traces to`
   carrying prose split on its own comma and yielded *"and the migration will
   not."* as a trace target — a wrong answer that looked exactly like a right
   one. Prose here is refused, not parsed (rule 14).

   **A rendering built for a human resolves every reference to its name.**
   The register file may carry the bare `G4` — it is written for the
   machine and for a reader with the goals open beside them. A generated
   view is not: it is the artifact built for the producer to *read*, and
   `**Traces to.** G4` asks him to hold eight goal numbers and four law
   numbers in his head, thirty-nine times over. So a view shows
   `G4 — Every approval is real`: **the reference stays**, because he has
   to be able to say it out loud, and it never travels alone. The name is
   quoted from its source, never paraphrased and never shortened into
   something snappier; where it will not fit inline it goes in full on
   hover or in a panel, never truncated into a different claim. **The rule
   generalises past this field** — it is the same rule that killed
   *"you say AU7 but how do i know what that is?"*: **name the behaviour,
   never the identifier.** It binds on requirement references, goal and law
   references, and any other identifier a rendering puts in front of a
   person. A reference that appears without its name in a human-facing view
   is a defect in the view, not a shorthand.

   A trace to a goal counts toward
   coverage; a trace to a law is a constraint link and is excluded from
   coverage arithmetic — laws are obeyed, not achieved, and counting the
   two together would make coverage mean nothing. A secondary source a
   requirement genuinely serves is a second target, not buried prose:
   prose is unqueryable, which is the loss the links element exists to
   prevent.

8. **Depends on** carries requirement references only — `R-nnnn`, separated
   by a comma and a single space — or the whole-field sentinel `none`. Never
   prose, on the same rule as 7: why a dependency exists, or why one was
   dropped, goes in the Why or in a note (rule 1), never into the field. A
   reference that does not resolve is an error that stops the run — already
   settled; restated here because it is the writer's rule too.

9. **The approval line** is either `none`, or `none — <reason>`, or
   `Tony, <date> · fp:<12 hex characters>` with nothing after it. **The
   reason after `none —` is the one place a structured field admits prose,
   and it is never parsed:** everything after the dash is free text for a
   reader, the machine reads only `none`. Anything that is neither of those
   three shapes is refused (rule 14), never guessed at. **The fingerprint
   recipe:** take the text of Statement, Why, Traces to and Depends on, in
   that order; strip each bold label **entirely — everything between the
   opening and closing double asterisks, modifier included, plus its full
   stop** — so `**Statement (derived).**` is removed whole, never leaving a
   stray `(derived)` in the hashed text; **then, if and only if the
   statement label carried the derived modifier, prefix the statement text
   with `derived: `** (lowercase, colon, one space), so that flipping the
   flag invalidates the approval — approving a derived block is approving
   the derivation, and un-flagging it un-says that. Trim each field and
   collapse every internal whitespace run to a single space; join the four
   with single newline characters; hash the UTF-8 bytes with SHA-256;
   record the first twelve hex characters. **Two test vectors are
   published in the examples above:** the first block proves the plain
   case; the third block is chosen to discriminate — an implementation
   that strips the label wrongly or drops the `derived: ` prefix fails
   against it while passing the first. A recorded fingerprint that no
   longer matches means **not
   approved** — that state is computed and reported by the tool, never
   written into the file. Collapsing whitespace is deliberate: a
   formatting-only edit must not un-approve a requirement; the recipe, not
   the file bytes, is the contract, and every implementation must share it
   exactly.

10. **A graveyard entry** replaces the five live fields with six:
    **Killed** (three facts, all required: the date; what killed it — a
    ruling, an analysis, or a test; and **who authorised the kill**, named.
    Killing a requirement is a change to the set, and a change to the set
    reaches the same approval theory as everything else — an entry that
    cannot say who agreed the death is a change nobody approved. A model
    may propose a kill; a kill lands with a named authoriser or the tool
    refuses the entry),
    **Statement as proposed**, **Why it was proposed**, **Why it is dead**
    (carrying the words that killed it, verbatim under the same reserved
    form), **What was learned** (the payload — written so the next
    proposer does not re-derive the dead idea), and **Superseded by** (a
    reference, or `nothing — killed outright`). The heading gains `— DEAD`
    between reference and handle. The machine name stays. Those six labels
    take the bold-label form and nothing else in the entry does: a note on a
    graveyard entry is a blockquote, under rule 1. **The links are
    dropped on death:** a dead requirement tracing to a live goal would
    corrupt every coverage count. The graveyard lives under a `## Graveyard`
    heading at the end of the same document — **last, with nothing between it
    and the requirements** (rule 13) — so anyone proposing into the register
    scans past it — or the tool does — before a new requirement lands. The formerly open question of where the graveyard sits is
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

13. **The document frame — what the register looks like as a whole.** The
    register is one file with exactly this skeleton, top to bottom: a
    level-one title naming the set (`# Requirements — <project>`); an
    optional preamble — prose about the set, never requirement content, and
    nothing in it is fingerprinted; then a `## Requirements` heading
    holding every live block; then the `## Graveyard` heading holding
    every dead one, always last, so a reader scanning to the end passes
    the dead ideas on the way. **Nothing else sits at heading level two, and
    nothing at all sits between the requirements and the graveyard.** That is
    not a tidiness rule: a `## Findings` section did sit there, and its
    numbered `### 1 — …` sub-headings mimic requirement blocks closely enough
    that a parser reading headings will file them as requirements. Analysis
    *about* the set — findings, triage, audits — lives in its own file beside
    the register (`docs/requirements/findings.md` for this one), pointed at
    from the preamble. The register holds the set and its dead, and nothing
    else.
    **Ordering rule: blocks appear in ascending reference order, in both
    sections, always.** Reading order is creation order — the story of the
    set in the order it was thought — and it is the one order that never
    needs maintaining, because the tool appends at filing and nothing ever
    moves. Grouping by theme is a rendering job for the generated view,
    never a reason to reorder the file. **"The register" in every rule
    above means this file; "the live set" means the blocks under its
    requirements heading.** A document that is not the register may quote
    blocks, draft them, or test them — it allocates nothing, approves
    nothing, and its markers count for nothing until filing.

14. **Ambiguity is refused, never guessed.** A tool reading this register that
    meets something it cannot classify — a paragraph inside a block that is
    neither a field nor a note, a field label repeated or out of order, a
    `Traces to` or `Depends on` that is neither a declared sentinel nor a list
    of references, an approval line in none of its three shapes, a level-two
    section that is neither the requirements nor the graveyard — **stops and
    says exactly what it could not classify, naming the block and the text.**
    It never picks the likely reading, and it never renders a page from a
    guess. This is the rule the three defects of the parsing test argue for:
    each of them produced a *plausible* wrong answer — four fabricated
    dependencies, a dangling reference to a graveyard entry, and a trace
    target reading *"and the migration will not."* — and a plausible wrong
    answer is worse than an error, because an error is seen and a plausible
    answer is believed. The repo already holds this rule elsewhere: G2's
    refusal to guess, and the old schema's own line, carried forward whole —
    *"a red check is a question the producer answers; a silent downgrade is a
    decision made for them."* A refusal is that question in the parser's
    mouth. The corollary binds the format, not just the tool: **any rule here
    that cannot be checked by a machine reading the file is a rule that will
    be broken silently**, which is why rules 1, 7, 8 and 9 are written as
    shapes a parser can accept or refuse rather than as habits a writer is
    asked to keep.

The existing register's blocks do
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

**RULED BY TONY, 2026-08-14 11:53 — his whole word was "agree", given to a
proposal he did not author** (interview record, consolidated morning
rulings). The rule is settled and binding: **the word list governs the
Statement; quoted words inside the Why are never linted.** The phrasing is
ours; the authority is his — an approved proposal, not a stated position,
and the two are recorded as what they are.

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
named it *"the only attribute that answers 'can we delete this yet?'"* — a
correction recorded by the fidelity audit of 2026-08-14: an earlier revision
of this sentence attributed the phrase "the only attribute that reliably pays
for itself" to the research, and the research never said it; the payoff
framing was this document's gloss wearing quotation's clothes. The verified
words stand alone now. A statement says what must be
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
  simple way for me to see the requirments and their dependencies"* — from his
  objection of 2026-08-14 08:16, carried whole in the interview record's
  consolidated morning rulings.

**ADOPTED — the storage rule is the strongest convergence in the whole
survey:** all five docs-as-code tools store a link at exactly one end and
derive the reverse, because two stored ends means two records to keep
consistent and a conflict every time they touch. A link naming a requirement
that does not exist is an error that stops the run — also unanimous. The
derived reverse is not decoration: it is what answers his change-of-mind
question — *"change requirement x and the impact can be measured and planned"*
(2026-08-13 23:05, in the interview record) — because "what depends on this?"
is the reverse direction, computed, never maintained by hand.

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
housekeeping details so metadata edits do not nag. **ADAPTED in two steps, and
their provenance differs:** Doorstop's fingerprint covers what its project
chooses; ours covers **the statement, the Why and the links, always**. **His
ruling of 09:00 covers the statement and the links** — *"no point doing half of the
fingerprint."*

**The Why joined the fingerprint at 2026-08-14 09:32 — and the provenance is
recorded exactly, because approved and authored are different things.** The
composer had left the Why out silently and flagged its own omission: *"I
applied his ruling narrowly where I could have asked."* The correction — that
a reason can change what a statement means, so an approval must not survive
an edit to it — was then **put to him as one half of a two-part proposal**
(the other half being the document decision below), after his own instruction
at 09:29: *"give me something i can say yes to."* **His word at 09:32 was
"yes"** — he approved both parts together; he authored neither phrasing. The
interview record's consolidated morning rulings carry this. The reasoning is
his own "no point doing half of the fingerprint" applied one element further,
and the approval makes it binding — but the sentence was ours, and a proposal
he approved must never be dressed as a position he stated.

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
draft never chose one. **The document corner was put to Tony as one half of a
two-part proposal — his instruction, 09:29: *"give me something i can say yes
to"* — and his word at 09:32 was "yes".** He approved the corner; the framing
of it was ours. The interview record's consolidated morning rulings carry
both the proposal shape and the answer.

**Requirements are blocks in a file you can read top to bottom.** Reading order
is meaningful and costs nothing to keep. Git carries the history. The HTML view
is generated *from* the document and stays disposable — the file is the only
writable surface, which is the one thing every tool in the survey agreed on.

**This does not override his objection to a markdown file — it answers a
different question, and the reconciliation deserves stating because both
rulings are real.** On 2026-08-13 22:58 he ruled: *"we cannot consider this
markdown file as how we capture and version and work on requirements. we need
a robust and easy to engage with solution."* The next morning, 08:16, he
separated the two things that ruling could have meant: *"a ingle huge
markdown for me to interact with is not the answer. However, im not going to
declare how we store that data, it could be a markdown file that you manage
and create."* **What he rejected is a file as the thing he must interact
with; what he left open — and then approved — is a file as the thing the
model manages underneath.** The document corner is the storage decision; his
interface is the generated view, which owes him what his 08:16 objection
itemises: seeing the requirements and their dependencies, editing the text,
seeing each one's standing, and leaving comments, links and images. Anyone
reading the document decision as "Tony works in a markdown file" has read it
backwards.

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
  dependencies"* (2026-08-14 08:16, in the interview record).

**And it is the corner we already stand in.** The register is already a document
with requirements as blocks in reading order. This confirms rather than
migrates — no conversion, no re-keying, no lost history.

**What it commits us to, stated plainly:** merge conflicts here are prose
conflicts, not field conflicts. Reordering is free. Anything that needs to
query across requirements is computed by reading the document, not by asking a
database — which is affordable at this scale and would not be at ten thousand.

**Deliberately still open:** whether it is *one* document or several. Cheap to
decide later and expensive to guess at now.

*(Where the graveyard sits was open when this section was written and is now
closed — it lives under a graveyard heading at the end of the same document.
See the rules.)*

---

## Beside the requirement, never on it

Three things the old draft put on the record that belong next to it. None of
these is an element of the shape.

**Comments and notes.** His ask stands in full: *"to add comments perhaps for
you to pick up or to record notes around the requirments"* (2026-08-14 08:16,
in the interview record's consolidated morning rulings) — note his own
preposition, **around**. **ADOPTED as a discipline — it is unanimous across
the territory:** discussion lives outside the record everywhere (proposals
mandate a discussion address; decision processes keep debate in the thread and
record only a link), and the enterprise finding is the sharp version:
**comments are not field values, so commenting must never version the
requirement.** A comment on our shape must never disturb the fingerprint — a
question about a requirement must not un-approve it. So comments live beside
the record, addressable to it by its reference, and the model reads them there.

**Attachments — links and images.** His ask: *"add links or images perhaps as
input"* (2026-08-14 08:16, in the interview record). **This is the one place we are on our own, and it is flagged loudly:
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
once — which is precisely the thing DOORS makes hard and expensive via
baseline sets."* (An earlier revision truncated this quote at "expensive"
with a full stop, silently dropping the mechanism it names; the full sentence
is restored.) One
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

**6 — The Statement/Why boundary was unreliable. SETTLED — the edge closed
with finding 5's ruling.** The boundary test is rule 11: statement content is
what a build can be rejected against, manner included; the Why explains and
never restates a binding clause. The inversion case — where his words in the
Why are the authority and the statement is derived — is exactly what the
derived-statement flag marks, now settled by the same ruling.

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

**The score: all ten settled.** Findings 5 and 6's edge landed together with
his ruling of 2026-08-14 11:53 on the precedence rule and its
derived-statement flag.

## Findings resolved — the second test's five gaps, each answered

The form was re-tested: same brief, a fresh agent barred from the first
test's output. Inventions fell from eleven to three, the fingerprint recipe
reproduced its published vector from the text alone on the first attempt,
and the graveyard entry — unwritable in the first test — was the easiest
block in the file, because the learning payload is a field, not a
discipline. The three remaining inventions were all at the edges of the
block, not in it. Five gaps came back; each is answered:

**1 — A reference could not be minted outside the register. SETTLED, and it
was the worst one.** Its damage was unique: every other gap costs a rewrite;
this one costs a permanent identifier under a doctrine that forbids changing
one — and this document had sprung the trap on itself, countermeasuring its
own example numbers with a warning label. Rule 2 now closes it by mechanism:
outside the register, references do not exist; drafts carry draft marks
(`R-@<handle>`) and never numbers; minting happens only at filing, where the
tool assigns and **refuses any block arriving with a pre-written number**. A
draft never filed consumed nothing. Collision cannot be typed into
existence.

**2 — The register had no document frame, and the live set was undefined.
SETTLED.** Rule 13: title, optional non-fingerprinted preamble, a
requirements heading holding the live set, the graveyard always last, blocks
in ascending reference order in both sections — creation order, the one
order that never needs maintaining. The live set is defined as the blocks
under the register's requirements heading; a draft's markers count for
nothing, and the cap cannot be evaded through drafts because it is enforced
at filing (rule 5).

**3 — Two rules gave opposite instructions about the machine name.
SETTLED.** The second test's reading was right and is now written: nobody
hand-writes one, a fresh block legitimately lacks the comment until the
tool's next run, and the absence-must-be-written rule governs the five
labelled fields only (rule 1).

**4 — Nothing recorded who authorised a kill. SETTLED.** The Killed field
now carries three required facts: the date, what killed it, and the named
authoriser (rule 10). Killing a requirement is a change to the set, so it
reaches the same approval theory as everything else — a model may propose a
kill; it lands with a named authoriser or the tool refuses the entry. The
worked graveyard entry shows the form.

**5 — The derived label had an undefined interaction with the fingerprint,
and one vector could not catch it. SETTLED.** Rule 9 now strips the label
whole — modifier included — and then prefixes a derived statement's text
with `derived: `, so flipping the flag invalidates the approval, which is
what "approving the derivation" demands. A second worked example with a
computed fingerprint is published, chosen specifically so an implementation
that strips wrongly or drops the prefix fails against it while passing the
first vector.

## Findings resolved — the fidelity audit of 2026-08-14 12:21

An audit checked every citation in this document against its declared
sources. **The research citations verified exactly** — standards, tool
findings, figures. **Six producer citations did not**, and the cause sat
upstream: his words had been captured into whichever file was in front of
the model rather than into the interview, so the source of truth had
stopped holding the truth. The interview record now carries the morning's
rulings consolidated, verbatim, with times. What was done here:

**Citations re-grounded.** The dependencies objection, the comments ask,
and the attachments ask now cite his 08:16 words against the consolidated
record; the 09:26, 09:28, 09:32 and 11:53 rulings cite it likewise.

**Approved and authored, separated everywhere.** The 09:32 "yes" answered a
two-part proposal — the document corner and the Why joining the fingerprint
— put to him together after his own *"give me something i can say yes
to"*; the 11:53 word was "agree", to a proposal he did not author. Every
passage that dressed an approved proposal as a stated position is
corrected. The distinction is not pedantry: a proposal he approved binds,
but citing it as his authorship manufactures words he never said, which is
the exact offence the never-summarise law names.

**The exemplar's open marker was spent on an answered question.** R-0102
marked the fine-tuning path as open — but he had ruled it at 2026-08-13
22:39: *"fine tunes move the way everything else does, just faster,
assuming they dont break the specs etc."* The goals file was fourteen hours
stale when it was read, and the exemplar failed his own check — *"did i
read from file or stale memory"* — in its worked example. R-0102 is
rewritten: the statement now carries the ruling (same path, faster,
conditional on the specs holding), and its marker moved to a question that
is genuinely open — who makes the borderline fine-tuning call, now that
role approval is ruled operational help rather than authority over the
agreements. No fingerprint was invalidated: R-0102 was never approved, and
both published vectors are untouched and re-verified.

**The exemplar broke its own reserved form.** The graveyard block wrote two
of the goals record's phrases in the italic-quoted form rule 6 reserves for
his verbatim words. Fixed: the record's phrasings are plain-quoted and
attributed as the record's; his actual words behind the ruling are quoted
in the reserved form. The remaining example blocks were checked — every
italic quotation in them is his.

**An invented attribution.** The research was credited with "the only
attribute that reliably pays for itself"; it said *"the only attribute that
answers 'can we delete this yet?'"*. Corrected, with the correction left
visible rather than silently patched.

**Minor, both fixed:** the DOORS quote is restored to its full sentence
(the truncation had dropped "via baseline sets" behind a full stop), and
the fabricated approval lines in the examples now say loudly that they are
fabricated — a model-written approval is a contradiction in terms here, and
the page a writer copies from must not normalise one.

## Findings resolved — the parsing test of 2026-08-14, three defects

The format had been tested twice by having a fresh agent **write** in it, and
audited twice for the fidelity of its citations. All four passes read the file
the way a person reads it. The first thing to read it the way a machine does
was a view generator, and it found three defects in an afternoon. **Writing
and parsing are different tests**, and that is the finding underneath the
three: a writer supplies the missing structure from meaning, so a writing test
cannot fail on a format that only *looks* structured. The three defects are
one design fault — **prose inside a structured field is indistinguishable from
structure** — and each is answered by a rule that a parser can enforce.

**1 — A bold note wrapping across lines is indistinguishable from a field
label. SETTLED, and it was the dangerous one.** The in-place notes this
register carries — *"Reworked 2026-08-14…"*, *"Re-pointed…"*, *"Unhomed by
that kill…"* — opened with bold text at the start of a paragraph, which is
exactly the five field labels' form, and one of them wrapped its bold lead
across two lines. A line-oriented parser matching a label within one line
found no label, absorbed the whole note into the `Depends on` above it, split
it on commas and **fabricated four dependencies and a dangling reference into
the graveyard** — every one of which rendered as a real link on a real page.
Rule 1 now gives a note its own marker: a blockquote, `>` on every line,
opening `> **Note — …**`, always after the five fields. A field line starts
with `*` and a note line starts with `>`, so no wrap can make one look like
the other. The countermeasure is a shape, not a caution.

**2 — A comma inside prose in a list field becomes a delimiter. SETTLED.**
One `Traces to` explained itself in a sentence, and splitting on commas made
*"and the migration will not."* a trace target. Rule 7 now says a structured
field carries references and nothing else, defines the separator exactly
(comma, single space), and declares the whole-field sentinels — matched
against the entire field before any comma is looked at, which is how
`no parent, by design` survives having a comma in it. Where a link needs
explaining, the explanation goes in the Why, which is where reasons already
live. Rule 8 binds `Depends on` the same way, and rule 9 confines the only
admitted prose — the reason after `none —` — to text no machine reads.

**3 — The graveyard was not last. SETTLED.** A `## Findings` section sat
between the requirements and the graveyard, breaking rule 13's own ordering,
and its numbered `### 1 — …` sub-headings are close enough to requirement
headings that a heading-driven parser will file them as blocks. Rule 13 now
states that nothing sits between the requirements and the graveyard, and
sends analysis about the set to its own file beside the register.

**And the principle underneath, now rule 14: ambiguity is refused, never
guessed.** All three defects produced *plausible* wrong answers rather than
errors — which is the worse failure, because a plausible answer is believed.
A parser meeting something it cannot classify stops and names it. Both
published fingerprint vectors were recomputed after this pass and reproduce
unchanged: the recipe was never the problem, and no field text in the worked
examples moved.

---

## Straw-man

Law 3, both passes.

### Inward — what is wrong or missing in what I wrote

**~~The versions are not carried.~~ CLOSED by Tony, 2026-08-14 09:26:** *"we
already discounted the FINAL 1.0 etc - ignore, we use fingerprint and
lifecycle."* (Interview record, consolidated morning rulings.)

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
suggestion — offered as one, not as a ruling — that *"maybe lifecycle is a
better way vs status"*: a progression rather than a flag. **If he meant a stored field, this reading is wrong and an element
is missing.**

*The shape therefore stands at six elements.*

**~~"Superseded" and "dropped" have no home.~~ ANSWERED by Tony, 2026-08-14
09:28:** *"we need a graveyard so we dont add them again and learn from them"*
(interview record, consolidated morning rulings)

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
CLOSED by Tony, 2026-08-14 09:32 — the Why is inside the fingerprint. It was
the model's correction, put to him and approved, not his own; the provenance is
recorded in the approval-mark element.** The original
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
all~~ — **CLOSED in two steps:** Tony approved the document corner, put to
him as a proposal (his "yes", 2026-08-14 09:32), and the normative form now
shows what a block inside that document looks like.

### What the normative form newly breaks — added 2026-08-14, the same pass inward

The form section fixed the writing test's findings and created its own
exposures. Named here so they are findable, not discovered:

- **~~The example references could be mistaken for allocations.~~ CLOSED,
  2026-08-14 second pass:** closed by mechanism rather than label — outside
  the register a number names nothing, and filing refuses a block arriving
  with a pre-written number (rule 2). The second test named the warning
  label as evidence of the gap, not a fix; the mechanism is the fix.
- **The minting rule assumes one document — still true, now with the frame
  behind it.** Rule 13 declares the register one file, so the assumption is
  now stated rather than silent. The deliberately open question of
  one-document-versus-several keeps its cost: splitting the set re-opens
  both reference allocation and the marker cap's scope, and both must find
  a new home before any split lands.
- **The cap has syntax and a defined scope, and still no counter.** The
  live set is defined and filing-time refusal is specified, but both are
  duties of a tool that does not yet exist. Until it runs, the cap is
  exactly the unenforced contract this document warns about.
- **The fingerprint recipe, not the file, is the contract — and it now has
  a branch.** The derived prefix means the recipe does one thing for plain
  statements and another for derived ones, which is a second way for two
  implementations to silently disagree. The discriminating second vector is
  the countermeasure — chosen so the wrong readings fail against it — but
  two vectors are still thin, and a real test suite around the recipe is
  owed before a second implementation exists.
- **The tool now rewrites prose.** At filing it mints the reference and
  rewrites every draft mark pointing at the block — the first time the
  tool writes into requirement text rather than beside it (the machine
  comment sits beside; a depends-on line is content). The write is
  mechanical and bounded to draft marks, but a tool that edits content is
  a new class of actor in a file whose whole theory is that the producer's
  words are never touched. The bound must hold: the tool rewrites draft
  marks and nothing else, ever.
- **The handle is meaning on the record.** It will go stale, by design, and
  the design's answer — rename freely, nothing breaks — is only true while
  every tool treats the heading after the reference as decoration. A tool
  that ever parses the handle inherits the staleness the reference was built
  to avoid.
- **The kill authoriser is a name in prose, not a fingerprint.** Approval
  of a live requirement is cryptographic; authorisation of a death is a
  written name (rule 10). The asymmetry is accepted for now — a graveyard
  entry's content is frozen by convention, not by hash — and it is the
  weakest link in the approval theory this pass leaves standing.
- **An open marker is minted against whatever the writer last read, and
  nothing checks it is still open.** The fidelity audit caught this
  document's own exemplar spending a marker on a question the producer had
  ruled fourteen hours earlier — the goals file was stale and the ruling
  lived elsewhere. The fix here was manual; the exposure is structural: a
  marker is a claim about the current state of the record of decisions,
  and the form provides no freshness check on it. Until one exists, "is
  this still open?" is a question the writer must put to the interview
  record at minting time, as discipline — which is exactly the kind of
  answer this document distrusts everywhere else.

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

1. ~~**What carries the named versions?**~~ **CLOSED — he withdrew the want
   itself, twice.** 08:53: *"ignore 'You've already said DRAFT / ACCEPTED /
   FINAL v1.0, v1.2.'  you asked me directly that was my thinking without
   research."* And 09:26: *"we already discounted the FINAL 1.0 etc - ignore, we
   use fingerprint and lifecycle."* Nothing carries named versions because
   nothing needs to: the fingerprint answers *has this changed since we agreed
   it?*, which is the question versions were being asked to carry.
2. ~~**Where do superseded and rejected requirements go?**~~ **CLOSED,
   2026-08-14:** the graveyard, at the end of the same document, with the
   entry form shown in the normative form section — a durable record, its
   reference retained, superseded-by as a named field.
3. ~~**Is the Why inside the fingerprint?**~~ **CLOSED by Tony, 2026-08-14
   09:32:** yes — approved as half of a two-part proposal put to him
   together; the provenance is recorded in the approval-mark element, and
   the fingerprint recipe hashes it.
4. **What is the container** — partly closed: Tony approved the document
   corner as the other half of the same 09:32 proposal, and the normative
   form defines the block. **Still
   open: one document or several** — and the minting rule now attaches a
   cost to splitting, named in the straw-man.
5. **Does the writing help ever refuse, or only advise?** Still open — its
   scope is now settled by his precedence ruling (the Statement only, never
   his quoted words), but whether it refuses or advises within that scope
   is not. The second test surfaced a related documentation gap worth
   settling with it: a statement deriving from an absolute law has to carry
   universal force without a banned totality word, and the technique for
   that (an indefinite subject — "a change that lands shall…") is nowhere
   taught, so writers who do not know it will quietly weaken absolute laws.
6. **Where exactly is the beside-space, and at which moments does the model
   read it?** His *"for you to pick up"* is a reading obligation, not just a
   storage location.
7. ~~**The precedence rule and the derived-statement flag — proposed, his
   ruling needed.**~~ **CLOSED — RULED BY TONY, 2026-08-14 11:53:
   *"agree"*.** The rule and what follows from it are recorded in their own
   section after the normative form; rule 12 carries the flag as settled.
