# Backlog archive

Backlog rows closed at Switch Out, each with its verdict, the evidence and the date; and
position paragraphs moved out of `CONTEXT.md` when they stopped being current. Nothing here
is edited after it lands. Started 2026-09-11 at the first run of the lean-start step (v0.111.0).


## Closed 2026-09-24 (day)

**Verdict: done — fixed in 0.151.1 and seen once in a real run; evidence in
`kivna/sessions/2026-09-24.md` ("Day sitting").** The four lines now describe the unexpanded
form instead of spelling it out; a test scoped to Tend and Slainte guards them. A headless
0.151.1 Tend in a scratch repo flagged a literal-placeholder settings entry and kept an
unrelated hook (12:58). One observation.

- **`tend` and `slainte` name the plugin placeholder literally, and Claude Code
  fills it in.** Measured 2026-09-18: `${CLAUDE_PLUGIN_ROOT}` in SKILL.md text
  is replaced by the install path at load. `skills/tend/SKILL.md` :213, :217,
  :241 and `skills/slainte/SKILL.md` :104 mean the literal placeholder (e.g.
  "a bare `${CLAUDE_PLUGIN_ROOT}/hooks/` path"), so the model likely reads a
  rewritten instruction. Not yet observed in a real tend run.

## Closed 2026-09-24 (morning)

**Verdict: done — seen in real use; evidence in `kivna/sessions/2026-09-24.md` ("Morning sitting").**

- **Watch 0.150.0's heading in the first real arrival after each install.** Claude Code: this
  sitting's Switch In heading read "KERD · SWITCH IN COMPLETE ✓ · Kerd 0.150.0" (08:2x).
  Codex: after Codex was brought to 0.150.0 (`codex plugin list --marketplace kerd-core`
  read 0.150.0 at 08:48), Anthony reported the fresh Codex arrival "its working"; Claude did
  not see that line itself. The Codex pickup trial it came from passed 2026-09-23 (Seinn).

## Closed 2026-09-23 (night)

**Verdict: done — the hold is lifted; evidence in `kivna/sessions/2026-09-23.md` ("Night sitting").**

- **The 2026-09-13 10:41 hold ("prove Kerd first").** Rows 3 and 5 of its verification list,
  open since 2026-09-13, closed this day: row 3 at 17:40 (a fresh Switch In recovered both
  accounts from the records alone), row 5 at 18:19 (Codex on 0.149.1, a fresh Codex session
  reported loading it). Anthony lifted the hold at 18:19 ("y"). The ruling is in
  `docs/decisions.md`; the deferred Codex pickup stays open in `TODO.md` as its own row.

## Closed 2026-09-23

**Verdict: done — fixed and released this day; evidence in `kivna/sessions/2026-09-23.md`.**

- **See the new job names in the running-job list (0.147.0 watch item).** Seen: on
  2026-09-23 17:28, with 0.149.0 installed, Anthony's running-job list read
  `kerd:sonnet-high` for a dispatched read-only job ("it shows kerd:sonnet-high").
  Sketchbook: `docs/work/job-label/work.md`.

- **Show the model and effort where a running job is listed (asked 2026-09-19).** The list
  shows only the agent name, so the fix was the name itself: `kerd:<model>-<effort>` and
  plain `kerd:haiku`, released in 0.147.0. The row's own plan, leading each dispatch
  description with the pair, was checked and would not have shown. The new names are not
  yet seen in the list; that is carried as a watch item.

## Closed 2026-09-22

**Verdict: done — each fixed and released this day, with its evidence in
`kivna/sessions/2026-09-22.md` and the release notes.**

- **The site tells the musical story now (2026-09-22).** The hero names the shape, a new
  band defines rehearsal and the concert before the pieces use them, the capabilities
  intro defines them for a reader arriving from the nav, and the README opening matches.
  Docs and examples were left alone: their few mentions explain themselves. Sketchbook:
  `docs/work/site-musical/work.md`.

- **The image-by-path route now has Claude evidence too (2026-09-22).** A fresh read-only
  Claude worker on Sonnet 5 read a PNG from its absolute path and answered three
  picture-only questions correctly. Still untested on Claude: an established partner
  rather than a fresh worker, and a file outside the project.

- **Pictures at a laptop width: fixed in 0.144.1.** Measured 2026-09-22 at 1440, 1280 and
  1152: the site now stacks below 1200px (labels 26px), 1201-1280 stays two-column at 14px,
  and the concert picture's smallest type went 28px to 32px. Phone widths stay unmeasured.

- **Release notes live in two places, now with a check.** `tools/release_check.py` (CI,
  every push) refuses a version whose note differs between `README.md` and `CHANGELOG.md`,
  or a version in the README and not the changelog; older entries the README trimmed are
  allowed. Each release still updates both by hand.

- **The stale-reference row is closed (2026-09-22).** The Codex core guide no longer
  pins 0.113.0 in its example paths and now says eight skills with four excluded by name;
  the state contract, machine-setup and playbook were corrected in 0.144.1.

Evidence: 0.144.1 (pictures, measured at 1440/1280/1152), 0.145.1 (Claude read a PNG from
its path), `f652a52` (CI refuses a release note that reads two ways), `4a89ee1` (the Codex
core guide), `ec5df1a` and `4e5d4bc` (the site's musical story).

## Closed 2026-09-21 (evening): the site and README tell one story

**"Fix the six places where the live site and the README contradict each other" — done.**
Re-checked against the live pages first, then settled against what Kerd does, both copies
corrected, Codex clear on first read, pushed as `8ff2196` on Anthony's "yes"; the live pages
were checked byte-identical to the repo afterwards. Two further wordings found on the way were
fixed the same evening: the Codex guide's skill count (`2816c9c`) and the host line (`927d46d`).
Evidence: `docs/work/front-page-claims/work.md`, section "Follow-on: the six site/README
contradictions".

## Closed 2026-09-21: the rest of the front page was checked, and the site went live

**"Check the rest of the front page the way the install was checked" — done.** A cold
reader classified 55 claims on README lines 1–224, the site was opened in a real browser at
two widths, and the trial route and a pinned-rollback install were run in a throwaway
profile. Four claims were wrong. The worst: the rollback section pinned to `716a099`,
whose manifest carries the SSH address 0.142.1 removed, and no environment variable
rescues it. Corrected in `1f8e8f5` after three Codex rounds, two of which blocked
overstatements in the rollback paragraph. Evidence: `docs/work/front-page-claims/work.md`.

**"`--plugin-dir` is not footprint-free, and the README says it is" — done.** Measured: a
session through it writes a `pluginUsage` row even when it does nothing, and `plugin list`
shows the installed copy still enabled beside the local one. The README, site and
getting-started guide all corrected in `1f8e8f5`.

**"Small picture labels fall near 8px at phone width" — closed as the wrong question.**
Measured at 390px: every label in every picture under 12px, worst 6.96px, worse than the row
said. But Anthony ruled on 2026-09-21 that Kerd's readers are on desktops and laptops, and at
1440px every label clears 12px. What remains, a laptop window narrower than 1440, is a new
narrower row in `TODO.md`.

**"Palette drift, upstream only" — obsolete.** The drift was in diagram-design's installed
Krutho working copy (a dark-mode accent still orange). That copy was replaced on 2026-09-21
by the `kerd` profile in both installed versions; the drifted copy is backed up at
`~/.diagram-design/profiles/krutho.md.bak-working-copy-2026-09-21`.

## Closed 2026-09-20: the install commands were run for the first time

**"The package's unverified claims: the install commands" — done.** The two commands the
README prints were run from scratch on 2026-09-20 in throwaway profiles, with a GitHub key
available and with SSH refused. The second command failed for the keyless case: Kerd's
manifest published an SSH source. Fixed and released as 0.142.1, then proved by a keyless
install against the live marketplace, which returned all eight skills at 0.142.1. Evidence:
`docs/work/first-install/work.md`, `kivna/sessions/2026-09-20.md`, commit `db97b78`.

**"Observe 0.140.0's report shape and the plain Who grid in real use" — done, first
sighting.** The 2026-09-19/20 sitting ran on the 0.142.0 cache rather than 0.139.0, so the
shape was live for about a dozen reports and held. One strain recorded: a report carrying a
result and a correction together wants more than five items. Kept open as a wording
question in `TODO.md`, not as an unobserved item.

**"Observe the risks rule in real use" — done, first sighting.** Three risks were written
into the sketchbook unprompted at Shape, each with what was being done about it, and read
back at the close with each disposition. Nothing invented to fill the list.

## Closed 2026-09-19, evening: the ladder retired

Anthony ruled on 2026-09-19 18:48 that nobody wants a machine that refuses their work and that
this level of risk ledger is not needed. 0.141.0 removed Drive, Lorg, Interrogate and Pair;
0.142.0 removed the check tools, the requirements register tools, the design matrix, the
progress board, the diagram generators, the handoff fidelity check and Conductor's step check.
Evidence for every row below: those two release commits on `main`, and
`docs/work/retire-four-skills/work.md`. The old records the rows point at remain in place as
unpoliced history.

- **Verdict: done. Drive was removed from the plugin in 0.141.0 (2026-09-19) with Lorg, Interrogate and Pair. Conductor carries work across sittings; Drive's frame-gate intake went with the ladder in 0.142.0 and was not carried over, by Anthony's ruling that nobody wants that machinery.** The row as it stood:
  - **Remove the Drive skill: Conductor replaces it** (ruling 2026-09-18 13:08,
    `docs/decisions.md`). Its own release: `skills/drive/`, README, both capability
    lists, cross-references, and the tests that count twelve skills. Anything Drive
    does that Conductor lacks, such as frame-gate intake, is named before removal
    rather than lost.

- **Verdict: done. `CHANGELOG.md` was revived on 2026-09-19 with the product package and has carried every release since (0.140.0, 0.141.0, 0.142.0); the README and the changelog are both updated at each release.** The row as it stood:
  - `CHANGELOG.md` stale at 0.14.0 while the repo is at 0.95.0, and absent from
    the release checklist. Revive or delete.

- **Verdict: done, overtaken. The pair hook was removed in 0.141.0, and the question-formation rule already stands in the owner's global instructions (seen loaded in the 2026-09-19 evening session).** The row as it stood:
  - Consider promoting the refined question-formation rule from the pair hook into
    global `~/.claude/CLAUDE.md`.

### Dead: 43 rows that were debt against the retired ladder, ledger, register or their tools

Verdict for each: **dead**. The thing the row would have repaired, checked or built on no longer
exists or is no longer policed. Moved verbatim, in their Backlog order.

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

- **The refusal surface does not travel with the plugin — the return condition
  FIRED 2026-08-07.** It was accepted "for now" with the trigger *"the first
  time Kerd's ladder is run in a repo that isn't Kerd"*; declaring requirements
  traceability a capability for consuming projects is that moment. Now
  interlocked with the `--root` row above.

- **Revisit the journey view when more data exists** (parked 2026-08-05, shape
  agreed on mock v4).

- Regenerate the choose-what-matters view before its next use.

- PR-event edge in the stale CI step (unexercised; no PR flow).

- Derive the rigor refusal messages from `RIGOR_LEVELS` via join.

- Gate records can only say GO: a refused gate has no dated home.

## Closed 2026-09-19

- **Observe 0.139.0's rehearsal and concert in real use — done.** The product package was
  rehearsed and performed 2026-09-18 23:26 to 2026-09-19: sketchbook kept unprompted,
  Ready from Conductor's side, three batches, twenty dispatches observed on the requested
  model and effort, the goal check reopened two failed goals. What was not exercised and
  what was found (rolling without publishing) moved to `TODO.md` `## Now`. Account:
  `kivna/sessions/2026-09-19.md`.
- **lorg-cut candidate, with Interrogate riding the same review — ruled, 2026-09-19.**
  Anthony cut Lorg, Interrogate and Pair; the evidence check was overtaken by his ruling.
  Case: `docs/decisions.md`. The plugin removal is the selected next in `TODO.md`. The row
  as it stood: "lorg-cut candidate — evidence check per the rip discipline before any
  license. Interrogate rides the same review — and note it now has a second caller:
  requirement qualification is the same shape as risk qualification."
- **Refresh the plugin to 0.139.0 — done** before the 2026-09-18 23:26 sitting; that
  session loaded 0.139.0 from the cache.

## Position paragraphs moved out of CONTEXT.md, 2026-09-16 (evening)

These were current while 0.131.0 and 0.132.0 were the boundary. Moved here unchanged
when 0.133.2 became the boundary and the lean-start measurement ran over target.

- **0.131.0**: a native picker may follow the speech bubble, never replace it; Agent's
  missing partner role offers four shortcuts. This withdrew 0.129.0's "no native
  pickers", which was Claude's over-reach defended by a *passing test* for two releases.
- **0.132.0**: visuals by default and the decision capsule, combined. The visual
  threshold is countable — two or more connected parts, a branch, an ownership boundary
  or a before → after change — because "substantial" carries no test a model can fail.
  Both rules behaviourally evidenced; see `docs/work/visual-communication/work.md`.

**The finding worth carrying: the defect was a class of sentence, not one sentence.**
Seven were closed across three files, each reading like discipline while handing the
model an unfalsifiable judgment about its own work ("only if it clarifies a real
relationship", "whenever they help", "when it helps", "a substantial proposal",
"Optional job/diagram tools", the inline-sketch licence). Static gates were green the
whole time all seven were live.

**Evidence went wrong twice before going right**, and the corrections are recorded, not
buried: the first behavioural design had no control arm; the second was scored off disk
while workers were still running and produced a reported failure that did not exist.
The third used three arms isolating each rule, byte-identical prompts, and criteria
fixed in writing before the last runs reported. Method, not just result:
`docs/work/visual-communication/work.md`.

## Closed 2026-09-16 (evening)

**Verdict: done — 0.133.0 released, `7cf5782` on `main`, CI entry gate green.** The
explicit-model dispatch contract: every native Claude `Agent` call names `model` and
`subagent_type`. Evidenced by one mixed-model fan-out (`haiku`/low, `sonnet`/medium,
`opus`/high in a single dispatch, observed `claude-haiku-4-5-20251001`,
`claude-sonnet-5`, `claude-opus-5`; the Haiku job returned no effort records, so its
effort is unverifiable). Reviewed by an Opus job (eleven findings) and Codex across
three before-push rounds. The row's earlier design — a `PreToolUse` hook, matcher
framework and model×effort matrix — was **refused by Anthony at 16:48** and is dead,
not deferred: see the ruling in `docs/decisions.md`. Record:
`docs/work/model-dispatch-guard/work.md`.

**Verdict: done — both installations updated, 2026-09-16 evening.** Claude's plugin
cache moved 0.132.0 → 0.133.0 (`claude plugin marketplace update` then
`claude plugin update kerd@kerd-marketplace`; applies on restart). Codex moved 0.129.0
→ 0.133.0: `output/kerd-codex-0.133.0` built from source, the `kerd-core` marketplace
re-pointed at it, `codex plugin add kerd@kerd-core` reporting `installed, enabled
0.133.0`. The row had been open since 0.130.0 with neither side current.

**Verdict: done — the CI/test-path defect, fixed across 0.133.1 and 0.133.2.**
`skills/switch/scripts/tests/test_roll_control.py` imported its siblings above its own
`sys.path` inserts, so the suite could not be invoked by dotted module name; both
inserts now precede every local import and the suite runs green with no `PYTHONPATH`.
`tools/run_tests.py` collects `skills/*/scripts/tests/test_*.py` by path, and
`.github/workflows/gate.yml` now runs it plus the hook tests — **CI had run none of the
730 tests before this**. Its first real run went red and found a second defect, fixed
in 0.133.2. **One part stays open and has moved to `TODO.md`, not closed here: which
`patch.object(agent, 'RPC', ...)` site leaks was never diagnosed.**

## Closed 2026-09-15

**Verdict: done — both real-build slots recorded 2026-09-14.** Builds 1 and 2 (a
consumer project on 0.126.0, non-code notes and a composer-route packaging build) are in
`docs/work/conductor-clean-entry/composer-restoration-comparison.md`. They are read from
source, reviewed by Codex, and assessed met, unmet or unassessed. The unmet findings
were fixed in 0.127.0.

- **Then: observe the next two real multi-step builds on 0.126.0** and fill the two
  slots in `composer-restoration-comparison.md`: the route Conductor chose, composer
  calls, delegation share and fan-out, returned-diff reads, failure routing, and a
  visible controller model/effort assessment.

**Verdict: done — released in 0.127.0 (2026-09-15).** Pairing asks once for role
and review cadence; Conductor plans review from it or offers once. Design, four Codex
before-push rounds and evidence: `docs/work/review-and-fit-corrections/`.

- **Proposed correction: Conductor offers reviews itself** (Anthony, 2026-09-14
  20:10 and 20:14): ask once how reviews run, store it with the pairing, plan from it.

**Verdict: done — released in 0.128.0 (2026-09-15).** Five `kerd:effort-<level>`
agents set a delegated Claude job's effort. `job_evidence.py` observes what ran. A probe
observed `kerd:effort-low` as Sonnet 5 at `low`. Record:
`docs/work/effort-sized-players/`.

- **Next release: effort-sized Claude players** (Anthony, 2026-09-14 23:55).

**Verdict: superseded — by bringing the plugins to 0.128.0 (current `TODO.md`).**
0.127.0 and 0.128.0 were released after this row.

- **First (proposed): bring the installed plugins to 0.126.0.**

**Verdict: superseded — the fit gap is fixed and the mangling is probably display
(one paste).** The grids in that 0.126.0 session were well-formed Markdown at source.
Anthony's pasted table was box-drawn by the client, which supports display or paste
as the cause, from one paste, not verified against the exact transcript Codex meant.
The missing controller fit assessment is addressed by 0.127.0's required Fit line.

- **Check the Conductor staffing grid in the original work-anthony transcript.**

## Closed 2026-09-14

**Verdict: done — observed 2026-09-13 16:08 EDT by the Claude session that adopted
`kerd-b5-review`.** That session's loaded skill path and `plugin.json` read 0.119.0;
`identity` matched, `adopt --expected-session … --record CONTEXT.md` consumed the
designation and wrote the recovery receipt against unchanged `CONTEXT.md` bytes;
`arrival` showed TEAM and returned the first live notice to `codex-tui` as
submitted-unconfirmed. The 0.119.0 layout it assessed was itself replaced the same
evening (0.120.0, no YOU box). Evidence: `kivna/sessions/2026-09-14.md`.

- **First: a fresh Claude In on 0.119.0** (rows 1, 2 and 4 of the shared
  verification list), with routing adoption and the first live arrival notice.

**Verdict: superseded — replaced by the two real-build observation slots in
`docs/work/conductor-clean-entry/composer-restoration-comparison.md`.** Delegation
was redesigned three times since (0.124.0 task assessment, 0.125.0 composer/score
restoration, 0.126.0 Conductor-written steps); observing "useful implementation
work with owners and edit boundaries" is now part of those slots.

- **Observe Conductor assigning useful implementation work with owners and edit
  boundaries at a real build (row 6).**

## Retained position, 2026-09-13 (moved from `CONTEXT.md` at the 2026-09-14 Out)

The 0.119.0 position paragraphs, no longer current: installed state and routing
sequence as they stood at the 2026-09-13 15:31 Out.

**Installed state, not to be overclaimed:** the 13:51 Claude session loaded the
0.118.0 cache (skill base path and `plugin.json`, observed once); no session has
been observed loading 0.119.0, and publication does not update a plugin cache.
Installed Codex Kerd is 0.118.0 (row 5, reported by Codex 13:30); no Codex
update to 0.119.0 is authorized. Verify the loaded skill path and version before
counting a result.

**Where the sequence stands at this save:** the 13:51 session adopted
`kerd-b5-review` at 13:52 from the 12:43 Out's designation against the unchanged
saved record (row 4's planned adoption), then took seven real requests from Codex
on that binding, all answered (row 4's messaging proof). It ran this Out on the
0.118.0 cache: the ownership check matched, and the contribution checkpoint
requested Codex's delta since the release, which returned "none". After the save
it designates its successor against this file with
`skills/agent/scripts/agent.py handoff --record CONTEXT.md`. Anthony then
restarts Claude so the plugin can load 0.119.0 (`/clear` is not assumed to
update it). The fresh session: verify the loaded skill path reads 0.119.0; Switch
In's routing runs `identity`, then `adopt --expected-session <the currently bound
ID> --record CONTEXT.md`, then 0.119.0's `arrival --provider claude --self-alias
kerd-b5-review` (its default recipient on Kerd is `codex-tui`, by a metadata-only
check); the arrival shows TEAM and the notice outcome for Anthony's assessment.
Receipts and the designation stop matching when this file's bytes change.


## Closed 2026-09-11

**Verdict: dead — the step it describes no longer exists.** Conductor has had no close-out
since 0.107.0 replaced it (`grep -rniE "close-out|closeout" skills/conductor` is empty; the
2026-09-11 Fable review, finding 1, and README's rewritten "How They Fit Together").

- **Close-out double-write** — conductor step 1 writes CONTEXT/TODO, step 6's
  invoked flow overwrites both.

**Verdict: superseded — the producer took option (c) on 2026-09-11** ("switch out should
clean up todos/backlogs/docs/etc and set next session start to make switch in faster/cheaper"),
before the row's own return condition fired (CONTEXT.md was 216 KB against the 250 KB
trigger). Built as Switch Out's lean-start step in v0.111.0: ruling in the loaded file, case
in `docs/decisions.md`. The row's measurements and its named risk (a reachable record can
sit unread) stand and are the reason the reading set is measured at every Out.

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

## Closed 2026-09-12

Verdicts from the closure review a native Opus 5 subagent returned on 2026-09-12
(the first real Conductor session on 0.111.0; full table at
`docs/work/model-ready-work/trials/2026-09-12-conductor-session-closure-review.md`).
Three done, eight dead; the sixty open and two unsure rows stay in TODO.md. The
hooks-verification row's open sub-finding was kept in TODO as its own row.

**Verdict: done.** `71391f8` exists; `docs/product/gate-visuals.md:8,12` carry the resealed fingerprints the row names.

- ~~**THREE sealed views are factually stale.**~~ **CLOSED 2026-08-29.**
  `funnel-driver`'s two were resealed 2026-08-28 (`71391f8`); `gate-visuals`'
  `visual-lifecycle.html` was corrected and resealed at its own acceptance gate
  on 2026-08-29 (`fp:3ef85a6441d5` -> `fp:c4f3e8949191`, producer's eye), and
  `design-gate-check.html` was found stale by cold eyes at the same gate and
  resealed with it (`fp:ccbac6efdb93` -> `fp:d210312a9bec`). The rule the row
  existed to enforce held throughout: each was redrawn at ITS OWN gate, never
  from another slug's slice.

**Verdict: done.** `hooks/hooks.json` present; `hooks/session-start.sh` builds the string; the row's three observations stand. Its open sub-finding stays in TODO as its own row.

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

**Verdict: done.** `find ~/development/work/krutho-strategy -maxdepth 4 -name 'sessions-of-record*'` returns nothing; the directory is gone.

- Clean krutho-strategy's stray `sessions-of-record/`.

**Verdict: dead.** The composer was removed at 0.107.0 (`21e6779`; `grep -rni composer skills/` is empty). Artifact half verified fixed: 0 absolute home paths, 21 `rev-parse --show-toplevel` in the 2026-09-01 spec.

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

**Verdict: dead.** Same composer removal (`21e6779`). Artifact half fixed: the spec's verify chain uses `test … -eq 0`.

- **`grep -c` in a fail-fast verify chain fails exactly when it should pass**
  (found 2026-09-01, second instance). The spec's final step ended
  `&& grep -c "^- \[ \] " <spec>` to prove zero unchecked boxes — and `grep -c`
  exits 1 on zero matches, so the `&&` chain aborted on the desired answer.
  Corrected to an exit-safe count (`awk` then `test -eq 0`), tested both ways.
  **Also handed back on 2026-08-28** as one of the same three sibling score
  defects. Two of those three have now recurred, which says the 2026-08-28
  findings were fixed in the artifact and never in the process that produces it.

**Verdict: dead.** Same composer removal (`21e6779`). Artifact half fixed by `528ca88`; cross-step invalidation marked in the spec.

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

**Verdict: dead.** Its named home, Conductor's "Calling the composer" section, no longer exists; the intent survives at `skills/conductor/references/execution.md` ("Finish the outcome").

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

**Verdict: dead.** The marker was removed at 0.107.0 (`21e6779`); `docs/state-contract.md:11` records the removal.

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
  with anything random. **SEVENTH instance 2026-09-09, and a new failure mode:
  six DAYS, not minutes.** No conductor ran that session at all, yet
  `kivna/.active-modes` still held `conductor: plan @ 2026-09-03 23:59 EDT` — the
  parked schema-split marker — so switch-out's fallback ("use the stamp on the
  `conductor:` line still in `.active-modes`, if one is there") pointed at a
  marker from a previous *session*, not a previous phase. The boundary wrote
  `closed HH:MM` instead. **This widens the diagnosis a second time:** the marker
  cannot report the first phase (the 2026-08-23 finding), and it cannot report
  *whether it belongs to this sitting at all*. A staleness guard is needed
  regardless of which of the two candidate fixes is chosen.

**Verdict: dead.** `hooks/stop.sh` was cut at v0.96.0 (`2146925`, "Ship hooks via plugin auto-load; cut stop.sh").

- **Stop-hook over-prescription**: distinguish work-dirty from
  session-state-dirty at a real stopping point.

**Verdict: dead.** Its reason is gone: `skills/tend/SKILL.md:207` says the hook path never version-rots (v0.96.0, `2146925`).

- Hook version staleness check in `/kerd:tend`.

**Verdict: dead.** Switch was replaced at 0.107.0 (`21e6779`); the numbered steps and the smoke test no longer exist.

- Guard switch-in step 3 smoke test against context bloat.

## Retained position, 2026-09-03

Moved verbatim from `CONTEXT.md` `## Where We Are` on 2026-09-11; it was a position
paragraph, not a decision, and TODO.md's "Earlier launch sequence" carries the live
version of the same items.

### Previous installed-Kerd position — retained, not freshly revalidated

**2026-09-03, three sittings (08:38–09:16 · 10:40–14:03 · 14:09–23:18 EDT) —
the schema migration SHIPPED.** Kerd at **v0.106.0**; CI green at the tip
(`f098ae5`).

- **`risk-state-split` is at ACCEPTANCE** — all 14 pieces landed. The whole
  ladder walked in one sitting: design package with three sealed views and a
  GO record (`1008a43`), a 14-step work specification, and the migration
  itself as **one atomic commit** (`e15a0f0`). The ledger's `State` column is
  now **Severity** (`fatal` | `non-fatal`) + **Treatment** (the four values);
  `Evidence` renamed `Risk evidence`; **`Treatment evidence`** is new, in
  three machine-distinguished forms — empty · `planned — <what will exist> ·
  <expected location>` · a resolving citation. 21 records, 84 rows migrated;
  selftest 51 → **57**. Next: the evidence-backed acceptance record.
- **`gate-reachability` still REFUSES at viability, on row 2** — and that is
  the intended outcome, not a regression. Row 1 parses clean (fatal +
  permanent + planned evidence): the new mechanism working on real data. Row 2
  is fatal with an `accepted unknown` treatment and empty evidence, so it
  refuses independently. **The migration clarified the blocker; it did not
  unblock the item.** Its narrow `${CLAUDE_PLUGIN_ROOT}` measurement must
  resolve before it advances.
- **Four fatal/accepted-family risks are newly VISIBLE and refusing** —
  `funnel-driver` row 4 · `gate-reachability` row 2 · `gate-visuals` row 1 ·
  `switch-fidelity` row 4. Each was carried as *accepted* while being fatal,
  a contradiction the one-column schema could not express. Remediation
  belongs to each owning item, never to the migration (the producer's ruling).
- **The migration-map view was RESEALED** (`fp:aef214c7ae05` →
  `fp:3b7b1c17243a`) after the producer's row-2 key superseded the
  design-time prediction that gate-reachability would unblock. Downgrade →
  correct → re-render → his eye → reseal, in that order; the dated GO record
  stands untouched and the supersession lives in
  `docs/plans/2026-09-03-risk-state-split-reseal.md`.
- **The launch plan is ON DISK** (`8b08ad1`) — five outcomes, the 8-step
  critical path, the binding rules. **Launch: 0 of 5 outcomes.**
- **v0.105.0 (morning): the Status Report talk format** — status speaks Work
  item · Stage · Issue · Resolution path, one final question.

## Closed 2026-09-17

- **The `agent.RPC` patch leak — DONE**, diagnosed and fixed at `0dda5ba`, CI green on
  3.12 with 731 tests. Verdict: the cause was `FinalReviewTests.tearDown` restarting a
  patcher its own `daemon()` had not stopped. That double start is refused from CPython
  v3.12.8 but silently succeeds below it, re-saving the current MagicMock as the
  original, so the parent's single `stop()` restored the mock — and CI's ubuntu-24.04
  runs 3.12.3. 11 of that class's 13 inherited tests triggered it; the three sibling
  classes were clean. Evidence: reproduced through `tools/run_tests.py` itself with the
  guard removed; before the fix 692 of 730 tests ran with a mocked `agent.RPC` and 53
  read it, 9 outside the family that manages the attribute, **no verdict ever changed**;
  after the fix the same probe reports no leak, 0 exposed, 0 uses. `FixtureIsolationTests`
  holds the invariant and fails when the old `tearDown` is restored. Codex reviewed
  twice; its finding — nested `TestResult`s discarded, so the regression could pass over
  hidden failures — was accepted and fixed. Case and both negative controls:
  `docs/work/model-dispatch-guard/work.md` and `patch-leak.html`.
- **The Kerd half of the palette drift — DONE** at `2b4f506` and `f8275f8`.
  `docs/work/visual-communication/scope.html` was the last Kerd view carrying the Krutho
  palette; it is now on diagram-design's shipped neutral tokens and was redrawn at the
  presentation type ramp, which also fixed two arrow-label masks narrower than their
  text. Verdict per Anthony's 2026-09-16 16:11 ruling: Krutho is his brand, Kerd ships to
  anyone. Evidence: re-applying the same substitution to a copy of the original produced
  a byte-identical file, so the re-skin changed no geometry; the redraw was inspected at
  1400px. **The upstream half stays open** and is still in `TODO.md`.

## Closed 2026-09-17 (afternoon)

- **0.134.0 — the Visuals contract correction. RELEASED,** `43241ae`, entry-gate CI
  green, 731 tests, `gate.py release` clean. Anthony supplied two versions of one
  diagram card (implementation-first against product language) and asked for the
  difference codified as a contract correction, not a governance protocol. Two clauses
  in `skills/visuals/SKILL.md`: code references sit in a subordinate evidence layer and
  removing them must leave the main relationship readable without the source; a view
  depicting or recommending a change carries the fuller test; every view saved beside
  work names its project, product or repository inside the render. **Evidence:**
  `docs/work/visual-communication/work.md`, both review rounds recorded there.
  **Not measured on real diagram output** — both halves are producer checks at review,
  and that limit stays open in `TODO.md ## Now`.

- **The 0.131.0 authority deferral — CLOSED by observation, twice.** A picked "Yes —
  open direction-setting" opens direction-setting without approving the saved task.
  First seen 2026-09-16; seen again at the 2026-09-17 12:23 arrival, where Conductor
  opened at Shape while the saved task stayed unapproved and unstarted. The visible
  label is doing the work it was added for, and the 0.132.0 Switch In capsule exemption
  rests on this. **Evidence:** `docs/work/question-pickers/work.md`,
  `kivna/sessions/2026-09-17.md`.

- **The 0.131.0 byte-identity deferral — CLOSED as worded, REOPENED corrected.** It
  named the renderer, and `where_we_are.py` has no picker argument, environment variable
  or awareness across 931 lines, so a picker cannot reach it: no situation in which the
  check could fail. Replaced by the claim it was protecting — whether the assistant
  returns that stdout unchanged when it also attaches a picker. That form is **tested,
  not verified** and stays open in `TODO.md ## Now`; it needs a reading taken outside
  the producing session. **Evidence:** `docs/work/question-pickers/work.md`, `8be16dc`.

**The through-line of all three rows.** The governing rule — a rule needs a test it can
fail and a situation it can pass — reached five instances today and has never needed
changing. Two of the five were introduced *inside 0.134.0*, the release that codifies
the class, one of them hours after its author wrote the record naming it. Every instance
was caught by an independent reader; none by a static check.

## Closed 2026-09-18

- **The assistant-side byte-identity claim — DROPPED by Anthony, 2026-09-18 10:07.**
  Verdict: dead. One outside reading was taken first (the 09:58 In's renderer output and
  the returned message, both 1,991 bytes, identical sha256, read from the host-written
  transcript), then Anthony ruled the check has no value: "switch in need to tell me what
  happens next and why, not just put up text from last session byte identical". The
  picker case is not owed. Evidence: `docs/work/question-pickers/work.md` `## Next`.
- **0.135.0 released — Switch In says what happens next and why, in plain English.**
  Verdict: done, commit `7d374ba` on `origin/main`, entry-gate CI success. 738 tests, gate
  clean, one Claude review (no authority holes; a null-input layout fallback fixed with a
  negative control). Not yet observed on a real arrival — that stays open in `TODO.md`.
  Record: `docs/work/switch-in-open-work/work.md`; ruling: `docs/decisions.md` entry 1.
- **Position paragraphs moved out of `CONTEXT.md`:** the 0.134.0 release boundary, the
  byte-identity continuation and "Both 0.131.0 deferrals are resolved". Their text is in
  Git at `7d374ba:CONTEXT.md`.

## Closed 2026-09-18 (afternoon)

- **Observe the first real 0.135.0 arrival.** Done 2026-09-18 10:40: the weighing
  held (product work led, with a reason), and the screen itself failed Anthony's
  reading on five points, fixed in 0.136.0 (`59cbd49`). Record
  `docs/work/switch-in-open-work/work.md`.
- **Launch sequence step 1, risk-state-split's acceptance record.** Done, accepted
  2026-09-18 11:23 with the measurement exception (`4ba70ca`,
  `docs/gates/2026-09-03-risk-state-split-acceptance.md`).
- **Launch sequence step 2, gate-reachability.** Done, reframed from Drive to
  Conductor, built as 0.137.0 and accepted 2026-09-18 15:29 (`4cbbeda`,
  `docs/gates/2026-09-18-gate-reachability-acceptance.md`). TODO's "still refusing
  at viability" was imprecise: it refused at scope.

## Position paragraphs moved out of CONTEXT.md, 2026-09-18 (afternoon)

Superseded by the afternoon sitting (0.136.0–0.138.0, launch sequence steps 1–2 done).

**Release boundary: 0.135.0 on `main`, released 2026-09-18** — Switch In says what
happens next and why, in plain English: it weighs every open item (a saved next step is
one candidate), shows the open work one line each and one recommendation with its
reason, and asks "What do you want this session to move forward?". Choosing work opens
Conductor at Shape for it, never approval of its operations. Record
`docs/work/switch-in-open-work/work.md`; ruling `docs/decisions.md` entry 1. **Not yet
observed on a real arrival.** Resolve IDs and CI with `git log` and `gh`. Earlier
position paragraphs are in `docs/backlog-archive.md`.

**0.133.0–0.135.0 are RELEASED and archived** in `docs/backlog-archive.md`
(`## Closed 2026-09-16 (evening)`, `2026-09-17 (afternoon)`, `2026-09-18`). **Claude owns
build and release; Codex `codex-tui` is the pairing partner for expert review and
investigation** (cadence: checkpoints, before-push). Codex had no tokens on 2026-09-18,
so 0.135.0's review was a fresh Claude reviewer.

**Installed state — keep three numbers distinct:** what each side runs, the latest
release, the tip. **Claude ran 0.134.0** at the 2026-09-18 arrival (skills loaded from
the `kerd/0.134.0/` cache — this corrects the saved "0.133.2"); **Codex runs 0.133.0**
(saved observation). 0.135.0 is released and the tip, installed nowhere yet; the next
Switch In shows the new arrival only once the Claude plugin updates. Resolve live
numbers rather than trusting this line.

**Selected continuation — proposed, not agreed: sign off the risk-state-split
migration.** Write the evidence-backed acceptance record at
`docs/gates/2026-09-03-risk-state-split-acceptance.md`. **Why:** it is the first step of
the launch sequence (0 of 5) and every later step waits on it; the migration shipped
2026-09-03 and only its acceptance is missing. Owner Claude drafts; Anthony gives the
expert-user pass (cold eyes, never mechanical cleanup — the 2026-09-02 ruling). It must
answer honestly that no stage-1 measurement was declared, so the product-outcome row is
*not assessable*. Stops at the record: no release. Detail: `TODO.md` "Earlier launch
sequence" item 1.

**Deferred, not dropped:** the first real 0.135.0 arrival, unobserved. **0.134.0's two clauses have never been measured on real diagram
output** — both are producer checks at review, and no diagram has yet exercised them.
Also unverified: whether either 0.132.0 rule holds beyond the one marginal scenario
tested; Archify's two Socket alerts; and `diagram-design`'s style guide, where `accent`
is Krutho blue while `accent-tint` still holds the old tangerine (upstream's file, found
independently by two sessions).

**The launch sequence is retained and untouched**: five outcomes, 0 of 5, detail in
TODO.md under "Earlier launch sequence" and `kivna/sessions/2026-09-03.md`.
