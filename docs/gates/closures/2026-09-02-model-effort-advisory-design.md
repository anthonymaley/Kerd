---
route: new
stage: scoped
---

# LEGACY CLOSURE — model-effort-advisory

**Keyed by the producer 2026-09-02**, on its own key — separate from
`inline-composer`'s design key and separate from `switch-fidelity`'s waiver.

> **THIS IS NEITHER A DESIGN GO RECORD NOR A WAIVER.**
>
> **It closes the ROUTING gap:** the item has been demanding a design GO record
> it was never going to receive, and it may now move forward.
>
> **It does NOT close the EVIDENCE gap:** no design was written, drawn, declared
> or agreed before the build. That evidence is missing, it stays missing, and
> **this record does not supply it, recreate it, or imply it has appeared.**

---

## 1. What shipped — verified, not recalled

**v0.98.0 · commit `f4c51c0` · 2026-08-13.** All five scope bullets are live in
`skills/conductor/SKILL.md` today, checked line by line on 2026-09-02:

| Scope bullet | Verified at |
|---|---|
| Advisory becomes model *and* effort, bidirectional | `:103` — *"advise the **conductor pair** — the model AND reasoning effort holding the baton"* |
| Names the downgrade explicitly when overpowered | `:111` — *"An overpowered session is advised DOWN, by name"*, with the `Fable xhigh → Opus medium` example |
| The composer call gains a sized effort | `:228` — *"at a sized effort of its own"* |
| Frontmatter trigger description follows the behaviour | `:3` — *"advises the conductor model and effort up front"* |
| README conductor section + version bump 0.97.0 → 0.98.0 | in `f4c51c0`'s diff: `README.md`, `plugin.json`, `marketplace.json` |

**The requirement it was built against exists and is keyed.** `FUN-010`, state
`final`, `Approved: sha256:b4537fbe358a`, carrying the producer's verbatim
mid-session words as its `Source`. **This is the one piece of prior declared
truth the item does have** — a keyed requirement is not a design, but it is
evidence that what shipped was what was asked for.

## 2. Why this is neither a GO nor a waiver

**Not a GO.** A GO says the design evidence exists and the producer read it.
There is no design document, no view, no declared concern and no approval. There
is nothing to have read.

**Not a waiver.** A waiver's load-bearing field is *evidence the skip was
deliberate rather than forgotten*. **Nothing was skipped, because nothing was
owed.** Two facts establish this, both measured:

- **The frame and the build landed in the same commit.** `docs/product/model-effort-advisory.md`
  was *created* by `f4c51c0` — the item never entered the ladder ahead of its
  own build, so there was no design rung standing in front of it to skip.
- **The rule exempting it was live in the same file at the same commit.**
  `skills/conductor/SKILL.md` at `f4c51c0` says *"No composer call, no spec
  file"* for lean/inline work. Inline work was routed away from the composer
  **by rule**. No score was owed, so no design artifact was owed.

Writing a waiver here would fabricate a decision nobody made. Writing a GO would
fabricate evidence nobody produced.

**The item's own successor says this is the route.** `inline-composer`'s frame
excludes closing it and states: *"They are the evidence that motivated this
item, not its scope; they close through whatever this produces, in their own
sitting."* This is that sitting.

## 3. When the obligation began

**2026-09-02** — the date `inline-composer`'s design was keyed (`83b1299`).
Before it, inline work owed no score and no design. **Work that shipped before
that date cannot be judged against an obligation that postdates it**, and this
record refuses to do so.

## 4. What future work MAY rely on

- **The shipped behaviour**, verified by reading the live text at the line
  numbers in §1. The advisory exists and works; that is checkable today and
  will stay checkable.
- **`FUN-010`** as the producer's stated requirement, keyed `final` with its
  approval hash intact.
- **Commit `f4c51c0`** as the immutable record of exactly what changed.

## 5. What future work must NEVER infer

- **That a design was agreed.** None was. No package, no drawing, no concern,
  no approval.
- **That the shipped shape was chosen over alternatives, or that alternatives
  were weighed.** Nothing records that, and it should not be assumed from the
  fact that the code is coherent.
- **That the absence of a design record means the design was sound.** Absence is
  not evidence. The reasoning behind the shipped shape was not preserved —
  **not because nobody could have produced it, but because the process did not
  require it and did not keep it.**
- **That this record is precedent.** It is not. See §6.

## 6. Scope and precedent

This closure covers **`model-effort-advisory` only.** `hooks-autoload` is the
sibling case named in the same frame clause and closes separately, on its own
key, with its own verified scope.

**It cannot become a precedent by construction.** The mechanism it closes under
was built on 2026-09-02: inline work now produces a score, so no item shipping
after that date can be in this position. A later item reaching for this record
would be claiming an exemption whose enabling condition no longer exists.

## 7. Downstream obligation — the evidence gap stays visible

**Every later `model-effort-advisory` record names this closure**: any handoff
record, any acceptance record, any future slice's frame. The design rung reads
**`legacy closure`** on every surface that reports it — never `design pass`,
never `design waived`.

**Known limit, measured rather than asserted.** With this record in place the
machine is unchanged:

```
$ python3 tools/gates/gate.py route model-effort-advisory
enters at: design
need: docs/design/model-effort-advisory.md — file exists
need: docs/gates/*-model-effort-advisory-design.md — design GO record
```

`tools/gates/` was untouched by the 2026-09-02 key. Nothing renders `legacy
closure`, nothing routes forward on one, and nothing carries the evidence gap
into downstream records automatically. **Until that is built this obligation is
prompt-layer and nothing enforces it.**

## 8. Home — and why it is not the waivers' home

**`docs/gates/closures/` holds legacy closures. `docs/gates/waivers/` holds
deliberate skips, and only those.** The producer's ruling, 2026-09-02:

> They represent opposite historical claims: a waiver proves an obligation
> existed and was consciously skipped; a legacy closure proves the obligation
> did not yet exist and must not be reconstructed. Combining them would blur the
> distinction the records are meant to preserve.

Both sit in subdirectories because `AU3` admits only rung-suffixed filenames
directly under `docs/gates/`, so neither record type has a legal gate-record
name today. AU3's glob is non-recursive, so a file here is correctly **not**
counted as a gate record — and the design-GO glob stays empty, verified with
this file in place.

---

**Producer key:** Tony, 2026-09-02

**Clock:** 15:16 EDT
