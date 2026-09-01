# TODO

## Now

**2026-08-31 — `requirements-success-measurement` passed the DESIGN gate and sits
at `handoff`** (`c01e10d`; GO record `docs/gates/2026-08-31-requirements-success-measurement-design.md`;
`stage: designed`). Three views keyed and sealed on the producer's key —
`condition-anatomy` `fp:fefa90380fe3` · `condition-lifecycle` `fp:0a91dbcac981` ·
`assurance-boundary` `fp:c9b8d06ebfb6`. `gate.py check design` -> PASS, 11 inputs
on disk. See `kivna/sessions/2026-08-31.md`.

**Next for this item: the work specification** — `docs/plans/<date>-requirements-success-measurement-spec.md`
with `## Pieces` and a `**Verify:**` on every step. That is composer territory
and wants a fresh session. **The boundary that still binds:** no build of `MSC`,
no absorption of `rigor-level` slice 2, no edit to `catalog.md`.

**Owed by the design, named in its GO record and NOT built:**

1. `MSC` needs a `categories.md` disposition and schema work, pending a category
   vocabulary review that may find a better term.
2. **Reciprocal link stamping.** Verified 2026-08-31 at `tools/gates/kit.py:1445`:
   the suspect-link stamp is the TARGET's hash stored on the SOURCE, so editing
   the target flags the source and **editing the source flags nothing**. For this
   design the unprotected direction is the dangerous one — a requirement whose
   statement changes leaves its condition measuring words that no longer exist.
3. **Where the `Observed result` lives** — a register category or an external
   evidence artifact. A fourth object either way.
4. **The comparison is unenforced.** Nothing checks whether the reading satisfies
   the target frozen at `KEYED` — the fourteenth assurance line. It is the row a
   machine could most plausibly check once `MSC` exists.
5. **The catalog supersession is RECORDED, not executed.** Its exact in-place
   strike text is in `docs/design/requirements-success-measurement.md`; the edit
   belongs to the schema implementation.

**Next, in order**


1. **The `funnel-driver` acceptance gate** — cold eyes over `94f4304..d318e9e`,
   then the expert-user pass, which is naturally a second real Drive run.
   **Carry the hand-back into that run:** Drive must state the subject in plain
   language when it opens a frame gate, never the slug alone (measured
   2026-08-28 — the producer could not tell whether the questions were about
   the skill or the item). Skill-text change -> composer, next slice, with the
   bump. **Read the `gate-visuals` record first** (`docs/gates/2026-08-30-gate-visuals-acceptance.md`):
   its measurement exception, its frozen-tree stopping rule, and its six-round
   cost are the precedent this gate will be judged against.
2. **`gate-visuals` slices 2 and 3** — the acceptance-gate redraw and
   comparison (starting `db-schema` and `dependency`, the two strong ones), then
   the remaining gates. Slice 1 shipped the design rung only.
3. **The four kept items from the standards spike** — 25010 -> `R-0011`'s
   quality column | 24774 §5.3 header on every `SKILL.md` (only `drive` has it)
   | the UI viewpoint as a build | the spine sentence in
   `docs/design/gate-visuals.md`.
4. **The archaeology batches** — 53 candidates in
   `docs/requirements/archaeology.md`. C-06 against R-0051, C-24 against R-0028
   are yours.
5. **Retire the old register** — `docs/requirements/findings.md` §9. One ruling:
   does the reqview validator graduate into `gate.py audit` first?
6. **The suspect-link stamp has no slot in the format** — a format change.

**Open, not yet rows:** does re-agreeing a lapsed approval cost anything? And:
does diagram-and-prose-together bind as discipline or as a gate refusal?
(Backlog row.)

**The reset's three questions stay open** — what the requirements system IS, the
draft to final, build-vs-adopt (`docs/kerd-interview.md`).

**Still parked by the reset, not cancelled:** closing `model-effort-advisory` and
`hooks-autoload` on the ladder. Do not walk these by hand.

## Backlog

*Ranked by consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**

- **A product doc's `stage:` is checked for LEGALITY only, never against the
  derived route — and it has already overclaimed** (found 2026-08-31 at
  `requirements-success-measurement`'s scope gate). `kit.py` validates the field
  against `STAGES` and stops; nothing compares it to what `gate.py route` derives
  from disk. Measured on three items the same minute: `hooks-autoload` declares
  `stage: scoped` while route says it **enters at `viability`** — a two-rung
  overclaim sitting in front matter; `model-effort-advisory` declares `scoped`
  against a derived `design`; `funnel-driver` declares `designed` against a
  derived `acceptance`. Only the items whose stage was flipped at an acceptance
  record are correct. **This is the repo's own recurring class, stated in
  CONTEXT.md 2026-08-26/27** — two living sources joined by nothing, where the
  test is *what fails if one side moves?* and the answer is nothing. The
  dangerous direction is the overclaim: a board reader trusting front matter
  believes `hooks-autoload` is two rungs further along than the machine can
  show. **Candidate countermeasure: an AU rule refusing a `stage:` that disagrees
  with the derived rung** — the `check_stage_schema()`/AU10 precedent, which did
  exactly this for gate-record filenames. Not built here; this session flipped
  only its own item's field.

- **Drive invented a risk-state value rather than refusing** (found 2026-08-31,
  the durable half of the scope-gate work). Its first real run wrote
  `unqualified — named only, per the frame-gate floor` into the State column.
  The producer's ruling: *"unqualified" is workflow incompleteness, not a durable
  risk disposition* — so `LEGAL_STATES` stays at five and the strings were
  removed, not legalised. **The finding is not the wrong words, it is the
  papering-over.** The frame gate's floor legitimately wants killer risks *named
  but not yet qualified*, and the five legal states cannot express that condition;
  meeting the gap, Drive manufactured a plausible-looking disposition instead of
  stopping at it. It never fooled the machine — `State '...' not a legal value`
  is the identical refusal an empty cell produces — it fooled a **reader**, who
  sees a considered verdict where none exists. Same shape as the `proposed`
  requirement state and the hollow-waiving countermeasure: the honest cheap state
  must be argued for. Open, and it sizes the fix: does the frame-gate floor get a
  legal way to say "named, not yet qualified", or does Drive simply refuse to
  write a State cell it cannot fill?

- **Rule 9 has two implementations and nothing tests them against each other**
  (filed 2026-08-29 at `gate-visuals`' acceptance gate; the claim that there was
  one stood live in `CONTEXT.md` for seven days). `tools/reqview/fingerprint.py`
  is the Python one; `tools/reqview/reqview.py` emits a second in JavaScript into
  the register's HTML (search `function fingerprint`), because that page
  recomputes approval state in a browser with no server to ask — a real reason,
  not an accident. A blind reviewer differential-tested them over 38 vectors:
  **0 mismatches**, with a harmless divergence in whitespace-collapse on six
  exotic characters — Python collapses `\x1c`-`\x1f` and `\x85` where JS does not,
  and JS collapses `\ufeff` where Python does not (counted 2026-08-30; an earlier
  version of this row said three, having named only the ones a reviewer listed). So the recipe is shared
  by inspection and by nothing else: edit one, edit both, with nothing to catch
  you. **Cheapest countermeasure: a test that runs the JS recipe (node, or a
  regex-extracted port) against the Python one over the published vectors, in
  `tests/`.** Until then the module docstrings carry the warning and that is all.

- **`tools/diagram/gen_kerd_map.py:107` says `audit AU1-AU8` — stale by two, and
  it renders** (found 2026-08-29 by the targeted pass). `kit.audit()` runs
  AU1–AU10. The string is baked into `docs/design/kerd-map.svg:182`, which is
  README's first image, so the wrong number is on the front page. Same file also
  says *"CI - eight steps"* against README's nine. **Joins the two rows already
  open on this generator** (it still draws NINE skills, and still names retired
  rungs) — one redraw with a human eye should close all four, not four separate
  text substitutions.

- **A fold has no closing check, and three enumerated sweeps in one session
  each missed sites the last one named** (2026-08-29, `gate-visuals`' acceptance
  gate). The repo's own rule since 2026-08-25 is *a rename gets an enumeration;
  a fold gets a closing check* — and the `build`+`goal` -> `loop`+`acceptance`
  fold still has no check. Measured cost this session: layer 4 blocked three times (17 findings, then 11, then 9),
  the second round finding that the two sealed drawings of ONE work item had
  been left using different words for the thing the gate counts (the file open
  for a different edit was not on the enumeration), and the third finding a
  docstring whose middle had been rewritten to retract a claim its own headline
  still made. **A fourth, targeted pass then caught the countermeasure itself
  committing the defect**: the closing scan was scoped to the eight files the
  earlier findings happened to name — an enumeration wearing a script — and a
  live retracted claim in `CONTEXT.md` sat outside it, one word of paraphrase
  (`has EXACTLY one implementation`) past a literal pattern. A throwaway scan
  written at the gate closed it (unsplit `\n`/`\t` escapes before matching ·
  retired rung names in RUNG-SHAPED positions only, so `the build is wrong` and
  `contract spec` are not false hits · the counted noun · cross-drawing
  vocabulary agreement) and reported zero. **It is a session artifact, not
  machinery.** Candidate home: a `gate.py` check or an AU rule, so it runs on
  every push rather than when someone remembers. `rung-vocabulary` slice 1's
  Step 12 purity scan is the precedent and covers different ground.

- **A work item can reach acceptance having declared no measurable outcome, and
  nothing refuses it** (filed 2026-08-29 by the producer at `gate-visuals`'
  acceptance gate). `docs/design/gate-visuals.md` declares zero stage-1
  measurements, so the acceptance record's product-outcome row had no antecedent
  to check. It was closed as **not assessable** under an explicit producer
  exception rather than by inventing a target after the build — the right call
  for that item, and a precedent that rots into *"declare nothing and pass"*
  unless the gate changes. **The requirement:** future work must declare
  measurable outcomes upstream — or explicitly declare them **inapplicable with a
  reason** — before it can reach acceptance. Same shape as `rigor-level`'s
  hollow-waiving countermeasure: the cheap state is the one that must be argued
  for, and a waiver carries a named reason the machine can check for presence.
  **Likely home: `requirements-success-measurement`**, at viability for exactly
  this question — fold-or-separate is a call for that item's scope gate, not
  decided here.

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


- ~~**THREE sealed views are factually stale.**~~ **CLOSED 2026-08-29.**
  `funnel-driver`'s two were resealed 2026-08-28 (`71391f8`); `gate-visuals`'
  `visual-lifecycle.html` was corrected and resealed at its own acceptance gate
  on 2026-08-29 (`fp:3ef85a6441d5` -> `fp:c4f3e8949191`, producer's eye), and
  `design-gate-check.html` was found stale by cold eyes at the same gate and
  resealed with it (`fp:ccbac6efdb93` -> `fp:d210312a9bec`). The rule the row
  existed to enforce held throughout: each was redrawn at ITS OWN gate, never
  from another slug's slice.

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

- **README's `## What's New (vX)` header is a second home for a fact the entries
  below already carry** (fixed forward 2026-08-30 by the release pass, v0.99.0 ->
  v0.104.0, having drifted five releases). The playbook records this exact class
  in its own `## Current Status` section — *"Two homes for one fact is how that
  happens, so there is now one home"* — and then the README does it one file
  over. Structural fix is to drop the version from the header entirely so the
  newest `### vX.Y.Z` entry is the only home; not done here because changing a
  convention at a close-out pass is the wrong moment for it.

- **Five citation/count slips in the `gate-visuals` acceptance record, filed by
  the frozen-tree review 2026-08-30 and deliberately NOT fixed in that gate**
  (the producer's rule: adjacent wording is filed, not edited, or the cleanup
  creates the next unreviewed tree). None is a false claim about the item, its
  evidence, its sealed views, or tested behaviour. **(1)** exercise 2's quoted
  `now fp:2c5fd12e53c6` is not reproducible by a single-character edit — a
  reviewer brute-forced every insert/delete/append/prepend across six recovered
  content versions with no match; the sibling `6,219 bytes` figure is exactly
  6,207 + 12, so the edit was ~12 bytes and *"one character appended"* is the
  loose part. The mechanism it demonstrates was verified verbatim. **(2)** two
  `tools/gates/README.md` line citations drift by two lines (`:111`/`:253` for
  text at `:113`/`:255`); quotes and substance correct. **(3)** *"all seven gate
  records"* — `docs/gates/` holds 19; 8 mention cold-eyes layers. **(4)** *"four
  cold-eyes gotchas"* in the playbook — 5 bullets reference cold eyes, 4 are
  gotchas proper. **(5)** a sentence about the closing scan reads as if the
  counted-noun check is zero on all four surfaces; it is zero in the two
  drawings, and `aspect` legitimately survives in the two docs as the 42010
  table's own term and in historical narration. Fix on the next touch of that
  record, not by reopening a closed gate.

- **`docs/playbook.md:391`'s cold-eyes trap names the wrong tool — the trap
  itself is ALIVE** (found 2026-08-29 at `gate-visuals`' acceptance gate by two
  reviewers who disagreed; the disagreement is the finding). The line says
  *"gate.py CLI pins root to kit.ROOT — run from any other cwd it silently
  audits the Kerd repo"*. **Half stale, half live, and the live half is worse.**
  `gate.py` no longer pins: it resolves `--root` -> `$CLAUDE_PROJECT_DIR` ->
  nearest `.git` ancestor -> cwd. But `kit.ROOT` is NOT dead code — one reviewer
  claimed it was, having grepped only `kit.py` and `gate.py`; `tools/design/matrix.py`
  references it 10+ times (`:31,33,37,41,60,83,106,108,112,136`), so **every
  `matrix.py` command run from any cwd audits and renders against the Kerd repo**,
  which is exactly the trap the playbook describes, one tool over. Fix the
  playbook to name `matrix.py`, and decide whether `matrix.py` grows the same
  root resolver `gate.py` has.

- **`gate.py`'s root resolver walks OUT of a git worktree into the parent repo**
  (found 2026-08-29 the hard way — a review subagent working in a worktree had
  its `gate.py` call bind to the live tree, then ran `git checkout --` on a file
  there and reverted in-flight uncommitted work; recovered only because the blob
  was still unreachable-but-present in the object store). **Mechanism, verified:**
  `_walk_up_for_git` (`tools/gates/gate.py:106`) tests
  `os.path.isdir(cur/".git")`, and in a worktree `.git` is a **file**, not a
  directory — so the test is False and the walk continues past a legitimate repo
  boundary into the enclosing one. Its docstring promises it "deliberately cannot
  reach the install path", which is true and says nothing about this. Fix: accept
  `.git` as file OR directory. **This is the repo's own recurring class** — a
  boundary asserted in a docstring and joined to reality by a check that does not
  test it.

- **`docs/design/kerd-map.svg` still draws NINE skills** (found by the v0.104.0 release pass, 2026-08-28). `tools/diagram/gen_kerd_map.py:35-45` enumerates the skills by hand and its band is titled *THE NINE SKILLS*; `drive` is absent and the README's first image is that render. A redraw with a human eye on the layout, not a text substitution — left untouched by the pass for that reason.

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
