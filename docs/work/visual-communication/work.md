# Visual communication by default

## Now

Owner: the Claude session holding `kerd-b5-review`, sole release owner for the
combined 0.132.0 by agreement with the Codex-side session and `codex-tui`
(2026-09-16 08:13). Stage: **Released.** Pushed as `a7daeec` on `main` with the
CI entry gate green; `195439b` closed the sitting. (This section read "at the
before-push boundary, nothing committed" until 2026-09-16 17:0x, when the next
Switch In caught the contradiction — the record was never updated after the push.)

0.132.0 combines two rules: visuals by default (this record) and the decision
capsule folded in on Anthony's authorization at 07:52-07:58. Both are behaviourally
evidenced — see the results below. 726 tests pass (Conductor 101, Agent 182,
Switch 443), `tools/gates/gate.py release` clean, versions synced in all three
locations. Codex's checkpoint and before-push reviews ran on the combined diff;
its findings are resolved.

Rulings (Anthony, 2026-09-15):
- Reply to the cadence question, about 14:46: "dont know wat that means, diagram?"
  Conductor answered with an ASCII timeline and no `kerd:visuals`.
- Relayed by another Claude session, 15:26: "its more than this also, we should be
  offering visuals as a matter of course, not heavy text only. when we show a solution
  or proposal"
- **15:31, direct: diagram-design and Archify are required for Kerd's rendered views,
  not merely allowed** ("yes required", answering "Did you mean diagram-design and
  Archify to be required for Kerd's rendered views, not just allowed?"). This
  supersedes the "complementary choices… neither tool becomes a universal Kerd
  dependency" wording in `docs/work/model-ready-work/visual-tools-assessment.md`,
  `skills/visuals/SKILL.md:71-85` and `skills/conductor/SKILL.md:270`. Reason, 15:31:
  "otherwise models wull chose to do their own thing". This sitting shows exactly that:
  the model hand-rolled ASCII when the tools were optional.

## Observed gap (this sitting)

- The standard existed but was not followed. `journey.md` says "Load the sibling Visuals
  skill when drawing"; its proactive wording ("consider whether…") is discretionary.
  Every drawing this sitting was ASCII in a code fence. There was no `kerd:visuals`
  load, no diagram-design, no rendered view: the context-aware Roll design, the route
  comparison and the review-cadence explanation.
- Install state, checked 15:31: the `diagram-design@diagram-design` plugin is installed
  in Claude. Archify is not installed: no plugin, nothing on PATH; only the 2026-09-09
  trial sample in `docs/work/model-ready-work/diagrams/`. Codex's state was not
  checked. **Superseded 21:37 — see below.**

## Archify installed, 2026-09-15 21:37

**Anthony's decision:** "i think we install ?" with the source, after Conductor
recommended shipping without it. His call taken as given.

Installed with the project's own documented command, `npx skills add tt-a1i/archify -g`,
to `~/.agents/skills/archify`, symlinked into `~/.claude/skills/`. This is user-global,
outside the Kerd repo. Its skill registered in-session immediately.

Verified rather than assumed:
- `archify doctor` passes 15/15 - renderers, schemas and examples for all five types,
  live preview, visual-check and compare runtimes. "Archify is ready."
- Node v26.7.0 against its declared `engines: >=18`. The `^22.19.0 || >=24.0.0` in the
  repo README belongs to a DeepSeek Harness integration, not the skill itself.
- **Zero runtime dependencies.** `ajv`, `parse5`, `saxes` and `simple-icons` are
  devDependencies and no `node_modules` is installed, which substantially limits the
  supply-chain surface the installer's "2 Socket alerts" could reach.

Not verified: what those two Socket alerts actually are. The installer printed the count
and a details URL (`skills.sh/tt-a1i/archify`) that does not carry the audit data; I did
not find them. Recorded as unknown, not as cleared. Snyk on the same screen said
Low Risk and Gen said Safe.

Still true from the 2026-09-09 assessment, and the reason static work stays with
diagram-design: it remains a dev snapshot (`2.17.0-dev.1`, no stable release a month
on), its sample rendered node text too small to read at 390px, and its explorer
controls distract from a simple "is this what you want?" moment. Archify earns the
exploration branch, not the default one.

## Proposed correction (not agreed; from two read-only peer replies, revised)

- **Explicit request:** every skill entry point invokes `kerd:visuals` when the person
  asks to see something, and the answer is a saved, rendered view.
- **Proactive default:** a substantial Shape or Agree presentation with several
  connected parts, a branch, an ownership boundary or a before → after change carries
  a rendered view of the solution itself. There is no offer question such as "Would
  you like a diagram?" and no quota. Tiny or factual proposals stay text-only.
- **Required tools (15:31; both installed as of 21:37):** Visuals renders through diagram-design
  (static layouts: processes, timelines, responsibilities, scope, comparisons) or
  Archify (exploration, focused paths, comparing changes), not the bundled starter
  patterns alone. Archify's install was approved and completed at 21:37. Codex availability is
  still to be resolved.
- **Guard:** a static test covering the rule anchors in all 12 entry points,
  Conductor and journey.md, Visuals' trigger description, the required-tool wording,
  and a ban on offer phrases. Mutation-checked.
- **Behavioural tests:** real-model, three runs each. T1 explicit request, T2 proactive
  proposal, T3 proportional control, T4 request outside Conductor. Evidence is limited
  to the run's own ordered stream blocks, a bounded slice of its output, and files it
  wrote. The full test design is in the Claude session's peer reply (request
  `ebc1e3b3`, retained privately); carry it into the score.


## Scope view

`scope.html` in this folder renders the three routing paths, the tool branch and the
two deliverables. Drawn with diagram-design under the Krutho profile; geometry verifier
and self-check both clean. It is the agreement aid for this release, kept current with
the decisions above.


## Built, 2026-09-15 21:45 - 22:05 (target 0.132.0)

Scope agreed by Anthony at 21:45 ("y"). Three players, all Opus 5 via
`kerd:effort-high`, all observed as `claude-opus-5`/`high` with no evidence gaps.
Change reads against `vc-s1`, `vc-s2`, `vc-s3`: each touched only its owned paths, HEAD
unmoved, nothing unexpected beyond a git-ignored `.pyc`.

- **S1** - the shared `**Showing the person:**` line in ten entry points, and the new
  guard `skills/conductor/scripts/tests/test_visual_default.py`.
- **S2** - `journey.md` `## Visuals belong throughout` and Conductor's
  `## Show the direction`.
- **S3** - `skills/visuals/SKILL.md` whole, and the supersession marking on
  `docs/work/model-ready-work/visual-tools-assessment.md`.

**The loophole was not one sentence.** `journey.md`'s "Use a small inline sketch for a
simple relationship" was the known one. Codex's checkpoint review then found the same
licence still live at `skills/visuals/SKILL.md:22` - "A small inline relationship can be
enough" - in the skill whose whole job is rendering views; Conductor's brief had named
sections rather than asking for a sweep, and that miss was Conductor's. Sweeps by S2 and
S3 then found four more of the same class, every one of them a sentence carrying no test
a model could fail:

- "Small explicit work uses a visual only if it clarifies a real relationship"
- "Show meaningful visuals whenever they help understanding"
- "Add a relevant sketch or comparison when it helps"
- "An early before/after **sketch**" - the word itself, in the sentence introducing the
  artefact a before → after change now requires.

**"Substantial" was the deeper defect.** Codex, finding 3: a model can call a multi-part
proposal small because it is easy to *describe*, and comply while shipping a wall of
text. The boundary is now countable - two or more connected parts, a branch, an
ownership boundary or a before → after change - with only a single action or a factual
answer staying text, and an explicit clause that being easy to describe in words does
not make something a single action.

## Question-context addition, 2026-09-16

Anthony supplied a real Work-Anthony exchange in which a long account ended on
“Does the Apple measurement run?” and then explained the failure directly: the
question was detached from the facts needed to answer it, so he had to search
back through the message. He asked to model the corrected form into the next
release, then ruled “or we can add to 132 and go”. This is part of 0.132.0, not a
separate release.

The corrected form keeps a compact, answer-ready capsule immediately above every
consequential bubble: recommended concrete action; what it decides or changes;
material cost or risk; and the stopping or authority boundary, only where each
applies. No unrelated account, Insight, history, follow-on or document list sits
between the capsule and the bubble. The bubble names the concrete action and
target rather than “it”, “that”, or an abstract label such as “the measurement”.
Longer provenance stays earlier or behind links. Tiny and factual questions stay
proportionate.

Ordinary Switch In is explicitly exempt. Its complete rendered dashboard is the
orientation, its question is fixed, and its labelled Yes opens direction-setting
only; adding a second capsule after the renderer would violate the unchanged-output
contract without improving the decision. Managed and task-specific questions are
not exempt merely because they come from Switch.

A Terra/medium player wrote the shared rule in all twelve entry points, the
linked journey contract and the static guard. The controller read the returned
diff against the combined uncommitted 0.132.0 tree. Focused verification: seven
question-form tests and `git diff --check` pass. Two isolated mutations — changing
one shared entry rule and weakening the no-intervening-content bound — were caught.
Those readings cover the capsule slice only; the earlier 0.132.0 readings cover
the visual slice only. The combined tree is re-verified below before release.

**Guard:** 31 mutations across both rounds, each reverted with sha256 re-checked, run
against a scratch copy of `skills/` because several targets were owned by concurrent
writers (the real files were proven byte-identical to a pristine snapshot). Two are
deliberately must-PASS: a mid-sentence rewrap of the shared line, and a sentence that
forbids the offer while discussing how the tools relate - which tripped three bans under
the old fragment list and now passes. That is 0.131.0's `"no native picker"` defect
demonstrated as fixed rather than asserted.

**Deliberately left:** Conductor's "For a substantial package, alongside the view give a
short direction summary" - that "substantial" gates the direction summary, not the
visual. `skills/visuals/SKILL.md`'s last unrendered route - if neither required tool can
run, say plainly that the view is not rendered and what it costs, rather than
substituting a hand-drawn picture - kept as a gated, disclosed exit. Making it an error
would have Kerd refuse to answer at all on a host missing both tools, which is worse
than answering with a stated cost.

## The open risk at 21:57 (historical; measurement follows)

**At that point, the behavioural tests T1-T4 were designed and unrun.** This release changes prose and
guards prose; nothing yet shows the prose changes model behaviour, and "a rule that
reads well and does not land" is the exact failure that produced the release - the old
rule read fine and every diagram still came out as ASCII. Codex made this its finding 2
independently of Conductor raising it.

A pre-release run must point a worker at the working tree rather than the installed
plugin, because the plugin cache does not yet carry 0.131.0; that tests the wording, not
the shipped path. Estimated 12 runs at roughly $1.50-4, stated as a guess, not a
reading. Put to Anthony at 21:57; his decision is recorded wherever it lands, and if the
runs are declined the record says the release shipped over a reviewer's high finding
rather than that the matter was settled.


## T2 round 1 - WITHDRAWN, THE RESULT WAS A MEASUREMENT ERROR

**Correction, 23:34.** Everything in this section's original conclusion was wrong,
and wrong in the direction that made the release look broken. Both treatment runs
recorded as "no view produced" had in fact produced one: t2c finished after 26
minutes and t2a after 37. Conductor sampled the disk at 23:05, while both were
still working, and reported that snapshot as the result. The completed controlled
set was sixteen runs: **treatment 8/8, control 8/8 — no detectable difference.**

**What those figures do and do not establish.** Both arms saturating at 100% means
the experiment could not discriminate: the scenario chosen was so obviously
diagram-shaped that the old discretionary wording fired exactly as often as the new
countable threshold. It is evidence the new rule does not *regress* behaviour. It is
**not** evidence the rule works, and it must never be cited as such. The
discriminating test is a **marginal** scenario - two connected parts and a small
branch, where "consider whether seeing the relationship would help" plausibly
resolves to no and "two or more connected parts" resolves to yes. That test is
designed and unrun.

**T1 is also unrun.** The T1 pilot (2026-09-16, fresh Sonnet 5 at medium, working-tree
plugin) returned **INVALID - no evidence**: the worker's Bash inspection was denied
and it exhausted its $0.30 budget at 5 turns before producing a final answer or any
artifact. `terminal_reason: budget_exhausted`, `is_error: true`, $0.3425866 spent. It
identifies a harness, permission and budget defect only, and enters neither T1's
numerator nor its denominator.

**What the behavioural tests establish.** Nineteen valid runs on 2026-09-16, plus
one invalid pilot recorded as invalid. The discriminating test used three arms isolating
each rule: *full* (both rules), *visual* (the 23:14 snapshot, visual rule only) and
*base* (HEAD, neither), with byte-identical prompts and scoring criteria fixed in writing
before the last runs reported.

| Test | Result |
| --- | --- |
| Marginal case, three arms | full **3/3** · visual **3/3** · base **0/3** |
| T1, explicit request | **2/2** rendered |
| T3, one-line factual question | **0/3** rendered — no over-fire |
| T4, outside Conductor (Tend, Slainte) | **2/2** rendered |

The visual rule is **demonstrated**: it fires on a marginal case that the wording it
replaces declines, it does not fire on factual questions, and it works from entry points
other than Conductor. The base arm did not fall back to ASCII either — it answered in
prose, which is correct for the discretionary wording it had.

The capsule rule is **not demonstrated**: 1/3 clean capsules in the full arm against 0/3
in the visual arm, with partial behaviour in both. Models already place some
decision-relevant context near a question unprompted, so the rule must beat that baseline
and has not been shown to. A separate measure — whether the bubble names a concrete
target — saturated at 9/9 across all three arms including base, and must not be cited as
evidence for the rule.

**Limits, stated rather than buried:** one marginal scenario in one domain; n=3 per arm;
the capsule and concreteness measures are Conductor's judgment, and Conductor is the party
with an interest in the release passing; workers read corpora from scratch paths rather
than an installed plugin.

**Capsule rule: tightened, re-tested, demonstrated (2026-09-16 13:33-13:58).** Anthony:
"Tighten and re-test. Keep 0.132.0 combined... If it still cannot beat the visual-only
baseline, split it to 0.133.0."

*Diagnosis.* The five partial failures failed identically: models gave the recommendation
early, continued with detail, then asked - so the block above the bubble held the deciding
consideration but not the recommended action. One run wrote "the three steps above",
sending the reader upward explicitly. The rule said "put the minimum facts needed", and
"minimum" read as licence to omit what had already been said. Nothing told them to repeat.

*Tightening.* The capsule is now self-contained: "Restate the recommendation there even
when it already appears earlier; the repetition costs less than the reader's search. Never
point upward with 'the steps above' or 'as described'." `journey.md` names the observed
failure directly - a capsule carrying only the deciding consideration while the
recommendation sits paragraphs above has failed the rule.

*Re-test.* Two arms, same marginal scenario, n=4 each, scored against the criteria fixed
at 11:45.

| Arm | Clean capsules |
| --- | --- |
| Tightened wording | **4/4** |
| Visual-only baseline | **0/4** (4/4 partial) |

Against 1/3 before the tightening. The capsule rule is **demonstrated** and stays in
0.132.0. Limits unchanged: one scenario, n=4 per arm, and the capsule measure is the
release owner's own judgment, recorded as PARTIAL wherever borderline.

**Superseded by the results immediately above; the historical conclusion follows.** The
visual rule has a non-discriminating null; the capsule rule has nothing at all. Both
are guarded statically, and a static guard proves the rule is *written*, never that it
is *followed* - which is precisely the failure that produced this release, since the
old rule was written correctly too.

There were no phantom
references; both files existed, just not yet. The "phantom view" failure mode was
an artifact of the measurement, not a behaviour of the rule. Round 2, with the
corpus confound removed, is the reading that counts. The original section follows
unchanged, as the record of what was claimed and why it was wrong.

## T2 interim result, 2026-09-15 23:05 — withdrawn, see the correction above

Anthony, 22:55: "Run T1-T4 before pushing. Model behavior is the release's central claim;
shipping without testing it would leave the exact failure 0.132.0 exists to fix
unproven." T2 ran first, because a null there answers the release without spending on
T1/T3/T4.

**Design.** Six fresh workers, byte-identical prompts, differing only in which corpus
they were told to follow. Treatment: the working tree. Control: `git archive HEAD`, the
same skills minus exactly this release. The scenario never mentioned diagrams, drawing
or seeing anything - a plain "what do you recommend?" about notification delivery with
six connected parts and a branch, qualifying under the new countable threshold and not
under the old discretionary one. A control was added beyond the 12 runs Anthony approved
because without it a rendering treatment arm proves nothing: the model might draw anyway
from disposition, from `diagram-design` sitting in its tool list, or from memory bleed.
Evidence is files on disk, not self-report.

**Result.**

| Arm | Rendered a view |
| --- | --- |
| Treatment (new rule, 12 entry lines) | **1 of 3** (t2b only) |
| Control (HEAD, old discretionary wording) | **3 of 3** |

The new wording did not improve rendering. In this sample it coincided with worse
rendering, and the arm that rendered every time is the one this release replaces.

**The failure mode is worse than not drawing.** Both non-rendering treatment runs wrote
a reference to a view they never produced:

- t2a: ``View: `notification-routing.html` (proposed, not agreed)``
- t2c: ``  `notification-delivery.html` - the rendered pipeline view (diagram-design,
  drawn by...)``

Neither file exists. Zero box-drawing glyphs or code fences in either: they did not fall
back to ASCII, they fell back to a *claim*. That is strictly worse than the behaviour
this release set out to fix - ASCII is visibly bad, a phantom reference reads as
compliance. The failure appeared only in the treatment arm.

**Held as hypothesis, not finding:** that the new rule *causes* phantom views. Three runs
per arm is small and the difference could be noise. There is also a real confound - the
treatment workers read the live repo path while control workers read a scratch copy, so
surrounding context was not identical. What is not in doubt is that the release's central
claim is unsupported.

**Every static check passed on a rule that does not work:** 32 mutations, three Codex
review rounds and six findings resolved, 725 tests, gate clean. The behavioural run
Anthony insisted on is the only thing that caught it. Conductor would have shipped this.

**Recommendation, 23:05: do not ship 0.132.0.** Diagnose before re-wording. Proposed next
step is a higher-n T2 with the corpus confound removed - same path shape for both arms -
to establish whether the phantom effect is real before a single sentence changes. Put to
Anthony; awaiting his answer.
