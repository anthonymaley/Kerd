---
name: agent
description: Connect Claude and Codex for a contribution, define ongoing partner roles and review cadence, carry designated roles across verified session-ID changes and recover eligible Claude roles after restart, announce arrivals to established partners, discover or pair local sessions, or start a bounded worker or persistent partner. Use for “ask Codex”, “ask Claude”, “which session is you”, “use the session with the context”, “pair these sessions”, or “start a reviewer”. Keeps the chosen session and native queue; never substitutes a fresh reviewer for a named partner.
---

# Agent

**Asking the person:** every question is one speech-bubble line, the last prose line of the message, `> 💬 **The question?**`, with any options, context or proposed answer listed above it, never inside it; where the host offers one, a native picker may follow the bubble carrying those same options and always leaving a free-form answer open, never replacing or preceding it — see [the question form](../conductor/references/journey.md#question-surface-and-host-adaptation).

Get a contribution from the right session, then use its answer. This command
supports Conductor or a direct user request; it does not start another intake.

For Switch In's informational arrival (no contribution or reply), use only the
[arrival notice](references/session-succession.md#arrival-notice-and-team-display)
path. It shows the restored team and deduplicates identity announcements without
turning them into review jobs or waiting for a response.

## Help

For `/kerd:agent help`, “how do I connect the models?” or a setup question, read
the [user guide](references/user-guide.md). Show its short help list first;
expand only the relevant section. Help alone does not discover sessions, pair,
install anything or launch a job. Natural-language examples are skill requests,
not shell subcommands. For execution, use the workflow below.

## Get a contribution

1. Establish the current project and requested contribution. Reuse the agreement
   and relevant context. A review request is not authority to edit or publish.
2. Use the established partner for this project and requested provider when no
   other session is specified. Resolve short follow-ups from the current exchange;
   do not ask the person to select the same partner again. If none is established
   or the target is ambiguous, discover with
   `scripts/agent.py --project ABSOLUTE_PROJECT sessions` and show the matching
   sessions before asking which to use. Lead with provider, established-partner
   status, alias and short ID; group aliases for the same provider/ID into one
   row. Discovery's `partner_aliases` supplies that exact match. Show native
   `name` second as **Saved title (may be old)**, never the current task.
   Keep project and observed availability visible; lengthen colliding short IDs.
   Mark **This session** only when a host-supplied current ID matches exactly,
   never from its title, working directory or position in the list. A peer may
   identify its own ID, but that is reported identity until locally checked.
   Label unavailable bindings separately; do not make them appear selectable
   merely because their alias survives. Use metadata, not invented summaries.
   Offer starting a new session as a separate choice, not a silent fallback.
   An explicit fresh/new request goes directly to that route. If an established
   partner is unavailable, explain before offering alternatives; never substitute.
   An empty list does not prove no saved conversation or other-app session exists.
   A recent exchange already in context may supply **Last exchange (recorded):
   contribution, result, date**. Keep that separate from present activity; don't
   read transcripts or scan all requests merely to decorate discovery. A project
   handoff is project context, not proof a listed session has loaded it. See the
   [user guide](references/user-guide.md#recognize-your-partner) for the display.
3. Choose deliberately: **existing partner**, **new persistent partner**, or
   **fresh bounded worker**. Do not silently replace one with another. A fresh
   independent review and a contextual pairing conversation serve different jobs.
   Define the partner's ongoing role during Agent setup, using the person's
   stated responsibility (for example implementation partner or reviewer).
   Reuse a recorded role; ask briefly if a needed role is unclear, not on every
   request. `pair` and `start --kind partner` accept `--partner-role`; pairing
   again with the exact alias/provider/ID and an explicit role updates that role.
   Show it from the private `partners` binding alongside provider, alias and ID.
   Missing means not defined, never guessed from the title or model. The existing
   `--role` on a job is that contribution, not an automatic standing-role change.
   A role is neither a permission grant nor appointment as the current Out owner.
   When pairing or starting a persistent partner, ask once for whatever is not
   yet recorded, never re-asking a recorded role or a recorded cadence. If
   neither is recorded, ask for both together, in one message: the options
   listed above, one speech-bubble question, `> 💬 **…?**`, as the last prose
   line, then the picker or pickers. For a missing role, follow the bubble,
   where the host offers one, with a native single-choice picker naming the
   four shortcuts — **Pairing partner**, **Implementation partner**,
   **Independent reviewer**, **Specialist adviser** — and leave anything else
   to the host's own free-form route; do not add an “Other” entry where the
   host supplies that route itself. Those four are shortcuts, never the
   permitted set: any responsibility the person names is a valid answer, and
   the role recorded is whatever they actually say, in their wording —
   `--partner-role` takes any wording, where `--review-cadence` enforces its
   four values. Where a host's picker offers no free-form route, the role
   question is answered in words instead. For a missing cadence, list the four values — `checkpoints`,
   `before-push`, `end`, `on-request` — with one-line meanings above the
   bubble, and follow the bubble with a native multi-select picker over those
   same four, since the person may name several values, though `on-request`
   stands alone. If a role is recorded and only the cadence is missing, ask
   for the cadence alone, the same way. Where the host offers no picker, the
   bubble is answered in words exactly as before; a picker accelerates the
   answer, never gates it, and never narrows it. Record the answers with
   `--partner-role` and `--review-cadence`; do not re-ask on later requests,
   and the person changes either by saying so. A cadence schedules this
   partner's review only inside authorized work and grants no work, contact
   beyond it, commit, push or release. Conductor reads bindings through
   `agent.py partners`.
   For a designated replacement after a clear, restart or handoff, follow
   [session succession](references/session-succession.md). Verify this host's
   actual identity; do not overwrite a binding just because its peer is absent.
4. Prepare the contribution using Conductor's
   [model-job guidance](../conductor/references/model-jobs.md): relevant source
   paths, outcome, contribution, checks, authority and stopping point. Consult
   only the applicable model profile. Requested model/effort and observed model
   are different facts. Resolve guidance at Conductor's
   [references/guidance/](../conductor/references/guidance/README.md), which
   ships with the plugin. Do not re-survey model choices every turn.
5. Read [native sessions](references/native-sessions.md) for the selected route
   and its commands. Handle setup within existing authority; ask before installing
   dependencies or changing account/settings scope. Never request secrets in chat.
6. Before dispatch, show the partner/model, job and edit boundary in the live
   task list when available. After dispatch, distinguish queued, unconfirmed,
   running and returned. Do other useful work while waiting; emit useful state
   changes. A wait timeout stops waiting, not the recipient, and never resends.
   Own retrieval through to a complete reply or an explicit blocker; dispatch is
   not completion. Use short waits during active work. If inbound approval blocks
   delivery, show that the review is waiting on the person. On their next reply,
   check the retained request before sending anything new or asking for pasted
   findings. There is no notification service waking an ended controller turn;
   disclose that limit when it matters rather than claiming unattended follow-up.
7. Read and assess the returned answer. Record the useful findings and disposition
   beside the work; keep private native IDs, prompts and raw transport records
   local. A returned review is not a passed outcome. Continue authorized work.
   When contributing to another session's Switch Out, return the missing account
   to its established owner; do not also rewrite shared handoff files. Follow
   [coordinated closeout](../switch/references/in-out.md#one-coordinated-closeout).

The same local command can be called by either provider when that session has
permission to run it. No human copy/paste relay, Kerd inbox, watcher or service.
Native Claude sessions, the native Codex server, and the Codex TUI a person
already has open own execution. A TUI is reached by `codex queue` and read back
from its own transcript; it is listed as a saved thread with activity unknown.

Existing sessions keep their permission settings. A peer cannot approve a
pending action or route around a refusal. New partners default to read-only;
file edits require the agreed scope and `--write`. The launcher currently gives
Claude file tools, not Bash or nested delegation. Choose another authorized
route when the contribution requires those tools; do not claim all native
session capabilities were enabled.

When pairing, explain that the local alias does not grant native inbound trust.
If Claude holds a message, the person may approve that message or explicitly
choose broader reception; see the guide's setup choices. Never attest a guessed
sender permission mode or borrow the recipient's token to bypass the hold.

New Claude partners also start with native `crossSessionInbound: accept` for
that session's lifetime. This is not an allowlist of Kerd peers: other local
senders can submit messages under the recipient's tool permissions. Disclose
that setup when creating a partner; existing sessions' inbound settings stay as-is.

Never kill an occupied terminal, resume “latest”, fork without saying so,
change global settings, or revive an unowned offline session to make delivery
look successful. Kerd-created Codex partners may be dormant between requests;
their exact native conversation is awakened on the next request. A person's own
Codex TUI is never resumed, forked or stopped: it is queued to exactly as it
stands, and whether it is attended is unknown until it answers. This is not
attachment to an arbitrary app's session. Keep these distinctions visible.
