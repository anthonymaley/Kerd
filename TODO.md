# TODO

## Now

**2026-08-14 (late) — an unattended session ran the mechanical block.** Six
things landed, all pushed and CI-green. Nothing here needed a decision; the
things that did are listed as waiting for you below.

**Landed:**

1. **Nine statements reworded** against the word list (`register-v2.md`). The
   obligation is unchanged in every case. Open question 5 split in two, and its
   research half — *the technique is nowhere taught* — **was false**: EARS's
   ubiquitous pattern and ISO 29148's `each` rule both teach it, and both are
   now ADOPTED in `docs/design/requirement-shape.md`. Full before/after in
   `docs/requirements/findings.md` §8.
2. **Both parser hazards closed** (`tools/reqview/reqview.py`). The em-dash
   handle was real and *silent* — it truncated and refused nothing. The
   findings-concatenation hazard was already closed; now proven and pinned.
   Four fixtures added.
3. **`gate.py --root` landed** — the gate aims at the project, never at its own
   install path, and refuses rather than falling back. Seven fixtures.
4. **The behind-upstream test fixed** — never environmental. `git init --bare`
   points HEAD at `master` while the fixture works on `main`, so the clone had
   no upstream at all. **22 passed, 0 failed** — first fully green run.
5. **The playbook's `## Current Status` split** into pointers plus an honest
   release-history heading. It had drifted to v0.95.0 / nine skills / four
   hooks / 26 tests.
6. **`docs/requirements/archaeology.md`** — **53 candidate requirements**
   recovered from CONTEXT.md's standing decisions, in six batches (A risk ·
   B record · C working relationship · D release and judgement · E method ·
   F the remainder), each quoting its source, none minted with an `R-`
   reference. **All 88 standing decisions are classified in its coverage
   table** (the Backlog row says 74 — it has grown). **The remainder is
   empty**: every decision carrying an unfiled obligation now has a candidate.
   That is not the same as the register being complete, and the file says so.

**Waiting on you — nothing below was guessed:**

- **The 38 Whys.** Unchanged; still yours, still never in bulk.
- **R-0007** — its defect is an uncheckable clause, not a totality word. Making
  it checkable decides what the register owes the tooling. Two readings named
  in `findings.md` §8.
- **Does `every` join the banned word list?** Widening the rule is yours.
  R-0048 is the only live statement it would touch.
- **Retiring the old register is coupled to the refuser** —
  `docs/requirements/findings.md` §9. Deleting `register.md` does not turn CI
  red; it makes AU7/AU8 **silent**, because `register_check` is a vacuous pass
  when the file is absent. The live register (`register-v2.md`) is validated
  only by the reqview spike, which is not in CI. One ruling: does the new
  validator graduate into `gate.py audit` before the old register goes, or does
  the old register stay until it does?
- **The archaeology batches**, keyed by family — A risk, B record, C working
  relationship, D release/judgement, E method. Several entries carry a named
  overlap or tension with an existing requirement (C-06 vs R-0051, C-24 vs
  R-0028) that only you can resolve.
- **Does this project keep a hand-written changelog at all?** `CHANGELOG.md`
  and the playbook's release history are the same abandoned artifact and sit in
  the Backlog as two rows. One question, not two.

**Deliberately not done:** the board's two features stuck below `goal` (TODO
says don't walk them by hand), the board label overlap (cosmetic, and touching
the renderer risks the byte-compare refuser), and the view's build (its one
decision is yours).

**2026-08-14 — the reset produced a working format, a cleaned register, and a
view.** See `kivna/sessions/2026-08-14.md`. Four laws now (Law 4 arrived with an
ordering rule); the requirement shape is settled at six elements and was tested
twice and audited twice; the register is migrated, triaged and cleaned — **39
live, 13 dead**; and a generated HTML view exists as a spike.

**Next, in order:**

1. **Thirty-eight requirements await Tony's words.** Their Why is honestly
   unwritten — the old register recorded provenance only, and 44 of the 51
   shared one identical pointer string. **Do not invent these.** Best taken a
   few at a time as work touches them, never as a batch: bulk authorship of
   reasons is the same failure shape as bulk approval.
2. **Twelve statements fail the adopted word list**, almost all on totality
   words. He ruled the statements yield, not the rule: *"they pre-dataed that
   rule - so need to rework or redo"*. Listed in `docs/requirements/findings.md`.
3. **The suspect-link stamp has no slot in the format.** The shape document
   recommends keeping it; the normative form has nowhere to put it. **This is a
   format change, not a fix** — it would put each target's fingerprint inside the
   dependency field, which is hashed, so it changes what the fingerprint covers
   and invalidates both published test vectors.
4. **Build the view properly, if it earns it.** The spike's own recommendation:
   the applier first (the page emits, nothing applies), drop the edit toggle,
   give comments a real home. **One decision is his:** *"no server" and "direct
   write-back" cannot both hold* — paste-back works from a file, direct
   write-back needs a local process.
5. **The old register still exists.** `docs/requirements/register.md` is
   superseded by `register-v2.md` and was deliberately left untouched until the
   new one was verified. It now is. Retiring it is a deliberate act, not a
   cleanup.

**Two residual parser hazards, reported and not closed:** a handle containing an
em dash would split wrong, and `docs/requirements/findings.md` keeps numbered
headings of the shape that caused a defect if it is ever concatenated back.

**Five residues are recorded in the graveyard** — binding fragments that outlived
their dead hosts. They are named where a future proposer will hit them, not
lost.

---

**THE PROJECT RESET, 2026-08-13 evening.** Tony called a full stop:
*"honestly i feel we are lost here, i have no clue if what we have build and
what the requirments will build is what we need now. the fact that we are both
confused tells me we need a reset."* Everything below supersedes the previous
plan for this sitting.

**What now exists** (all committed, see `kivna/sessions/2026-08-13.md`):

- `docs/kerd-interview.md` — the reset interview, verbatim, **confirmed by Tony
  as the source of truth**. Deliberately grounded in nothing that already
  existed. Everything else gets checked against it, not the reverse.
- `docs/kerd-goals.md` — **APPROVED 18:30**. Three laws, eight goals, each
  carrying a design input in his own words.
- `docs/kerd-requirements.md` — **a DRAFT, not awaiting a yes.** Goals are
  inputs to requirements; finalisation is a worked process.

**Next, in order:**

1. **What the requirements system actually IS.** His ruling: *"we cannot
   consider this markdown file as how we capture and version and work on
   requirements. we need a robust and easy to engage with solution."* The
   pre-reset tooling evaluation (`docs/design/requirements-traceability.md`, 6
   options × 24 criteria) is **now legitimate input** — the bracketing rule
   expired when the interview was captured. Re-examine it against the approved
   goals rather than as precedent. Note the requirements draft's own finding:
   the register demands per-entry change management of the product while
   practising none on itself.
2. **Work the requirements draft through to final** — translated, drafted,
   worked on, finalised. Not one composer pass and an approval.
3. **The build-vs-adopt decision (interview Q4), still open.** Now has criteria:
   the approved goals. The superpowers material in Q4 is **experience, not
   requirement** — input to that evaluation only.

**Carried, unresolved, from the outward pass:** our answer to false approval is
presentation-based (borders, brevity, visuals) while current human-in-the-loop
practice uses *active confirmation*. Tony's ruling: proper requirements
management plus strong pairing mitigates but does not cure — accepted, residue
named.

**Parked by the reset, not cancelled:** closing `model-effort-advisory` and
`hooks-autoload` on the ladder (both shipped, both stuck below `goal` because a
proportional build skips rungs the gates demand). `hooks-autoload` also fails at
`slice` on an illegal risk-ledger State token — `accepted (named loss)` is not a
legal value. The board is currently misreporting two live features. Do not walk
these by hand: the reset may change what the ladder even is.

**Also parked:** `docs/product/inline-composer.md` — framed during this sitting,
deliberately left unbuilt. It is the funnel working correctly (captured without
displacing), and the reset may supersede it entirely.

**DONE 2026-08-13 afternoon sittings** — AU7/AU8 the register validator
(v0.97.0, `8b7f52d`) and the model+effort advisory building `FUN-010` (v0.98.0,
`f4c51c0`), both CI-green. Hooks auto-load was **empirically verified** at this
sitting's switch-in — the top High backlog row, now closed.

**Then, in order:**

1. **Land `gate.py --root`** — a hard dependency, not a follow-up. Its CLI half
   is minutes; its **script-location half is undesigned** and that is the real
   work (`${CLAUDE_PLUGIN_ROOT}` expands nowhere in this repo,
   `$CLAUDE_PROJECT_DIR` measured unset).
2. **Rework the blocked design package** against everything keyed today. It has
   ~19 original findings, ~15 from the terrain pass, ~5 from the schema study
   and ~60 surviving the verification pass. **Absorbs the trace gap (agreed
   2026-08-13):** after the producer files the origin rows, the model drafts
   `refines` parents in category batches and he keys them as sets; the forward
   half is slice 2. The AU8 finding (46 unparented at last audit) is the live
   tracker.
3. The release grouping artifact, then the board.

*(Retired 2026-08-13: "move the twenty category codes out of kit.py" — the
validator reads the legal set from `categories.md` and the codes were never
hardcoded anywhere.)*

**Owed by the producer, neither blocking:**

- **File the origin rows — BUS/STA/USR.** The trace's top: the handful of
  requirements stating what Kerd is for and who is asking (~5-10 blocks, frame
  rung, his stakes). The disposition file already calls all three categories
  a gap. Prerequisite for wiring the 46 `refines` parents.

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

- ~~**Verify hooks auto-load fires on this machine.**~~ **CLOSED 2026-08-13
  ~16:40**, at this sitting's switch-in. Three confirming observations: the
  cache carries 0.96.0 with `hooks/hooks.json`; neither `.claude/settings.local.json`
  nor `~/.claude/settings.json` holds any Kerd hook wiring; and `📋 Last session:
  2026-08-13` appeared at session start — a string built only by
  `hooks/session-start.sh` (lines 39, 58, 63). Auto-load works and
  `${CLAUDE_PLUGIN_ROOT}` resolves at runtime with zero per-repo wiring.
  **Note for `docs/product/hooks-autoload.md`:** its risk ledger still calls
  this open, and its acceptance test quotes the rendered string `Last session`
  when the source literal is lowercase — a grep for the documented string
  returns nothing and reads as "the hook didn't fire".
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
  session running current cache text is one where nothing shipped. (Narrowed by
  v0.96.0: this is now about stale *skill text* only — hooks no longer rot with
  the cache version, they auto-load and resolve `${CLAUDE_PLUGIN_ROOT}` at runtime.)
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
- **`tests/hooks_test.sh` behind-upstream test fails environmentally** — `git
  fetch --dry-run` against the fixture's local bare remote emits no `->` line in
  this sandbox, so the behind-remote assertion gets an empty message. Fails on
  HEAD too (pre-existing, not from the v0.96.0 hooks work). Fix the fixture's
  remote setup or the hook's behind-detection to not depend on fetch dry-run output.
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
