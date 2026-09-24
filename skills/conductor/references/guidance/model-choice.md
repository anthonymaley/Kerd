# Choose the model for the work

Selection guide v2026-09-24. Read when assigning a new kind of job or reconsidering
a choice; reuse a still-applicable choice for the same work. This is Conductor's
input, not a questionnaire for the user or an automatic scoring service.

## What each source can tell us

Keep three different facts separate: **provider-described capability**, **tools
and access on this execution route**, and **results on comparable work**. A model
can be capable but unable to inspect an image or run a test through this route.
Vendor recommendations are useful starting hypotheses, not neutral league tables.
No cross-provider ranking or statistically established winner exists in this pack.

### Working shortlist, not an exhaustive model catalogue

Official descriptions below were checked on 2026-09-23. They suggest candidates
to consider, not exclusive jobs or automatic assignments. Availability in an API
catalogue is not proof of access through this user's CLI/account. Other models,
including an explicitly requested older model, can be considered on the same basis.

| Model | Provider-described fit | Local prompt guidance | Evidence qualification |
| --- | --- | --- | --- |
| GPT-6 Astra · `gpt-6-astra` | Most capable model for complex work across code, apps and research | [GPT-6](openai/gpt-6.md) | No matched selection comparison recorded here |
| GPT-6 Sol · `gpt-6-sol` | Complex coding and agentic workflows, with stronger factual reliability | [GPT-6](openai/gpt-6.md) | No matched selection comparison recorded here; the GPT-5.6 Sol evidence below is not credited to it |
| GPT-6 Luna · `gpt-6-luna` | Most efficient, for focused high-volume work | [GPT-6](openai/gpt-6.md) | No matched selection comparison recorded here; price is not eligibility |
| Claude Opus 5.5 · `claude-opus-5-5` | Long-running agentic coding and knowledge work; Anthropic's default starting point | [Opus 5.5](anthropic/opus-5-5.md) | No matched selection comparison recorded here; the Opus 5 review evidence is not credited to it |
| Claude Fable 5.1 · `claude-fable-5-1` | Demanding reasoning and long-horizon agentic work, after Opus 5.5 still falls short at xhigh or max | [Fable 5.1](anthropic/fable-5-1.md) | Do not credit the earlier Fable 5 drafting trial to 5.1 |
| Claude Sonnet 5 · `claude-sonnet-5` | The best combination of speed and intelligence | [Sonnet 5](anthropic/sonnet-5.md), explicitly partial | No matched selection comparison recorded here |
| Claude Haiku 4.5 · `claude-haiku-4-5` | The fastest model with near-frontier intelligence; takes no effort setting | No specific profile here | No matched selection comparison recorded here; not a default cheap worker |

**The conducting session:** Kerd recommends Opus 5.5 for the session that
conducts, at medium effort by default, for its efficiency on long agentic work
(the person's direction, 2026-09-24). This is advice for the person's own session
setup: Conductor never changes the current session's model or effort itself, and
it reports that session's active effort as unverified unless read from the session.

**Older:** Claude Opus 5 (`claude-opus-5`, [profile](anthropic/opus-5.md)),
which Anthropic now lists as a legacy model, still available. **Previous OpenAI
line:** GPT-5.6 Sol, Terra and Luna ([profile](openai/gpt-5-6.md)) are no longer in the
API catalogue's general-model list (2026-09-23), while the Codex models page says they
remain available during the GPT-6 rollout. GPT-6 has no Terra tier. Use either when a person asks for it
or a run is being reproduced; their evidence below stays theirs.

The three OpenAI descriptions come from the [official model catalogue](https://developers.openai.com/api/docs/models),
except Sol's "stronger factual reliability", which is from the [Codex models page](https://learn.chatgpt.com/docs/models).
The four Claude descriptions come from [Anthropic's selection guide](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model).
These descriptions do not establish that one provider is better at writing or
coding than the other. Broad text/image capability does not establish audio,
video, live browsing or native document editing in a particular job route.

Local evidence: [portable task-evidence summary](task-evidence.md), with the
original development-record locations and limits. The installed package does
not need the trial repositories or their private session metadata.
In the latter, historical `model/high` shorthand records the requested pair unless
separate runtime evidence establishes more. None of these is a matched tier or
effort sweep. A passed job is evidence for that job, not certification of a class.

## Who delivers and who reviews

By default, Conductor delivers with its own host's native workers and the other
provider reviews: in Claude Code, Claude players with a Codex reviewer; in Codex,
the reverse. That arrangement is working, and mixed-provider builds are not a goal.

A cross-provider implementation worker is an exception, used only when the person
explicitly asks for it or approves Conductor's proposal of it, with a concrete
reason: work stalled on the native route, relevant evidence of a better fit for this
task, or the person's own reason (spare capacity on the other provider, for example).
Name the reason in the Fit line. Where no comparative evidence backs it, call the
exception a reasonable trial, not a claim that one model is better. Conductor may
propose an exception; it never assigns one on its own reading. The other provider reviewing
is the default; the existing rules for an established partner, its review cadence
and the fresh-reviewer fallback are unchanged.

### Task fit: what each kind of evidence supports

Profiles suggest candidates; results earn preferences. Keep the three kinds apart:

- **A vendor suggestion** (the provider's description, the profiles here) makes a
  model a candidate for a kind of task. It supports no preference.
- **Successful local use** (a recorded job on similar work that met its agreed
  outcome) supports trying that model again for similar work. One success is not
  a preference over models that were never tried on it.
- **Comparative evidence** (the same brief, inputs and checks run on more than one
  model, with the results recorded) is the only kind that supports preferring one
  model over another for that kind of task, and only as far as the comparison went.

Broad labels such as "coding" or "writing" are not task fits and never become fixed
provider assignments. Describe the task by its outcome, the judgment it needs and
the tools it requires, then ask which kind of evidence speaks to that.

## Make the choice

1. **Understand this contribution.** Identify the outcome, kind of judgment,
   consequences of error, required sources/tools, review independence and any
   actual time/resource constraints. Do not assign by a level name alone.
2. **Check what can actually do it.** Respect a requested model, permitted
   providers and data boundaries. Exclude routes missing essential tools/access.
   The bundled Claude worker has file tools, not shell: it cannot own a run-tests
   obligation without a separate authorized test step. Rendering/vision must
   actually be available for visual assessment. A bigger model cannot fix this.
3. **Prefer relevant evidence over reputation.** Consider suitable candidates
   on the delivery route [above](#who-delivers-and-who-reviews), and across both
   providers for review or an agreed exception, using the same success bar. Do not
   favor inherited settings, highest price, newest name or a familiar role label. Retain or inherit the current pair only after that
   assessment, with a task-based reason.
   With no comparable evidence, choose a defensible capability-first starting
   point, state the uncertainty and assess its first useful result. Missing
   historical evaluation is not a universal ban on trying a model.
4. **Choose supported effort, then prepare the prompt.** Use task evidence and
   current model/route guidance. Opus 5.5 defaults to medium and Fable 5.1 to
   high; the documented default is a starting point, not a proved optimum. For other models, use an evidenced
   supported setting or disclose the native default; never copy effort labels
   between providers as though equal. Apply the level through the route's control
   in the [route table](../model-jobs.md#prepare-work-the-chosen-model-can-do-well):
   for a native Claude job that is the matching `kerd:<model>-<effort>`, or plain `kerd:haiku`, whose effort is not supported, then confirm what ran
   with `job_evidence.py`. Load only applicable prompt guidance and
   keep the same outcome, proof and boundaries whatever the model.
5. **Explain briefly, run, learn.** Record the chosen model/route, requested
   effort, profile version, reason, relevant alternative and uncertainty in the
   existing job note. Show the person a short useful explanation as the Fit line
   under the work grid ([startup contract](../orchestration.md#one-visible-startup-view)),
   not a selection approval form. Assess actual artifacts and feed findings into future choices.

Quality remains the agreed bar. Among routes with evidence they meet it, use
elapsed time and total resources per accepted outcome to improve efficiency—not
token price alone. If no suitable route fits a real allowance, propose a smaller
scope or staged delivery and obtain agreement; don't silently lower quality or
change a named model. No stated limit does not grant new purchasing authority.
These are product choices; vendor cost-first strategies do not override them.

For independent review, use a different suitable model where available, with
the original brief, raw artifacts and relevant sources. Different branding is
not proof of independence; avoid priming with the builder's verdict. If only
the same model is suitable, use a fresh session and disclose the limitation.
Do not add model-to-model conversation rounds without a concrete job to do.

Official basis for task-specific evaluation and quality-first optimization:
[OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection).
Effort differences and testing advice:
[Claude effort](https://platform.claude.com/docs/en/build-with-claude/effort).

## Examples of decisions, not routing rules

| Job | A defensible decision |
| --- | --- |
| Review a draft guide against supplied notes | Consider appropriate analysis-capable models from either provider. Terra has one relevant bounded example here; that supports consideration, not superiority over Sonnet or Opus. Use a different suitable reviewer from the builder. |
| Implement a change and run its tests | Choose a route with authorized editing and shell/testing. Claude's file-only bridge can contribute implementation, but cannot claim the test result; name who runs it. |
| Judge a diagram's readability | Require actual rendered-image access. A text-only reply about SVG source cannot establish visual quality, regardless of model tier. |
| Draft a novel executive recommendation | Consider strong reasoning/source-synthesis candidates on the native delivery route, or from the other provider as an agreed exception. Novel work may have no close local baseline; disclose that and independently check claims, options and decision consequences. |
| The person says “use Codex for this build, it has capacity” (Conductor in Claude Code) | An explicitly requested exception with the person's reason. Name it in the Fit line as a trial unless comparative evidence exists; the review still goes to a different suitable model. |
| A native player has stalled twice on the same step | Propose a cross-provider worker for that step with the stall as the reason, and wait for the person's yes; do not switch on Conductor's own reading. |
| User says “ask Claude” | Use a suitable available Claude route. If unavailable, ask about the alternative; do not silently substitute Codex to keep moving. |

User-facing example: “I'll use an independent source-based review for this draft.
The selected route can read the notes and finished file. We have one similar
trial, but no evidence that it is the best model; the agreed checks still decide.”
In a real job, name the selected model and requested effort rather than hiding them.

## Keep it useful without building a benchmarking bureaucracy

Use local guidance first. Refresh the relevant official source when a new model,
changed CLI, capability conflict, provider change or adverse result makes it
necessary; do not browse the entire catalogue for every job. Check exact limits
when the job depends on them. Record catalogue/profile version and source date
in the choice note so past decisions remain understandable after guidance changes.
Preserve a prior version when changing a claim used in a recorded run.

Judge a result first by whether it met the agreed outcome; then by rework, human
intervention, elapsed time and usage. Record the actual model,
effort and tool access beside it (requested and observed kept separate), with the
task, checks and prompt/profile, so an observation is not credited to the wrong
thing. Unknown readings stay unknown. Keep the observation in the work's own
record and link the useful ones where the next model choice will find them (for
Kerd's own development, [task evidence](task-evidence.md)); no new routing
framework, provider quota, leaderboard or database.

When a comparison is worthwhile and authorized, hold the brief, inputs, authority
and success checks stable; allow each model an appropriate prompt and supported
effort. Record route differences. Include failures and retries, not only winners;
use order-balanced or blinded review where practical. Compare enough representative
work before a broad claim, without inventing a mandatory sample count. A routine
job need not run on several models merely to feed a leaderboard.
