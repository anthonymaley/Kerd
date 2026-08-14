# Triage — the 51 migrated requirements against the approved goals

**What this is.** The 51 blocks in `docs/requirements/register-v2.md` were
written before the reset, in a register with no goals above it. This file
checks every one of them against `docs/kerd-goals.md` — four laws and eight
goals, approved 2026-08-13 — and recommends a bucket.

**What this is not.** Nothing here moves, edits or kills anything. Rule 10
requires a named authoriser for a kill and that is the producer's. Every
DEAD below is a recommendation with its instrument named.

**The rule this triage runs under.** Producer, 2026-08-14: *"if the analysis
proved a better way, then we go agaist what i said before, we chnage the
rule"* and *"if wer agree a better way then we superseed and strike off prior
comments for sure. otherwise we go in loops."* Age is not a defence. Equally,
a missing Why is not evidence against a requirement — 46 of the 51 have no
recorded reason, which is a known gap, and no requirement is cut for it here.

**Counts.** LIVE 38 · DEAD 8 · PRODUCER'S CALL 5.

---

## Summary

| Ref | Handle | Bucket | Serves / dies by |
|---|---|---|---|
| R-0001 | Kerd is the supplier, not the subject | DEAD | duplicates Law 1 itself |
| R-0002 | what requirements are for | DEAD | obsolete by design change — purpose, not obligation |
| R-0003 | the taxonomy ships as default | PRODUCER'S CALL | G8 / dead schema — does the taxonomy survive its filing system? |
| R-0004 | applicability is declared, never assumed | DEAD | duplicated by R-0048; keyed to the dead category field |
| R-0005 | project type and release type are one vocabulary | PRODUCER'S CALL | G3 / Law 4 — is the twelve-type list researched or assumed? |
| R-0006 | the alignment gate is a shared structure | LIVE | G1, G4 |
| R-0007 | the register feeds the tooling | LIVE | G5 |
| R-0008 | the evaluation mark set | LIVE | G4 |
| R-0009 | the cross takes no modifier | LIVE | G4 |
| R-0010 | building it ourselves is a legal countermeasure | LIVE | Law 4, G7 |
| R-0011 | the four summary columns | LIVE | G4 |
| R-0012 | a lesser mark says why, briefly | LIVE | G4 |
| R-0013 | dependency cost is marginal and proportionate | LIVE | Law 4, G7 |
| R-0014 | approving the design is enough | LIVE | G1, G3 |
| R-0015 | a plan executes the design and carries its measurements | LIVE | G6 |
| R-0016 | every requirement is identified and traceable | DEAD | contradicted — no Category exists; superseded by rule 2 |
| R-0017 | a request is qualified before it becomes a requirement | DEAD | contradicted — no lifecycle, no `final` state |
| R-0018 | project type is declared once | LIVE | G1, G5 |
| R-0019 | the goal gate increments the type | LIVE | G3 |
| R-0020 | conductor suggests a type change, the producer agrees it | LIVE | G1, G5 |
| R-0021 | type is a stack | LIVE | G3 |
| R-0022 | route and rigor are derived, not declared | LIVE | G3 |
| R-0023 | conductor sizes the model and the effort | LIVE | G7 |
| R-0024 | the boundary records everything agreed | LIVE | G7, G2 |
| R-0025 | floors compose as a union | LIVE | G3 |
| R-0026 | a spike carries its own rigor | LIVE | G3 |
| R-0027 | artifacts do not scatter | LIVE | G5 |
| R-0028 | the mark carries the verdict, not the box | LIVE | G4 |
| R-0029 | mark size inside its cell | LIVE | G4 |
| R-0030 | headings render as headings | LIVE | G4 |
| R-0031 | diagrams use a sans-serif font | PRODUCER'S CALL | G6 / G3 — all diagrams, or the matrix only? |
| R-0032 | the preferred option's verdict cell | LIVE | G4 |
| R-0033 | brevity is the point of a table | LIVE | G4 |
| R-0034 | the producer marks the page without typing | DEAD | contradicted — status and release-on-requirement both cut |
| R-0035 | a stale view's marks are refused | LIVE | Law 3, G4 |
| R-0036 | state lives in the user's repo | LIVE | Law 1 |
| R-0037 | the nine-link traceability chain | PRODUCER'S CALL | Law 2, G2 — nine links, or the two the shape implements? |
| R-0038 | the machinery aims at the consuming project | LIVE | Law 1 |
| R-0039 | no routing to superpowers | DEAD | contradicted by Law 4 and by open question 2 |
| R-0040 | the register is a standalone file | LIVE | G5 |
| R-0041 | a requirement carries its dependencies | LIVE | G5 |
| R-0042 | git-native, per project | LIVE | Law 1 |
| R-0043 | one representation, no parallel store | LIVE | Law 1, G2 |
| R-0044 | a requirement is a block, liftable as a unit | LIVE | G4, G5 |
| R-0045 | the audit refuses on divergence | DEAD | contradicted twice — `final` state, statement-only fingerprint |
| R-0046 | the funnel needs a conductor session | LIVE | G1 |
| R-0047 | the plan proves the measurements carried across | LIVE | Law 3, G6 |
| R-0048 | every type owes every gate | LIVE | G3 |
| R-0049 | due date, not effort | LIVE | G6 |
| R-0050 | the completeness check is tiered | PRODUCER'S CALL | Law 3 — trigger is the stage, but the law says the weight |
| R-0051 | the check binds on facts from outside the model | LIVE | Law 3 |

---

## DEAD — recommended for the graveyard

Fullest reasoning, as the brief requires. Each names its instrument and, where
one exists, the words that kill it.

### R-0045 — the audit refuses on divergence — **superseded and contradicted**

The clearest kill in the register, and the register's own findings reached the
same verdict.

Two of its clauses are dead machinery. *"A `final` requirement"* names a state
that no longer exists — the approved shape's settled decision is **"there is
no lifecycle or status field on a requirement"**, and the standards research
behind it found that **no standard in the territory defines a status on the
requirement at all**. *"a hash of its statement as keyed"* names a fingerprint
over the statement alone, which the producer himself overrode — *"no point
doing half of the fingerprint"* (09:00), widened again to the Why at 09:32.
Rule 9 now hashes statement, Why, traces and depends-on together.

Its payload is genuinely valuable and is already carried elsewhere: the audit
refuses rather than silently rewriting, because *"a silent downgrade is a
decision made for them"*. Rule 9 states the refusal outright — a recorded
fingerprint that no longer matches means **not approved**, computed and
reported, never written into the file.

**Recommend:** killed, superseded by a fresh requirement stating the
fingerprint recipe and the refusal, with no reference to a `final` state.

### R-0039 — never route to superpowers — **contradicted by Law 4**

The register did not flag this one, and it is the kill with the widest
consequence.

Law 4, in his own words and governing every aspect of the project: *"we always
need to 1. assess and learn from industry standards, leading approaches,
emerging approahes 2. decide what fits for us 3. consume/adopt whole if
perfect…"* — and the half added the same morning: *"dont just assume we are
correct unless an explicit requirement states this is the only way."* A blanket
ban on one named alternative is exactly the privileged conclusion that clause
closes off.

Worse, it pre-decides a question the goals record keeps explicitly open. Open
question 2: **"What evidence settles build-vs-adopt, and who takes the
decision?"** — with the instruction that *"The prior evaluation in this repo is
to be re-examined as evidence, not treated as precedent."* G8's own grounding
carries *"superpowers does some great things... so we can learn from it"*. A
live requirement forbidding the routing forecloses an open decision by having
been written down first, which is the precise failure Law 4's ordering rule
exists to prevent.

**There is a real payload underneath it**, and it is the second half of the
same sentence: *"i just want the process to be ours and visable."* Routing
work into a process the producer cannot see fails G5 outright — *"its not clear
what or why its doing in a black box way."*

**Recommend:** killed, re-proposed as the visibility principle — no step of our
process is delegated to a process the producer cannot see — with no
third-party name in the statement.

### R-0034 — the producer marks the page without typing — **contradicted**

The statement names two things to mark: *"status, release assignment"*. Both
were cut by settled decisions in the approved shape: **"there is no lifecycle
or status field on a requirement"**, and **"which release a requirement is in
lives on the release, never on the requirement"**. The requirement therefore
asks for a marking interface over two fields that do not exist.

The mechanism it describes — mark on the page, saved to a file, applied next
session on the word "updated" — is alive and wanted. His 08:16 objection
itemises what the generated view owes him: seeing the requirements and their
dependencies, editing the text, seeing each one's standing, leaving comments,
links and images. None of that is status or release membership.

**Recommend:** killed, re-proposed as the marking mechanism over the fields
that exist (approval, comments, links, dependency edits).

### R-0016 — every requirement is identified and traceable — **contradicted and superseded**

*"Every requirement gets a Category and ID."* The Category half is contradicted:
the approved shape has no category field, and the research lesson behind that
is quoted in the shape doc — *every scheme that encoded meaning in the
identifier eventually had the meaning change.* The ID half is superseded by
rule 2, which says the same thing with the doctrine attached (opaque,
permanent, never changed, never reused, minted only at filing).

**Recommend:** killed, re-proposed as an identity requirement with the category
clause gone. The register reached the same verdict independently.

### R-0017 — a request is qualified before it becomes a requirement — **contradicted**

*"through stages to final"* names the five-state lifecycle the approved shape
deliberately cut, for the reason the research gave: the two tools that shipped
a status field shipped it unenforced, *"the worst of both worlds: it looks like
a contract and isn't one."*

The qualification idea itself is untouched and is real work — it is what
`/kerd:interrogate` does, and it serves G2's refusal to guess.

**Recommend:** killed, re-proposed without the lifecycle clause.

### R-0004 — applicability is declared, never assumed — **duplicated**

*"Applicability is declared per category — `applies`, or `n/a` with a named
reason."* R-0048 says the same thing about the same kind of object: *"Every
project type owes every gate unless that type explicitly marks it `n/a` with a
reason."* Flat in one list, they are one requirement written twice; under
category headings they read as two because they sat in different sections.

It also depends on R-0003, whose survival is a producer's call, and its subject
noun is the category field the shape removed.

**Recommend:** killed as a duplicate. R-0048 is the survivor and states the
obligation in terms of a thing that still exists.

### R-0001 — Kerd is the supplier, not the subject — **duplicates Law 1**

*"Kerd gives consuming projects this capability; Kerd is only a user of it"* is
Law 1 restated: *"Kerd installs into a user's own project and operates inside
that repository's boundaries; the Kerd project never holds sessions for anybody
else's work."*

Rule 11's boundary test asks what a build could be *rejected against*. Nothing
can be rejected against this statement that is not already rejected by R-0036
(state lives in the user's repo), R-0038 (the machinery aims at the consuming
project) or R-0042 (git-native, per project) — the three checkable forms of the
same law, all of which stay live.

A requirement that restates its own law adds a second text that will drift from
the first.

**Recommend:** killed as a duplicate of Law 1. Nothing is lost — the law is
above it and three live requirements implement it.

### R-0002 — what requirements are for — **obsolete by design change**

Two problems, and the smaller one has already been resolved on the page.

The ID collision is settled. The migration struck *"speak in IDs that mean
something"* under Law 4's ordering rule and kept the reading that survives —
a name he can point at and say, served by the handle in rule 3. That was the
correct application of his own rule, and it does **not** need to go back to
him (see Findings 3).

What remains is a statement of purpose, not an obligation: *"Requirements exist
so the producer can review them, plan enhancements, plan releases, and refer to
any of them by a name he can say out loud."* No build can be rejected against
it. Its four clauses are each carried by something checkable — review by R-0007
and R-0040, dependencies and planning by R-0007 and R-0041, the sayable name by
rule 3 of the approved shape.

This is a Why with a Statement label on it.

**Recommend:** killed as content that belongs in the register's preamble (rule
13 explicitly allows non-fingerprinted prose about the set) rather than as a
requirement. If any clause is wanted as binding, it is *plan releases* — and
that has no home yet (see Findings 7).

---

## PRODUCER'S CALL

Five. Each turns on intent, not on evidence I can go and get.

### R-0003 — the taxonomy ships as default

The twenty-category discipline taxonomy was both the *shipped checklist* and
the *filing key* for requirements. The filing key is gone — no category field
exists on the shape. Whether the checklist survives as content is a different
question and the goals do not answer it. Law 4 also bites: the taxonomy was
designed with no step-1 research recorded, and *"dont just assume we are
correct"* applies to it as much as to anything.

R-0004 and R-0048 both hang off it.

### R-0005 — project type and release type are one vocabulary

*"the same thing for the twelve types that ship."* The goals never mention
project types. Nothing kills this — but nothing approves it either, and the
number twelve is a pre-reset design decision with no research behind it. Seven
further requirements (R-0018 to R-0022, R-0025, R-0048) build on it; all are
marked LIVE on the assumption that it stands.

### R-0031 — diagrams use a sans-serif font

The register left this untraced. I disagree that it cannot be traced (see
Findings 4) — G6's design input is *"should not look different or behave
differt fromt he agreed spec"*, and G3's guard makes a font spec content
outright: *"imagine for g3 if the design spec designer saw his font being
changed without his approval....."*

The real question is scope. The other four look-and-feel requirements were
narrowed on his ruling *"UX-001 was for the eval matrix only"* (2026-08-08
21:23). This one was not narrowed, and it says *"Diagrams"* without
qualification.

### R-0037 — the nine-link traceability chain

Business Goal → Stakeholder Need → Product Requirement → Functional/Technical →
Design → Implementation → Test Case → Release Evidence → Post-Launch Metric.

The approved shape implements two of those links (traces-to for goals and laws,
depends-on between requirements) and **deliberately deferred** the mechanism
that would compute the rest, with a stated return condition: declared coverage
*"returns for consideration the day the downstream artifact kinds exist."* So
the chain is not contradicted — it is an ambition the approved design does not
yet reach. Whether it stays the target changes what gets built next.

### R-0050 — the completeness check is tiered

Its trigger is the **stage**: *"the LIGHT check fires at every step; BOTH light
and heavy fire at the design GO."* Law 3's approved ladder triggers on the
**weight of the work** — *"doing a thing, check it yourself, doing a bigger
thing, strawman, doing a critical thing, get adveserial model to check"* — and
the goals record spells the difference out: *"the trigger is the weight of the
work, not the stage it sits in and not a cost budget."*

Heavy is *"N independent readers working from the RAW sources"*, which is the
adversarial tier. So the two rules give different answers about the same event,
and only he can say which governs. The light check is untouched either way.

---

## LIVE

One line each: what it does that nothing else does.

- **R-0006** (G1, G4) — makes the alignment gate a shared object both parties
  point at, which is his *"strong visuals and specs for approval so we are
  clear with each other"* given a form.
- **R-0007** (G5) — makes the register a data source, which is what any
  generated view, impact report or release plan is computed from.
- **R-0008** (G4) — fixes the mark vocabulary, without which a matrix is
  opinion.
- **R-0009** (G4) — the only statement saying there is no degree of
  impossibility; prevents a `×-` softening a hard no.
- **R-0010** (Law 4, G7) — keeps build-for-the-gaps legal inside an option
  comparison, which is Law 4 step 5 made usable.
- **R-0011** (G4) — names the four summary columns; nothing else says what a
  comparison must total up to.
- **R-0012** (G4) — forces a lesser mark to carry a reason without turning the
  table into prose; G4's brevity-against-noise input in one rule.
- **R-0013** (Law 4, G7) — the only rule that stops "it adds a dependency"
  being used as an automatic veto on adopting something.
- **R-0014** (G1, G3) — caps the number of producer approvals per piece of
  work, serving *"a user never feels overwhelmed by the process"*.
- **R-0015** (G6) — requires the plan to carry the measurements; the content
  obligation R-0047 later checks.
- **R-0018** (G1, G5) — declared once, never re-asked: the anti-nagging rule.
- **R-0019** (G3) — the only statement saying the type advances rather than
  being re-declared.
- **R-0020** (G1, G5) — puts type change under the producer's agreement rather
  than the model's discretion.
- **R-0021** (G3) — inheritance and forward-only override; the only rule
  covering nested work.
- **R-0022** (G3) — derives route and rigor instead of asking, which is where
  "sized to the work" stops being a question the producer answers.
- **R-0023** (G7) — his own words, in full, and the only requirement in the
  register with an honest Why: model and effort advised in both directions.
- **R-0024** (G7, G2) — the recording-completeness rule; G7's *"never sumarize
  memories or requirments or achievements etc"* given a boundary.
- **R-0025** (G3) — floors as a union; the only rule stopping nesting from
  laundering rigor away.
- **R-0026** (G3) — denies a spike the small-work exemption G3 refuses to grant
  anyone.
- **R-0027** (G5) — artifacts findable in one place; weakly worded, but nothing
  else says it.
- **R-0028** (G4) — the mark, not the fill, carries the verdict.
- **R-0029** (G4) — mark legibility at a glance.
- **R-0030** (G4) — headings that read as headings; the difference between a
  table and a grid of strings.
- **R-0032** (G4) — one filled cell says which option won.
- **R-0033** (G4) — brevity as an obligation rather than a taste; the general
  form of G4's design input.
- **R-0035** (Law 3, G4) — marks against a stale view are refused rather than
  applied blind. Note it depends on R-0034, which is recommended dead; the
  dependency needs re-pointing, the requirement does not.
- **R-0036** (Law 1) — names the data that lives in the user's repo.
- **R-0038** (Law 1) — names the execution target; the runtime form of Law 1.
- **R-0040** (G5) — a standalone file at a known location, which the approved
  document decision confirms rather than contradicts.
- **R-0041** (G5) — dependencies carried on the requirement, which is what makes
  *"change requirement x and the impact can be measured"* computable. (Wording
  says "row"; the shape says block. Notation, not content.)
- **R-0042** (Law 1) — git-native and per project; the storage form of Law 1.
- **R-0043** (Law 1, G2) — one representation, no parallel store; the only rule
  forbidding a shadow copy that drifts.
- **R-0044** (G4, G5) — a requirement is a block, liftable as a unit. **I
  disagree with the register's recommendation to kill this** — see Findings 5.
- **R-0046** (G1) — funnel work needs a session; keeps Q&A and admin free of
  ceremony, which serves the don't-overwhelm input.
- **R-0047** (Law 3, G6) — the plan proves the measurements carried across
  *and shows it*; the check on R-0015's content.
- **R-0048** (G3) — every type owes every gate unless explicitly excused with a
  reason; the no-skipped-stages rule with the escape hatch made visible.
- **R-0049** (G6) — outcome measure over input measure; stops DUE DATE decaying
  into EFFORT.
- **R-0051** (Law 3) — the check binds on countable facts from outside the
  model. The single most load-bearing requirement against Law 3's *"did i infer
  that"*.

---

## For the producer

Five questions. Answer each in a sentence.

1. We used to file every requirement under one of twenty subject areas. That
   filing system is gone. Do those twenty areas still ship as the standard
   checklist a project works through, or do they die with it?

2. We have a fixed list of twelve project types, where three of them
   (ideation, spike, security review) produce findings instead of a release.
   That list was drawn up before we started researching how others do this.
   Keep it as is, or re-open it? A fair amount is built on top of it.

3. Diagrams must use a plain sans-serif font. Does that cover every diagram we
   produce, or only the comparison matrix — which is where you narrowed the
   other look-and-feel rules?

4. Do you still want the full nine-step trail from a business goal all the way
   to a post-launch metric, or is it enough for now that each requirement
   points at the goal it serves?

5. There is a deep check where several independent readers go back to the raw
   sources and we look for them to agree. Should that fire automatically at
   design sign-off, or only when the work is weighty enough to deserve it?

---

## Findings

**1 — The register's biggest exposure is a requirement it never flagged.**
R-0039, *"Never route to superpowers"*, forecloses a decision the goals record
keeps explicitly open (open question 2, build-versus-adopt) and collides head-on
with Law 4's *"dont just assume we are correct unless an explicit requirement
states this is the only way."* The migration's own graveyard shortlist did not
include it. It is the strongest DEAD in this triage after R-0045, and unlike
R-0045 nobody had noticed.

**2 — The register asks the producer a question its governing rule already
answers.** Finding 7 of the register calls R-0002's ID collision *"the one thing
to look at first"* and puts two readings to him. But the migration had already
struck the offending clause in the same file, correctly, under Law 4's ordering
rule — *"if the analysis proved a better way, then we go agaist what i said
before."* The rule was applied and then the settled question was escalated
anyway. It is not on his list here. Escalating a question your own rule has
answered is how the loop his ruling exists to prevent gets started.

**3 — Five pre-reset requirements survive on merit despite having no rationale
at all.** R-0013, R-0024, R-0025, R-0049 and R-0051 all read as if they were
written yesterday against the approved goals. The missing-Why problem is real
and is 46 blocks wide, but it correlates with nothing — the requirements with
the weakest paperwork include some of the strongest statements in the set.

**4 — The one requirement declared untraceable is traceable.** The register
left R-0031 with *"not yet traced… No goal or law is served by this statement
without inventing a rationale."* Two of his own inputs cover it: G6's *"should
not look different or behave differt fromt he agreed spec"* makes appearance
spec content, and G3's guard says so explicitly — *"imagine for g3 if the
design spec designer saw his font being changed without his approval....."* A
font **is** the design spec, in his words. The open question about R-0031 is
its scope, not its parent.

**5 — I disagree with the register on R-0044.** Its Finding 6 recommends
killing it because *"the render detail it specifies is no longer the render."*
It is: R-0044 says heading, bolded meta lines, statement as text, links as a
trailing list, liftable as a unit — and rule 1 of the approved shape specifies
a level-three heading, five bold labelled lines, statement as text, links near
the end, blocks separated by a rule. That is the same render. R-0044 predicted
the approved form and should stay live.

**6 — Two requirements conflict outright.** R-0050 fires the heavy check at a
**stage** (the design GO); Law 3's approved ladder fires checks by the **weight
of the work**, and the goals record rules out the stage explicitly. Both cannot
govern the same event. It is question 5 for the producer.

**7 — What the register assumes and the goals never mention.** This is the
honest limit of this triage: the eight goals name failures to prevent, not
machinery, so several clusters cannot be adjudicated against them at all.

- **Releases.** R-0002, R-0005, R-0007 and R-0034 all assume release planning
  and release membership. The word "release" appears nowhere in the eight
  goals. This is the largest uncovered assumption in the register.
- **Project types and the type stack.** Seven requirements build on a
  vocabulary the goals never mention. Hence question 2.
- **The funnel and its gates.** R-0019, R-0046 and R-0048 assume a funnel with
  gates. The goals describe *"one path"* without naming its stations.
- **The evaluation matrix.** Nine requirements (R-0008 to R-0013, R-0028 to
  R-0033) specify an instrument the goals never ask for. They are all live —
  the matrix is how G4's *"visual confirmations… vs wall of noise text"* is
  delivered — but the instrument itself has no goal-level mandate.
- **Conductor and composer roles.** R-0020, R-0023 and R-0046 assume them; the
  goals mention them once, parenthetically, in his own words: *"the composer or
  conductor roles (if we keep them)"*.

**8 — The Law 1 cluster is five requirements deep.** R-0001, R-0036, R-0038,
R-0042 and R-0043 all state the repo boundary from different angles. Only
R-0001 dies here, as pure restatement of the law. The other four are each
checkable against something different (data, execution target, storage, no
shadow copy) — but they were written under four different category headings and
now sit adjacent, and they are worth one consolidation pass by whoever next
touches them.

**9 — Two more near-duplicate pairs, kept as pairs deliberately.** R-0015 and
R-0047 (the plan *carries* measurements; the plan *proves* it carried them) and
R-0012 and R-0033 (a lesser mark's reason is brief; brevity is the point of a
table). In both cases the second is a check or a generalisation of the first
rather than a restatement, so both stay. Flagged so nobody re-derives the
question.

**10 — A dependency needs re-pointing if R-0034 is killed.** R-0035 (stale
views refused) depends on R-0034 (mark without typing). R-0035 survives on its
own — any generated surface that accepts marks must refuse stale ones — but its
`Depends on` line would dangle, and rule 8 says an unresolved reference is an
error that stops the run.
