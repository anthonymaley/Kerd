# Requirements traceability — slice 1 design

> **STATUS: BLOCKED at cold eyes, 2026-08-07. NOT signed. No design GO record
> exists and none may be written against this version.** Four independent
> lenses raised findings; 18 survived adversarial refutation. The blocking
> themes are recorded below and must be resolved before this is re-reviewed.
> The producer's human key was given on the alignment artifact (the taxonomy
> and chain); the machine key is refused.
>
> **Blocking themes:**
> 1. **The killer risk's countermeasure does not exist.** The frame grades the
>    skipped-promotion risk `countermeasure - permanent` on the strength of a
>    `gate.py` refusal. AU7/AU8 as designed only validate a register that is
>    already there — nothing refuses a promotion that never happened, and this
>    doc's own Testing strategy waives exactly that. A killer risk without a
>    real countermeasure is a BLOCKER by standing rule.
> 2. **The promotion beat cannot catch its own evidence.** It rides conductor's
>    task framing, which fires only for *new work* and only where entry gates
>    exist. All eight requirements in frame gap 2 — the entire basis for grading
>    the risk — arrived mid-session, not at task framing. As designed the beat
>    would have caught none of them.
> 3. **A false premise is load-bearing.** This doc claims `FUN-001` "deleted the
>    plan gate this same day". It did not: the decision is `final`, the deletion
>    is deliberately blocked (`TODO.md`), and the double-approval it argues
>    against still exists today.
> 4. **The aiming fix is half-designed.** `${CLAUDE_PLUGIN_ROOT}` expands only
>    inside the plugin's own `hooks.json` — not as an environment variable a
>    skill-issued command can read. The state half is real; the script half
>    (how a consuming repo locates `gate.py` at all) is undesigned.
> 5. **The ID regex rejects a legal ID.** `^[A-Z]{3,4}-\d{3}$` refuses `UX-001`
>    — a shipped category and the frame's own worked example. Kerd files zero UX
>    requirements, so its dogfood register cannot catch this; the first
>    consuming project with a UI would. The thin-dogfood risk, biting inside its
>    own design.
> 6. **The edit map is incomplete.** `tools/gates/README.md` is the AU law's
>    declared home and states "the six rules" and "AU1–AU6"; adding AU7/AU8
>    without amending it manufactures a declared-truth gap.
> 7. **An obligation the frame placed on this rung was declined.** The frame
>    said whether category dispositions and rigor classes share one table or one
>    pattern "is a design-rung decision". This doc restates the exclusion
>    instead of deciding, then ships a second disposition table anyway.

Frame: `docs/product/requirements-traceability.md`. Slice 1 only: a durable
input becomes an addressable requirement, in the user's own repo, and the
machinery can read it there.

**The alignment artifact for this design is the producer's taxonomy and chain,
not a drawing** (Tony, 2026-08-07: *"i gave you the drawing in text form there,
the categories etc - i approve the drawing not needed"*). Both are in the
frame's `## Value`, enumerable and pointed-at row by row. The standing rule is
that alignment needs a shared structure; a drawing is its usual form, not its
only one.

## What it does

A project opts in by declaring a **register** in its own repo. The register
holds one row per requirement: a stable ID, its category, the requirement in
the producer's words, and exactly one state. Alongside it, the project declares
a **disposition** for each of the twenty categories — `applies`, or `n/a` with a
named reason — so an empty category can be told from a missing one.

Nothing is derived. The register is written by the promotion beat and read by
everything downstream. That is deliberate: this is the one artifact in the
system whose content cannot be derived from disk, because human input leaves no
trace until someone writes it down.

## The three artifacts

All three live in the **user's project**, never in Kerd. Kerd's own copies exist
because Kerd is built with Kerd.

| Artifact | Path | Kind | Written by |
|---|---|---|---|
| The register | `docs/requirements/register.md` | living, overwritten in place | the promotion beat |
| The category disposition | `docs/requirements/categories.md` | living, rarely changed | the producer, at opt-in |
| The catalog (shipped default) | the skill's own text | immutable, ships with Kerd | nobody — it is the standard |

`docs/requirements/` is a new directory and the only structural addition.

### The register row

```
| ID | Category | Requirement | State | Source |
|---|---|---|---|---|
| NFR-001 | Non-functional | The boundary records everything agreed; efficiency is a tiebreaker, never a reason to record less | final | 2026-08-07 session |
```

- **ID** — `<CODE>-<NNN>`, zero-padded to three. Stable for the life of the
  project; never renumbered, never reused. A superseded requirement keeps its
  ID and changes state.
- **Category** — one of the twenty codes, and its disposition must be `applies`.
- **Requirement** — the producer's words. Compressed for the row, never
  paraphrased into the model's vocabulary.
- **State** — exactly one of a closed set (below).
- **Source** — where it came from, so the full wording is reachable.

### The states

Borrowed wholesale from the risk ledger, which has run since v0.72.0 and is
machine-checked today. Tony's shape: *"any request should be qualified and if
its durable we should make it a requirement, might go through stages to be
final."*

| State | Meaning |
|---|---|
| `proposed` | captured, not yet qualified — the holding state |
| `qualified` | judged durable, wording agreed, not yet signed |
| `final` | the producer's key is on it; it is a requirement |
| `superseded` | replaced by another ID, which is named |
| `dropped` | deliberately abandoned, with a reason |

`proposed` and `qualified` exist because Tony named stages explicitly. Without
them the register would force a request to be either final or absent, which is
the same all-or-nothing failure prose has.

### The category disposition

One row per category, all twenty present, none omittable:

```
| Code | Disposition | Reason |
|---|---|---|
| SEC | n/a | no security surface — a local CLI plugin with no auth, no network, no user data |
| FUN | applies | |
```

`n/a` **requires** a reason; `applies` takes none. Same asymmetry the risk
ledger already enforces on `accepted`, and for the same purpose: the cheap
state is the one that must be argued for.

## The promotion beat

Where a request becomes a requirement. This is the killer risk's countermeasure
and the only part of the design that spends producer attention.

**It sits inside the framing conversation, not beside it.** Conductor's task
framing already produces `docs/product/<slug>.md` with the producer's key on
`## Value` (v0.94.0). Promotion rides that same beat rather than adding a second
sign-off — adding one would repeat the double-approval that `FUN-001` deleted
from the plan gate this same day.

The sequence, from Tony's words:

1. **A request arrives** — in conversation, as it always does.
2. **Qualify it.** Is it durable, or is it about this task only? Durable means
   it constrains future work. `/kerd:interrogate` does exactly this shape for
   risks already.
3. **If durable, draft a row** — proposed state, category assigned, the
   producer's wording preserved.
4. **The producer's key moves it to final.** Read back before writing, as
   `## Value` already requires.

**What makes this survive contact with a busy session:** it is a declared
artifact with a gate, not a habit. The frame's killer-risk row says plainly
that encouragement has a measured success rate of zero here — the evidence
being that this very session produced eight durable requirements while
discussing the need to capture them, and promoted none.

## The aiming fix

`tools/gates/kit.py:24` derives `ROOT` from the tool file's own path. Run from a
consuming project, that resolves to the plugin cache rather than the project.

**The pattern is already in this repo, in four files, shipping since v0.19.0:**
every hook uses `${CLAUDE_PLUGIN_ROOT}` to find its *script* and
`$CLAUDE_PROJECT_DIR` to find its *state*, guards the variable, and `cd`s there
before doing anything.

The change is a CLI argument, not a refactor. `kit.py:22-24`'s own comment says
why: *"The CLI passes ROOT; selftest passes a temp tree instead — every function
below takes `root` as a parameter for exactly that reason."* The library is
already parameterised. Only `gate.py`'s entry point pins it.

- `gate.py` gains `--root <path>`, defaulting to `kit.ROOT` so every existing
  invocation is byte-identical in behaviour.
- Skill text that instructs a tool run passes the project directory.

## Edit map — four files

| File | Change | Why |
|---|---|---|
| `tools/gates/gate.py` | add `--root <path>`, default `kit.ROOT`; thread to every subcommand | the aiming fix; without it the checks below cannot run in a consuming repo |
| `tools/gates/kit.py` | add `REQUIREMENT_STATES`, `CATEGORY_CODES`, and a register/disposition parser + checker | the legal sets and the refusal, beside the ones they resemble |
| `skills/conductor/SKILL.md` | the promotion beat inside task framing | where a request becomes a requirement |
| `README.md` | the capability, and What's New | a user-facing capability must be described in the user's terms |

`docs/requirements/` is created by the opt-in, not by this edit.

## The checks

Two, both inside `gate.py audit` (AU7, AU8). **CI gains no step** — they ride
the existing audit, following the AU5 and AU6 precedent.

- **AU7 — the register is well-formed.** Every row has five columns; every ID
  matches `^[A-Z]{3,4}-\d{3}$` and is unique; every state is in the legal set;
  every `superseded` row names its replacement and that ID exists; every
  category code is real and its disposition is `applies`.
- **AU8 — the disposition is complete.** All twenty categories present, each
  `applies` or `n/a`, and every `n/a` carries a non-empty reason.

**A project with no `docs/requirements/` is silent, not red.** Declaring is
opting in — the grounding-was-read precedent (2026-08-05), where retrofits were
refused because they manufacture hollow declarations.

## Named answers — the stage-1 measurements

| Measurement (frame, Value) | Target | Named answer |
|---|---|---|
| Durable inputs recorded as addressable rows, not prose | 0 → the session's own count | Kerd's register is seeded at build with the eight requirements the 2026-08-07 session produced (frame gap 2), which is the first real content and the only honest one available — they are already extracted and filed. Verified by `gate.py audit` passing AU7 over a non-empty register. **Limit, named:** this measures that the beat ran once, not that it keeps running; the second is prompt-layer and unmeasurable from disk. |
| Categories whose applicability is undeclared | all 20 → 0 | AU8 refuses any disposition file missing a category or carrying a reasonless `n/a`. Asserted by fixture: a disposition with 19 rows must fail, and one with 20 where `SEC`'s reason is empty must fail. |
| The machinery can audit a project that is not Kerd | no → yes | `gate.py --root <tmpdir> audit` run against a temp tree containing a register, asserting it reports that tree's rows and not Kerd's. This is the existing selftest pattern — `kit` functions already take `root`, and the selftest already passes temp trees. |
| A requirement is answerable by ID | not answerable → answerable from one file | `gate.py` reports a named ID's row, or refuses if absent. Asserted by fixture on `NFR-001`. **Limit, named:** slice 1 answers *what the requirement is*, not *what satisfies it* — the forward wiring to measurements and pieces is slice 2, so "what code satisfies NFR-001" is still unanswerable after this ships. |
| Existing behaviour unchanged for repos that do not opt in | byte-identical | `gate.py audit` with no `docs/requirements/` present produces the same output as today, asserted by the existing 26 selftest cases passing unmodified, plus this repo's own audit before the register is seeded. |

## Testing strategy

New fixtures in the existing selftest harness, which is where the legal-set
checks already live: a well-formed register and disposition (pass); a duplicate
ID; a malformed ID; an illegal state; a `superseded` row naming a missing ID; a
requirement in a category dispositioned `n/a`; a 19-row disposition; a reasonless
`n/a`. Plus one `--root` case asserting a temp tree is audited rather than Kerd.

The rigor level is `mvp` and this is its honest disposition:

- **Measured** — the five rows above, all diff- or fixture-scoped.
- **Waived by name** — that the promotion beat is actually *used* in later
  sessions. No harness can observe a conversation, and a model choosing to
  comply is not a check. The observation is the first session after ship that
  produces a durable requirement; recorded in that session's log. This is the
  killer risk's residue and it is stated rather than designed away.

## Out of scope, named

- **The forward wiring** — requirement → measurement → piece. Slice 2. Building
  both halves at once means neither gets a real test.
- **Project-type templates and per-level floors.** The same object as
  `rigor-level` slice 2 (*"catalog + pre-filled disposition table"*), designed
  and unbuilt. Two mechanisms declaring what a project owes would disagree.
- **Any retrofit of the twenty existing slugs.** Manufactures requirements
  nobody stated.
- **The top and bottom of the chain** — Business Goal, Stakeholder Need,
  Post-Launch Metric. Recorded in frame gap 6; slice 1 builds only the link
  where the break is.
- **Release planning.** This makes it expressible; building it is its own work.
- **Rendering the register on the journey page.** The page should render
  something that exists.
