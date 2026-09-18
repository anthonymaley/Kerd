---
route: new
stage: ready-to-release
---

# Acceptance record: gate-reachability, 2026-09-18

**THE PRODUCER'S KEY, given 2026-09-18 15:29 EDT.** Anthony answered **"yes"** to
this question, asked with the record open and the proposal immediately above it:

> Do you accept gate-reachability with the measurement exception, and shall I
> push 0.137.1 with its record?

That answer accepts the item with the product-measurement gap as an explicit
exception, and accepts the qualifications below as written. The record was
drafted before the key and moved here only after it.

**What shipped.** Conductor, working in the user's own repository, asks that
project which step a work item is on (at pickup, and when a build first starts),
names missing groundwork and offers it, and records a go-ahead anyway in the
work record. Kerd 0.137.0 (`8a72c0f`, render follow-up `d770f18`) and 0.137.1
(the reverse-direction test, this record's own repair). Launch step 2.

## Release condition

Conformance against what was declared before the build; what cannot be
assessed; the producer's decision. **Observed** means run 2026-09-18;
**recorded** means taken from a commit or log and not re-run.

### Conformance: checked against what was declared before the build

- **The reframed winning line holds** (declared at scope, 2026-09-18 13:15):
  *"Conductor, run from a repository that is not Kerd, asks that project which
  step a piece of work is on, names missing groundwork before moving on, and
  reads nothing of Kerd's own tree."* Observed in
  `skills/conductor/scripts/tests/test_step_check.py`, which runs the command
  exactly as written in Conductor's `SKILL.md`: an item with its groundwork
  enters at `loop`; an item without a Scope enters at `viability` with the
  Scope named; a slug that exists only in Kerd is not found in the project.
- **The original frame's first condition, "no manually supplied path"**
  (2026-09-02), holds for the plugin: the path is written in `SKILL.md`, where
  Claude Code fills it in. Recorded: measured once, 2026-09-18, with a
  throwaway plugin in one headless run, and consistent with the plugins
  reference. The project root comes from
  `git rev-parse --show-toplevel`, never typed.
- **The five design decisions** (`docs/design/gate-reachability.md`, keyed
  13:39) are each stated in Conductor's section `## Check where the work
  stands` and guarded by phrase tests: when it checks; what the user sees; the
  recorded go-ahead, written under `## Decisions and changes` in the work record
  and never in the `docs/product/` record the check reads, and shown at the next
  pickup; no check when the project cannot be identified; the plugin path in
  `SKILL.md` only. **The phrase tests show the words are present, not that a
  model follows them.**
- **The spec: 4 of 4 pieces landed** (`docs/plans/2026-09-18-gate-reachability-spec.md`).
  Recorded: every Verify was run 2026-09-18 during the build.
- **Risk row 1, the killer risk (the wrong repository), fatal, permanent
  countermeasure: treated in both directions, as the 2026-09-02 ruling asked.**
  From inside Kerd against a separate project, the check never answers from
  Kerd. From inside that project against Kerd, it never answers from the
  project. Negative controls, run by hand 2026-09-18 and reproduced by the
  reviewer: with `--root` removed, the first answered from Kerd's own records
  (`risk-state-split` at ready-to-release; the project's item not found) and the
  second from the project; the tests failed as they should. The reviewer found
  that with `CLAUDE_PROJECT_DIR` set, `gate.py` falls back to it and the reverse
  test passed without `--root`. **Repaired before acceptance:** the tests now
  clear that variable; with it set to Kerd and `--root` removed, all three
  fixture tests fail (observed 2026-09-18).
- **Risk row 2 (the plugin path), fatal, permanent countermeasure:** the fixture
  resolves the command as written; no Conductor reference file carries the
  placeholder (tested).
- **Proof layers pass on the 0.137.1 working tree:** 746 tests · `gate.py
  release` clean · `gate.py audit` clean (1 unrelated requirements finding) ·
  `gate.py check gate-reachability acceptance` → PASS, 14 inputs on disk. Both
  fatal rows' evidence cells were read by hand against the tests they cite. The
  render is regenerated in a follow-up commit after this one lands.
- **Review:** recorded, from `8a72c0f`'s message: a fresh Claude reviewer, two
  rounds on 0.137.0, 2 blocking and 7 non-blocking findings, then 1 minor, all
  fixed before commit.

### Qualified

- **The frame's second condition, "surface a real refusal", is not met, by
  decision.** The 2026-09-02 frame asked that Drive and Conductor "invoke the
  gate with no manually supplied path and surface a real refusal". At scope,
  2026-09-18 13:15, the producer chose a named gap and an offer, never a
  refusal, with a go-ahead recorded. The check names the gap (`enters at:
  viability`, the missing Scope named, exit 0) and does not refuse. Risk row
  3's countermeasure, which said the fixture "asserts a real refusal", was
  reworded to match before this record.
- **0.137.0's own push was red.** CI failed at `progress.py stale` on
  `8a72c0f`; the render-only `d770f18` passed. The render marks a piece landed
  only once it is committed, so a render made before the commit is stale after
  it. It recurred although `docs/playbook.md` already records the trap from
  `7418657`, 2026-09-03: a recorded trap did not stop the second instance. Not
  a defect in this item.
- **Not yet seen in a real Conductor session with a model.** Everything above
  is the command, its output and the instruction text. Whether a model applies
  the check at the right moments is unobserved until the diagnostic pilot, which
  this item exists to unblock.
- **The frame's original scope named Drive and Conductor, four calls.** Scope
  narrowed to Conductor after the 2026-09-18 ruling that Conductor replaces
  Drive. Drive still ships, with its two relative-path calls unchanged. They
  remain broken outside Kerd until Drive is removed (TODO Backlog).
- **Risk row 3** (silent degradation), non-fatal, temporary: the fixture is its
  check. It asserts the named gap, not a refusal. **Row 4** (board and fidelity still Kerd-pinned), non-fatal, accepted:
  deferred by the producer's 2026-09-02 scope ruling, unchanged.

### Not assessable: no antecedent exists

- **Product outcome: not assessable.** No measurable outcome was declared before
  the build; "Winning, in units" is a pass/fail condition, checked above. No
  target is written now.
- **This is the third time.** gate-visuals (2026-08-30) and risk-state-split
  (earlier today) were accepted with the same gap. The 2026-08-29 countermeasure,
  that work declares a measure or its inapplicability before acceptance, is
  still unbuilt (`requirements-success-measurement`, at viability).

### The producer's decision

- **Accepted with the measurement gap named as an exception, 2026-09-18 15:29
  EDT** (the key above). No target is authored after the build, and nothing
  here implies a product measurement was met.
- **Repaired before acceptance, not filed:** the reverse-direction test (risk
  row 1's other half) and the `CLAUDE_PROJECT_DIR` fallback that let a test pass
  without `--root`, both in 0.137.1.
- **Accepted as written:** the non-refusing behaviour chosen at scope, the red
  0.137.0 push, the unobserved model behaviour (the pilot's to observe), and
  Drive's calls left broken until Drive is removed.
- **The third measurement exception carries the same unmet bound** as the first
  two: the 2026-08-29 countermeasure is still unbuilt.

## Cold eyes

One blind reviewer (fresh Claude, opus · high), 2026-09-18, checked the claims
against the tree, CI and the tests, and reproduced the negative controls.
**Two blocking:** the frame's "real refusal" half was left unstated, and risk
row 3 still described a refusal. **Five non-blocking:** the render claim at
HEAD, the playbook already naming the trap, the `CLAUDE_PROJECT_DIR` fallback
that let the reverse test pass without `--root`, gate-visuals' date, and the
observed/recorded labels not applied. All seven were corrected, and the test
weakness was repaired, before the key.
