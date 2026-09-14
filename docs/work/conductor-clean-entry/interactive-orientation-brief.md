# Interactive orientation and task-first model selection

Implementation brief, 2026-09-14. Owner: Codex; independent review: established
Claude partner. Local changes and checks authorized, no new release or install.

## Agreement

Anthony: every ordinary Switch In must offer a Conductor session, whether or not
an agent-owned task is selected. The saved task is a jumping-off point, not a
prerequisite: Conductor can view the work and propose. Short NOW output must not
mean only one or two tasks were restored. He confirmed that exact continuation
remains critical for rolling Conductor sessions, which are not interactive.

Anthony also corrected the controller's inherited-settings default: assess the
model requirement rather than accepting the current pair. He reports this
controller is Astra/xhigh and says that is unnecessary for this work.

## Outcomes

1. Ordinary interactive In always ends on the single offer “Start a Conductor
   session?” after END. No task-specific/factual question replaces it, including
   human checks, unresolved design/product decisions or an empty active list.
   Pending questions stay represented as unresolved context. Opening guidance
   is not native-session creation, task selection, permission to build/install,
   a factual answer, or a result from the person. A plain yes enters scoped
   direction-setting; an explicit selected/authorized task can enter actual work.
2. Restore the wider current work picture, independently of the compact display:
   complete active task list including child sections, relevant current decisions,
   standing constraints and known risks. Saved read_args are navigation, not
   permission to omit other active work. Missing coverage triggers bounded local
   retrieval and an honest gap if unavailable, not an archive sweep. Keep deeper
   backlog/history discoverable, load full relevant entries when proposing from
   them, and don't create duplicate task/rules stores. Out's interactive reading
   set must support this coverage as well as the selected continuation.
3. On interactive Conductor entry, reuse that context, inspect missing relevant
   active work itself and recommend direction before asking the person to supply
   facts already recorded. A human-blocked saved task doesn't erase other work or
   authorize a substitute. Keep known authority/priority/deferred choices intact.
4. Managed To/Roll remains non-interactive: exact selected work, current approval,
   ownership and next step continue without this offer or broad reorientation.
   An ordinary interactive In with a managed owner must not take over/duplicate
   that work: its Conductor discussion can inspect the ownership issue only.
5. Task-first model/effort selection: assess requirements and suitable available
   pairs before deciding to retain current settings or inherit them for workers.
   Being capable is insufficient reason to use the highest pair. Consider scope,
   consequence, context, tools and evidence; give a reason for the chosen pair and
   for inheritance when used. Distinguish requested/reported/observed settings;
   unknown live settings don't become a compulsory survey or blanket blocker.
   Recommend a change when current settings exceed or miss the task's needs;
   do not silently change controller settings, permissions or an established
   partner. Select worker settings through supported controls. No universal cheap
   tier, unmeasured efficiency claim or compulsory effort sweep.

## Scope and proof

Update skills/switch/{SKILL.md,references/in-out.md}, relevant Conductor entry,
orchestration, job-split/prompt/model-choice guidance, and living README usage.
Correct directly contradictory living clauses/examples/anchors only. Released
What's New notes stay unchanged. No version bump, manifests, runtime Roll code,
consumer repo files, CONTEXT.md, TODO.md, session logs, bindings or global settings.
Preserve root kerd-laptop-result.patch. No commit, push, install or live dispatch.

Read CLAUDE.md and use skill-creator guidance. Keep instructions focused; no parser
framework or wording-match tests. Update documented JSON coherently and run the
renderer/example and packaging tests plus skill validation. Source tests don't
prove model compliance; report failures and limitations. Return edited files and
evidence, not a self-awarded installed-use verdict.

## Evidence supplied to implementation

Three supplied arrivals are in /Users/anthonymaley/development/dump/switchin123.
None proves its loaded version. They ended with a design vote, format preference
and human test-report request; only Weefish mentioned Conductor in THIS SESSION.
Seinn's 2026-09-14 session record reports bare Conductor asked what to do, then
read TODO only after the person told it to. Current saved set includes full Now
with Owed subsections: prior read omission vs failure to use it is not established.
Do not inspect/edit consumer repositories for this implementation.

## Assignment settings and preparation

Native implementation worker: requested gpt-5.6-terra, medium. Basis: bounded
instruction/code-adjacent editing with local tests and independent review; no
new architecture or unresolved domain research. This is not an evaluated optimum.
Prompt prepared using shared OpenAI reasoning guidance (2026-09) and GPT-5.6
profile (2026-09-05): outcome-first, method freedom, explicit proof and boundaries;
effort set on the native tool, not in prompt prose. Full native prompt retained in
native history; this is the shareable brief. Controller prepares review/fixtures
only while the worker owns the listed runtime/living files.
