# TODO

## Now

**Release boundary:** 0.117.0, branch `main`, subject "Release Kerd 0.117.0:
question after the marker and restart recovery", authorized 2026-09-13 12:35;
resolve its revision and remote state with Git. Position, installed state and
the reading set: `CONTEXT.md` `## Where We Are`. Records:
`docs/work/switch-coordinated-closeout/work.md` (compact arrival, coordinated Out,
partner roles, succession, delegation and review dispositions),
`docs/work/codex-plugin/work.md` (0.113.0: package, install, the clarification
scenario), `docs/work/release-111-followup/` (0.112.0). These lists are not
authority to run installation or checks during pickup.

- **First: a fresh Claude In on 0.117.0** (rows 1, 2 and 4 of the shared
  verification list in `docs/work/switch-coordinated-closeout/work.md`).
  Restart Claude if needed; don't assume `/clear` updates the plugin (Anthony,
  12:43). The new session first verifies the loaded skill path reads 0.117.0,
  then runs Switch In: the routing step adopts `kerd-b5-review` from the Out
  designation against the saved `CONTEXT.md` (planned adoption, row 4); the
  arrival puts its one question after END OF PICKUP with NOW numbered (rows
  1–2: Anthony's assessment; "not now" starts nothing). Results go on the rows.
- Then Codex checks the binding and sends the successor one real request that
  arrives (row 4 messaging proof).
- Codex's Out pre-save role ownership check is local and unreleased in five
  files (work record, `### Out pre-save role ownership check — local,
  unreleased`). Reviewed ready; both wording fixes made and confirmed; Codex's
  full Switch regression result not yet recorded. Include it in the next release
  Anthony authorizes; the fresh 0.117.0 In does not contain it.
- Unplanned restart recovery is observed only when a role-holding session is
  actually lost later; nothing is crashed deliberately (Anthony, via Codex,
  12:42). Receipts stop matching when `CONTEXT.md` bytes change.
- DEFERRED until rows 1–5 carry evidence (Anthony, 10:41): a fresh Codex
  Switch In in a work project. Installed Codex Kerd is 0.116.0 (row 5); 0.117.0
  is not installed there.
- Run the behavioural scenario in `docs/work/codex-plugin/work.md` with a
  model, not a fixture: a factual Yes, No or Not sure that grants no approval.
- Coordinated Out with a live contributor on a 0.117.0 cache: observe
  ownership, contributor capture and the MEMORY row. (The 12:43 Out ran from
  the 0.116.0 cache under the repository's 0.117.0 guide, whose Out section is
  unchanged; Codex's account came from the work record.)
- Observe Conductor assigning useful implementation work with owners and edit
  boundaries at a real build (row 6). The 0.117.0 split (Codex built, Claude
  reviewed) was a peer arrangement Anthony set up, not a Conductor decision.

### Earlier launch sequence — retained pending reconciliation

**The launch sequence — `docs/design/launch-plan.md` (five outcomes, 0 of 5).**
Everything below it sits in Backlog as repository-quality debt and stays there
unless the diagnostic pilot surfaces it.

1. **`risk-state-split` — the acceptance record.** The migration SHIPPED
   2026-09-03 as one atomic commit (`e15a0f0`, v0.106.0, CI green at
   `f098ae5`); the item is at **acceptance**, all 14 pieces landed. What is
   left is the producer's last gate: an **evidence-backed** acceptance record
   at `docs/gates/2026-09-03-risk-state-split-acceptance.md` — cold eyes and
   the expert-user pass, never mechanical cleanup (the 2026-09-02 ruling).
   Note the measurement question it must answer honestly: this item declared
   no stage-1 measurement, so the product-outcome row is *not assessable*
   unless one was declared before the build.
   → `docs/product/risk-state-split.md` · `docs/plans/2026-09-03-risk-state-split-spec.md`
2. **`gate-reachability`** — still refusing at **viability, on row 2**, which
   is the intended outcome. Row 1 parses clean under the new schema. Row 2 is
   fatal + `accepted unknown` + empty Treatment evidence, so it refuses
   independently: its narrow `${CLAUDE_PLUGIN_ROOT}` measurement must resolve
   before the item advances, then scope as the producer already stated.
   → `docs/product/gate-reachability.md`
3. **The four newly exposed fatal/accepted-family risks — one per owning
   item, never this migration's** (the producer's ruling, 2026-09-03). Each
   was carried as *accepted* while being fatal, which the one-column schema
   could not express; each now refuses visibly until re-treated:
   `funnel-driver` row 4 · `gate-reachability` row 2 · `gate-visuals` row 1 ·
   `switch-fidelity` row 4.
4. **`agent-request` diagnostic pilot** — begins only after item 2 and the
   cache refresh; its own repository, never inside Kerd; Kerd frozen for the
   run. Subject framed at `~/eolas/vault/kerd/Agent Request Skill Sketch.md`.
5. **Pilot findings** — placeholder only; contents deliberately unknown until
   the run.

## Backlog

*Repository-quality debt: important, and none of it blocks the launch
sequence in `## Now` unless the diagnostic pilot surfaces it. Ranked by
consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**Ladder work — behind the launch sequence, not blocking it**

- `inline-composer` at handoff — spec unwritten; its intended first real use is
  `gate-reachability`'s short spec.
- `hooks-autoload` at viability — the sibling legacy closure, owing its own
  evidence-backed key; its ledger's illegal State is touched by the
  `risk-state-split` migration anyway.
- `funnel-driver` + `progress-html` at acceptance, 0 Pieces each, each owing an
  evidence-backed key. **Do not key `funnel-driver` before the pilot** — its
  acceptance record is the claim that Drive is done, the thing the pilot tests.
- `requirements-traceability` and `shared-memory` at design — blocked by their
  own design docs.
- A FATAL row is told to file into "What we ruled out", whose shape was never
  settled — open in CONTEXT.md `## Open Questions`.

**High consequence**

- **Agent's four disclosed-not-built limits** (Fable foundation review,
  2026-09-11; stated in `native-sessions.md`): a native log rewritten in place
  with its inode preserved passes the replacement guard; the Claude socket's
  peer process is not verified where the native client verifies it; a new
  partner's first contribution and every `codex queue` message travel in argv,
  readable by other local accounts; every Kerd controller sends as
  `kerd-agent`, so a per-sender throttle is shared. Each has a smallest
  correction on record; none is built.

- **A derived question set needs source-bound invalidation plus a scheduled
  discovery review — recommended, NOT built; FRAMED as `question-set-staleness`**
  (`85b8683`, at viability). The mechanism and both refused alternatives are
  in [docs/decisions.md](docs/decisions.md), the 2026-09-02 source-bound-invalidation
  ruling; frame, value statement and ledger in
  `docs/product/question-set-staleness.md`. Candidate fingerprint shape, not
  decided: reuse `approval_fingerprint(category, fields)` rather than a second
  recipe — the rule-9 lesson. Next: viability, where the granularity tradeoff
  sizes the item.

- **`Impact` and `Likelihood` are risk-ledger columns that nothing refuses when
  empty** — STILL OPEN after the 2026-09-03 split, which deliberately did not
  fold it in (that design's call was *separate*). Line citations below are
  **pre-split and stale**; re-measure against the ten-column `parse_ledger`
  before acting. `LEDGER_COLUMNS` declares every column, and `parse_ledger`
  checks per row only `Risk evidence`, `Severity`, `Treatment`,
  `Countermeasure`, `Review trigger` and (at fatal) `Treatment evidence` —
  never `Impact` or `Likelihood`. **So the sizing of a risk is structurally
  optional** while the standing decision of 2026-08-03 requires it — *"Qualified
  = proven AND measured: impact in the value's units, likelihood recorded
  separately."* This is the sole reason one of the six derived viability
  questions has no machine citation. Same recurring class: a declared contract
  joined to reality by nothing. Candidate countermeasure, not built: refuse an
  empty `Impact` or `Likelihood` at the viability gate the way `Evidence` is
  already refused — but note it would demand a migration pass over every
  existing ledger, which is why it is a row and not an edit.
  **Interlocked with `risk-state-split`'s design** — same parser; fold or
  separate is that design's call.

- **THIS ROW IS NOW THE PILOT FOR `requirements-success-measurement`** (chosen
  by the producer 2026-09-01, slug `stage-route-consistency`, framed by Step 12
  of that item's spec — it is still unframed, so nothing yet notices it).
  **A product doc's `stage:` is checked for LEGALITY only, never against the
  derived route — and it has already overclaimed** (found 2026-08-31 at
  `requirements-success-measurement`'s scope gate). `kit.py` validates the field
  against `STAGES` and stops; nothing compares it to what `gate.py route` derives
  from disk. Measured on three items the same minute: `hooks-autoload` declares
  `stage: scoped` while route says it **enters at `viability`** — a two-rung
  overclaim sitting in front matter; `model-effort-advisory` declares `scoped`
  against a derived `design`; `funnel-driver` declares `designed` against a
  derived `acceptance`. Only the items whose stage was flipped at an acceptance
  record are correct. **This is the repo's own recurring class, stated in
  the 2026-08-26/27 entries in [docs/decisions.md](docs/decisions.md)** — two living sources joined by nothing, where the
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
  stopping at it. **The schema half is ANSWERED, 2026-09-03:** the producer ruled that
  "named, not yet qualified" stays represented by **empty** Severity and
  Treatment cells, refused at viability — workflow incompleteness, never a
  legal durable value, so no sixth value was minted. What remains open is
  only Drive's own behaviour: it must refuse to write a cell it cannot fill
  rather than inventing a plausible one. It never fooled the machine — the
  illegal-value refusal is the identical refusal an empty cell produces — it
  fooled a **reader**, who
  sees a considered verdict where none exists. Same shape as the `proposed`
  requirement state and the hollow-waiving countermeasure: the honest cheap state
  must be argued for. Open, and it sizes the fix: does the frame-gate floor get a
  legal way to say "named, not yet qualified", or does Drive simply refuse to
  write a State cell it cannot fill?

- **Waiver and legacy-closure records are named exactly like GO records, and
  only a non-recursive glob keeps them apart** (created 2026-09-02, filed by the
  producer the same sitting). `docs/gates/waivers/2026-09-02-switch-fidelity-design.md`
  and `docs/gates/closures/2026-09-02-model-effort-advisory-design.md` both match
  `GATE_RECORD_RE` cleanly — **verified, the regex returns a match** — and the
  only thing stopping either being read as a passed design gate is that `AU3`
  and the design-GO glob look directly under `docs/gates/` and do not recurse.
  **This is the repo's own recurring defect class, freshly created:** two things
  distinguished by convention alone, where the test is *what fails if one side
  moves?* Make any gates discovery recursive — an entirely reasonable future
  change — and two items silently report a design gate that never happened, with
  nothing going red.
  **The durable fix, as the producer specified it: type-distinct filenames, plus
  a refusal test proving a waiver or closure record can NEVER satisfy a GO
  lookup, even if discovery later becomes recursive.** The test is the load
  bearing half — a naming convention with nothing checking it is exactly what
  this row is about. Home for the test: `tests/`, or a `gate.py` selftest case
  alongside the existing 51.
  **Both existing files are MIGRATION CASES, not examples to copy.** Neither was
  renamed in the sitting that created them: they are keyed records and renaming
  a keyed record is a producer decision, not a tidy-up. The fix must migrate
  them explicitly rather than leave them as the two instances that predate the
  convention.
  **Why it was not fixed on the spot,** recorded because the reasoning
  generalises: *"The three intended outcomes are safely landed; extending an
  already seven-hour sitting into record-schema design is the wrong risk."*

- **The suspect-link stamp has no slot in the requirement format** — a format
  change, carried out of `## Now` on 2026-09-01. Narrowed twice that day: the
  stamp's RECIPE is settled (category-aware, one mechanism), and **reciprocal
  stamping is no longer owed** — Step 3 was keyed the same evening and builds it
  for Requirement <-> `MSC`. **What remains open is only the block shape:** where
  the stamp is written, and now where the SECOND (reverse) edge is written, since
  ruling 3 requires two stored edges where the grammar has always had one.

- **An observed result binds to its METHOD by bare reference, never by version —
  filed by the producer 2026-09-01 at the D6 check-6 correction, deliberately NOT
  built in this slice.** The immutable acceptance-record entry binds to its `MSC`
  by the **exact frozen fingerprint**, so a condition that moves after acceptance
  makes the record visibly diverge. It binds to its **method** by bare `TST-nnn`.
  Check 6 was corrected the same evening to require **resolution** — the ID must
  resolve to an existing register block whose category is `TST`, not merely match
  `^TST-[0-9]+$`, because *"a phantom method would make the observed result
  unverifiable and therefore NOT ASSESSABLE."* **But resolution is not sameness.**
  A `TST` block can be edited after the reading was taken; the record still
  resolves, and the historical evidence now cites a method that has moved, with
  nothing diverging. **Same family as the suspect-link-stamp row above:** a stored
  reference proves existence, never that the thing referenced is what was judged.
  **The producer's boundary, and the reason this is a row rather than a contract
  clause:** *"the sealed design requires a method reference, not a frozen method
  version. Whether historical evidence must bind to the exact keyed TST version is
  a legitimate follow-up integrity question, but it should be filed rather than
  silently added to this contract."* So **no `Method-SHA256`, no stamp on the
  method edge, and no version-pinning ships in this slice** — the composer was
  bounded explicitly against adding one.
  **Candidate shape if it is ever taken, not decided:** reuse
  `approval_fingerprint(category, fields)` — the one versioned mechanism with
  artifact-specific canonical payloads, keyed 2026-09-01 — rather than inventing a
  second recipe, which is the rule-9 lesson (two implementations tested against
  each other by nothing). **Open question that sizes it:** does an immutable record
  owe a frozen pointer to EVERY living thing it cites, or only to the one whose
  movement changes the verdict? The `MSC` moving changes whether the target was
  met; the `TST` moving changes how it was measured, which may be a weaker claim.

- **A visual of where the whole process build-out stands — asked for by the
  producer 2026-09-01, deferred the same minute.** Two readings, recorded so the
  next sitting does not re-derive the ambiguity, and they are different drawings
  from different data. **(a) The board:** 28 slugs against seven rungs — already
  derived at `docs/plans/progress.svg`, CI-stale-checked, and dense; the renderer
  currently reports one text/text overlap in it (`requirements-project-type-templates`
  over `requirements-success-measurement` at 4594,250). **(b) The capability:**
  how much of Kerd's own process — ladder, gates, refusers, skills — is built vs
  designed vs still prose. **No artifact on disk answers (b) today**, which is
  why it is filed High rather than as a rendering chore. Ask which before
  drawing. Whatever is drawn must be derived from disk, per the standing rule.

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
  2026-08-23 ([docs/decisions.md](docs/decisions.md), diagram-and-prose ruling). One deliverable, two renderings, produced from one
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
- **`hooks-autoload`'s product doc is uncorrected** — its ledger and acceptance
  test still carry the pre-verification case, and the item still enters at
  viability (sub-finding kept open when the verification row was archived
  2026-09-12; see `docs/backlog-archive.md`).
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
- **Requirement archaeology over the then-74 standing decisions, now in [docs/decisions.md](docs/decisions.md).** Framed
  work, never ad-hoc, and **never from session logs** (see the decision in
  docs/decisions.md, requirement-archaeology ruling). Provenance must be marked permanently or the register becomes
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

- **Stashes and local-equals-remote are unchecked at the boundary.** Evidence
  arrived 2026-09-06, handed off by the apple-music session (`apple-music-78`,
  approved at that session's plan gate — reported, not verified here): on
  2026-09-02 its Switch Out banner passed three times over 53 commits that no
  remote had reached. The mechanism is in Kerd's own text —
  `skills/switch/SKILL.md:246-261` proves the boundary with `git status` +
  `git log -1`: `Tree: clean` tests uncommitted work, `Pushed:` is a claim
  about a command's output, and the log header's `**Tracking:**` line is
  model-written. A *failed* push already stops (`:261`); an unverified one does
  not, and nothing fetches or checks containment on the way out —
  `hooks/session-start.sh:21` checks only the inbound direction (remote ahead
  of local). A working countermeasure exists outside the repo, verified
  read-only: `~/eolas/vault/kerd/bin/boundary-check` (v3, 2026-09-02) fetches,
  then exits 1 on a failed fetch, a HEAD no remote ref contains, or a dirty
  tree, on every repo passed to it, with no success bypass
  (`BOUNDARY_LOCAL_REASON` prints as an unverified operator assertion; the exit
  stays 1). apple-music's CLAUDE.md carries the override ("Switch-out is not
  complete until BOTH repos pass the mechanical gate"). The ask as handed off:
  Switch Out runs it on every repo the boundary owns and refuses the ✓ banner
  while it fails. **Decision owed to the producer:** fold it into switch step 7
  as a required evidence line, promote the script into `tools/` or a hook, or
  frame it as its own item. Same class as `check_stage_schema()`/AU10 — a
  prose rule that did not grip, replaced by a check that refuses.
  **Narrowed 2026-09-11:** Agent's `handoff.py save` verifies the remote carries the
  exact commit, but Switch Out itself still does not — `(done? — confirm)` is not
  warranted; the row stays open.
- **The playbook's `## Current Status` duplicates CONTEXT.md.** Its stale
  content was fixed this session (v0.90.0 → v0.95.0, three hooks → four); the
  duplication itself remains. Kill it or make it a pointer.
- **Out-of-repo artifacts have no home** — PRs, URLs, decks, external docs.
**Medium**

- **A `## Risk ledger` section parses PROSE as rows, and nothing distinguishes
  the two** (found 2026-09-02 while framing `question-set-staleness`).
  `parse_ledger` treats every non-empty line in the section body as a row, so an
  explanatory paragraph placed under the table reported as `row 5: expected 8
  columns, found 1` through `row 12` — eight phantom rows, inflating the scope
  rung from `need 9` to `need 17`. **The refusal is loud but misdirected:** it
  names row numbers that are not rows, so the natural reading is a malformed
  table rather than parsed prose. **Same family as the fence-aware fix of
  v0.83.1** (`2a0ea4a`), which taught the structural parsers that lines inside a
  fenced block are content and not structure — this is the inverse case, prose
  outside a fence sitting inside a structured section. **Candidate
  countermeasure, not built:** stop parsing at the first line that is not a
  table row, or refuse non-table content in the section with a message that says
  so. Either is a parser change and belongs to its own rung; mirrored to
  `docs/playbook.md` as the durable net meanwhile.

- **The 2026-08-25 risk-check bullet, now in [docs/decisions.md](docs/decisions.md), labels both checks one rung too high**
  (found 2026-09-02 by the derivation spike). It reads *"viability requires
  killer risks named … scope requires every row qualified."* Under
  `tools/gates/README.md:42` — *"a rung's exit is the next rung's entry; it is
  the frame gate's input, not viability's"* — and the 2026-08-28 ruling that a
  check's reader-facing name wins over its code location, killer-risks-named is
  the **frame** gate's input and every-row-qualified is the **viability** gate's
  input. Conductor's own frame rule already says the frame carries the killer
  risk, so the skills agree and the standing decision does not. **The machine
  description in the bullet is accurate; only the rung names are wrong.** Filed
  rather than edited — it is a keyed tree and the standing rule is *file, don't
  edit*. **Why it is not cosmetic:** standing decisions are one of the two legal
  citation sources for deriving a question set, so a derivation citing this
  bullet naively files its questions against the wrong rung.

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
- AGENTS.md needs its own verdict: gitignored, machine-local, stale Codex-era fork.
- Regenerate the choose-what-matters view before its next use.
- PR-event edge in the stale CI step (unexercised; no PR flow).
- **lorg-cut candidate** — evidence check per the rip discipline before any
  license. **Interrogate rides the same review** — and note it now has a second
  caller: requirement qualification is the same shape as risk qualification.
- **kivna verdict** — same zero-usage smell as the vault; import/export
  confirmed unused.
- **CI rule for the single-definition law** — nothing machine-enforces
  "conductor never re-describes a Switch Out step".
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
