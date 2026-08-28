# TODO

## Now

**2026-08-27 — `rung-vocabulary` is ACCEPTED and at `ready-to-release`.** The
first acceptance record this repo has written, and writing it found three live
gaps in the machinery meant to guard it. Kerd is at v0.103.0.
See `kivna/sessions/2026-08-27.md`.

**2026-08-27 evening — work moved to the Mac Studio.** No product work, board
unchanged. Setup audited and three machine-local gaps cleared; the move
checklist is now `docs/machine-setup.md`. Second sitting in the same log.

**Next, in order**

1. **`funnel-driver`'s handoff spec** — `docs/plans/*-funnel-driver-spec.md`.
   Ninth day. Open when it resumes: does slice 2 build `skills/drive/SKILL.md`,
   or only the question set and its checker? Asked, answered yes, never written
   down. Note its two stale sealed views (Backlog, High) belong to this gate.
2. **The `gate-visuals` acceptance gate** — cold eyes, then the expert-user
   pass. Its `Product measurements met` row has no upstream declaration; write
   the gap honestly rather than inventing a target after the fact. Fix its stale
   `visual-lifecycle.html` here, at its own gate.
3. **Frame the measurement item** — Tony's value statement is captured verbatim
   in CONTEXT.md and nothing is framed yet.
4. **The four kept items from the standards spike** — 25010 -> `R-0011`'s
   quality column | 24774 §5.3 header on every `SKILL.md` | the UI viewpoint as
   a build | the spine sentence in `docs/design/gate-visuals.md`.
5. **The archaeology batches** — 53 candidates in
   `docs/requirements/archaeology.md`. C-06 against R-0051, C-24 against R-0028
   are yours.
6. **Retire the old register** — `docs/requirements/findings.md` §9. One ruling:
   does the reqview validator graduate into `gate.py audit` first?
7. **The suspect-link stamp has no slot in the format** — a format change.

**Open, not yet rows:** does re-agreeing a lapsed approval cost anything? If
coming back means re-walking the gate, early gates must not lock at all.
Untested — recorded in the frame as an open question. And: does
diagram-and-prose-together bind as discipline or as a gate refusal? (Backlog row.)

**The reset's three questions stay open** — what the requirements system IS, the
draft to final, build-vs-adopt (`docs/kerd-interview.md`).

**Still parked by the reset, not cancelled:** closing `model-effort-advisory` and
`hooks-autoload` on the ladder. Do not walk these by hand.

## Backlog

*Ranked by consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**

- **`fidelity.py`'s range and its reader set disagree, and the mismatch cuts
  both ways** (found 2026-08-27 at the boundary). `session_range()` anchors on
  the most recent commit that **ADDED** a session log (`--diff-filter=A`),
  deliberately, so the range does not collapse when a session appends to its own
  log mid-sitting. But `newest_log()` reads only the single newest log file. When
  the previous boundary APPENDED (a second sitting on a day whose log already
  existed), the anchor stays behind that boundary and the range spans two
  sessions — while the reader set holds only the newer log. Measured: 22
  artifacts reported unreachable, every one of them named in
  `kivna/sessions/2026-08-25.md`, which was not in the reader set. **And the
  opposite hole is worse:** when a boundary CREATES a log (any first sitting of a
  day), the anchor becomes that very commit and the range collapses to empty, so
  the check passes having inspected nothing — the exact vacuous pass its own
  docstring says the naive anchor caused. Two candidate fixes, neither chosen:
  widen the reader set to every log in the range, or anchor on the previous
  boundary commit rather than on log-file creation. Do not "fix" this by
  exempting — the exemption list is for derived or immutable artifacts.


- **THREE sealed views are factually stale, across two work items** (found
  2026-08-27 by cold eyes; each is its own item's gate work, never another
  slug's slice). `funnel-driver/why-an-umbrella.html` carries a live coverage
  claim over "the funnel's eight stages" and names four retired rungs;
  `funnel-driver/span-vs-slice.html` teaches the retired ladder sequence in its
  lower panel (its TITLE is the time-slice sense and is correct — leave it);
  and `gate-visuals`' `visual-lifecycle.html`, below. Redraw and reseal each at
  ITS OWN acceptance gate: resealing re-keys the evidence that item's producer
  is about to judge.

- **`gate-visuals`' `visual-lifecycle.html` still says "At the goal gate".** The
  sealed view (`fp:3ef85a6441d5`, Tony 2026-08-22) narrates a rung the
  2026-08-25 rename folded into `loop` + `acceptance`. Correct the `<desc>`,
  reseal and re-render the PNG **at `gate-visuals`' own acceptance gate** — not
  from another slug's slice. Ruled out of `rung-vocabulary` slice 1 because
  resealing another item's view re-keys the evidence its producer is about to
  judge.

- **`docs/design/diagram-types-by-rung.md` is still organised by the retired
  rungs.** Slice 1 did the substitution half only. `### BUILD` and `### GOAL`
  must merge into `### LOOP` with `### ACCEPTANCE` beside it, heading order
  re-decided, line 152's quote "The rung's own name" re-checked against the new
  names, and the six `USE · acceptance` type tags re-read against their headings
  — **fishbone** and **loop** were mapped old-`loop` → `acceptance`, which the
  fold makes wrong. All live names, so nothing retired ships; tags and headings
  disagree. Editorial, ruled out of slice 1 on 2026-08-25.

- **Two diagram generators still name the `build` rung.**
  `tools/diagram/gen_flow_build.py` (filename, `Flow` title, step label) and
  `tools/diagram/gen_functions.py`'s two `("BUILD", [` section keys hold entries
  that split across `loop` and `acceptance` under the fold — the same editorial
  merge as the row above, not a swap. Step 12's purity check prints both as
  `deferred` on every run, so this cannot decay into a silent miss.
  **A THIRD was found by cold eyes on 2026-08-27 and fixed** —
  `gen_project_types.py` had the substitutions but not the fold (`= build`,
  `~ goal`, "eight rungs", a stage-left-EMPTY claim), all rendering into
  `project-types.svg`. It was on nobody's list, which is the point: the purity
  check names only what it was told to defer.

- **The `design` gate can check nothing — and as of 2026-08-25 this is live, not
  pending.** `## Scope` moved to the scope gate when slice 1 shipped, so design's
  only check is now one sealed view per *declared* concern —
  and the concerns block is optional. A work item declaring no concerns passes
  design with zero checks. True today too, but slice 1 makes design the only gate
  that can be empty. The question is whether declaring a concern should itself be
  mandatory, which is `gate-visuals`' territory.

- **`## Release condition` will collide with the release-planning artifact.** A
  release is a grouping, not a time axis (2026-08-03), and that artifact has
  never been built. When it is, `## Release condition` on a per-item gate record
  and a release as a set of items both use the word. Filed now so it is a known
  collision rather than a discovered one.

- **`## Grounding` cannot cite an external source.** Found 2026-08-23 when
  `gate.py audit` refused both URLs in `rung-vocabulary`'s own grounding: AU5
  resolves every reference against the filesystem, so a URL is always a problem.
  **Law 4 obliges learning from industry standards and the section that records
  what was read rejects every one of them** — so external reading is recorded in
  prose the machine cannot check. Workaround in use: cite inline in the findings.
  The format owes a slot. **Second bite, 2026-08-25, and it is worse than a
  missing citation:** AU5 resolves file *paths* and never *symbols inside a line*,
  so `docs/design/rung-vocabulary.md` named a function `stage_ahead` that does not
  exist in `kit.py` and `## Grounding` passed clean. A grounding section that
  cannot check what it points *at* inside a line is not only refusing URLs — it is
  silently accepting phantoms.

- **Diagram-and-prose-together: flip the default in the skills.** Decided
  2026-08-23 (CONTEXT.md). One deliverable, two renderings, produced from one
  structure; declining to draw costs a `view: n/a — <reason>`, which
  `kit.py` already refuses without a reason — so this is a default flip, not new
  machinery. **Open, and it sizes the work:** does it bind as model discipline or
  as a gate refusal? Discipline-dependent steps have twice measured at zero in
  this repo, which argues for the refusal — but a refusal needs a rule for what
  counts as prose, and that has no answer yet.

- **Standards grounding — second pass.** The spike (`docs/product/standards-grounding.md`,
  findings at `docs/design/standards-grounding-findings.md`) left three
  surfaced and unread: **ISO/IEC/IEEE 82079-1** (writing instructions — what
  a `SKILL.md` step body is, by 24774 §5.2), **ISO/IEC 25040** (the SQuaRE
  evaluation *process*, which `tools/design/` reinvented), **ISO/IEC/IEEE 24748**
  (life-cycle stages — the `stage:` field and the rung ladder, misfiled under
  product on his map). And 29148 never got the 42010 term-mapping test.
- **The conductor marker cannot carry a sitting's open time, and 2026-08-23 is
  the second and worse instance — the diagnosis is now broader than "planning
  twice".** First bite (2026-08-22): re-entering `plan` overwrote the `execute`
  stamp. Second bite (2026-08-23): the session ran ~08:44–12:17 almost entirely
  in `plan` — a design conversation carried by drawings — so `execute` stamped
  at **12:17**, fourteen minutes before close. Handing that over as the sitting's
  open time would have labelled a four-hour session as fourteen minutes. **The
  real defect: the marker holds one line, so it can only ever report the LAST
  phase, while the open time is a property of the FIRST.** Any design-heavy
  session reproduces this, planning once or twice. Two candidate fixes, neither
  chosen: keep a separate never-overwritten `opened` stamp, or have the boundary
  derive the open side from the session's first machine-written timestamp rather
  than from the marker at all. Owner: conductor's mode-marker section + switch's
  sitting-heading rule. **SIXTH instance 2026-08-25 at ~14 minutes, the smallest yet** (switch-in
  12:13, `execute` stamped 12:27). **FIFTH instance 2026-08-25, ~26
  minutes** (switch-in 07:46, `execute` stamped 08:12) — small because execute
  was reached early. The measured spread is now 14 min · 26 min · 66 min · 157
  min, which shows the defect scales with how long the planning phase runs, not
  with anything random.

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
- **Machine-local state has an inventory but no refuser** (filed 2026-08-27 at
  the Mac Studio move). `docs/machine-setup.md` §4 lists what git cannot carry —
  `kivna/.pair`, `kivna/.active-modes`, `~/.claude/settings.json`, the `~/eolas`
  symlink — and §3 greps for hand-wired hook duplicates that must print nothing.
  Both are prose a person runs, so nothing refuses a machine that drifts. **The
  drift that actually bit was the silent kind:** a duplicate pair hook fires
  correctly and looks like the feature working while injecting text that
  contradicts the live version. Candidate shape, not chosen: a `/kerd:tend`
  category that runs the doc's greps, since tend already owns structural
  convergence and already had its Category 9 rewritten to *remove* stale wiring
  rather than add it. Open question before any build — does this belong to tend
  at all, or is a machine's config outside every repo's business?

- **Stashes and local-equals-remote are unchecked at the boundary.**
- **The playbook's `## Current Status` duplicates CONTEXT.md.** Its stale
  content was fixed this session (v0.90.0 → v0.95.0, three hooks → four); the
  duplication itself remains. Kill it or make it a pointer.
- **Out-of-repo artifacts have no home** — PRs, URLs, decks, external docs.
- **Stop-hook over-prescription**: distinguish work-dirty from
  session-state-dirty at a real stopping point.

**Medium**

- **skriv bans em dashes; the README's What's New voice uses them and always
  has.** Measured 2026-08-25: the v0.98.0 entry runs 0.019 em dashes per word
  and the new v0.99.0 entry matches it exactly. Writing the next entry to
  skriv's rule would make it the only one in the file in a different voice.
  The rule and the house surface genuinely disagree; needs a ruling, not a
  silent split.

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
- **Three vault-spec violations, all kivna's to fix** (tend detects, kivna
  writes — v0.83.0). `Kerd.md` MOC has one broken wikilink: the actual link is
  `[[eloas/Eloas]]`, double-typo'd (this row previously recorded it as
  `[[eloas/Eolas]]`; corrected 2026-08-25) — 16 of 17 resolve. And two files in
  the vault folder are not self-identifying: `discover-sources.json` and
  `2026-08-02-product-to-build.excalidraw`. The spine itself is complete
  (`Kerd.md`, `Kerd Status.md`, `Kerd Weekly.md`).
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
