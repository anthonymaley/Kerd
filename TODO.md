# TODO

## Now

**Release boundary:** 0.175.0 on `main` (overtone 0.8.0 public in its marketplace); **releases are paused** (Anthony 2026-09-28 15:00; 0.165.0 through 0.175.0 released on his asks): findings go to the Backlog; a fix comes back to him for the release decision. Claude Code has 0.175.0 (2026-10-06 13:5x, loads on restart) and overtone 0.8.0; Codex has 0.175.0 (13:5x), level with main; a running Codex thread picks up an install on its next turn. Position is in `CONTEXT.md` `## Where We Are`.

- **Watch 0.174.0 in real use:** a question that chooses among listed options should end on the recommendation ("Start with <it>?"), not an open question (0.173.0's first real use, 11:41, asked the open one; fixed 0.174.0); a missing fact still gets its own question; Switch Out's new order (vault commit written before the last project commit, nothing after the boundary check); a refused chat roll said in chat. Wording tests only. Sketchbook `notes:fixes-2026-10-06/work.md`.
- **Watch 0.175.0's chat roll fire on a reported window:** a Conductor chat in tmux past 50% of the window overtone reports (~500k at 1M) should roll at a batch boundary; after a model switch it should refuse until restart. Wording tests only; never seen live. Sketchbook `notes:chat-roll-window/work.md`.
- **0.174.0's question rule held at its first two real sightings** (2026-10-06 13:0x: Switch In's "Start with the chat-roll fix?" answered "y"; a decision block's "— approve?" answered "y"); keep watching other sittings.
- **Watch overtone 0.8.0's workers rows:** a finished nested helper should leave the band when the agent above it ends; one overtone cannot explain shows "quiet" after ten minutes, never "running" for hours. Reviewed safe by codex-tui in three rounds, 469 tests; never seen live, and the cause of the 2026-10-05 stuck rows is likely, not proven.
- **Watch 0.170.0 Switch, 0.171.0 Conductor and 0.171.1 Agent in real use** (and 0.172.1: Switch Out ends on its box, nothing after the closing line; wording test only, evals not re-run): Switch's must-hold lists ran their first real In and Out on 2026-10-05 (Opus; In and Out on 0.170.0); Conductor's restructure has evals only (entry 2 of 3 clean, the go 0 of 3).
- **Watch `overtone` in real use (0.7.1 installed 2026-10-05 13:1x, loads on restart: worker rows show the task; 0.7.0 09:5x the new guard and the workers-and-cache band; 0.6.0 from 2026-10-04 17:3x; 0.5.2 history below)** (0.5.0 live 2026-10-03 23:1x; 0.5.1 blocks 2026-10-04 10:1x ran solid in his font; 0.5.2 medium squares `◼` 10:5x; backup
  `~/.claude/mods-work/overtone-live-pre-0.5.2`). `◼` bars confirmed separate by Anthony 10:52 in a fresh session (he saw 0.5.0's solid
  bars and asked for blocks like the mock `notes:overtone/band-bars.html`). Never seen live: the red alerts and their `⚠ N` fold, the cache card, Codex rows on real data,
  the guard passing a new work folder in a private repo, and the guard's "GitHub did not answer within 5 s" wording (needs a real
  stall). The 17:51 false stop on the vault was a `gh` timeout (identical retry passed 2.5 min later), fixed in 0.5.0. Sketchbook
  `notes:overtone/work.md`.
- **Watch 0.167.x in real use:** the first arrival with its screen above the picker was seen 2026-10-05 10:52 (Kerd 0.169.1, Claude, picker with three options and free text; one sitting). Still to see: a Switch Out box showing "Switch In will offer" read back by the next arrival.
- **Watch the Sonnet 5.5 profile (0.166.0) in real use** (`notes:sonnet-55/work.md`): 24 clauses pending. First check
  2026-10-03: on the apple-music grading job medium matched high (6 of 6 slips each, ~7% fewer tokens); one run each, not a
  verdict. Readers stay at high, no release (Anthony 2026-10-04 10:56); the Backlog row collects more runs, revisit after two or three agree. Still to see: whether the two Sonnet agent lines hold.
- **After any diagram-design update, reload the Kerd profile** (Anthony 2026-09-26 09:54). Updates replace the installed
  `style-guide.md` with the default; a project without a `.diagram-design` marker then draws in orange.
- **Bring Codex along with each release** that changes its four-skill package (Conductor, Switch, Visuals, Agent); Codex
  builds and installs only on Anthony's go in its window.
- **Roll at ~200k by hand, then compare (trial since 2026-09-25; plan parked 2026-09-27, "i want more data first").** Three
  hand rolls judged, none with loss reported; the decision waits on more sittings. The thrash guard stays parked unless a real
  roll is refused. Readings and history: `notes:rolling-session/threshold.md`.
- **Unseen in real use, watch for the first time each happens:** the push-first trigger (0.156.0), the unanswered-review rule
  (0.149.0), the chat roll in a real Conductor build (0.154.x), rolling without publishing (0.144.0), the composer and managed
  Conductor, the arrival's "Something else" route, the first cross-provider build exception (0.151.0), and a pickup of
  `notes:` on a second machine (0.157.0). Leftovers that are Anthony's to delete: tmux `codexprobe`, and the trust entry for
  `/private/tmp/codex-img-probe.kykwaJ` in `~/.codex/config.toml`.

**The launch plan is accepted** (Anthony, 2026-09-22 09:38): `docs/design/launch-plan.md`, sketchbook
`notes:launch-plan/work.md`. Ready to launch when someone other than Anthony carries real work in their own repository to its
agreed result, unaided. **Step 1: 3of3 is using Kerd in its own sessions; Kerd evidence is read from those sittings when
Anthony asks for it.** 3of3's own work is not Kerd's open work. Where and when to announce is Anthony's.

## Backlog
- **Switch evals: grader limits** (2026-10-05; two fixed in 0.174.0: the measurement check takes "0.7k tokens", `conductor-not-read` catches In reading Conductor through Read). Left (codex-tui 2026-10-06 11:51): guide-read passes a `head` slice, and command names cannot prove a whole-file read (`cat x | head`, `bat --line-range`, Read with `limit`); `boundary-ran` does not check success or that it ran after the last save, and `tool_order` compares first matches only, so an order grader cannot prove a final boundary; `conductor-not-read` misses shell reads. On this Mac evals need `PATH=~/.cache/kerd-eval/gitbin:$PATH`.
- **Haiku does not follow Switch** (evals 2026-10-05, before and after 0.170.0): In never opens its guide or runs the renderer (hand-writes the screen, ~0.6); Out skips most steps (~0.2) and once wrote `boundary: "passed"` without running it. Not a target today; noted for anyone routing Switch to Haiku.
- overtone guard, rare in-scope gaps left at 0.7.0 (2026-10-04 fourth review): `cd /a && cd /b && cd - && git push` reads the wrong repo; a shell alias running `git -C ..` from inside a nested repo resolves from the wrong root; `push --all/--tags/--mirror` trusts stale tracking refs after the public remote was rewound (verify excluded refs live, or ask). `notes:overtone/work.md`.
- overtone guard, out of scope by decision (Anthony 2026-10-04 22:18, "safety net for honest mistakes"): a command string piped into a shell (`printf 'git add' | bash`), command strings or names in variables (`bash -c "$CMD"`, `"$G" "$C"`), `GIT_CONFIG_*` set before `bash -c`, `git config remote.*.pushurl …; git push`, `--git-dir`/`GIT_DIR` to a public repo from a private one, an on-the-spot `-c alias.x='!git push …'`; also unguarded: `git update-index --add`, `send-pack`, `http-push`, `gh pr create`. Revisit only if a real slip shows one.
- overtone lows (0.7.0): `git push --dry-run` asks; read-only shell aliases (`!git log`) ask in public repos; `git lfs`/`git-<name>` programs ask there; a nonzero `git show` of `kivna/vault.json` at HEAD or a named pushed branch counts as absent; a short band can fold one worker more than needed; below 3 rows the band can overrun.

- Sonnet readers at medium instead of high (2026-10-03 effort check: medium matched high on one grading job, ~7% fewer
  tokens, one run each; `notes:sonnet-55/work.md`). Held 2026-10-04 (Anthony): no release; collect two or three more runs first.
- The 2026-09-28 apple-music question-shape grade undercounted: the 2026-10-03 re-run found more consequential asks without a
  block on 0.162.1/0.163.2 (three confirmed). Old versions; recheck on a current-version sitting before any rule change.
- skriv voice profile wiring — needs non-founder-genre samples.
- A named wait missed a partner's reply once (apple-music, 2026-09-28 11:14 to 11:30, Kerd 0.163.2): the session
  said it was waiting on Codex's review, the reply landed, the watcher missed it, and Anthony had to ask "waiting?".
  1 of ~69 named waits in the 2026-09-28 re-grade (`notes:real-use-evidence/work.md`). **Studied 2026-09-28 19:5x,
  cause found:** Codex mistyped the reply's ID when it renamed its file (asked `3a9c94da-441c-44d4-a9c9-cf05b49f7e59`,
  wrote `3a9c94da-441c-44a9-c9cf05b49f7e59.md` at 11:17:10), so the waiter, still correctly polling the asked path,
  never matched. The session's wait was honest; the reply went to the wrong name. The bridge was apple-music's own
  `ask-codex` (v7, in its vault), not Kerd Agent. Kerd Agent has the same kind of risk, not yet seen: a reply counts
  only if the partner types the full 36-character `<kerd-reply-ID>` marker back exactly (`agent.py:467`). Also found:
  four `.tmp` replies from 2026-09-25 that were never renamed. Possible fixes for Anthony's release decision: a near-miss
  match on the ID, or a shorter marker. Detail in the evidence note.
  **Anthony 2026-09-28 23:09, "y": kept in the Backlog, unfixed, until the reply-ID miss is seen in Kerd Agent itself.**
- **Claude Code mods (shipped 2.1.287, 2026-10-01): `overtone` 0.2.0 is live** (context, model and workers band; private-path guard;
  turn-end check removed on his word). Left from the six ideas: idea 6, one-button Switch Out, as "fill the prompt, he presses Enter"
  (probe `notes:overtone/evidence/f-idea6-probe.md`; not agreed). Claude Code only; Codex looked at separately. `notes:overtone/work.md`.
