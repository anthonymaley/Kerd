# First real Conductor session on 0.111.0: the Backlog closure review — 2026-09-12

The owed proof from TODO `## Now`: one real Conductor session on the current
release, confirming a Claude player is dispatched as a native subagent rather
than through `ask.py`. Observed at dispatch, 09:41 EDT: the player ran through
the host's Agent tool as a background subagent (requested Opus 5, effort high;
identity requested, not observed), read-only, and returned this result at
09:49. No `ask.py` call, no fresh CLI. That is the dispatch proof; the result
below is the player's, verbatim, and is information for the next Switch Out,
which acts on verdicts. Nothing has been moved yet.

Note on authority: the session was opened on a typed "approve" that turned
out to be meant for a held Codex peer request, not for this NOW bullet. The
job was read-only and owed, so it ran to completion; the misreading is
recorded here rather than hidden.

---

Closure review complete. Here is the full result.

---

# Backlog closure review — TODO.md `## Backlog`, 73 rows
Repo `/Users/anthonymaley/development/product/Kerd`, branch `main`, HEAD `b139519`, Kerd 0.111.0. Read-only; nothing edited.

## 1. Summary

**done 3 · dead 8 · open 60 · unsure 2**

## 2. Verdicts, in Backlog order

| # | Row (first ~8 words, verbatim) | Group | Verdict | Evidence |
|---|---|---|---|---|
| 1 | `inline-composer` at handoff — spec unwritten; its intended | Ladder | open | `gate.py route inline-composer` → `enters at: handoff`, missing for loop: `docs/plans/*-inline-composer-spec.md`; `gate-reachability` still `enters at: viability` |
| 2 | `hooks-autoload` at viability — the sibling legacy closure | Ladder | open | `gate.py route hooks-autoload` → `enters at: viability`; scope blocked on row 1 Treatment evidence empty |
| 3 | `funnel-driver` + `progress-html` at acceptance, 0 Pieces each | Ladder | open | `progress-html` → `enters at: acceptance` (owes the record); **premise stale** — `funnel-driver` now → `enters at: viability` (FATAL row 4 + empty Treatment evidence), not acceptance |
| 4 | `requirements-traceability` and `shared-memory` at design — blocked | Ladder | open | **premise stale** — both now → `enters at: viability` (Treatment evidence empty: 1 row / 3 rows), not design |
| 5 | A FATAL row is told to file into "What we ruled out" | Ladder | open | Still live verbatim at `CONTEXT.md:78` `## Open Questions` |
| 6 | **Agent's four disclosed-not-built limits** (Fable foundation review | High | open | All four still stated as limits at `skills/agent/references/native-sessions.md:129-142`; no correction in `skills/agent/scripts/agent.py` |
| 7 | **A derived question set needs source-bound invalidation plus** | High | open | `docs/product/question-set-staleness.md` exists (framed, `85b8683`); `gate.py route` → `enters at: viability`, `scope need 13` |
| 8 | **`Impact` and `Likelihood` are risk-ledger columns that nothing** | High | open | `tools/gates/kit.py:63` declares both in `LEDGER_COLUMNS`; `parse_ledger` (`kit.py:534-560`) checks only Risk evidence / Severity / Treatment / Countermeasure / Review trigger / Treatment evidence |
| 9 | **THIS ROW IS NOW THE PILOT FOR `requirements-success-measurement`** | High | open | No stage-vs-route AU rule (`_audit_au1`…`_audit_au10`, `kit.py:1109-1580`). Re-measured today: `hooks-autoload` `scoped` vs derived viability; `model-effort-advisory` `scoped` vs derived design; **`funnel-driver` `designed` vs derived viability** — a 3-rung overclaim, worse than the recorded 1 |
| 10 | **Drive invented a risk-state value rather than refusing** | High | open | Schema half confirmed answered — `kit.py:541,547` refuse empty cells with *"named, not yet qualified; qualify at viability"*. Drive's half unbuilt: `grep -n "cannot fill\|refuse to write" skills/drive/SKILL.md` empty |
| 11 | **The composer emits hard-coded absolute repository paths, and** | High | dead | Composer removed at 0.107.0 — `grep -rni composer skills/` empty (`21e6779`). Artifact half verified fixed: 0 `/Users/anthonymaley`, 21 `rev-parse --show-toplevel` in `docs/plans/2026-09-01-requirements-success-measurement-spec.md` |
| 12 | **`grep -c` in a fail-fast verify chain fails exactly** | High | dead | Same removal (`21e6779`). Artifact half fixed: spec `:1052` uses `test … -eq 0`; the clause itself sits in the spec body at `:121` |
| 13 | **A spec writes the CONSEQUENCE of an open question as settled** | High | dead | Same removal (`21e6779`). Artifact half fixed by `528ca88`; cross-step invalidation now marked at spec `:182` and `:1139` |
| 14 | **Waiver and legacy-closure records are named exactly like GO** | High | open | `docs/gates/waivers/2026-09-02-switch-fidelity-design.md` and `docs/gates/closures/2026-09-02-model-effort-advisory-design.md` unrenamed; `GATE_RECORD_RE` (`kit.py:124`) unchanged; `tests/` holds only `hooks_test.sh` — no refusal test |
| 15 | **The three composer-brief clauses need a DURABLE home in** | High | dead | Its named home is gone: `skills/conductor/SKILL.md:226-249` "Calling the composer" no longer exists (that range is now "Record agreement and carry the work forward"); `grep -rni composer skills/` empty. Intent survives — successor surface is `skills/conductor/references/execution.md:45-50` |
| 16 | **The suspect-link stamp has no slot in the requirement format** | High | open | Mechanism described at `docs/requirements/catalog.md:208-216`; `docs/requirements/register.md` carries no stamped link and no reverse edge |
| 17 | **An observed result binds to its METHOD by bare reference** | High | open | No `Method-SHA256` anywhere in the tree; row's own producer boundary bars it from that slice |
| 18 | **A visual of where the whole process build-out stands** | High | open | `python3 tools/diagram/progress.py` still prints `!! 1 text/text overlap(s)` (now at 5284,250; row records 4594,250); no artifact answers reading (b) |
| 19 | **Rule 9 has two implementations and nothing tests them** | High | open | `tools/reqview/fingerprint.py` and `tools/reqview/reqview.py` both present; `tests/` holds only `hooks_test.sh` |
| 20 | **`tools/diagram/gen_kerd_map.py:107` says `audit AU1-AU8` — stale** | High | open | `gen_kerd_map.py:107` `audit AU1-AU8` and `:110` `CI - eight steps`; `kit.py:1619` runs AU1–AU10 and `.github/workflows/gate.yml` has 9 steps |
| 21 | **A fold has no closing check, and three enumerated sweeps** | High | open | No fold check in `gate.py` or the AU set; only `kit.py:3063` T45 rung-name purity assertion, which the row already excludes |
| 22 | **A work item can reach acceptance having declared no measurable** | High | open | No stage-1/"Named answers" check anywhere in `tools/gates/kit.py`; the named likely home `requirements-success-measurement` is still at viability |
| 23 | **`fidelity.py`'s range and its reader set disagree** | High | open | `tools/gates/fidelity.py:81` `newest_log()` and `:103` `--diff-filter=A` both unchanged |
| 24 | ~~**THREE sealed views are factually stale.**~~ **CLOSED 2026-08-29.** | High | **done** | `71391f8` exists; `docs/product/gate-visuals.md:8` `fp:c4f3e8949191` and `:12` `fp:d210312a9bec` are the resealed values the row names |
| 25 | **`docs/design/diagram-types-by-rung.md` is still organised by** | High | open | `### BUILD` `:134`, `### GOAL` `:139`, `### LOOP` `:148` — the fold never happened |
| 26 | **Two diagram generators still name the `build` rung.** | High | open | `tools/diagram/gen_flow_build.py` still present; `gen_functions.py:54` and `:646` both `("BUILD", [` |
| 27 | **The `design` gate can check nothing — and as of 2026-08-25** | High | open | `kit.py:896-898` states it verbatim in its own comment: *"a work item declaring no concerns passes design vacuously"* |
| 28 | **`## Release condition` will collide with the release-planning** | High | open | The release-planning artifact still does not exist; `## Release condition` live at `docs/design/rung-vocabulary.md:40` |
| 29 | **`## Grounding` cannot cite an external source.** Found 2026-08-23 | High | open | `_audit_au5` (`kit.py:1241-1272`) resolves each ref by `glob.glob` against disk; no URL branch, no in-line symbol resolution |
| 30 | **Diagram-and-prose-together: flip the default in the skills.** | High | open | `view: n/a — <reason>` refusal exists in `kit.py`/`tools/gates/README.md:453`; `grep -rn "view: n/a" skills/` empty — no skill default flipped |
| 31 | **Standards grounding — second pass.** The spike | High | open | `docs/design/standards-grounding-findings.md` last touched at `33e2753`; 82079-1 / 25040 / 24748 still listed surfaced-not-read |
| 32 | **The conductor marker cannot carry a sitting's open time** | High | **dead** | The marker was removed at 0.107.0 (`21e6779`): `grep -rn "conductor:" skills/conductor/SKILL.md` and `grep -rn "active-modes" skills/switch/SKILL.md` both empty; `docs/state-contract.md:11` records the removal |
| 33 | ~~**Verify hooks auto-load fires on this machine.**~~ **CLOSED** | High | **done** | `hooks/hooks.json` present; `hooks/session-start.sh` builds the string; row's three observations stand. *Sub-finding still open:* `docs/product/hooks-autoload.md`'s ledger and acceptance test are uncorrected, and the item still enters at viability |
| 34 | **`gate.py --root` — the CLI half shipped 2026-08-14** | High | open | `grep -rn -- "--root" skills/ hooks/` returns nothing — no consumer calls it |
| 35 | **Hookify — promoted to a dependency.** `OPS-001` | High | open | hookify installed at `~/.claude/plugins`; zero references in Kerd outside TODO and session logs; `OPS-001` live at `docs/requirements/register.md:486` |
| 36 | **Requirement archaeology over CONTEXT.md's 74 standing decisions.** | High | open | Never run. Corpus moved and grew: 158 entries now in `docs/decisions.md` (0.111.0 rulings/cases split), not CONTEXT.md |
| 37 | **The release-planning artifact.** Gained two inputs today | High | open | No such artifact under `docs/` |
| 38 | **Frame switch-fidelity slice 2 — capture human input.** | High | open | Gaps 10/11/12 still described at `docs/product/switch-fidelity.md:209-223`; no slice-2 frame; design rung waived 2026-09-02 |
| 39 | **The fidelity check** (accepted unknown; review trigger already | High | open | `tools/gates/fidelity.py` proves file reachability only, as the row states |
| 40 | **boundary-cycle, in-half** — the reset ritual's automation. | High | open | No product or design doc; still named as a backlog item at `docs/product/conductor-boundary.md:72` |
| 41 | **Plugin cache repin debt.** Reopened by v0.95.0 | High | open | `TODO.md ## Now` still carries "Confirm the plugin cache picks up 0.111.0 on an ordinary startup" |
| 42 | **Machine-local state has an inventory but no refuser** | High | open | `docs/machine-setup.md` present; `skills/tend/SKILL.md` still has 9 categories, none running its greps |
| 43 | **Stashes and local-equals-remote are unchecked at the boundary.** | High | open | `skills/switch/SKILL.md` (94 lines) has no fetch/push/containment check — `grep -n "push\|remote\|fetch\|contains"` hits only `:55`; `~/eolas/vault/kerd/bin/boundary-check` still outside the repo |
| 44 | **The playbook's `## Current Status` duplicates CONTEXT.md.** | High | open | `docs/playbook.md:618` `## Current Status` still present |
| 45 | **Out-of-repo artifacts have no home** — PRs, URLs, decks | High | open | No mechanism anywhere; nothing has changed |
| 46 | **Stop-hook over-prescription**: distinguish work-dirty from | High | **dead** | `hooks/stop.sh` deleted at v0.96.0 — `2146925` "Ship hooks via plugin auto-load; cut stop.sh"; `hooks/` now holds pair, session-start, skill-complete, statusline only |
| 47 | **A `## Risk ledger` section parses PROSE as rows** | Medium | open | `kit.py:529-533` still enumerates every non-empty body line as a row |
| 48 | **`CONTEXT.md`'s 2026-08-25 bullet labels both risk checks one rung** | Medium | open | The bullet moved to `docs/decisions.md:287` (0.111.0 case migration) with the wording *"viability requires killer risks named … scope requires every row qualified"* unchanged |
| 49 | **README's `## What's New (vX)` header is a second home** | Medium | open | `README.md:43` `## What's New (v0.111.0)` sits above `### v0.111.0` at `:45` — the two homes persist |
| 50 | **Five citation/count slips in the `gate-visuals` acceptance record** | Medium | open | `docs/gates/2026-08-30-gate-visuals-acceptance.md:253-254` (`:111`/`:253` drift) and `:356` (`fp:2c5fd12e53c6`) unchanged |
| 51 | **`docs/playbook.md:391`'s cold-eyes trap names the wrong tool** | Medium | open | Line moved to `docs/playbook.md:529`, text unchanged; `tools/design/matrix.py` still references `kit.ROOT` 10 times |
| 52 | **`gate.py`'s root resolver walks OUT of a git worktree** | Medium | open | `tools/gates/gate.py:106` still `os.path.isdir(os.path.join(cur, ".git"))` — a worktree's `.git` file still fails the test |
| 53 | **`docs/design/kerd-map.svg` still draws NINE skills** | Medium | open | `gen_kerd_map.py:35` "THE NINE SKILLS"; `skills/` now holds **twelve** dirs, so the drift widened by three |
| 54 | **skriv bans em dashes; the README's What's New voice uses them** | Medium | open | `skills/skriv/SKILL.md:54` bans em dashes; README's v0.111.0 entry uses them — no ruling recorded |
| 55 | **The refusal surface does not travel with the plugin — the return** | Medium | open | Interlocked with row 34, which is confirmed unbuilt (`--root` uncalled by any skill or hook) |
| 56 | **`docs/vault-spec.md` contradicts itself** (found by tend | Medium | open | `:39` "the one append-style file in the vault" vs `:78`/`:88` decisions files "Updated when new decisions are made" — unresolved |
| 57 | **Three vault-spec violations, all kivna's to fix** | Medium | open | `~/eolas/vault/kerd/Kerd.md:72` still `[[eloas/Eloas\|Eloas]]`; `discover-sources.json` still in the vault folder. *Sub-finding done:* `2026-08-02-product-to-build.excalidraw` is no longer in the vault folder |
| 58 | **Revisit the journey view when more data exists** (parked | Medium | open | Parked with a return condition; no evidence it fired |
| 59 | Clean krutho-strategy's stray `sessions-of-record/`. | Medium | **done** | `find /Users/anthonymaley/development/work/krutho-strategy -maxdepth 4 -name "sessions-of-record*"` returns nothing; the directory is gone |
| 60 | AGENTS.md needs its own verdict: gitignored, machine-local | Medium | **unsure** | No `AGENTS.md` in this tree, but `.gitignore:7` lists it, so its absence here is expected and proves nothing about the other machine |
| 61 | Regenerate the choose-what-matters view before its next use. | Medium | open | `docs/plans/2026-08-03-choose-what-matters-view.excalidraw` is still the Backlog preamble's cited ranking artifact and is unregenerated |
| 62 | Hook version staleness check in `/kerd:tend`. | Medium | **dead** | Its reason is gone: `skills/tend/SKILL.md:207` — *"it never version-rots, because there is no cached version path to go stale"* (v0.96.0, `2146925`); row 41 records the same narrowing |
| 63 | PR-event edge in the stale CI step (unexercised; no PR flow). | Medium | open | `.github/workflows/gate.yml:2` `on: [push, pull_request]`; still no PR flow to exercise it |
| 64 | Guard switch-in step 3 smoke test against context bloat. | Medium | **dead** | Switch was replaced at 0.107.0 (`21e6779`); `skills/switch/SKILL.md` is 94 lines with four prose sections, no numbered steps; `grep -rn "smoke" skills/switch/` empty |
| 65 | **lorg-cut candidate** — evidence check per the rip discipline | Medium | open | `skills/lorg` and `skills/interrogate` both still shipped; no evidence check on record |
| 66 | **kivna verdict** — same zero-usage smell as the vault | Medium | open | `skills/kivna` still shipped; no ruling in `docs/decisions.md` |
| 67 | **CI rule for the single-definition law** — nothing machine-enforces | Medium | open | None of gate.yml's 9 steps checks it. Narrowed, not dead: conductor stopped invoking Switch Out at 0.107.0 (`docs/playbook.md:78`), so the specific re-description it names is less likely |
| 68 | Derive the rigor refusal messages from `RIGOR_LEVELS` via join. | Medium | open | `kit.py:378` still hard-codes `"(legal: spike, mvp, production-v1)"` beside `RIGOR_LEVELS` at `:90` |
| 69 | Gate records can only say GO: a refused gate has no dated home. | Medium | open | Restated as live at `docs/playbook.md:190`; `docs/gates/` has `waivers/` and `closures/` but still no refusal home |
| 70 | `CHANGELOG.md` stale at 0.14.0 while the repo is at 0.95.0 | Low | open | `CHANGELOG.md:3` `## 0.14.0`; repo at 0.111.0; `CLAUDE.md`'s release checklist still omits it (the gap widened by 16 releases) |
| 71 | Stale `Kerd.md` MOC version field (says 0.31.0). | Low | open | `~/eolas/vault/kerd/Kerd.md:6` `**Version:** 0.31.0` |
| 72 | Consider promoting the refined question-formation rule from the pair | Low | **unsure** | `~/.claude/CLAUDE.md:70` has a "Question-formation gate", but it bans multiple-choice outright while `hooks/pair.sh:16` permits it — a global rule exists and *contradicts* the hook rather than being it promoted |
| 73 | skriv voice profile wiring — needs non-founder-genre samples. | Blocked | open | `grep -rn "voice profile" skills/skriv/` empty; the return condition (non-founder-genre samples) has not fired |

## 3. Needs a decision — the 2 unsure rows

- **#60 — AGENTS.md needs its own verdict.** One check settles it: run `ls -la AGENTS.md` on the MacBook (and any other machine that has held this repo). The file is gitignored (`.gitignore:7`), so it cannot be seen from here; if it is absent everywhere the row is dead, if it is present anywhere it needs the verdict it asks for.
- **#72 — promote the question-formation rule into global CLAUDE.md.** One check settles it: decide whether `~/.claude/CLAUDE.md:70-83`'s ban on multiple-choice *is* the promotion asked for, or whether the pair hook's permissive wording at `hooks/pair.sh:16` should be brought into line with it. The two now disagree in substance, which is either a completed promotion plus a new drift row, or an incomplete one.

## 4. What I did not check

- **`## Now` and the "Earlier launch sequence" block** (TODO.md lines 1-50) — out of scope by the brief; the launch-sequence items are only cross-referenced where a Backlog row points at them.
- **Rows already in `docs/backlog-archive.md`** (the close-out double-write row and the switch-in-cost row) — closed 2026-09-11, not re-verdicted per the brief.
- **Whether the artifact-half fixes in rows 11–13 are *correct***, only that they are present. I verified path counts, the exit-safe count and the cross-step dependency markers exist; I did not re-run the spec's verify chains.
- **The other machine's state** — the laptop's `AGENTS.md`, any `kivna/.active-modes` there, and anything under `~/eolas` that this session cannot observe read-only from the Mac Studio. `boundary-check` was confirmed to exist but not executed.
- **Row 33's sub-finding** (`docs/product/hooks-autoload.md`'s stale ledger and its acceptance test's case mismatch) — I confirmed the item still enters at viability but did not grep the acceptance test's exact literal.
- **Whether any row's subject moved into `docs/work/` records** created by the new Conductor — `docs/work/release-111-followup/` is untracked in git status and I did not read it, since untracked scratch is not evidence of closure.

One cross-cutting observation worth flagging: `docs/state-contract.md:126` still points at *"`skills/switch/SKILL.md` step 3 (single-definition law)"*, and that step no longer exists after the 0.107.0 rewrite. That is not a Backlog row, so I have not verdicted it, but it is the same class several rows describe.
