# Drive — design

The design package for the work item `funnel-driver`. The thing being built is
**Drive** (`/kerd:drive`, `skills/drive`). The slug keeps its original name
because slugs name work items, not skills — the same convention as `mode-cut`,
`vault-unhook` and `gate-visuals`.

Frame: `docs/product/funnel-driver.md`. Three views sealed beside this document,
all approved by Tony on 2026-08-23: `funnel-driver/why-an-umbrella.html`
(`fp:54f84887b8b8`), `funnel-driver/gate-loop.html` (`fp:47883502cf4b`) and
`funnel-driver/span-vs-slice.html` (`fp:5adeb340c7ee`).

## Grounding

- docs/product/funnel-driver.md — the frame this designs; the mechanism and the gate loop were decided there
- docs/design/funnel-driver/why-an-umbrella.html — why Drive sits above conductor, sealed
- docs/design/funnel-driver/gate-loop.html — how one gate behaves end to end, sealed
- docs/design/funnel-driver/span-vs-slice.html — why a work item and a session cannot be nested, sealed
- docs/design/conductor-role.md — the 2026-08-04 spec whose graduation map this replaces
- skills/conductor/SKILL.md — the thing Drive calls and must never require to change
- docs/product/requirements-project-type-templates.md — the fifteen types, now migration evidence rather than canon
- tools/gates/README.md — the rung ladder, the front-matter vocabulary, the gate record schema
- CONTEXT.md — the four-role seating, the currency rule, Law 4 supersession

## The canonical language — DECIDED 2026-08-23

Drive moves things that are not products. A content plan, a business plan, a
document, a repair and a rough idea are all legitimate work, and the existing
vocabulary silently assumed software. Three names change and one field is
retired.

| Concept | Canonical name | Note |
|---|---|---|
| The thing Drive moves | **work item** | not "product", not "feature" |
| Its living artifact | **work record** | one file, the item's home |
| That file's home | `docs/work/<slug>.md` | **canonical target** |
| That file's home *today* | `docs/product/<slug>.md` | **current physical storage — legacy** |
| Reusable question sets | `docs/work/question-sets/<work-type>.md` | seeds, per work type |

`docs/product/` is named here as **physical storage that has not migrated yet**,
never as the concept. Every sentence in this design says *work record*; the path
appears only where the machinery's current behaviour is being described. The
migration is a following slice, measured below.

### Three axes, and `project type` is superseded

The 2026-08-07 decision made `project type` a single field that "is the
project's current state" and advances at the goal gate. **That decision is
superseded.** The field mixed three things under one name — the same defect that
`Cost` had in the tooling evaluation, and it fails the same way: a field wearing
three meanings cannot be checked against any of them.

| Axis | Answers | Declared by | Advances? |
|---|---|---|---|
| **Work type** | what kind of thing this is at all | the producer, at intake | no |
| **Route** | how it enters the ladder — `new \| problem \| spike` | derived at the entry gate | no |
| **Lifecycle position** | where the thing is in its life | the goal gate | **yes** |

Work type examples, deliberately not software-only: software change ·
enhancement · content plan · business plan · document · repair.

**`project type` is retired as a field name.** It is not kept as a valid axis
underneath the three, because keeping it would leave two overlapping
classifications standing — which is precisely the loop the supersession rule
exists to prevent.

**The fifteen written types become migration evidence, not canon:**

- **Eight are lifecycle positions** — Ideation, Spike, MVP, Pilot, Beta, Full
  Release, Maintenance, Decommission. These genuinely advance into one another.
- **Seven are work types wrongly filed** — Security Review, Experiment/A-B,
  Hotfix, Migration/Cutover, Platform Change, Compliance Release, Internal
  Tooling. None of these advances into any other; a Hotfix does not become a
  Migration.
- **The gaps are the argument.** No entry among the fifteen accommodates a
  content plan or a business plan. The old field was too narrow by construction,
  and the absence is the evidence.

## The settled mechanism — Drive owns the item, conductor owns the session

The sharpest statement of the umbrella decision, and the reason "above" rather
than "inside" is structural rather than a preference:

```
/kerd:drive       owns the WORK ITEM
                  frame → viability → slice → design → contract → build → goal → loop
                  spans many sessions · state lives on disk in the work record

/kerd:conductor   owns the SESSION
                  orient → plan → execute → close
                  spans one sitting · state lives in kivna/.active-modes
```

They are different objects with different lifetimes. A work item outlives dozens
of sessions; a session may touch several work items. **Drawn at
`funnel-driver/span-vs-slice.html`** — a span and a slice on one grid, which is
what makes the mismatch countable rather than merely asserted. **That is why the driver
could never have been a graduation into conductor** — it would have made one
object's lifecycle a phase of another's, and every awkward clause in the
2026-08-04 graduation map is a symptom of that mismatch.

**The rule this is built under, carried verbatim from the frame:**

> Drive may CALL conductor, but must never REQUIRE conductor to change.

The moment a slice needs conductor to behave differently, the retired killer risk
is back in full, and that slice either does the work itself or stops.

## What Drive is

A skill at `skills/drive/SKILL.md`, invoked as `/kerd:drive`. In Kerd a skill
*is* its command — the plugin system supplies the `kerd:` prefix — so there is no
separate command artifact to build.

**Why `drive` and not a standard-vocabulary term, stated because it does not pass
the currency rule cleanly.** The rule says use the name the field already says;
the closest standard term is Stage-Gate, which is gate-centric, corporate, and a
registered mark. `concert` was refused as an invented name because parsing it
required knowing Kerd's own producer/composer/conductor metaphor. `drive` is
different in kind: it is a common verb used in its plain meaning — guide, keep
moving, hold accountable — so nobody has to learn anything to read it. The test
the currency rule is actually protecting is *does the reader need to be taught
this word*, and `drive` passes that even though it is not a term of art.

## How Drive calls conductor

Drive holds the item's rung. When a rung needs work done in a sitting, Drive
invokes `/kerd:conductor` through the Skill tool and hands it a task framed from
the work record — the same invoke pattern conductor's own close-out already uses
to call `/kerd:switch out`. One definition, two callers, no re-description.

Conductor receives a framed task and does not know it came from Drive. It runs
orient → plan → execute → close exactly as it does today. Nothing in
`skills/conductor/SKILL.md` changes.

**The check that keeps this honest at build time:** a diff on
`skills/conductor/SKILL.md` in any Drive slice is a refusal, not a review
comment.

## Where the question set lives

**In the work record, as a `## Question set` section.** Not a separate top-level
file, not skill text.

- **The seed** comes from `docs/work/question-sets/<work-type>.md` — a reusable
  set per declared work type.
- **The instance** is copied into the work record at intake and edited there.
  What the person edited is what exists; the seed is never read again.
- **Editable before starting, never skippable during.** Skipping was withdrawn by
  its proposer (*"yeah i was wrong on skip"*): editing up front preserves
  flexibility, while skipping mid-flight breaks all three uses of the list at
  once.
- **Declared, never inferred.** The work type is declared by the producer. A
  system that guesses is wrong about a third of the time (33.8% misclassification
  across 7,000+ manually reviewed reports — Herzig, Just & Zeller, ICSE 2013) and
  fails *silently*: the question you needed is never asked and you never learn it
  was missing.

Because the person owns the set, it lives in **their** repo — the standing house
rule for anything project-specific.

## How the completeness check reads it

One list, three uses, one source — the producer's correction at the gate loop
(*"this needs to be based on step 2 as well right?"*):

| Use | Reads | Produces |
|---|---|---|
| **Ask** | `## Question set` | the questions put to the person |
| **Check** | the same section | what counts as finished at this gate |
| **Show** | the same section | *now > X, next Y, after Z* |

**Two gaps in today's machinery this replaces, both measured rather than
asserted.** *Ask · check · show from one source* does not exist now: the three
are separate things and **two of them do not exist at all**. And **approval today
has no "comment" state** — a view is sealed or it is not, so *"nearly, but change
this"*, which the gate loop says is the normal answer, has nowhere to land.

The check counts answered entries against declared entries in the same section.
It never judges whether an answer is *good* — that is the human key at the gate,
and the machine's writ stops at presence.

**This is a design proposal, not a settled decision.** It is the design rung's
business and the producer rules on it at the GO.

## Named answers — the stage-1 measurements

| Measurement (work record, `### Value, in units`) | Target | Named answer |
|---|---|---|
| Funnel stages with an owner | 5 of 8 → 8 of 8 | Drive owns `frame`, `slice` and `design` — the three with no owner in any skill. Verified at build by `gate.py route` on a real item reaching `design pass` with every input written by Drive rather than by hand. Honest limit: ownership is prompt-layer; no runtime refuser observes whether Drive or a human wrote the section. |
| Skills that know the funnel exists | 2 of 9 → 3 of 10 | `grep -c 'frame\|viability\|slice\|design\|contract\|build\|goal\|loop' skills/drive/SKILL.md` non-zero at build; count of skills rises by the new one. |
| Graduation triggers fired and shed nothing | 1 → 0 | The pre-flight inventory trigger is discharged by Drive owning intake, not by editing conductor. Asserted by diff scope: zero hunks in `skills/conductor/SKILL.md`. |
| Standing decisions contradicted by shipped skill text | 1 → 0 | The unconditional plan gate. **Not answered by this slice** — named as an open gap rather than claimed, since it lives inside conductor and the umbrella rule forbids touching it. |
| Work commits carrying machine-readable piece progress | 0 → every one | Shipped at v0.91.0 (`Piece:` trailer). Verified by `git log --format=%B -50 \| grep -c '^Piece:'` returning non-zero. |

The fourth row is deliberately unanswered. A named answer that cannot be given is
recorded as a gap rather than invented — the gap `gate-visuals` left open, not
repeated here by writing a target after the fact.

## Open questions

- **Does re-agreeing a lapsed approval cost anything?** The fingerprint machinery
  records what was agreed and lapses on edit, which is compatible with
  *agreed-for-now, not locked* — provided coming back is cheap. If re-agreeing
  means re-walking the gate, early gates must not lock at all. Untested.
- **Which of the fifteen types seed which question sets.** The eight/seven split
  above is the mapping's input, not the mapping. Slice 2 writes exactly one set
  by hand and the generalisation waits for evidence.
- **Where the declared work type is stored.** Front matter on the work record is
  the candidate, consistent with `route` and `stage`. Contract's to settle.

## What this design does NOT do

- **It does not migrate `docs/product/` to `docs/work/`.** Measured at ~180
  references (`kit.py` 127, `gate.py` 9, `fidelity.py` 3, 2 skill files, 40
  files under `docs/design/` including text baked into `.excalidraw` and `.svg`,
  plus README, CLAUDE.md, the playbook) and a 20-file move. The board derives
  every slug from `docs/product/*.md` filenames, so a half-done migration turns
  the render red. Named as a following slice with the measurement attached so
  nobody re-derives the cost.
- **It does not split the fifteen project types into their new axes.** Separate
  item, following slice. This design settles the *language*; the retrofit is
  work.
- **It does not touch conductor.** By rule.
- **It does not build a question-set template system.** One set, hand-written,
  used once — the abstraction waits for a second instance.

## The limit, stated

Drive can force the stages and count the answers. It cannot tell whether an
answer is true, whether a drawing means anything, or whether the work item was
worth starting. Every one of those is a human key, and this design adds no
machinery that pretends otherwise.

The declared-limit class is the same as `grounding-was-read` and the view lock:
**presence is checkable, comprehension is not.**
