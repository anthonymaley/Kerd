# The risk ledger — viability made measurable

Living design doc. Owner: **Test viability** (PRODUCT rung, function 2).
Source: post-walk decision 3 — interrogate modified, not replaced: its
exhaustive-interview engine stays, its output becomes this ledger.

## What it does

Turns named risks into QUALIFIED risks — sized, evidenced, and left in
exactly one state — because a named, unsized risk reads as managed, and
that is the failure this function exists to stop.

## The ledger

Risks as rows. Columns:

| Column | Rule |
|---|---|
| **Risk** | the concept, not the incident — one row per eliminated-or-carried idea |
| **Killer?** | marks THE killer assumption — tested first, always |
| **Impact** | in the units of the VALUE declared by *Frame the intent* — never a vibe word |
| **Likelihood** | recorded SEPARATELY, never multiplied — expected value is the wrong maths for a bet taken once |
| **Risk evidence** | a test OR an analysis — the same kind of evidence, differing in cost. Empty evidence = unqualified = cannot pass the gate |
| **Severity** | `fatal` or `non-fatal` — set by impact alone |
| **Treatment** | exactly one of the four below |
| **Countermeasure** | named, with a CONFIDENCE statement |
| **Treatment evidence** | what proves the treatment — `planned — <what will exist> · <expected location>` until the proof exists, a resolving citation once it does; required at fatal, optional at non-fatal |
| **Review trigger** | for accepted states: the date or condition that brings the risk back — closes the "accepted risks age" debt |

## Severity and Treatment

### Severity

| Severity | Meaning |
|---|---|
| **fatal** | impact ≥ the declared value, at ANY likelihood |
| **non-fatal** | impact below it |

### Treatment

| Treatment | Meaning |
|---|---|
| **Countermeasure — permanent** | closed by design |
| **Countermeasure — TEMPORARY** | carries its return condition; an unmarked temporary countermeasure is permanent by neglect |
| **Accepted** | by whom, when — and its review trigger |
| **Accepted unknown** | by whom, when, why the evidence was not gathered — and its review trigger |

## The rules

- **FATAL is set by impact alone** — likelihood sets the response, never
  the class.
- **A risk without a countermeasure is a BLOCKER** — the default flips so
  silence stops work instead of passing it.
- **The one unacceptable state**: high impact + high likelihood + no
  countermeasure = dead project. A fatal-severity risk cannot carry an accepted treatment — it cannot be accepted by name.
- **Killer assumption first**: the riskiest thing gets the cheapest test
  before anything else is examined. The **SPIKE** is that instrument —
  declared up front, cheap, built for a kill-or-keep decision.
- An unqualified risk MUST NOT reach the next stage.
- A treatment is not proven merely because its field is populated: acceptance demands the citation resolve.

## Tiering

| Tier | Instrument |
|---|---|
| Everyday | the ledger filled inside the framing conversation — normal-sized work |
| Large bet | the full interrogate session — exhaustive across the axes (technical · business · legal · operational); its co-sign becomes the **viability gate record** (dated, `docs/gates/` shape) |

## Flows

- **Out**: risks arrive PRE-CHEWED at slicing and design — never
  re-assessed there. A feature carrying a temporary countermeasure is a
  different slicing candidate from one carrying a permanent fix.
- **In**: every △ verdict in the evaluation matrix lands its countermeasure
  here, with confidence and return condition.
- **On fatality**: an idea killed by a FATAL risk is recorded in *What we
  ruled out* with the ledger row as evidence and its return condition
  attached — elimination by analysis, captured as a byproduct.
- The ledger's states map onto the Toyota marks (○ = no countermeasure
  needed · △ = countermeasured · × = fatal/none) — one vocabulary across
  viability and evaluation.
