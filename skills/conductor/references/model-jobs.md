# Ask another model to contribute

Read when preparing a delegated job. For a direct “ask Claude/Codex”, use
`/kerd:agent` (sibling `../../agent/SKILL.md`) to resolve the established partner
or show session choices before dispatch. If Agent is absent from the
installation, disclose the missing partner route; do not silently substitute
a fresh worker. Agent also reads this guide for prompt preparation: when it has
already selected the route, do not route back or repeat selection. The `ask.py`
instructions below apply to deliberately chosen CLI workers, not existing native
partners. A direct review request authorizes that review, not a new interview
or implementation. The current agreement supplies standing authority for jobs
inside a delivery loop. Neither route creates permission for extra effects.

## Prepare work the chosen model can do well

Read [model choice](guidance/model-choice.md) when assigning a new kind
of job or changing the pair. It supplies the cross-provider shortlist, evidence
limits and decision method. Reuse an applicable choice; do not run a new survey
or ask the user to staff every job. Then load only the chosen model's guidance.

Choose the model for the contribution and available tools. Check installed CLI
help and known account availability when the route is unfamiliar; don't probe
with paid jobs merely to list models. Prefer a different suitable model for
independent assessment. Do not silently replace a specifically requested model.

Read the applicable local provider/model guidance linked from execution.md.
Use only clauses relevant to this job and actual model. Record the selected
profile/version, or the absence of a matching profile. A CLI default is not an
observed model identity. Do not claim that a prompt is optimized merely because
its headings look vendor-specific. Effort is a native setting, not a sentence
asking the worker to think harder. Label it requested unless the route supplies
evidence of the applied setting. Record observed model identity separately;
neither identity nor a successful request proves that effort was applied.

Write the actual prompt beside the work using ordinary Markdown or useful XML
boundaries. This is Conductor's judgment, not a required JSON form. A useful
job contains the outcome, selected source material, specific contribution,
agreed success/proof, allowed changes and stopping condition. A review receives
the original agreement and artifacts, not only the builder's summary. Keep
irrelevant interview history and the whole skill pack out of worker prompts.

For Claude, use descriptive tags when mixing instructions and source material;
use the selected profile's relevant effort/autonomy advice. For OpenAI reasoning
models, an applicable profile may favor outcome-first prose with native tools
and freedom over method. With no matching profile, use the same clear outcome
contract and disclose the fallback. Neither presentation changes the agreement.
An example is a writing aid, never an extra requirement or invented project fact.

Before sending, compare the prepared prompt with the agreed contribution: did
it retain the required outcome, evidence and boundaries? Correct omissions.
This is a semantic check, not a fingerprint, parser gate or separate user stop.

## First use: handle setup, not a session-ID exercise

When another model is needed, check only the chosen route: CLI availability,
supported flags and sign-in status. Do not make every new project configure both
providers. Use status commands without displaying account identifiers or reading
credential files; a successful sign-in check is not a successful model job.

If a tool is missing, explain what would be installed, where and why, and offer
to do the setup using current official instructions. Installation needs explicit
or already-applicable authority; a review request alone does not grant it.
The person completes provider sign-in themselves in its native flow. Never ask
for credentials in chat or save authentication material in the repository.
For Codex, `codex login status` checks sign-in and `codex login` opens its sign-in
flow ([official authentication guidance](https://developers.openai.com/codex/auth)).
For Claude, consult installed `claude auth --help` for the supported status/login
commands. Respect managed account restrictions; do not change billing or accounts.

Once ready, Conductor handles the project path, prompt, alias, request, waiting
and returned evidence. Use the first real authorized contribution to verify the
route, not an extra paid greeting. Say what is ready, what needs the person's
action and what remains untested. Keep any relevant setup limitation in the
existing work record; no setup manifest, background inbox or new service.

This bridge creates a worker session and records its exact native ID automatically.
It can resume its registered repo-local aliases. It does not attach to any open
Codex or Claude terminal. If the person names a particular existing session that
is not connected, explain that and provide its handoff prompt or ask whether a
new worker is acceptable; never silently substitute one. Private session bindings
are local, not transferred with the project's ordinary Git files.

## Native route first

When the host actually exposes a native subagent for the chosen model and the
job is bounded to this session, dispatch it there: the same prepared brief, the model chosen from
[model choice](guidance/model-choice.md), and the effort **requested**
in the native setting when exposed, otherwise in the brief. Keep requested and
observed effort distinct. A subagent's return is its result; nothing is
retrieved from a transcript. Prefer a different suitable model for independent
assessment, as for any route. Use the bundled runner below only when the job
needs what this host's subagents lack: another provider, resumability by native ID, a CLI sandbox,
or a life beyond this session.

Claude Code's native subagents are not a way for a Codex host to run Claude.
Use Agent for a named/existing Claude partner from Codex; a deliberately fresh
cross-provider worker uses the bounded CLI route. Do not substitute an OpenAI
subagent and label it a Claude review (or vice versa).

## Send it without adding project infrastructure

Use [the live work view](journey.md#keep-the-tasks-visible-while-the-work-unfolds)
for this handoff. Before sending, name the chosen model, its contribution and
whether it may edit. After launch is confirmed, update the task to running.
On return, show the useful findings and what happens next; do not leave a
successful cross-model contribution hidden in a final evidence document.

The bundled `../scripts/ask.py` is resolved relative to this reference file.
Invoke it with Python 3 and the **current project's absolute root**; never use
the skill's repository as the project by accident. It uses Git, authenticated
Codex/Claude CLIs and POSIX process controls (macOS/Linux); this adapter is not
Windows-tested. Kerd's native job route may work where this adapter does not.
No CI, service, inbox, hook, SDK, API key setup or project script copy is required.
Existing CLI authentication, host permissions and usage charges still apply.

Illustrative command—replace the marked paths and choose model/effort from
available evidence; do not dispatch this example literally:

```sh
python3 /path/to/conductor/scripts/ask.py --project /path/to/project run \
  --target claude --session work-review --role "Independent outcome reviewer" \
  --request-id work-review-1 --prompt-file /path/to/work/review-prompt.md \
  --model VERIFIED_MODEL --effort SUPPORTED_EFFORT --background
```

Omit `--background` for foreground work. Omit model/effort only when deliberately
using native defaults; record that choice and any unknown resolved value.
Omit `--write` for review. Add it only for an authorized editing job, with the
file boundary stated in its prompt. Claude workers have file tools, not Bash
or further delegation; a job needing shell tests needs another suitable route
or Conductor to run the tests. Codex's workspace-write option is not a per-file
allowlist. The prompt's narrower file boundary is an instruction, not a sandbox.
Do not expand a worker's tools or nest another controller just to evade that.
Read-only Codex jobs may use inspection commands to read relevant files; they
must not run tests/builds that write, install or perform network operations.
Do not paste a whole repository into a prompt to compensate for a needless ban
on reading it. Include only useful selected material and resolvable source paths.

The alias is repo-local and captures/resumes the exact native session for you.
Use a fresh alias for an independent review when an earlier conversation could
bias it. Reuse the alias for relevant follow-ups, but supply the current job and
changed facts each time. Never resume “latest.” Different sessions can run in
parallel; this runner does not prevent their file edits colliding. Give parallel
editors disjoint ownership or serialize edits.

## Receive, use and keep moving

For background work, save the request ID and current activity in the existing
work record, do other useful work, and retrieve the result. This is a local
request ID, not a private native session ID. Wait in short intervals when that
is necessary to keep the user informed:

```sh
python3 /path/to/conductor/scripts/ask.py --project /path/to/project wait work-review-1 --timeout 30
```

That timeout stops waiting, **not the job**. Work limits are optional; the run's
separate `--timeout` cancels work at that supplied limit. No number is required.
Inspect returned `status`: `starting`/`running` means active, not successful.
`completed` means a reply arrived, not that the outcome passed assessment.
Read the reply, inspect actual artifacts and check required evidence. Save a
short model/effort/profile/result/contribution note and necessary review evidence
beside the work. Private logs/session IDs remain in Git metadata. Do not copy
raw results containing private identifiers or secrets into shared documents.

Use supported findings: correct within authority, run relevant checks and obtain
needed reassessment. Continue the next authorized job without another “okay.”
Close a finished alias with `close ALIAS` when useful; results remain retrievable.
This retires the bridge alias, not somebody's open terminal or native history.

On a failed request, inspect `status REQUEST` before retrying. Reusing an identical
request ID returns its existing result; a correction is a new request, not a
hidden rerun. Do not relabel a failed assessment by changing its measure name.
Use `cancel REQUEST` to request cancellation; inspect the final state before
claiming it stopped. `interrupted`/`unknown` means native work may still exist.
Reuse stays blocked; do not delete its metadata or kill an unverified stored PID.
`resolve REQUEST` retires uncertainty only after the recorded process group is
gone. Missing identity, permissions or detached work can still need inspection.
Report that limit honestly; never turn an uncertain launch into a claimed result.
