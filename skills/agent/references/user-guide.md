# Working with Claude and Codex

Ask for the contribution you need. Kerd handles finding the session, preparing
the request, sending it and bringing the answer back. You do not need to copy
messages between terminals or remember session IDs.

## Quick help

In Claude Code with this skill loaded, enter `/kerd:agent help`, or use
`/kerd:agent` followed by a request below. In another host, ask naturally with
the Agent skill loaded; the Claude slash command is not a universal Codex command.

| You want to… | Say… |
| --- | --- |
| See available sessions | “Show sessions” |
| Ask the established partner | “Ask Claude to review, RO” |
| Keep a pairing partner | “Pair with Codex on this” |
| Get a fresh perspective | “Start a fresh Claude reviewer” |
| Start an ongoing conversation | “Start a Codex pairing partner” |
| Follow up | “Ask Claude to recheck the fix” |
| Check progress | “Anything back from Codex?” |
| Get setup help | “Connect Codex” |

These are examples, not exact phrases you must memorize. Help does not start
work. Pairing alone remembers a session; it does not send it a job.

Once a partner is established for this project, Kerd uses it by default. You
can say “ask it to recheck” or “anything back?” when the conversation makes the
target clear. “RO” means read-only.

If no partner is established, or it is unclear which you mean, Kerd shows the
matching sessions so you can choose: provider, available name/topic, project
and availability, with a short ID only when needed to distinguish them. You
can choose an existing session or ask for a new one. An unavailable partner is
reported, never silently replaced. Explicitly asking for a fresh reviewer or
new partner skips choosing an existing session.

The command must be present in the loaded Kerd version. If your installed copy
does not include Agent, ask to check availability before changing the installation.
Loading these instructions does not install missing provider tools or dependencies.

## Which kind of session?

**Existing partner:** use when its earlier conversation matters. Kerd finds
matching local sessions and asks which one only if the choice is ambiguous.
It does not silently send a fresh reviewer instead.

**Fresh worker:** use for one bounded contribution, such as an independent
review. It starts without the partner's previous conversation; Kerd supplies
the relevant brief and sources. This route creates a CLI worker, not a native
subagent inside your current host. Native subagents can be used when appropriate.

**New partner:** use for continuing collaboration. It is a persistent native
conversation you can address again by a local name, with its previous context.
A partner is not automatically a visible terminal window. Kerd can provide
the supported native route for opening it; it will not take over an occupied one.

## A typical exchange

You: “Ask Codex to review this change against the agreed design. No edits.”

Kerd identifies the session and shows the job before sending:

```text
Codex · build-partner · Review the change · read-only
You: nothing needed.
```

Then it reports meaningful changes: submitted or queued, an observed start
when available, and the returned findings. A queued job is not yet running;
a returned review is not proof that the work passes. Kerd assesses the answer
and continues only work already authorized. A review request by itself does
not authorize fixes, commits or publication.

If you name a model, Kerd keeps that choice or explains why it is unavailable.
Otherwise it chooses for the job and available tools using the model guidance,
then prepares the prompt from the agreed goal, sources, checks and boundaries.
An existing partner keeps its model and permissions. Requested effort and
observed model identity are reported separately when relevant.

## First use: what you need to do

Ask for the real contribution first. Kerd checks only the route it needs and
handles project paths, session selection, aliases and result retrieval.

- Already set up: it proceeds within your permission to do the job.
- Missing software or a dependency: it explains what and where, and asks before
  installing unless you already authorized that setup. Codex's connection uses
  an optional WebSocket dependency in a private Python environment.
- Sign-in needed: you sign in through the provider's own flow. Never paste
  credentials into the conversation. Existing account usage charges apply.
- New Claude partner: Kerd discloses that its native inbound setting accepts
  other local senders too, not only Kerd. That setting lasts for the session;
  it does not enlarge the session's tool permissions.

### If Claude asks you to approve the message

Pairing remembers a session; it does not make Claude trust incoming requests.
A session that bypasses tool prompts may hold Kerd's message when the sender's
permission class is unknown. Choose **Deliver this message to Claude** to
approve only that request. Kerd then retrieves the same request's answer; you
should not have to copy the review back.

For unattended reception in a new partner session, a session-only setting is:

```sh
claude --settings '{"crossSessionInbound":"accept"}'
```

That command starts a new session, not a replacement for an occupied partner.
Alternatively, Claude's configuration menu has **Messages from your other
sessions → Accept**, but that writes a **user-wide** setting. Either choice
accepts other local senders too, not just the paired Kerd session. Kerd explains
the scope and leaves the choice to you; it never changes global settings merely
because a request was held. See [Claude's inbound controls](https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages).

While it is working, Kerd checks for the reply and reports changes. If its turn
ends waiting for your approval, it checks the pending request when you return.
There is no Kerd background watcher that wakes a finished controller turn.

### Stopping repeated inbound prompts

If your own session keeps asking whether to accept messages from other sessions,
you have two controls, and they differ in scope.

Open `/config` and set **Messages from your other sessions** to **Accept**. This
is a user-wide setting: it accepts incoming peer messages for all your sessions,
not only this Kerd partner. Choose it deliberately.

The narrower option is to launch just the partner session with the setting:

```sh
claude --settings '{"crossSessionInbound":"accept"}'
```

That affects only the session you launch. Both are Claude's own documented
controls, described under [inbound
messaging](https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages).
Kerd never changes the user-wide setting for you; a partner it creates carries
the narrow per-session form, and your existing sessions keep whatever you chose.

New partners default to read-only. File-edit access needs the agreed scope;
the prompt's named files are not an enforced per-file sandbox. The current
Claude launcher enables file tools, not shell tests or nested delegation.
If the job needs those capabilities, Kerd must select an authorized route that
has them, not label an unrun test as passed.

## When something is unavailable

- **Session missing:** discovery covers Claude native listings and Codex's
  shared server, not every desktop/IDE session or saved conversation. Kerd
  explains the limitation; it does not kill a terminal or resume “latest.”
- **No reply yet:** ask for status. Kerd retrieves the original request, not a
  duplicate. A wait timeout neither cancels the job nor proves delivery failed.
- **Permission or inbound refusal:** Kerd reports it. Another model cannot
  supply your approval or bypass the recipient's settings.
- **New machine:** pair again. Local names, native IDs and raw exchanges stay
  private in Git metadata; they do not travel with normal project commits.

## Commands for people who want the terminal details

The skill is the conversational interface. Its Python helper provides
`sessions`, `pair`, `start`, `ask`, `status` and `wait`; each accepts `--help`.
From the Kerd checkout:

```sh
python3 skills/agent/scripts/agent.py --help
python3 skills/agent/scripts/agent.py start --help
```

Use [native sessions and setup](native-sessions.md) for executable command
patterns, dependencies and tested versions. In particular, fresh workers return
Conductor's runner and request ID: use that runner for their status and wait.
The Agent helper's own status and wait retrieve partner requests.
