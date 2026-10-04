# TODO

## Now

**Release boundary:** 0.167.1 on `main` (overtone mod 0.5.2 live, outside Kerd); **releases are paused** (Anthony 2026-09-28 15:00; 0.165.0, 0.166.0, 0.167.0 and 0.167.1 released on his asks): findings go to the Backlog; a fix comes back to him for the release decision. Claude Code and Codex both have 0.167.1 installed (Codex 2026-10-04 10:5x); the open codex-tui window loads it only after he restarts it (`codex resume`). Position is in `CONTEXT.md` `## Where We Are`. Rows closed 2026-10-03 (watch-row prune) are in `docs/backlog-archive.md`.

- **Watch `overtone` 0.5.2 in real use** (0.5.0 live 2026-10-03 23:1x; 0.5.1 blocks 2026-10-04 10:1x ran solid in his font; 0.5.2 medium squares `◼` 10:5x; backup
  `~/.claude/mods-work/overtone-live-pre-0.5.2`). `◼` bars confirmed separate by Anthony 10:52 in a fresh session (he saw 0.5.0's solid
  bars and asked for blocks like the mock `notes:overtone/band-bars.html`). Never seen live: the red alerts and their `⚠ N` fold, the cache card, Codex rows on real data,
  the guard passing a new work folder in a private repo, and the guard's "GitHub did not answer within 5 s" wording (needs a real
  stall). The 17:51 false stop on the vault was a `gh` timeout (identical retry passed 2.5 min later), fixed in 0.5.0. Sketchbook
  `notes:overtone/work.md`.
- **Watch 0.167.x in real use:** the first Switch Out that shows "Switch In will offer"; the first arrival on 0.167.1 shows its
  screen above the picker (0.167.0 skipped it in 2 of 5 arrivals on 2026-10-03, and for a Kerd user 2026-10-04).
- **Anthony: restart codex-tui** (`codex resume`) so it loads 0.167.1 (installed 2026-10-04 10:5x; `notes:codex-update/work.md`).
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

- overtone guard misses wrapped git commands (pre-existing since 0.5.2, found 2026-10-04 review): `env git add .env`, `sudo git`, `nice`/`timeout`, `bash -c "git add"`, `eval`, `xargs git add`, `find -exec git add`, git aliases, `git subtree push`. Fix: skip-prefix env/sudo/nice/timeout/xargs, re-parse `-c`/eval strings, ask on unknown wrapped forms mentioning add/commit/push. `notes:overtone/work.md`.
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
- **A Codex that Kerd starts has no internet (user feedback relayed by Anthony 2026-09-29 09:22 to 09:25: "spins up
  codex in a sandbox with no internet access", "anytime i ask it to do anything").** Checked in code: every Codex Kerd
  starts is `read-only`, or `workspace-write` for an editing job, with approval "never" and no network setting
  (`agent.py:1088` new partner, `conductor/scripts/ask.py:267` worker or reviewer, `switch/scripts/codex_roll.py:330`
  managed Roll, which also turns web search off). Codex keeps network off in those sandboxes unless the config turns it on
  (openai/codex `codex-network.md`). Messages into the person's own open Codex session carry no sandbox override
  (`agent.py:1230`), so the person's settings apply there. Stated rule: `conductor/references/model-jobs.md:298`
  (read-only jobs perform no network operations). Cost: a Codex job can't check docs, fetch packages or run tests that
  download. **Tested 2026-09-29 09:3x** (scratch repo, `ask.py run --target codex`, codex-cli 0.159.0, `curl
  https://example.com`): editing job without the setting "Could not resolve host"; with `[sandbox_workspace_write]
  network_access = true` in `~/.codex/config.toml`, HTTP 200; read-only job with the setting still "Could not resolve
  host". Config restored after. So the config line fixes editing jobs only; reviews stay offline. **Web search, tested
  09:58:** a read-only `ask.py` Codex job used Codex's own web search and returned requests 2.34.2 from PyPI, so the
  limit is shell-command network, not lookups (codex-tui round 3 caught the conflation). **Built as 0.165.0 on
  Anthony's "lets just implement it" (09:37).** **Anthony's proposed countermeasure (09:29):** when Kerd would start a Codex, ask what Codex's
  role is and advise the person to run `codex` in a new terminal and share its session ID, so Kerd pairs with their own
  session and their settings apply. **Proposed fix (Anthony "yes" 09:34 to record it; not built):** in Agent's choice of
  existing session / new persistent partner / fresh worker (`skills/agent/SKILL.md:64`), say that a Codex Kerd starts is
  offline, e.g. "A Codex I start is offline: read-only, no internet. For internet, open `codex` in a new terminal in this
  folder and I'll find it." No ID sharing needed: `agent.py sessions` already discovers open Codex sessions from the
  local session store (checked 09:3x: found `codex-tui` and one other in Kerd). Its "partial discovery" when the
  optional `websockets` dependency is missing (seen on the Studio 09:3x) belongs in the same advice. Fix is Anthony's
  release decision.
- **The chat roll can't fire without a declared context window (alapah a15a217f, Kerd 0.164.0, 2026-09-29 03:30Z).**
  The session called `/kerd:switch roll` after a merge, then did not roll: "no host-declared context window for this
  model" (model ID `claude-opus-5-5`, no `[1m]`). The context-reading hook gives tokens only (`hooks/context-reading.sh:6`),
  so on this setup the 50% trigger can never fire; the refusal was written only to the sketchbook, not said to the
  person as `to-roll.md:147` asks. One sitting and a code reading; how the 2026-09-25 test rolls got their window not checked.
- **Claude Code mods (shipped 2.1.287, 2026-10-01): `overtone` 0.2.0 is live** (context, model and workers band; private-path guard;
  turn-end check removed on his word). Left from the six ideas: idea 6, one-button Switch Out, as "fill the prompt, he presses Enter"
  (probe `notes:overtone/evidence/f-idea6-probe.md`; not agreed). Claude Code only; Codex looked at separately. `notes:overtone/work.md`.
- **Switch SKILL.md frontmatter is unquoted and holds ": "** (found 2026-10-03 by the description fixer): a strict YAML parser rejects
  it; the pre-0.167.0 text had the same shape and Claude Code loads it. Fix only if a host refuses it.
