# Annotation log

Annotations are a **queue, not an archive**. Tony writes on the canvas, the
comment is captured to `<diagram>-tony.json`, it gets acted on, and then it is
**deleted** — the substance now lives in the diagram, the generator, or a
decision record.

This file is the disposition trail, so a comment never disappears with nothing
to show for it. Append-only; it is a record of events, so entries are dated and
never rewritten.

Deleting them also fixes a real defect: preserved annotations kept absolute
position but not attachment, so a comment drifted away from what it annotated
whenever the layout reflowed. A comment that lives one cycle cannot drift.

---

## 2026-08-03 — `2026-08-03-frame-the-intent-flow`

**"Its extensively tested in ~/toyota-sensei and other projects though"**
Placed on the sensei bet at step 5.
→ **Dealt with.** The bet was wrong as written. Sensei is not untested — it is
proven elsewhere and has simply never run inside Kerd, so the bet narrowed to
*transfer, not the method*. Changed in the step 5 note and in the tooling
catalogue (`gen_functions.py` → `TOOLING`). Commit `a976e11`.

**"Green is collaboration Foudner > Claude"**
Placed top-left, as a grammar addition.
→ **Dealt with.** `GREEN` added to `kit.py`. First applied wrongly — I read it
as *steps where both of us act* and coloured capture and the two-key approval;
Tony's rule is **his input into the work**. Reverted the steps, kept the colour,
and it is now in the flow legend. Commit `a976e11`.

---

## 2026-08-03 — `2026-08-02-product-to-build` (backlog: six pre-queue comments)

These six predate the queue policy — captured 2026-08-02, preserved and
re-merged on every regeneration since. One had drifted onto movement-4 text
(the exact defect the queue dissolves). All six were acted on long before the
policy existed; dispositions recorded now, file deleted.

**"we need an actual measurement that we can use to know when we have achieved
or to show the gap"**
→ **Dealt with.** Became the EVIDENCE column of the function map — the
`gen_functions.py` header quotes it verbatim. Every row states what you could
point at.

**"super important, MVP vs someday"**
→ **Dealt with.** Movement 7 — the build sequence with MVP / SPIKE / v1 /
SOMEDAY bands. Tony's call on the ordering.

**"diagram to show gap/change/impact"**
→ **Dealt with.** The story-format MUST in *How we talk to each other*
(compare/contrast: current → new → what changes) and v0.68's now / the change /
what it means shape.

**"Where doest TDD and testing live"**
→ **Dealt with.** Settled today: testing strategy is part of the *Design the
solution* package (test bias per layer, contract seams named), proof layers are
BUILD's verify functions.

**"Leverage Sensei Story formats for diagrams (see examples)"**
→ **Dealt with.** The pick-a-story-format MUST, and sensei's TOOLING row
(proven elsewhere; the bet is transfer).

**"Could be a spike too."**
→ **Dealt with.** The SPIKE band exists — "SPIKE — not a decision", routing
bet tested rather than decided.

## 2026-08-03 — `2026-08-03-frame-the-intent-flow` (file cleanup)

Both comments were dispositioned above (commit `a976e11`) but the capture file
lingered — deleting a dealt-with file is part of the queue policy. Deleted.

---

## 2026-08-03 — `2026-08-03-choose-what-matters-view` (canvas race incident)

Both comments were written onto LAST SESSION'S view: Tony's open Excalidraw tab
wrote its old scene back over the freshly pasted design flow, so the "new"
diagram he reviewed was the previous one. Gotcha logged in the playbook.

**"Forget Bree, im not working on that right now. also where has sherpa came
back from? we should not be thinking solution (skills) at this point, just the
requirments etc"**
→ **Dealt with.** The Bree dogfood item is REMOVED from TODO (not blocked —
gone). Sherpa was on the view because the blocked band mirrored TODO's backlog,
which still names skills — solution vocabulary. Standing correction accepted:
during the requirements walk, candidate views name REQUIREMENTS and outcomes,
never skills. Skill-fate items (sherpa, mode, skriv wiring) stay in TODO's
blocked section only, out of any candidate view, until the design pass decides
solutions.

**"Not really following what these diagrams are to be hnest, they are so vauge
and high level and look identical to previous ones - or im tired."**
→ **Partly dissolved, partly held.** Dissolved: it WAS the previous diagram —
the race above. Held: the verdict on whether the actual design-the-solution
flow reads clearly is still owed, on the correct artifact. If the real flow
also reads vague/identical, that is a real defect in the shared flow template
(every stage flow looks the same by construction) and gets treated as one.

## 2026-08-04 — Celtic Ticket Exchange worked-example flow (six questions)

All six are tooling-per-stage questions — exactly the post-walk phase's
agenda. Each answered in chat, carried into the post-walk scope, and deleted
from the canvas. They are the first six items of "define how the skills must
change to support the agreed requirements."

**"so, we will be using /conducter here?"** (at SPARK)
→ **Answered: today yes, tomorrow is the post-walk decision.** Conductor is
the only session-driving machinery that exists, so any work starts there
now. But the flow is bigger than one session skill — conductor's shapes map
onto the CONTRACT and BUILD rungs, and what conductor becomes (or splits
into) is the post-walk phase's central question.

**"Probably Fable as the model to compose?"** (at FRAME)
→ **Answered: yes — the one place the top tier pays.** The framing
conversation is where intent is captured; a wrong word there poisons every
downstream declaration, and the sizing rule's "never top tier for difficulty
alone" is about mechanical work, not the intent interview. Top tier at
FRAME, sized-down players everywhere the work is specified.

**"Is Sherpa the the right tool? do we need to review an modify?"** (at FRAME)
→ **Answered: measure it, don't assume it.** Sherpa is unused by measurement
(the orphan finding). Post-walk move: hold sherpa Explore against Frame the
intent's agreed requirement (triage, two documents, two keys, grounding) and
keep/modify/kill on conformance. Candidate for the SPIKE — route ONE dead
skill and watch — possibly ahead of capturerequirements.

**"Do we need to build or find a viablity tool or do we have it covered?"**
(at VIABILITY)
→ **Answered: partially covered; expect modify, not build.** Interrogate
serves the exhaustive-interview shape today, but the agreed requirement adds
risk machinery it doesn't enforce: impact in the value's units, likelihood
separate, the fatal rule, countermeasure states with return conditions.
Measure interrogate against function 2's MUSTs. The spike instrument needs
no tool at all — it's a discipline.

**"Do we need to superpowers at all?  what does it do for us that we need?"**
(at DESIGN)
→ **Answered: one capability, nothing else.** The walk already measured
this: the 2-3-independent-approaches generation is the only part that earned
its keep; the waterfall, the menus, the writing-plans handoff and the
dated-snapshot home are explicitly not adopted, and writing-plans was
superseded by conductor in July. Under the tool rule (bounded contract,
returns to caller) superpowers survives as exactly that one capability —
post-walk can test extracting or replacing it so the dependency drops.

**"what about sensei skill for positioning of gaps, and problem solving ?"**
(near GOAL GATE)
→ **Answered: already routed, by the agreed rule.** Sensei declares its
route — asserting a position, proving a gap with measurement, a complex
problem needing point of cause / 5 whys — trigger: a problem that survived a
few attempts. In this flow that fires at FRAME (problem route), VIABILITY
(qualifying with analysis), and inside the LOOP when a piece keeps failing —
feeding What we ruled out. Proven elsewhere; the bet is transfer. Invoked on
match, never as obligation.

**"Sherpa doing heavy lifting, we need to review it to make sure its what we
need"** (at SLICE — sherpa Launch is the drafted server there too)
→ **Agreed and widened.** Sherpa is now named at TWO stages (Explore at
FRAME, Launch at SLICE) while being measurably unused at both. The post-walk
review covers the whole skill against both agreed requirements — triage/two
documents/two keys at FRAME, grouping/ceiling/DONE-assembled at SLICE —
keep/modify/kill per stage on conformance, not as one verdict for the skill.

**"Do we build out own CAPABILITY?"** (at DESIGN — the one superpowers piece
that earned its keep)
→ **Probably yes, and through the flow itself.** The capability is now
specified by our own agreed requirement (generate 2-3 independent
approaches from the intent + qualified risks, score on constant axes), so
building it is a normal piece: framed, sliced, specced, built by a player,
measured. That removes the external dependency and its never-came-back
class entirely. The post-walk phase decides build-vs-extract on cost — the
capability is small enough that build likely wins.

**"Do we need visualization skills for progress / output. What about
documentation or code writing (swift, apple UI etc)"** (near GOAL GATE)
→ **Progress: the requirement already exists — Show where we are.** No new
skill class; the post-walk build gives it its renderer (tools/diagram is
the drafted server: renders the map today, no progress state, nothing
invokes it). Output visualization is already demanded by the design package
(diagrams per aspect) and served by the excalidraw round trip.
→ **Documentation: derived, never a standing skill.** Docs travel with code
as pieces carrying their own checks — "documentation complete" is assembled
from declarations like everything else in DONE.
→ **Specialist code (Swift, Apple UI…): players + declared tools, per the
tool rule.** A builder is a sized model handed an exact spec; domain
capability enters as a bounded tool declared for the terrain (e.g. the
Apple build toolchain) when a piece needs it — invoked on match, returns to
caller, killable. The post-walk inventory should map which domain tools
exist vs are missing for the projects actually in flight.
- 2026-08-06 · kerd-map · Tony: "Do we need these two still, lorg can go, never used — or does it have a place? Claude has plugin management now." → Disposition: lorg-cut queued as evidence-checked Backlog item (rip discipline); interrogate's skill-vs-engine question queued with it; comment cleared at next map re-paste.
