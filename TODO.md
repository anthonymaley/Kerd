# TODO

## Now

**2026-08-22 evening — `gate-visuals` slice 1 is BUILT and sits at goal; the
standards map is answered.** See `kivna/sessions/2026-08-22.md`.

**Where things stand**

- **Register: 38 live, 33 approved, 0 invalidated.** `R-0018` re-approved.
- **`gate-visuals` enters at goal** — 8 of 8 pieces landed by trailer, full
  suite green. Needs the goal record (`docs/gates/*-gate-visuals-goal.md`,
  Done condition) with both keys: cold eyes on the whole change, and your
  expert-user pass — declare a concern on a real item, approve a drawing,
  edit it, watch the push refuse.
- **`standards-grounding` spike is answered** — 4 of 4 layers can name a
  standard (`docs/design/standards-grounding-findings.md`). Spine agreed.

**Next, in order**

1. **The `gate-visuals` goal gate** — cold eyes first, fresh context, then your
   pass. Lands the first goal record since the reset, which is a licensed prune
   event for CONTEXT.md.
2. **The four kept items from the spike, each its own small change:**
   ISO 25010 → the definition of `R-0011`'s quality column
   (`docs/design/iso-25010-quality-model.md` is the reference) · ISO/IEC/IEEE
   24774 §5.3 → a name / purpose / outcomes header on every `SKILL.md` (a skill
   change — version bump) · the UI viewpoint as a build, borrowing wireframe
   notation from design practice (no standard supplies it) · one sentence in
   `docs/design/gate-visuals.md`'s 42010 section: spine, not vocabulary.
3. **The archaeology batches** — 53 candidates in
   `docs/requirements/archaeology.md`, keyed by family (A risk · B record ·
   C working relationship · D release and judgement · E method · F remainder).
   C-06 against R-0051, C-24 against R-0028 are yours to resolve.
4. **Retire the old register — still coupled to the refuser.**
   `docs/requirements/findings.md` §9. One ruling: does the reqview validator
   graduate into `gate.py audit` first, or does `register.md` stay until it does?
5. **The suspect-link stamp still has no slot in the format** — a format
   change, because it alters what the fingerprint covers.

**The reset's three questions stay open** — what the requirements system IS,
the draft to final, build-vs-adopt (`docs/kerd-interview.md`). Not rows; the
work above is how they get answered.

**Still parked by the reset, not cancelled:** closing `model-effort-advisory`
and `hooks-autoload` on the ladder. Do not walk these by hand.

## Backlog

*Ranked by consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**

- **Standards grounding — second pass.** The spike (`docs/product/standards-grounding.md`,
  findings at `docs/design/standards-grounding-findings.md`) left three
  surfaced and unread: **ISO/IEC/IEEE 82079-1** (writing instructions — what
  a `SKILL.md` step body is, by 24774 §5.2), **ISO/IEC 25040** (the SQuaRE
  evaluation *process*, which `tools/design/` reinvented), **ISO/IEC/IEEE 24748**
  (life-cycle stages — the `stage:` field and the rung ladder, misfiled under
  product on his map). And 29148 never got the 42010 term-mapping test.
- **The conductor marker loses the sitting's open time when a session plans
  twice** — see the playbook gotcha of 2026-08-22. Design question: should
  `kivna/.active-modes` keep its first `execute` stamp across later phase
  rewrites? Owner: conductor's mode-marker section.

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
- **`gate.py --root` — the CLI half shipped 2026-08-14 (7 fixtures).** What is
  left: the hooks and skills that *invoke* the tools still assume the Kerd
  tree; nothing in a consuming repo calls `--root` yet. Narrowed, not closed.
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
