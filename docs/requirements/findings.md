# Findings — the Kerd requirements register

Written for the producer, alongside `register-v2.md`. Nothing below has been
acted on.

**This file was carved out of the register on 2026-08-14, unchanged.** It sat
as a `## Findings` section between the requirements and the graveyard, which
breaks rule 13 of `docs/design/requirement-shape.md` two ways: nothing sits at
heading level two in the register but the requirements and the graveyard, and
the graveyard is always last. Its numbered `### 1 — …` sub-headings are also
close enough in shape to `### R-nnnn — handle` that a parser reading headings
will file them as requirement blocks. The text below is the section as it
stood; the section heading became this file's title and nothing else was
touched, so it still describes the register as it read when it was written —
including blocks that have since been killed.

---

### 1 — Forty-six requirements have no honest Why, and one reason explains all of them

Forty-four of the 51 blocks carry the same `Source` in the old register:

> `2026-08-07/08 session — docs/product/requirements-traceability.md`

Two more carry the same shape with a different date (`2026-08-08 session —
docs/product/requirements-traceability.md`): R-0050 and R-0051.

That string is a **pointer to where the words came from**, not a reason the
requirement exists. It supports no Why at all. Writing one from it would be
manufacturing rationale, so none was written. The forty-six:

R-0001, R-0002, R-0003, R-0004, R-0005, R-0006, R-0007, R-0008, R-0009,
R-0010, R-0011, R-0012, R-0013, R-0014, R-0015, R-0016, R-0017, R-0018,
R-0019, R-0020, R-0021, R-0022, R-0024, R-0025, R-0026, R-0027, R-0031,
R-0033, R-0034, R-0035, R-0036, R-0037, R-0038, R-0039, R-0040, R-0041,
R-0042, R-0043, R-0044, R-0045, R-0046, R-0047, R-0048, R-0049, R-0050,
R-0051.

*(That list is 46 references; 44 carry the 2026-08-07/08 pointer and two —
R-0050 and R-0051 — carry the 2026-08-08 one. All 46 need his words.)*

**Four have a partial Why** — R-0028, R-0029, R-0030, R-0032. Their source
carries one verbatim ruling of his, *"UX-001 was for the eval matrix only"*
(2026-08-08 21:23), which honestly explains **the scope** of the statement
and nothing else. What is written is exactly that, and it says on the page
that the reason itself is still missing.

**One has a full, honest Why** — R-0023. Its old source carried his words
verbatim and in full; they are carried across unchanged, under the reserved
italic-quotation form.

The register is therefore 1 honest Why, 4 partial, 46 needing his words.

**The single sentence that matters here:** the old register's `Source` field
was a *provenance pointer*, and the new format's Why is a *reason*. The
migration cannot convert one into the other, and no amount of care makes it
possible. This is not a transcription defect — the content never existed.

### 2 — One requirement could not be traced

**R-0031 — "Diagrams render in a sans-serif font."** No goal and no law is
served by it without inventing a rationale. G4 is about a message being
readable rather than a wall of noise, and stretching that to cover a font
family is exactly the forced trace the brief said to refuse. It is left as
`not yet traced` and named here.

Two traces I want you to check rather than trust, because they were the
closest calls:

- **R-0005** (project type and release type are one vocabulary) → **G3**. My
  reasoning: collapsing two type vocabularies into one is in service of "one
  path". It is a definitional claim, and G3 is a defensible but not obvious
  home.
- **R-0039** ("Never route to superpowers") → **G8**. My reasoning: G8's
  grounding in the goals file carries *"i just want the process to be ours
  and visable"*. That is the nearest honest anchor, but the requirement
  itself names no goal.

### 3 — No statement wording was changed

> **ACTED ON 2026-08-14 (late) — this section records the state before the
> rework and is kept for the record only.** The recommendation below was to
> settle open question 5 first, then reword the twelve as one pass. That was
> followed, with one correction: **open question 5 turned out to be two
> questions**, and only one of them was the producer's. Its research half —
> *the technique for carrying universal force without a totality word is
> nowhere taught* — **was false**, and Law 4 caught it: the technique is
> taught by EARS's ubiquitous pattern and by ISO 29148's own `each` rule, the
> same standard this word list came from. The rework is recorded in section 8
> below. **The list of twelve is also superseded**: three were killed at the
> 2026-08-14 triage, one is deferred to the producer, and one the list missed
> was found by machine scan.

Zero statements were reworded. The brief permitted fixing what the format's
plain-language rules require; I did not exercise it, and the reason is a
judgement you should be able to overturn.

The adopted ISO 29148 word list bans totality words (`all`, `always`,
`never`), superlatives, and vague subjects, and holds that `shall` binds.
Rewriting 51 statements into shall-form is **authorship**, not
transcription — it runs straight into your standing law against
paraphrasing requirements, and the format's own open question 5 admits the
technique for carrying universal force without a totality word *"is nowhere
taught"*. So the statements are verbatim and the violations are listed
instead.

**Statements that fail the word list as they stand:**

| Reference | The problem |
|---|---|
| R-0003 | `never invent one` — totality word |
| R-0007 | `not merely a record` — not a checkable clause |
| R-0012 | `never a sentence` — totality word |
| R-0024 | `never a reason to record less` — totality word |
| R-0028 | `boxes are never coloured` — totality word |
| R-0036 | `nothing in Kerd, ever` — totality word |
| R-0038 | `never at its own install path` — totality word |
| R-0039 | `Never route to superpowers` — totality word **and** no subject at all |
| R-0040 | `never embedded in a product doc` — totality word |
| R-0043 | `never a parallel store` — totality word |
| R-0045 | `it never rewrites the state` — totality word |
| R-0051 | `never on a question the model answers about itself` — totality word |

Most of these are absolute laws expressed with an absolute word, which is
the exact case open question 5 has not settled. **Recommendation: settle
open question 5 first, then reword these twelve as one pass — not
requirement by requirement.**

**One change I did make, and it is notation not content:** every heading
handle is fresh. The old headings were mechanically truncated statements
("…plan enhancements, plan…"), which rule 3 says a handle must not be. Under
rule 3 a handle sits outside the fingerprint and may be reworded at any
time, so this costs nothing and can be overruled freely.

### 4 — What the new format has no home for

Named so it does not vanish silently.

**a. The `refines` link role — collapsed, and this is the one I am least
comfortable with.** The old register had 15 link lines in two roles:
11 `depends-on` and **4 `refines`** (R-0009, R-0010 and R-0012 refining
R-0008; R-0049 refining R-0011). The new format's rule 8 gives one link
between requirements — `Depends on` — and rule 7 reserves `Traces to` for
goals and laws only. So `refines` has nowhere to go. I mapped all four onto
`Depends on`, keeping the direction, on the ground that a refinement
genuinely needs its parent to exist. **The parent/child relationship itself
is lost**, and with it the "is this an origin requirement or a refinement?"
question that the shape doc's own `no parent, by design` marker is built to
answer. Recommend either a second link role or an explicit ruling that
refinement is not modelled.

**b. The suspect-link stamps — dropped, and the shape doc wants them
kept.** Every old link carried its target's hash: `depends-on → FUN-005
(sha256:b76da5ae7fe2)`. Fifteen stamps. Rule 8 says `Depends on` takes
"references only", so there is no slot for them. This is a live
contradiction inside the shape doc itself: its comparison section says of
the suspect-link stamp *"Recommend keeping it; the new draft's links element
is compatible with it"* — but the normative form has no place to write one.
**Recommend resolving this in the format before the migration lands.**

**c. The `Category` field.** All 51 carried one of the twenty codes. The new
reference is deliberately meaning-free and the shape doc recommends
categories become tags. There is no category slot in the block. The taxonomy
survives as *content* (R-0003 requires it to ship) but the per-requirement
filing key is gone.

> **OVERTAKEN 2026-08-14 14:54.** The content half is gone too — R-0003 was
> killed on the producer's ruling that the twenty subject areas are dead, not
> demoted and not kept as a reference list. The taxonomy now survives in
> neither form, so nothing here is left to decide.

**d. The `Tags` field.** Twelve requirements carried tags recording the other
disciplines they touch. No home, and unlike categories, nothing else in the
new format records them.

**e. The `State` field, and four requirements that were not `final`.** The
no-status decision is settled, and the migration's blanket unapproval
happens to be correct for all 51. But the old register distinguished
*proposed* (captured, never qualified) from *final* (approved and later
un-approved by a format change), and that distinction is now invisible. The
four never-final requirements were:

- **R-0022** (`route` and rigor derived) — was `qualified`
- **R-0025** (floors compose as a union) — was `proposed`
- **R-0038** (machinery aims at consuming project) — was `qualified`
- **R-0048** (every type owes every gate) — was `proposed`

Under the new file these read identically to the other 47. If "this was
never agreed at all" is worth telling apart from "this was agreed and the
format un-agreed it", the format has no way to say so.

**f. Forty-seven approval hashes.** Deliberately dropped, per the brief.
Recorded here as a count so the scale of the re-approval debt is visible:
47 previously-approved requirements now sit unapproved.

### 5 — What the format did not tell me how to handle

1. **A Why that cannot be written.** Rule 1 requires all five fields and says
   an inapplicable field writes `none`. But a Why is not *inapplicable* — it
   is *missing*, and `none` would assert the requirement has no reason,
   which is false. I wrote an explicit unwritten-Why sentence naming what
   the source actually said. The format has no sanctioned form for this and
   should get one, because a migration is not the last time it will happen.
2. **A trace that is not yet known.** Rule 7 offers targets or
   `no parent, by design`. It has no value for "not yet determined", and
   using the by-design marker would be a false declaration. R-0031 carries a
   written-out unknown instead.
3. **Bulk minting.** Rule 2 says filing refuses a block arriving with a
   pre-written number and the tool assigns. There is no tool, and 51 numbers
   were assigned by hand. The rule has no migration path.
4. **Migration ordering.** Rule 13 says ascending reference order is creation
   order. A migration has no creation order, so I minted in the old
   register's reading order (PRD → FUN → NFR → UX → TECH → OPS → TST). That
   preserves the document you already read, but it bakes the dead category
   taxonomy into the reference sequence permanently — the one encoding rule
   2 exists to avoid. Worth a conscious ruling before this file replaces the
   old one.
5. **A forward dependency.** R-0007 depends on R-0041 — a higher number. The
   format forbids nothing here, but under natural creation order a
   dependency would normally precede its dependent, and this file has one
   that does not.

### 6 — Recommended for the graveyard, not moved

> **ACTED ON 2026-08-14 — this section records the state before the kills and
> is kept for the record only.** Four of the six named below were killed and
> moved (R-0045, R-0016, R-0017, R-0002), together with four this section
> never named (R-0001, R-0004, R-0034, R-0039), on the fuller triage in
> `docs/requirements/triage.md` and with Tony as the named authoriser. **Two
> of the six were not killed:** R-0003 stays live as this section recommends,
> and **R-0044 stays live against this section's recommendation** — the
> triage found its render detail *is* the approved render (level-three
> heading, bold labelled lines, statement as text, links near the end,
> liftable as a unit), so it predicted rule 1 rather than contradicting it.
>
> **R-0003 did not stay live for long.** It was killed later the same day, at
> 14:54, on the producer's ruling against the twenty subject areas — for a
> reason this section could not reach, because the research that settled it had
> not been commissioned when this was written. Its recommendation to leave
> R-0003 live and decide the categories question separately is superseded: the
> question was decided, and decided against it.

Each of these is contradicted or overtaken by the format we are migrating
*into*. I have left all six in the live set. Moving one is a kill, and rule
10 requires a named authoriser, which is you.

**R-0045 — "A `final` requirement carries a hash of its statement as
keyed."** The strongest case. It names the `final` state, which no longer
exists, and a fingerprint over the statement alone, which the recipe now
overrides (statement, Why, links). Its surviving payload — *the audit
refuses on divergence and never rewrites the state* — is genuinely valuable
and is already carried by rule 9. Recommend: killed, superseded by whatever
requirement eventually states the fingerprint recipe.

**R-0016 — "Every requirement gets a Category and ID."** Half of it is dead
outright: the shape has no Category. The other half is now rule 2.
Recommend: killed and re-proposed as an identity requirement without the
category clause.

**R-0017 — "Any request is qualified; if durable it becomes a requirement,
through stages to final."** *"through stages to final"* names the
five-state lifecycle the shape deliberately cut. The qualification idea
survives; the stages do not. Recommend: killed and re-proposed without the
lifecycle clause.

**R-0002 — "…and speak in IDs that mean something."** This is a direct
collision, and it is the one I most want you to look at — see below.

**R-0044 — "A requirement is a block, not a table row — heading, bolded meta
lines, statement as text, links as a trailing list."** The principle
(*liftable as a unit*) survives and is exactly what rule 1 implements. The
render detail it specifies is no longer the render. Recommend: killed and
re-proposed as the principle alone.

**R-0003 — the twenty-category taxonomy ships as the default.** Not dead,
but at risk: the shape doc recommends the categories become tags and the
reference go opaque, and it flags that as its own decision with a real cost.
Recommend: leave live, decide the categories question separately.

### 7 — The one thing to look at first

> **CLOSED 2026-08-14 — the question below no longer needs answering, and it
> did not need escalating.** The migration had already struck the offending
> clause in this same file under Law 4's ordering rule (*"if the analysis
> proved a better way, then we go agaist what i said before, we chnage the
> rule"*), which was the correct application of that rule; escalating a
> question your own governing rule has already answered is how the loop it
> exists to prevent gets started. R-0002 was then killed on 2026-08-14 for a
> different reason entirely — what remained after the amendment states a
> purpose, not an obligation — and is in the graveyard. This section is kept
> for the record only.

**R-0002 — "Requirements exist so the producer can review, plan
enhancements, plan releases, and speak in IDs that mean something."**

That requirement is approved in the old register, in your name, and its
final clause is the exact opposite of rule 2 of the format we are migrating
into: *"The uniform `R-` prefix carries no meaning — every requirement wears
the same one."*

The migration has just replaced `PRD-002` — an identifier that told you it
was a product requirement — with `R-0002`, which tells you nothing. The
research reason for that is strong (*every scheme that encoded meaning in
the identifier eventually had the meaning change*) and the shape doc knows
it costs something. But a live requirement in this file now says the
opposite of the file's own numbering rule, and nothing in the format
notices.

The two readings are genuinely different and only you can pick one: either
"IDs that mean something" meant *IDs I can say out loud and point at* — in
which case `R-0002` satisfies it and the requirement stands unchanged — or
it meant *IDs that tell me what kind of thing this is* — in which case
either the requirement goes to the graveyard or rule 2 is wrong.

---

### 8 — The word-list rework, 2026-08-14 (late)

Nine live statements were reworded. **The obligation is unchanged in every
case** — only the construction carrying universal force changed. Where a
rewording would have altered what a requirement demands, it was not made and
is named below instead.

**The technique, and why it is not invention.** Section 3 recommended settling
open question 5 first. OQ5 was two questions welded together, and only one is
his:

- **His, still open** — does the writing help *refuse* or only *advise*? That
  decides whether a rule blocks or informs.
- **Not his, and now closed** — how do you carry universal force without a
  banned totality word? The shape doc said the technique *"is nowhere
  taught"*. **That was wrong.** EARS's **ubiquitous pattern** carries
  universality structurally (a requirement with no keyword, no trigger and no
  precondition is always active — so `always` is redundant, not merely
  banned), and ISO 29148 — the source the word list itself came from —
  supplies `each` for universal qualification. Recorded in
  `docs/design/requirement-shape.md` under *Carrying universal force without a
  totality word*, ADOPTED from both.

The rewording did not need the missing Whys. **Rewording is safe without the
Why; supplying missing force or a missing subject is not** — that line was held
across the pass and the one block that crossed it is deferred.

**Zero fingerprint cost.** All nine stood at `Approval. none`, so no approval
was invalidated and no published test vector moved. Both vectors still
reproduce; the register passes all ten format checks.

| Reference | Before | After |
|---|---|---|
| R-0012 | `…states why, in a few words — **never** a sentence` | `…shall state why as a phrase of a few words, not as a sentence` |
| R-0024 | `records **everything** agreed; efficiency is a tiebreaker, **never** a reason to record less` | `shall record **each** thing agreed; efficiency shall serve **only** as a tiebreaker between designs that preserve that record` |
| R-0028 | `**In the evaluation matrix**, boxes are **never** coloured` | `**Where** the render is the evaluation matrix, the box shall remain uncoloured` |
| R-0036 | `…— nothing in Kerd, **ever**` | `…; Kerd shall hold **no project state**` |
| R-0038 | `**must** aim at…, **never** at its own install path` | `**shall** resolve its target to…, **not** to its own install path` |
| R-0040 | `— **never** embedded in a product doc —` | `; a product doc **shall not** contain it` |
| R-0043 | `**must** be the same files…, **never** a parallel store` | `**shall** be the same files…; the tooling **shall not** maintain a parallel store alongside them` |
| R-0051 | `**must not** be a step the model can assume or skip…, **never** on a question…` | `**shall** bind on countable facts produced outside the model, so that the model can neither assume nor skip it; it **shall not** bind on a question…` |
| R-0050 | `working from the RAW sources, **never** from a summary` | `working from the RAW sources **rather than** from a summary` |

**R-0028 is the one that changed shape, and it is the argument for the
technique.** `boxes are never coloured` reads as a universal law. It is not
one — its scope was corrected by the producer on 2026-08-08 (*"UX-001 was for
the eval matrix only"*) and that scope was carried in **bolded prose**, where
nothing enforces it. Choosing the EARS pattern forced the question *is this
genuinely universal?*, and the answer was no. The scope now sits in the
requirement's structure (`Where …`) instead of in its typography.

#### Three that were on the list of twelve and are already dead

R-0003, R-0039 and R-0045 were killed at the 2026-08-14 triage. Section 3 was
written before those kills, so its table of twelve overstates the live work by
three. No action.

#### One deferred to the producer — R-0007

**`The register is the data source for release planning, dependency and
visualization tooling — not merely a record`**

The only one of the twelve whose defect is **not** a totality word. Section 3
flags it as *not a checkable clause*, and it is: `not merely a record` says
what the register is not, and nothing about what it must do. Making it
checkable means deciding what the register owes the tooling — **that is the
obligation itself, not its grammar**, and writing it would be authoring the
requirement rather than rewording it.

The two readings, which only he can pick:

- **A format guarantee** — the register must be machine-parsable to a declared
  schema, so a tool can consume it without a human step. Checkable, and
  already true (the view's parser reads it).
- **A dependency direction** — the tooling must read the register rather than
  keep its own copy of the same facts. Also checkable, and close enough to
  R-0043 that it may be a duplicate.

Left verbatim and unapproved until he rules. Its Why is one of the 38 and
would probably settle it in the same breath.

#### One found by machine scan that the list missed — R-0050

The list of twelve was compiled by reading. A scan of every live statement for
banned words found **R-0050** carrying `never from a summary`, which the
reading missed. Reworded above.

**This is yesterday's lesson repeating one level down.** The register was
audited twice by reading; a mechanical pass found the miss in seconds. Reading
and scanning are different tests, and the same gap that let three format
defects survive four reviews let one word-list violation survive the audit that
existed to catch exactly it.

#### One judgement call left open — should `every` join the banned list?

The scan flags **R-0048** (`Every work item owes every gate unless it
explicitly marks that gate n/a with a named reason`). `every` is **not** on the
adopted word list, which names `all / always / never`. The statement is also
bounded — it carries an explicit exception clause, so it is checkable as it
stands.

Not changed, because **widening the word list is a change to the rule, and the
rule is his.** ISO 29148's `each` guidance would prefer `Each work item shall
owe each gate…`, which is a nudge rather than a violation. Named here so the
decision is visible rather than silently taken either way.

---

### 9 — Retiring the old register would silently disarm the refuser

**Investigated 2026-08-14 (late). NOT acted on — this one needs a ruling.**

`docs/requirements/register.md` is superseded by `register-v2.md` and the TODO
calls retiring it *"a deliberate act, not a cleanup"*. It is more than that: it
is **coupled to the only machine refusal the requirements work has.**

`kit.register_check()` reads `docs/requirements/register.md` by name, and its
declared behaviour is a **vacuous pass when the file is absent** — keeping a
register is opting in (kit.py:829). So deleting the old register does not turn
CI red. It turns AU7 and AU8 **silent**, and nothing reports that they stopped
having anything to check.

That is the whole of the repo's requirement refusal: illegal IDs, states and
categories, unknown fields, `Approved` hash divergence, `superseded` without
its `superseded-by`, unregistered link roles, dangling targets. All of it
aimed at a file that would no longer exist.

**The new register is not covered by it.** AU7 expects the old identifier shape
(`^[A-Z]{2,4}-\d{3}$`); `register-v2.md` uses `R-nnnn`. The new format's ten
checks live in `tools/reqview/reqview.py`, which is **a spike and is not in
CI**. So today the position is:

| | validated by | in CI |
|---|---|---|
| `register.md` (dead content) | AU7/AU8 in `gate.py audit` | yes |
| `register-v2.md` (live content) | `reqview.py` format checks | **no** |

**The refusal is pointed at the wrong file, and has been since the migration
landed.** Retiring the old register does not cause that — it makes it visible.

**Why this was not fixed here.** The obvious repair is to give the new format
the same treatment AU7/AU8 got — riding `gate.py audit`, no new CI step, the
AU5/AU6 precedent. But the checks currently live in a **spike that has not been
through the gates**, so wiring CI to depend on it is a coupling decision, not a
mechanical one. The alternative — reimplementing the checks inside `kit.py` —
creates a second parser for one format, which is the drift the single-serializer
rule exists to forbid.

**The ruling needed, and it is one sentence:** does the new format's validator
graduate out of the spike and into `gate.py audit` before the old register is
retired, or does the old register stay in place until it does? Either is
defensible; doing neither leaves the live register unrefused.

---

### 10 — The riddle pass: 39 titles and 29 descriptions rewritten, 2026-08-15

**The producer read a few and stopped:** *"the descriptions and titles are like
puzzles, riddles."*

He was right, and the diagnosis is one sentence: **the subject was implied and
never named.** R-0008 through R-0012 are all about the evaluation matrix and
only one of them said so. Read in the room, an hour into a conversation about
evaluation matrices, *"the cross takes no modifier"* is obvious. Read cold six
weeks later it is unanswerable — what cross, on what?

That is what the migration inherited. The old register was filled from the
middle of the chain outward, each row a shorthand for the conversation that had
just happened.

**The fix was a rule already adopted and applied to only nine blocks.** EARS
requires naming the subject — `the <system> shall <response>` — and the
2026-08-14 pass applied it to the nine statements carrying banned totality
words. The other thirty kept their shorthand. This pass finishes the job.

**Two conventions, agreed on three worked examples before the pass ran:**

- **A title names its subject first** — `Subject — what it says`, not the
  punchline alone.
- **A description names what it is about before what it demands.**

| | Before | After |
|---|---|---|
| R-0009 | `the cross takes no modifier` | `Evaluation marks — the cross has no degrees` |
| R-0012 | `a lesser mark says why, briefly` | `Evaluation marks — anything below ○ says why` |
| R-0006 | `the alignment gate is a shared structure` | `Agreeing a design — both parties point at one structure` |

**Cost: zero.** Nothing is approved, so no fingerprint broke; and rule 3 puts
the handle outside the fingerprint permanently, so titles are free at any time.

**39 titles rewritten. 29 descriptions rewritten. Ten left verbatim** because
they already named their subject — R-0007, R-0024, R-0028, R-0036, R-0038,
R-0040, R-0043, R-0048, R-0051, R-0052.

**Two deliberately not touched beyond their titles:**

- **R-0007** — its open question is unchanged: `not merely a record` is still an
  uncheckable clause, and making it checkable decides what the register owes
  the tooling. That is the obligation, not its grammar. Still his (§8).
- **R-0048** — still carries `every`, which is not on the adopted word list.
  Widening the list is a change to the rule, and the rule is his (§8).

**Verified after the pass:** the register parses, 10/10 format checks, 0
refusals, 39 live and 13 dead unchanged, 10 dependency links unchanged, both
fingerprint vectors reproduce, and **zero live statements carry a banned
totality word**.

**One accident worth recording.** Every new title contains an em dash, which is
the exact input that silently truncated handles until it was fixed the night
before. Had the pass run a day earlier it would have quietly shortened all 39
titles and refused nothing.

> **SUPERSEDED the same day.** The `Subject — what it says` convention below was
> replaced within the hour. The producer's next reading: *"can we also use
> natural languge and not haikui?"* — the titles were compressed aphorisms, not
> sentences anyone would say aloud. Titles and descriptions were rewritten again
> as plain sentences, which name their subject naturally without needing the dash
> construction, and then a third pass applied his actual test: **"if my mum can
> read it then its fine."** That test caught what the first two passes did not —
> `ships a change`, `distinction`, `rigor`, `mechanism`, `repository`, `block`
> are all words we use here and nobody else does. Fourteen blocks were rewritten
> again to remove them. The rule that survives is his, not mine: **a requirement
> is written for someone who does not work here.**
