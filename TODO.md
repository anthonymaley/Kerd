# TODO

## Now

**Release boundary:** 0.154.1 on `main`; both hosts run it (Codex read back 2026-09-25 09:41). Resolve IDs with `git log`. Position, the
local-only paths and the reading set are in `CONTEXT.md` `## Where We Are`.

**The launch plan is accepted** (Anthony, 2026-09-22 09:38): `docs/design/launch-plan.md`,
sketchbook `docs/work/launch-plan/work.md`. Kerd is ready to launch when someone other than
Anthony carries real work in their own repository to its agreed result, unaided. **Step 1 is
under way, in 3of3's own session** (Anthony, 2026-09-23: "that project is already using kerd
and is switched in"): its next item is the TV-to-TV iCloud sync proof (Anthony is doing it on 2026-09-24,
in 3of3's own session, and will say here when it is done), his hands on the
televisions. Not in 3of3's records as of 2026-09-24 14:58. Kerd hands nothing over; after each sitting there, one line of evidence goes
into `docs/work/launch-plan/work.md`, which already holds step 1's evidence so far.

**The team note is going out** (Anthony, 2026-09-23 17:05, "y" to sending it now; not yet
confirmed sent). **Parked:** "delay any sam and auble work for now" (Anthony, 2026-09-24
08:55); don't ask about it until he picks it up. Each team's reply goes into its lines under "The team note goes out" in
`docs/work/launch-plan/work.md`, one per field of the plan's per-person record.

**The 2026-09-13 hold is lifted** (Anthony, 2026-09-23 18:19; `docs/decisions.md`), so
launch step 2 is open. **Anthony's:** who the three to five invited are (asked 18:20,
parked 21:13: "skip lets skip that"); where and when to announce. GitHub's README rendering, checked 2026-09-22: all four pictures
load and the smallest label shows at 16.8px; the repo homepage already links the site. The
repo's GitHub description now matches the site's line (set 2026-09-22 on Anthony's "sure"). Leftovers from the
2026-09-21 image test, both harmless and left because they are his: an idle Codex session in
tmux `codexprobe`, and a trust entry for `/private/tmp/codex-img-probe.kykwaJ` in
`~/.codex/config.toml`.


- **A session should never sit idle with nothing asked** — shipped in 0.146.0; on 2026-09-24 it
  did not hold (ten status prompts across four sessions). 0.153.1 names the two missing endings
  and his global CLAUDE.md now carries a turn-end gate; watch whether he still has to ask.
  Both hosts run 0.153.1 (Codex read back 17:29). Sketchbooks: `docs/work/no-idle-sessions/work.md`,
  and the superseded monitor framing in `docs/work/waiting-on-you/work.md`.
- **The report shape and the finish: changed in 0.145.0, watch them in use.** A
  correction of Kerd's own earlier claim now rides in the opening lines and never
  competes for the five items; a finish names the next item instead of ending on "no
  action needed". Both came from repeated real instances, four of them on 2026-09-22.


- **Watch the unanswered-review rule (0.149.0)** the first time a partner doesn't answer:
  a fresh reviewer recommended on his yes, never a waiver. Record:
  `docs/work/partner-closed/work.md`.
- **The Opus 5.5 profile was revised in 0.152.0 against Anthropic's guide;** two clauses
  carry one paired observation each, three new clauses are pending (unattended premature stop,
  fan-out time budget, explore before acting). Watch the first real brief that uses them.
  Sketchbook `docs/work/opus-55/work.md` (local). The GPT-6 profile (0.148.0) is untested.
- **Watch the context reading (0.153.0) in its first live session:** a `Context: N tokens in
  the last request` line at each prompt and during long turns, matching the status line. Seen
  once by hand before release (170,532 tokens vs "83%" free, 2026-09-24 15:34). First live delivery
  17:39: a fresh headless session got the line on its second prompt (35,110 tokens). Silent at
  a session's first prompt by design (no reply to count yet); wording fixed in 0.153.2. Since
  0.154.0 it also records the host's permission mode for the chat roll. **First seen in an
  interactive session on 2026-09-25 (0.154.1):** the line arrived at every prompt from the second
  (91,889 at 08:58 up to 115,948 at 09:42) and after tool calls mid-turn. One session, not verified.
- **The homepage redesign: dropped, to revisit** (Anthony, 2026-09-24 12:56). Three Codex
  passes and his reactions: `docs/work/homepage-redesign/work.md` (local).
- **Rolling without publishing: built in 0.144.0, not yet seen in a real concert.** A
  concert now performs on `concert/<work>`, and the merge back is the person's go
  (Anthony agreed the design 2026-09-22 11:53). Watch the first real concert that rolls.


- **Watch the chat roll (0.154.0–0.154.1) in a real Conductor build.** Two test rolls worked on
  2026-09-25 (pane restarted, same model/effort/mode, next step done); a concert rolling itself at
  50% is unseen, and so is a roll from a process shown as capital `Claude` (unit-tested). The
  three-in-a-row limit counts every roll in a checkout within six hours; see whether it bites.
  Sketchbook `docs/work/rolling-session/work.md` (local).
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
  first request and its Fit line. Sketchbook `docs/work/codex-players/work.md` (local).
  Codex building the homepage on 2026-09-24 was Anthony giving it the work directly, not a
  Conductor dispatch.
- **Roll at ~200k by hand, then compare (Anthony, 2026-09-25 10:26).** The Studio status line
  now shows tokens used and a coloured state (green keep working, yellow switch at a break from
  200k or 60% used, red switch now from 80%); he rolls by hand at a break. After a few
  sittings, compare average tokens re-sent per call, rolled vs not, and decide whether Kerd's
  chat roll moves from 50% to 200k. The built alternative was dropped as too complex. Sketchbook
  `docs/work/rolling-session/threshold.md` (local).
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

- **Which session is waiting on you** (parked 2026-09-21 by Anthony's agreement; not
  started). From a `weefish-c8` research drop prompted by herdr.dev: surface which agent
  is working, idle or blocked on a human. Anthony is not leaving tmux; only the signal is
  wanted. Checked here: the harness's `ListAgents` already gives busy/idle and the tmux
  pane for every **Claude** session, but lists **no Codex sessions**, so for Codex even
  "working" needs another source. Pane-scraping a Codex TUI worked on 2026-09-21 but broke
  twice (a missed match pattern; an Enter that raced the paste). **Verified 2026-09-21**
  against code.claude.com/docs/en/hooks-guide (reported by `weefish-c8`, then read here):
  `Notification` fires "when Claude is waiting for input or permission"; matcher
  `permission_prompt` after about 6s, `idle_prompt` about 60s after Claude finished;
  every event carries `session_id`. So the Claude half is a documented hook-driven state
  machine. Caveats: `agent_needs_input`/`agent_completed` fire only while agent view is
  open; `permission_prompt` is timed differently under Agent-SDK hosts. Codex has no
  hooks, so pane-scraping stays its only path — the hard half. Kerd's own 💬 question ending every turn is a native
  "waiting on you" signal. Needs its own Shape; it carries a hook, so weigh it against
  the rule that a countermeasure matches the defect's size.

*Repository-quality debt that survived the ladder's retirement. Forty-three rows that were
debt against the ladder, the ledger, the register or their tools were closed as dead on
2026-09-19; they are in `docs/backlog-archive.md` with the verdict.*

- **Agent's four disclosed-not-built limits** (Fable foundation review,
  2026-09-11; stated in `native-sessions.md`): a native log rewritten in place
  with its inode preserved passes the replacement guard; the Claude socket's
  peer process is not verified where the native client verifies it; a new
  partner's first contribution and every `codex queue` message travel in argv,
  readable by other local accounts; every Kerd controller sends as
  `kerd-agent`, so a per-sender throttle is shared. Each has a smallest
  correction on record; none is built.

- **The fidelity check** (accepted unknown; review trigger already fired).
  Nothing verifies a pickup restored what the close recorded. It proves *file*
  reachability, never *finding* reachability.

- **boundary-cycle, in-half** — the reset ritual's automation. Killer
  feasibility question first, verified against harness docs at frame.

- **Plugin cache repin debt.** Reopened by v0.95.0: the cache was current at
  0.94.0 this afternoon and the repo has since shipped. Structural — the only
  session running current cache text is one where nothing shipped. (Narrowed by
  v0.96.0: this is now about stale *skill text* only — hooks no longer rot with
  the cache version, they auto-load and resolve `${CLAUDE_PLUGIN_ROOT}` at runtime.)

- **Machine-local state has an inventory but no refuser** (filed 2026-08-27 at
  the Mac Studio move). `docs/machine-setup.md` §4 lists what git cannot carry —
  `kivna/.pair`, `kivna/.active-modes`, `~/.claude/settings.json`, the `~/eolas`
  symlink — and §3 greps for hand-wired hook duplicates that must print nothing.
  Both are prose a person runs, so nothing refuses a machine that drifts. **The
  drift that actually bit was the silent kind:** a duplicate pair hook fires
  correctly and looks like the feature working while injecting text that
  contradicts the live version. Candidate shape, not chosen: a `/kerd:tend`
  category that runs the doc's greps, since tend already owns structural
  convergence and already had its Category 9 rewritten to *remove* stale wiring
  rather than add it. Open question before any build — does this belong to tend
  at all, or is a machine's config outside every repo's business?

- **Stashes and local-equals-remote are unchecked at the boundary.** Evidence
  arrived 2026-09-06, handed off by the apple-music session (`apple-music-78`,
  approved at that session's plan gate — reported, not verified here): on
  2026-09-02 its Switch Out banner passed three times over 53 commits that no
  remote had reached. The mechanism is in Kerd's own text —
  `skills/switch/SKILL.md:246-261` proves the boundary with `git status` +
  `git log -1`: `Tree: clean` tests uncommitted work, `Pushed:` is a claim
  about a command's output, and the log header's `**Tracking:**` line is
  model-written. A *failed* push already stops (`:261`); an unverified one does
  not, and nothing fetches or checks containment on the way out —
  `hooks/session-start.sh:21` checks only the inbound direction (remote ahead
  of local). A working countermeasure exists outside the repo, verified
  read-only: `~/eolas/vault/kerd/bin/boundary-check` (v3, 2026-09-02) fetches,
  then exits 1 on a failed fetch, a HEAD no remote ref contains, or a dirty
  tree, on every repo passed to it, with no success bypass
  (`BOUNDARY_LOCAL_REASON` prints as an unverified operator assertion; the exit
  stays 1). apple-music's CLAUDE.md carries the override ("Switch-out is not
  complete until BOTH repos pass the mechanical gate"). The ask as handed off:
  Switch Out runs it on every repo the boundary owns and refuses the ✓ banner
  while it fails. **Decision owed to the producer:** fold it into switch step 7
  as a required evidence line, promote the script into `tools/` or a hook, or
  frame it as its own item. Same class as `check_stage_schema()`/AU10 — a
  prose rule that did not grip, replaced by a check that refuses.
  **Narrowed 2026-09-11:** Agent's `handoff.py save` verifies the remote carries the
  exact commit, but Switch Out itself still does not — `(done? — confirm)` is not
  warranted; the row stays open.

- **The playbook's `## Current Status` duplicates CONTEXT.md.** Its stale
  content was fixed this session (v0.90.0 → v0.95.0, three hooks → four); the
  duplication itself remains. Kill it or make it a pointer.

- **Out-of-repo artifacts have no home** — PRs, URLs, decks, external docs.

- **README's `## What's New (vX)` header is a second home for a fact the entries
  below already carry** (fixed forward 2026-08-30 by the release pass, v0.99.0 ->
  v0.104.0, having drifted five releases). The playbook records this exact class
  in its own `## Current Status` section — *"Two homes for one fact is how that
  happens, so there is now one home"* — and then the README does it one file
  over. Structural fix is to drop the version from the header entirely so the
  newest `### vX.Y.Z` entry is the only home; not done here because changing a
  convention at a close-out pass is the wrong moment for it.

- **skriv bans em dashes; the README's What's New voice uses them and always
  has.** Measured 2026-08-25: the v0.98.0 entry runs 0.019 em dashes per word
  and the new v0.99.0 entry matches it exactly. Writing the next entry to
  skriv's rule would make it the only one in the file in a different voice.
  The rule and the house surface genuinely disagree; needs a ruling, not a
  silent split.

- **`docs/vault-spec.md` contradicts itself** (found by tend this session): line
  39 says Weekly is "the one append-style file in the vault", line 88 describes
  the decisions file as accumulating entries. `Kerd Architecture Decisions.md`
  (6 dated sections) and `Kerd Skill Lessons.md` (5) sit in the gap. Not drift —
  a genuine unresolved rule.

- **Three vault-spec violations, all kivna's to fix** (tend detects, kivna
  writes — v0.83.0). `Kerd.md` MOC has one broken wikilink: the actual link is
  `[[eloas/Eloas]]`, double-typo'd (this row previously recorded it as
  `[[eloas/Eolas]]`; corrected 2026-08-25) — 16 of 17 resolve. And two files in
  the vault folder are not self-identifying: `discover-sources.json` and
  `2026-08-02-product-to-build.excalidraw`. The spine itself is complete
  (`Kerd.md`, `Kerd Status.md`, `Kerd Weekly.md`).

- AGENTS.md needs its own verdict: gitignored, machine-local, stale Codex-era fork.

- **kivna verdict** — same zero-usage smell as the vault; import/export
  confirmed unused.

- **CI rule for the single-definition law** — nothing machine-enforces
  "conductor never re-describes a Switch Out step".

- Stale `Kerd.md` MOC version field (says 0.31.0).

- skriv voice profile wiring — needs non-founder-genre samples.
