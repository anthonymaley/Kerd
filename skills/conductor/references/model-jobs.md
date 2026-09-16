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

Choose the model for the contribution and available tools. Assess suitable
available pairs before retaining or inheriting the controller's settings; the
current pair is one candidate, not the default. State the brief task-based reason
when retaining or inheriting it. Check installed CLI
help and known account availability when the route is unfamiliar; don't probe
with paid jobs merely to list models. Prefer a different suitable model for
independent assessment. Do not silently replace a specifically requested model.
When a job is dispatched with a different model, effort or route than its plan
recorded, state why in a Fit line
([startup contract](orchestration.md#one-visible-startup-view)) before sending.

Read the applicable local provider/model guidance linked from execution.md.
Use only clauses relevant to this job and actual model. Record the selected
profile/version, or the absence of a matching profile. A CLI default is not an
observed model identity. Do not claim that a prompt is optimized merely because
its headings look vendor-specific. Effort is a native setting, not a sentence
asking the worker to think harder: never write a level into the prompt as if it
applied. Set it through the route's own control:

| Route | How effort is set | What to show |
| --- | --- | --- |
| Claude native subagent, Kerd's effort agents installed | `subagent_type: kerd:effort-<low\|medium\|high\|xhigh\|max>` plus the per-call `model` | requested via definition; observed with `job_evidence.py` |
| Claude native subagent, no effort agents | the ordinary native route; the call still names `model` | effort unset and unverified; requested model still shown |
| Fresh Codex worker or native Codex subagent | that route's supported model and effort controls | requested; observed where the route reports it |
| Established Codex partner or TUI | not retunable by a queued contribution; the session keeps its own pair | configured, observed or unknown |
| Managed Conductor | its existing explicit pair | as that route records it |

The `kerd:effort-*` agents set only effort; the call still passes `model`. Their
descriptions ask Claude to use them only when Kerd selects one. That is routing
guidance, not a host prohibition.

**The dispatch contract: every `Agent` call names both keys, concretely.** This
covers every native Claude job this session sends — composer, player or reviewer.
`model` requests the model and `subagent_type` sets the effort:

```
Agent(
  subagent_type: "kerd:effort-high",
  model: "sonnet",
  ...
)
```

There is no unplanned dispatch. If you are calling `Agent`, the call is the plan,
whatever the job is called and whether or not a row was drawn for it. “Per
definition”, “inherited”, “the controller's” and “default” are not softer choices;
they are the defect described in words. The `model` value is a concrete alias —
`haiku`, `sonnet`, `opus` or `fable`; the field itself also accepts a full model ID,
but a host may expose only the aliases, so name an alias unless a full ID is known
to pass on this host.

The two keys are required differently, because one of them can be genuinely
unavailable:

- **`model` is required in every case.** No route and no session state excuses
  omitting it. One host state removes the *route* instead of the requirement: while
  `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` is `1` a caller cannot pass a model at all, so
  a native Claude dispatch is not a compliant Kerd route in that state — see below.
- **`subagent_type` names a `kerd:effort-<level>` whenever those definitions are
  loaded.** When they are not — a session opened before they were installed cannot
  load them — the call still names a concrete ordinary `subagent_type`, effort is
  shown as *unset and unverified*, and the disclosure says why. That is the
  documented fallback, not a waiver: the `model` half is untouched by it.

Omission is not a neutral default, and it does not resolve to the caller's model by
some simple rule. [The documented resolution order](https://code.claude.com/docs/en/sub-agents#choose-a-model)
is: the per-invocation `model`; then the definition's `model` frontmatter, where
`inherit` selects the main conversation's model; then `CLAUDE_CODE_SUBAGENT_MODEL`
when it is set to an alias or ID; then the main conversation's model. Kerd's effort
definitions are deliberately model-free, so an omitted `model` lands on the
environment variable when it is set and on the caller's model when it is not —
either way, on a model **not selected explicitly by the call**, which the call
cannot show. It may coincide with the one the plan wanted; nothing records that it
was chosen. A slice planned for Haiku can run on Opus, and the plan's cost
reasoning is then void.

**Naming `model` requests the model; it does not guarantee what runs.** Two
documented host conditions override an explicit request: with
`CLAUDE_CODE_SUBAGENT_MODEL_FORCE` set to `1`, Claude Code ignores the model field
and a caller cannot pass a model at all; and every requested value is checked
against an organization's `availableModels` allowlist, which substitutes the newest
permitted version of a blocked family alias, or the inherited model when no version
is permitted. So the request is what Kerd controls, and observed evidence is what
establishes the model that ran.

The two conditions call for different handling, and the difference is not cosmetic:

- **`CLAUDE_CODE_SUBAGENT_MODEL_FORCE` is `1`.** The call cannot carry a model, so
  native Claude dispatch is **unavailable as a compliant Kerd route** for as long as
  that setting holds. Choose another authorized route, or say plainly that the
  setting has to change and let the person decide. **Never retry the dispatch
  without `model` to get past it** — that is the defect this contract exists to
  remove, arriving with an excuse. Report the state rather than working around it.
- **An `availableModels` allowlist.** The request can still be made, and must be:
  send the explicit `model`, then report any substitution the observed evidence
  shows. A substitution is a finding about the environment, not a reason to stop
  naming the model.

**The countable test is `requested_model`, with one qualification that matters.**
`job_evidence.py` fills it from the job's own metadata, so a call that omitted
`model` reports `requested_model: null` while its status may still read `observed`.
But the field is *initialised* to null, and unreadable or invalid metadata leaves it
null too, recording a gap. So null is evidence of omission **only when the metadata
parsed and carries no model-related gap**; otherwise it is unverified, and counting
it as a violation would accuse a compliant dispatch. Count the qualified nulls
across a run's jobs and report the count separately from the unverified ones; the
contract holds at zero qualified nulls. A non-zero count is a finding about this
session's dispatches, not about the rows that described them.

Be exact about what that buys. This contract is instruction text at the point of
use: nothing blocks a dispatch mechanically, and no static check can confirm that a
call carried what a row promised. Afterward, `job_evidence.py` reads the requested
and observed values separately from the host's private transcript records; it
returns `unverified` with a reason whenever those records are missing or partial,
and an absent effort record means unverifiable, not confirmed.

Never send a dispatch without `model`. If you cannot choose between two models,
name both and their cost difference to the person and wait; no call goes out
meanwhile.

**A resume is not a second dispatch.** `SendMessage` to an existing job carries no
`subagent_type` and no new pair. The per-invocation `model` from the original call
keeps applying to a resume or follow-up, so an explicitly dispatched job stays on
its named model — which is another reason to name it at the first call. Say which
job is being resumed and the pair it was dispatched with; start a new dispatch
rather than a resume when the work needs a different pair.

A Claude session loads agent definitions when it starts, so a session opened before
they were installed cannot load them: say so rather than claim a reload, and take
the fallback above. Codex models are not added as Claude agent files. A Codex or
established-partner route names that route's own model and effort evidence instead;
it cannot carry a `kerd:effort-<level>` and is not expected to.

Effective effort can still differ from the request. `CLAUDE_CODE_EFFORT_LEVEL`
overrides definitions, `maxEffortLevel` and organization caps still apply, and an
unsupported level falls back to the highest supported level below it. Keep the
requested level, report the observed one separately, and treat a mismatch as a
finding. Record observed model identity separately; neither identity nor a
successful request proves that effort was applied.

This preparation applies to every assignment, including a delegated composer:
choose the recipient/route, consult applicable guidance, compose the actual
prompt and check it against the agreement before sending. Reuse matching guidance
already loaded for this model and task; don't reread it merely to announce a check.
An unresolved alias gets only guidance known to apply to that alias/family, or
the disclosed clear-contract fallback, never a guessed profile. If a returned
model identity differs, reassess the fit and preserve both requested and observed
facts; do not rewrite the history or automatically resend the job.

When an execution score applies, its complete applicable score step is the
shareable worker brief; do not require Conductor to rewrite it into a second
specification. Supplement it only with terrain the recipient lacks, current
dependency results, route/tool permissions, resolved recipient and required
transport or private-request fields. Provider guidance may change presentation,
not the intended outcome, exact constraints, proof or decision rights. Confirm
that the score step and supplement together are resolvable by this recipient.

Otherwise write a shareable prompt brief beside the work using ordinary Markdown
or useful XML boundaries. Agent's full requests and transport framing stay in
its existing private records; native subagent prompts stay in native history
unless safe to retain beside the work. Do not copy private inputs into public
files. Label sanitized briefs as such rather than claiming they are exact copies.
This is Conductor's judgment, not a required JSON form. A useful job contains
the outcome, selected source material, specific contribution, agreed success/proof,
allowed changes and stopping condition. A review receives the original agreement
and artifacts, not only the builder's summary. Keep irrelevant interview history
and the whole skill pack out of worker prompts.

For Claude, use descriptive tags when mixing instructions and source material;
use the selected profile's relevant effort/autonomy advice. For OpenAI reasoning
models, an applicable profile may favor outcome-first prose with native tools
and freedom over method. With no matching profile, use the same clear outcome
contract and disclose the fallback. Neither presentation changes the agreement.
An example is a writing aid, never an extra requirement or invented project fact.

Before sending, compare the prepared prompt or reused score step and transport
supplement with the agreed contribution: did it retain the required outcome,
evidence and boundaries? Correct transport omissions without changing the score's
semantics. This is a semantic check, not a fingerprint, parser gate or separate
user stop.

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
in the native setting when exposed. If the control isn't exposed, say no override
was set and leave effective effort unverified; prompt wording doesn't configure
reasoning effort. Keep requested and observed effort distinct. A subagent's return is its result; nothing is
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
request ID returns its existing result; another dispatch is a new request, not a
hidden rerun. Apply execution.md's score-failure distinction before sending it:
a sound step keeps the same semantics and gains useful failure evidence plus only
supported dispatch changes; a known defective passage returns immediately to
its author instead (Composer or Conductor). Keep the unsuccessful-attempt count for the same step and
measure across request IDs, aliases, routes, names and score repairs. The third
failed Player attempt triggers reassessment/hand-back, not a fourth request or a
conclusion that the score must be wrong. Do not relabel a failed assessment by
changing its measure name.
Use `cancel REQUEST` to request cancellation; inspect the final state before
claiming it stopped. `interrupted`/`unknown` means native work may still exist.
Reuse stays blocked; do not delete its metadata or kill an unverified stored PID.
`resolve REQUEST` retires uncertainty only after the recorded process group is
gone. Missing identity, permissions or detached work can still need inspection.
Report that limit honestly; never turn an uncertain launch into a claimed result.
