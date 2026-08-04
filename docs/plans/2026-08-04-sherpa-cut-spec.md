---
route: new
stage: contracted
---

# The sherpa cut — spec

Kerd's second rip. `skills/sherpa/` is deleted whole. The lifecycle IS the ladder (post-walk decision 4): stages→rungs (gate-checked, not advised), enter-anywhere→gates route by construction, exit tests→gate checks, jump-back→gate re-entry + FATAL ledger rows, the promised `kivna/sherpa.md` expedition log→self-reported position which the derived-from-disk rule forbids (route/stage front matter in `docs/product/` + the progress view replace it), park→state-in-declared-artifacts. The five stage sections are explicit skeletons (Phase 2 never happened). Zero usage ever; `kivna/sherpa.md` never existed on disk (verified). The rigor-rises-ceremony-low principle already survived into the design specs.

**Return condition** (recorded in the What's New entry): a need the gates + progress view cannot answer brings the lifecycle-conductor concept back.

Version: 0.73.0 → **0.74.0** (MINOR — the v0.43.0 GSD-removal and v0.73.0 capturerequirements-cut precedents).

**Composer amendment governs every rewritten passage**: a wrong line does not survive; the no-touch protection is for correct content only. Every replacement below is exact text. If a step's verify does not produce its expected output, or an old string does not match the file, the player STOPS and hands back to the orchestrator. No improvisation.

## The count finding — counts hold at Eleven

The conductor's sweep called for "Eleven workflow skills" → "Ten" and a skills-dir count of 10. Disk disagrees. `skills/` holds **12** directories today (conductor, interrogate, kivna, lorg, mode, pair, sherpa, skriv, slainte, switch, tend, trim); after this cut it holds **11**. Sherpa was never in any count: README line 5 says "Eleven workflow skills" against 12 sections; CLAUDE.md line 3 says "eleven workflow skills" against 12 dirs; the playbook says "Eleven skills" over an 11-line roster that has no sherpa line; and the capturerequirements cut moved all three Twelve→Eleven while the dir count went 13→12 — the same dirs-minus-sherpa arithmetic at both versions. Four independent confirming observations. Deleting sherpa makes every existing "Eleven" literally exact. **Therefore: README line 5, CLAUDE.md, and the playbook are all UNTOUCHED, and the sweep's dir-count criterion is 11, not 10.** Writing "Ten" anywhere would create the wrong line the composer amendment forbids.

## Surface

The diff may touch ONLY these files (plus this spec file itself):

- `skills/sherpa/SKILL.md` (deleted — the directory's only file, confirmed by `ls`)
- `README.md`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `skills/interrogate/SKILL.md`
- `skills/switch/SKILL.md`
- `docs/state-contract.md`

**Deliberately not touched**: `docs/playbook.md` (roster never listed sherpa; "Eleven skills" is correct post-cut — verify-only, step 7), `CLAUDE.md` ("eleven workflow skills", no lifecycle item — correct post-cut), and `tools/diagram/gen_excalidraw.py` / `gen_choose.py` / `gen_flow_celtic_example.py` / `gen_functions.py` — the generators of the dated walk diagrams in `docs/plans/`; their sherpa strings ("unused today", "sherpa may be routed, reshaped or ripped") are the *content of records*, and editing them would falsify the diagrams they regenerate. `tools/diagram/progress.py` (the live renderer) is sherpa-clean.

**Records — never edited**: `kivna/sessions/`, dated `docs/plans/` files (this spec included), the annotations log, README What's New history entries (sherpa records at :62, :66, :74, :78), `Sensei Input/`. **Session state — not spec steps**: `CONTEXT.md` and `TODO.md` mention sherpa; they are the conductor's own close-out updates, excluded from this spec and its surface.

## Pieces

- [x] 1. Rip the skill directory
- [x] 2. README: sherpa section out, What's New 0.74.0
- [x] 3. Manifests: capability lists + triple version bump
- [x] 4. interrogate: exit-bullet repoint
- [x] 5. switch: snapshot comment + pick-list example
- [x] 6. state-contract: snapshot comment
- [x] 7. Counts hold at eleven (verify-only)
- [x] 8. Collateral diff review + sherpa sweep
- [x] 9. Ship

## Steps

All commands run from `/Users/anthonymaley/Kerd`.

### Step 1 — Rip the skill directory [delegate, haiku, low]

First confirm the directory's contents:

```
ls skills/sherpa/
```

Expected: exactly `SKILL.md`. Anything else ⇒ STOP, hand back. Then:

```
git rm -r skills/sherpa
```

**Verify:**

```
test -e skills/sherpa && echo STILL-THERE || echo GONE
git status --short skills/
```

Expected: `GONE`, and `D  skills/sherpa/SKILL.md` as the only `skills/` entry.

### Step 2 — README: sherpa section out, What's New 0.74.0 [delegate, haiku, medium]

Two edits, in this order (Edit A first — Edit B's insertion shifts later line numbers). Line 5's "Eleven workflow skills" is **NOT changed** (see the count finding).

Edit A — delete the whole `### sherpa (Idea→Launch Lifecycle)` section, currently lines 174–185: the heading (174), the three paragraphs ("Sherpa is the lifecycle conductor…" at 176, "Durable state lives in a committed `kivna/sherpa.md`…" at 178, "**Build status:** all five stages are trained…" at 180), the code fence containing `/sherpa` (182–184), and the trailing blank line (185) — so exactly one blank line remains between conductor's closing code fence (the one containing `/conductor`) and `### interrogate (Risk Ledger)`. Pre-check the bounds:

```
sed -n '174p;184p;186p' README.md
```

Expected: `### sherpa (Idea→Launch Lifecycle)`, then a bare ` ``` ` fence line, then `### interrogate (Risk Ledger)`. Any mismatch ⇒ STOP, hand back.

Edit B — What's New. Change line 14 from `## What's New (v0.73.0)` to `## What's New (v0.74.0)`, then insert immediately after it (before `### v0.73.0`):

```

### v0.74.0

**sherpa is cut — a capability you had yesterday is gone.** Yesterday, `/kerd:sherpa` was the lifecycle PM: it walked one idea from spark to launch — Explore → Validate → Plan → Build → Launch across many sessions, rigor rising per stage, with jump-back and park. Today nothing answers that phrase. What replaces it: the ladder does this — the entry gates route each piece of work to its rung and refuse what hasn't earned passage (stages were advice; rungs are checked), the progress view shows position derived from `docs/product/` front matter on disk (never self-reported — which is why the promised `kivna/sherpa.md` expedition log dies with it; it never existed on disk), and the risk ledger qualifies viability, with FATAL rows + gate re-entry covering the jump-back. Rigor-rises-ceremony-stays-low survives in the gate design. Return condition: a need the gates + progress view cannot answer brings the lifecycle-conductor concept back.
```

The existing `### v0.73.0` entry and everything below it (including the sherpa records at :62/:66/:74/:78) are untouched.

**Verify:**

```
sed -n '5p' README.md | cut -c1-30
grep -n "What's New (v0.74.0)" README.md
grep -c '### sherpa' README.md
grep -n 'sherpa' README.md
grep -n '### conductor' README.md
```

Expected: `Eleven workflow skills plus co` (unchanged); a hit at line 14; `0` (grep -c exits 1 on zero matches — that exit code is the pass); every remaining `sherpa` hit at a line number ABOVE the `### conductor (Session Discipline)` heading (i.e. inside What's New entries only — the new v0.74.0 text plus the four history records); zero hits at or below it.

### Step 3 — Manifests: capability lists + triple version bump [delegate, haiku, low]

Both capability lists lose `idea-to-launch lifecycle, ` and stay byte-identical. The one replacement string, used verbatim in BOTH `.claude-plugin/plugin.json` → `description` AND `.claude-plugin/marketplace.json` → `plugins[0].description`:

```
Opinionated workflow toolkit with community-contributed modes: session discipline, session and machine handoff, knowledge management, project audits, human writing voice, structural health, skill discovery, token optimization, risk qualification, conversational pair mode, and workflow routing
```

`metadata.description` in marketplace.json is intentionally a different shape — do not touch it.

Version bump `0.73.0` → `0.74.0` in all three places: `plugin.json` → `version`; `marketplace.json` → `metadata.version`; `marketplace.json` → `plugins[0].version`.

**Verify:**

```
python3 -c "
import json
a=json.load(open('.claude-plugin/plugin.json')); b=json.load(open('.claude-plugin/marketplace.json'))
print(a['description']==b['plugins'][0]['description'])
print(a['version'], b['metadata']['version'], b['plugins'][0]['version'])
print('idea-to-launch' in a['description'] or 'idea-to-launch' in b['plugins'][0]['description'])"
```

Expected:

```
True
0.74.0 0.74.0 0.74.0
False
```

### Step 4 — interrogate: exit-bullet repoint [delegate, haiku, low]

In `skills/interrogate/SKILL.md` (currently line 311, inside the "Does not produce the implementation plan itself" bullet), replace exactly. Old:

```
In a Kerd session that continuation runs through `/kerd:conductor` (this session's build) or `/kerd:sherpa` (the lifecycle walk).
```

New:

```
In a Kerd session that continuation runs through `/kerd:conductor`.
```

The rest of the bullet ("Boundary kept to prevent design synthesis from sneaking in too early.") is untouched. The "(this session's build)" parenthetical goes too — it existed only as contrast with the sherpa alternative.

**Verify:**

```
grep -c 'sherpa' skills/interrogate/SKILL.md; grep -n 'runs through' skills/interrogate/SKILL.md
```

Expected: `0` (exit 1); the rewritten sentence at ~line 311 ending `` runs through `/kerd:conductor`. Boundary kept ``…

### Step 5 — switch: snapshot comment + pick-list example [delegate, haiku, low]

Two edits in `skills/switch/SKILL.md`.

Edit A — line 85, the CONTEXT.md template comment. Old:

```
## Active Mode         — mode/sherpa/conductor snapshot for cross-machine handoff
```

New (spacing before the em-dash preserved exactly):

```
## Active Mode         — mode/conductor snapshot for cross-machine handoff
```

Edit B — line 367, an illustrative pick-list example line naming the dead skill. Old:

```
  1. [Now]      Dogfood sherpa on ~/Bree — mid-lifecycle vs fresh feature
```

New (same indent and column shape; it is illustrative text, any realistic item works — use this one):

```
  1. [Now]      Wire the progress renderer into the entry gate
```

**Verify:**

```
grep -c 'sherpa' skills/switch/SKILL.md
grep -n 'mode/conductor snapshot' skills/switch/SKILL.md
grep -n 'Wire the progress renderer' skills/switch/SKILL.md
```

Expected: `0` (exit 1); a hit at ~85; a hit at ~367.

### Step 6 — state-contract: snapshot comment [delegate, haiku, low]

In `docs/state-contract.md` line 22, the same fix as step 5 Edit A. Old:

```
## Active Mode         — mode/sherpa/conductor snapshot for cross-machine handoff
```

New:

```
## Active Mode         — mode/conductor snapshot for cross-machine handoff
```

**Verify:**

```
grep -c 'sherpa' docs/state-contract.md; grep -n 'mode/conductor snapshot' docs/state-contract.md
```

Expected: `0` (exit 1); a hit at ~22.

### Step 7 — Counts hold at eleven (verify-only) [delegate, haiku, low]

No edit. This step pins the count finding to disk after the rip:

```
ls skills/ | wc -l
grep -c 'sherpa' docs/playbook.md
grep -n 'Eleven skills' docs/playbook.md
sed -n '5p' README.md | cut -c1-6
grep -n 'eleven workflow skills' CLAUDE.md
```

Expected: `11`; `0` (exit 1 — the playbook roster never listed sherpa); a hit at ~61; `Eleven`; a hit at line 3. Any other outcome ⇒ STOP, hand back — the count reasoning is broken and the composer must re-decide before anything ships.

### Step 8 — Collateral diff review + sherpa sweep [keep]

Deletion blast radius check. Three parts, all must pass.

Part A — the diff touches nothing outside the surface:

```
git add -A -n; git status --short
```

Expected changed paths, exactly and only: `skills/sherpa/SKILL.md` (D), `README.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `skills/interrogate/SKILL.md`, `skills/switch/SKILL.md`, `docs/state-contract.md`, this spec file (`docs/plans/2026-08-04-sherpa-cut-spec.md`, new) — plus possibly `CONTEXT.md`/`TODO.md` if the conductor has begun close-out (session state, never staged with this commit). Any other path ⇒ FAIL, hand back.

Part B — no live doc still references the dead skill:

```
grep -rni 'sherpa' . --exclude-dir=.git
```

PASS iff every remaining hit is a record or session state: `kivna/sessions/` logs; dated `docs/plans/` files (this spec included) and the annotations log; README What's New entries (all hits above the `### conductor` heading); the four `tools/diagram/` record-generators (`gen_excalidraw.py`, `gen_choose.py`, `gen_flow_celtic_example.py`, `gen_functions.py` — sources of the dated walk diagrams; their sherpa strings are record content); `Sensei Input/`; `CONTEXT.md`/`TODO.md` (conductor's close-out cleans these). Any hit in `skills/`, `modes/`, `hooks/`, `docs/playbook.md`, `docs/state-contract.md`, `docs/vault-spec.md`, `CLAUDE.md`, `.claude-plugin/`, `tools/gates/`, `tools/diagram/progress.py`, or README at/below `### conductor` ⇒ FAIL: hand the hit back to the orchestrator — do not improvise a fix.

Part C — the skills directory holds eleven:

```
ls skills/ | wc -l
```

Expected: `11`.

### Step 9 — Ship [keep]

1. Run the full local gate — the same four checks CI enforces. All must exit 0; any failure ⇒ hand back, do not ship:

```
python3 tools/gates/gate.py selftest
python3 tools/gates/gate.py audit
python3 tools/gates/gate.py release
python3 tools/diagram/progress.py selftest
```

2. Stage by name. The `skills/sherpa` deletion is ALREADY STAGED by step 1's `git rm` — do NOT `git add` the deleted path (it no longer exists on disk; adding it would error):

```
git add README.md .claude-plugin/plugin.json .claude-plugin/marketplace.json skills/interrogate/SKILL.md skills/switch/SKILL.md docs/state-contract.md docs/plans/2026-08-04-sherpa-cut-spec.md
```

3. Commit with piece trailers (conductor appends its own session trailer per its conventions). Trailers cover pieces 1–8 only: a commit cannot witness its own landing, so `Piece: sherpa-cut/9` is explicitly assigned to the follow-up render-refresh commit (the progress-view re-render that follows the ship) — the previous cut hit exactly this:

```
Cut sherpa: the lifecycle is the ladder (v0.74.0)

The skill is deleted whole — the second rip. Its five stages were
explicit skeletons; zero usage; kivna/sherpa.md never existed on disk.
What it promised, the ladder now does: the entry gates route and refuse
by construction, the progress view derives position from disk, the risk
ledger qualifies viability, FATAL rows + gate re-entry cover jump-back.
README, both capability lists, interrogate, switch and state-contract
re-point; the counts stay Eleven (sherpa was never counted); What's New
names the cut as a loss and records the return condition.

Piece: sherpa-cut/1
Piece: sherpa-cut/2
Piece: sherpa-cut/3
Piece: sherpa-cut/4
Piece: sherpa-cut/5
Piece: sherpa-cut/6
Piece: sherpa-cut/7
Piece: sherpa-cut/8
```

4. Push:

```
git push
```

**Verify:** all four gate commands exit 0; after commit, `git status --short` shows nothing staged and no surface file modified (only `CONTEXT.md`/`TODO.md` may remain dirty — session state, committed later by switch); push accepted by remote; `git log --oneline -1` shows the cut commit.
