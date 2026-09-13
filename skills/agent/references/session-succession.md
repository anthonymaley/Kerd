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
If this session resumes work instead of handing over, revoke the designation
with `handoff --provider claude --alias ROLE_ALIAS --cancel` before that work.

## In: keep or adopt, then stop at the dashboard

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
record to match. Without it, ask for the actual role replacement; only after
the person's explicit selection use `--confirm-replacement` instead of `--record`.
Unknown identity or ambiguity leaves routing unchanged, not pickup memory failed.
No probing other peers, launching, resuming, stopping, dispatching or project
file repairs is authorized by this local routing update. This is the narrow
private-metadata exception to status-only In, not authority to start the plan.

Replacement locks and checks the expected old ID, preserves the ongoing role
and previous identity, and consumes the designation. A competing update refuses;
inspect that conflict rather than retrying with a newly guessed expectation.
Old request/reply records keep their original targets. Owned launch partners
cannot be replaced externally. Roles may be changed separately through ordinary
`pair --partner-role`; this operation never inherits permissions or launch settings.

Bindings and designations are local to this Git worktree and machine. A fresh
clone has no routing state; retain the project handoff and select a local partner
when needed. These checks protect ordinary mistakes, not against a same-user
process forging environment values or editing private metadata. The helper
checks identity and saved bytes, not whether a person authorized the command.

Source: [Claude session environment](https://code.claude.com/docs/en/env-vars).
`CODEX_THREAD_ID` was observed and corroborated locally on 2026-09-13; hosts
without it remain unsupported for self-adoption, never inferred from history.
Codex corroboration supports daemon-loaded threads or stored TUI threads; a
non-TUI thread without a daemon is unsupported, not inferred to be live.
