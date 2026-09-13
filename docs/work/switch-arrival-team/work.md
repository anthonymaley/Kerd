# Visible pairing at arrival

## Now

Outcome: Switch In makes the established team recognizable and tells those
partners when the current native identity arrives, without starting work.
Stage: Complete — implementation and independent review for 0.119.0.
Source boundary: main, “Release Kerd 0.119.0: visible team and recommended next action”.
This account is saved with the release; remote publication and CI are checked
after saving, not pre-asserted inside this commit.
Owner: Codex implements Agent/Switch and tests. Established Claude partner
reviews read-only; its separate shared verification record stays under its ownership.
Next action: observe the next ordinary arrival after confirming the client loaded
0.119.0. Anthony authorized “whe done work with claude to release”; Codex owns
the source save/push and remote CI check, Claude the independent review. No
plugin installation or consumer work is included in that release authority.
Pending question: none.

## Agreement

Anthony supplied the ordinary Claude 0.118.0 arrival on Kerd: numbered NOW and
the question after END were visible, but pairing was buried in ATTENTION. He
asked for session IDs and a notice saying “im online, new switch in and new id,
no need to reply”, then authorized “yes lets do these chnages”. The agreed
wording distinguishes a restored identity from a peer being online.

- TEAM belongs in the existing completion box: provider, role and short native
  ID, with colliding prefixes lengthened and repeated identities grouped.
- Exact IDs stay private and accessible through Agent, not tracked rosters.
- After self identity and routing are restored, send an informational notice to
  established partners. No discovered-session broadcast, task, reply, automatic retry,
  acknowledgement wait, binding mutation or dormant-session resume.
- Deduplicate by sender and recipient provider/ID pair in the existing private
  request store. Same-ID clears/repeated In reuse the result; new IDs permit a
  new notice. This is identity announcement, not a presence heartbeat.
- Missing/uncertain delivery is visible; it cannot turn complete memory into
  incomplete pickup or claim the peer is available. Native receipt may trigger
  a model turn or be held: no promise of zero token cost or silent delivery.

Implementation interpretation, not a separate quoted ruling: explicit restored
peer selection wins; otherwise read the already-existing private bindings and
apply the unambiguous-partner default described below. This replaces the first
draft's context-only recipient rule, which a fresh Kerd pickup could not follow.
It does not establish a new partner, change any role or send to every binding.
The choice is disclosed for release preparation; ambiguous recipients remain
unsent rather than becoming an arrival setup stop.

## Implementation and evidence

Agent's `arrival` command takes the actual provider, an optional restored self
role alias and optional selected peer aliases. With no explicit peer selection,
the helper uses unambiguous private pairing, preferring a recorded ongoing role,
otherwise a unique other-provider identity. Same-provider contacts without roles
are not default peers; competing eligible identities remain unresolved. A missing
role does not erase an established unique partner or invent its responsibility.
It verifies self identity and the
self-role match, checks project-local peer bindings, and sends via the existing
native transport with no reply envelope or transcript reads. `status`/`wait`
recognize the no-reply receipt and return without waiting. Bindings are not
rewritten. It excludes self's retired IDs, workers and unassigned owned launches;
a role-bearing persistent owned partner is not a worker and is never resumed
for an arrival notice.

Switch passes the returned `team` directly to its documented summary shape.
The renderer shows TEAM and notice status in chat and terminal, preserving the
single question after END and the numbered NOW list. No current peer IDs are
stored in this account.

Focused checks after review: 24 Agent arrival tests and 120 renderer tests passed
(`python3 -B -m unittest discover -s <skill>/scripts/tests -p <test_file>`).
Coverage includes both send adapters, no reply protocol/history reads, duplicate
aliases and concurrent retry, same/new sender and recipient IDs, uncertain and
offline outcomes, missing identity, wrong role/project, unselected historical
bindings, no peers, help without provider tools, short-ID collisions, wrapping
and unknown versus empty team. These are fixture results, not live delivery or
proof of model compliance. Additional probes exercise the real transport methods
with native sockets/CLI/RPC mocked at their boundaries: pre-enqueue refusal versus
uncertainty, both Codex queue paths and no resume, Claude metadata refusal versus
socket-write failure. No real arrival notice has been sent by these tests.

The first full run passed Agent 157, Switch 328, Conductor 37, packaging 9 and
hooks 21 (optional shellcheck unavailable); gate selftest 57 plus root resolution
7, release gate and both skill validators passed. Audit retained its existing
requirements trace finding. The full corrected run passed Agent 167, Switch 329
and packaging 9. After the final exec-refusal test and unresolved-slot wording,
Agent 168, renderer 120 and packaging 9 passed again, as did release, both skill
validators and the diff whitespace check. The unchanged non-renderer Switch tests
were not repeated after that final wording correction.

## Independent review and disposition

Claude returned eight findings. Accepted: an executable recipient rule for a
fresh context, retired/temporary recipient exclusion, pre-send refusal versus
uncertainty, visible reuse with original time, consistent unavailable status,
notice-ID rejection by `ask`, avoiding a binding lock across native delivery,
and explicit clear-versus-ID semantics. Exact target is captured under the lock;
subsequent sends retain that target, as existing queued contributions do, and
cannot change bindings on receipt. A concurrent succession may move the alias
after capture; later work resolves it anew.

Two qualifications: requiring a role for every peer would exclude Kerd's already
established Codex partner merely because its role field is absent; the unique
cross-provider fallback preserves it without changing its binding. `owned` means
Kerd launched a persistent partner, not necessarily a worker; owned sessions with
an explicit partner role remain eligible without permission to wake them.

Codex also reproduced and corrected malformed partner objects raising a traceback
instead of returning an unresolved row. The review's standalone renderer count
was 35 because its `unittest.main()` guard precedes later classes; discovery ran
119 before corrections and 120 now. Test discovery is the verification command;
the pre-existing standalone guard is not moved as part of this change.

Claude's reassessment: ready for release preparation; both recipient-selection
qualifications accepted after its own metadata-only Kerd probe. Codex independently
ran that probe too: each provider selects the expected opposite partner without
native calls, writes or notices. This establishes selection, not peer availability.
Three small corrections followed: a missing/nonexecutable Codex CLI is a known
pre-exec refusal, not uncertainty; an unresolved TEAM slot says recipient not
selected; this account distinguishes the implemented default from Anthony's
quoted request. The same-ID/no-reply and all earlier restrictions remain.

Final Claude confirmation received: all three corrections independently checked,
Agent 168 and renderer 120 passed again, no consequential finding remains.
The reviewer retained this contribution account for its next owned Out. Optional
wording remains: a missing explicit alias says recipient not selected rather than
unresolved, but its PEER error gives the actual missing-binding reason.

Review prompt uses the local Claude Opus 5 profile (2026-09), scoped original
agreement and artifacts. Established partner retained; no model/effort change
requested. Normal review traffic is distinct from testing the arrival notice.

## YOU recommendation refinement

Anthony supplied Seinn's 0.118.0 YOU box: a dense paragraph and a confusing REPLY
menu. He explicitly rejected a compound question offering “now or later” and
approved “yes, lets tweak YOU with recommendations”. The renderer now shows a
RECOMMENDED heading, paragraph spacing and caller-supplied numbered/bulleted
steps with hanging indents. It does not invent steps from prose or turn the
checklist into answer choices. The scope remains separate and complete. Legacy
`question.reply` is accepted but not displayed. The question remains once after
END in chat, and no question is invented for a no-action arrival.

Switch and Conductor guidance now ask one direct question about the recommendation,
without appended alternatives or a routine reply menu. A factual answer remains
a fact; agreeing to do a human check is not evidence it passed. This is not a
delegation-policy change: the Apple Music report remains separate evidence of
skipping the split decision, not permission to redesign delegation here.

Renderer discovery: 125 passed (five new recommendation tests), including complete
steps/limits, spacing, hanging indents, narrow/wide-character wrapping, legacy
single-paragraph inputs and suppression of old reply menus. The generic legacy
record view is unchanged; this adjustment covers Switch's dashboard modes.

Release checklist: 0.119.0 in all three fields; new README entry and current
usage updated; changed skill descriptions checked. The high-level capability
lists remain accurate and identical: this extends existing collaboration and
handoff, not a new skill. Publication and remote CI are checked after saving,
never asserted inside the commit that will save this account.

Final combined review: Claude independently ran Switch 334, Agent 168, Conductor
37 and the release gate, plus five narrow/standard chat/terminal render cases.
It found one remaining contradictory Correct / Change instruction in Conductor;
the line was corrected as requested, with no further review required by Claude.
All proposal words, scope limits and list markers survived; no old reply menu,
duplicate question or invented step appeared. Full Codex checks: Switch 334,
Agent 168, Conductor 37, packaging 9, hooks 21, all CI steps and skill validators.
The pre-save fidelity command skipped because existing HEAD was not a boundary
commit; this is not claimed as a successful boundary-fidelity observation.

Contribution coverage: Codex implementation/checks plus Claude review and final
delta captured here. Claude also reported its 0.118.0 arrival/adoption and owns
the corresponding shared verification-record update after this release. Its
assessment/report is not promoted into verified human acceptance. No separate
shared-file closeout was performed by Codex, and no live notice was sent.

## Next ordinary observation

After review and an explicitly authorized release/install, the next ordinary In
should show the correct team/IDs and notice outcome without waiting or starting
work. Compare the receiver's native notice with the sender's retained receipt
only if live delivery needs verification. Human judgement remains the dashboard
experience; fixtures cover mechanics without requiring Anthony to supervise them.
