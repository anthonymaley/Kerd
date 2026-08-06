---
route: new
stage: done
---

# Conductor-boundary — the close-out runs the boundary and names what's next

## Value

Born from three briefs in one evening (Tony, 2026-08-06, all mid-turn
while watching the machinery run): tonight's conductor close ended
with "run `/kerd:switch out` when you're ready" — a wait-for-human ask
carrying no decision; the session then sat quiet after the boundary
until told to keep going, though TODO named the next pick; and the
observed workflow question ("are we not in a loop here?") resolved to
a simpler truth — no loop is wanted, the conductor should just *know*
what's next and say so.

Value, in units:

- **Boundary acts per conductor session: 2 → 1.** Close-out and
  switch-out become one act; the handoff ask dies.
- **Wait-for-human asks carrying no decision at close: 1 → 0.** The
  only prompts left at a close are real keys.
- **Every close names the next pick.** At task completion and at
  close-out, conductor reads TODO and names the suggested next item —
  mid-spec the plan chains itself; early in a project the suggestion
  comes from Now/Backlog. No loop, no hook — it is close-out text.
- **The reset ritual is named in place: out → `/clear` → in.** The
  close banner ends by offering `/clear` to free context (the model
  cannot run it — CLI built-in, wall confirmed 2026-08-06 — so the
  banner names the two keystrokes).

Named honestly, the loss: **the v0.67.0 two-owner split dies.** The
boundary stops being switch-only; "conductor doesn't own the boundary"
disappears from the contract. Switch keeps switch-in unchanged and
keeps a standalone switch-out — a session without conductor still has
its boundary (Tony's key: "we need to be able to use switch without
conductor").

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| Two copies of the boundary flow drift apart: conductor's close-out re-describes switch-out and the descriptions diverge over releases | yes | boundaries silently differ by entry path — the exact failure class the single-serializer rule closed in code | medium-high if duplicated — prompt-layer copies have no byte-compare | the v0.83.0 goal block: two routing documents carried stale boundary claims the edit map missed; prompt-layer drift is the system's best-evidenced failure | countermeasure - permanent | conductor never re-describes the flow: its close-out step INVOKES the switch-out contract as written in skills/switch/SKILL.md (one canonical definition, one reference to it); the design's edit map must show conductor's text pointing, not copying | |
| A second boundary run after conductor already closed (user habit: `/kerd:switch out` after close) | no | one no-op commit attempt on a clean tree | medium during habit transition | switch-out on a clean tree reports clean and commits nothing beyond an empty-state check; observed behaviour of the flow | accepted | | a real double-commit or confusing banner is observed at a boundary |
| Pull discipline blurs: conductor running the boundary starts to look like license to pull | no | mid-task file changes under in-flight work — the reason pull was boundary-only | low — the contract line survives verbatim | v0.67.0 rationale unchanged; switch-IN owns pull and is untouched by this slice | countermeasure - permanent | the contract keeps pull in switch-in only; conductor's close-out runs the OUT flow, which has never pulled | |
| Next-pick suggestions harden into auto-execution (scope creep toward the loop nobody asked for) | no | composer key eroded — the pick is Tony's by design (choose-what-matters) | low — text can only suggest | Tony 2026-08-06: "suggest when a task completes without building a loop or hook"; the 2026-08-02 loop guard stands for execution even though its CI precondition flipped | countermeasure - permanent | the suggestion is one line naming the item; starting it stays a human reply; no loop, no hook, no scheduling in this slice | |

## Release slice

Rigor level: mvp

Smallest valuable slice — **slice 1: conductor's close-out runs the
boundary and names what's next**: conductor close-out, after checks
pass and the marker clears, flows directly into the switch-out
contract (full mode, as written in skills/switch/SKILL.md — invoked,
never copied) with no handoff ask; the completion banner gains two
closing lines — the suggested next pick read from TODO, and the
`/clear` offer naming the out → `/clear` → in ritual; conductor's
execute phase names the next step at each task completion (plan step
while a plan runs, TODO Now/Backlog top when the plan is done);
switch-in untouched; standalone `/kerd:switch out` kept for
conductor-less sessions (its text gains one line naming conductor as
the other caller of this flow); docs/state-contract.md ownership rows
and README updated together; MINOR version bump.

Deliberately excluded, named:

- **Any `/clear` automation** — the model cannot invoke CLI built-ins
  (wall confirmed); the banner offers, the human types.
- **Loops, hooks, scheduling** — Tony's call 2026-08-06: suggestion
  without a loop; the boundary-cycle backlog item keeps the wider
  automation question with its own killer feasibility check.
- **Boundary auto-sizing and the light/low modifier question** —
  separate Backlog item, untouched here.
- **Release-triggered whole-doc-surface conformance** — the widened
  tend/slainte review, its own queued item.

## Grounding

- skills/conductor/SKILL.md — the close-out being given boundary authority
- skills/switch/SKILL.md — the canonical boundary flow conductor will invoke; stays the single definition
- docs/state-contract.md — the ownership rows the v0.83.0 goal block proved route behaviour
- CONTEXT.md — standing decisions bound: v0.67.0 two-owner split (superseded by this frame), pull-is-switch-only (survives), the loop guard
- kivna/sessions/2026-08-06.md — the evening sitting's three briefs, this frame's evidence
