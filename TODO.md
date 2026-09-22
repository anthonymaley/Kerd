# TODO

## Now

**Release boundary:** 0.146.0 on `main`. Resolve IDs with `git log`. Position, the
local-only paths and the reading set are in `CONTEXT.md` `## Where We Are`.

**The launch plan is accepted** (Anthony, 2026-09-22 09:38): `docs/design/launch-plan.md`,
sketchbook `docs/work/launch-plan/work.md`. Kerd is ready to launch when someone other than
Anthony carries real work in their own repository to its agreed result, unaided. **Next on
the route, step 1:** Anthony takes one real piece of work on a project that isn't Kerd
through Kerd, over at least two sittings: **3of3, proving its iCloud sync** (Anthony,
2026-09-22 10:41). Kept light; Kerd's own sittings count as proof of use too. Runs in a session
in `product/3of3`, not from Kerd.

**Anthony's:** whether the 2026-09-13 hold is lifted (rows 3
and 5 of its list are unclosed); who the invited few are; where and when to announce. Decide whether the
explanatory output style stays on for this machine; it asks for Insight blocks and pulls
against the report shape. GitHub's README rendering, checked 2026-09-22: all four pictures
load and the smallest label shows at 16.8px; the repo homepage already links the site. The
repo's GitHub description now matches the site's line (set 2026-09-22 on Anthony's "sure"). Leftovers from the
2026-09-21 image test, both harmless and left because they are his: an idle Codex session in
tmux `codexprobe`, and a trust entry for `/private/tmp/codex-img-probe.kykwaJ` in
`~/.codex/config.toml`.

- **The site does not tell the musical story** (Anthony, 2026-09-22 17:31): "i dont see
  any of the strong musical narrative in the website - we could really use that to convey
  Kerd". Rehearsal, the sketchbook, Ready, the score, the concert, players — the language
  the product is built on — barely appears on the pages. Its own Shape.
- **The report shape and the finish: changed in 0.145.0, watch them in use.** A
  correction of Kerd's own earlier claim now rides in the opening lines and never
  competes for the five items; a finish names the next item instead of ending on "no
  action needed". Both came from repeated real instances, four of them on 2026-09-22.
- **The image-by-path route now has Claude evidence too (2026-09-22).** A fresh read-only
  Claude worker on Sonnet 5 read a PNG from its absolute path and answered three
  picture-only questions correctly. Still untested on Claude: an established partner
  rather than a fresh worker, and a file outside the project.
- **Pictures at a laptop width: fixed in 0.144.1.** Measured 2026-09-22 at 1440, 1280 and
  1152: the site now stacks below 1200px (labels 26px), 1201-1280 stays two-column at 14px,
  and the concert picture's smallest type went 28px to 32px. Phone widths stay unmeasured.
- **Show the model and effort where a running job is listed.** Asked 2026-09-19 22:09 with
  a screenshot Claude could not open (it was on the laptop): the job list shows
  `kerd:effort-high` rather than the model and effort. Kerd's status line does not draw that
  label; Claude Code prints the agent's type name, which cannot carry a model because the
  effort agents are model-free. What Kerd controls is the short per-job description each
  dispatch sends; leading it with the pair ("Opus · high — …") is a wording change to the
  dispatch contract. First confirm which string the bar shows. Its own go.
- **Rolling without publishing: built in 0.144.0, not yet seen in a real concert.** A
  concert now performs on `concert/<work>`, and the merge back is the person's go
  (Anthony agreed the design 2026-09-22 11:53). Watch the first real concert that rolls.
- **Release notes live in two places, now with a check.** `tools/release_check.py` (CI,
  every push) refuses a version whose note differs between `README.md` and `CHANGELOG.md`,
  or a version in the README and not the changelog; older entries the README trimmed are
  allowed. Each release still updates both by hand.
- **The stale-reference row is closed (2026-09-22).** The Codex core guide no longer
  pins 0.113.0 in its example paths and now says eight skills with four excluded by name;
  the state contract, machine-setup and playbook were corrected in 0.144.1.
- **Observe the composer, managed Conductor and a roll in a real session.** None has been
  exercised. Fan-out has now run four times (twenty dispatches, then four, then two, then
  two plus one).
- **Observe the arrival's "Something else" route** and the closing box over several
  sittings. The arrival and "Yes" were seen again on 2026-09-20 14:35.

- **0.134.0's two clauses have never been measured on real diagram output.**
- **Unverified for 0.132.0:** whether either rule holds beyond the one marginal scenario.
- **Archify's two Socket alerts were never identified**: unknown, not cleared. Its
  version is still the dev snapshot `2.17.0-dev.1`.
- Run the behavioural scenario in `docs/work/codex-plugin/work.md` with a model, not a
  fixture.
- The 2026-09-13 10:41 hold ("prove Kerd first") deferred a Codex pickup in a work
  project. Whether it is lifted is Anthony's call; don't assume it.

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

- **`tend` and `slainte` name the plugin placeholder literally, and Claude Code
  fills it in.** Measured 2026-09-18: `${CLAUDE_PLUGIN_ROOT}` in SKILL.md text
  is replaced by the install path at load. `skills/tend/SKILL.md` :213, :217,
  :241 and `skills/slainte/SKILL.md` :104 mean the literal placeholder (e.g.
  "a bare `${CLAUDE_PLUGIN_ROOT}/hooks/` path"), so the model likely reads a
  rewritten instruction. Not yet observed in a real tend run.

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
