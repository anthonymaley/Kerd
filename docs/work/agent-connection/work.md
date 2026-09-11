# Agent connection — native sessions and queues

## Direction

The producer asks Kerd to connect Claude and Codex bidirectionally using their
queues, not inbox infrastructure, and make that a core command. The addition on
2026-09-11 explicitly includes discovering sessions and starting both bounded
workers and full conversations that become pairing partners. Preserve existing
context when requested; a fresh independent reviewer is a deliberate choice.

Scope is Kerd. Apple-music and work-anthony supply evidence, not edit targets.
No installation, publication, Git commit/push or global settings change is
authorized by this implementation. Isolated native test sessions are in scope.

## Sources read

- The producer's work-anthony transcript: closing a busy Codex TUI then resuming
  its exact ID worked, but is not a safe automatic messaging route.
- The producer's apple-music transcript and the canonical vault `bin/ask-codex`
  v7: native Codex queue, one request/reply, archive before printing, resumable
  wait. The retired mailbox is not to be rebuilt.
- Vault: `Agent Request Skill Sketch.md`, `Claude Codex Collaboration Setup.md`,
  `Claude Codex Collaboration User Guide.md`.
- Kerd: `trials/software-session-routing.md`, current Conductor `ask.py` and
  model-job guidance; the accepted cross-LLM task trial in
  `trial-session-routing-03/docs/work/cross-llm-tasks/work.md`.

Correction: the existing managed-worker runner was accepted for a narrower
scope, including no attachment to already-open terminals. It is not evidence
of an unapproved downgrade. This work adds native partners alongside it.

## Implementation

`skills/agent/` adds the core command. No relay service, mailbox watcher or model
written reply files. Discovery reads metadata. Requests use native queues;
retrieval reads only new text in the chosen native transcript and privately
archives a request-marked answer. Existing workers reuse the accepted runner.

New partners are real native conversations. Claude's background launch chooses
its own ID; the adapter resolves the returned short ID against fresh native
discovery, not the requested UUID or latest session. Codex unloads dormant
threads; only adapter-created partners may be awakened under their exact ID.
An arbitrary user terminal is never stopped, forked or exec-resumed.

## Evidence so far

- Isolated Claude print session: socket-delivered second request recalled the
  marker from the first request under the same native session ID.
- Isolated Codex standard-input app-server: two native queue submissions,
  completion correlated with client request IDs, same session recalled its marker.
- Implemented command: new Codex native partner returned its first marked reply,
  then its exact dormant session resumed and returned the remembered marker.
- Implemented command: new Claude background partner returned its first marked
  reply, then received a native socket request and returned the remembered marker.
- Initial unit suite: 18 passing, including a real local Unix socket receiver,
  request matching, partial-answer refusal, duplicate prevention, wrong-project
  rejection, private storage and no retry after uncertain delivery.
- Final local connection suite: 27 passing. Existing Conductor suite: 37 passing.
  Existing Switch suite: 273 passing. Skill validation and whitespace check pass.
  The mechanical release gate is clean on the combined worktree; that is not
  approval to release this new command or a check of every native client.
- Productive queue use: the existing Claude Kerd session received the read-only
  review, read the new source and ran the tests, then returned six findings through
  the same session. Its returned message identifies `claude-opus-5`; effort was
  inherited and not observed. No fresh reviewer substituted for its context.

These are transport checks, not proof of productive collaboration quality,
all-app discovery, renderer visibility, or token savings. No such pass is awarded.

Problems found and corrected during implementation: Codex Unix transport is
WebSocket, not JSONL; the tested native server rejected the client's compression
offer, so compression is disabled; paginated Codex history does not support the
old includeTurns read used by the first probe; Claude background launch ignores
a supplied session UUID; Codex dormant threads are not live sessions. All failed
probes remained isolated. No existing user terminal was closed.

## Independent review disposition

The actual prompt is [review-prompt.md](review-prompt.md). The complete returned
answer and native binding remain private in Git metadata. Summary:

1. Reproduced: a reply spanning multiple assistant events was not retrieved.
   Fixed accumulation across events; tests retain the full ending for both
   providers, refuse incomplete JSON, and reject overlapping different replies.
2. Reproduced: a session opened in a project subdirectory was omitted. Fixed
   Git-root membership, with strict pre-send cwd identity checking retained.
   A nested Git repository remains excluded; containment alone was insufficient.
3. Disclosure gap: explicitly named `crossSessionInbound: accept`, its lifetime,
   other-local-sender scope, disabled permission prompts and tool limits for new
   Claude partners. Existing partner settings remain untouched.
4. Normalized discovered status to strings across providers; saved launch status
   and observed live status stay separate.
5. Unmeasured scaling risk: added a shared five-second Codex discovery budget
   with partial results, and direct lookup for an exact selected target. This
   is not an invented work allowance or a measured performance comparison.
6. Failed-start retry now reports the used alias with an actionable message,
   not a raw errno/private path. It still never relaunches automatically.

Corrections were verified with focused regression checks locally, not another
claimed independent pass. The reviewer offered no producer acceptance verdict.

The two isolated Claude background sessions were stopped using their verified
native test IDs. The Codex server started solely for these tests was stopped
after checking it held no loaded threads. Native histories and temporary private
test evidence remain; no history was deleted. The existing Kerd Claude session
was neither stopped nor reconfigured.

## User help

Added the [user guide](../../../skills/agent/references/user-guide.md) at the
producer's request: everyday requests, choosing a partner or worker, first-use
setup, visible handoffs and unavailable routes. `/kerd:agent help` routes to
the short help list without starting discovery or a job. Detailed command
patterns remain in the existing native-sessions reference rather than being
duplicated. The skill-creator guidance shaped that short-help-first routing.

The helper's `--help` now describes all six commands and distinguishes worker
retrieval from partner retrieval. All seven help entry points (top level and
six commands) were exercised outside a Git repository with no provider tools
on PATH: exit 0, no stderr and no files created. Connection suite: 28 passing;
skill validation and whitespace check pass. Conversational help routing is
instructional; these checks do not prove it has appeared in an installed client.
No release files, installations or live partner sessions were changed for help.

## Combined release review — 2026-09-11

The producer authorized review, correction and release, then explicitly chose
one combined 0.108.0 release with the pending Switch/Conductor work instead of
an Agent-only release. The [combined prompt](combined-review-prompt.md)
supersedes the [earlier split proposal](release-review-prompt.md).

The established Claude Kerd partner returned the review through the native
request. Observed model: claude-opus-5; effort retained and unobserved. It
reran 28 Agent checks, seven help paths and isolated reproductions, confirming
the earlier reply-completeness and project-membership fixes. It reported no
new Agent code defect. It found incomplete release surfaces and a real routing
collision: Conductor could choose its older fresh-worker route for a direct
request meant for an established partner.

Corrections: Conductor now delegates session choice to Agent without a recursive
handoff when Agent reads the prompt guide. The existing runner remains the
deliberate worker route. README's count, Agent section and 0.108.0 release notes,
CLAUDE.md's count and both capability descriptions include the new skill. Existing
Switch release notes are retained, with orientation cost explicitly unmeasured.

The live review also exposed a controller follow-through failure: inbound policy
held the message, and the controller ended its turn without retrieving the
eventual answer before the producer pasted it. Native retrieval subsequently
returned that complete answer. Dispatch is not completion; the skill now keeps
the request pending, retrieves it on return from a permission blocker, and names
the lack of a background wakeup mechanism. Setup help explains per-message,
session-only and user-wide inbound choices without changing any setting.

## Now

Stage: Release preparation

Current activity: hand the integrated 0.108.0 release to the established Claude
Kerd partner, as the producer explicitly requested. Codex stops editing before
dispatch and remains responsible for retrieving the release result. The exact
scope and checks are in [release-handoff.md](release-handoff.md).

Pending question: none.

Next action: confirm in ordinary use that the published release reaches installed
plugins; publication is not installation, and neither is a use-quality pass.
Installation and ordinary-use experience remain separate observations. The
three-skill controlled-trial package has not been expanded to include Agent.

Remaining limits: discovery covers Claude native listings and Codex shared-server
threads, not every desktop/IDE backend. Claude partner launcher has file tools,
not Bash/nested delegation. Existing partners retain their own permissions.
Answer markers/native logs are a cooperative, version-sensitive retrieval route.
The optional WebSocket dependency has only been installed in the temporary test
environment, not globally or in a consumer project. Native test sessions and
their private records are not production pairing assignments.
