# Conductor rework — next implementation spec

**Isolated candidate build in progress; session-routing MVP accepted.** See
[the trial history and unproved behaviors](trials/conductor-first-slice.md) and
[the connected delivery build](trials/integrated-delivery.md).
The broader removal/adoption work is not executed. Implements
[the lightweight-process design](kerd-conductor-rework.md), replacing the previous
plan to extend Kerd's gate ladder. No live skill, gate, hook, CI workflow, session
marker or user record is changed by this document.

## The result we want

A person uses Kerd without setting up CI, hooks, seals, requirement fingerprints
or a gate schema. Conductor guides understanding and design, records agreement,
and delivers through appropriately prepared model jobs, independent review and
evidence. Switch can resume the work.

**Understand → Shape → Agree → Deliver → Complete.** Stages communicate the work,
not permission granted by file parsers. Success means achieving the agreed
outcome, not satisfying a paperwork contract.

## Remove, do not rename

| Existing mechanism | Implementation action |
|---|---|
| gate.py route/check and rung-specific artifact obligations | Remove from skill entry, advancement and completion. Do not add another new-path rung contract. |
| View seals, requirement/approval fingerprints, hash-triggered invalidation | Remove from approval and resume. Record agreement in readable text; review meaningful changes. |
| Required question sets, rigor enums, killer-risk rows, MSC registration and reciprocal links | Remove as Kerd usage obligations. Keep useful facts without forcing the old schema. |
| Mandatory Pieces/Verify scores and Piece trailers | Remove as execution/progress prerequisites. Retain ordinary plans, useful tests and commit evidence where relevant. |
| CI presence, progress-staleness and fidelity refusers | Remove from all Kerd usage paths. No-CI projects are fully supported, not a degraded exception. |
| Custom hooks for dispatch, approval or retry enforcement | Do not build or require them. Remove workflow-critical dependence on informational hooks. |
| Compulsory composer, fixed staffing tiers, separate Drive loop | Replace with one Conductor process and bounded jobs chosen for need. |
| Duplicate state and mandatory question endings | One active work record; update affected skill and injected instructions consistently. |

Tools contain shared helpers and Kerd-development checks. Remove runtime callers
first, retain clearly separated development-only checks where useful, and delete
obsolete implementations after checking remaining callers. Do not blindly delete
directories or export developer checks to consuming projects.

Ordinary Git hashing and unrelated integrity tools are not deletion targets.
The target is the Kerd agreement/requirement fingerprinting protocol and its
usage obligations. Existing useful optional hooks may remain, but no Kerd
workflow may require the user to configure them.

## Minimum work record

One readable file per work package, in an existing appropriate location or
docs/work/<work-name>/work.md. Add drawings, long prompts, reviews and deliverables
beside it only as needed. No schema parser is required before the first trial.

~~~markdown
# Work: <outcome in ordinary language>

## Agreement
Outcome and deliverables:
Success measures and how we will assess them:
Scope, boundaries and authority:
Time/resources and stopping point:
Direction shown: <drawing and necessary detail>
User agreement: <actual response and conditions>

## Decisions and changes
<What changed, why, and any new user decision.>

## Now
Stage and current activity:
Open issue or pending question:
Next action:
Active jobs and result links, if any:

## Results and evidence
<Each measure: met / not met / cannot be assessed; evidence and reviewer.>
~~~

These are writing aids, not required headings a checker uses to permit work.
Omit irrelevant detail, not unresolved authority. Do not silently rewrite the
original agreement. Link full prompts and longer reviews so pickup can find
them. Session IDs and sensitive routing data stay local.

Use named measures, readings and evidence where appropriate. Reference existing
project measurement records directly. No new requirement-ID system or formal
acceptance-record grammar is part of this build.

## Build sequence

### 1. Prove start, shape, agreement and resume

Build the first experience in an isolated ordinary Kerd clone. Do not replace
the installed plugin, repin other projects or alter the parked session. Load
the candidate explicitly and report which copy is under trial. Do not carry two
whole protocols in one skill or migrate old records just to try the new one.

Check minimally for active work. If fresh, use the supplied intent or ask the
opener, then read relevant context. Ask useful questions one at a time, challenge
unsupported premises and shape the direction. Conductor decides necessary
analysis/review depth; the user does not select a rigor tier.

Load [the adaptive understanding guide](skills/conductor/references/understanding.md)
after intent is known. The 2026-09-08 user agreement supersedes mandatory ten-topic
presentation and confirmation; the ten areas stay internal. Reuse the request
and relevant sources. Ask only consequential missing information, propose scope
and checks where useful, or defer a later issue with a named revisit point.
No fixed question count, duplicate register or required parser fields.

Keep each material item's status/source and when it is needed with the brief.
Source facts are not new permission. Missing budget is not spending authority.
Must / Prefer / Open distinguish requirements from preferences and delegated
method. Help deciding produces advice; uncertainty stays open. Show a concise
working interpretation before substantial execution and obtain any new material
agreement, not a second yes for clear existing authority.

Natural build/create/plan wording belongs in the skill description for host
discovery. Don't promise activation before installation or precedence over higher
instructions. Route small explicit authorized edits directly; don't create a work
package just to change a typo. Preserve planning-only and review-only scope.

Recover the person's stated definition of success or ask for it. Translate it
together into observable results, what is good enough and independent evidence;
do not substitute agent-written functional tests for the desired benefit.
Present and establish agreement to that summary within the direction conversation.
Keep proposals distinct from agreed measures. A scope-only “yes” cannot close
this step while success remains unconfirmed. Resume at that gap if necessary,
preserving the scope decision instead of restarting intake. No numeric targets,
measurement registry or extra formal approval step are required by this rule.

Use [the journey presentation guide](skills/conductor/references/journey.md) as
the single presentation contract. It owns the bounded question/answer card, native
and plain-text host adaptations, compact working-brief view, acknowledgement and useful
insight pattern, early visuals and live-work view. Do not copy a second layout rule
here. A ban on textual choices removes the choices, not the answer panel or progress.

Show the current stage, what is settled, the live decision/activity and next action.
Use visuals when they clarify the actual work; no numbered-topic schedule or
required visual quota. Keep internal Can use / Save labels out of the user flow.

A substantial package’s integrated direction still needs a useful rendered product view. Small explicit work does not need a compulsory diagram.
Progress and handoffs distinguish actual activity, completed work and next owner.
Save the actual agreement and next action; no seal or approval fingerprint.
The original first-slice planning stop is superseded for the expanded candidate:
when direction and execution are actually authorized, continue into step 2 in
the same run. Preserve expressly planning-only agreements; don't reinterpret
historical permission. A document finished is not the work finished.

Use the [journey presentation guide](skills/conductor/references/journey.md):
show the current stage in the whole journey, with interview topic or active job
underneath. At consequential decisions, present relevant findings, uncertainty,
recommendation and tradeoff, then the complete decision card. Explain which part
of the outcome the decision affects and what it enables. No intake counter is required for orientation. The product drawing shows what we are creating;
the journey strip shows where we are. Keep them distinct and connected.

For this candidate, read [the local visual skill](skills/visuals/SKILL.md) when
preparing that view, then its selected pattern guidance. This codifies the useful
diagram-design approach without its onboarding pauses. Use the
[worked example](skills/visuals/assets/review-flow.html) as a visual starting
point, not as the task's approved facts. [Both diagram-design and Archify are
retained choices](visual-tools-assessment.md): Conductor chooses by the work and
the person's preference, without a rigid division of uses. Either may serve the
first direction review, and both may serve one work package when useful. Do not
duplicate every view or turn either tool into a universal setup prerequisite.

**Demonstrate:** the real session-routing request reaches a direction the person
can explain unaided: outcome, connected parts, success, boundaries and next step.
A fresh session restores the exact pending question/action from saved work, not
remembered conversation. Missing context is disclosed. No CI, hooks, gate tools
or special register files are installed or invoked.
The person can locate the question and tell what response is needed without
reading a progress essay. Check the callout in the actual chat/terminal surface;
source formatting alone does not prove that it stands out.
Also check whether the person can identify the current stage, the key finding
behind the decision and what happens after answering. Observe a real transition
from agreement into authorized action: no extra “go on”, no bare acknowledgement,
and no skipped visual direction or success agreement. A resumed delivery record
continues its next action rather than replaying the interview. These are behavior
checks, not heading/string assertions, and remain unproved until exercised.
Also demonstrate that the recorded success criteria trace to the person's input
or explicit response to the presented summary. With no success definition, the
candidate asks; with one already supplied, it reuses it. Scope-only agreement
leaves success unresolved rather than manufacturing approval of proposed checks.
Exercise an already-answered brief as well as an incomplete one: the former
presents supported answers to confirm instead of blank questions. A follow-up
stays under the same topic; a revised answer updates affected topics without
restarting. Resume must restore the pending confirmation or follow-up, not count
a drafted answer as settled. A discoverable technical unknown leads to authorized
investigation, not a demand that the person supply an implementation answer.

### 2. Connect prompt preparation and the work loop

Reuse useful parts of mvp/compiler.py and guidance/, not their existing
manifest/fingerprint scheme as a runtime dependency. Keep official source links,
retrieval dates, applicable model and examples locally. Refresh guidance
separately when needed, not by browsing before every job.

Implementation choice: Conductor prepares the prompt using the relevant local
guidance; the old deterministic compiler remains a historical experiment. The
candidate bundles the accepted transport under skills/conductor/scripts/ask.py
and loads references/model-jobs.md at delegation. The consuming project needs
no copied script, CI or hooks. Native authenticated CLIs, Git and Python/POSIX
support are dependencies of this optional adapter, not fabricated capabilities.

For each bounded job, choose an appropriate available model and effort, prepare
the outcome/context/boundaries/proof prompt and use a supported execution route.
The [model-choice guide](guidance/model-choice.md) is the shared selection input:
dated provider-described fit, applicable prompt profiles and linked task evidence,
qualified by the actual route's tools and permissions. Consider permitted providers
on the same success bar; record why the choice fits and any important alternative
or uncertainty. No model gets a staffing role by brand, price or controller identity.
Choose appropriate supported effort before preparing the prompt. Preserve the
agreed quality; negotiate scope if real resource constraints cannot support it.
Missing comparisons remain unknown, not invented scores or a universal ban on
first use. Assess the first real contribution and retain failures as well as wins.
The preparation step must actually select and read the relevant guidance—not
just mention a reference folder. Inspect actual prompts for preserved meaning.

Use foreground or background work as supported. No inbox or manual ID copying;
session routing must demonstrate its capabilities, not assume them. Independent
review uses the original agreement and result. Correct specific failures and
verify the integrated outcome. Three materially different failed corrections
of one measure trigger reassessment, not an automatic user question or reset.
Honor resource limits and revoked authority.
Numeric/time limits are optional; absent limits do not block dispatch. “Use it
all” means pursue the agreed outcome until complete or the available allowance
is exhausted, not manufacture work or authorize new purchases/paid overages.
Within agreed authority, continue from one useful job to the next without asking
for permission merely because a step finished. Progress reports are not stops.

**Demonstrate:** actual Claude and OpenAI jobs return useful results, with prompts,
model/effort, reviews and evidence available. A failed measure gets a targeted
correction; changed desired outcomes get a user decision; exhausted resources
stop further work; unavailable providers are reported honestly. Exercise actual
behavior, not whether a fixture can parse a counter. These observations do not
prove that a skill is an unbypassable security mechanism.

Selection checks: a named model is not silently substituted; a route without shell
cannot own an unassigned test obligation; a text-only reviewer cannot claim visual
inspection; an untested inexpensive model is not selected merely to lower price;
a new capable model may be tried with disclosed uncertainty and independent proof.
These are behavior cases to exercise, not a claim that documenting them passed them.

### 3. Connect progress and Switch; remove old runtime dependencies

Present the record's stage/activity, completed outcomes, evidence, next action
and user decisions. Do not derive a rung through kit.py or require a commit,
board refresh or CI run to update progress. Separate reported activity from
reviewed results and reconcile discrepancies with the actual work.

Switch reads the work pointer and next action. Update its Active Mode snapshot
handling explicitly. Conductor records work progress; Switch writes the boundary
summary/history, without rewriting the complete work plan a second time.

Candidate implementation: use an existing appropriate project handoff location,
or docs/work/SESSION.md pointing to the work and appended session history.
Do not write or restore legacy .active-modes. Saving is local unless Git/transfer
was separately authorized; pickup never assumes private native sessions moved
with project files. The isolated Switch replaces the old clone's boundary skill;
the installed Switch and parked session remain untouched.

Remove obsolete usage rules from Conductor, Drive, Switch and affected specialist
skills, plus playbook/state/talk instructions and hook-injected text. Inspection
found relevant references in interrogate, lorg and slainte too: this is not a
Conductor-only CI exception. Review callers rather than blanket-delete useful
tests or project-specific evidence handling.

**Demonstrate:** start/resume/status/completion and affected skill entry paths
work in a consuming repository with no CI workflows, custom hooks, old gate
scripts or registered requirement schema. Views remain understandable after
failure, interruption and missing evidence. Existing project CI can supply
relevant evidence without Kerd installing, modifying or depending on it.

### 4. Finish real-work proof and adopt

Continue the [session-routing](trials/software-session-routing.md) and
[Wholematter](trials/wholematter-ddil-outcomes.md) contracts using this process.
Do not preload interview answers or duplicate the old-path baseline. A peer
reviews against the original outcome. Report usable deliverables, unmet measures,
questions/interventions, elapsed time and resource information actually available.

At adoption, replace the old Drive/Conductor ownership, outside-model rung
enforcement, producer-only acceptance, measurement freeze scheme and compulsory
question rules in living instructions. Do not leave contradictory contracts
side by side. Report external/global instruction conflicts; never silently edit
user-global files.

Dated approvals and logs remain intact. Existing active work continues on its
current installation until intentionally moved. On moving an item, capture its
still-applicable agreement and next action, with necessary user clarification.
Do not reinterpret an old approval. Preserve history and a known previous
installation for rollback, not a permanent second gate ladder in the new skill.

**Demonstrate before release:** people can operate the process without developer
infrastructure or internal terminology. Completed work has independent evidence;
unmet or unassessable mandatory outcomes are not called complete. Legacy records
remain unchanged and interrupted work is resumable. Review behavior changes and
ordinary Kerd package/release updates before installation or publication.
Kerd-development tests/CI may support that release; they are not user requirements.

## What we are not building

No new gate engine, approval schema, seal service, requirement fingerprint scheme,
mandatory risk/rigor register, hook framework, automatic CI setup or dashboard
platform. No forced final approval based on a level name. No rule that every
possible error needs an automated blocker before a person can try the experience.

Keep real validation: clear success, appropriate tests/demonstrations, source
checks, independent assessment and permission boundaries. Disclose limits of the
execution environment; address the specific operation rather than imposing a
universal infrastructure requirement.

**Next experience milestone: a real-person run through the complete candidate.**
The [current review reconciliation](consolidation.md#review-reconciliation--2026-09-08)
owns agreed adoption actions: optional assisted setup, verified authorized saves,
nested record discovery, evidence qualifications and unresolved trial gaps. These
extend the existing skills, not a new setup service, gate or installation mandate.

The session connection, bounded delivery loop and save/pickup examples are now
exercised; [the behavior pass](trials/experience-checks.md) records further
transition checks and their limits. Synthetic scenarios do not close user
comprehension or full first-use evidence. Keep that separate from broader
installed-family migration and intentional adoption.
