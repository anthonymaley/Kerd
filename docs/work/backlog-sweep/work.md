# Backlog sweep: the Kerd work that is still owed

Sketchbook, kept by Conductor. Started 2026-09-25 11:27 EDT.

## Agreed (Anthony, 2026-09-25 11:27)

After a read-only sweep of the Backlog against current code, Anthony chose to do:

1. **Agent's four security limits** ("yes agree"), starting with messages travelling in process
   arguments; the others: unverified Claude socket peer, in-place log rewrite passing the
   replacement guard, one shared `kerd-agent` sender throttle.
2. **Which session is waiting on you** (was parked 2026-09-21).
4. **`docs/vault-spec.md` contradiction** (Weekly "the one append-style file" vs Decisions accumulating).
5. **The stale vault** (`Kerd.md` version 0.31.0, broken `[[eloas/Eloas]]`, `discover-sources.json`).
6. **Kivna stays** ("kivna is kerd").
7. **Skriv all the content people can read** (resolves the em-dash row: skriv's rule wins).
8. **README What's New header**: fix so it cannot drift.
9. **Single-definition check**: stop Conductor re-describing a Switch Out step ("sounds like we need to stop it").

Defaults, push back if wrong: the six done/dead rows (push check, playbook status, AGENTS.md,
boundary-cycle, cache repin, machine-local inventory) close at Switch Out into
`docs/backlog-archive.md`. Skriv voice profile and out-of-repo artifacts stay open.

## Stage

Rehearsal: composing the score. No build, install or push approved yet.

## Risks

- Item 7 touches every reader-facing page; a voice pass can change meaning. Each rewrite is
  checked against the original for claims added or lost.
- Item 2 carries a hook; the countermeasure must match the defect's size.

## Pending

Score research dispatched 11:3x (four jobs); then the score, the rendered view, and Ready.

## Returns

**11:29 skriv inventory (Sonnet, medium; my check: counts plausible, parity rule R4 confirmed in
release_check).** About 52k reader-facing words. 272 of ~283 em dashes are in the release history
(README lines 268+ and CHANGELOG, which must match byte-for-byte per version). Top matter 7,
site/index 2, guides 0. Proposed seven parts: README top matter; release history newer half and
older half (each writes README then copies to CHANGELOG, then release_check); CHANGELOG-only tail;
four site pages (text only, no markup); guides A and B. Plugin descriptions: edit both together.
Open: whether the 17k-word release history is rewritten or only de-dashed (history vs voice).
`docs/guide/reference-from-readme.md` is untracked, out of scope.

**11:29 items 4, 5, 8, 9 (Sonnet, medium; my spot-check: vault files, spec line 39, kivna:315,
tend:157, slainte:99 confirmed; its "Kerd.md:72 version" is line 6).**
- 4: narrow vault-spec:39 to "the one file with dated, append-only sections"; Decisions grows as
  one running document. Same wording in `skills/kivna/SKILL.md:315`; `skills/tend/SKILL.md:157`
  already exempts only Weekly, consistent. No test covers it.
- 5: the vault (`~/eolas`, its own git repo, clean) is far staler than a link: Kerd Status's
  newest content is 2026-06-25 (it still describes modes and an architecture redesign), Kerd
  Weekly's newest week is 2026-03-31. Fix link to `[[eolas/Eolas|Eolas]]`; version 0.31.0 →
  drop or update. **Finding:** nothing feeds the vault; Switch Out writes `kivna/sessions/`, not
  Status or Weekly. Anthony believes Kivna records the sessions. Decision at Ready.
- 8: add R5 to `tools/release_check.py`: the README What's New header version equals plugin.json;
  self-test case. Slainte:99 already checks it by hand.
- 9: the law lives in `docs/design/conductor-boundary.md:70-74`; Conductor already links rather
  than restates (spot-check). A phrase-match CI rule would miss paraphrase and false-positive on
  links; recommends no CI rule, keep it in slainte's release pass.

**11:31 "waiting on you" (composer, Opus high; my spot-check: `-CC` control mode, set-titles "#W",
after-rename snapshot hook, no preferredNotifChannel, `[tui]` present in Codex config — confirmed).**
The tmux status bar is never drawn under iTerm2 control mode, and renaming windows would be saved by
the restore snapshot, so neither carries the signal. **Passage A, no Kerd code:** native terminal
bells, iTerm2 marks the tab. Check first that a bell crosses `-CC` to a laptop tab
(`sleep 8; printf '\a'`, switch tab). Then Claude `"preferredNotifChannel": "terminal_bell"` in
`~/.claude/settings.json`; Codex `[tui] notifications = ["agent-turn-complete",
"approval-requested"]`, `notification_method = "bel"`. Limit: a bell means stopped, not "asking
you". **Passage B, only if false bells matter:** a passive Kerd hook (`hooks/waiting-bell.sh`) that
rings on permission prompts and on turns ending in 💬, tested with a fake tmux. Unrun. Also found:
`cc-status` hooks likely update the Studio's own iTerm2, not the laptop (unverified).

**11:31 Agent security (composer, Opus high; my spot-check: guard at agent.py:1205 compares inode
and size only; `codex queue --message framed` at :1162; `'from': 'kerd-agent'` at :464 — confirmed).**
Neither CLI takes a message on stdin or from a file (help text, claude 2.1.282, codex-cli 0.156.1).
The TODO row's "each has a smallest correction on record" was wrong: only 2 and 3 had one.
Correction noted.

## Score (draft, 11:35)

Performed on `concert/backlog-sweep` from `main`. Release 0.155.0 (MINOR). Codex before-push review.

**Part A, Agent security** (one Opus-high player, steps in order, `skills/agent/scripts/agent.py`):
A1 pointer file: full prompt to `.git/kerd-agent/requests/<id>.prompt` (0600, atomic), argv
carries only a pointer (`start()` :1036-1040, `send_codex()` :1162); tests on both fakes. Live
check owed before release: a partner may Read the file under `.git/` (else move to a gitignored
0700 folder). A2 socket peer pid check in `send_claude()` via LOCAL_PEERPID / SO_PEERCRED, refuse
on mismatch; fix MagicMock socket tests. A3 64-byte tail check before the log seek. A4 `from:
kerd-agent:<8 chars of controller id>`, fallback `kerd-agent`. A5 rewrite the limits paragraph in
`native-sessions.md:183-196` to the residuals.

**Part B, skriv pass** (Sonnet-medium players, one per part, no markup changes): B1 README top
matter; B2 guides A (getting-started, conductor, agent); B3 guides B (switch, reference, visuals,
kivna-and-skriv minus its example block, tend-and-slainte); B4 four site pages, text only; B5 release
history: em dashes out, README and CHANGELOG changed identically (default: de-dash only, no
rewrite of history). Check each: dash count 0, release_check clean, no claim added or lost.

**Part C, small fixes** (one Sonnet-medium player): C1 vault-spec:39 and kivna SKILL.md:315 wording;
C2 release_check R5 What's New header = plugin.json version, with self-test; C3 vault (`~/eolas`,
its own repo): link `[[eolas/Eolas|Eolas]]`, drop the stale version line, rewrite Kerd Status from
CONTEXT.md once, add a Weekly entry for this week.

**Part D, waiting on you** (Anthony's config, no Kerd code): D1 bell test on the laptop (his
hands); D2 Claude `preferredNotifChannel: terminal_bell`; D3 Codex `[tui]` bell. Kerd hook only
if false bells bother him.

**Dropped:** item 9 CI rule (too fuzzy; Conductor already links; slainte keeps it).

Goal check: all tests and release_check green; zero em dashes on reader-facing pages; Agent's
residual limits paragraph matches the code; Codex review clear; Anthony sees a bell on a laptop tab.

## Ready (11:36)

View: `build.html` / `build.png` (its "dashes out only" belongs to the release history only; the
rest gets the full voice pass). Risks open: the human-voice pass could change meaning (checked per
part); partners reading a file under `.git/` is untested (live check before release).
**Pending question:** the go to perform this score on `concert/backlog-sweep`, rolling first into
a fresh session (this one is at ~180k), stopping before merge and push.

## Concert (go: Anthony, 2026-09-25 12:50, "go")

Branch `concert/backlog-sweep`, started from `main` at `0bbb4f3`. Records commit 95fa20f
on the branch (not pushed). Approval: perform the score above on this branch, players in parallel,
Codex before-push review, live check that partners can read the message file, release prepared as
0.155.0; Anthony's own Claude/Codex settings files change only after he has seen a bell on a laptop
tab; **stop before merge and push**.

**Next action (exact):** dispatch batch 1 in parallel — Part A (one Opus-high player, steps A1–A5
in order), Part B (five Sonnet-medium players B1–B5), Part C (one Sonnet-medium player C1–C3) —
each with its passage from the Score section; in the same turn, ask Anthony to run the bell test
(D1: on the laptop in a studio tab run `sleep 8; printf '\a'`, switch tabs, look for a bell icon).

**12:55 batch 1 dispatched (after chat roll, chain 3):** A (kerd:opus-high), B1-B5 (kerd:sonnet-medium x5),
C (kerd:sonnet-medium), in parallel, no player commits. D1 bell test asked of Anthony.
**B2 returned 12:5x:** guides A already clean, 0 dashes, no changes (my check: 0 dashes, no diff).
**B1 returned:** README top matter 6 dashes to 0, plugin descriptions clean, release_check clean (my check: 0 in region, diff read).
**B4 returned:** site/index.html 2 dashes to 0, other pages clean, text only (my check: 0 in all four, diff 2 lines).
**B3 returned:** guides B already clean, no changes (my check: 0 dashes, no diff).
**C returned 12:56:** C1 vault-spec and kivna wording narrowed (my check: diff read); C2 R5 added,
release_check clean, selftest 9 ok, run_tests 849 OK (player's reading); C3 vault fixed and committed
in ~/eolas as 862e298, not pushed (my check: commit stat, link line 70). discover-sources.json is
orphaned since lorg's retirement; default: leave the file, link removed.
**A returned 12:57 (Opus high):** A1-A5 done; agent tests 228 OK, run_tests 891 OK (player's
readings). My spot-check: prompt_pointer writes a private file and argv carries only the path;
peer_pid uses LOCAL_PEERPID/SO_PEERCRED; tail stored and compared; sender kerd-agent:<8>.
Player's choices, defaults unless Anthony objects: unknown socket peer is refused; the 8 chars
come from the running session's id (CLAUDE_CODE_SESSION_ID, then CODEX_THREAD_ID). Unverified:
a live partner reading `.git/kerd-agent/requests/*.prompt` (owed, batch 2), --bg sockets' pid,
and whether the receiver accepts the new `from` shape.
**B5 returned 12:58:** release history de-dashed, 2 left per file inside code spans (quoted
labels, correct). **Defect:** B5 restored README lines 1-266 to HEAD, wiping B1's six fixes;
Conductor reapplied them from B1's diff (my check: 0 dashes in top matter, release_check clean).
Lesson: two players on one file must not verify against HEAD.
