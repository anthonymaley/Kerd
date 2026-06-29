# Mode + Lifecycle Redesign — 2026-06-28

Reopens and largely supersedes `2026-05-04-skill-architecture-review.md`. That doc
designed modes as orchestrators of *external* skills (GSD, Superpowers). This one
starts from a different premise.

## Why we reopened it

The 2026-05-04 design assumed Kerd would be a thin router over other people's
skills — "I won't be the expert; link and orchestrate GSD, Superpowers, more."
In practice:

- **GSD** — removed entirely (v0.43.0). Not the shape Tony wants.
- **Superpowers** — feels like waterfall / over-planning. The frustration that
  produced `jit`: "I just want the minimum to test if an idea has legs" — mins,
  not hours; signal, not noise.

New premise: **Kerd owns modes shaped to how Tony actually works**, invokable when
needed — not a router over tools he dislikes.

## The core distinction (load-bearing)

- **Skills are tools.** dian, switch, kivna, slainte, skriv, tend, lorg, trim,
  focus, capturerequirements, interrogate. Everyday, always available. You reach
  for a tool anytime; no mode required to use one.
- **A mode is a right-sizing contract.** Its only job is to stop you over-cooking
  (plans you don't need) or under-cooking (skipping what the task needs). Not "a
  list of skills to call" — *the rules that keep process the right size for a shape
  of work.*

**The mode test:** does this shape of work have a characteristic way I get the
process *wrong* that a ruleset would prevent? If yes → mode. If it's just "use a
tool" (run the health loop, write in voice, review a contract) → it's a skill, not
a mode. This kills most of the old "business modes" (legal, sales, writing,
maintain) as modes — they're tool-use.

## The architecture — three altitudes

They nest; they don't compete.

1. **switch** — the *boundary*. Session in/out, git, the substrate. Offers the
   coach on switch-in (offered, **not** auto-started — a 2-min task shouldn't be
   forced into ceremony).
2. **coach** (rename of `dian`) — the *session* conductor. Frames one session,
   keeps it disciplined and on-point, closes out. Domain-agnostic (build, writing,
   strategy — not dev-only). Runs every session you opt it into.
3. **dial** (new skill — the PM) — the *lifecycle* conductor. Walks an idea
   through its stages across many sessions, sets the right rigor per stage, advises
   when to graduate. Spans days and many coach-sessions.

Analogy: **dial = PM/manager** (owns the *what/when* of the idea's journey);
**coach = agile coach** (owns the *how-well* of each session). switch is the
boundary under both.

```
switch in → session opens → coach frames + keeps it disciplined
   └─ optionally: /dial → PM walks the idea through stages 1–5 across sessions
        coach keeps every one of those sessions on point
```

A one-off (fix a bug) uses the coach, no dial. A new idea uses the dial, which
conducts many coach-sessions over time.

## The dial — idea→realization lifecycle

A **graduating, self-learning, connected flow.** Start at any stage; jump back on
failure. The dial hand-holds from a given stage and advises the next when ready.

| # | Stage | What it's for | Rigor |
|---|-------|---------------|-------|
| 1 | **Explore** | "What could this be? How might it look/work?" Move fast, mins not hours. | lowest |
| 2 | **Validate** | Worth it? Does it exist? Will it work? Feasibility / research / pitch. | rising |
| 3 | **Plan** | Only once it's earned planning. | |
| 4 | **Build** | Implement, iteratively. | |
| 5 | **Launch** | Test, ship. | highest |

**The dial is rigor, not ceremony.** As stages mature you want *more
information/depth* (validation needs real research; planning needs real thought) —
but the **decision style stays JIT the whole way**: drill one question, decide,
eyeball-gate, low-noise, fail-fast. Rigor goes up; ceremony and noise stay down.

This resolves spike vs jit:
- **spike = the Explore stage** (throw ideas, learn fast, no plan).
- **JIT is not a stage — it's the philosophy running through all of them**
  (minimum viable, prove before you invest, fail fast). The Build stage is JIT
  applied to implementation; the universal *decision style* is the partner-mode
  / `focus` style we wired today.

## Stage details

### Stage 1 — Explore  *(= spike)*

- **Goal:** see what this could be / whether it could work. Not "build it" — prove
  it *could*.
- **Rigor:** lowest. Fast, mins not hours, low ceremony, low noise.
- **Rules (right-sizing):** prove it could work, then stop. Throwaway code/design
  is expected and fine. No polishing, no test scaffolding, no feature breadth.
- **Tripwire (drift signal):** the moment you start over-engineering or adding lots
  of features, you've overstayed — that's dev/build mode, not Explore. Stop and
  graduate.
- **Exit when:** you can *see it working* — conceptually, as a spike, or a rough
  MVP. Potential demonstrated.
- **Produces (handoff to Validate):** the *knowledge* is the asset, not the code.
  Carry forward: **how it works / how we got it to work**, the **input vision +
  requirements** that drove it, and **optionally the code itself if it's good** —
  assessed and extractable, not assumed good. The throwaway parts are discarded.

### Stage 2 — Validate

- **Goal:** decide whether the idea is worth building — viable *and* likely to
  succeed — before investing in a real build.
- **Rigor:** rising. Real research/analysis (more *depth* than Explore), but the
  decision style stays JIT (drill, decide, gate; no waterfall).
- **Method is adaptive** — pick the validation that fits the thing: market test,
  research, theory check, ROI, feasibility, "does it already exist," competitor
  scan, prototype test. There is no single fixed path; the dial helps choose.
- **Exit when:** there's a **viable pathway to build that will bring success** —
  confidence it's worth it *and* a clear route to build it.
- **Produces (handoff to Plan):** the validated pathway + the evidence behind it
  (why it's worth building, what success looks like, the chosen route).
- **⚠ Needs a deeper design session:** the validation *methods toolkit* (how to run
  each kind of validation, when to use which) is the hardest, least-specified part
  of the dial. Tony flagged it explicitly. Spec it on its own, later.

### Stage 3 — Plan

- **Goal:** get *just enough* plan to build with confidence — without stalling
  progress. Not anti-planning: detailed plans are fine **where they earn it**, just
  never at the expense of momentum, especially early.
- **Rigor:** scalable. Light early; can deepen later or for high-stakes builds. The
  dial sets how much.
- **"Enough plan" test (exit / produces):** the plan answers all five —
  1. **What** exactly we need to do
  2. **When** we need to do it
  3. **How we know it's done** to the level we need (acceptance)
  4. **What comes next**
  5. **Why** we're doing this now
- **Tripwire:** planning past those five (early) / planning that stalls progress =
  over-planning, the waterfall drift.
- **Produces (handoff to Build):** the scoped, sequenced task set with done-criteria
  and the why-now. (This is the coach's plan phase — dian already does this shape.)

### Stage 4 — Build  *(= jit)*

- **Goal:** implement the validated, planned idea until its requirements are met.
- **Rigor:** scaled — JIT-iterative for an MVP, deeper for bigger committed builds.
  The decision style stays JIT throughout: smallest valuable slice → show → eyeball-
  gate → revise.
- **Exit when:** requirements from **all areas** are met successfully —
  architecture, business, vision, design, etc. Not just "code runs"; the holistic
  intent captured upstream (Validate/Plan) is satisfied.
- **Tripwire:** building past the requirements (gold-plating) or adding features
  not required — "build what you need, not what you think you need."
- **Produces (handoff to Launch):** the built thing meeting all-area requirements.

### Stage 5 — Launch

- **Goal:** get everything ready to go live across *all* launch dimensions, then
  ship. Build made the thing; Launch puts it in the world.
- **Rigor:** highest — it's public and hard to walk back.
- **Coverage is adaptive** — the launch checklist fits the thing: marketing, app
  store / distribution, social accounts (Instagram etc.), staff/people, support,
  comms. A TV app and a SaaS feature need different lists. (Mirrors Validate's
  adaptive-method shape — these are the two "wide" stages that reach into
  business/marketing/ops, vs. the tighter Plan/Build.)
- **Exit when:** "do we have everything done to launch?" — readiness confirmed
  across every required area, and it's shipped. The lifecycle is **complete** when
  the idea is live in the world.
- **Produces:** the launched product + the launch-readiness record.

## Where today's shipped work fits

- `jit` mode → the Build stage (and the name of the whole philosophy).
- `capturerequirements` → a Validate/requirements tool used in the early stages.
- `focus` → the universal JIT decision-style, as a toggle.
- `spike` → the Explore stage.
- `interrogate` → heavyweight Validate, when the cost of being wrong is high.

## What this supersedes / reopens from 2026-05-04

- **Reopened:** "Kerd = modes only; skills move to a separate plugin." The
  rationale (orchestrating external skills) is gone. Likely Kerd keeps its skills.
  Decision pending.
- **Dead:** capability-first 16-mode model; matching ~35 capabilities to external
  skills; the whole GSD/Superpowers-orchestration framing.
- **Kept (still good):** skills are atomic and don't reference each other in flow
  terms; discipline gates fire universally; linear (no in-mode branching — branch
  = jump to a different stage); no mode composition; terse `.active-modes`.

## Implementation plan (TODOs)

Stage detailing (was item 1) is **done** — all 5 stages are spec'd above. What's
left, in dependency order. Build it in slices, eyeball-gate each (dogfood the dial
on itself).

### Phase 0 — Decisions to lock first (gate the build) — LOCKED 2026-06-29

- [x] **Renames.** `dian` → **`conductor`** (session conductor — keeps one session
  in tempo and coherent, present and in-the-moment; "coach" rejected as too sporty,
  "sensei" collides with the existing sensei plugin). `dial` → **`sherpa`** (the
  lifecycle PM — guides the long staged ascent across many sessions, knows the
  route, paces stage to stage, calls the turn-back). Two concrete guide-roles:
  sherpa for the long climb, conductor for the single run.
- [x] **dial = one skill.** One `sherpa` skill holds all 5 stages + graduation
  logic — not five separate mode files.
- [x] **Skills-split.** Kerd stays **one plugin** (skills + sherpa + conductor).
  No split.
- [x] **Mode-set prune.** spike/jit fold into `sherpa` (Explore / Build stages);
  the rest (legal/sales/writing/research/strategy/maintain, greenfield/quickfix/
  deepwork) retire as modes — they're skill-use, not right-sizing contracts.

### Phase 1 — Build the dial conductor

- [ ] Dial skill skeleton: stage tracking in `.active-modes` (terse), start-at-any-
  stage, advise-next-when-ready, jump-back-on-failure, the rising rigor dial, JIT
  decision-style throughout.
- [ ] Stage handoff mechanic: each stage's "Produces" becomes the next stage's input.

### Phase 2 — Train each stage into the dial

One slice per stage; encode its goal / rules / tripwire / exit / handoff (from the
Stage details above) into the dial, and wire the tools each stage uses.

- [ ] **Explore** — wire spike; enforce the over-engineering tripwire + the
  knowledge/vision/code handoff.
- [ ] **Validate** — **needs its own deeper design session first** (the adaptive
  methods toolkit: market test / ROI / feasibility / exists-check / theory — how
  and when to use each). Then wire (capturerequirements, interrogate for high-stakes).
- [ ] **Plan** — the "enough plan" 5-question test; reuse the coach's plan phase.
- [ ] **Build** — wire jit; exit = all-area requirements met.
- [ ] **Launch** — adaptive readiness checklist (marketing/store/social/staff/comms).

### Phase 3 — Rename + reconcile

- [ ] Rename `dian` → `conductor` and `dial` → `sherpa` across all skill files, docs, hooks, modes (full grep).
- [ ] Reconcile/retire the pruned mode files; update `mode` skill accordingly.

### Phase 4 — Docs, vault, release

- [ ] Update READMEs, plugin descriptions (both, byte-identical), skill triggers.
- [ ] Update vault MOC + Status (and fix the stale MOC version field).
- [ ] Release checklist + version bump per slice (each stage ship is MINOR).

## Method note

This design was produced in a fast partner-mode whiteboard, dogfooding the working
style: short exchanges, one decision at a time, no big solo dumps. Build it the
same way — detail stages incrementally, eyeball-gate each, ship in slices.
