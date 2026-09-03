# TODO

## Now

**The staleness mechanism is FRAMED** (`85b8683` frame, `920c952` board, CI
green). Slug `question-set-staleness`, work record
`docs/product/question-set-staleness.md`. `gate.py route` reports **enters at
viability**. Nothing was built: no `kit.py` edit, no check, no fingerprint,
`tools/` untouched.

**The value is stated in TWO directions and both bind.** A stale set creates
false confidence and pushes the defect into later work where correction costs
more; and invalidating for unrelated edits so often that freshness becomes noise
makes people ignore or bypass it. A mechanism satisfying only the first is met by
invalidating everything always, only the second by never firing. **Success is
measurable and the producer's:** fixtures proving both directions — relevant
changes refuse, irrelevant stay valid — plus six weeks with **zero stale sets
used** and **zero invalidations dismissed as noise**.

**NEXT, AND IT IS ITS OWN RUNG: viability for `question-set-staleness`.** Four
ledger rows are named and unqualified, so the scope gate refuses all four
honestly. The producer's call at this boundary, 2026-09-02 — *"viability requires
four new producer judgments — including the granularity tradeoff — and should
begin as its own deliberate rung rather than ride the momentum of a finished
task."* **The granularity question is the one that sizes the item:** if the
fingerprint covers whole files, every unrelated edit to `kit.py` or CONTEXT.md
invalidates every set derived from them and the killer risk fires by
construction; if it covers the cited rules, unrelated edits are silent. Row 3 of
the ledger is the hard half — a standing decision is a prose bullet with no
stable anchor, so there may be nothing addressable to fingerprint at all.

**No `## Scope` was written, deliberately.** The smallest increment is the
producer's rung; authoring it at the frame is what the 2026-09-02 deferral was
protecting.

**Do NOT start the five remaining question sets before it** — unchanged. They are
bounded, but writing five artifacts that go stale silently is building the thing
the spike warned about.

**Still blocked, and by their own documents:**

- **`requirements-traceability`** — its design doc carries
  `## The design package — BLOCKED, not yet reworked`. Remainder after a key is
  small: the `--root` invoke side, **0 skills pass it**.
- **`shared-memory`** — 164 lines of annotation plus `## Open at design` with
  three unresolved questions. Only the status word is missing from its journey
  page.

**Unblocked — and NONE of these is mechanical cleanup.** The producer's standing
correction: *"don't treat the acceptance records or legacy closure as mechanical
cleanup; each still requires an evidence-backed key."* An acceptance record is
the producer's **last** gate and a legacy closure asserts an obligation did not
exist — a historical claim that has to be evidenced. Zero Pieces means the build
is done, not that the gate is a formality.

- **`funnel-driver` + `progress-html`** at **acceptance**, 0 Pieces each. Each
  needs an evidence-backed acceptance record and the producer's key.
- **`hooks-autoload`** — the sibling legacy closure named in the same frame
  clause as `model-effort-advisory`. Closing it means evidencing that no design
  rung ever stood in front of it, the way `65a2265` did with two measured facts.
- **`inline-composer` at `handoff`** — spec unwritten; the first real use of the
  mechanism it defined.

**TODO closure review** (this boundary):

```
  ✓ done   — "frame the staleness mechanism"          (85b8683 + 920c952; enters at viability, CI green)
  · open   — "requirements-traceability" · "shared-memory"  (blocked on design work their own docs say is owed)
  · open   — "inline-composer handoff spec" · "hooks-autoload closure"  (untouched)
  · open   — "funnel-driver acceptance" · "progress-html acceptance"  (0 Pieces each)
  · open   — "the three composer-brief clauses need a durable home"  (untouched)
  · open   — "gate-visuals slices 2 and 3" · standards spike x4 · archaeology
  + new    — a Risk ledger section parses prose as rows; nothing distinguishes the two
  ! note   — the board's one text/text overlap moved with the wider board (4824,250 -> 5054,250); already filed
```

## Backlog

*Ranked by consequence x value. See `docs/plans/2026-08-03-choose-what-matters-view.excalidraw`.*

**High consequence**

- **A DERIVED QUESTION SET NEEDS SOURCE-BOUND INVALIDATION PLUS A SCHEDULED
  DISCOVERY REVIEW — the producer's ruling 2026-09-02, recommended and NOT
  built.** The spike proved a viability set derives from gate demands plus
  standing decisions (`docs/design/question-set-derivation-findings.md`), and
  proved the harder thing: **derivation is backward-looking.** A set is exactly
  as good as the decisions accumulated when it was derived, and nothing about
  its own text changes when a new ruling lands. His shape, four elements: the
  exact gate demands and standing decisions it was derived from, named
  individually · a **derivation fingerprint** over those named sources · a
  **refusal condition** — any named source changes and the set is stale, to be
  re-derived before use · a **periodic Law 4 review trigger** for discovering
  relevant new sources that were never named. **Both halves are load-bearing and
  he ruled out the alternatives by name:** re-deriving on every invocation
  *"wastes work without solving the harder problem: an unlisted new decision
  would remain invisible"*, and a date-only review trigger *"is also too weak."*
  **Candidate shape for the fingerprint, not decided:** reuse
  `approval_fingerprint(category, fields)` — the one versioned mechanism, keyed
  2026-09-01 — rather than a second recipe, per the rule-9 lesson. **This is the
  real work, not the six sets** — writing them is cheap, keeping them honest is
  what needs designing. ~~Unframed, no slug: the same invisibility the spike just
  fixed for itself.~~ **FRAMED 2026-09-02 as `question-set-staleness`**
  (`85b8683`) — this row's mechanism is now carried by
  `docs/product/question-set-staleness.md`, which enters at viability. The row
  stays because the mechanism is still **recommended and not built**; it is now
  tracked work rather than an invisible one. Its `## Now` successor is the
  viability rung, where the fingerprint's granularity is decided.

- **`Impact` and `Likelihood` are risk-ledger columns that nothing refuses when
  empty** (measured 2026-09-02 during the derivation). `LEDGER_COLUMNS`
  (`kit.py:61`) declares all eight, and `parse_ledger` checks per row only
  `Evidence` (`:482`), `State` (`:486`), `Countermeasure` (`:492`) and
  `Review trigger` (`:496`). **So the sizing of a risk is structurally
  optional** while the standing decision of 2026-08-03 requires it — *"Qualified
  = proven AND measured: impact in the value's units, likelihood recorded
  separately."* This is the sole reason one of the six derived viability
  questions has no machine citation. Same recurring class: a declared contract
  joined to reality by nothing. Candidate countermeasure, not built: refuse an
  empty `Impact` or `Likelihood` at the viability gate the way `Evidence` is
  already refused — but note it would demand a migration pass over every
  existing ledger, which is why it is a row and not an edit.


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
  CONTEXT.md 2026-08-26/27** — two living sources joined by nothing, where the
  test is *what fails if one side moves?* and the answer is nothing. The
  dangerous direction is the overclaim: a board reader trusting front matter
  believes `hooks-autoload` is two rungs further along than the machine can
  show. **Candidate countermeasure: an AU rule refusing a `stage:` that disagrees
  with the derived rung** — the `check_stage_schema()`/AU10 precedent, which did
  exactly this for gate-record filenames. Not built here; this session flipped
  only its own item's field.

- **Switch-in costs ~17% of the context window — measured, diagnosed, and
  DEFERRED by the producer 2026-09-01.** *"Do nothing for now"* — this repo is
  complex, mid-planning, and losing context is the more expensive error. The
  measurement is recorded here so no later session re-derives it, and **the row
  as first filed blamed the wrong lever (pruning); that framing is superseded by
  what follows.**
  **Where the cost is:** the read set is 250KB — `CONTEXT.md` 177KB (70.7%, so
  **12 of the 17 points**) · the day's session log 37KB (2.5 pts) · `TODO.md`
  36KB (2.5 pts). `## Key Decisions` alone is **97.9%** of CONTEXT.md; every
  other section totals 3.8KB.
  **Growth is two multipliers, and pruning only reaches one.** Bullets went 17
  (2026-07-06) -> 48 -> 74 -> 101 -> **131** today, while the MEAN bullet went
  232B -> 676 -> 919 -> 1,239 -> **1,352B**. Count 7.7x, size 5.8x.
  **The decisive measurement: old bullets do not accrete.** Of the 48 standing on
  2026-08-04, **44 survive and grew 1.01x** (29,376B -> 29,593B) with 4 removed;
  the **87 added since average 1,696B — 2.5x the survivors' 672B — and are 147KB,
  83% of the whole section.** So deleting every pre-August decision recovers 29KB
  (16%) and touches none of the growth. **Pruning is aimed at the wrong
  variable**, which is why two licensed prune events both ended with the file
  bigger.
  **Rate: linear, not compounding.** ~30 new bullets per window, per-window mean
  1,297B -> 2,117B -> 1,695B (inflated once in mid-August, then plateaued). ~5.3
  KB/day, projecting ~250KB in two weeks (~22% of a pickup) and ~320KB in four
  (~26%).
  **Two options were priced and neither taken.** (a) A size budget per decision —
  **refused on the producer's own reasoning**, the argument that got to a ruling
  is the thing the boundary exists to preserve. (b) Tiered loading, his idea:
  deferring the whole Backlog buys **2.2 pts**, and rank-and-read-High-only buys
  **0.5 pts** because High is already 76% of the Backlog — both aimed at the
  2.5-point file. (c) Named but untested: split CONTEXT.md the way 2026-07-03
  split state/work/history, keeping the **ruling** in the loaded file and moving
  the **case** to a reachable record — a full read of a smaller file rather than
  a reduced mode, which `skills/switch/SKILL.md` forbids outright. **Its risk is
  the one this repo has already paid:** `docs/design/conductor-role.md` was
  reachable by name and sat unbuilt for three days, which is why `fidelity.py`
  exists.
  **Return condition:** CONTEXT.md passes **250KB**, or a pickup passes **25%**,
  or the per-window bullet mean resumes climbing — whichever comes first. Until
  one fires, this is an accepted cost, not an open task.

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

- **The composer emits hard-coded absolute repository paths, and a cold review
  pass does not catch them** (measured 2026-09-01 on the
  `requirements-success-measurement` spec). Pass 1 produced 24 of them
  (`/Users/anthonymaley/development/product/Kerd`), the dedicated cold-review
  pass read the whole spec and missed every one, and the amendment inherited
  them and added two more — 26 at review. **This is the same defect handed back
  to the composer on 2026-08-28**, when a reviewer's host had the repo at
  `~/Kerd` and the score assumed this one; it is therefore reproduced, not
  new. A player on another machine, or in a git worktree, follows the score to
  the wrong tree. Fixed in place this time on the producer's call (mechanical,
  no judgment): every block now derives `repo_root=$(git rev-parse
  --show-toplevel)`. **The countermeasure is a brief clause, not a fix:** the
  composer dispatch should forbid absolute paths outright, and the cold-review
  brief should name them as a hunt target. Neither is written down anywhere
  today, which is why the same defect arrived twice.

- **`grep -c` in a fail-fast verify chain fails exactly when it should pass**
  (found 2026-09-01, second instance). The spec's final step ended
  `&& grep -c "^- \[ \] " <spec>` to prove zero unchecked boxes — and `grep -c`
  exits 1 on zero matches, so the `&&` chain aborted on the desired answer.
  Corrected to an exit-safe count (`awk` then `test -eq 0`), tested both ways.
  **Also handed back on 2026-08-28** as one of the same three sibling score
  defects. Two of those three have now recurred, which says the 2026-08-28
  findings were fixed in the artifact and never in the process that produces it.

- **A spec writes the CONSEQUENCE of an open question as settled fact, so
  answering the question falsifies prose elsewhere in the document** (measured
  2026-09-01, twice in one sitting, on the
  `requirements-success-measurement` spec). Step 5's `categories.md` rewrite was
  written assuming `MSC` would be another requirement category, and ruling 1
  falsified it — its own override clause covers only item 1, so items 2 and 3
  stand as written and contradict the ruling. Step 4 stated that a machine
  comparison was *"feasible only under Step 2's ruling (a)"*, and ruling 2 took
  (b) — but the premise was already wrong on its own terms: `kit.py:892` globs
  and parses acceptance records today, so the option was **relocated, not
  eliminated**, and would have been silently dropped by anyone reading the spec
  literally. **Same family as the hard-coded-path and `grep -c` rows above: a
  countermeasure that is a brief clause nobody has written down.** The clause:
  a spec whose steps depend on an unanswered gate must mark those cross-step
  dependencies explicitly, so keying a gate names what it invalidates instead of
  leaving it to be found one gate at a time. Not fixed here — carried into the
  composer hand-back for this item, which is not the same as fixing the process.

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

- **The three composer-brief clauses need a DURABLE home in
  `skills/conductor/SKILL.md` — the producer's ruling, 2026-09-01: two places at
  two times.** *Now* they are explicit acceptance conditions in tonight's
  composer brief (done — dispatched this sitting). *Later*, as **its own scoped
  skill-behaviour change — not inside `requirements-success-measurement`** — they
  land in the composer-brief section (`skills/conductor/SKILL.md:226-249`,
  "Calling the composer" / what the brief carries), **with verification that a
  future score actually carries all three.** The three, as he worded them: every
  repository path derives from `git rev-parse --show-toplevel` · zero-match
  checks remain successful when zero is the expected result · consequences of
  unresolved producer gates are expressed as dependencies or branches, never as
  settled facts.
  **Why this is High and not Medium: it is the generator fix for the three rows
  above, and the defect has now survived being fixed twice.** Two of the three
  sibling score defects handed back on 2026-08-28 came back on 2026-09-01,
  because the correction was written into the artifact and never into the thing
  that produces artifacts. The session log's own insight states the mechanism —
  *a finding fixed in the artifact and not in the generator is a finding that
  will arrive again* — and this is its measured proof. **Verified 2026-09-01:**
  `grep -rn "absolute path\|hard-coded path\|rev-parse --show-toplevel" skills/`
  returns **zero**, so nothing in any skill forbids absolute paths, names them as
  a cold-review hunt target, or requires cross-step dependencies to be marked.
  **Sizing note:** this is a real skill-behaviour change, so it carries the full
  release checklist (version in three locations, README, trigger description) —
  which is exactly why the producer refused to fold it into tonight's sitting,
  per the 2026-08-27 ruling that bumps are not for corrections inside one
  unfinished item. **Cold-review brief is a second surface** and may need the
  same clause: the dedicated cold-review pass read the whole spec on 2026-09-01
  and missed all 24 hard-coded paths — *a reviewer hunting meaning does not see
  form*, which argues the two hunts are separate briefs.

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

- **`CONTEXT.md`'s 2026-08-25 bullet labels both risk checks one rung too high**
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
