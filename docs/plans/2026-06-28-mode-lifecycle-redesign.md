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

## Open items (next)

1. **Detail the 5 dial stages** — for each: goal, the right-sizing rules, exit
   condition, what it produces, how it advises the next stage / handles jump-back.
2. **Renames** — `dian` → a role-clear name (coach/conductor). `dial` working
   name. Pick once roles are locked; don't bikeshed mid-design. The naming bar:
   the name should say what it does (even Tony gets confused by "dian").
3. **dial = one skill vs five stage-modes** — leaning one `dial` skill holding all
   five stages + graduation logic (Tony's instinct), not five separate mode files.
4. **Skills-split decision** — does Kerd stay one plugin (skills + dial + coach)
   or split. Reopened; lean "stay one."
5. **Prune the current mode set** — legal/sales/writing/research/strategy/maintain
   are tool-use, not modes. Decide what happens to those mode files.

## Method note

This design was produced in a fast partner-mode whiteboard, dogfooding the working
style: short exchanges, one decision at a time, no big solo dumps. Build it the
same way — detail stages incrementally, eyeball-gate each, ship in slices.
