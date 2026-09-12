# Kerd follow-up: a clear arrival and dependable review results

## Now

Status: implemented locally and reviewed by Claude (verdict: ready for the
release checklist as a MINOR bump after three wording fixes, which Claude made);
Codex reviewed Claude's new Out box and the release diff (four findings, fixed).
Release as 0.112.0 prepared by Claude; not yet committed or pushed at the time
of this line.

User request, 2026-09-12: "go ahead and spec he changes needed and get the paired
claude session to review". Scope: Kerd only. The supplied Leru pickup is experience
evidence, not permission to design its alert, edit Leru or deploy anything.

This specification covers the arrival defects in that example and the five
reproduced findings from the review of 0.109.0 through 0.111.0 at `b139519`.
Subsequent authority: the person chose Codex to implement and Claude to review,
then said "do it". Installation, a version bump, commit and publication remain
outside this step.

## Intended result

One useful arrival dashboard: what happened, the next bounded action, where that
action sits, and whether the person is needed. Conductor is loaded, but no work
starts during ordinary In. An Agent review is complete only when the actual
marked answer has been retrieved. Memory stays reachable and size reporting
does not double-count the same selection.

Keep the existing skills, renderer, native queues and project memory. No new
tracker, inbox, background service, approval framework or record schema.

## Evidence and limits

The pasted Leru pickup visibly loaded `Skill(kerd:conductor)` and stopped on an
approval question. That is useful evidence for entry and the stop boundary.
It also:

- Said "Nothing needs you right now" before asking for approval.
- Marked Shape and Agree done and Deliver current, while saying the selected
  alert's shape had not been designed. Agreement to priority is not agreement
  to a design or to deployment.
- Displayed the same seven items in NOW and a second fallback task list.
- Called Conductor a candidate and asserted that the terminal shows only the
  final message. Neither the installed version nor that client behaviour can
  be established from this paste. These are observations to check, not proved
  cache or host failures.

The source project and its logs were not inspected. No measured duration or
token count accompanied the example; do not award a speed or token-saving pass.

## A. Compose arrival once, with one honest decision

Change the existing In instructions in `skills/conductor/SKILL.md`, with short
references from Switch's `references/in-out.md` and Conductor's journey guide.
This corrects the 0.110.0 two-step arrival: rendering "Nothing needs you" before
Conductor asks for approval gives conflicting answers to the same question.
Compose them together and delete the second report; do not add another ceremony.

1. Restore the named reading set, then load Conductor from the same distribution
   before finalizing the dashboard summary. Reuse the restored material; do not
   perform a second pickup or design the work during In.
2. Select the next action using the existing precedence: saved next action,
   otherwise first NOW item, otherwise explicitly no selected task. Preserve a
   genuine pending question instead of manufacturing a second approval.
3. Preserve the saved next action's wording and authority; do not expand it
   into all later work. Name the next *bounded action*. If the selected item's
   design is unresolved, propose designing it. Do not turn "design the alert"
   into "design, build and deploy". A yes grants only the stated action within
   existing boundaries; separate unresolved authority still matters.
4. PHASE and any journey indication describe the selected work, with no completed
   tick unsupported by its record; distinguish a programme's stage only when
   needed, and leave unknown stages unknown.
5. Use the existing summary `question` object for the real arrival decision.
   If ordinary In will wait for approval, YOU must say that and carry the same
   action and scope as STATE/THIS SESSION. Never show "Nothing needs you" while
   requiring an answer elsewhere. THIS SESSION says "Proposed" until this
   sitting's action is authorized, distinguishing any previously agreed plan.
6. Put the one actionable question inside the YOU box. If the host requires a
   plain-text question, keep the scope in YOU and ask it immediately below,
   once. Replace the rule requiring a second trailing approval line after the
   dashboard; retain the deliberate arrival approval itself. An explicit
   current request to continue keeps its existing exception, as do managed To
   and Roll. No selected task means no fabricated approval question.
7. Conductor owns the continuation after approval, without printing a second
   brief, full journey and duplicate text task list. Use native task tools when
   exposed. Otherwise NOW is the fallback list; do not repeat it below. Detail
   stays behind real document links. Preserve the current colour fallbacks.
8. Use the current skill's identity wording, already corrected in 0.110.1.
   Do not add cache diagnosis to In or explain visibility using an untested
   client limitation. Installation troubleshooting is separate work.

Illustrative content for the supplied case, not a new Leru agreement:

```text
PHASE  Design needed — manifest-staleness alert
TASK   Design the alert
STATE  Awaiting your approval

THIS SESSION
  Proposed: decide where the alert runs, what it checks and how it notifies
  you. Implementation and deployment are not included in this approval.

YOU
  Starting on the alert design — approve?
```

This is a content example inside the existing dashboard, not another renderer
or a prescription to drop Last session, NOW, restrictions or document links.
In the actual pickup, carry forward any existing permission without weakening
it or manufacturing a new grant. No new renderer fields are needed: the current
question/proposal/reply fields can carry this content.

Acceptance: render the Leru-shaped summary with the existing renderer, including
unknown stage, selected-but-not-approved design, already-approved continuation,
real pending question and no-selected-task cases. Assert complete decision and
scope text reaches YOU. Read the resulting arrival as one whole response:
no "nothing needed" plus an approval, no unsupported completed stages, no
duplicate fallback list, no implementation during In. Script fixtures establish
rendering, not that an LLM follows the guide. Leave ordinary-use experience and
actual pickup cost unassessed until observed; do not commission a consumer job
merely to pass this specification.

## B. Correct the five release-review findings

### 1. Agent must not archive a marker mention as the review

Source: `skills/agent/scripts/agent.py`, `_status`, around lines 740–756.
Reproduction using existing QueueTests fixtures: append an assistant message
`I will use <opening marker> and <closing marker>`, then a separate ordinary
update. The first status is unconfirmed; the second becomes `reply-received`
with `reply = "and"`. A subsequent real reply is ignored because completion is
cached. Reproduced with Claude events and Codex final-answer events.

The cause is the trim at `collected = begin + collected.rsplit(begin, 1)[1]`:
it discards the prefix that proved the marker was inline. Preserve the opening
marker's actual line boundary across events. A minimal correction is to retain
the marker's whole line when trimming, not start the buffer at the marker.
Trimming must not turn a rejected inline mention into a valid opening on the
next iteration. Ignore rejected mentions and accept a later valid complete
reply. Keep split replies, message-ID joining, overlapping-request refusal,
Codex phase filtering and archive-before-return behaviour. The reproduction's
closing marker ends its message; retain a separate trailing-prose rejection case.

Tests: mention followed by unrelated text remains pending for both providers;
the later genuine reply is retrieved in full; a valid opening split across
events still works; unrelated request markers never complete this request.
Repeat the case with a status call between fragments and without one. No real
session dispatch is needed for these regression tests.

### 2. Restore portable packaging after the guidance move

Source: `docs/work/model-ready-work/packaging/build.py`, `inputs()` line 23.
It still adds the removed pack-root `guidance/`. Three of five tests fail with
`Missing or linked source directory: guidance`.

Consume guidance from its canonical home under
`skills/conductor/references/guidance/`, already included in the skill tree.
Remove the obsolete source and update packaging instructions/START references
to the actual shipped layout. Keep the supported three-skill package; adding
Agent is not part of this correction. Do not create another guidance copy.

Tests: all five packaging checks; a build into a fresh temporary `kerd/`
directory; relocated Conductor guidance links resolve with the source checkout
out of scope. Missing Agent remains an explicit unavailable partner route.

### 3. Measure unique, normalized selections

Source: `skills/switch/scripts/handoff.py`, `measure()` lines 271–281.
`--record CONTEXT.md --file ./CONTEXT.md` counts one 9,254-byte file twice.

Validate and normalize project-relative paths and heading whitespace using the
same semantics as the reader, then reject duplicate selections. Preserve the
current explicit duplicate refusal, not silent deduplication. Do not add a
tokenizer or claim this measures host overhead or actual input tokens.

Tests: exact duplicates, `./` aliases and headings differing only by accepted
trailing whitespace are refused. Distinct sections still work; existing path,
symlink, source-preservation and nonblocking over-target checks keep passing.
Whole-file plus subsection overlap should be named in output/documentation as
overlap if retained; it is not evidence of unique context loaded once.

### 4. Finish the memory move's living pointers

Example: TODO.md line 86 says the question-set-staleness mechanism and rejected
alternatives are verbatim in CONTEXT.md, but that case moved to docs/decisions.md.

Search living references across the whole TODO Backlog and `docs/product/`,
not just the example row; read each relevant match in context and repoint moved
entries by subject to their actual home. Leave valid CONTEXT references alone,
such as its still-existing Open Questions section. Keep entry dates and rationale
intact; do not rewrite dated logs or re-adjudicate unrelated backlog rows. This
is a pointer repair, not another closure review. A generic archive link alone
does not make an explicitly incorrect per-item pointer correct.

Checks: follow each changed pointer to the complete intended entry; compare
moved cases against the pre-migration source. The earlier review found 153/156
old entries byte-identical and small command-wording edits in the other three;
do not widen that into a claim that all retained rulings are semantically enough
for every future project.

### 5. Refuse known oversized Claude sends before recording delivery

Source: `Agent.ask()` creates a request before `send_claude()` checks frame size.
An oversized prompt produces a retained `delivery-uncertain` request despite no
socket attempt. The current test calls only `send_claude()`, missing this path.

Build and validate the exact serialized Claude frame before creating the request
JSON or attempting delivery. Share that calculation with the sender so Unicode,
escaping and envelope size cannot drift. Validate once before send, retaining
the existing uncertainty record for an actual attempted transport operation.
Retry lookup for an already recorded request remains idempotent. No new status
taxonomy is needed. Clarify that the frame cap describes the Claude socket
route; do not imply identical Codex CLI limits.

Tests through the real `Agent.ask()` path with the socket mocked: oversized
input returns a local refusal, writes no request JSON and makes no socket call;
normal messages still send once; a transport timeout remains recorded and is
never automatically resent. A guard/lock file is not a delivery record; describe
that distinction honestly rather than promising no filesystem side effects.

## Implementation order and verification

If implementation is subsequently authorized: fix false review completion
first; then arrival guidance and its composed example; packaging, measurement,
living pointers and size preflight follow. Keep changes bounded to the named
surfaces and their tests. Run Agent, Conductor, Switch and packaging suites;
release/audit/selftest/root-resolution and hook checks for integration.

Before any later release, follow the existing version/README checklist and
obtain publication authority. The changed arrival behaviour requires a minor
release under Kerd's current convention, with README and Switch's In description
updated alongside the canonical Conductor rule. No version is reserved here.
No global configuration, consumer repo, preserved local file, session lifecycle
or transport permission change is included.

## Review

Requested: contextual review by the available Kerd Claude partner, preserving
its current model/effort and permissions. Prompt uses the local shared-Claude
2026-09 guidance (bounded outcome, sources and scope); no tuned-model or observed
effort claim. Review should challenge the proposed behaviour and reproduce
technical findings, not approve the user's experience or implement changes.

Dispatch: sent once to the available Kerd Claude session after the user's go-ahead;
the old unavailable partner binding was not overwritten. Initial delivery was
unconfirmed and the recipient showed a permission wait. Typed approvals then
resumed its other saved work. When the user requested a resend, a final status
check found the complete review already received, so no duplicate was sent.
No inbound-setting change was made.

Local check: the existing renderer rendered the proposed design-only approval
at 78 columns without new fields. Assertions confirmed the complete scope text,
one approval question and absence of "Nothing needs you right now". This is a
content check, not a live-client visibility or ordinary-pickup result.

Reviewer: Claude Fable 5.1 (identity observed in the returned assistant event;
effort not independently observed), the contextual Kerd partner and author of
0.110.0–0.111.0, not a fresh blind reviewer. Full response retained in Agent's
private request record. It reported reproducing all five technical findings
using isolated fixtures and judged the spec ready with tightenings.

Dispositions:

- Accepted: identify the exact buffer trim causing B1 and preserve the line
  prefix; require the later real answer to remain retrievable for both providers.
- Accepted: describe A as a correction of two conflicting arrival surfaces;
  select before rendering and remove the duplicate report. Reuse existing fields.
- Accepted: preserve the saved action's scope, shorten stage guidance, and omit
  cache diagnosis. Do not claim this paste identifies an installed version.
- Accepted: search the living Backlog/product references, not just one row,
  while preserving valid pointers and leaving closure judgments out of scope.
- Accepted: name the minor-release/README/skill-description consequences without
  reserving or authorizing a release.
- Not adopted: the review's passing assertion that Leru ran an older cache.
  It later qualified that version as unknown; the paste alone cannot establish it.
  The duplicated text lists are visible; native task-tool availability is not.

Review complete. The changes above tighten the reviewed proposal rather than
introduce a new work package. No second model round is required to repeat it.
The person subsequently authorized implementation; progress follows below.

## Implementation — 2026-09-12

Implemented by Codex. Agent retains the opening marker's line prefix and checks
the exact Claude frame before a request JSON exists. Switch rejects normalized
duplicate selections and labels overlap in its counting method. Packaging reads
the canonical guidance from Conductor's tree. Arrival is composed before one
render, with its actual decision in YOU; the renderer itself needed no change.
Living TODO/product pointers now lead to the moved cases. Historical observations
about CONTEXT and its valid current-state pointers remain; no backlog verdicts
were changed.

Regression tests failed against the old marker, size-preflight and measurement
behaviour before the corrections. Checks after changes: Agent 117, Switch 286,
Conductor 37, packaging 5 passed, including Claude timeout retention without
resend. All 33 relative file links in the changed Markdown resolve. Release
mechanical check clean; audit clean with its pre-existing
trace gap; gate selftest 57, root resolution 7 and hooks 21 passed (shellcheck
unavailable). Conductor and Switch skill validation passed. The first audit
caught Markdown links in grounding source lines, which require bare repo paths;
those were corrected without changing the gate.

Review: one implementation request sent to the same contextual Claude partner;
it waited at a native permission prompt until Anthony accepted peer messages,
then Claude answered from the retained request. Outcome (2026-09-12, retrieved
by marker from Claude's transcript): all five fixes verified by Claude's own
reproductions; no code defect; three wording findings — the In ordering stated
three ways (heading, anchor and "Then open"), a README full stop, and an edit
to the released 0.109.0 note — all made by Claude in the 0.112.0 preparation.
The separate closure-review trial and preserved root patch belong to other
work and were not edited by this implementation.

Still not observed: a fresh ordinary pickup's user experience, client colours,
or actual token savings. No consumer repo, global configuration, version field,
session lifecycle or native permission setting changed.
