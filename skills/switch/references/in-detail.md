# In: detail

Moved out of [In](in.md) so a Switch In reads a short core. Open a section only when the situation in its pointer holds; the rules are unchanged.

Contents:

- [Carry the chief of staff signal](#carry-the-chief-of-staff-signal): only when `prepare` or `pickup` output carries it
- [Restore the existing team](#restore-the-existing-team): pairing, succession, the arrival notice and stale pairings
- [Summary field details](#summary-field-details): what each field of the arrival summary means

### Carry the chief of staff signal

Only `prepare` and `pickup` carry it. With no chief-of-staff config on this
machine their output has no `chief_of_staff` key, and nothing here applies: no
role, no warning, no mention. When the output carries `chief_of_staff`, carry it
into the session as this sitting's signal; Conductor and Out read it from there and
make no extra call to find it.

- `on: true` means Conductor keeps the project's `### Queue` table and its
  `### Asks` table of open decisions this sitting and Out tidies them; `on: false`
  means neither does. `why` is for the session, not the screen.
- `relay` (present only when on) is the project's `chief_of_staff_relay` rule:
  `decisions` means an answer the chief of staff relays counts for a decision,
  never for a push, release, install or live change; `none` (also the reading when
  unset) means the person answers in this window. Carry it with the signal;
  Conductor reads it there. `relay_warning` set (not null): the value in
  `kivna/vault.json` is neither, so it reads as `none`; put one line in `warnings`
  saying so.
- `on: true` and `is_cos_repo: true` (this is the chief of staff's own project,
  and the config covers it): put `"role": "chief of staff"` in the summary JSON;
  the renderer shows it as a ROLE cell. Nothing else changes, and the arrival never resumes the chief of staff's
  checks or scans: In restores and never executes. With `on: false` (the chief of
  staff's repo skipped, opted out or not in `projects`) there is no role: the helper
  reports `is_cos_repo: false` then, and the summary leaves `role` out.
- `config_error` set (not null): the config could not be used, so the chief of
  staff is off for every project. Put one line in `warnings` naming which problem
  it is (unreadable, invalid JSON, or the bad key), never more than one.
- On, with `queue_md_present: true` beside `chief_of_staff` in the output: the
  project also keeps `docs/work/queue.md` by hand, so there are two lists. Put one line in `warnings` saying the project keeps
  two lists and should choose one; choosing, and any move, is that project's own
  decision on its own yes, never Kerd's. In only knows the file exists; it never
  reads its contents.

A hand pickup (Switch In done by hand) or an arrival from records the caller
supplied runs no helper, so it has no signal: the chief of staff is off for that
sitting, and nothing is said about it. The next helper-run Switch In restores it.

### Restore the existing team

If collaboration is already established, restore it too. Resolve the local
pairing directory with `git rev-parse --git-path kerd-agent/partners` in the
current project; if it exists, read its binding metadata, not request archives
or transcripts. Use only bindings for this project; malformed or conflicting
metadata is unresolved, not a reason to guess a peer. The directory is local to
this Git worktree, not shared with linked worktrees or transferred by Git.
With an existing binding, retain the sibling [Agent](../../agent/SKILL.md) as
the route for later contributions; load its full instructions when a contribution
is requested, not merely to display a pairing. Retain the exact
provider, alias, session ID, recorded ongoing role and any recorded review cadence
privately in context. TEAM still shows provider and role only; the cadence is for
Conductor's review planning, not the dashboard.
First compare the actual host's session variable (`CLAUDE_CODE_SESSION_ID` or
`CODEX_THREAD_ID`) with the bindings, and look for a `handoff` designation or
`recovery` receipt (including its retired IDs).
When an ID matches or either form of continuity evidence exists, read the short
[succession guide](../../agent/references/session-succession.md) and check its
verified identity. Same ID keeps the binding; an authorized successor uses its
prepared handoff, eligible restart receipt or explicit selection. A retired
session reports the moved role instead of reclaiming it. Only this private routing update is
permitted during In alongside the informational arrival notice below, never a
project repair or plan execution.
This restores routing, not a running job or a Conductor mode. The succession
helper's native identity/absence check is allowed for restart recovery. Do not
otherwise discover or resume peers merely to validate a binding.
Availability stays unverified until Agent checks the selected target for work.
Missing roles stay undefined; ambiguous bindings remain a choice when a
contribution is requested. No binding means no Agent setup question during In.
After identity and any required adoption, run Agent's bounded
[arrival notice](../../agent/references/session-succession.md#arrival-notice-and-team-display)
for the selected established partners, or the helper's unambiguous private
pairing default when the restored context names none. The caller does not
enumerate aliases as recipients; the helper reads private binding metadata and
selects only an unambiguous partner, never by title or recency. It skips stale
bindings (no reply in 14 days, or a contribution request sent since its last
reply and unconfirmed for over a day), even when they are passed explicitly, so
no notice goes to a stale partner, and returns them in a top-level `stale` list. When that list is not empty, Open work
carries one line owned by the person: “You: retire N stale pairings
(<aliases or count>), set aside, recoverable”. It is one line for all of them,
never repeated and never the recommendation. Retirement runs through Agent
(`retire --alias`) only on the person's yes; it moves each binding aside, never
deletes it. Show the team
in the arrival grid's TEAM cell: `Claude (role) + Codex (role)`. Use brief faithful role labels,
not new assignments; a missing role stays unassigned. IDs and routine notice status
remain in Agent details, not the dashboard or project records. Surface a routing
problem in ATTENTION only when it affects the recommendation. A failed notice does not make restored memory incomplete.

### Summary field details

`project` is the project already restored, by its display name: the text of
the first heading in its `README.md` when there is one (markup removed); with no
README, or a README with no heading, the first heading of a `notes.md` at its
root (any case: `Notes.md`, `NOTES.md`) when there is one; else the folder name; and
when that name is itself a placeholder word (`project`, `app`, `work`), “Your
project”. Never a file picked by alphabetical order: with no README and no
`notes.md`, another `.md` at the root (`customer-quotes.md`) is the person's
material, not the project's name. Never the literal word “project” on its own, and never inferred from the renderer's installation path. A folder
called `project`, `app` or `work` would otherwise head the arrival with a word
that reads as a placeholder. `phase` is the recommended item's rung, or the start point's
recorded `Phase:` line when the item has none, shown in the grid;
`first_arrival` is `true` only for a project with no Kerd records (above);
`where` is the position sentence; `open_work` a list of plain
lines (a single string is one item); `recommendation` carries `text` and `why`,
or `null` when nothing is actionable, which the renderer states. `question.text`
is the one arrival question; leave `proposed` null, since the recommendation is
already on screen. `documents` are `[label, path]` pairs resolved against
`base`; a path that does not exist is reported as a warning rather than offered
as a link. Supplying `open_work` or `recommendation` selects this layout; the
renderer's older grid keys (`task`, `state`, `now`, `this_session`, `source`,
`updated`) remain only for record-driven views and older callers, and new
arrivals do not use them.

`team` uses the Agent arrival result's array; the fictional IDs above illustrate
its input shape only. A caller may shorten a role's wording faithfully for
display, without modifying its private binding or assigning new responsibility.
Do not synthesize the team from project history or a legacy bridge's
collaborator names. The renderer groups identical identities and displays
providers and roles only. Use `[]` for no established pairing (the grid then shows no TEAM cell) and
`null` for unread/unresolved state. A team row's `attention` line (Kerd requests waiting
undelivered in a Codex partner's queue over ten minutes) goes into `warnings`
as it reads. When that line's “since” date is an earlier calendar day than
today, Open work also carries one line owned by the person, since only they can
reach that window: “You: look at the Codex <role> window (N Kerd requests
waiting, the oldest since <date>); say which still matter before it takes them”. Typing in
the window woke one stalled session; a closed one needs reopening. The queue
shows those requests waiting, not that the partner has stopped everything, and
some may still be wanted: the person decides, never a blanket “stale”. The line
stays on each arrival while the attention line does, and is never the
recommendation. The arrival's `stale` list never fills `team`; it becomes the
one retire line in Open work ([Restore the existing team](#restore-the-existing-team)).
A consequential routing problem belongs in `warnings`;
routine unconfirmed notice delivery is not a blocker or an availability claim.

`role` appears only in the chief of staff's own project, as
[Carry the chief of staff signal](#carry-the-chief-of-staff-signal) says; leave it
out everywhere else. `"automatic": true` appears only when a scheduled or automatic
run, not the person, started the arrival; leave it out of every arrival the person
started, where it defaults to false and the screen is unchanged.

Given a correctly shaped JSON object, fields are not required: a missing or null
one degrades to a plain “not recorded” line or an explicit “nothing open”
statement rather than an error. Malformed JSON exits 2 with a message. Where
things stand, Last session, Open work, Recommended and the grid always render,
except on a first arrival (`first_arrival: true`), where the one plain line
replaces them all; only the attention panel, documents and Insight are omitted
when empty.

It reads stdin, so nothing is written to disk. Do not re-read files to fill it,
and do not stop for approval before showing it. Only if rendering fails or the
renderer is unavailable, disclose that failure and present the restored facts
and single question as plain text.
