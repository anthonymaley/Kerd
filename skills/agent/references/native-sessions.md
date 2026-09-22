# Local sessions, native queues

Use `python3 /PATH/TO/skills/agent/scripts/agent.py --project /PROJECT` as the
prefix below. Paths are resolved by the caller; never copy this helper into
consumer projects. Python 3.10+ and macOS/Linux process/filesystem semantics.

## Select or start

`sessions` lists Claude's native interactive/background sessions in this project,
threads currently loaded in Codex's shared server, and — from Codex's local store
— the Codex sessions a person opened in this project (the TUIs in your terminals),
plus Kerd's local partner bindings. Store rows are labelled `native-thread` with
status `saved thread — activity unknown`: the store has no PID or heartbeat, so a
row proves a selectable conversation, never that anyone is at the keyboard.
Archived threads and spawned subagents are excluded. The store scan needs no
daemon and no optional dependency. It does not read every transcript, launch a
model, or discover every Codex desktop/IDE/private-stdio backend.

Each discovered row carries `partner_aliases`, derived from exact provider/ID
matches in existing bindings. It adds no saved state or history reads. `name`
remains the native saved title, not a current-work summary. Unlisted bindings
remain in `partners` with their unavailable status; no discovery row is invented.

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
Add `--partner-role 'Implementation partner'` to `pair` or `start --kind partner`
to retain an ongoing responsibility in that existing private binding. Repeating
`pair` for the same alias/provider/ID with the flag updates only that role;
omitting it preserves a recorded role. Pair still checks the exact native target,
so an unavailable target cannot be re-paired just to change its role. The per-job
`--role` remains separate. `sessions` returns the role in `partners`; it does not
infer roles for unpaired sessions. No tracked roster or permissions change.

Add a repeatable `--review-cadence VALUE` to `pair` or `start --kind partner`
for how that partner reviews: `checkpoints`, `before-push` and `end` may be
combined freely; `on-request` is refused in combination with any of them and
must be given alone. Repeating `pair` for the same alias/provider/ID with the
flag replaces the stored list; omitting it preserves a recorded cadence, the
same way an omitted role is preserved. `start` refuses the flag for
`--kind worker`.

`partners` (no arguments) reads this project's private bindings only — no
native discovery, socket or contact — and returns `{"partners": [...]}`
ordered by alias. Each row has `alias`, `provider`, `kind` (`partner` when
absent), `role` (or null), `review_cadence` (list or null) and `valid`. A row
can be invalid for more reasons than these: its JSON is unreadable, provider
or alias is missing, the provider is not `claude` or `codex`, the alias does
not match its file, the project does not match, the binding has no confirmed
session yet (for example an unconfirmed `start`), the role is not a string, or
the stored cadence is malformed. An invalid row is kept, with `valid: false`,
an `error` string and `review_cadence: null`; Conductor never selects an
invalid row. A mix of valid and invalid rows exits 0, so one corrupt binding
never hides usable partners; a non-zero exit is reserved for a store-level
failure such as an unreadable partners directory or a project that is not a
Git repository. It shows no session IDs beyond what `sessions` already
returns.

For a session taking over an established role after Out/In, use
[session succession](session-succession.md): `identity`, `handoff`, and `adopt`
reuse the private binding, with explicit expected-old-ID replacement. Ordinary
`pair` still refuses a conflicting identity and discovery never replaces it.
After record-based adoption, the same binding holds a restart receipt for the
saved account. The succession guide defines Claude's same-machine absence check,
retired-ID refusal and Codex's new-ID recovery limit; ordinary discovery never
chooses or installs a successor.

For a new session, supply its first real contribution rather than a paid greeting:

```sh
… start --provider codex --kind partner --alias build-partner \
  --role 'Implementation partner' --prompt-file /PATH/TO/job.md
… start --provider claude --kind worker --alias independent-review \
  --role 'Independent reviewer' --prompt-file /PATH/TO/review.md
```

Use `--model` and `--effort` from the chosen available model's guidance, or omit
them deliberately to use native defaults. These launch flags set a new persistent
partner's own session. They are separate from Conductor's `kerd:effort-<level>`
agents, which set effort for native subagent jobs inside a session. `--write` allows file edits within
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

Switch In's no-reply identity announcement uses `arrival --provider ...
--self-alias ... --peer ...`, not `ask`. See
[arrival notices](session-succession.md#arrival-notice-and-team-display) for
recipient selection, deduplication and TEAM display. Its `arrival-notice`
receipt has `reply_expected: false`; `status` and `wait` return it immediately
without reading transcripts. This is not an unanswered contribution job.

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

Claude receives a message through its native session socket. A daemon-loaded
Codex thread receives `thread/queue/add`. A saved Codex thread with no daemon —
a TUI — receives `codex queue --cd <root> --thread <uuid> --message …`; `--cd`
names the working root (both `codex` and `queue` accept it), it is not a
project check, so the stored project is re-validated immediately before
sending. A daemon never loads a TUI, so it reports every TUI as not loaded;
that is why a session a person opened (`source = 'cli'`) always takes the
`codex queue` route, daemon or not. The "not loaded" refusal applies only to
app-server-created threads Kerd does not own: their owner's session is
offline, and `codex queue` must never be used to find out whether it can wake
one. The
message text travels in the process's arguments, which other local accounts
on the machine can read; do not put secrets in a request. The route is decided
before anything is sent, and one request is enqueued by one route: an uncertain
send is retained as `delivery-uncertain` and never followed by a second send
elsewhere. Busy recipients retain their native queue ordering. Both a Claude
socket write and a `codex queue` exit 0 are only **submitted-unconfirmed**:
enqueued, not consumed, not answered. Native inbound policy can hold or refuse
a Claude message. Neither ever counts as a reply. Do not override that policy globally.
New Claude partners use native `crossSessionInbound: accept` for that session's
lifetime, with permission prompts disabled and the listed tool restrictions.
This is not a Kerd-peer allowlist: other local senders can submit messages too.
Existing partners' inbound settings remain untouched. The setting permits
reception, not escalation or a grant of the person's pending approval.

The recipient returns a complete answer with request-specific text markers.
The helper reads only the selected native transcript's new suffix, accumulating
final-answer text across events (a reply split across a commentary/final boundary
yields no reply, never a false one), and archives the complete marked reply
before returning it. Codex streams `commentary` before its `final_answer`; a marker
quoted in commentary — in a fenced example, say — is not a reply and is ignored.
Only `final_answer` text counts, and events with no phase at all (older
rollouts) are read by explicit policy. The markers must delimit lines: the
opening marker starts a line and the closing marker ends one, as the request
instructs. A reply written inline — `<marker>answer</marker> Let me know…` —
is not recognised and leaves the request submitted-unconfirmed, by design:
that shape is indistinguishable from a sentence mentioning the markers. Codex may archive a thread, which moves
its rollout file; a moved or truncated log is reported as observation
unavailable, never re-read from the start and never re-sent. It does not ask the
recipient to write an inbox/reply file, parse thinking, or pass earlier history
back to the controller. Missing markers or unavailable native logs leave the
reply unconfirmed; they never become a guessed success. Native log formats and
cooperative answer markers are limitations, not authenticated proof of work.
Inspect native state if a refusal or an interrupted job supplies no marked reply.

Limits stated rather than glossed. On the Claude socket route, a message larger
than the native sender's documented same-machine cap (1,000,000 serialized
characters) is refused before a request JSON or socket attempt; a local lock
file may remain. Point the recipient at a file instead. This cap does not
describe the Codex CLI or a new partner's CLI launch. Every
Kerd controller sends as `from: kerd-agent`, so a per-sender throttle on the
recipient's side is shared across them, and a held, expired or throttled
message is indistinguishable from a slow reply: all remain submitted-unconfirmed.
The Claude socket target is checked for owner and type only; the native client
additionally verifies the peer process, and Kerd does not, so a same-user write
to session metadata could redirect a send. A native log rewritten in place with
its inode preserved would pass the replacement guard; neither provider is known
to do this. A new partner's first contribution, like a `codex queue` message,
travels in process arguments visible to other local accounts.

Private aliases, request prompts and returned text live under the current Git
directory's `kerd-agent/`, not in the worktree or public Git history. The existing
worker runner retains its own `cross-llm/` records. Only selected, sanitized
evidence belongs in the work record. No bindings travel between machines.

## Images

A partner is shown an image by path, not by attachment. The request text names the
file's absolute path and asks the partner to open it; the partner looks with its own
viewer, and answers as the partner that already knows the project.

Observed on 2026-09-21 with codex-cli 0.154.0, on a throwaway Codex terminal session
reached through the same `codex queue` route as `ask`:

- `codex queue … -i FILE` exits with `codex queue does not support image attachments`.
  The `-i, --image` in its help is inherited from the top-level command.
- A text request naming an absolute path was answered correctly: the session ran its
  image viewer and read back content it could only know by seeing it.
- The same held for a file outside the session's working directory, the usual case for
  a person's screenshots.

A Claude session was tested the same way on 2026-09-22: a fresh read-only worker on
Sonnet 5, given one absolute path to a PNG in this project, opened it and answered three
questions whose answers are only in the picture — a box's two lines, a caption under a
rule, and the number of boxes in a row — all correct. So the path route holds for both
providers. Not yet tested on Claude: an established partner rather than a fresh worker,
and a file outside the project.

Limits: one Codex model and one Claude model, three synthetic images, the default
sandbox. A sandbox that forbids reading outside the workspace would block the path; say
so rather than substituting.
`codex exec -i` starts a fresh worker with no project context: it can take the
attachment, but it is not the partner, and the person chooses it.

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
methods. Development evidence is at `docs/work/agent-connection/work.md` in the
Kerd source checkout; it is not shipped or needed at runtime.
