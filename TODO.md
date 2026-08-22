# TODO

## Now

**2026-08-22 — the register is agreed, and `gate-visuals` waits at design.**
See `kivna/sessions/2026-08-22.md`.

**Where things stand**

- **Register: 38 live, 32 approved, 0 without a Why.** Every reason is his.
- **`R-0018` is invalidated and needs re-approval** — folding `R-0020` into it
  changed its words. Nothing was silently downgraded.
- **`gate-visuals` design PASSES.** Only the design GO record stands between it
  and contract, and that record is his — by `R-0014`, approving the design is
  the only approval needed to build.

**Next, in order**

1. **Re-approve `R-0018`** in the editor — one click, the words are the folded
   version you agreed.
2. **The `gate-visuals` design GO**, or push back on the package.
   `docs/design/gate-visuals.md`, two drawings beside it.
3. **The archaeology batches** — 53 candidates in
   `docs/requirements/archaeology.md`, keyed by family (A risk · B record ·
   C working relationship · D release and judgement · E method · F remainder).
   Several carry a named tension with an existing requirement — C-06 against
   R-0051, C-24 against R-0028 — that only you can resolve.
4. **Retire the old register — still coupled to the refuser.**
   `docs/requirements/findings.md` §9. Deleting `register.md` does not turn CI
   red; it makes AU7/AU8 **silent**, because `register_check` is a vacuous pass
   when the file is absent, and the live register is validated only by the
   reqview spike, which is not in CI. One ruling: does the new validator
   graduate into `gate.py audit` first, or does the old register stay until it
   does?
5. **The suspect-link stamp still has no slot in the format** — a format change,
   not a fix, because it alters what the fingerprint covers.

**Two open questions inside the `gate-visuals` design**, named rather than
guessed: the **UI concern has no viewpoint** in the 39 types, and **where the
agreed concern list is stored** (front matter is the obvious candidate — the
gates already parse it).

**Closed this sitting** — verdicts against session evidence:

```
  ✓ done   the 38 Whys                      (0 missing; every one his)
  ✓ done   R-0007's uncheckable clause      (approved as written)
  ✓ done   `every` in R-0048                (approved with it; the rule stands)
  ✓ done   twelve statements reworded       (nine live + R-0050 found by scan)
  ✓ done   both parser hazards              (one real and silent, one proven closed)
  ✓ done   gate.py --root                   (7 fixtures; CLI half only)
  ✓ done   the behind-upstream test         (22/22, first fully green run)
  ✓ done   build the view properly          (tools/reqview/editor.py)
  ✓ done   playbook ## Current Status       (split into pointers + history)
  ✓ done   requirement archaeology drafted  (53 candidates, 88 classified)
  · open   retire the old register          (coupled — see 4 above)
  · open   suspect-link stamp               (format change)
  · open   the reset's three questions      (what the requirements system IS,
                                             the draft to final, build-vs-adopt)
  ✗ dead   "no server" as his constraint    (he never said it — struck 08-15)
```

**Still parked by the reset, not cancelled:** closing `model-effort-advisory`
and `hooks-autoload` on the ladder. Do not walk these by hand.

## Backlog

*Ranked by consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**

- **Ground every layer in a standard, not just architecture and requirements —
  his map, 2026-08-22.** Law 4 at the whole-project altitude: *assess and learn
  from industry standards … for every aspect of our project.* Two of four layers
  are already grounded, which is why the other two now look conspicuous.

  | Layer | Standard | Where we stand |
  |---|---|---|
  | **architecture** | **ISO/IEC/IEEE 42010** — stakeholders, concerns, viewpoints, views | **ADOPTED 2026-08-22** in `docs/design/gate-visuals.md`. Its completeness rule *is* the design gate |
  | **requirements / features** | **ISO/IEC/IEEE 29148** — elicitation, writing, structure, SyRS/SRS templates | **ADOPTED** — the plain-language word list and the `each` rule both came from it |
  | | **ISO/IEC 26550** — software product lines, feature modelling, variability | not looked at. This is where *features* as a formal concept actually lives |
  | | **ISO 9241-210** — human-centred design | not looked at. Governs how user needs become requirements — and we have no viewpoint for UI |
  | **process** | **ISO/IEC/IEEE 12207** (software) / **15288** (system) — the reference set of life-cycle processes | not looked at |
  | | **ISO/IEC/IEEE 24774** — guidelines for *describing* a process: purpose, outcomes, activities, tasks | **the nearest analogue to 42010's "how to describe it" flavour.** Kerd *is* a process and describes itself in prose |
  | | **BPMN** (OMG, also ISO/IEC 19510) | the de facto notation. The toolkit has `process` and `swimlane`; neither claims BPMN conformance |
  | | **ISO/IEC 33000** (was 15504, SPICE) · **CMMI** | process capability and maturity assessment |
  | **product** | **ISO/IEC 25010** (SQuaRE) — product quality model: functionality, reliability, usability, security, maintainability | **the live one — see below** |
  | | **ISO/IEC/IEEE 15289** — content of life-cycle information items: plans, specifications, reports, user documentation | this is what `docs/product/`, `docs/design/` and `docs/gates/` are, ungrounded |
  | | **ISO 10007** — configuration management, defining and controlling the product baseline | relevant to what a release *is* |
  | | **ISO/IEC 24748** — the life-cycle management guide tying 12207/15288 together | |

  **His closing observation, which is the design question underneath the map:**
  *"42010's concepts (stakeholders, concerns, viewpoints) are general enough that
  people often reuse them to organize the other layers too."* If that holds, one
  vocabulary covers all four and we do not need four.

  **The one that is already live, and cheap:** `R-0011` is approved and says every
  evaluation carries four summary columns — cost, **quality**, due date, rating.
  **Nothing defines quality.** ISO 25010 is exactly that definition, off the
  shelf, and the evaluation matrix is machine-checked already. That is a small
  adoption against an approved requirement rather than a new project.


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
