# Context

## What This Is

Kerd — a Claude Code plugin of eight workflow skills: switch (session handoff and the boundary), conductor (rehearsal, then the concert: a sketchbook that becomes a score, players, a goal check), visuals, agent (Claude and Codex working together), tend, slainte, kivna and skriv. Cut: capturerequirements (v0.73.0), sherpa (v0.74.0), mode and all eleven modes/ files (v0.75.0), trim (v0.87.0), and on 2026-09-19 drive, lorg, interrogate and pair (v0.141.0) and the whole ladder of machine checks with its tiered risk ledger (v0.142.0).

## Where We Are

**Release boundary: 0.163.1 on `main`** (2026-09-27 18:3x; CI green). 0.163.1 came from the matched composer
trial (Anthony 16:39 "lets do the trial"; 17:57 "y" to the release): one real brief (the 2026-09-25 Agent security
composer passage) replayed unchanged on a checkout frozen at 0bbb4f3 to Opus 5.5 xhigh, Fable 5.1 high and (on
his 16:50 ask) a fresh Codex. Blind grades: Codex (two-way) Opus first, clearly; Sonnet 5 (three-way) Opus first,
Fable a slight second, Codex a clear third. One brief, one reading, not a ranking. The trial also found a live leak
shipped in 0.155.0: Agent's printed output carried up to 64 bytes of the partner's session log (`tail`); 0.163.1
strips it, with a test. Evidence: `task-evidence.md` "Matched composer trial"; `model-choice.md` Opus row links it.
Sketchbook `notes:model-fit/work.md`. Anthony on the "Opus first, Fable when Opus falls short" line (16:39): "is
that a real rule? dont remember setting that" — it is guide text from Anthropic's guidance (0.148.0), not his ruling.
0.163.0 (earlier today) filled the model profiles; account `kivna/sessions/2026-09-27.md`.

**Claude Code runs 0.164.1** (2026-09-28 16:xx; applies on restart). **Codex runs 0.164.0** (installed
2026-09-28 08:5x on Anthony's go in its window, skills checked identical to `main`); 0.164.1 changes only Switch's
roll script, which Codex does not run, so its install waits for his go. Laptop bells are on for both
(backups `*.bak-bell`). Sketchbook `notes:codex-update/work.md`.

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
- **Releases are paused so Anthony can use Kerd (2026-09-28 15:00: "i would like stabalize releases for a while and
  use it"; "yes but only if there is nothing left to fix").** The pause starts at 0.164.1, which fixed the one
  defect the 2026-09-28 apple-music re-grade found. While it holds: grades, findings and ideas go to the Backlog, not
  into releases; any fix found comes back to him for the release decision; he lifts the pause.
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

**Selected continuation (proposed, not approved to run):** re-grade apple-music's real use of Kerd from
~2026-09-28 13:00 (it restarted onto 0.162.1 at ~13:1x 2026-09-27, the agreed day of use), read-only, brief
`notes:real-use-evidence/reader-brief.md`; grades into `notes:real-use-evidence/work.md`. Why: it is the next real-use
evidence on the rules shipped since 0.160, including the question and report shapes, from a project other than Kerd.
Stops at the grades; any fix is a separate go. **Anthony's:** Codex install of 0.163.1; the hand-roll judgment (this
sitting was rolled at ~227k). Still on watch, unseen in real use: push-first trigger, chat roll, findings-coverage
and departure rules. Model fit: one matched trial done; a second brief would firm it up (not scheduled). Parked: the
200k roll plan, the announcement, SAM and Aubel.app, the homepage, the thrash guard. Dropped: launch step 2. Backlog:
one row, Skriv voice-profile wiring, blocked on his writing samples.

**Pickup reading set** (update 2026-09-27 18:5x):
- this file complete: position, rulings, the continuation;
- `TODO.md` `## Now`, the designated active list;
- `kivna/sessions/2026-09-27.md`, today's three sittings (0.162.1, 0.163.0, 0.163.1);
- `notes:real-use-evidence/reader-brief.md`, the brief for the apple-music re-grade;
- `notes:outside-the-repo.md`, live links outside the repo.
Deeper: `docs/decisions.md`; `notes:model-fit/work.md` (the trial, closed); `notes:real-use-evidence/work.md`;
`notes:rolling-session/threshold.md`.

**Notes commit:** `4b3382064ef14dcacef228022c65e40455082144` (pass it to `prepare`/`pickup` as `--notes-commit`).

The observed position before this save is 0.163.1 on `main`; the boundary commit is this save itself.
Ask `git log` for its ID.

**Measured** 2026-09-27 18:5x: 38,818 bytes, about 9,705 tokens (estimate), 1,705 over the 8,000 target; kept
because `## Now` (13.5 KB) holds the watch items the apple-music re-grade grades, and the reader brief is the next
action's input. The model-fit sketchbook left the set (trial closed). All five carried findings are in the set.
`read_args` for the next pickup:

```
["--record", "CONTEXT.md", "--file", "kivna/sessions/2026-09-27.md",
 "--file", "notes:real-use-evidence/reader-brief.md", "--file", "notes:outside-the-repo.md",
 "--section", "TODO.md", "## Now"]
```
