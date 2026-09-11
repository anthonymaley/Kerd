# Local sessions, native queues

Use `python3 /PATH/TO/skills/agent/scripts/agent.py --project /PROJECT` as the
prefix below. Paths are resolved by the caller; never copy this helper into
consumer projects. Python 3.10+ and macOS/Linux process/filesystem semantics.

## Select or start

`sessions` lists Claude's native interactive/background sessions in this project
and threads currently loaded in Codex's shared server, plus Kerd's local partner
bindings. It does not read every transcript, launch a model, or discover every
Codex desktop/IDE/private-stdio backend. Saved partner metadata is not live state.

Subdirectories of the same Git project are included; a nested repository is
not. Codex discovery has a five-second native-connection/RPC budget and returns
partial results with an explicit note if exhausted. This is a responsiveness
control, not a job allowance or a claim that every session has been found.
An exact target lookup does not scan all loaded threads.

Bind the exact session selected from discovery:

```sh
… pair --provider claude --session EXACT_UUID --alias design-partner
```

The ellipsis denotes the command prefix above, not literal shell syntax.
Pairing writes a private local alias. It does not send work or change the
session's tools, model or authority. A conflicting alias is not overwritten.

For a new session, supply its first real contribution rather than a paid greeting:

```sh
… start --provider codex --kind partner --alias build-partner \
  --role 'Implementation partner' --prompt-file /PATH/TO/job.md
… start --provider claude --kind worker --alias independent-review \
  --role 'Independent reviewer' --prompt-file /PATH/TO/review.md
```

Use `--model` and `--effort` from the chosen available model's guidance, or omit
them deliberately to use native defaults. `--write` allows file edits within
the existing agreement; a prompt's per-file scope is not a sandbox allowlist.
Claude's launcher enables Read/Glob/Grep (and Edit/Write with `--write`), not shell
tests. Codex starts read-only or workspace-write, with no automatic permission
escalation. Do not widen an existing partner's tools to evade a denied action.

Workers reuse Conductor's existing `ask.py`, start a fresh local alias, and return
that runner's request ID. Retrieve those results with the returned runner's
`status`/`wait` commands. They are CLI workers, not native subagents of the host.
Use host-native subagents when they fit the job better.

Partners retain a native conversation. Claude uses `claude --bg`; its returned
native ID is discovered and verified (the background launcher chooses its own
ID). The native launch output supplies `claude attach`/`logs` for the person.
Codex uses `thread/start` in its native shared server. `start` may start that
native server if absent; it does not install a service or alter startup settings.
The server can unload an idle thread. Only Kerd-created partners are automatically
awakened with native `thread/resume`, preserving the exact ID and settings.
An existing user partner that goes offline is not automatically resumed.

Do not use either provider's interactive resume command on an occupied terminal.
There is no automatic stop/delete operation here. Native session management is
available when the person wants to open or retire a partner.

## Ask and receive

```sh
… ask --alias design-partner --role 'Review the changed design' \
  --prompt-file /PATH/TO/follow-up.md
… wait REQUEST_UUID --seconds 30
… status REQUEST_UUID
```

`ask` submits once and returns a request ID. Keep it in the working activity;
retrieving after a timeout uses that ID, not a second ask. An optional
`--request-id UUID` makes repeated submission of identical work idempotent;
different work with that ID is refused. An uncertain send is never auto-retried.
`--seconds` bounds retrieval only; it is not a work budget or cancellation.

Claude receives a message through its native session socket. Codex receives
`thread/queue/add`; busy recipients retain their native queue ordering. A Claude
socket write is only **submitted-unconfirmed**: native inbound policy can hold
or refuse it. It never counts as a reply. Do not override that policy globally.
New Claude partners use native `crossSessionInbound: accept` for that session's
lifetime, with permission prompts disabled and the listed tool restrictions.
This is not a Kerd-peer allowlist: other local senders can submit messages too.
Existing partners' inbound settings remain untouched. The setting permits
reception, not escalation or a grant of the person's pending approval.

The recipient returns a complete answer with request-specific text markers.
The helper reads only the selected native transcript's new suffix and archives
the complete marked assistant reply before returning it. It does not ask the
recipient to write an inbox/reply file, parse thinking, or pass earlier history
back to the controller. Missing markers or unavailable native logs leave the
reply unconfirmed; they never become a guessed success. Native log formats and
cooperative answer markers are limitations, not authenticated proof of work.
Inspect native state if a refusal or an interrupted job supplies no marked reply.

Private aliases, request prompts and returned text live under the current Git
directory's `kerd-agent/`, not in the worktree or public Git history. The existing
worker runner retains its own `cross-llm/` records. Only selected, sanitized
evidence belongs in the work record. No bindings travel between machines.

## Setup and compatibility

Both providers use their existing CLI sign-in. Do not inspect credentials.
The Claude adapter uses Python's standard library. Codex's Unix endpoint requires
a WebSocket client; do not send JSON lines directly through `app-server proxy`.
After approval, install the optional dependency in a chosen private virtual
environment, not the system interpreter:

```sh
python3 -m venv /CHOSEN/PRIVATE/ENV
/CHOSEN/PRIVATE/ENV/bin/python -m pip install -r /PATH/TO/skills/agent/scripts/requirements.txt
```

Then use that environment's Python as the prefix. No packages are auto-installed
by discovery, pairing or submission. Missing dependencies are reported.

Tested on 2026-09-11 with Claude Code 2.1.268, Codex 0.154.0 and websockets
17.0.1. Codex queue APIs are experimental; Claude's public docs describe the
session socket but not every wire field used by this adapter. Native transcripts
and background-launch output are also version-sensitive. Unsupported changes
must produce unavailable/uncertain status, never a silent CLI-resume fallback.

Sources: [Claude cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging),
[Codex app-server transport](https://learn.chatgpt.com/docs/app-server),
[WebSocket Unix client](https://websockets.readthedocs.io/en/stable/reference/sync/client.html).
Local CLI help and generated experimental schemas supplied the installed queue
methods. See the [implementation evidence](../../../docs/work/agent-connection/work.md)
in the Kerd source checkout; it is not a runtime dependency of this skill.
