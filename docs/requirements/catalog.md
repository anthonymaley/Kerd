# Requirements catalog — the schema

What a requirement *is* in this project: which fields exist, which are
required, what a state means and what it owes, which links are legal, and which
fields each surface shows.

**Declared separately from the register on purpose.** Measured 2026-08-08:
StrictDoc's default `REQUIREMENT` node has eight fields and **none of them is
mandatory** — required-ness is a per-project declaration, not a vendor opinion,
and it lives in a grammar block that can be shared across documents. This file
is that grammar.

**A consuming project REFERENCES this catalog rather than copying it.**
StrictDoc's mechanism is `IMPORT_FROM_FILE` — one schema file serving many
documents — and the distinction is load-bearing: a copy drifts silently and
nothing can tell you it has. A project extends the catalog by declaring
additions beside the reference, never by editing a duplicate.

> **On this directory's name.** `docs/requirements/` was the output path of
> `capturerequirements`, the skill cut at v0.73.0 — cut partly *because* that
> path produced **dated snapshots**, which violated the date-split rule and
> re-created measured scatter. The standing rule is that dead solutions stay
> dead unless a named return condition fires. **The named condition: the defect
> that caused the cut is not reproduced here.** These are living files,
> overwritten in place, with no date in any filename. The path returns; the
> shape that killed it does not.

## Fields

**The ID prefix is the PRIMARY discipline, not the only one.** Added 2026-08-08
after measuring how the four mature requirements tools actually classify:
StrictDoc has **no category field at all** (structure comes from document
sections, classification from free tags); Doorstop classifies by **which
document you are in**, a parent/child tree; Sphinx-Needs uses a `type` of four
or five lifecycle values plus tags; ReqIF reserves `ReqIF.Category` as a slot
and never says what goes in it. **None of the four uses a twenty-way mutually
exclusive partition as its filing key** — every one pairs a small exclusive key
with many non-exclusive tags.

Twenty-way exclusion is hard at speed and most requirements are genuinely
multi-aspect: *"boxes are never coloured; the mark carries the verdict"* is a UX
rule and a functional rule, and forcing one bucket destroys the other. The only
thing that forced exclusivity here was `<CODE>-<NNN>`, because an ID carries one
prefix.

**The producer's three jobs never needed exclusivity.** Review a category as a
set, judge an enhancement's blast radius, name a release as a set of IDs — all
three are *filtering* jobs, and filtering works on tags. So the prefix stays his
format and keeps "speak in IDs that mean something"; `Tags` records what the
single bucket used to destroy; and choosing which discipline is *primary* is a
far easier call at speed than choosing the only one.


| Field | Required | Type | Notes |
|---|---|---|---|
| ID | yes | `^[A-Z]{2,4}-\d{3}$` | The code must be one of the twenty below. Widened from `{3,4}`, which rejected `UX-001` — a shipped code and the frame's own worked example. |
| Category | yes | one of the twenty codes | Its disposition in `categories.md` must be `applies`. |
| State | yes | one of the five below | |
| Statement | yes | free text, may be multi-line | The producer's words, compressed but never paraphrased into the model's vocabulary. |
| Source | yes | free text | Where it came from, so the full wording stays reachable. |
| Approved | when `final` | `sha256:<12 hex>` | The statement as it read when keyed. See **State obligations**. |
| Tags | no | zero or more of the twenty codes | **The other disciplines this requirement touches.** The ID prefix names the PRIMARY one; tags carry the rest. |
| Title | no | free text | Currently the heading. Earns its own field when a statement outgrows one line. |

**An unknown field is a hard error**, not a warning — the same rule StrictDoc
enforces under its default grammar. A field nobody declared is either a typo or
an undeclared extension, and both should stop the run.

**Field ORDER is NOT enforced, deliberately.** StrictDoc does enforce it, and it
is the single decision in that format actively hostile to a model editing a
file — Kerd's entire capture beat is a model editing a file, so the one thing
not copied is copied nowhere.

**Deferred, each with a return condition** — Priority (returns when a release
object exists to consume it), Owner (returns on the first register with two
writers), Acceptance Criteria and Verification Method (the forward trace, slice
2), Project Type (returns with the project-type work), Subtype (appears exactly
once in the whole repo with no legal set — must not be built until one exists).

## The twenty categories — the filing key

Each definition carries three things: **who owns it**, **the one question that
decides it**, and **the boundary against its nearest neighbour, with a real
requirement from this register as the bait**. Examples do not decide edge cases;
these questions do.

Every question is answerable **with one block visible and the rest of the file
covered.** That is deliberate: a key that needs you to know where a *related*
requirement was filed makes the answer depend on filing order, which a first
attempt did and which is fatal.

**The four that blur, resolved as one axis in four positions:**

> **PRD** leaves order and materials open · **FUN** pins order · **TECH** pins
> materials · **NFR** pins degree.

**For a compound sentence, file on the decision whose removal makes the other
pointless.** `TECH-010` carries a fingerprint *and* a refusal — remove the hash
and the refusal has nothing to fire on, so it files TECH.

Rows marked ⚠ are ones the drafting pass declared **low confidence**, almost all
because the category holds zero requirements and its definition has never met
real data.

| Code | Owner | The question that decides | Not this — and the bait |
|---|---|---|---|
| `BUS` ⚠ | Whoever can stop paying for it. Business owns the sentences whose stake is counted outside the thing being built. | Is what is at stake counted OUTSIDE the thing being built — money, time bought, people's hours, or standing among parties who owe you nothing — so that no amount of building it differently changes the number? | Nearest is STA. Take 'Sales asked for a one-page summary they can send out.' Apply the question: is the stake money, hours, or standing among strangers? No — the stake is one party's want, and a different build satisfies it. Returns NO. The separator: BUS is answerable in a number nobody here controls; STA is answerable by asking one person if they are happy. |
| `STA` ⚠ | Whoever carries an outside party's ask into the room. Stakeholder owns sentences that exist because somebody not building the thing spoke. | Does the sentence exist because somebody who is not building this asked for something, such that dropping it means going back to a named party and telling them no? | Nearest is USR. Take 'A colour-blind producer must be able to read every verdict without relying on colour.' Apply the question: did somebody outside ask for it, such that dropping it means telling a named party no? No — nobody asked; it binds because of a capacity that exists whether or not it was ever raised. Returns NO. The old wording's 'will never operate the thing' clause is deleted outright: it was false of customers, support and contributors, and it made STA unfillable. Provenance is the axis, not whether the party touches the product. |
| `USR` | Whoever answers for the human at the controls. User owns the sentences that make the thing bend around that human. | Does the sentence force the thing to FIT a person — bending to a limit, a habit, or a setting they brought with them — and would it still bind if nobody had asked for it? | Nearest is PRD, and PRD-002 is where the previous attempt broke. 'Requirements exist so the producer can review, plan enhancements, plan releases, and speak in IDs that mean something.' Apply the question: does it force the thing to bend around a limit or a habit? No — it states why an artifact exists. The four job-shaped verbs are its stated purpose, not a limit or habit anyone has, and filing on the purpose is exactly the keyword move that produced the error. Returns NO on clause one. The cancellation-survival clause from the earlier draft is deleted: it rejected accessibility and jobs-to-be-done wholesale, because every user obligation mentions the thing and no thing survives cancellation. |
| `PRD` | The producer, fixing what there is and what the words mean. | Does the sentence fix a NAME — putting something into what the project offers, ruling something out of it, or settling what a word will mean — rather than fixing how well, how it looks, when it happens, how it is built, or how it is proved? | Nearest is NFR, and NFR-003 is the bait because it reads as a list of five items: 'A spike carries its own rigor: scope boundary, timebox, spec, design, and measurements.' Apply the question: does it fix a name, or how well? The sentence names its own object in its own words — 'its own rigor' — and rigor is a level of care, not a member of what the project offers. Returns NO. The separator: PRD adds to what a user gets; NFR raises what the work owes. The old residue test ('leaves order and materials free') is deleted entirely, along with its cross-requirement tiebreak — that tiebreak was the constraint-3 violation, because it could only run with TST-002 held open beside the sentence. |
| `FUN` | Whoever specifies what the machine does with work in flight. | Name the thing the sentence changes. Is it work in flight — a step taken, the point at which it is taken, who may take it, or a value worked out from another — rather than a check, a record's shape, a look, or which mode the operator must be in? | Nearest is TST, and TST-004 is the bait because it carries two moments in plain sight: 'the LIGHT check fires at every step; BOTH light and heavy fire at the design GO.' Apply the question: name the thing it changes. Not the work — the check's own tiering and firing. A schedule attached to a check changes the check, not what flows through the machine. Returns NO. This is why the question asks what the sentence CHANGES rather than whether a moment appears in it: a moment appears in almost every sentence that mentions a gate. |
| `NFR` | Whoever answers for how well the whole thing holds up and how much care the work owes. | Could the thing be exactly right and still fail this — by being less complete, less thorough, less sound, or costlier to live with — where the shortfall is in the DOING rather than in how it reads on a page? | Nearest is UX, and UX-006 is the exact bait: 'The point of a table is to avoid reading lots of text to understand it — brevity is the requirement, not a preference.' A verbose table did the work right and reads badly, so the degree clause fires — and the observer clause stops it: the shortfall is in how it reads on a page. Returns NO. The 'dial not binary' separator from the earlier draft is deleted, because it rejected NFR-002 and NFR-003, two of NFR's own four rows. The degree axis was right; the dial framing was not. |
| `UX` | Whoever answers for what meets the eye and the hand. | Name the thing the sentence rules on. Is it a SURFACE somebody looks at or acts on — its colour, size, shape, wording density, or what they must do to it — rather than a member of a set, a record's slot, or a check? | Nearest is PRD, and PRD-012 is the bait because length is visible: 'A mark that is not ◎ or ○ states why, in a few words — never a sentence.' Apply the question: name the thing it rules on. A mark that is not ◎ or ○ — a member of the legal set — and what that member must carry. Not a surface. Returns NO. The old glance test is deleted: perceptibility does not track presentation ownership, and it imported PRD-012 and TECH-009 wholesale. The noun does the work, not the visibility of the violation. |
| `TECH` | Whoever answers for how it is put together. | Does the sentence fix how the thing is CONSTRUCTED — where it sits, what it is made of, what shape a machine must read it in, which slots a record carries, or how one record points at another — such that somebody could honour it without knowing what the thing is for? | Nearest is NFR, and NFR-004 ('The mechanism must not scatter artifacts') is the bait because scatter sounds like a place. Apply the question: does it fix where anything sits? It names no location, no shape and no slot — only that outputs must not spread. And you cannot honour it without knowing what the mechanism produces, so the last clause fails too. Returns NO. The separator: TECH names a place or a shape; NFR names a degree. The old invisible-swap test is deleted, not narrowed — it returned NO on eight of TECH's own ten rows, which is a test that does not cover its own category. |
| `INT` ⚠ | Whoever holds the seam with a system nobody here controls. | Does the sentence name a specific interface owned by somebody else — a format, an address it must reach, a file shape, a payload — that our side must match, or hand something across to be read by software this project does not ship? | Nearest is TECH, and TECH-004 ('Never route to superpowers') is the keyword bait — it names an outside thing by name and nothing else. Apply the question: does it name a format, an address, a file shape or a payload we must match? No; it names a destination we refuse to send to, and hands nothing across. Returns NO. The old 'would this be the thing that broke' wording is deleted: it inverts the value of every defensive seam requirement, because a version pin exists precisely so that you do not break. |
| `DATA` | Whoever answers for the record itself, after it is written. | Does the sentence bind the record itself once written — how long it survives, whether it may be altered, when it must go, or how faithfully it mirrors what it stands for — rather than binding the machinery that produces it? | Nearest is TECH, and TECH-006 ('A requirement row carries its dependencies on other requirement IDs') is the bait because a record is right there in the sentence. Apply the question: does it bind what becomes of that record once written — survival, alteration, destruction, fidelity? None of the four. It adds a slot. Returns NO. The separator is time: TECH shapes the container, DATA governs the contents' life afterwards. The three life-verbs of the earlier draft are gone; 'must come into being' is true of every recording requirement in every category and discriminated nothing. |
| `SEC` ⚠ | Whoever answers for who may reach a thing, and for who did. | Does the sentence control WHO or WHAT may reach something, or preserve the ability to say afterwards who did reach it? | Nearest is PRIV. Take 'a named contributor may demand their verbatim words be removed from committed session logs.' Apply the question: does it control who may reach something, or preserve who did? Neither — it controls whether the project may hold the words at all, and one person's standing is the trigger. Returns NO. SEC's axis is reach; PRIV's is whose the fact is. The adversary-intent clause of the earlier draft is deleted: it was one Covers sub-type promoted to the whole test, and it returned NO for an append-only action log and for an authorization rule, which are two more. |
| `PRIV` ⚠ | Whoever answers to the individual a record is about. | Is the sentence here because a record is ABOUT one identifiable human — their words, their traces, their circumstances — such that that human, and not the project, says whether it may be held or shown? Authority to write, key or rescind a requirement is never standing: every row in this register has that, and it discriminates nothing. | Nearest is CMP. Take 'design records must be kept for seven years because the certification body requires it.' Apply the question: is a record about one identifiable human, whose say-so governs? No — no individual can release you, and no individual is its subject. Returns NO. Where both fire — an employer's policy that requires you to honour a person's deletion demand — that is two requirements, not one: the individual's entitlement files PRIV and the body's requirement files CMP. The earlier draft's separator asserted that configuration cannot occur; it can, and it is the ordinary shape of regulated privacy. |
| `CMP` ⚠ | Whoever answers to an authority that can punish the project. | Is the sentence imposed by a body that could penalise the undertaking for ignoring it, and that the undertaking cannot escape by choosing different software or a different supplier? | Nearest is TECH, and a platform manifest is the bait: '.claude-plugin/plugin.json must carry name, version and description in the shape the plugin system parses, or the plugin does not load.' Apply the question: could the plugin system penalise the undertaking? It penalises nothing; it declines to load. And could the undertaking escape by choosing different software? Yes — by not shipping a plugin. Returns NO on both clauses, and it files TECH. The bare 'would it survive a unanimous vote' wording captured every externally imposed format, which is most of TECH and all of INT. |
| `ANA` | Whoever builds the instrument that counts. | Does the sentence build an INSTRUMENT — what gets tallied, how, and where the tally lands — while saying nothing about what anyone must do once they read it, and producing a number rather than a verdict? | Nearest is TST, and TST-004 is the bait because it enumerates countable facts and keeps firing forever: 'the LIGHT check fires at every step … did the register move, do approval hashes still match, are link stamps stale, does declared grounding resolve.' Apply the question: does it produce a number somebody reads, or a verdict that stops something? A verdict. Returns NO. The old 'the counting continues after the work is over' clause is deleted: it was written against a one-shot boundary check, it does not survive a recurring one, and it expelled experimentation, which ends by definition. The output separates these, not the duration. |
| `OPS` | Whoever keeps the running thing running. | Is the sentence about a live instance going wrong, or about something kept ready for that moment — a way back in, a written recovery route, a warning — rather than about a step the design already calls for? | Nearest is FUN, and FUN-007 is the bait because it says 'mid-flight' in as many words: 'Conductor may suggest a type change — at the gate or mid-flight — and the producer agrees it.' Apply the question: is anything going wrong, or being kept ready for a fault? Neither; a suggested type change with the producer agreeing it is the flow working exactly as designed. Returns NO. The separator: OPS needs a fault or readiness for one, and a designed step is not a fault. The readiness limb is new and deliberate — the old wording's 'only bites while running' clause excluded recovery routes and operator levers, which must exist before anything runs. |
| `SUP` ⚠ | Whoever shortens the distance from stuck to unstuck. | Does the sentence exist to shorten the gap between somebody being stuck and being unstuck — so that with nobody stuck there would be nothing for it to do? | Nearest is DOC. Take 'the README states which skills refuse and which advise.' Apply the question: with nobody stuck, is there nothing for it to do? No — it is owed on a quiet day to a reader who is merely curious, and nobody's difficulty is its trigger. Returns NO. The separator is the trigger: SUP is owed to somebody blocked; DOC is owed unasked. The old 'somebody's understanding must change' wording could not reach a troubleshooting lever, where what changes is the product, and it did not separate from DOC at all, because changing a reader's understanding is what documentation is. |
| `TST` | Whoever decides what will count as proof. | Is the thing the sentence rules on a CHECK itself — what it owes, when it runs, what would satisfy it, or who may vouch for it — and would running it produce a verdict that stops or passes something? | Nearest is TECH, and TECH-010 is the trap because a refusal sits in it: 'A final requirement carries a hash of its statement as keyed. When they diverge the audit REFUSES.' Strip the checking clause and 'a final requirement carries a hash of its statement as keyed' still stands on its own — a slot on a record. The check is the consequence, not the subject. Returns NO. This strip test operates strictly inside one sentence and never reaches for a second, which is what constraint 3 requires; the earlier draft's version reached for TST-002 and was the order-dependence itself. |
| `REL` | Whoever owns the act of handing over and the act of taking back. | Does the sentence constrain a datable EVENT of handing something over or pulling it back — when it may happen, in what order, behind what switch, or how it is undone — with a moment before it and a moment after, rather than what the handed-over work contains? | Nearest is PRD, and PRD-005 is the sharpest keyword bait in the register because it carries both 'release' and 'ship': 'Project type and release type are the same thing for the twelve types that ship; Ideation, Spike and Security Review produce findings instead.' Apply the question: is a datable event constrained, with a moment before and after? No — it is an identity claim between two vocabularies, and it would read the same if nothing ever shipped. Returns NO. PRD-001 is the harder semantic bait and fails the same clause: 'Kerd gives consuming projects this capability' is about who the finished thing is for, names no event and no moment, and is scope. |
| `DOC` | Whoever answers for what is written to be read by somebody who was not there. | Is the obligation to EXPLAIN the thing to somebody who was not there — discharged by writing prose they read and nothing else — with no machine, gate or tool consuming what gets written? | Nearest is TECH, and TECH-005 is the trap because it is entirely about a written file: 'The register is a standalone file at a known location — never embedded in a product doc — so it can be read quickly by a person and directly by a tool.' Apply the question: is the obligation to explain, with no machine consuming what is written? The sentence names a tool as a consumer in its own words. Returns NO. The machine-consumer clause is the mirror image of TECH's 'honourable without knowing what the thing is for', so the pair is settled once from both sides rather than twice from neither. |
| `POST` ⚠ | Whoever converts what came back into what happens next. | Does the sentence bind what the project must DO with something that can only arrive from people who did not build it — a report of a fault, a complaint, a figure about how many took it up, a request? | Nearest is ANA. Take 'adoption is tallied as the count of repos holding a non-empty register, reviewed monthly.' Apply the question: does it bind what the project must do with what arrived? No — it defines how to count, and by itself nothing follows from the number. Returns NO. ANA builds the instrument; POST binds the response. The old answerability clause is deleted outright: it tested when a QUESTION becomes answerable, while the producer's list is of ACTIVITIES, and every activity rule is statable and bindable today — it rejected three of POST's own five sub-types. |

### These definitions survived attack rather than review

Drafted once, then attacked by six specialists each hunting one named failure —
echoing the `Covers` list, catching the neighbouring category, depending on
filing order, asserting something false about this repo, failing under time
pressure, and collapsing on the categories with no data.

**Six questions were deleted rather than patched, because each rejected its own
category's rows:** PRD's residue test returned yes for four rows in three other
categories; TECH's invisible-swap test returned no on eight of TECH's own ten;
NFR's dial clause expelled `NFR-002` and `NFR-003`; USR's cancellation clause
admitted nothing that could ever be filed; STA's "will never operate" clause
made the category unfillable, since customers and support staff *do* operate the
thing; and PRIV's authority clause returned yes for **all fifty rows**.

An earlier attempt used three independent drafters and their agreement looked
like evidence — until attackers showed all three had made the same lexical
error. **Convergence of proposers is worthless when they share a brief.**

### Portability — the ReqIF 1.2 mapping

Carried so an export is a rendering rather than a re-modelling. Verified
2026-08-08: `FUN-001` passes strict XSD validation as a ReqIF `IDENTIFIER`
(an `NCName`), while `001-FUN`, `FUN 001` and `FUN:001` all fail it.

| Kerd field | ReqIF |
|---|---|
| ID | `ReqIF.ForeignID` — **and** `IDENTIFIER`. The industry convention (prostep ivip Implementation Guide, mapping DOORS "Absolute Number" and PTC "Item ID") puts the human-visible number in `ForeignID` and leaves `IDENTIFIER` an opaque GUID. Carrying it in both is the portable move. |
| Category | `ReqIF.Category` — a reserved enumeration, so the twenty codes fit the standard exactly |
| Statement | `ReqIF.Text` |
| Title | `ReqIF.Name` |
| Acceptance Criteria *(deferred)* | `ReqIF.FitCriteria` |
| State | **no reserved name exists.** `ReqIF.ForeignState` is defined only at Specification level, so the five states stay a custom enumeration Kerd validates itself |
| Links | `SpecRelation`, a first-class object whose `TYPE`, `SOURCE` and `TARGET` are all mandatory |

The Implementation Guide specifies XHTML for `Name` and `Text`; StrictDoc emits
String. If Kerd ever writes its own exporter, XHTML is the conventional choice.

## States, and what each one owes

A state is not a label. Measured 2026-08-08: Sphinx-Needs attaches obligations
to a state — *"a `fun` in status `final` must be `verified_by` at least one
`tst`"* was written and produced a real refusal. Kerd's five states owed
nothing, while the producer's own `G0`–`G8` gates state those obligations in
prose. This table is their machine form.

| State | Means | Owes |
|---|---|---|
| `proposed` | captured, not yet qualified — the holding state | nothing; this is the free-capture landing zone |
| `qualified` | judged durable, wording agreed, not yet signed | a `Source` |
| `final` | the producer's key is on it | a `Source` **and** an `Approved` hash matching the statement |
| `superseded` | replaced, and the replacement is named | a `superseded-by` link to a requirement that exists |
| `dropped` | deliberately abandoned | a reason in `Source` |

**The `final` obligation is the one that closes a real hole.** Doorstop's
`reviewed` is a sha256 fingerprint rather than a label; editing one line of a
requirement's text immediately reported *"unreviewed changes"*. Kerd's `final`
survived any later edit, so an approval could not be told from one whose
subject had changed underneath it. **The audit REFUSES on divergence and never
rewrites the state** — a red check is a question the producer answers; a silent
downgrade is a decision made for them.

## Link roles

A link is a typed object, never a column. ReqIF's `SpecRelation` makes `TYPE`,
`SOURCE` and `TARGET` all mandatory — a relation cannot be untyped. StrictDoc
requires a role to be **registered in the grammar** (`ROLE: Refines` was refused
until declared) and its `REVERSE_ROLE` gives both reading directions from one
declaration.

| Role | Reverse | Used for |
|---|---|---|
| `depends-on` | `required-by` | `TECH-006` — one requirement depends on another |
| `supersedes` | `superseded-by` | supersession as a typed edge, not a prose convention |
| `refines` | `refined-by` | a functional requirement under a product one |
| `satisfied-by` | `satisfies` | requirement → the contract piece that builds it *(slice 2)* |
| `verified-by` | `verifies` | requirement → the test that proves it *(slice 2)* |

A link naming an ID that does not exist is refused.

**A link carries its target's stamp — the suspect-link mechanism.** Written as
`- depends-on → FUN-005 (sha256:…)`, where the hash is the target's statement
as it read when the link was made. Edit `FUN-005` and every link pointing at it
diverges, so its dependents are flagged for re-look rather than silently
carrying a claim about words that have changed. Measured 2026-08-08 in Doorstop:
one edit marked three dependents suspect across two documents. **Kerd's
`superseded` names a replacement but never tells dependents to look again** —
this is that gap closed, and it is the same idea as `TECH-010` applied to edges
instead of nodes.

**`derived` — an origin requirement may have no parent.** `BUS`, `STA` and `USR`
requirements originate rather than refine; without an explicit allowance every
such row reads as a broken trace the moment a completeness check exists. A
requirement in an origin category needs no `refines` parent; one in any other
category that declares none is a finding, not an error, until slice 2 wires the
forward half. *(Wording corrected at the validator's build, 2026-08-13: an
earlier draft said "inbound `refines`", but the trace a completeness check
follows is the outbound edge naming your parent — AU8 checks that reading.)*

## Views

Named field subsets, stored as data. StrictDoc's `VISIBLE_FIELDS` idea, adopted
because it dissolves an argument this design had been having with itself: the
producer's fifteen-field row against `UX-006`'s *"avoid reading lots of text"*
was never fifteen fields against seven. It was **one model against one
rendering**, and shrinking the model was the wrong half to change.

| View | Shows | Surface |
|---|---|---|
| `card` | ID · Category · State · Statement | the board |
| `table` | + Source | a scan of the file |
| `full` | every declared field and every link | one record open |
| `release` | ID · Title · State · release | release planning *(needs the release artifact, which does not exist)* |
