---
name: sherpa
description: "Use when the user has an idea to walk from spark to launch and wants a guide for the whole journey — or says 'sherpa', 'walk this idea', 'new idea', 'take this to launch', 'what stage am I at', 'explore / validate / plan / build / launch this'. The lifecycle conductor (the PM): walks one idea through its stages across many sessions, sets the right rigor per stage, advises when to graduate, jumps back on failure. Spans days and many conductor-sessions. NOT a single-session tool — that's conductor (the session skill)."
---

# Sherpa (Idea→Launch Lifecycle)

A sherpa guides one idea up the mountain: knows the route, paces you stage to
stage, carries the accumulated knowledge between camps, and calls the turn-back
when the weather's wrong. Sherpa is the **lifecycle conductor** — the PM that owns
the *what/when* of an idea's journey from spark to launch, across many sessions.

It nests under the other two altitudes:

- **switch** — the boundary (git, session in/out).
- **conductor** — the *session* conductor: keeps one session in tempo. (Runs every
  session you opt into; sherpa rides on top of it.)
- **sherpa** — the *lifecycle* conductor: walks the idea across all of those
  sessions, stage by stage.

A one-off (fix a bug) needs no sherpa — just the conductor. A new idea uses the
sherpa, which conducts many conductor-sessions over time.

## The five stages

| # | Stage | What it's for | Rigor |
|---|-------|---------------|-------|
| 1 | **Explore** | "What could this be? Could it even work?" Move fast, mins not hours. | lowest |
| 2 | **Validate** | Worth it? Does it exist? Will it work? | rising |
| 3 | **Plan** | Just enough plan to build with confidence, once it's earned. | scalable |
| 4 | **Build** | Implement the validated, planned idea until requirements are met. | scaled |
| 5 | **Launch** | Get ready across every dimension, then ship. | highest |

**Rigor rises; ceremony and noise stay low.** As stages mature you want more
*depth* (real validation, real planning) — but the **decision style stays JIT the
whole way**: drill one question, decide, eyeball-gate, fail fast. The dial is
rigor, not ceremony.

> Full stage specs (goal / rules / tripwire / exit / handoff) live in the design
> doc `docs/plans/2026-06-28-mode-lifecycle-redesign.md`. They get trained into
> the per-stage sections below one slice at a time (Phase 2). **The sections below
> are skeletons** — do not treat a stub as a finished stage.

## State model

Sherpa spans many sessions, so its state cannot live in `.active-modes` (that file
is session-ephemeral — the conductor clears its line on close-out). Sherpa's
durable state lives in a committed repo file; `.active-modes` only carries a
lightweight pointer for the current session.

**`kivna/sherpa.md`** — the expedition log. One per repo (one repo = one idea).
Committed, travels in git like `TODO.md`. Holds:

```markdown
# Sherpa — <idea name>

**Stage:** <1–5> <stage name>
**Started:** YYYY-MM-DD

## The idea
<one or two lines — what this is and why>

## Stage log
<for each completed stage: what it produced — the handoff that fed the next stage>

### Explore → (handoff)
### Validate → (handoff)
...
```

**`kivna/.active-modes`** — sherpa owns one line only, the current-session pointer:

```
sherpa: <stage>
```

Example: `sherpa: validate`. switch-in and hooks read this to report the active
lifecycle stage. Remove the line when the lifecycle is parked or complete. Never
touch another skill's line in this file.

## Mode markers

Sherpa is modal — announce the current stage so the user always knows where on the
mountain they are. On every stage transition, emit a marker on its own line at the
top of the response:

- `[sherpa: explore]` / `[sherpa: validate]` / `[sherpa: plan]` /
  `[sherpa: build]` / `[sherpa: launch]`
- `[sherpa: parked]` when stopping mid-climb (state saved to `kivna/sherpa.md`).

## Core moves

The sherpa skeleton — the navigation, not the per-stage internals.

### Start (at any stage)

You can enter the climb at any stage, not just Explore — a mature idea might start
at Plan. On start: create or read `kivna/sherpa.md`, set the stage, write the
`.active-modes` pointer, and announce the stage marker. If no `kivna/sherpa.md`
exists, seed it from the idea (name + the one-line "what/why").

### Advance (graduate to the next stage)

Each stage has an **exit test** (in the design doc, trained in Phase 2). When the
test passes, the stage's **Produces** becomes the next stage's input: write the
handoff into `kivna/sherpa.md`'s Stage log, bump the stage, move the pointer,
announce the new marker. Sherpa *advises* the graduation — it confirms the exit
test is met before turning the dial up.

### Jump back (on failure)

If a later stage reveals the idea doesn't hold (Validate kills it, Build proves it
infeasible), jump back to an earlier stage rather than forcing forward. Record why
in the Stage log, reset the stage + pointer. A jump back is information, not
failure.

### Park

Stop the climb cleanly: ensure `kivna/sherpa.md` reflects the current stage +
handoffs, set `[sherpa: parked]`, remove the `.active-modes` line. The expedition
log is what lets a cold session pick the climb back up.

---

## Stages — detail *(skeletons; Phase 2 fills these)*

Each stage section will encode its **goal / rules (right-sizing) / tripwire (drift
signal) / exit test / produces (handoff)** from the design doc. Until trained,
these are pointers, not protocol.

### Stage 1 — Explore *(= the spike mode)*

Marker: `[sherpa: explore]`.

- **Goal:** see what this could be / whether it could even work. Prove it *could*,
  don't build it. The knowledge is the asset, not the code.
- **Rigor:** lowest. Fast — mins not hours. Low ceremony, low noise.
- **Rules (right-sizing):** prove it could work, then stop. Throwaway code/design
  is expected and fine. No polishing, no test scaffolding, no feature breadth.
- **How to run it** (the spike Try-loop, compressed — full discipline in
  `modes/spike.md` until it folds in at Phase 3):
  1. **Empirical primitive first.** Name the cheap, fast, ground-truth probe for
     this domain and run it once across the whole surface *before* generating any
     try matrix — observation over guessing. Say so explicitly if none exists.
  2. **Batch the tries.** Generate the try matrix hard; default to N+1 variants
     over what was asked. The round-trip is the bottleneck.
  3. **Verify each variant in the same loop iteration** before tagging it ✓.
     "I added it" never equals "it works."
  4. **Provisional-loss survival gate.** A loss is not canonical until it survives
     one config change OR one user push-back. Each provisional entry lists "what
     would change my mind" + "what I haven't tried." Closure-bias is the default
     failure mode; this gate is the structural fix.
  5. **Strong-language / claim gate.** "verified / impossible / always / never /
     it works" needs ≥3 confirming observations or a cited source — else downgrade
     to "tested but not yet verified" / "from training data; may be wrong."
- **Tripwire (drift signal):** the moment you start over-engineering or adding lots
  of features, you've overstayed — that's the Build stage, not Explore. Stop and
  graduate.
- **Exit test:** you can *see it working* — conceptually, as a spike, or a rough
  MVP. Potential demonstrated.
- **Produces → Validate (write into `kivna/sherpa.md` Stage log):** **how it works
  / how we got it to work**, the **input vision + requirements** that drove it, and
  **optionally the code itself if it's good** — assessed and extractable, not
  assumed good. Throwaway parts are discarded.

### Stage 2 — Validate

Marker: `[sherpa: validate]`. Full design: `docs/plans/2026-06-29-validate-methods-toolkit.md`.

- **Goal:** decide whether the idea is worth building — viable *and* likely to
  succeed — before investing in a real build.
- **Rigor:** rising. Real research/evidence (more depth than Explore's throwaway
  spike), but the decision style stays JIT.
- **Principle — risk-driven, not menu-driven.** Don't run a fixed battery of
  analyses. Find the idea's **killer assumption** (the thing that, if false, kills
  it) and run the **cheapest test of that one thing**. The method falls *out of*
  the risk — you never pick a method first.
- **The five risk categories** (each names a distinct failure mode; cheapest tests
  in parens):
  - **Demand** — nobody wants it (exists-check, talk to users, light market test).
  - **Feasibility** — it can't be built/made to work (technical spike = reuse
    Explore's, prototype, theory check).
  - **Economics** — the numbers don't work (ROI / cost model).
  - **Differentiation** — it already exists / no reason it's us (exists-check,
    competitor scan).
  - **Access** — can't reach the users or not allowed (channel check, legal scan).
  - *(Floor, not a cage — name and test a killer that doesn't fit these five.)*
- **How to run it (the loop):**
  1. **Surface the risks** from the Explore handoff (vision + how-it-works +
     requirements); map each to a category. **Drill the user once:** "of these,
     which scares you most / is least certain?"
  2. **Rank** by `most-likely-to-kill × least-certain`. The top is the killer.
  3. **Test the top risk, cheapest method first.** Run it JIT — enough signal to
     decide, no more. (exists-check is often the cheapest first move — it can kill
     Demand and Differentiation at once.)
  4. **Survives** → next-riskiest, re-check the exit bar. **Fails** → kill-or-pivot:
     **jump back to Explore** to reshape, or kill. A failed validation is the stage
     doing its job.
- **Tripwire (drift signal):** validating a risk that's cheaper to just *build
  past* is over-cooking — the waterfall drift. If the next test costs more than
  building would teach you, stop and graduate.
- **Exit test (all three):** the killer assumption(s) tested and **survived**; a
  **clear pathway to build**; the **remaining risks acceptable to carry** into
  Build (known, non-fatal, cheaper to resolve by building than by more validating).
  You clear the *fatal* risks, not every risk.
- **Produces → Plan (write into `kivna/sherpa.md` Stage log):** the validated
  pathway, the evidence (which risks tested, by which method, what signal — with
  claim-discipline tags), and the named **carried risks**.

### Stage 3 — Plan

Marker: `[sherpa: plan]`.

- **Goal:** get *just enough* plan to build with confidence — without stalling
  progress. Not anti-planning: detailed plans are fine **where they earn it**, just
  never at the expense of momentum, especially early.
- **Rigor:** scalable. Light early; deepen later or for high-stakes builds. Sherpa
  sets how much — turn the dial up for a committed build, keep it thin for an MVP.
- **How to run it:** reuse the **conductor's plan phase** (the `/kerd:conductor`
  skill): decompose into scoped tasks with acceptance criteria and concrete,
  verifiable steps (file paths, expected output), pushing back on vague items. Sherpa adds the stage-level **"enough plan" exit test** on
  top — the plan is done the moment it answers all five, and no sooner:
  1. **What** exactly we need to do
  2. **When** we need to do it
  3. **How we know it's done** to the level we need (acceptance)
  4. **What comes next**
  5. **Why** we're doing this now
- **Tripwire (drift signal):** planning *past* those five (early), or planning that
  stalls progress, is over-planning — the waterfall drift sherpa exists to prevent.
  Stop and graduate to Build.
- **Exit test:** the five questions are answered to the depth this build needs.
- **Produces → Build (write into `kivna/sherpa.md` Stage log):** the scoped,
  sequenced task set with done-criteria and the why-now.

### Stage 4 — Build *(= the jit mode)*

Marker: `[sherpa: build]`.

- **Goal:** implement the validated, planned idea until its requirements are met.
- **Rigor:** scaled — JIT-iterative for an MVP, deeper for a bigger committed
  build. The decision style stays JIT throughout: smallest valuable slice → show →
  eyeball-gate → revise.
- **How to run it** (the jit loop — full mode in `modes/jit.md` until it folds in at
  Phase 3):
  1. **Lock requirements, defer the rest.** Use `/kerd:capturerequirements` to pin
     the MVP must-haves (the Plan stage's handoff seeds this). Then name the
     **first slice** — the smallest valuable thing to build and show.
  2. **Thin spec.** Just enough for the first slice, not exhaustive.
  3. **Build → show → gate.** Build the slice (TDD where it fits), show it, the
     user calls it: go or revise. Wrong slice? update requirements + spec and
     reslice. Right? next slice. Verify before claiming done.
- **Tripwire (drift signal):** building *past* the requirements (gold-plating) or
  adding features not required — "build what you need, not what you think you
  need." Stop and graduate to Launch.
- **Exit test:** requirements from **all areas** are met — not just "code runs,"
  but the holistic intent captured upstream (architecture, business, vision,
  design). The Validate/Plan handoffs define "all areas" for this idea.
- **Produces → Launch (write into `kivna/sherpa.md` Stage log):** the built thing
  meeting all-area requirements.

### Stage 5 — Launch

Marker: `[sherpa: launch]`.

- **Goal:** get everything ready to go live across *all* launch dimensions, then
  ship. Build made the thing; Launch puts it in the world.
- **Rigor:** highest — it's public and hard to walk back. This is the one stage
  where thoroughness beats speed; a missed dimension is visible to everyone.
- **How to run it — adaptive readiness checklist.** There is no fixed list: build
  the checklist to fit *this* thing (a TV app and a SaaS feature need different
  ones). Walk the candidate dimensions, keep the ones that apply, and confirm each
  is ready before shipping:
  - **Distribution** — app store / package registry / deploy target / release
    artifact.
  - **Marketing** — landing page, launch copy, announcement, positioning.
  - **Social** — accounts that need to exist or post (Instagram, X, etc.).
  - **People/staff** — who needs to be briefed, on-call, or trained.
  - **Support** — docs, help channels, feedback path, known-issues list.
  - **Comms** — who gets told, when, in what order (users, stakeholders, press).
  (This adaptive shape mirrors Validate — the two "wide" stages that reach into
  business/marketing/ops, vs. the tighter Plan/Build.)
- **Tripwire (drift signal):** shipping with a required dimension unconfirmed
  ("we'll do the support docs after launch") — the opposite drift from the early
  stages: here, under-covering is the risk, not over-cooking.
- **Exit test:** "do we have everything done to launch?" — readiness confirmed
  across every required dimension, **and it's shipped**. The lifecycle is
  **complete** when the idea is live in the world.
- **Produces:** the launched product + the launch-readiness record (what was
  covered, written into `kivna/sherpa.md` as the final Stage log entry).
