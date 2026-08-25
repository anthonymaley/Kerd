---
route: new
stage: designed
story: proposal
concerns:
  - concern: what each gate checks, and what each renamed word actually costs
    viewpoint: matrix
    view: docs/design/rung-vocabulary/rungs-and-artifacts.html
    approval: Tony, 2026-08-25 · fp:8daab36a9d76
  - concern: why loop is a container and acceptance is the producer's last gate
    viewpoint: nested
    view: docs/design/rung-vocabulary/the-ladder.html
    approval: Tony, 2026-08-25 · fp:e2e788033798
---

# Three rung names only work for software — and drawing the ladder found a fourth defect

## Value

Tony's statement, 2026-08-23 evening, raised while the `funnel-driver` contract
spec was about to be written:

> What I'm after: names a newcomer can understand or search unaided, but not
> blindly Stage-Gate or software jargon.
>
> The rule is cross-work readability. Drive handles software changes, content
> plans, business plans, documents, repairs, and rough ideas. So a term that
> only works cleanly in product/software fails, even if it has currency there.

And the sharpening that started it, on `slice` specifically:

> It is not really "proprietary." `vertical slice` and story slicing are real
> agile terms, but they are software-shaped and mean the deliverable increment,
> not the phase. That makes `slice` a bad Drive rung because Drive now covers
> content plans, business plans, documents, repairs, etc. A newcomer may know
> what "scope" means; they may not know why a business plan is being "sliced."

**This is a cross-work naming pass, not a Stage-Gate adoption pass.** Stated
here because the obvious failure mode is swapping one closed vocabulary for
another: Stage-Gate is launch-shaped and corporate, and adopting it wholesale
would fail the same newcomer for the opposite reason.

**It amends the currency rule rather than replacing it.** The 2026-08-23 morning
rule was *use the name the field actually says*. That is necessary and not
sufficient: `slice` has real currency in agile and still fails here, because the
field it has currency in is only one of the six kinds of work Drive moves. The
test gains a second clause — **current AND readable across every work type.**

### Value, in units

| Measurement | Now | Target |
|---|---|---|
| Rung names readable across all six declared work types | 5 of 8 | 7 of 7 |
| Rung names with no term-of-art collision | 7 of 8 | 7 of 7 |
| Rung names a newcomer can search and get this meaning | 5 of 8 | 7 of 7 |
| Route positions that blur machine work with producer approval | 2 | 0 |
| Execution mechanics exposed as producer-visible gates | 2 | 0 |

The six work types are the ones named in `docs/design/funnel-driver.md`:
software change · enhancement · content plan · business plan · document ·
repair.

## Grounding

- docs/design/funnel-driver.md — the canonical language and the six work types this must read across
- docs/product/funnel-driver.md — the frame whose contract spec is blocked behind this
- tools/gates/kit.py — `RUNGS` (line 34) and `GATE_RECORD_RE` (line 91) are the two places the ladder is pinned
- tools/gates/README.md — the canonical home of the rung vocabulary and the gate-record schema
- CONTEXT.md — the currency rule (2026-08-23), Law 4 supersession, the cross-cutting sweep obligation

External sources are cited inline in the findings below rather than listed here:
`## Grounding` resolves every reference against the filesystem, so a URL is
refused. Named as a gap in the ledger.

## The findings — all eight rungs tested

Tested against two questions: does the field use this word for this thing, and
does it read across all six work types?

| Rung | What it does | Field term | Cross-work | Verdict |
|---|---|---|---|---|
| `frame` | state the problem, value in units, grounding | *Discovery*; "problem framing" | reads fine for a repair, a document, a business plan | **keep** |
| `viability` | is this worth doing at all | *Viability* — one of the three DVF lenses | reads fine everywhere | **keep** |
| `slice` | pick the smallest valuable increment, name exclusions | "vertical slice", "story slicing" | **fails** — software-shaped | **rename** |
| `design` | the design package | Design, within Development | reads fine everywhere | **keep** |
| `contract` | make the work build-ready | none; collides with design-by-contract | reads, but the word is Kerd-internal | **rename → `handoff`** |
| `build` | build it | *Development* | reads fine everywhere | **keep, but demoted — a loop internal, not a route position** |
| `goal` | a machine check: zero unchecked pieces | *Launch*; "acceptance", "definition of done" | **fails** — names the target, not the phase, and no human is near it | **folds into `loop`; its human key becomes `acceptance`** |
| `loop` | today: gated by the goal record (the human key) | *Post-Launch Review*; "feedback loop" | plain enough; launch-shaped alternatives are worse | **keep the word, move the job — becomes the build/verify/adjust container; its human key becomes `acceptance`** |

**The evidence that `slice` is software-shaped rather than merely unfamiliar.**
Humanizing Work's definition, fetched 2026-08-23 from
`humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/`: *"a
work item that delivers a valuable change in **system behavior** such that
you'll probably have to touch multiple **architectural layers** to implement the
change."* Both anchors — system behavior, architectural layers — are software.
The term is current; its currency does not travel.

**Stage-Gate was checked and deliberately not adopted wholesale**
(`stage-gate.com/blog/the-stage-gate-model-an-overview/`, read 2026-08-23). Its
stages — Discovery, Scoping, Business Case, Development, Testing & Validation,
Launch — are launch-shaped and corporate. `scope` is taken from it; the rest is
not.

**`goal` fails harder than `slice`, and it was not the one flagged.** "Goal"
names the target you were aiming at, not the stage where you prove you hit it. A
search for it returns goal-setting, not an acceptance phase. It is also the only
renamed rung appearing in an immutable filename — see the ledger.

**The eight tested become seven, because drawing them found a structural defect
under the naming one.** That is in the settled ladder below, not here: the
findings table is what the currency test returned, kept as the record of what was
asked and answered.

## The settled ladder

Tony's, 2026-08-23, and amended by him the same evening after it was drawn.

**Amended after the ladder was drawn.** The first version of
this section was a flat eight-rung list with three renames. Drawing it showed
that was wrong: `build` and `acceptance` were never peer rungs. **`RUNGS` goes
from eight entries to seven.**

```
frame → viability → scope → design → handoff → loop → acceptance
                                                 │
                                                 └─ build → verify → adjust ─┘
```

| Change | From | To | Stage value |
|---|---|---|---|
| 1 | `slice` | `scope` | `scoped` |
| 2 | `contract` | `handoff` | (stage value to settle at design) |
| 3 | `goal` + `build` | `loop` (one route position, a container) | (to settle at design) |
| 4 | `loop` | `acceptance` | (stage value to settle at design) |

**`loop` is a container, and `acceptance` is the producer's last gate.** His
model: *"loop = build, verify, adjust, repeat · acceptance = producer approval
that the work meets the agreed goal."* The loop starts once handoff has produced
a build-ready package and runs until the work is worth putting in front of a
person. If the producer says *"nearly, change X"*, acceptance fails and the item
goes back round rather than ending.

**Inside the loop, the check is never called acceptance.** Call it **verify**,
goal check, or proof. His rule: *"The machine can verify against the spec and the
goal; only the producer accepts the work."*

**A retired name is an alias for READING, never for writing — and that is what
makes the fold real.** New gate records at the last gate are written
`docs/gates/<date>-<slug>-acceptance.md`. The seven existing `-goal.md` records
are never renamed and stay readable forever. His test, raised at the view gate
and the reason this sentence exists: *"if the intent is to keep writing goal.md
forever, then `goal` is not really folded away."* Correct — an alias that is
still written is not a retirement, it is a synonym, and two live names for one
thing is the defect this item exists to remove.

**The producer holds two keys, and they answer different questions** — `handoff`
says the package is **build-ready**, `acceptance` says the work is **done**.
Conflating them was a defect in the first draft of the drawing, caught by its
reader.

### build, verify and adjust are loop internals, not route positions

His ruling, and the rationale is the load-bearing part:

> Gates should be producer-visible state transitions. Build/verify/adjust are
> execution mechanics. If they become gates, you recreate the old problem where
> machine work and producer approval are blurred.

So the machine checks at the **loop's edges**, never inside it:

| Moment | What the machine checks |
|---|---|
| **Enter loop** | handoff has passed — a build-ready package exists |
| **Stay in loop** | pieces are being built, verified and adjusted — *not gated* |
| **Exit loop** | no unchecked pieces remain, evidence ready for producer review |
| **Acceptance** | the producer's final approval, or it goes back into loop |

`gate.py` must not expose `build`, `verify` or `adjust` as `enters at:`
positions. **If internal visibility is wanted, it belongs in the progress view,
not the gate router** — the router answers *where does the producer look*, the
board answers *how far along is the machine*.

### The old names had the machine check and the human key backwards

~~**This restructure changes no machinery — it is the first naming that matches
what the gates already do.**~~ **STRUCK 2026-08-25 — two checks do move.** The
claim was true of the `build`/`goal`/`loop` fold below, which is what it was
written about, and it was then read as covering the whole item. It does not:
`## Release slice` moves from the design gate to the scope gate, and viability
gains a check it has never had. See *The gates were also holding the wrong
things* below. Verified in `tools/gates/kit.py`:

- The old **`goal`** rung requires exactly one thing: *"zero unchecked boxes in
  Pieces"*. A pure machine test. The word sounds like the producer's target and
  no human is anywhere near it.
- The old **`loop`** rung is gated by `docs/gates/*-<slug>-goal.md` **with a
  `Done condition` section** — which is where cold eyes and the expert-user pass
  actually live. The human key was already there.

So machine-check-then-human-key was already the order. Only the labels were
inverted — **for this fold**. The fold itself is free; the item is not.

### The gates were also holding the wrong things — 2026-08-25

The producer, reading the sealed drawing: *"scope, that is not a risk ledger.
its where we lock in what we want, what features etc... that will go into design
and then loop."*

He is right, and `tools/gates/kit.py` confirms the mismatch. Today `kit.py:627`
gates the scope rung on `## Risk ledger`, while `kit.py:643` gates the **design**
rung on `## Release slice` — so the machine checks *risk* where scope belongs and
checks *what we are committing to build* one rung later.

**`## Release slice` moves up to the scope gate and is renamed `## Scope`.** It
cannot keep a retired word in its own name. 17 work records carry it.

**The risk ledger does NOT move — and that was tested rather than assumed.** The
session's instinct was to lift it to viability on the reasoning that *is this
worth doing* and *what could kill it* are the same question. An independent
top-tier call was made to refute that, and it did:

- **Stage-Gate** (fetched from `stage-gate.com`, the model owner's own text):
  Stage 1 Scoping is deliberately cheap desk research; the named **risk
  assessment sits in Stage 2, Build the Business Case** — the same stage that
  produces product definition.
- **PRINCE2** (the non-software test, secondary via `prince2.wiki`): the outline
  business case carries a *summary* of major risks; the **Risk Register** — the
  qualified artifact — is created at initiation, alongside the detailed business
  case and the scope.
- **ISO/IEC/IEEE 29148** (primary, 2011 edition): requirements specs carry **no
  risk section at all**. Risk is a per-requirement attribute and part of the
  "Feasible" well-formedness test — qualification interleaved with defining what
  you want.
- **ISO/IEC/IEEE 24748** was reached only as far as its official preview: stage
  names and order are primary, stage *bodies* are paywalled and taken secondary
  from SEBoK. Named so the tier is not overstated.

**The argument that killed the instinct:** you cannot qualify the risks of an
undefined thing. Rows are relative to a commitment, so qualifying before
scope-lock means every scope change invalidates them. It also inverts gate
economics — a fully evidenced ledger demanded to pass *is this worth
investigating* front-loads the exact cost the gate exists to defer.

**So risk is checked twice, at two depths, in ONE section.** Viability requires
that killer risks are **named** — no sizing, no evidence, cheap. Scope requires
**every row qualified**. The producer's ruling on adding the viability tier:
*"yes of course."*

This is the second measured instance of Kerd's viability gate being thinner than
its counterparts: it checks that a `## Value` section **exists** and nothing
about its content, while every standard consulted sees named risks at its first
go/no-go.

`scope` carries the strongest cross-work evidence of the three: *scope of work*
is standard in construction, consulting and law, not only software. The artifact
name is open — `## Delivery scope` or `## Release scope`, settled at design.

**`handoff` names the act, not the artifact** — his sharpening of what the rung
does: *"that rung is really 'make the work build-ready,' not 'the spec artifact
exists.'"* It is the most cross-work of the candidates considered (`plan`,
`brief`, `spec`): handoff is standard in construction, manufacturing, healthcare
and journalism, so it reads unaided for a repair or a business plan.

`loop` stays. `learn` is an open alternative; Stage-Gate's *post-launch review*
is refused here because Drive is not only launch-shaped.

### The qualification rule — DECIDED 2026-08-23

`handoff` has a real incumbent: switch's **session handoff**, 15 uses in
`skills/switch/SKILL.md` alone and 19 across `skills/`. That was raised as an
objection and overruled, and the reasoning is the decision:

> The incumbent use is real, but it is manageable because it is the same verb at
> two altitudes, not two unrelated meanings. Switch owns session handoff. Drive
> owns work handoff. That actually reinforces the item-vs-session distinction if
> we qualify it consistently.

**So: bare `handoff` is no longer allowed in living docs where ambiguity
matters.** Say **session handoff** for switch, **work handoff** for the Drive
rung. The rung slug stays `handoff`.

This is the same shape as the R3 quoting convention — a naming rule that binds
prose rather than machinery, and the two-altitude split it enforces is the one
`funnel-driver/span-vs-slice.html` was drawn to establish.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| A half-done rename turns the board red and blocks every push | yes | CI refuses on `progress.py stale` and on front-matter validation; nobody can ship anything until it is finished | high if done piecemeal | the ladder is pinned in exactly two places — `kit.py:34` `RUNGS` and `kit.py:91` `GATE_RECORD_RE` — but `stage:` values live in 20 work records and the board derives from disk | countermeasure - permanent | the rename lands as one atomic change with the sweep done at design time, per the standing cross-cutting rule; the board is re-rendered in the same commit | |
| `handoff` collides with switch's session handoff, inside our own vocabulary | no | a newcomer reading bare `handoff` cannot tell whether a session or a work item is being handed over — the exact confusion this item exists to remove, and an inside collision cannot be disambiguated by context the way an outside one can | certain if left bare | 15 uses in `skills/switch/SKILL.md`, 19 across `skills/`, 17 across `docs/design/` and the gates README | countermeasure - permanent | the qualification rule above: bare `handoff` banned in living docs where ambiguity matters, **session handoff** for switch and **work handoff** for the rung; slice 1 carries the sweep across every bare incumbent use | |
| `spec` was rejected as the contract replacement because it collides on filenames | no | `docs/gates/<date>-<slug>-spec.md` and `docs/plans/<date>-<slug>-spec.md` would differ only by folder | n/a — not adopted | `kit.py:682` and `kit.py:711` glob `docs/plans/*-<slug>-spec.md`; `GATE_RECORD_RE` would have matched the same basename shape | accepted | recorded so the option is not re-proposed; `handoff` has no filename collision | a future rung name lands under `docs/gates/` sharing a basename with a `docs/plans/` artifact |
| The grounding section cannot cite an external source | no | Law 4 obliges learning from standards, and the section that records what was read refuses every URL — so the reading is recorded in prose the machine cannot check | certain | `gate.py audit` refused both URLs in this file's own grounding on first write, 2026-08-23 | accepted | external sources cited inline in the findings instead; the reference is readable but unchecked | a second item needs external grounding — at which point the format owes a slot |
| Renaming `goal` breaks 7 immutable gate records | no | history becomes unreadable to the parser, or gets rewritten — and gate records are immutable by contract | certain unless handled | `ls docs/gates/` — 17 records, 10 `design` and 7 `goal`; no other rung has ever been recorded | countermeasure - permanent | the parser keeps the retired names in its legal set forever as read-only aliases; no file on disk is renamed, ever | |
| `RUNGS` goes from eight entries to seven, and the router walks it | yes | `route()` returns the deepest rung whose cumulative inputs exist; collapsing two rungs into one container changes what every slug reports, including the 20 already on the board | certain | `kit.py:34` defines `RUNGS` as a flat list and `route()` iterates it; the board derives every position from that call | countermeasure - permanent | the two folded checks keep their exact test and only their label changes — old `build`'s spec+Pieces+Verify becomes the loop's entry, old `goal`'s zero-unchecked becomes the loop's exit; no test is added, removed or reordered, so every slug's reported position is unchanged in substance | |
| ~~Nothing marks an item done once `acceptance` is the last position~~ **ANSWERED 2026-08-25: the terminal state is READY TO RELEASE, not done** — the producer's ruling, *"not done, but 'ready to release'"*, because the work loops after release so `done` names nothing. The literal `stage:` value stays open for design. | no | today the last rung is `loop`, so a finished item reports `enters at: loop` forever; with `acceptance` last the same ambiguity moves rather than resolving | certain | `route()` returns the deepest rung whose inputs exist, and there is no rung beyond the last one to enter | accepted unknown | none yet — it is pre-existing rather than introduced here, but the restructure is the moment to settle it | the design rung |
| This is vocabulary churn dressed as work | no | a sitting spent on words while `funnel-driver` sits at contract for a fourth day | medium | the item was raised precisely to block that spec | countermeasure - permanent | the cross-work rule makes it functional rather than cosmetic — Drive's stated premise is non-software work, and three rung names fail for non-software items *today*, before Drive ships and bakes them into every consuming repo | |

## Why now rather than after Drive ships

The rung names travel into every consuming project's front matter and gate
records the moment Drive exists. Renaming them afterwards is a migration in
someone else's repo, which this project cannot perform and would not be forgiven
for.

## Release slice

Rigor level: mvp

**Slice 1 — the restructure and the renames, atomic.** `RUNGS` goes eight → seven:
`slice → scope`, `contract → handoff`, `build`+`goal` fold into `loop` as one
route position, and old `loop`'s human key becomes `acceptance`. Retired names
stay as read-only parser aliases so no gate record is ever rewritten. Includes the cross-cutting sweep, the front-matter
`stage:` migration across all work records, the qualification sweep over every
bare `handoff` in living docs, `tools/gates/README.md` as the canonical home, and
a board re-render in the same commit.

**Deliberately excluded from slice 1, each with its reason:**

- **The `stage:` values for `handoff` and `acceptance`.** `scoped` is settled;
  the other two are not, and inventing them here would put design-rung decisions
  in a frame.
- **`loop → learn`.** No evidence either way yet. Changing a name that passes on
  a hunch is the failure this item exists to prevent.
- **The `docs/product` → `docs/work` migration.** Different item, already
  measured at ~180 references in `funnel-driver` slice 3. These two want to ride
  together and must not: two cross-cutting renames in one commit make the
  collateral check unaffordable.
- **Anything in `skills/drive/`.** It does not exist yet.

## Deliberately not in this item

- Renaming the four rungs that pass. `frame`, `viability`, `design` and `build`
  are current and cross-work; touching them is churn.
- Adopting Stage-Gate's stage names. Checked, and refused: launch-shaped and
  corporate, failing the newcomer for the opposite reason.
- The work-type vocabulary itself. Settled in `docs/design/funnel-driver.md`.
