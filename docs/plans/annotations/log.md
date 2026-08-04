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
