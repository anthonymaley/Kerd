# Choose the model for the work

Selection guide v2026-09-08. Read when assigning a new kind of job or reconsidering
a choice; reuse a still-applicable choice for the same work. This is Conductor's
input, not a questionnaire for the user or an automatic scoring service.

## What each source can tell us

Keep three different facts separate: **provider-described capability**, **tools
and access on this execution route**, and **results on comparable work**. A model
can be capable but unable to inspect an image or run a test through this route.
Vendor recommendations are useful starting hypotheses, not neutral league tables.
No cross-provider ranking or statistically established winner exists in this pack.

### Working shortlist, not an exhaustive model catalogue

Official descriptions below were checked on 2026-09-08. They suggest candidates
to consider, not exclusive jobs or automatic assignments. Availability in an API
catalogue is not proof of access through this user's CLI/account. Other models,
including an explicitly requested older model, can be considered on the same basis.

| Model | Provider-described fit | Local prompt guidance | Evidence qualification |
| --- | --- | --- | --- |
| GPT-6 Astra · `gpt-6-astra` | Difficult reasoning, coding and end-to-end work | No model-specific profile in this pack; disclose the clear outcome-contract fallback | No matched selection comparison recorded here |
| GPT-5.6 Sol · `gpt-5.6-sol` | Complex professional work | [GPT-5.6](openai/gpt-5-6.md) | Bounded managed-work evidence; not a general ranking |
| GPT-5.6 Terra · `gpt-5.6-terra` | Balance of capability and cost | [GPT-5.6](openai/gpt-5-6.md) | Bounded source-based review; requested identity/effort, not observed Codex identity |
| GPT-5.6 Luna · `gpt-5.6-luna` | Cost-sensitive, high-volume work | [GPT-5.6](openai/gpt-5-6.md) | No matched selection comparison recorded here; price is not eligibility |
| Claude Fable 5.1 · `claude-fable-5-1` | Demanding reasoning and sustained agentic work | [Fable 5.1](anthropic/fable-5-1.md) | Do not credit the earlier Fable 5 drafting trial to 5.1 |
| Claude Opus 5 · `claude-opus-5` | Complex coding and enterprise work | [Opus 5](anthropic/opus-5.md) | Bounded independent-review evidence; not a general ranking |
| Claude Sonnet 5 · `claude-sonnet-5` | Everyday coding, analysis, content and tool use | [Sonnet 5](anthropic/sonnet-5.md), explicitly partial | No matched selection comparison recorded here |
| Claude Haiku 4.5 | Low-latency, high-volume work | No specific profile here; verify exact available ID and supported controls | No matched selection comparison recorded here; not a default cheap worker |

The four OpenAI descriptions come from the [official model catalogue](https://developers.openai.com/api/docs/models).
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
   across permitted providers using the same success bar. Do not favor the
   controller's own provider, its inherited settings, highest price, newest name
   or a familiar role label. Retain or inherit the current pair only after that
   assessment, with a task-based reason.
   With no comparable evidence, choose a defensible capability-first starting
   point, state the uncertainty and assess its first useful result. Missing
   historical evaluation is not a universal ban on trying a model.
4. **Choose supported effort, then prepare the prompt.** Use task evidence and
   current model/route guidance. For Opus 5 and Fable 5.1, high is the documented
   starting point, not a proved optimum. For other models, use an evidenced
   supported setting or disclose the native default; never copy effort labels
   between providers as though equal. Load only applicable prompt guidance and
   keep the same outcome, proof and boundaries whatever the model.
5. **Explain briefly, run, learn.** Record the chosen model/route, requested
   effort, profile version, reason, relevant alternative and uncertainty in the
   existing job note. Show the person a short useful explanation, not a selection
   approval form. Assess actual artifacts and feed findings into future choices.

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
| Draft a novel executive recommendation | Consider strong reasoning/source-synthesis candidates from either provider. Novel work may have no close local baseline; disclose that and independently check claims, options and decision consequences. |
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

Keep result evidence beside the work: task/checks, requested and observed model
details separately, prompt/profile, route/tool access, actual outcome, corrections,
human interventions, elapsed time and available usage. Unknown readings stay
unknown. Link useful evidence here rather than copying full results into a database.

When a comparison is worthwhile and authorized, hold the brief, inputs, authority
and success checks stable; allow each model an appropriate prompt and supported
effort. Record route differences. Include failures and retries, not only winners;
use order-balanced or blinded review where practical. Compare enough representative
work before a broad claim, without inventing a mandatory sample count. A routine
job need not run on several models merely to feed a leaderboard.
