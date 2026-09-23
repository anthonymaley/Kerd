# Assess and show the work before starting

For a substantial build, design or workflow request, new or existing, offer
Conductor and useful proposed contributions; small fixes run directly. An explicit Conductor request opens it
without another invitation; ongoing guided work never needs a repeat offer.
Once selected, assess every task: a user-visible job/result, not each tool call
or microstep. Include small edits, questions, research and reviews within guided
work. Reassess material scope, dependency, evidence or route changes. Reuse settled
choices and guidance on unchanged work/resume; no repeated intake, profile reads
or model/account/billing surveys. Reconcile resumed jobs before dispatching.

## Establish suitability from available evidence

Start with the task's outcome, consequences of error, tools, context, authority,
success check and supplied resource limits. Assess the requirement and suitable
available pairs before deciding to retain the current controller or inherit it
for a worker; capability alone is not a reason to use the highest pair. Consider
the current controller and each useful contribution using [model choice](guidance/model-choice.md).
State the main pair's fit and evidence limits briefly; recommend an available
alternative when the current pair materially exceeds or misses the work's needs.
Give a brief reason for retaining or inheriting a pair. No universal switch,
cheap tier or proven optimum. Respect named models, existing partners, host role
choices and permission limits.

Keep settings evidence explicit: **host-declared** means supplied by the host;
**observed** means runtime confirmation; **configured** means a default/override
was read; **requested** means asked for; **reported** means otherwise supplied
without confirmation; **unknown** means no reliable reading. Model and effort
have separate evidence. Inheritance or defaults do not prove the effective pair,
and a successful reply proves neither identity nor applied effort.

Use already available session evidence or a supported, bounded status check.
Do not mine native transcripts, inspect credentials or survey accounts to fill
the display. The one exception is the observed model and effort of a native
Claude job Conductor dispatched in this session, read with
`skills/conductor/scripts/job_evidence.py --agent-id <id>`: best-effort. It
parses private, version-specific transcript records but reads only their
structured model and effort fields, and never emits conversation content. Partial
or malformed evidence returns `unverified`. When
it returns `unverified`, that is an evidence gap, not a failed job. Unknown live settings do not automatically block safe work or require
the person to verify them. Ask only if the missing fact changes a material
decision. Do not automatically change the current session's model/effort,
configuration defaults, permissions or accounts; state a recommendation and its
reason when a change is warranted. Select delegated settings only through the
chosen route's supported controls and within existing authority.

## Write the score before assigning executable work

Keep four responsibilities distinct; they are capability requirements, not
provider brands or permanent named assignments:

- **Producer** owns intent, priorities and agreement on consequential choices.
- **Composer** owns the score passages it writes and repairs to them.
- **Conductor** owns task-based session advice, the choice of who writes each
  step, staffing, dispatch, integration and judging returned evidence. When the
  work is already clear, Conductor writes the steps itself.
- **Players** execute individual complete score steps and return their evidence.

A composer call neither approves work, dispatches players, nor becomes a
persistent controller or an independent reviewer; it returns its score to
Conductor. Conductor preserves the agreement and makes routine staffing choices
within it. A new score exposes a material outcome, quality, scope or authority
change for producer agreement, but writing a score does not require a second
approval of an unchanged authorized request.

### Choose who writes the steps

Delegate by default whenever a job can be briefed and checked and the contribution
is useful, authorized and worth its transfer and integration cost; route 3 below
is the exception when it is not. The decision is who writes the brief, not whether
delegation needs a composer first. For each piece of executable work, choose one
route:

1. **Conductor writes the steps and delegates them** when the outcome, approach,
   files and checks are already settled by the agreement and terrain Conductor
   holds. Write each step in the complete form below, then assign it. Fan out
   independent steps to parallel players, choosing a suitable available pair for
   each and preferring lower cost where task evidence supports it against the
   complete step and its evidence bar. A composer call here adds cost without
   adding judgment.
2. **The composer writes the score** when the specification still needs design
   or reasoning Conductor cannot settle confidently: an unclear approach, a
   cross-file or public contract, competing constraints, or a step Conductor
   cannot write precisely enough for a cold player. Uncertainty about whether a
   step can be written precisely is itself the signal for this route.
3. **Conductor does it inline** only when the work is tiny, tightly coupled
   through shared state or sequencing, or judgment all the way through, so that
   briefing and integrating would cost more than it saves. State that concrete
   reason; being able to do it faster yourself is not one when a brief is cheap.

Routes can mix in one task: Conductor may write the clear steps and send a
design-heavy passage to the composer. Whoever writes a step owns its repair: a
defect in a Conductor-written step returns to Conductor, a defect in a composer
passage returns to the composer. Mark each step's author in the score or work
record so repairs route correctly.

For route 2, use an available top reasoning-capability composer at a separately
sized, supported effort. Compose in two passes:

1. Send the intended outcome, boundaries, constraints and actual authority, and
   ask for the smallest explicit named-file reading set required to write the
   score.
2. Retrieve exactly that terrain, the relevant agreement and available routes;
   provide them with a score template. The composer writes the score directly
   beside the existing work record and returns a short summary plus material
   risks to Conductor, which checks the score against the agreement before
   tagging or assigning any step.

Retrieval belongs to Conductor. If necessary terrain is missing, the composer
returns a named gap; it does not guess an interface or receive an unlimited
context dump. Whoever writes a step writes its substantive detail; never pass an
unfinished specification to a lower-capability player to complete.

Direction-setting without a selected authorized task stays inline; do not launch
a contributor merely to choose work. If route 2 is warranted but a suitable
composer is unavailable, disclose why and that Conductor is authoring that score,
then assess it against the same success bar. Do not claim that fallback is
necessarily inferior, silently substitute a named partner, or demand new approval
for an unchanged authorized task. Stop only when a real missing capability or
decision prevents safe progress. Return later defects in a composer passage to
the composer when that composer is available.

### Make every score step independently executable

Before assigning a step, write its complete body. A score step states its
intended result; rationale for non-obvious choices; exact files, interfaces and
values where relevant; dependencies; owned boundaries, including any generated or
ignored output paths the step may produce; authority; success and evidence; a
verification command and expected result; and any needed collateral or
qualitative review. Use the same contract for non-code work, with appropriate
artifacts and checks. A player receives sufficient settled intent to execute the
slice without re-deriving product intent.

Only after that body is complete, tag it `[delegate]` or `[keep]`. A
command-verifiable mechanical edit is necessary but not sufficient for
delegation: assess remaining judgment, context transfer, access, tools,
consequences and independent-review needs. A passing grep is not semantic proof.
Risk alone does not require keeping an otherwise well-specified edit; add an
explicit independent or seam review where damage could escape its command. Bias
toward delegation for a well-factored multi-step score, never toward a ratio,
quota, fixed keep count or a presumption that a kept step is mistagged.

Consider useful independent research, implementation and review at startup and
as they emerge, including the review an established partner's recorded cadence
schedules (see [plan independent review](#plan-independent-review-from-the-pairing)). Apply [job splitting](execution.md#prepare-and-do-the-next-useful-job):
assign a useful authorized complete score step or give its concrete inline reason,
such as tiny scope, shared-state sequencing, coordination/context-transfer cost,
or writing the step costing more than doing the work. A finished score step's
remaining transport supplement is not by itself a reason to keep work inline.
Independent steps run in parallel; give editors disjoint ownership or serialize
shared-file changes.

### Size roles and advise the controller by the work

Size the controller for dispatch, conformance judgment and escalation, separately
from the hardest underlying design problem. Advise down as well as up where the
available evidence supports it: top-tier design does not automatically require a
top-tier or high-effort controller session. Do not require a settings-confirmation
survey or change settings automatically.

Use [model choice](guidance/model-choice.md) to map composition, evidence
judgment, standard implementation and mechanical work to suitable available
capability. Choose supported effort independently for each contribution, and give
a task-based reason for retaining or inheriting a pair. Respect named models,
existing partners, host role choices and permission limits; no universal tier,
cheap-worker rule, worker quota or claimed optimum follows from this guidance.

When Conductor is open for direction-setting without a selected authorized task,
keep composition and control inline using bounded local context. Show that
boundary; do not dispatch model jobs merely to choose work. A direct authorized
research/review request can itself be the task, authorizing its permitted contributors.

### Plan independent review from the pairing

At startup, read this project's established partners with Agent's read-only
`agent.py --project /PROJECT partners`; do not parse its private binding files.
It returns each binding's role, `review_cadence` and validity without contacting
any session. Select the reviewer by recorded role and task fit; when several
remain materially plausible, show that choice once. Never schedule every binding
or choose by recency. An invalid row is a routing gap to show, not a partner.

Plan that partner's reviews from its cadence and show them as rows in the startup
grid, with the gate each protects:

- `checkpoints`: at the risk points this plan names;
- `before-push`: the full change set before commit, push or release;
- `end`: once when the work completes;
- `on-request`: no automatic partner review.

With an established partner and no recorded cadence, propose one grounded in this
task's risk, ask once, and record the answer through Agent (`pair` with
`--review-cadence`); do not ask again. The person can change it by telling any
session. With no established partner, plan independent review from the other
available routes as before.

A cadence schedules review only inside authorized work. It grants no work,
contact beyond that work, commit, push or release, and a review never approves
an action. `on-request` does not waive Conductor's own independent assessment in
[review, prove and improve](execution.md#review-prove-and-improve). Inside
[managed Conductor](managed-conductor.md), the forced review after every
implementation takes precedence over a stored cadence.

One accepted review satisfies coincident gates, such as a final checkpoint,
before-push and end, only while the reviewed tree and evidence stay unchanged.
Any change after it, including a correction the reviewer asked for, invalidates
every gate that review satisfied: repeat that gate before its protected effect,
unless another coincident gate necessarily runs first and reviews the current
tree and evidence.

## One visible startup view

Before substantive execution, show the actual stage, intended result, owner and
stopping boundary, with the suitability and inline/delegation decision. Use the
[existing work grid](journey.md#delegation-grid-and-preparation-updates), including
the controller, any composer call and each assigned step (Conductor- or
composer-written) in the same view. Show only real
assignments; inline composition need not become a separate row. Include a controller
row even when no worker launches. This illustrative tiny task needs only one row:

| Task | Who | Model requested | Effort | Status |
| --- | --- | --- | --- | --- |
| Controller: correct the heading and check the diff | This session, inline | Host-declared model if supplied, otherwise unknown | Live effort unknown unless verified | Ready inline |

Fit · Controller — needs one exact wording edit and a diff check; the current
session because the edit is tiny and judgment is minimal.

“This single heading edit fits inline work; briefing a contributor adds more
work than it resolves. I'll retain the current session and check the diff.”
In real work, substitute the actual evidence and decision.

Directly under the grid, give a **Fit** line for the controller and for every
newly selected model job — composer, player and reviewer — as
`Fit · <job> — needs <requirement>; <pair> because <reason>`. Identical jobs may
share one line. Add `; consider <alternative>` only when the pair materially
exceeds or misses the need; do not manufacture alternatives. Write another Fit
line whenever a job's model, effort or route differs from its plan or changes on
retry, before dispatching it. A grid row naming a model without its Fit line is
incomplete.

**Every native Claude dispatch row names both cells concretely before dispatch**,
matching the call that will be sent: the model as Haiku, Sonnet, Opus or Fable, and
the effort as low, medium, high, xhigh or max. The call carries that `model` and the
matching `kerd:<model>-<effort>` agent (`kerd:sonnet-high`), or plain `kerd:haiku`,
whose effort cell reads not supported; the grid shows the plain level and says who does the
work in plain words, never the routing label. This covers composer, player and reviewer alike — anything
sent with an `Agent` call. The `model` cell has no exception. The effort cell takes
the documented fallback when the effort definitions are not loaded in this session:
a concrete ordinary `subagent_type` with effort shown as “unset and unverified”, and
the reason disclosed. “Per definition”, “inherited”, “the controller's”,
“default”, “unknown” or an empty cell is not a valid plan for such a row; see
[the dispatch contract](model-jobs.md), which also gives the documented resolution
order an omitted `model` actually follows. A Codex or established-partner row names
that route's own model and effort evidence instead, labelled configured, requested,
observed or unknown; it cannot carry a Kerd routing agent and is not expected to.

Exactly one row per grid is the controller row: the row whose work this session
performs itself, with no `Agent` call. It reports its own host-declared or unknown
settings, because it is not a dispatch. Any row whose work is performed by another
agent is a dispatch and carries both cells, whatever the row is called — a row
labelled “controller” that results in an `Agent` call is a mislabelled dispatch,
not an exemption.

After the run, what actually executed is read with `job_evidence.py` and reported
beside the requested values; a mismatch is a finding, and a returned result never
proves the pair. `requested_model: null` is the signature of a call that omitted
`model` **only when that job's metadata parsed without a model-related gap** —
the field is also null when metadata is unreadable, and treating that as a
violation would accuse a compliant dispatch. Naming `model` requests a model; a
forced-model host setting or an organization allowlist can still substitute
another, which is why observed evidence and not the call establishes what ran.

## Prepare, send and assess visibly

Before an actual send, follow [model jobs](model-jobs.md) and consult applicable
[local guidance](guidance/README.md) for the selected model and route. Reuse a
still-applicable profile already read. Apply matching clauses and record the
version, or disclose no matching profile and use the clear outcome-contract
fallback. A family name or formatted headings do not establish tailored prompting.

For a complete score step, reuse that step plus its identified transport
supplement as the saved shareable brief; do not rewrite its outcome, constraints,
proof or decision rights. Only when no score step applies, prepare the real brief
with outcome, sources, contribution, success/proof, allowed changes, unresolved
questions and stopping condition. Check it against the agreement. Full private
requests stay in their established private store or native history. State which
brief was retained; a sanitized brief is not an exact copy. Inline work needs the
same clear contract, without a fake prompt or dispatch log.

Show actual guidance use and preparation before sending; then distinguish
prepared, submitted/queued, observed running, returned, checked and blocked/failed.
A saved prompt is not a launch, submission is not running, and return is not a
passed outcome. Retrieve and assess actual results, show useful findings and
their effect on the next action, and continue authorized work. Keep choice,
prompt and result evidence in the existing record, without private IDs or a
second tracker. Follow the journey guide for ongoing updates.
