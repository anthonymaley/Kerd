# Conductor-boundary — design

Slice 1 of `docs/product/conductor-boundary.md`: conductor's close-out
runs the boundary and names what's next. Canvas:
`docs/design/conductor-boundary.excalidraw` (generator:
`tools/diagram/gen_conductor_boundary.py`).

## The mechanism — invoke is literal

The frame's killer risk was prompt-layer drift: two descriptions of the
boundary flow diverging over releases. The design dissolves it
structurally rather than mitigating it: **conductor's close-out calls
`/kerd:switch out` through the Skill tool** — the same chaining this
repo's sessions already exercise in the other direction (switch-in
step 11 flows into conductor; observed working 2026-08-06, twice in
one session). Conductor's text gains one instruction to invoke, zero
descriptions of what the flow does. The boundary stays defined in
exactly one place: `skills/switch/SKILL.md`, Switch Out.

Consequences that fall out for free:

- The banner additions (next pick, `/clear` offer) belong to
  **switch's** completion banner — both callers get them; a
  conductor-less session sees the same ritual line.
- Closure inference, triage, gotcha-mirroring, the session log — all
  arrive unmodified because nothing is re-implemented.
- Switch-out's own behaviour needs no two-caller conditionals: the
  flow cannot tell who called it, and doesn't need to.

## Edit map

Every truth site from the design-time cross-cutting sweep
(`grep -rn` over skills/, docs/state-contract.md, docs/playbook.md,
README.md, CLAUDE.md for boundary-ownership claims — the standing
obligation from the vault-unhook goal block). One site is a dated
release-note record (`docs/playbook.md` v0.26.0 entry) and is left as
history, considered and named.

**skills/conductor/SKILL.md — 5 edits**

1. Close-out intro (§4 first paragraph): "Conductor closes the *work*,
   not the *session boundary* … what remains for switch" → close-out
   ends by running the boundary itself; the sentence naming what
   remains for switch dies.
2. New close-out step 6: **Run the boundary** — invoke `/kerd:switch
   out` via the Skill tool (full mode; the modifier may be dropped to
   the standalone default). Placed after step 5 (marker clear), so the
   `[conductor: closed]` marker moves to after the boundary completes.
3. The hand-off paragraph ("Then hand off: tell the user to run
   `/kerd:switch out` …") — deleted whole. Its truth ("conductor does
   not pull, does not write session logs" ) survives restated in the
   principles bullet (edit 5): the boundary work happens inside the
   invoked switch flow, not in conductor's own hands.
4. Execute phase, Work commits section: one added paragraph — at each
   task's verified commit, name what's next in one line (the next plan
   step while a plan runs; the top TODO `## Now`/Backlog pick when the
   plan is done). Suggestion only; starting it stays a human reply.
5. Principles bullet "Conductor doesn't own the boundary — but it does
   own its work" → "**Conductor closes the session it conducted.**
   Work commits per verified task, then close-out invokes the Switch
   Out flow (`/kerd:switch out`) as its final act — one definition of
   the boundary, two callers. Standalone switch out serves sessions
   without conductor. Conductor still never pulls (pull is
   switch-in's) and never writes session state by hand."

**skills/switch/SKILL.md — 3 edits**

6. Ownership paragraph (line ~10): "**Switch owns `git pull` and the
   session-state commit.** Nothing else pulls." → "**This file is the
   single definition of the boundary.** Switch-in owns `git pull` —
   nothing else pulls, ever. Switch Out makes the session-state commit
   and has two callers: standalone `/kerd:switch out`, and conductor's
   close-out invoking the same flow as its final act. Either way the
   steps below are the only definition — no caller re-describes them."
7. Switch Out section intro: one added line naming the second caller.
8. Completion banner (step 8): two added lines in the template —
   `Next: [suggested pick from TODO]` already exists; add
   `Free context: type /clear, then /kerd:switch in` beneath it.
   (Applies to the full-mode banner; low keeps its one-liner.)

**docs/state-contract.md — 4 row edits**

9. CONTEXT.md Owner row: "switch (writes at out)" → "the Switch Out
   flow (standalone, or invoked by conductor close-out)".
10. TODO.md Owner row: same two-caller phrasing for the wrap-up
    writer.
11. Session-log Owner/notes rows ("Switch is the sole creator") →
    "the Switch Out flow is the sole creator (either caller)".
12. Git row ("Git pull/push/commit | **switch** | No other skill
    touches git boundaries") → pull: switch-in only; session-state
    commit: the Switch Out flow, either caller; work commits:
    conductor per verified task (already true since v0.67.0 — this row
    was stale for it).

**README.md — 3 edits**

13. Conductor section (line ~62): closing sentences → close-out runs
    the boundary itself (one act), names the next pick, offers
    `/clear`; standalone switch out remains for conductor-less
    sessions.
14. Layers paragraph (line ~263): "Switch owns the session boundary —
    pull, and the session-state commit" → boundary defined in switch,
    two callers; pull on switch-in.
15. What's New: v0.84.0 entry, cap at five versions (drop v0.79.0).

**docs/playbook.md — 1 edit**

16. Architecture role line (line ~64): switch = "session boundary
    (pull on arrive…)" → two-caller phrasing, one line.

**.claude-plugin — version bump**

17. 0.83.1 → 0.84.0 in the three fields (MINOR: changed behaviour).
    Capability lists: unchanged — "session discipline, machine
    handoff" still describes both skills; checked at design time, no
    drift introduced.

## Stage-1 measurements — named answers

- **Handoff ask 1 → 0**: `grep -c 'tell the user to run' skills/conductor/SKILL.md`
  prints `0` after edit 3 (today: 1).
- **Single definition**: conductor's file contains no switch-out step
  headings — `grep -c 'Update CONTEXT.md (state)\|Heal and self-migrate\|Completion banner' skills/conductor/SKILL.md`
  prints `0`; the invoke instruction names `/kerd:switch out` —
  `grep -c 'invoke.*kerd:switch out\|invokes.*kerd:switch out' skills/conductor/SKILL.md` ≥ 1.
- **Both banner lines exist once, in switch**:
  `grep -c 'Free context: type /clear' skills/switch/SKILL.md` prints
  `1`; same grep over `skills/conductor/SKILL.md` prints `0`.
- **Pull untouched**: the Switch In section of `skills/switch/SKILL.md`
  is byte-identical before/after (awk-extract + `diff`), same proof
  shape as vault-unhook's.
- **Standalone flow intact**: the Switch Out `### ` step-heading list
  is unchanged except the banner template body (awk-extract + diff
  against parent tree).
- **Next-pick naming present**:
  `grep -c 'name what.s next' skills/conductor/SKILL.md` ≥ 1 (execute
  phase) — exact phrase fixed at contract time.

## Out of scope, named

- Any `/clear` automation (CLI built-in wall; the banner offers, the
  human types).
- Loops, hooks, scheduling — suggestion only, per the frame's
  permanent countermeasure.
- Light/low modifier changes and boundary auto-sizing (separate
  Backlog item).
- The stop-hook over-prescription fix (separate Backlog High item) —
  adjacent but untouched here.
- kivna scaffold / tend first-run wiring (captured to the tend/slainte
  review brief, 2026-08-06).
