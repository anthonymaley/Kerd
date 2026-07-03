# Context/History Split — Lean Switch Handoff — 2026-07-03

Origin: Tony asked whether RDF could make switch-out/switch-in context "full but
easier / cheaper to load". The investigation found the cost is not the format —
markdown is near-optimal for the LLM reader — it's that **switch-out writes the
same session narrative three times** (TODO.md Current Session, the session log,
vault Status.md) and switch-in reads all three copies. Diagrammed against the
2026-07-03 switch-in: ~4,300 tokens read, ~1,700 of them duplicate copies.

RDF was rejected: an LLM has no query engine at load time — it pays per token of
serialized text; triples repeat their subject on every fact (~2× the tokens of
prose for the same decision) and drop the causal "why" that makes cold pickup
work. Prose is the compressed format *for this reader*.

Decisions below are co-signed with Tony (2026-07-03).

## The principle — state, work, and history are three different things

The current design smears them: TODO.md carries work AND state (its `### Context`
section is half the file), the session log carries narrative AND forward items,
Status.md re-tells everything for the vault. One kind of information per file:

| File | Kind | Discipline |
|---|---|---|
| **CONTEXT.md** (root, new) | **State** — what's currently true | Overwritten in place, bounded size |
| **TODO.md** (root) | **Work** — what's still to do | Forward-only, lean |
| **kivna/sessions/** | **History** — what happened | Immutable, append-forever, full fidelity |

**Completeness without degradation:** history is never compressed — session logs
keep full narrative forever, and git history is the archive of every CONTEXT.md
version ever pruned. Nothing is lost in storage; the *working set* (what a fresh
session reads) stays small. Efficiency comes from reading less, not storing less.

**The sharp edge — a context file must never become a diary.** If CONTEXT.md
accumulates per-session "what was said/done", it regrows the bloat and starts
degrading under its own weight. The session log is the diary. CONTEXT.md holds
only what is *currently true*; superseded content is pruned (git keeps it).

## File contracts

### CONTEXT.md (new, root, committed)

Living state document. Sections (bare headers, omit-if-empty discipline as in
session logs):

```
# Context

## What This Is        — one paragraph, the project in brief
## Where We Are        — current working state, a short paragraph, overwritten
## Key Decisions       — standing decisions + their why; prune when superseded
## Open Questions      — genuinely unresolved; remove when answered
## Active Mode         — mode/sherpa/conductor snapshot for cross-machine handoff
```

- Absorbs TODO.md's `### Context` section (moves out of TODO entirely).
- Absorbs the mode snapshot job (switch-out step 1 currently writes it to TODO).
- Overwritten in place each switch-out — like Status.md, but LLM-facing.
- NOT a copy of the session narrative. If a fact is in the latest session log
  and is episodic (what happened), it does not belong here. If it's standing
  (a decision, a constraint, the current stage), it does.

### TODO.md (slimmed)

```
# TODO

## Now       — current focus: pointers + deltas, a few lines, no re-narration
## Backlog   — queued items, one line each
```

- `## Current Session` block and `### Context` section are retired.
- No session story. The latest session log carries "what happened"; TODO points
  ("see kivna/sessions/<date>.md") instead of re-telling.
- Forward-only rule and the heal-accumulated-history backstop (switch-out 1b)
  stay, retargeted at the new shape.

### kivna/sessions/ (unchanged format, changed read policy)

- Switch-out writes the full session log exactly as today — this is the
  canonical record and the fidelity guarantee.
- Switch-in reads **only the newest file**. Older logs are archive: grep/read
  on demand, never per-session load. Safe because forward-only discipline
  already guarantees anything still-relevant was carried into CONTEXT/TODO or
  the latest log's What's Next — if it wasn't, that's a switch-out bug.

### docs/playbook.md (the gotcha guarantee)

Dropping the older-log skim is safe for forward items (forward-only discipline
carries them) but gotchas need their durable home to actually work. Switch-out
step 5 already mirrors gotchas to the playbook — but nothing verifies it, and
the 2026-06-28 Edit-tool gotcha proved the step can silently slip (it lived
only in the session log for five days; see Test 1 below).

- **New switch-out check:** before committing, verify every entry in this
  session's `## Gotchas` has a playbook counterpart. Cheap grep, closes the
  hole. This makes the older-log skim safely droppable — the playbook, not
  the log tail, is the gotcha net.
- Playbook stays on-demand at switch-in (reference, not per-session load).

### Vault Status.md (write-only from switch's perspective)

- Still written at switch-out via `kivna save` — the vault stays human-first,
  kivna is untouched.
- **No longer read at switch-in.** It contains nothing the log + CONTEXT.md
  didn't already say; it exists for the Obsidian reader.

## Switch-in read set (full mode)

| | Today | Proposed |
|---|---|---|
| TODO.md | full (~1,300 tok) | full, lean (~350 tok) |
| Latest session log | full (~1,500 tok) | full (~1,500 tok) |
| Older logs | skim What's Next/Decisions/Gotchas | **not read** |
| Vault Status.md + MOC | read (~1,100 + skim) | **not read** |
| CONTEXT.md | — | full (~400–600 tok) |
| **Total** | **≈ 4,300 tok** | **≈ 2,300 tok** |

Same fidelity — everything removed is a duplicate copy or human-facing framing.
Matters most for Tony's working rhythm: switch out at ~50% context free, switch
back in, keep going — the pickup cost is paid several times a day.

## Validation

**Test 1 — A/B cold-pickup quiz (2026-07-03): PASS.** Two isolated agents, no
session context, simulating a next-session pickup. Set A read today's full
switch-in set (TODO + latest log + Status.md + MOC + older-log skim); Set B
read only the lean set (hand-drafted CONTEXT.md + lean TODO + latest log,
~700 tok of state/work vs ~2,400). Twelve questions, several derived
adversarially from the content the lean set removes. Result: 11/12
substantively identical, zero NOT-FOUNDs on either side; the Status.md-derived
questions were fully answered by Set B (confirming that content is duplicate).
The one delta: Set A surfaced the 2026-06-28 Edit-tool gotcha via the
older-log skim — root cause was the unverified gotcha-mirror step (see the
playbook contract above), a pre-existing hole in the *current* design, now
countermeasured. Instance healed: gotcha mirrored to playbook 2026-07-03.

**Test 2 — one manual lean switch cycle (pending).** At the next switch-out,
write CONTEXT.md + lean TODO by hand alongside the normal files (skill
unchanged); next switch-in reads only the lean set. Tony judges the acceptance
criterion no quiz can: does it still feel like the same session? Pass → build.

## Implementation plan

One conductor session, eyeball-gated slices:

1. **Slice 1 — switch SKILL.md rewrite.**
   - Switch-out step 1 splits: write CONTEXT.md (state, overwrite) + lean
     TODO.md (work). Mode snapshot moves to CONTEXT.md `## Active Mode`.
   - Switch-out 1b (heal) retargets: also migrates a legacy `## Current
     Session` block / `### Context` section into CONTEXT.md + session log on
     first run (self-migrating — no separate migration step for other repos).
   - Switch-in: read CONTEXT.md + TODO.md + newest session log only. Drop
     vault read (step 5) and older-log skim (step 6). Handoff verification
     (step 2) now checks CONTEXT.md exists + TODO.md exists + latest log has
     `## What's Next`.
   - Modifier table updated (light/low inherit the lean read set; low reads
     CONTEXT.md `## Where We Are` + TODO `## Now` only).
2. **Slice 2 — cross-cutting reconciliation.** Grep ALL skills/docs for
   readers/writers of TODO's Current Session/Context shape: conductor
   (close-out), tend (structure checks), trim (TODO pruning), kivna
   (save/scaffold), sherpa (state pointers), state-contract doc, playbook,
   README. Retarget each. (Known gotcha: plans miss files — final grep is
   mandatory.)
3. **Slice 3 — migrate this repo.** Run the new switch-out once: creates
   CONTEXT.md from TODO's Context section, slims TODO. Eyeball the result.
4. **Release checklist.** MINOR bump (behavior change), README switch section,
   switch SKILL.md trigger description, capability list if warranted.

## Out of scope

- kivna/vault design (Status.md, MOC, Weekly) — unchanged, human-first.
- `kivna/sherpa.md` — already a correct "state" file; CONTEXT.md `## Active
  Mode` holds only the pointer, sherpa.md stays the stage record.
- RDF / any serialization change — rejected above.
- Retiring the vault-read question in Backlog ("should switch commit the vault
  repo") — separate decision, unaffected: switch still *writes* the vault.

## Open questions (to settle at build time)

- Does the `## Now` / `## Backlog` TODO shape cover conductor's close-out
  writes, or does conductor need its own line in the contract?
- Whether tend should gain a Category check for "CONTEXT.md exists + TODO is
  lean-shaped" (lean yes — it's cheap drift detection).
