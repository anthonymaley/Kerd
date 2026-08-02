# Product layer, design rung, and the diagram grammar — proposal

**Date:** 2026-08-02
**Status:** proposal — nothing here is approved, nothing is built
**Session:** 2026-08-01/02, Kerd (v0.65.0 → v0.68.0 shipped separately during it)

---

## What this is about

Kerd is well served from the **contract** rung down. The layer Tony actually works in
— what the product *does for the people using it* — has no artifact anywhere, so it
gets reconstructed by hand, in prose, once per session, and only when he explicitly
asks for it.

v0.68 ("say it in the user's terms") was a patch on the **message**. This proposal is
about the **memory**: a durable product-level artifact, a design rung above the
contract, and the visual grammar Tony actually reviews in.

---

## What we measured

Not opinions — counts taken this session across `3of3`, `dinner-tonight`, `Bree`,
`leru`, `krutho-*` and `Kerd`.

| Finding | Evidence | Confidence |
|---|---|---|
| superpowers **plans** are inert | 10,177 lines across 17 docs in 3of3; **0 of 472 checkboxes ticked** | measured |
| conductor already replaced `writing-plans` | superpowers artifacts: 20 Jun, 17 Jul, **0 Aug**. Kerd `docs/plans`: 0 Jun, 7 Jul, 3 Aug. Conductor's spec flow shipped 7 Jul; last superpowers artifact 8 Jul | measured |
| superpowers **specs** are alive | 19 docs, ~110 line median, referenced from 5+ session logs, survived every trim pass | measured |
| `capturerequirements` has never been used | **zero** artifacts in `docs/requirements/` in any repo, ever | measured |
| design docs are never retrieved | the 6 Jul `tv-seasons-episodes-design.md` held the exact answer to a 1 Aug question; the session read a stale code comment instead and got it wrong twice | measured |
| **nothing in the system can refuse** | **0 CI workflows, 0 pre-commit hooks — every repo** | measured |
| brainstorming captures the plan phase | `brainstorming/SKILL.md:66` — "The terminal state is invoking writing-plans… the ONLY skill you invoke after brainstorming is writing-plans." It never returns to conductor | measured |
| prose is the wrong review modality for Tony | six turns of prose produced refinements; one diagram produced a structural realisation about his own working style | observed, n=1 |

### Collisions between superpowers and Kerd, specifically

- **Multiple choice.** `capturerequirements` — *"Do not enumerate multiple-choice menus."*
  `brainstorming:141` — *"Multiple choice preferred."* Flat contradiction, and Tony's
  recorded call (CONTEXT.md, 2026-07-06) sides with Kerd.
- **Uniform process.** `brainstorming:18` — *"Every project goes through this process.
  A todo list, a single-function utility, a config change — all of them."* Directly
  opposed to conductor's right-sizing thesis.
- **Worktrees.** `writing-plans:14` assumes a dedicated worktree created by
  brainstorming. Kerd never creates one; switch owns git.
- **Artifact scatter.** Three conventions live simultaneously: `docs/plans/`,
  `docs/superpowers/{specs,plans}/`, `docs/requirements/`. `tend` and `trim` know
  about one of them.

---

## The altitude model

Four altitudes between an intention and a shipped change. Three are occupied.

| Rung | Answers | Occupied by | State |
|---|---|---|---|
| **Product** | what it does for the people using it | — | **empty** |
| **Design** | approaches, architecture, components, data flow | superpowers specs (~110 ln) | good, but tech-leaning and never retrieved |
| **Contract** | exact files, signatures, the why, a verify command | conductor spec file (~200 ln) | won this rung in July |
| **Implementation** | the steps themselves | superpowers plans (~510 ln) | superseded, inert |

Conductor's orient reads `CONTEXT.md`, `TODO.md` and the newest session log. All three
describe **the work**. None describes **the product**.

---

## The diagram grammar

Taken from Tony's DDIL identity deck (Excalidraw, 266 elements, 5 numbered movements).
This is the form he agrees designs in, and it is not a flowchart.

**Structure:** an argument in numbered movements — problem → naive fix → the dilemma
(with variants) → dissolution → the concrete fork.

**Five devices:**

1. **A constant verdict line per option, on two fixed axes.**
   *Presence ensured — Governance forks* / *Presence conditional — Governance kept* /
   *Presence ensured — Governance corrupted* / *Presence ensured — Governance kept*.
   Every option scored on the same pair; the winner is the only row where both halves
   are good. A comparison matrix carried in a caption.
2. **Colour marks cost, and nothing else.** 23 of 266 elements are red, every one on
   the thing that hurts — `identity data (local, ×N)`, `governance (local, ×N)`,
   `source???`. The pain is visible before it is legible.
3. **Named bets, discharged by name.** *"Timing bet: replica updated before the person
   arrives. Scope bet: the correct subset, guessed in advance."* Movement 4 then pays
   them off explicitly: *"no scope bet, no timing bet, no racing the link."*
4. **Containment, not arrows.** Zone → site → component as nested boxes. The nesting
   *is* the boundary. This is the "logical becoming physical" hybrid.
5. **Altitude shifts between movements.** Movements 1–4 are conceptual (IAM, identity
   data, governance as abstractions). Movement 5 drops to physical (`Bridge (verifier /
   OIDC OP)`, `oid4vp`, `redeem code -> tokens`, `holder priv keys`). Same document.

**Mermaid cannot express this.** It draws sequence and branching. It cannot do
containment-as-boundary, a semantic colour overlay, verdict captions, or an altitude
shift. The altitude-bands block in this session's HTML sketch *did* express it — nested
containers, one semantic colour for the gap, a verdict line per row.

---

## Proposals

Each stated as: what it gives, **what it costs**, and the bet it rides on.

### P1 — A living product spec

One document per product describing what it does for the people using it. Overwritten
in place like `CONTEXT.md`, never dated, never a snapshot.

- **Gives:** the translation stops being rebuilt per session; a durable answer to
  "what is this and what can someone do with it".
- **Costs:** one more document to keep true. If it drifts it becomes the stale comment
  that cost two rounds on 1 Aug.
- **The bet:** that it gets *read*. An artifact nobody retrieves is worse than none —
  it costs the writing and pays nothing. **This bet is currently losing** for design
  docs, which is the strongest argument against building it naively.

### P2 — Put it in a read set

Conductor's orient reads the product spec when work touches a feature area. Without
this, P1 is a second unread document.

- **Gives:** discharges P1's bet. This is the load-bearing half.
- **Costs:** orient gets more expensive; risks context bloat on large products.
- **The bet:** that relevance can be judged cheaply — that conductor can tell when work
  touches an area without reading everything.

### P3 — The design rung, in the diagram grammar

A design step between requirements and contract, producing options on constant axes
with costs marked and bets named — not a flowchart of the plan.

- **Gives:** fills the rung conductor reached outside for; produces the form Tony
  actually reviews in.
- **Costs:** a real artifact per non-trivial change. Ceremony if untriggered.
- **The bet:** that the trigger holds — *structure worth seeing* (more than one
  component, a flow, a before/after), never a palette change or a copy fix.

### P4 — Diagram at the gate, spec behind it

The approval gate leads with the diagram; the spec detail sits behind it. Diagram in
the same file as the spec — never a separate artifact.

- **Gives:** approval in the modality Tony reads; one file so both rot together.
- **Costs:** ~~none~~ — **approving a diagram is not approving the detail.** A swallowed
  deletion range does not appear in a flowchart.
- **The bet:** that the diagram leads without replacing. v0.66's rule stands — spec
  detail is the safety mechanism.

### P5 — Read Tony's diagrams as input

Kerd parses an `.excalidraw` file and treats it as the source of truth for a design.

- **Gives:** he draws, Kerd builds from it — the reverse direction, and the one that
  matches "how I agree design".
- **Costs:** a parser, and a convention for where drawings live.
- **The bet:** that his drawings carry enough to build from without a prose round trip.
  **Untested.**

### P6 — Spec self-review

Stolen from `brainstorming:116` — placeholder scan, internal consistency, scope check,
ambiguity check, fix inline. ~15 lines, not a clone.

- **Gives:** catches vague slices before the gate, where v0.66 says the failure lives.
- **Costs:** negligible.
- **The bet:** none material. This is the cheapest item here.

### P7 — Fresh-context reviewer

A subagent given only the spec and the diff, asked what is missing — never the
conductor, which has been in the loop and is anchored.

- **Gives:** a genuinely unanchored second read; composes with the v0.66 collateral check.
- **Costs:** one subagent per task.
- **The bet:** that anchoring is the real failure mode. Supported by 1 Aug's "never
  contacts your server" — a confident wrong claim that survived its own author's first
  correction and needed an outside push.

### P8 — An enforcement layer

CI that refuses. Currently **zero** across every repo.

- **Gives:** the first mechanism in the entire system that can say no. Everything else
  — every gate, every rule shipped today — is prompt-layer compliance.
- **Costs:** real setup, per repo, outside Kerd.
- **The bet:** none. This is the only item here that changes what is *possible* rather
  than what is *likely*. **Probably the highest-value item on this list, and the one
  least related to Kerd.**

### P9 — Unwire the brainstorming handoff

Conductor asserts that its plan phase is the shaping step and does not hand off;
a CLAUDE.md line makes it stick.

- **Gives:** stops the plan phase being captured and routed to `writing-plans`.
- **Costs:** superpowers' design step stops arriving automatically — P3 must exist first
  or the rung goes empty again.
- **The bet:** that a CLAUDE.md line outranks a session-start `EXTREMELY_IMPORTANT`
  block. Superpowers concedes this itself: *"If CLAUDE.md says 'don't use TDD' and a
  skill says 'always use TDD,' follow the user's instructions."*

### P10 — Test bias by layer, and contract tests

Business logic heavy; UI at behaviour level not component level; infrastructure
smoke-only. Contract tests where a client and a server meet.

- **Gives:** answers the "80 mediocre tests" failure directly.
- **Costs:** none structural — it is a bias, not a mechanism.
- **The bet:** that 3of3's shape (Swift app ↔ Python pipeline ↔ Jellyfin) is where this
  pays. It already has a `movie-catalog-client-contract.md` spec with nothing enforcing it.

---

## Rejected, with reasons

- **OpenSpec** — would be a fourth planning convention on a scatter problem we measured.
  Its delta model is genuinely good; the cost is a second artifact to maintain.
- **GitHub Spec Kit** — the Constitution idea is sound and `CLAUDE.md` already is one.
  The rest duplicates conductor.
- **BMAD** — replacing one opinionated system with a heavier one.
- **Cloning superpowers** — a rival brainstorming skill faces the identical
  injection-order problem. The CLAUDE.md line is what makes either approach work, and
  if it exists the clone is unnecessary.
- **Removing superpowers wholesale** — its two halves had opposite fates. Removing the
  plugin discards the design step that survived along with the plan step that died.
- **A third executor tag naming *why* a step is kept** — tags encode actions; a tag
  encoding a reason decays into a vibe marker. Reasons go in the step body.
- **Splitting orchestration from transcription (a "copyist" tier)** — spec detail is
  where judgment is encoded; delegating it attacks the safety mechanism to save the
  cheapest tokens.

---

## Open questions

1. **Current truth, or intent?** A product spec describing what the product does *today*
   stays honest and can be diffed against reality. One describing what it is *meant* to
   do doubles as a roadmap and rots when a build slips. OpenSpec splits the difference —
   current spec plus change deltas — at the cost of a second artifact.
2. **Home.** Root-level beside `CONTEXT.md` and `TODO.md`, or in the vault where the
   human-first, no-prior-knowledge audience already lives?
3. **Owner.** Repurpose `capturerequirements` — kill a dead skill and fill a real gap in
   one move — or make it a file convention conductor reads and writes, with no skill?
4. **Diagram format.** `.excalidraw` is editable by Tony and already his tool; generated
   HTML is richer but read-only to him. Agreeing a design means moving a box, which
   argues for the former. **Untested: whether Claude-generated `.excalidraw` opens and
   edits cleanly.**

---

## Sequencing

Nothing here is built. In dependency order rather than value order:

1. **P8 (CI)** — independent of everything else, and the only item that changes what is
   possible. Highest value, least Kerd.
2. **P6 (spec self-review)** — cheapest, no bet, ships on its own.
3. **Test P5's format question** — generate one `.excalidraw`, confirm it opens. One
   command's worth of evidence gates two proposals.
4. **P1 + P2 together** — the product spec and its read path. Building P1 without P2 is
   building a second unread document; the measured retrieval failure says this is the
   likely outcome, not the pessimistic one.
5. **P3 + P4** — design rung and the gate that presents it.
6. **P9** — only after P3 exists, or the design rung goes empty.

**Everything shipped this session (v0.66–v0.68) is written but unrun.** Only the
orchestrator write-to-disk mechanic has been tested — one trial, 1,601 words to disk
against ~180 returned.
