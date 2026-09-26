# TODO

## Now

**Release boundary:** 0.161.0 on `main`; Claude Code runs it (applies on restart); Codex on 0.160.0,
needs 0.161.0 (Visuals changed; his go in its window). Position is in `CONTEXT.md` `## Where We Are`.

- **After any diagram-design update, reload the Kerd profile** (Anthony 2026-09-26 09:54: his other
  projects use the Kerd look too). Updates replace the installed `style-guide.md` with the default;
  a project without a `.diagram-design` marker then draws in orange.
- **Bring Codex to 0.161.0:** its window, his go; read back the installed version.
- **Watch the question shape (0.159.0) and the diagram heading and states (0.161.0) in real use.**
  Repeatable checks: `evals/question-shape/` (per `CONTRIBUTING.md`) and `evals/visuals-owner-cost/`
  (scripted `claude -p`, README there).

- **Watch the outside-the-repo list (0.158.0):** the first Switch Out that adds or prunes a line in
  `notes:outside-the-repo.md`, and a Switch In that reads it. Seeded with two lines; unseen live.
- **Watch the private vault notes (0.157.0) in real use:** the first Switch In that reads a
  `notes:` sketchbook pinned by `--notes-commit`, and a pickup on a second machine. Unseen.
- **Watch the push-first trigger (0.156.0):** "just push it" / "skip the review" on Conductor
  work should now load Conductor; evidence (4 runs) showed it did not before; unseen live.
- **Watch the report's second line and the finish (0.156.0):** "where the work stands" was missing
  in 10 of 10 evidence reports before the change. Evidence: `notes:unattended-sweep/evidence/`.

**The launch plan is accepted** (Anthony, 2026-09-22 09:38): `docs/design/launch-plan.md`,
sketchbook `notes:launch-plan/work.md`. Kerd is ready to launch when someone other than
Anthony carries real work in their own repository to its agreed result, unaided. **Step 1: 3of3
is using Kerd in its own sessions; Kerd evidence is read from those sittings when Anthony asks for
it.** 3of3's own work is not Kerd's open work (Anthony, 2026-09-25 10:49: "we are mixing work").
Evidence so far: `notes:launch-plan/work.md`.

**The team note is going out** (Anthony, 2026-09-23 17:05, "y" to sending it now; not yet
confirmed sent). **Parked:** "delay any sam and auble work for now" (Anthony, 2026-09-24
08:55); don't ask about it until he picks it up. Each team's reply goes into its lines under "The team note goes out" in
`notes:launch-plan/work.md`, one per field of the plan's per-person record.

**The 2026-09-13 hold is lifted** (Anthony, 2026-09-23 18:19; `docs/decisions.md`), so
**launch step 2 (inviting three to five people) is dropped** (Anthony, 2026-09-25 11:16: "i dont.
drop this"; don't raise it again). **Anthony's:** where and when to announce. GitHub's README rendering, checked 2026-09-22: all four pictures
load and the smallest label shows at 16.8px; the repo homepage already links the site. The
repo's GitHub description now matches the site's line (set 2026-09-22 on Anthony's "sure"). Leftovers from the
2026-09-21 image test, both harmless and left because they are his: an idle Codex session in
tmux `codexprobe`, and a trust entry for `/private/tmp/codex-img-probe.kykwaJ` in
`~/.codex/config.toml`.


- **A session should never sit idle with nothing asked** — shipped in 0.146.0; on 2026-09-24 it
  did not hold (ten status prompts across four sessions). 0.153.1 names the two missing endings
  and his global CLAUDE.md now carries a turn-end gate; watch whether he still has to ask.
  Both hosts run 0.153.1 (Codex read back 17:29). Sketchbooks: `notes:no-idle-sessions/work.md`,
  and the superseded monitor framing in `notes:waiting-on-you/work.md`.
- **The report shape and the finish: changed in 0.145.0, watch them in use.** A
  correction of Kerd's own earlier claim now rides in the opening lines and never
  competes for the five items; a finish names the next item instead of ending on "no
  action needed". Both came from repeated real instances, four of them on 2026-09-22.


- **Watch the unanswered-review rule (0.149.0)** the first time a partner doesn't answer:
  a fresh reviewer recommended on his yes, never a waiver. Record:
  `notes:partner-closed/work.md`.
- **The Opus 5.5 profile was revised in 0.152.0 against Anthropic's guide;** two clauses
  carry one paired observation each, three new clauses are pending (unattended premature stop,
  fan-out time budget, explore before acting). Watch the first real brief that uses them.
  Sketchbook `notes:opus-55/work.md`. The GPT-6 profile (0.148.0) is untested.
- **Watch the context reading (0.153.0) in its first live session:** a `Context: N tokens in
  the last request` line at each prompt and during long turns, matching the status line. Seen
  once by hand before release (170,532 tokens vs "83%" free, 2026-09-24 15:34). First live delivery
  17:39: a fresh headless session got the line on its second prompt (35,110 tokens). Silent at
  a session's first prompt by design (no reply to count yet); wording fixed in 0.153.2. Since
  0.154.0 it also records the host's permission mode for the chat roll. **First seen in an
  interactive session on 2026-09-25 (0.154.1):** the line arrived at every prompt from the second
  (91,889 at 08:58 up to 115,948 at 09:42) and after tool calls mid-turn. One session, not verified.
- **The homepage redesign: dropped, to revisit** (Anthony, 2026-09-24 12:56). Three Codex
  passes and his reactions: `notes:homepage-redesign/work.md`.
- **Rolling without publishing: built in 0.144.0, not yet seen in a real concert.** A
  concert now performs on `concert/<work>`, and the merge back is the person's go
  (Anthony agreed the design 2026-09-22 11:53). Watch the first real concert that rolls.


- **Watch the chat roll (0.154.0–0.154.1) in a real Conductor build.** Two test rolls worked on
  2026-09-25 (pane restarted, same model/effort/mode, next step done); a concert rolling itself at
  50% is unseen, and so is a roll from a process shown as capital `Claude` (unit-tested). The
  three-in-a-row limit counts every roll in a checkout within six hours; see whether it bites.
  Sketchbook `notes:rolling-session/work.md`.
- **Observe the composer and managed Conductor in a real session.** Worker Roll's
  context-triggered handover to a second run is still unseen (the trigger fired twice; each job
  finished first). The composer and managed Conductor are still unexercised. Fan-out has now run four times (twenty dispatches, then four, then two, then
  two plus one).
- **Observe the arrival's "Something else" route** and the closing box over several
  sittings. The arrival and "Yes" were seen again on 2026-09-20 14:35.

- **0.134.0's two clauses, first measured 2026-09-25 on the 16 work diagrams saved since
  2026-09-20** (text read from each render): 15 of 16 name their project inside the picture;
  `codex-players/availability.html` names only Agent and Conductor. Code references are light
  and subordinate everywhere: 0 in 12 diagrams, 1 to 3 labels in four, all in captions or
  evidence lines. Not measured: whether proposal and correction views show what works today,
  what doesn't, who owns the gap, what changes and its cost; that needs a reading, not a count.
- **Unverified for 0.132.0:** whether either rule holds beyond the one marginal scenario.
- **Archify's two Socket alerts, identified 2026-09-25 09:4x** (skills.sh Socket audit, dated
  2026-09-23; the 2026-09-15 installer's alerts are presumed the same two, not proven): (1) LOW
  "anomaly", `bin/visual-check.mjs` runs headless Chrome, `--no-sandbox` only as root or with
  `ARCHIFY_CHROME_NO_SANDBOX=1`; here uid 501, variable unset, so the sandbox stays on. (2) HIGH
  "malware", `test/fixtures/fail-migration-cleanup.mjs`: a test fixture that fakes one EPERM
  on cleanup, loaded only by `test/workflow-migration.test.mjs`; read in full, a fault injection,
  not malware. Neither runs when drawing diagrams. Still a dev snapshot `2.17.0-dev.1`.
- **The `codex-plugin` behavioural scenario, first run with a model 2026-09-25 09:4x** (one fresh
  headless Opus Switch In on a scratch shop repo whose notes say a preview was seen, whose
  checklist says not, with a log reconstructed from memory and an unapproved design): it put the
  contradiction in ATTENTION, called the reconstructed log not evidence, kept the design
  unapproved, recommended the independent approved fix, asked only "Start a Conductor
  session?" and changed nothing. Reply half, same session, answered "not sure - I think I
  glanced at the preview but I can't say I really reviewed it": it opened Conductor at
  Understand (right for "not sure"), kept the design unapproved, started no work and asked one
  question. **But it settled the doubt:** it wrote "the preview has not been reviewed" into
  the record and called the "owner saw the preview" note wrong, though glancing fits that note;
  the scenario says Not sure leaves it unresolved. My reply mixed "not sure" with a fact, so
  one ambiguous run. **Clean rerun 09:59** (fresh session, fresh copy, reply just "not sure"):
  same arrival; Conductor opened at Understand, changed no file, left the preview's status as the
  records have it, approved nothing, asked one question. So the earlier write followed the fact I
  added, which the rules allow recording. Two runs pass on "not sure"; not verified, no wording
  change indicated.
  The scenario's "one factual question" is superseded by the arrival's single question.
- **Watch the first cross-provider build exception (0.151.0).** Conductor builds with its
  own host's workers; a Codex builder under Claude (or the reverse) is an exception the
  person asks for or approves, called a trial without a comparison. Not yet seen: the
  first request and its Fit line. Sketchbook `notes:codex-players/work.md`.
  Codex building the homepage on 2026-09-24 was Anthony giving it the work directly, not a
  Conductor dispatch.
- **Roll at ~200k by hand, then compare (Anthony, 2026-09-25 10:26).** The Studio status line
  now shows tokens used and a coloured state (green keep working, yellow switch at a break from
  200k or 60% used, red switch now from 80%); he rolls by hand at a break. After a few
  sittings, compare average tokens re-sent per call, rolled vs not, and decide whether Kerd's
  chat roll moves from 50% to 200k. The built alternative was dropped as too complex. Sketchbook
  `notes:rolling-session/threshold.md`.
  **Latent, parked (Anthony, 2026-09-25 20:08):** the no-progress check never fires, because
  every save rewrites the sketchbook (`tmux_roll.py:368`), so only the three-in-6h count stops a
  loop. No roll has ever been refused: on 2026-09-25 the cap *would* have refused one before
  ~18:51, but the ~1M window never needed it. The thrash guard was dropped at 10:26 as too
  complex; revisit only if a real roll is refused or the 200k trial decides the trigger.
  **Trial so far (2026-09-25, `measure.py`):** kept near the mark, avg re-sent per call 145k and
  133k; ran past it, 221k (the 0.155–0.157 sitting, peak 378k, not rolled by hand) and 247k.
  Two against two, not verified; rolling by hand did not hold in a busy sitting.
- **Bring Codex along with each release** that changes its four-skill package (Conductor,
  Switch, Visuals, Agent); Codex builds and installs only on Anthony's go in its window.

Records: the 2026-09-20/21 sitting's sketchbooks are at `docs/work/front-page-claims/` (the
front-page check, the site going live, and the evening's six contradictions and host line) and
`docs/work/partner-images/` (0.143.0). The Jev trial is closed as not worth a place now;
`docs/work/jev-trial/work.md` keeps the results, the untested hook idea and three other-project
candidates. Rows closed
on 2026-09-21 are in `docs/backlog-archive.md`. The diagram theme is this machine's setup,
not Kerd work: recorded in `docs/decisions.md`. These lists are not authority to install or
run checks during pickup.

## Backlog

- skriv voice profile wiring — needs non-founder-genre samples.
