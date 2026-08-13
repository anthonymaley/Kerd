---
route: new
stage: sliced
---

# Model + effort advisory — conductor manages both, in both directions

## Value

Tony's requirement, in his words (2026-08-13, stated live mid-session after
setting the session to Fable and asking who conducts and who composes):

> basically we need kerd conductor to effectively manage model usage and
> effort, i.e. if we are at fable xhigh, it should tell us to change to opus
> medium or whatever and then bring fable and other models in to do the work
> at the right effort too

Keyed as `FUN-010` (final, `sha256:b4537fbe358a`) in
`docs/requirements/register.md`.

The measure of winning: a session opened on an oversized model/effort pair gets
told so at orient — with the named cheaper pair and the reasoning — and the
expensive tiers are bought back per-call (composer, players) at a sized effort,
instead of the whole session running at premium rates. Nothing beyond the gap
Kerd can honestly close: the advisory is advice plus a confirmation gate, never
detection the harness does not offer.

## Grounding

- skills/conductor/SKILL.md — the Model advisory section being extended: today it sizes upward only ("recommend a strong mid-to-upper model") and says nothing about effort or about advising down.
- docs/requirements/register.md — FUN-010, the requirement this builds, and the register discipline it rides.
- docs/design/conductor-role.md — the four-role seating (producer/composer/conductor/players) whose cost model this completes: top tier per-call, not per-session.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| The model cannot reliably know the session's current model or effort, so the advisory asserts a wrong current state and advises from it | yes | advice built on a false premise — e.g. telling a session already on Opus to "switch down to Opus", or missing a Fable session entirely | high without the countermeasure: the system prompt names the model at session start and goes stale on every mid-session `/model` switch; effort is exposed nowhere | this very session — the prompt says Opus 4.8, the session has run on Fable since 13:26; effort was never visible | countermeasure - permanent | The advisory states its *belief* and its source, asks the user to confirm the actual pair, and gates on the answer — belief, never detection; effort is always asked, never guessed | Fires if the harness ever exposes current model/effort to skills — then detection replaces asking |
| The advisory beat becomes a nag — every session opens with a model interrogation | no | friction at orient; users skip conductor | medium | the existing advisory already carries a skip rule ("skip the gate only when the work is trivially small") | countermeasure - permanent | The gate is sized to the task exactly as today: trivial work skips with a stated reason; the effort question rides the existing confirmation beat as one extra word, never a separate exchange | |
| Advising down mid-flow loses session context on the switch | no | none — `/model` preserves the conversation | certain it does not | this session switched Opus → Fable mid-conversation with full context carried; the risk is empty on the evidence | accepted | | Fires if the harness changes `/model` semantics |

## Release slice

Rigor level: mvp

One proportional build (design settled in the framing conversation 2026-08-13,
no separate design/contract rung):

- `skills/conductor/SKILL.md` Model advisory section becomes model *and* effort, bidirectional: state the believed current pair and its source, confirm, then advise the cheapest pair that conducts well — naming the downgrade explicitly when the session is overpowered (e.g. Fable xhigh → Opus medium) with the reasoning that difficulty is bought per-call.
- The composer call gains a sized effort in its dispatch (model *and* effort, like player tags already have).
- The principles bullet and the SKILL.md frontmatter trigger description follow the behavior.
- `README.md` conductor section updated; version 0.97.0 → 0.98.0; release checklist run.

Deliberately excluded: any automatic detection of the session pair (no harness
surface exists — the risk ledger's review trigger names the return condition);
changes to any other skill; hook-layer enforcement.
