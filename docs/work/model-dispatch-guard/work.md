# The explicit-model dispatch contract (0.133.0)

## Now

Owner: the Claude session holding `kerd-b5-review` (adopted at Switch In,
2026-09-16, from the handoff designated against `CONTEXT.md`).
Stage: **Released** — see the commit on `main` for its revision and CI state.

**Codex's before-push gate passed on round 3, 2026-09-16 17:51: "ready for Anthony's
release decision. No blocking findings."** It kept the verbatim ruling block where it
is, found no new defects, and closed with the judgment that matters more than the
pass: *"three review rounds and increasingly exact prose guards are the limit of
useful refinement here. Further semantic hardening would be protocol work for its own
sake; ship this version, observe real dispatches, and only change it again for
demonstrated behavior."* Anthony authorized the push at 18:02.

**The pattern across all four passes, and the thing to carry forward: every defect in
this release was a calibration defect, never a design defect.** Three of them were the
same error — a rule stated so absolutely that a legitimate situation could not satisfy
it: the all-keys absolute that contradicted the no-effort-agent route, the fix for it,
and then the `FORCE` fact added without saying what to do when it fires. That is the
defect class 0.132.0 was written to remove, produced three times while removing it.
Anthony's design from 16:48 was never altered by any round.

### Round-by-round

Codex `codex-tui`'s before-push review returned **not ready to push** with five
findings (three High). All five are applied; a focused re-review of the frozen tree
was queued 2026-09-16 17:40 and is **submitted-unconfirmed**. Those fixes invalidate
the gate the first review satisfied, which is why the repeat is owed before any push.

### Codex's five, and their disposition

1. **High — the contract made a documented route impossible.** "Every `Agent` call
   names both keys … omitting either key is a defect" contradicted the
   no-effort-agent route the same file allows. **Cause worth keeping: the Opus pass
   had flagged the opposite asymmetry — only `model` omission was declared invalid —
   and the fix made both keys absolute, turning a gap into a contradiction.** Now
   separated: `model` is required in every case; `subagent_type` names a
   `kerd:effort-<level>` when the definitions are loaded, and otherwise a concrete
   ordinary `subagent_type` with effort *unset and unverified* and the reason
   disclosed. Mirrored in `orchestration.md`; guarded by a test that includes
   `assertNotIn("omitting either key is a defect")`.
2. **High — `requested_model: null` did not uniquely prove omission.** The field is
   initialised to null and unreadable metadata leaves it null with a gap, so an
   unqualified count could accuse a compliant dispatch. Null is now evidence only
   when the metadata parsed without a model-related gap, counted separately from the
   unverified. `test_job_evidence.py`'s case is renamed from "absent model is
   inherited" to "absent model is unspecified".
3. **High — request confused with execution.** "Never the one the plan chose" and "a
   slice planned for Haiku runs on Opus" are false when the fall-through happens to
   match. Corrected in all five agent files, `model-jobs.md`, `README.md` twice and
   this record. Codex also named `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`; verified against
   the docs rather than taken on trust, and it is **stronger** than reported — at `1`
   the host ignores the model field and a caller cannot pass a model at all. The same
   page documents `availableModels` substitution. Both are now in the guidance.
4. **Medium — README narrowed the contract to a "native Claude player"** while the
   release covers composers and reviewers. Widened; `planned player` no longer appears
   anywhere in the repo.
5. **Medium — `CONTEXT.md` still restored the refused hook design**, so the next
   Switch In could have revived the rejected subsystem while `TODO.md` restored the
   accepted one. Rewritten with the refusal, its quote, the out-of-scope list and
   "Do not revive them", plus the contract's ceiling and both review passes. Two
   further stale claims in that file were corrected in passing: installed-plugin
   state and the pickup reading set.

Codex confirmed the rejected finding was rightly rejected: "The dispatch grid is the
contract surface; duplicating model details in prose would not strengthen it." It
found no release-checklist or namespace blocker, and versions/capability lists
synchronized.

**The pattern across both reviews, worth carrying past this release:** every defect
in this release was a *calibration* defect, not a design defect — an absolute that
contradicted a route, a signature treated as proof, a request described as a
guarantee. The design Anthony set at 16:48 survived both passes untouched.

## What 0.133.0 is — Anthony's ruling, 2026-09-16 16:48

**The dispatch contract, made impossible to misunderstand at the point of use.**

```
Agent(
  subagent_type: "kerd:effort-high",
  model: "sonnet",
  ...
)
```

Anthony's wording, kept verbatim as the ruling:

- `model` chooses Haiku, Sonnet, Opus or Fable.
- `subagent_type` chooses the effort.
- The grid names both concretely before dispatch.
- "Per definition" or "inherited" is invalid for a planned Kerd player.
- `job_evidence.py` verifies what actually ran, afterward.

How the release states it, after two review passes tightened the claims — the ruling
is unchanged, its wording is made exact:

- `model` **requests** the model; `subagent_type` sets the effort. The request is
  what Kerd controls; a forced-model host setting or an `availableModels` allowlist
  can still decide what runs.
- The rule binds **every native Claude `Agent` call** — composer, player and
  reviewer — not the player role alone.
- `job_evidence.py` **reads and reports** the requested and observed values
  afterward; it returns `unverified` on any gap and proves nothing on its own.

Explicitly **not** in 0.133.0: a `PreToolUse` hook, a matcher framework, a
model×effort agent matrix. The palette drift is separate work.

## The design that was refused, and why it mattered

Claude proposed a `PreToolUse` hook that would deny a `kerd:effort-*` dispatch
carrying no explicit `model`. **Anthony refused it at 16:48: "It turns a missing
tool argument into a hook subsystem."** The refusal is the useful record — the
defect was a missing argument at the point of use, and the proposal answered it
with a subsystem, a registration format, a matcher and a test framework, none of
which the defect required. The superseded design and its three traps are kept
below because the `hooks.json` nesting trap and the four-alias enum remain true
facts about this host; they are just no longer this release's problem.

`direction.html` in this folder was redrawn to the agreed contract and carries the
fan-out evidence; it no longer draws the refused design.

## What the contract is for

A `kerd:effort-*` job dispatched through the `Agent` tool without an explicit
`model` runs on a model the call never selected — `CLAUDE_CODE_SUBAGENT_MODEL` when
it is set, the caller's model otherwise. Observed in the 2026-09-15/16 sitting:
`requested_model` null with `claude-opus-5` running, six times; Sonnet workers' own
sub-jobs came back `claude-sonnet-5` from the same agent definitions, which isolates
the fall-through as the mechanism rather than the agent files. A Seinn run burned
roughly 860K tokens on Opus for mechanical survey slices.

The countermeasure is the call itself: the model is named in the dispatch, so a plan
for Haiku cannot *silently* arrive as Opus — the row and the call would have to
disagree in writing. Be exact about the ceiling on that. Naming `model` is a
request, not a guarantee: with `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` set to `1` the
host ignores the field and a caller cannot pass a model at all, and an
organization's `availableModels` allowlist substitutes another version or the
inherited model for a blocked value. So a Haiku request can still run elsewhere with
the row and the call in perfect agreement. This is instruction text at the point of
use, not an enforcement mechanism — nothing blocks a dispatch mechanically, and
`job_evidence.py` is what reads, afterward, what actually ran.

## Facts corrected against the docs, 2026-09-16

Three claims carried in `TODO.md` from the refused design were checked against
[the subagent docs](https://code.claude.com/docs/en/sub-agents) and two were wrong.

1. **"An omitted `model` silently inherits the caller's" — only one of two
   branches.** The documented order is: the per-invocation `model`; then the
   definition's `model` frontmatter, where `inherit` selects the main
   conversation's model; then `CLAUDE_CODE_SUBAGENT_MODEL` when set to an alias or
   ID; then the main conversation's model. Kerd's effort definitions are model-free
   by test, so an omitted `model` lands on the environment variable when it is set
   and the caller's model when it is not. The first draft of this release asserted
   the caller's model as the mechanism in eight places **and pinned it with a new
   CI assertion** — the reviewer caught both.
2. **"Full model IDs cannot pass" — overstated.** The field accepts an alias or a
   full model ID. The four-alias enum is this host's `Agent` *tool parameter*, not
   the field itself. Kerd's guidance therefore asks for an alias unless a full ID
   is known to pass on the host, rather than claiming IDs are rejected.
3. **"`SendMessage` resume sits outside the guard" — wrong in the part that
   matters.** A resume carries no `subagent_type` and no new pair, but the
   per-invocation `model` from the original call keeps applying to a resume or
   follow-up. That is an argument for naming it at the first call, not a coverage
   gap. `hooks/hooks.json` nesting events under a `hooks` key remains true and is
   now simply out of scope.

## The review that shaped this release

An Opus job at high effort read the new wording adversarially against the 0.132.0
lesson — that the defect is a *class* of sentence handing the model an
unfalsifiable judgment. It returned eleven findings; all eleven were acted on.
The ones that changed the release's substance:

- the mechanism claim above, and the CI assertion pinning it;
- the contract said **player** while the same file enumerates composer, player and
  reviewer — a native Claude composer is the most expensive call Conductor makes
  and was uncovered. It is now anchored on the `Agent` call, not the role;
- **"planned" was the escape hatch**: a status the model assigns its own work.
  Replaced with "there is no unplanned dispatch — if you are calling `Agent`, the
  call is the plan";
- the controller exemption hung on the row's *label*, so `Controller: <delegated
  work>` could claim it. Now: exactly one row per grid, the row this session
  performs itself with no `Agent` call; a labelled row that dispatches is a
  mislabelled dispatch;
- **overclaim**: the draft called the prose "the guard" and said what ran "is
  verified". Neither is true — nothing blocks a dispatch mechanically and
  `job_evidence.py` returns `unverified` on any gap against an undocumented
  private format. The honest limit was in this record and had not reached the
  guidance; it has now;
- the **countable test** was missing. `requested_model: null` is the machine-readable
  signature of a call that omitted `model`, and the contract holds only at a count
  of zero. The reviewer found 104 of 577 subagent metadata files on this machine
  carry no `model` key;
- `orchestration.md` and `journey.md` had dropped the "native Claude" scope, making
  the rule unsatisfiable for a Codex row — the worst shape to hand a model, because
  it invents its own exemption. Scope restored, Codex rows given their own sentence.

**One finding was rejected with reason.** The reviewer flagged a progress example
in `journey.md` showing "Claude independently reviewing it" with no model named.
That is the person-facing plain-language progress list, not a dispatch row; the
grid carries route, model and effort by design. Cramming a model alias into it
would satisfy the letter of the contract and damage the thing the list is for.

## Release wording, when it comes

The contract makes the pair explicit **at dispatch** and proves nothing about what
a grid later claims. A static check cannot verify runtime prose, and the release
says so rather than implying enforcement.

## Record

- 2026-09-16, Switch In: position restored from `CONTEXT.md`, `TODO.md` `## Now`
  and `kivna/sessions/2026-09-16.md`. Continuation agreed by Anthony at 14:20,
  ownership settled at 14:21. Conductor opened for direction-setting on a picked
  "Yes — open direction-setting"; that pick did not approve this build.
- 2026-09-16 16:48, Anthony refused the hook design and set the contract above.
  Built in the same sitting: the five `agents/effort-*.md` descriptions, the
  dispatch contract in `skills/conductor/references/model-jobs.md`, the grid rule
  in `orchestration.md`, the grid note in `journey.md`, the Conductor trigger
  description, and tests in `test_effort_agents.py`. One real mixed-model fan-out
  (haiku/low, sonnet/medium, opus/high, each with an explicit model) was dispatched
  as the release's behavioural evidence.
- 2026-09-16, evidence: one mixed-model fan-out, three jobs in a single dispatch.
  Requested `haiku`/low, `sonnet`/medium, `opus`/high; observed
  `claude-haiku-4-5-20251001` (42 records), `claude-sonnet-5` (28, effort medium)
  and `claude-opus-5` (23, effort high). **The Haiku job returned no effort records
  at all**, so its requested effort is unverifiable rather than confirmed — recorded
  as a gap, not smoothed over. 728 tests green, `gate.py release` clean, hooks 21/21.
  A pre-existing import-order bug in `skills/switch/scripts/tests/test_roll_control.py`
  (it imports `roll_control` before inserting the path) means the suite only runs
  clean with `skills/switch/scripts` and its `tests/` dir on `PYTHONPATH`; unrelated
  to this change, and CI never runs these modules.
- 2026-09-16, drawing: Anthony corrected the skin mid-draw — Krutho blue is his
  brand, not Kerd's, and Kerd ships to anyone, so this view uses
  diagram-design's neutral default tokens. `docs/work/visual-communication/scope.html`
  still carries the Krutho palette; that is drift to fix, not a Kerd standard.
