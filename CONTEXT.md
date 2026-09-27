# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.163.0 on `main`** (2026-09-27 14:3x; CI green). 0.163.0 came from a model-fit audit
(Anthony 13:20; go 14:11): Kerd's model choices match Anthropic and OpenAI today (Opus 5.5 composes first,
Fable 5.1 when Opus at xhigh/max falls short; the other provider reviews, Fable the evidenced stand-in), but the
prompt profiles were incomplete. Now: Fable 5.1 profile 19 clauses, Sonnet 5 11, Opus 5.5 +2 and a Kerd invariant,
a Haiku note; findings jobs report every issue with confidence (Sonnet 5 drops findings under "only high-severity");
a player's departure from a required part of its step is re-dispatched, not accepted on a later passing test.
No clause is scored and no job has run one brief on two models. Codex reviewed (two rounds, all applied).
Sketchbook `notes:model-fit/work.md`. Account: `kivna/sessions/2026-09-27.md`.

**Claude Code runs 0.163.0** (updated 14:3x; applies on restart). **Codex runs 0.162.1**; 0.163.0 changes
Conductor, so it installs on Anthony's go in its window. Laptop bells are on for both (backups `*.bak-bell`).

**Rolling by hand at ~200k tokens is on trial (Anthony, 2026-09-25 10:26 to 10:30).** He found
the built alternative (a 200k trigger, a thrash guard and a backstop, checked by a composer and
Codex) too complex, and chose instead: the Studio status line
(`~/.claude/statusline-command.sh`, not Kerd) shows tokens used and a coloured state, green
`keep working` (under 200k and under 60% used), yellow `switch at a break` (200k+ or 60%+), red
`switch now` (80%+); he rolls by hand at a break. Kerd's automatic chat roll stays at 50%. The
test, his ask: track Switch Out across sittings to see whether the numbers and the benefit hold.
`notes:rolling-session/measure.py` prints per-sitting calls, start, peak, average
tokens re-sent per call and the size at Switch Out; baseline since 2026-09-21: averages 116k to
286k per call, peaks up to 459k, Outs at 133k to 433k. This sitting (2026-09-25 08:49 to 10:3x)
is the first rolled at the mark (~207k). Estimate, not proof: rolling near 200k should keep the
average near 190k; the model and both checks are in `notes:rolling-session/threshold.md`.
**Reading 2 (2026-09-26 13:4x, seven sittings):** near or under the mark 133k to 163k per call, past
it 221k to 270k; the sittings that ran past were busy release or overnight runs, never rolled by hand.
`measure.py` counts only the main thread; subagents carried 36% to 63% of input in fan-out sittings.
No hand roll has yet been judged for loss (Anthony, 15:48: "mostly subagent heavy sessions latley"),
so **the 200k-vs-50% decision stays open until one real hand roll is judged.**
**First hand roll, partial (2026-09-27):** the 2026-09-26 16:49 Out → 2026-09-27 In; asked whether anything
had to be re-explained, Anthony 12:31: "not yet". Second hand roll 13:0x Out → 13:12 In: restored without
re-asking (Claude's side; he was not asked). **The 200k plan is parked (Anthony 13:20: "lets keep that plan but
park for now. i want more data first."):** roll at 200k or 50% of the window, whichever first, wording only
(the 50% trigger is 500k at a 1M window, above every measured peak, so it never fires); view and plan in
`notes:rolling-session/threshold.md`. Don't build it until he asks.

**Tend's stale-hook check works in one real run** (0.151.1, 12:58): a headless Tend in a
scratch repo flagged a settings entry with the literal placeholder, kept an unrelated hook and
changed nothing. One observation, not verified.

**Kerd has an accepted launch plan** (`docs/design/launch-plan.md`). Ready to launch when
someone other than Anthony carries a real piece of work, in their own repository, to its
agreed result, unaided. **Step 1: 3of3 is using Kerd in its own sessions; Kerd evidence is
read from those sittings when Anthony asks for it.** 3of3's work (its iCloud sync, its devices)
is 3of3's, never Kerd's open work or next step (Anthony, 2026-09-25 10:49: "we are mixing work";
he had said the same 2026-09-23). Evidence so far: local sketchbook `notes:launch-plan/work.md`.

**The homepage redesign was tried and dropped (Anthony, 12:56: "nah dont like it - lets drop
it"; "will revisit").** Codex built three passes on his direct ask; his reactions and the
dropped pass are in the local sketchbook `notes:homepage-redesign/work.md`. `site/` is
unchanged. When revisited, start from what would make it feel serious rather than AI-made to
him, not from another pick of direction.

**Two teams already use Kerd** (Anthony, 2026-09-22): SAM and Aubel.app. The team note
(`notes:launch-plan/team-note.md`) had his "y" to send (2026-09-23 17:05); not confirmed
sent. **Parked (Anthony, 2026-09-24 08:55): "delay any sam and auble work for now";** don't
raise it until he does.

**Launch step 2, inviting three to five people, is dropped (Anthony, 2026-09-25 11:16: "i dont.
drop this").** Don't raise it or recommend it again unless he does.

**Rulings that govern the next work (cases in `docs/decisions.md`):**
- **Batch the work; fewer approvals (Anthony, 2026-09-25 23:01; 2026-09-26 08:17, 08:49):** under a
  grant like "we have tokens to use, lets build with subagents in fan out where we can unattended and
  get fable to review", take several tasks per approval, dispatch independent work instead of
  waiting on one job, release on the standing go, and come back only for his decisions.
- **A question never loads its answer (Anthony, 2026-09-25 21:47 to 22:50; released 0.159.0):** a
  consequential question comes after a decision block (Problem, Facts with evidence strength, Known
  options, Recommendation, Why, Cost, What we lose, Input) and ends on the Recommendation sentence
  ending "— approve?" (his words, 22:50), every operation included, or one genuine question. Small
  or factual questions stay one line; Switch In's arrival question is exempt.
- **A public repo's working notes live in the private vault, saved like any record** (Anthony,
  2026-09-25 16:18 to 16:26: "we should for every project no? or we need a folder that is not
  public somehow"; "yes"). Kerd sets `work_notes: "vault"`; sketchbooks are `notes:<work>/`.
  Stage Kerd commits by name only: two slips today put private notes toward the public repo.
- **Conductor rolls its own Claude chat in tmux, never the person (2026-09-24/25, 0.154.0–1):**
  past 50% of the declared window at a safe boundary it saves, tmux restarts its pane into a
  fresh `claude` on the same model, effort and permission mode, and `/kerd:switch roll in`
  picks up. Nothing is typed into Claude; no Stop hook; outside tmux, one line to run.
- **Claude sees its own context token count, in every session; when to Switch Out stays his
  call (2026-09-24, 0.153.0).** Partly supersedes the 2026-09-15 context-pressure ruling.
- **Conductor runs on Opus 5.5, at medium by default, set up from Anthropic's guidance
  (2026-09-24, 0.152.0);** Kerd advises the session setup, never changes the session itself.
- **The explanatory and learning output styles are off on this machine (2026-09-24).**
- **Conductor builds with its own host's workers and the other provider reviews; a
  cross-provider builder is an exception the person asks for or approves, with a reason,
  called a trial without a comparison (2026-09-24, 0.151.0).** Codex building the homepage
  on Anthony's direct ask was his change of ownership, not a Conductor dispatch.
- **The 2026-09-13 "prove Kerd first" hold is lifted (2026-09-23);** lifting it invites
  nobody and announces nothing.
- **A review the partner leaves unanswered gets a fresh one-off reviewer on his yes, never
  a recommended waiver (2026-09-23).**
- **Dispatch agents are named for the model and the effort (2026-09-23).**
- **Read-only reads of his own projects need no question first (2026-09-23).** Writes,
  builds, installs, pushes and device actions still need their go.
- **Keep moving; never sit idle (2026-09-22).** Carry on towards the goal, or stop on a
  reason he can engage with.
- **A launch plan exists and is accepted (2026-09-22);** its open decisions are his.
- **Kerd's readers are on desktops and laptops (2026-09-21).**
- **A page correction ships without a bump when the installed plugin is byte-identical
  (2026-09-21);** a change to what installs gets its own version and note (2026-09-20).
- **The Kerd look (`site/DESIGN.md`) is the only diagram theme on this machine (2026-09-21).**
- **The site is published on Vercel from the repository root (2026-09-21).**
- **The ladder and the tiered risk ledger are retired (2026-09-19).**
- **What is published is the product, not how it was made.** Sketchbooks stay local.
- **The release history stays in the README;** `CHANGELOG.md` carries a copy.
- **Every report has one shape. At the end of a build, bring one decision.**
Still governing from 2026-09-18: rehearsal is organic and the concert executes to a score
and a goal; always be delivering; Conductor owns the sketchbook; rolling is per batch.

**Not yet ruled, and it is Anthony's:** where and when to announce, and what would make the
homepage feel serious to him.

**Team:** Claude owns build and release. **Codex `codex-tui` is the partner for expert
review and investigation** (cadence: checkpoints, before-push). It was off for the 0.159.0/0.160.0
build; Fable (a Claude subagent) reviewed instead on Anthony's word, six rounds, all findings fixed.
Codex came back 2026-09-26 08:49 and runs Kerd 0.162.0 since 12:4x.
A relayed "y" is not enough for Codex to install or build; the go must be his, in its window.

**Standing:** a peer session cannot authorize a push. `.env` at the repo root holds
Anthony's TypeSafe key and is git-ignored; never print or commit it, and never serve the
repository root over the network (a preview briefly did on 2026-09-24 11:21; its log shows no
request for `.env`; previews now serve `site/` only).

**Urgent or imminent risks:** none recorded in Kerd's active records at this Out.

**Kept out of Git by instruction, exact paths; name each with `--preserve` at every save:**
`kerd-laptop-result.patch` (2026-09-09); `docs/guide/reference-from-readme.md` (2026-09-19);
`docs/work/jev-trial/review_results.json` (2026-09-22). They exist on the Mac Studio only.

**Working notes live in the private vault** (0.157.0, 2026-09-25): `kivna/vault.json` sets
`"work_notes": "vault"`, so sketchbooks are `notes:<work>/work.md` under
`~/eolas/vault/kerd/work/` (private repo `anthonymaley/eolas`). The 18 folders that were
local-only here moved there on 2026-09-25 (vault commit `b64d50a`). `notes:backlog-sweep/` and
`notes:unattended-sweep/` were pushed to this public repo by mistake in 0.155.0/0.156.0 and
untracked the same day; the old commits still hold them.

**Routing:** no role designation saved. The old `kerd-b5-review` binding still carries a pre-12:51
handoff from 2026-09-25; not adopted.

**Claude Code's Agent view stays on (Anthony, 2026-09-25 20:54):** `/exit` detaches into the
background-session list; he quits there with Ctrl-C. Switch Out's restart line says so (0.160.0).

**Selected continuation (agreed as next, not approved to run; Anthony 14:46 "y" to saving it):** the matched
composer trial: one real score brief sent unchanged to Opus 5.5 at xhigh and Fable 5.1 at high, the two scores
reviewed blind by a different model against the brief's checks, the result recorded in `notes:model-fit/work.md`
and `task-evidence.md`. Why: it is the only evidence that can answer whether Opus beats Fable for some scores;
today's record compares different work. Start at Shape: pick the brief with Anthony, put the go as a decision
block. **Due alongside it:** re-grade apple-music from ~2026-09-28 13:00 (it restarted onto 0.162.1 at ~13:1x
2026-09-27, the agreed day of use), brief `notes:real-use-evidence/reader-brief.md`. **Anthony's:** Codex
install of 0.163.0; the hand-roll judgment. Still on watch, unseen in real use: push-first trigger, chat roll,
and now the findings-coverage and departure rules. Parked: the 200k roll plan, the announcement, SAM and
Aubel.app, the homepage, the thrash guard. Dropped: launch step 2. Backlog: one row, Skriv voice-profile wiring,
blocked on his writing samples.

**Pickup reading set** (update 2026-09-27 14:4x):
- this file complete: position, rulings, the continuation;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-27.md`, today's sittings (0.162.1, 0.163.0);
- `notes:model-fit/work.md`, the audit, the release and the composer trial's starting facts;
- `notes:outside-the-repo.md`, live links outside the repo.
Deeper: `docs/decisions.md`; `notes:real-use-evidence/work.md`; `notes:rolling-session/threshold.md`.

**Notes commit:** `4592a483707c5f2a18d1916f983761647820e649` (pass it to `prepare`/`pickup` as `--notes-commit`).

The observed position before this save is 0.163.0 on `main`; the boundary commit is this save itself.
Ask `git log` for its ID.

**Measured** 2026-09-27 14:4x: 38,805 bytes, about 9,702 tokens (estimate), 1,702 over the 8,000 target; kept because `## Now` (12.9 KB) holds the watch items the apple-music re-grade grades and today's log carries both sittings; the model-fit sketchbook holds the composer trial's starting facts. All five carried findings are in the set. `read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-27.md",
 "--file", "notes:model-fit/work.md", "--file", "notes:outside-the-repo.md",
 "--section", "TODO.md", "## Now"]
```
