---
route: spike
stage: framed
---

# Standards grounding — every layer stands on a standard, or says why none fits

## Value

**Two of the project's four layers stand on a published standard. Two were
about to be invented.** Measured 2026-08-22, the day both adoptions happened:

| Layer | Standard | Where we stand |
|---|---|---|
| architecture | ISO/IEC/IEEE 42010 | **adopted** — its completeness rule *is* the design gate (`docs/design/gate-visuals.md`) |
| requirements | ISO/IEC/IEEE 29148 | **adopted** — the plain-language word list and the `each` rule both came from it (`docs/design/requirement-shape.md`) |
| process | — | **ungrounded.** Kerd *is* a process and describes itself in prose |
| product | — | **ungrounded.** `R-0011` is approved and says every evaluation carries a **quality** column; nothing defines quality |

**Both adoptions were caught by Law 4, and both times the assumption had
already been written down as fact.** The technique for universal force without
a totality word was declared *"nowhere taught"* and is taught twice over; the
concern/viewpoint/view vocabulary and its completeness rule were about to be
invented and are 42010 verbatim. That is the cost this item measures: invention
where a standard exists, discovered after the invention is on disk.

The law this executes is Tony's, 2026-08-14, at the whole-project altitude:
*"we always need to 1. assess and learn from industry standards, leading
approaches, emerging approaches 2. decide what fits for us 3. consume/adopt
whole if perfect or be inspired by them, 4. design or adapt for our gaps 5.
build for the gaps. do this for every aspect of our project."*

**The design question underneath the map is his too**, 2026-08-22: *"42010's
concepts (stakeholders, concerns, viewpoints) are general enough that people
often reuse them to organize the other layers too."* If that holds, one
vocabulary covers all four layers and we do not need four.

**Winning, in his words (2026-08-22):** *every layer — architecture,
requirements, process, product — names the standard it stands on, or says why
none fits; nothing is invented where a standard already exists.* Measured:
**4 of 4 layers grounded; today 2 of 4.**

## The question

Which standard grounds each of the four layers — and does 42010's
stakeholder / concern / viewpoint / view vocabulary cover all four, so that the
project needs one vocabulary rather than four?

## His map — the candidates, declared before any is read

| Layer | Candidate | Why it is on the list |
|---|---|---|
| requirements | ISO/IEC 26550 — software product lines, feature modelling | where *features* as a formal concept actually lives |
| requirements | ISO 9241-210 — human-centred design | governs how user needs become requirements — and `gate-visuals` has **no viewpoint for UI** (`docs/design/gate-visuals.md`, open question 1) |
| process | ISO/IEC/IEEE 12207 — software life-cycle processes | the reference set |
| process | ISO/IEC/IEEE 24774 — how to *describe* a process: purpose, outcomes, activities, tasks | the nearest analogue to 42010's "how to describe it" flavour |
| process | BPMN (OMG; ISO/IEC 19510) | the de facto notation. The toolkit has `process` and `swimlane`; neither claims conformance |
| product | ISO/IEC 25010 (SQuaRE) — product quality model | **the live one**: `R-0011`'s quality column has no definition, and this is that definition off the shelf |
| product | ISO/IEC/IEEE 15289 — content of life-cycle information items | this is what `docs/product/`, `docs/design/` and `docs/gates/` are, ungrounded |
| product | ISO 10007 — configuration management, the product baseline | relevant to what a *release* is |
| product | ISO/IEC 24748 — the life-cycle management guide tying 12207/15288 together | the map of the maps |

## Method

Per layer, in Law 4's order: read the candidate, decide fit, record one of
three verdicts — **adopt whole**, **adapt** (naming the gap), or **none fits**
(naming why). The verdict is read off against the kill-or-keep below, never
argued afterwards.

**How "read" is done, stated because it bounds the finding.** ISO texts are
paywalled. Reading means the standard's published scope and vocabulary
(freely available), its secondary literature, and wherever a full text is
lawfully reachable. A verdict resting on a summary says so; a verdict on the
full text says so. The two are not the same evidence and are not reported as
the same.

Then the one-vocabulary test: for each layer whose standard is adopted or
adapted, map its core terms onto *stakeholder / concern / viewpoint / view*.
The map either closes or it does not.

**Analysis outranks what was said before it** (Law 4, second half). A
candidate on his map may die on reading; a standard not on the map may
surface. Both are findings, recorded in place with the superseded line struck.

## Kill-or-keep

Declared before it runs.

**A layer's candidate is KILLED if any one of these holds:**

1. **It governs something we do not do.** A standard for system-of-systems
   acquisition, safety certification, or an appraisal programme grounds
   nothing here — it would be adopted for the name.
2. **Adopting it adds ceremony the law forbids.** Law 2: every change lands in
   the spec, design or requirements *"but doesnt have to be huge process"*. A
   standard whose minimum conformance is heavier than the project's own gates
   is adapted or refused, never adopted whole.
3. **It contradicts an approved requirement without beating it on evidence.**
   The register is declared truth. A standard that says otherwise either
   supersedes the requirement by analysis — struck in place, per Law 4 — or
   loses.

**The one-vocabulary hypothesis is KILLED if** mapping any grounded layer
onto 42010's four terms needs a term the standard does not have, or bends one
of its terms past its definition. Bending a word is inventing, one level down.

**KEPT if** a layer's standard survives all three and the project can point at
the clause it stands on. What is kept is **the finding, per layer** — never a
shipped adoption. A spike that ships is not a spike. Each adoption re-enters
the ladder as its own small change, and the first is already visible:

- **ISO 25010 → the definition of `R-0011`'s quality column.** One approved
  requirement, one column, and `tools/design/` already machine-checks the
  matrix. The smallest valuable thing this spike can unlock.
- **ISO 9241-210 → the UI viewpoint `gate-visuals` is missing.** Its design GO
  is held behind this finding, deliberately.

## Deliberately not in this spike

- **Adopting anything.** Findings only; adoptions are separate items.
- **ISO/IEC/IEEE 15288.** System-level; this is software. 12207 is the software
  instance of the same process set.
- **ISO/IEC 33000 and CMMI.** Maturity *appraisal* is a programme, not a
  grounding, and fails kill criterion 1 before it is read.
- **BPMN conformance of the diagram toolkit.** Whether `process` and
  `swimlane` should claim it is a question for the toolkit's adoption, not for
  this map.
- **Rewriting Kerd's skills as 24774 process descriptions.** If 24774 is
  adopted, that is the adaptation item it produces.

## Grounding

- docs/design/gate-visuals.md — where 42010 was adopted, and open question 1 (no viewpoint for UI) that 9241-210 may answer
- docs/design/requirement-shape.md — where 29148 was adopted, and the two techniques that were nearly invented
- docs/requirements/register-v2.md — `R-0011`, the approved requirement whose quality column this grounds; `R-0018`, which routed this item as a spike
- docs/kerd-goals.md — the three laws; Law 2's ceremony limit is kill criterion 2
- CONTEXT.md — Law 4 and its second half, the ordering rule that lets analysis strike a prior statement
