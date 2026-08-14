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
