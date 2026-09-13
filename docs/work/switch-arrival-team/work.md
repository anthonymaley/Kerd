# Visible pairing at arrival

## Now

Outcome: Switch In makes the established team recognizable and tells those
partners when the current native identity arrives, without starting work.
Stage: Complete — compact arrival follow-up implemented, reviewed and released as 0.120.0.
Source boundary: main, “Release Kerd 0.120.0: compact arrival without YOU”.
This account is saved with the release; remote publication and CI are checked
after saving, not pre-asserted inside this commit.
Owner: Codex implemented Agent/Switch and tests. The established Claude partner
reviewed read-only and published 0.120.0 on Anthony's direct “lets release”
(2026-09-13 16:51), after Codex confirmed its edits finished and that it would
not release in parallel. Claude's separate shared verification record stays
under its ownership.
Next action: a fresh Claude session loads 0.120.0 and shows the compact arrival
for Anthony's assessment. Publication does not update an installed plugin cache;
no install or Codex update is authorized. Anthony approved the implementation
with “perfect - okay lets do it”; approving it is not his assessment of the
arrival in ordinary use. The earlier 0.119.0 release is history, not this
boundary.
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

## Compact arrival follow-up (2026-09-13, local)

Anthony's assessment of the ordinary 0.119.0 arrival changed the presentation:
remove YOU entirely; put known owners against pressing actions and logical next
steps in numbered NOW, rather than listing evidence rows. TEAM becomes one
provider/role line. IDs and routine notice state stay in Agent details; surface
only routing problems consequential to the next action in ATTENTION. The actual
question comes once after END as `> 💬 **Question?**`. Do not add alternatives.
These supersede the earlier display agreement above, not its routing safeguards.

Codex received the preceding Claude arrival notice in this conversation and did
not acknowledge it or start work. This confirms that notice's receipt only, not
general availability or acceptance. Anthony's revised display preferences are
the evidence for this change, not a generic passed dashboard verdict.

Implementation changes dashboard rendering and living Switch/Conductor/Agent
display guidance only. No new schema, roster, transport, bindings or workflow.
The caller supplies faithful brief role labels and known owners; the renderer
does not invent them. Old `question.proposed` values keep their full scope below
NOW; new inputs leave it null and keep limits in the actions or THIS SESSION.
Legacy non-dashboard record view and Out completion rendering are unchanged.

131 renderer tests pass, including compact identity grouping, actual helper
undefined-role wording, explicit owner emphasis, ordinary colon text not treated
as an owner, escaped question text, no-question arrivals and full old-input scope
and Markdown list structure. Full Switch 340 and Conductor 37 passed.
Release gate and skill validators pass; audit retains its pre-existing trace gap.
These checks are not a release, installation or user experience verdict.

Claude returned five supported findings: ordinary colon text had been styled as
owners; README Day to day still named YOU; Conductor's generic blockquote ban
conflicted with arrival; old proposals lost Markdown list layout; real helper
undefined-role text produced nested parentheses. All corrected, with regression
checks for the behavior changes. Explicit `**Owner:** action` is display notation
inside the existing NOW string, not a new record field or owner assignment.

One proposed correction was declined: automatically showing every failed notice.
Anthony agreed that only routing problems affecting the next action belong in
ATTENTION. The caller sees the plan and receipt, so supplies that warning when
consequential; a failed greeting alone cannot establish it. Agent retains the
error/receipt. A test verifies supplied routing warnings are not lost. This is
an intentional caller judgment, not a promise that every failed notice appears.
Claude rechecked the corrections read-only and cleared the local implementation,
not publication. It independently reran 131 renderer tests, checked owner syntax
and near misses, old proposal structure, actual undefined-role wording and both
guidance corrections. It withdrew the unconditional notice-warning finding as
contrary to Anthony's agreed display scope. Profile used:
Opus 5 2026-09, existing native model/effort unchanged; observed model is recorded
as claude-opus-5 by the reply metadata; applied effort remains unobserved.

Non-blocking display limit retained: an old proposal with a restriction directly
after a list and no blank line is treated by Markdown as continuation of the last
item. Its full text survives; the documented blank-line shape renders separately.
No known caller evidence requires another formatting rule. No shared handoff,
verification-record, binding or installed-plugin changes were made in this task.
