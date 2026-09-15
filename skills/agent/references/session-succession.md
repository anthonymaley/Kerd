# Keep the role, verify the session

Use only for an existing local pairing during Switch In/Out or an explicitly
selected role replacement. The shared Markdown holds the work and handoff;
native IDs stay in the existing Git-private Agent binding. No new roster.
Resolve `scripts/agent.py` from this Agent skill, with the current project.
The commands below abbreviate that prefix as `agent.py --project /PROJECT`.

## Identity first

Run `agent.py --project /PROJECT identity --provider claude` (or `codex`).
Choose the provider of this actual host, not an inherited peer variable. It
reads `CLAUDE_CODE_SESSION_ID` or `CODEX_THREAD_ID` and corroborates the exact
ID against native project metadata. It writes nothing, sends nothing and never
chooses the newest session. Missing or stale identity stays unresolved. Use a
current host tool process: an older MCP process can retain an obsolete ID.
Claude documents its ID changing on `/clear`; compare IDs rather than guessing
from terminal lifetime. Codex TUI membership is not a heartbeat.

## Out: designate this role's continuation

Before editing the handoff account, check this Out owner's existing role binding.
Read only the project's private partner metadata; no binding means skip this
step, not compulsory Agent setup. Verify this host's current identity using
`identity` above and compare it with the intended role's bound ID. Out ownership
is the person's choice of who saves; it does not itself grant a pairing role.

If the IDs match, retain the alias and recorded role without re-pairing. A second
contact alias for the same ID is not another role to designate. If they differ,
use an already-established role replacement choice from this conversation:
`adopt --provider ... --alias ... --expected-session ... --confirm-replacement`.
Do not ask the person to repeat that explicit choice. Without such a choice,
use the In adoption/recovery path below only when this session is the intended
pickup of a matching saved designation or receipt and has restored that account.
Do this before rewriting its bytes. Never substitute a convenient current file,
infer selection from an absent peer, or run `--confirm-replacement` merely because
Out was requested. Unknown identity, a competing update or genuinely ambiguous
role leaves routing unchanged. When only pairing continuity is unresolved,
complete the safe memory save and put the unresolved choice in the closing next
action; do not add a pre-save approval stop. Report role continuation unavailable.

After any adoption, read its result: the intended alias must name this verified
ID and retain its recorded role. Do not create a role, transfer another
contributor's role, or replace an owned launch partner as an Out prerequisite.
Keep IDs private. This pre-save check settles who can designate; it does not yet
designate a successor or prove the necessary session memory was saved.

After the final handoff file is saved and necessary memory is ready, prepare
the existing alias belonging to this verified session:

```sh
agent.py --project /PROJECT handoff --provider claude --alias ROLE_ALIAS --record CONTEXT.md
```

This designates the session restoring this handoff at Switch In to continue
the role. The helper cannot distinguish that intended pickup from another
same-project session holding the same record; a second adopter refuses on the
changed expected ID. A session not performing that pickup must not run adopt.
Use the final saved pointer (`CONTEXT.md` by convention), not a changing scratch
plan. Its relative path and content
digest bind the designation to that saved account; later edits invalidate it.
Never prepare another contributor's binding on its behalf. Reuse the selected
alias; when several roles could be transferred, resolve which before writing.
No existing binding means no compulsory pairing during Out. The command records
no future ID and does not end a process or stop its jobs. A failed designation
leaves the saved work intact; disclose that automatic pairing pickup is unavailable.
Report designation succeeded, unavailable with its reason, or not applicable
in the closing box's existing `next` text, alongside the intact saved next action
and separately from Git save and memory readiness. If the
pre-save ownership check was unresolved, do not attempt designation anyway.
If this session resumes work instead of handing over, revoke the designation
with `handoff --provider claude --alias ROLE_ALIAS --cancel` before that work.

## In: keep, adopt or recover, then stop at the dashboard

Restore the designated handoff before changing routing. Reuse the role selected
by that handoff or by the person; same cwd, provider, title, latest activity or
an old binding's existence does not select a successor. If that choice is clear:

```sh
agent.py --project /PROJECT adopt --provider claude --alias ROLE_ALIAS --expected-session OLD_UUID --record CONTEXT.md
```

Use the currently bound UUID as `OLD_UUID`. Same verified ID is a byte-preserving
no-op; no handoff record is needed for that case. If the returned binding still
has `handoff`, name the outstanding designation in dashboard attention. Cancel
it during this routing step if this session is continuing the role; otherwise
state that it remains designated for a successor. Do not silently continue work
with an outstanding designation. A new ID requires the prepared
record to match. A successful record-based adoption consumes `handoff` but keeps
a private `recovery` receipt bound to this holder and the saved record. It is
not a release of an active role. After a lost session and another restart, use
the same `adopt --expected-session ... --record ...` command against that receipt:

- The current session verifies its own native identity and restores the exact
  recorded path and bytes. The helper checks the recorded machine fingerprint.
- For Claude recovery, a successful unfiltered native listing must include the
  current ID and exclude the predecessor. Missing, malformed or unavailable
  evidence refuses. It does not choose a replacement from that list.
- The receipt carries retired IDs so an old session cannot automatically reclaim
  the role, even after several restarts. A session matching one of those IDs
  reports that the role moved; it does not adopt back. Each successful recovery
  updates the same alias and receipt, retaining the role. There is no arbitrary
  one-restart limit requiring the user to select the teammate again.
- Codex saved-thread metadata does not establish terminal absence. New-ID
  unplanned recovery is unsupported there; same-ID continuation and prepared
  Out handoffs still work. No cross-provider parity is implied.

Show the restored pairing and ongoing role in the arrival summary. After crash
recovery, attention must say that routing was recovered from the saved account,
not that the lost session's later work was saved. Carry any missing account and
dirty-tree facts already found during ordinary pickup; do not infer lost work
solely from a restart or award memory completeness from a successful adoption.

New Out supersedes the receipt; `handoff --cancel` revokes both designation and
recovery. Explicit replacement drops recovery evidence rather than inheriting
it. A dead holder cannot cancel itself; an explicit user-selected replacement
remains the override. Earlier versions that consumed their handoff without a
receipt cannot be retroactively recovered from a guessed history.

Without a matching designation or recovery receipt, ask for the actual role replacement; only after
the person's explicit selection use `--confirm-replacement` instead of `--record`.
Unknown identity or ambiguity leaves routing unchanged, not pickup memory failed.
Show the actual refusal in dashboard attention: changed saved record, predecessor
still listed, missing/different machine, or unresolved identity—not just “routing
unchanged”. A missing fingerprint disables unplanned recovery, not a prepared
Out handoff or its designated adoption.
The narrow native listing above is allowed for recovery, not a peer health check.
No launching, resuming, stopping, work dispatch or project
file repairs is authorized by this local routing update. The bounded arrival
notice below is its only peer-contact exception. This is the narrow
private-metadata exception to status-only In, not authority to start the plan.

Replacement locks and checks the expected old ID, preserves the ongoing role,
review cadence and previous identity, and consumes the designation. A
competing update refuses; inspect that conflict rather than retrying with a
newly guessed expectation. Old request/reply records keep their original
targets. Owned launch partners cannot be replaced externally. Roles may be
changed separately through ordinary `pair --partner-role`; this operation
never inherits permissions or launch settings.

The recorded review cadence travels the same way through a prepared handoff
and restart recovery, not only explicit replacement. An invalid stored
cadence is carried unchanged rather than corrected here; readers report it.

Bindings and designations live in this Git worktree's private directory. A shared
filesystem can expose that directory to another machine; unplanned recovery
refuses a different or missing host fingerprint. A fresh
clone has no routing state; retain the project handoff and select a local partner
when needed. These checks protect ordinary mistakes, not against a same-user
process forging environment values or editing private metadata. The helper
checks identity and saved bytes, not whether a person authorized the command.
Native absence is only a current observation, not authenticated proof of death;
a predecessor could resume after the check. Its next In must honor the moved
role, and senders resolve the alias again for new jobs. Old requests keep their
original target. If several roles or intended pickups are genuinely ambiguous,
retain the bindings and ask about that choice, not a routine session-ID selection.
Another same-machine project session holding the same account could take this
role while its holder is unlisted; the helper cannot prove intended readership.
Only the session performing that role's pickup may recover it. The strict listing
also refuses malformed metadata from unrelated sessions rather than trusting an
incomplete view; this is a diagnosable refusal, not evidence the partner died.

Source: [Claude session environment](https://code.claude.com/docs/en/env-vars).
`CODEX_THREAD_ID` was observed and corroborated locally on 2026-09-13; hosts
without it remain unsupported for self-adoption, never inferred from history.
Codex corroboration supports daemon-loaded threads or stored TUI threads; a
non-TUI thread without a daemon is unsupported, not inferred to be live.

## Arrival notice and TEAM display

After restoring identity and routing, announce this arrival once to established
pairing partners. If the restored context explicitly selects peer aliases, pass
them; otherwise omit `--peer` and use the private pairing's unambiguous default:

```sh
agent.py --project /PROJECT arrival --provider claude --self-alias RESTORED_ROLE --peer PARTNER_ALIAS
```

Use the actual host provider. Omit `--self-alias` if this session has no standing
role; repeat `--peer` only for additional selected established partners. Without
`--peer`, the helper groups existing bindings by provider and exact ID, preferring
an explicitly recorded ongoing role. A unique other-provider binding can supply
the partner even without a defined role; its role remains undefined. Same-provider
contact aliases without roles are not default recipients. Multiple eligible IDs
for a provider stay unresolved and unsent, with Agent available to choose when
needed; no setup stop or guessed newest session. This uses private binding
metadata only, not native discovery or request history.

Self and its previous/retired IDs are excluded. Workers and owned launches with
no defined ongoing partner role are excluded too. An explicitly role-bearing
persistent partner is eligible, but cannot be resumed merely for a notice.
With no established partner, no notice or setup prompt. The helper corroborates self identity and refuses a
self-role binding that was not restored to this ID.

Pass the returned `team` to Switch's in-memory summary, optionally shortening role
wording faithfully for display without editing the binding. Show one compact
TEAM cell in the status grid: provider (role) + provider (role). IDs and routine notice status stay
in Agent details, not the welcome dashboard or tracked Markdown. Repeated
aliases for the same provider/ID are one member. Missing role means undefined,
not inferred from the native title. Sending cannot make availability verified.

The notice names project, sender ID, recorded role and previous ID when known.
It says no reply needed and no work requested; recipients do not acknowledge,
announce back, change bindings or treat it as user approval. Native queues may
still activate a recipient turn or hold the message under inbound policy; this
is informational content, not a promise of zero token cost or silent delivery.

Receipts reuse Git-private Agent requests. One sender/recipient identity pair
gets one attempt, including unavailable or uncertain attempts: no automatic
retry, alternate route, transcript retrieval, acknowledgement wait or dormant
partner resume. Repeating In with the same IDs reuses that result, labelled
“earlier notice … (not resent)”; the original time remains in the returned
receipt. A new ID on either side permits a new notice. Compare identities, not
commands: a Claude clear that changes its ID sends a new notice; any same-ID
continuation does not. This is identity announcement, not a heartbeat.
Pre-enqueue refusals are unavailable; only an attempted native send can be
delivery-uncertain. A failed notice remains in Agent details; surface it in
dashboard ATTENTION when it affects the next action, without turning complete
memory into incomplete pickup. Later actual work uses
ordinary Agent request/reply handling and resolves the binding again.
