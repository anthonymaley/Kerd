---
route: new
stage: ready-to-release
---

# Acceptance record — gate-visuals slice 1, 2026-08-30

**THE PRODUCER'S KEY, given 2026-08-30 14:35 EDT, in his own words:**

> I accept the expert-user evidence and approve gate-visuals as ready to
> release, with the missing upstream product measurement recorded as an
> explicit exception. No target is to be authored retroactively.

An earlier draft of this record said "both keys given" before the producer had
approved anything. That was the session overclaiming; it was struck rather than
quietly deleted, and the key above is the first and only acceptance this record
carries.

**Cold eyes ran as four blind reviewers by layer.**
**Layer 4 blocked three times** — seventeen findings, then eleven against the
amended tree, then nine against the second amendment. A fourth, targeted
pass found four; a fifth, a final diff check, found one blocking and three
minor; a sixth, a frozen-tree acceptance review under a strict
blocking/non-blocking rule, found two blocking and filed five. **Six rounds.** Every finding
on this item's own surfaces was repaired before acceptance rather than filed.
The producer's eye passed both redrawn views on 2026-08-29, and both were
resealed from final content **after** that review, never before it.

**Clock:** view key 2026-08-29 16:23 EDT — the producer's eye on the final renders. **Acceptance key 2026-08-30 14:35 EDT.** The first eye was
given at 15:52 EDT on drawings the second cold-eyes pass then found defects in;
that seal was withdrawn rather than carried forward.

## Release condition

This record separates three things that a single list of rows would blur:
**conformance conditions that genuinely passed against a prior declaration**,
**one condition that is not assessable because no antecedent was ever declared**,
and **the producer's decision to accept anyway**. The third is an explicit
exception, not a vacuous pass.

### Conformance — checked against declarations that predate the build

- **Met the contract** — 8/8 pieces landed, verified against the tree rather
  than read off the checklist. `docs/plans/2026-08-22-gate-visuals-spec.md`
  carries 8 `## Pieces` items, all checked and zero unchecked; the range
  `137065a..576c213` (18 commits) carries exactly 8 `Piece:` trailers,
  `gate-visuals/1` through `/8`, one-for-one with them. An independent reviewer
  that never saw the build opened each piece and confirmed it present, and
  re-ran every `**Verify:**` block in Steps 1–4 — each matched the spec's
  expected output character for character.

- **Met the design** — the mechanism `docs/design/gate-visuals.md` describes is
  the mechanism that ships. A second independent reviewer exercised it rather
  than reading it: built fixture trees and proved the gate refuses a declared
  concern with no view, a view with no approval, and a view edited after
  sealing; proved it passes when all three are correct; reproduced the
  fingerprint recipe's three published test vectors by hand; and confirmed
  `seal` computes from file **content**, refusing rather than fabricating when
  handed a missing or non-`.html` path. It found no failure mode that refuses
  when it should not, or passes when it should not.

- **Proof layers pass** — nine of nine green at the tip, each run rather than
  assumed: `gate.py selftest` (51 cases) · `gate.py audit` (clean; 1
  pre-existing register trace-gap finding, unrelated) · `gate.py release`
  (clean) · `progress.py selftest` (15 ok) · `progress.py stale` (render
  current) · `matrix.py selftest` (16 ok) · `matrix.py audit` (clean) ·
  `gen_journey.py check` (7 stages) · `tests/hooks_test.sh` (21/21).
  `gate.py check gate-visuals design` → PASS, 8 inputs on disk.

- **Both views sealed on the key, from final content** — `visual-lifecycle.html`
  `fp:3ef85a6441d5 → fp:c4f3e8949191`, `design-gate-check.html`
  `fp:ccbac6efdb93 → fp:d210312a9bec`, both `Tony, 2026-08-29`. The order was
  the one this repo settled on 2026-08-28: downgrade → correct → render → the
  producer's eye → seal, with `seal`, `check design` and `audit` run **on** the
  key. **It ran twice**, because the second cold-eyes pass found defects in both
  drawings after the first seal: the intermediate fingerprints
  (`1d6f6235359a`, `31f73d2d5de5`) were downgraded, the drawings corrected, both
  re-rendered, and a **second producer's eye** given before the final seal. No
  fingerprint in this record was computed before the drawing it certifies was
  looked at, and no eye was given on content that later changed without a new one.

- **The feature caught its own drift, unprompted.** Editing the two approved
  drawings in the second amendment round invalidated their seals, and the gate
  refused before anything was told to check: `REFUSED at design — gate-visuals:
  2 missing`, naming each concern, each drawing, and both sides of each
  fingerprint (`approved at fp:1d6f6235359a, now fp:c4f3e8949191`). Slice 1's
  whole claim is that an edited drawing loses its key; that is the claim
  executing on its own author's edit, which is the strongest evidence available
  that the mechanism is real and not merely present.

### Not assessable — no antecedent exists

- **Product outcome: not assessable.** No measurable product outcome was
  declared before the build, so this acceptance gate cannot determine whether
  the item achieved one. The producer accepts this known gap; no target was
  retroactively authored.

  **The absence is structural, not a matter of reading.** Every comparison item
  carries a stage-1 measurement section — `docs/design/rung-vocabulary.md:261`,
  `docs/design/push-wiring.md:129`, `docs/design/time-awareness.md:93` — and
  neither `docs/design/gate-visuals.md` nor `docs/product/gate-visuals.md` has
  one. A blind reviewer read all four of this item's artifacts in full, searched
  for anything measurement-shaped, and classified everything it found as
  something other than a declaration: the 27-generators/5,961-lines figure and
  the 39-requirements-versus-one-drawing table are **evidence for why the item
  mattered**, measured before and during design rather than targets for the
  build; *"its firing frequency is the measurement"* is an expectation about
  **future** divergence with no baseline, no unit and no target; the
  strong/medium/weak checkability table is qualitative. The reviewer was
  explicitly forbidden to propose a target and did not.

  **Why this row is not repaired.** Authoring a target seven days after the
  build is the fabrication an acceptance record exists to prevent — it would
  make the gate check the build against a number written to fit it. The honest
  record is that the item shipped with no measurable claim about whether it
  worked, and that this cannot be fixed backwards.

### The producer's decision

- **Accepted with the measurement gap named as an exception, 2026-08-29.** The
  producer's ruling: close the gate, do not create a target after the build, and
  do not let the record imply that product measurements were met. This is an
  explicit exception on a known process gap, not a condition that passed.

- **The exception is bounded by a filed countermeasure**, so the precedent
  cannot decay into *"declare nothing and pass"*: future work must declare
  measurable outcomes upstream — or explicitly declare them **inapplicable with
  a reason** — before it can reach acceptance. Filed as its own item; likely
  home `requirements-success-measurement`, which sits at viability for exactly
  this question. Same shape as `rigor-level`'s hollow-waiving countermeasure:
  the cheap state is the one that must be argued for.

- **One exception, not twenty-two.** Twenty-one further defects found at this
  gate — eleven in the first cold-eyes round, ten in the second — were
  **repaired before acceptance rather than filed as additional exceptions.**
  The producer's line is repairability: the measurement absence stays an
  exception because it cannot honestly be repaired retroactively; anything that
  can be repaired now is, or the exception count inflates for no reason and cold
  eyes degrades from an acceptance mechanism into advisory commentary. His
  words: *"Accepting those known contradictions would turn the review into
  advisory commentary."*

## Cold eyes — the block, and what it cost

Four blind reviewers over `137065a..576c213`, none of which saw the session
narrative, one per layer.

**Layers 1, 3 and 5 passed.** Layer 4 — declared truth — **blocked**, holding
the pattern: this layer has now blocked at every gate where it has run.

**Layer 2 was not run, because nobody can say what it is.** Across all seven
gate records in `docs/gates/`, layer 2 appears only inside ranges (`layers 1–3`,
`layers 1–4`, and once `layers 1/3/4`, which skips it); it has never been named,
reported, passed or blocked on its own in six runs. `docs/playbook.md` carries
cold-eyes *gotchas* and no cold-eyes *mechanism*, and the practice is named as
the acceptance gate's key only in `CONTEXT.md:157` — a standing decision, not a
procedure. **Nothing under `skills/` mentions cold eyes at all**, in any variant,
and `git log -S` shows it never has. An earlier draft of this record cited
`skills/conductor` as naming it; that citation was false and is corrected here.
The correction makes the finding stronger rather than weaker: the practice that
gates acceptance is not merely undefined, it is absent from the skill files that
route the work. Prior records saying
"layers 1–4 pass" therefore asserted a layer nobody had defined. Recorded here
rather than repeated, and filed: **cold eyes is the repo's most load-bearing
review practice and it has no written definition.**

### The seventeen findings, and where each went

**Eleven repaired before acceptance** — all on this item's own surfaces or the
canonical documentation of the machinery it shipped:

1. `visual-lifecycle.html` named the retired `goal` rung in its visible label
   and in its `<desc>` — the accessibility text a screen reader speaks. The file
   was **sealed on 2026-08-27, two days after the fold**, so the build
   re-affirmed a stale word rather than catching it. Corrected to `acceptance`,
   which is where the redraw-and-compare belongs: it is producer-facing evidence,
   and machine checks live at the loop's edges.
2. `docs/product/gate-visuals.md`'s gate table enumerated the retired
   eight-rung ladder (`slice`, `contract`, `build`, `goal`) in an order the live
   ladder no longer has. Folded to the seven live rungs; old-`loop`'s learning
   types merged into `acceptance`, where the round-again verdict is actually made.
3. `docs/design/gate-visuals.md:161` and the product doc's exception section
   both said *"Build's visual"* — the retired rung. Now *"The loop's visual"*.
4. `tools/reqview/fingerprint.py`'s docstring claimed *"nothing else computes a
   fingerprint"*. **False.** `reqview.py` emits a second, field-for-field
   identical implementation of rule 9 in JavaScript into the register's own HTML,
   because the page recomputes approval state in a browser with no server to ask.
   The module exists to make "one implementation" true and there are two, with
   **nothing testing them against each other** — so the guarantee holds by
   inspection, not by check. The docstring now says all of that, and names the
   two sites that are *not* counter-examples (`kit.req_statement_hash` is a
   different recipe, honestly labelled; `progress_kit`'s local `fingerprint` is
   an md5 over a JSON model) so they are not re-reported.
5. `tools/gates/README.md:23` said `check`, `audit`, `release` and `seal` were
   *"the only four subcommands that can exit 1"*. `selftest` returns 1 on a
   failed root case or fixture assertion — and the same file's usage block four
   lines above already printed `exit 0 / 1` for it. Now five.
6. The README's **published Views schema, copied literally, was refused by the
   parser.** `CONCERN_FIELD_RE` captures everything after the colon, so the two
   `#` comments in the block became part of the field: the `approval` line
   matched neither sealed nor unsealed form and was refused as unreadable, while
   the same comment on a `view: n/a` line parsed and silently swallowed the
   comment into the stored reason. A reviewer found this by pasting the
   documented example onto a fixture and watching the audit refuse it. Comments
   removed; the trap written out; the two annotations they carried moved to prose.
7. The README's AU9 row listed four wrong-states and reassured the reader that
   pending approvals do not fail the audit. `kit.py` excludes exactly `ok`, `na`,
   `unapproved`, `unsealed` — so AU9 fails on all seven of the rest, and the
   reassurance covered a fifth state it does not cover. The consequence the row
   hid is the sharp one: **declaring a concern before its drawing exists turns
   the repo-wide audit red.** Corrected, with that consequence stated.
8. The README's `design` gate-table row never mentioned the `viewpoint` rule or
   the `.png`-is-never-the-view rule, both of which `_view_row` enforces. The
   gate table is the row a reader consults; it under-stated the gate.
9. **`design-gate-check.html` — a sealed, producer-approved drawing asserting a
   mechanism the code does not have.** It read *"derive the drawings owed — one
   per aspect · nobody chooses"*. The shipped gate derives nothing: `viewpoint:`
   is free text checked only for presence. **The build was not at fault** — the
   contract said so in terms (`2026-08-22-gate-visuals-spec.md:170`, *"the
   viewpoint is free text at mvp: no closed viewpoint list is checked"*). The
   drawing and the frame overclaimed against a deliberate deferral. The
   producer's instruction was to **preserve the mvp contract rather than quietly
   expand the implementation to match the picture**, so the drawing now says
   viewpoints are declared free text whose presence the gate checks. Its refusal
   sidebar previously said *"which of the three"* while the gate refuses on nine
   codes; it now says *"which fault"* — **deliberately carrying no number**,
   because a count baked into a sealed drawing is precisely what has been wrong
   four separate times on this item, and the `<desc>` names the further shape
   faults in prose where correcting them is cheap.
10. The product doc's *"The set is closed. A gate draws from its own row and
    from nowhere else. Reaching outside it is a defect"* was contradicted by its
    own aspect table fifty-five lines below, which owes four types the design row
    did not list (`medallion`, `dp-integration`, `dp-security-matrix`,
    `org-chart`). The row now lists them, making the claim true, with the
    converse noted honestly: a type sitting in a row and owed by no current
    aspect (`tree`) is spare capacity, not a contradiction.
11. Vocabulary and hygiene: `aspect` — recorded in the design doc as *"what we
    were calling it"*, past tense — survived as the counted noun in both sealed
    drawings and the product doc, while the front-matter key a reader must type
    is `concerns:`. **The first round corrected it in one drawing and missed the
    other, which the second round caught** — see round two below. A paragraph
    duplicated verbatim in the product doc was removed. `gantt at slice` →
    `gantt at scope`.

**Six filed, not repaired** — each belonging to another item, to global tool
behaviour, or to a surface older than this slice:

- `skills/drive/SKILL.md:70` gives a false reason for a real convention: it
  claims the front-matter parser *"stops reading keys at the first `key: value`
  line after `concerns:`"*. `read_front_matter` does no such thing; the parser
  that stops there is `parse_concerns`, correctly terminating a list. The
  ordering advice is harmless, the reason for it is untrue. **`funnel-driver`'s.**
- `tools/gates/README.md:111` *"The six system design docs in `docs/design/`"*
  and `:253` AU1 *"Runs against ten real files today"* — 27 files match today.
  Predates this slice.
- `README.md:18` *"## What's New (v0.99.0)"* while the newest entry is v0.104.0.
  **Release-closeout drift** — the pass fired by this record's landing owns it.
- `docs/design/diagram-types-by-rung.md:55` says the ladder is *"a cycle of
  eight"* and `:192` says *"exactly seven positions"*, same document, same type.
  Already an open Backlog row from the rung fold.
- **`gate.py`'s root resolver walks out of a git worktree into the parent repo.**
  `_walk_up_for_git` tests `os.path.isdir(cur/".git")`, and in a worktree `.git`
  is a **file** — so the test is false and the walk continues past a legitimate
  repo boundary. Found the hard way: a review subagent working in a worktree had
  its `gate.py` call bind to the live tree and then reverted uncommitted work
  there, recovered only because the blob was still unreachable-but-present.
  Global tool behaviour, filed with its one-line fix.
- `docs/playbook.md:391`'s cold-eyes trap names the wrong tool. `gate.py` no
  longer pins root to `kit.ROOT`; `tools/design/matrix.py` still does, in ten
  places, so **every `matrix.py` command run from any cwd targets the Kerd repo**
  — the trap is alive, one tool over. Two reviewers disagreed about this and the
  truth was in neither report; it was settled by reading the code.

**Six more were raised and refuted rather than acted on**, and the reviewer
separated them itself — among them the "design GO recorded" label (the drawing
describes the human step, as the repo's own generators do), and the dated spec's
retired vocabulary (old words in a **dated** record are honesty, not drift, per
the 2026-08-25 ruling).

### The second round — layer 4 blocked again, and the method was wrong

**Layer 4 was re-run against the amended tree** rather than trusted, on the
producer's instruction. **It blocked a second time, with eleven findings**, and
the diagnosis is more useful than the list: *an enumerated sweep is precise and
non-exhaustive*, a mechanism this repo recorded on 2026-08-25 and which the
first amendment round reproduced exactly. Every miss was a site no list had
named.

**The worst of them: the two sealed drawings were left disagreeing with each
other.** `aspect` → `concern` was applied to `design-gate-check.html` at all
five sites and to neither site in `visual-lifecycle.html` — a file open in the
same pass, edited for something else. Two approved drawings for one work item,
in one folder, using different words for the thing the gate counts.

Ten further repairs, all on this item's own surfaces: the design-against-built
ladder still read `build` / `goal gate` eleven lines above a risk ledger, in the
same file whose gate table had just been folded · *"Slice 2 — the goal-gate
redraw"* · the risk ledger still promised a visual *"for each **aspect the work
touches**"*, which the gate cannot know — it reads a **declaration** · the
design doc's caption under the corrected drawing still said *"**Three**
questions"*, the exact count deleted from that drawing for being wrong · and
`kit.py`'s own `_audit_au9` docstring carried, verbatim, the four-of-seven
defect the README's AU9 row had just been corrected for — the README was right
and the code it paraphrases was not.

**One defect the amendment itself introduced, and it is instructive.** Making
*"the set is closed"* true against the aspect table meant adding four types to
the design row — and one of them, `dp-security-matrix`, is assigned to
**handoff** by `docs/design/diagram-types-by-rung.md:40`. Reconciling two lists
broke a third. Reverted; the residual disagreement is now named in the product
doc rather than silently resolved, because that file is another work item's
editorial merge and reaching through its gate is the thing the fingerprint
mechanism exists to prevent.

### The method changed, because three enumerations produced three blocks

The repo's own rule is *a rename gets an enumeration; a fold gets a closing
check*. Three rounds had all been enumerations. A **closing purity scan** now
covers gate-visuals' four living surfaces: it unsplits `\n`/`\t` escapes before
matching — the trick that hid `"GOAL\nGATE"` from every grep in an earlier
session — looks for retired rung names in *rung-shaped positions* rather than as
bare words (so `the build is wrong` and `contract spec` are not false hits),
looks for the stale counted noun, and asserts the two sealed drawings agree with
each other. It reports zero on all four surfaces, and `aspect=0` in both
drawings.

**That check is a REVIEW AID, not a guard, and this record claims nothing more.**
It lives in the session scratchpad, not in `tools/`; nothing in CI calls it; it
will not survive this session. It has no fixtures, and its own scoping is a
judgement — a fourth review pass caught it committing the very defect it exists
to catch, being scoped to the eight files earlier findings happened to name.
Widened repo-wide it then returned 99 hits of which almost all were legitimate
history, which produced the rule it now runs on: **claim patterns generalise
(a false claim is false anywhere) and vocabulary patterns do not (a retired rung
name inside narration of a past event is honest)**. A reviewer confirmed it is
load-bearing rather than decorative — four broken fixtures caught in a
disposable copy, no false positives on `fix the build` or `contract spec` — but
that was one reviewer on one afternoon, not a test suite. **Promoting it to
maintained machinery is filed, not built**, and nothing in this slice should be
read as shipping a guard against the defect class it found.

## The expert-user pass — EXERCISES RUN 2026-08-29, KEY GIVEN 2026-08-30

**Who ran it, stated exactly.** This repo defines the expert-user pass as the
producer using the output. Here the producer instructed the session to execute
the exercises and report behaviour *and wording* for his judgement, so the
running was the model's and the judging his. That is a weaker instrument than
the producer driving it himself and is recorded as such rather than rounded up.

Six exercises against a disposable copy of the live tree, each naming what it
expected before it ran.

| | Exercise | Result |
|---|---|---|
| 1 | correct state | `PASS design — gate-visuals: 8 inputs on disk` |
| 2 | one character appended to an approved drawing | `REFUSED` — *fingerprint mismatch — approved at `fp:c4f3e8949191`, now `fp:2c5fd12e53c6`* |
| 3 | a concern declared, never drawn | `REFUSED` — names the concern *"how the thing is deployed"* and the path it expected |
| 4 | the same state, seen by the repo-wide audit | `problem:` line **textually identical** to the gate's `need:` line |
| 5 | `n/a — <reason>` on that concern | `PASS ... 9 inputs on disk` — the hatch opens **and the other concern stays verified** |
| 6 | `n/a` with the reason removed | `REFUSED` — *"n/a without a reason"*. The hatch is not a bypass |

All five criteria the producer set are met: correct state passes · an edited
approved drawing refuses and identifies the mismatch on both sides · an undrawn
concern refuses by name · the audit agrees with the gate word for word · and the
escape hatch opens without weakening any other concern.

**A defect in the harness, not the feature, found mid-pass and worth recording.**
The first run's step 3 restored the drawing with `git checkout --`, which
restores from HEAD — the *pre-amendment* file — so a stale fingerprint leaked
into steps 4 and 5 and muddied the demonstration. The script now snapshots the
working tree and restores from that. The lesson generalises past this script:
**on a tree with uncommitted work, `git checkout --` is not an undo, it is a
different edit.** A review subagent had already made the same mistake against
the live repo earlier the same day.

### Four findings, all wording, none blocking

Only a user hits these; every one is a machine-emitted string, which by this
repo's own currency rule is where vocabulary binds hardest.

1. **`audit: 1 problems`** — plural at n=1, on a tool whose job is refusing
   other people's work. **Fixed** (`gate.py`, both `audit` and `release`, plus the
   `audit: clean (n findings)` line and the sibling emitters in `matrix.py` and
   `progress_kit.py`; both README templates updated to `<n> problem(s)`. The
   first attempt fixed both code paths and only one of the two README
   paragraphs — caught by the final diff check). Verified in both directions:
   `audit: 1 problem` / `audit: 2 problems`.
2. **`REFUSED at design — gate-visuals: 1 missing` when the file is present.**
   The drawing exists, 6,219 bytes; what is missing is a *valid approval*. In
   the gate's own model an "input" is a satisfied requirement rather than a
   file, so the string is defensible — and it is still the sentence most likely
   to send a reader hunting for a deleted file. **Recorded, not fixed:** it is
   loose, not false, and changing an emitted string at an acceptance gate for
   looseness is how a sixth review round gets created.
3. **`need:` at the gate, `problem:` at the audit, for one identical state.**
   Two registers for one condition, met by a newcomer in whichever order they
   happen to run the commands. Recorded.
4. **Editing one drawing reports the item at `enters at: scope`.** Derivation is
   correct — a broken design gate means the item cannot be past design — but a
   one-character edit moving a work item from `acceptance` to `scope` reads as
   catastrophic when it is a stale seal. The router says *why* on the next line;
   the position line alone does not. Recorded as the shape of a future finding
   about how `route` reports fall-back, not as a defect in this slice.


## What this record does not claim

- **The proof layers prove conformance and reachability, never comprehension.**
  A document that names a file passes even if it misdescribes it.
- **Layer 2 of cold eyes was not run and is not defined.** No claim is made
  about whatever it was meant to cover.
- **The two rule-9 implementations are field-identical today by inspection.**
  Nothing tests them against each other, so that is an observation with a
  shelf life, not a guarantee.
- **The gate counts drawings; it cannot read them.** Nothing here checks that a
  drawing is a diagram rather than prose in rectangles — the limit this item's
  own design states, unchanged by shipping.
- **`viewpoint` is free text at mvp.** The gate checks that it is present. It
  does not derive a closed set, and the drawing no longer says it does.
- **The closing scan is a session review aid, not shipped machinery.** No CI
  step runs it, it has no fixtures, and it does not survive this session.
- **The expert-user pass was executed by the model on the producer's
  instruction**, with the producer judging the reported behaviour and wording.
  That is not the same instrument as the producer driving the tool himself, and
  no claim here should be read as though it were.
- **Six review rounds, every one of which found something.** Layer 4 blocked
  three times (17 -> 11 -> 9); a fourth, targeted pass found four; a fifth,
  a final diff check, found one blocking defect and three minor; a sixth, a
  frozen-tree acceptance review against a hashed artifact under a strict
  blocking/non-blocking rule, found two blocking and filed five.
  **Round six's two blockers were both introduced by round five's fixes, and
  round six's own fix introduced a seventh-round finding** — a miscount one
  clause after correcting a miscount. That is recorded rather than smoothed:
  the amendment spiral was ended by freezing the tree and narrowing the
  decision rule, not by the work becoming defect-free. Two of the fourth
  pass's findings were in the countermeasure, two in the work. **Each round's
  fixes created the next round's findings**, and the recurring mechanism was the
  same every time — an enumerated sweep is precise and non-exhaustive. The fifth
  round's block is the cleanest instance: both `audit` and `release` code paths
  were fixed and only one of the two structurally identical README paragraphs
  documenting them, sixteen lines apart. **This is convergence, not a proven
  fixed point**, and this record does not claim the work is defect-free — only
  that every defect found was repaired or filed.
