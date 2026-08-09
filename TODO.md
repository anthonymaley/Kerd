# TODO

## Now

**Requirements is the live subject.** The producer's shape, 2026-08-07:
**requirements → features → releases**. The middle layer partly exists — 13
product docs. Both other ends are empty.

**DONE and pushed this sitting** — see `kivna/sessions/2026-08-08.md`:
the build-vs-adopt evaluation (verdict BUILD, on merit), the mark set and its
machinery, the schema study, the register data model, and
**`docs/requirements/` itself** — catalog, disposition and 50 requirements as
blocks with 15 typed links.

**BLOCKING, and it is the honest next move:** `docs/requirements/catalog.md`
declares refusals — *"an unknown field is a hard error"*, *"the audit REFUSES"*
— and **nothing enforces any of them.** No AU7, no AU8, no validator. A
declaration of refusals with no refuser is exactly the criticism this design
makes of the `Piece:` trailer. AU7/AU8 were prototyped at 117 lines and 11
fixtures, passing first run; the working stdlib parser is in this sitting's log.

**Then, in order:**

1. **Land `gate.py --root`** — a hard dependency, not a follow-up. Its CLI half
   is minutes; its **script-location half is undesigned** and that is the real
   work (`${CLAUDE_PLUGIN_ROOT}` expands nowhere in this repo,
   `$CLAUDE_PROJECT_DIR` measured unset).
2. **Rework the blocked design package** against everything keyed today. It has
   ~19 original findings, ~15 from the terrain pass, ~5 from the schema study
   and ~60 surviving the verification pass.
3. **Move the twenty category codes out of `kit.py`** into the project's own
   catalog — Build scores `△+` on its own taxonomy criterion because they are
   hardcoded, contradicting the standing "declared per project" rule.
4. The release grouping artifact, then the board.

**Owed by the producer, neither blocking:**

- **`categories.md` needs his key.** The disposition is his by design; it is
  model-drafted, and three rows are flagged as genuine judgment calls. `SEC` was
  corrected to `applies` on 2026-08-08 after code falsified its `n/a` reason.
- **The board's mechanism** — a served stdlib process with true write-back, or a
  downloaded edits file the next session applies. Open since 2026-08-08 ~10:00.

**Standing conduct:** the producer's rungs are frame, viability, slice and
design, plus evaluation at goal; contract and build are the model's. Do not
narrate build mechanics. The plan-approval gate is deleted — his key lands on
the design.

## Backlog

*Ranked by consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**

- **`gate.py --root` — promoted from Medium.** No longer a nice-to-have: it is
  a hard dependency of requirements-traceability slice 1. `tools/gates/kit.py:24`
  derives `ROOT` from the tool's own path, so a consuming project would audit
  the plugin cache. The pattern already exists in all four hooks
  (`${CLAUDE_PLUGIN_ROOT}` finds the script, `$CLAUDE_PROJECT_DIR` finds the
  state) and the gate library already takes `root` as a parameter everywhere —
  only the CLI pins it.
- **Hookify — promoted to a dependency.** `OPS-001` (funnel interaction requires
  a conductor session, everything else stays open) is a **refusal**, and skill
  text cannot enforce it on itself. A hook fires outside the model, which is the
  only layer that can. `hookify` is installed and unused. Its
  `conversation-analyzer` also reads a transcript for behaviours worth
  preventing — the superpowers pull is one, since the v0.77.0 "tie is cut"
  countermeasure aims one layer below the cause.
- **Requirement archaeology over CONTEXT.md's 74 standing decisions.** Framed
  work, never ad-hoc, and **never from session logs** (see the decision in
  CONTEXT.md). Provenance must be marked permanently or the register becomes
  untrustworthy with no way back.
- **The release-planning artifact.** Gained two inputs today: project type ==
  release type for the twelve that ship, and `TECH-006` requirement dependency —
  which is the missing artifact behind the 2026-08-03 decision's first deciding
  factor, *"dependency forbids (hard constraint)"*.
- **Frame switch-fidelity slice 2 — capture human input.** Gaps 10/11/12. Note
  the overlap: requirements-traceability is arguably this slice's mechanism.
- **The fidelity check** (accepted unknown; review trigger already fired).
  Nothing verifies a pickup restored what the close recorded. It proves *file*
  reachability, never *finding* reachability.
- **boundary-cycle, in-half** — the reset ritual's automation. Killer
  feasibility question first, verified against harness docs at frame.
- **Plugin cache repin debt.** Reopened by v0.95.0: the cache was current at
  0.94.0 this afternoon and the repo has since shipped. Structural — the only
  session running current cache text is one where nothing shipped.
- **Stashes and local-equals-remote are unchecked at the boundary.**
- **The playbook's `## Current Status` duplicates CONTEXT.md.** Its stale
  content was fixed this session (v0.90.0 → v0.95.0, three hooks → four); the
  duplication itself remains. Kill it or make it a pointer.
- **Out-of-repo artifacts have no home** — PRs, URLs, decks, external docs.
- **Stop-hook over-prescription**: distinguish work-dirty from
  session-state-dirty at a real stopping point.

**Medium**

- **The refusal surface does not travel with the plugin — the return condition
  FIRED 2026-08-07.** It was accepted "for now" with the trigger *"the first
  time Kerd's ladder is run in a repo that isn't Kerd"*; declaring requirements
  traceability a capability for consuming projects is that moment. Now
  interlocked with the `--root` row above.
- **`docs/vault-spec.md` contradicts itself** (found by tend this session): line
  39 says Weekly is "the one append-style file in the vault", line 88 describes
  the decisions file as accumulating entries. `Kerd Architecture Decisions.md`
  (6 dated sections) and `Kerd Skill Lessons.md` (5) sit in the gap. Not drift —
  a genuine unresolved rule.
- **`Kerd.md` MOC has one broken wikilink** — `[[eloas/Eolas]]`, a typo for
  `eolas`. 16 of 17 resolve. Vault write, so kivna's.
- **Revisit the journey view when more data exists** (parked 2026-08-05, shape
  agreed on mock v4).
- Clean krutho-strategy's stray `sessions-of-record/`.
- AGENTS.md needs its own verdict: gitignored, machine-local, stale Codex-era fork.
- Regenerate the choose-what-matters view before its next use.
- Hook version staleness check in `/kerd:tend`.
- PR-event edge in the stale CI step (unexercised; no PR flow).
- Guard switch-in step 3 smoke test against context bloat.
- **lorg-cut candidate** — evidence check per the rip discipline before any
  license. **Interrogate rides the same review** — and note it now has a second
  caller: requirement qualification is the same shape as risk qualification.
- **kivna verdict** — same zero-usage smell as the vault; import/export
  confirmed unused.
- **CI rule for the single-definition law** — nothing machine-enforces
  "conductor never re-describes a Switch Out step".
- **Close-out double-write** — conductor step 1 writes CONTEXT/TODO, step 6's
  invoked flow overwrites both.
- Derive the rigor refusal messages from `RIGOR_LEVELS` via join.
- Gate records can only say GO: a refused gate has no dated home.

**Low — genuinely ignorable, and you can see what ignoring costs**

- `CHANGELOG.md` stale at 0.14.0 while the repo is at 0.95.0, and absent from
  the release checklist. Revive or delete.
- Stale `Kerd.md` MOC version field (says 0.31.0).
- Consider promoting the refined question-formation rule from the pair hook into
  global `~/.claude/CLAUDE.md`.

**Blocked — not candidates at any consequence**

- skriv voice profile wiring — needs non-founder-genre samples.
