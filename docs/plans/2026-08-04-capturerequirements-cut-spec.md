---
route: new
stage: contracted
---

# The capturerequirements cut — spec

Kerd's first true rip. `skills/capturerequirements/` is deleted whole. Its job — pinning what a piece of work must do before building — moves to the frame flow: the `Value` and `Release slice` sections of `docs/product/<slug>.md`, with everyday-tier work filling the `Risk ledger` in the same framing conversation (v0.72.0). Section names are verified against the gate table in `tools/gates/README.md` (rungs `viability` → `Value`, `slice` → `Risk ledger`, `design` → `Release slice`).

Version: 0.72.0 → **0.73.0** (MINOR — the v0.43.0 GSD-removal precedent).

**Composer amendment governs every rewritten passage**: a wrong line does not survive; the no-touch protection is for correct content only. Every replacement below is exact text. If a step's verify does not produce its expected output, or an old string does not match the file, the player STOPS and hands back to the orchestrator. No improvisation.

## Surface

The diff may touch ONLY these files (plus this spec file itself):

- `skills/capturerequirements/SKILL.md` (deleted — the directory's only file, confirmed by `ls`)
- `modes/jit.md`
- `README.md`
- `CLAUDE.md`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `docs/playbook.md`
- `skills/kivna/SKILL.md`
- `skills/sherpa/SKILL.md`

**Records — never edited**: `kivna/sessions/`, dated `docs/plans/` files, the annotations log, README What's New history entries (README.md ~:70 sherpa-training entry, ~:86 v0.43.0 entry). **Session state — not spec steps**: `CONTEXT.md:5` and `TODO.md:18` are the conductor's own close-out updates; they are excluded from this spec and from the surface list above.

**Sherpa note**: sherpa is itself decision-CUT (post-walk decision 4) but its rip is not licensed yet — sherpa survives this build. Step 8 is a minimal repoint only, licensed because a dangling reference is a wrong line.

## Pieces

- [x] 1. Rip the skill directory
- [x] 2. jit re-points at the frame flow
- [x] 3. README: count, section removal, What's New 0.73.0
- [x] 4. CLAUDE.md capability line
- [x] 5. Manifests: capability lists + triple version bump
- [x] 6. Playbook: count + roster line
- [x] 7. kivna: intake parenthetical
- [x] 8. sherpa: Build-stage repoint
- [x] 9. Collateral diff review + trigger-phrase sweep
- [x] 10. Ship

## Steps

All commands run from `/Users/anthonymaley/Kerd`.

### Step 1 — Rip the skill directory [delegate, haiku, low]

Do:

```
git rm -r skills/capturerequirements
```

Verify:

```
test -e skills/capturerequirements && echo STILL-THERE || echo GONE
git status --short skills/
```

Expected: `GONE`, and `D  skills/capturerequirements/SKILL.md` as the only `skills/` entry.

### Step 2 — jit re-points at the frame flow [delegate, haiku, low]

Two edits in `modes/jit.md`.

Edit A — delete this line from `core_skills` (currently line 7):

```
  - kerd:capturerequirements
```

Edit B — replace the Reqs step (currently line 27). Old:

```
- [x] `/kerd:capturerequirements` -- interview to lock MVP must-haves, defer the rest
```

New:

```
- [x] Frame the work -- declare the `Value` and `Release slice` sections of `docs/product/<slug>.md`; everyday-tier work fills the `Risk ledger` in the same conversation
```

Verify:

```
grep -c 'capturerequirements' modes/jit.md; grep -n 'Release slice' modes/jit.md
```

Expected: `0` (grep -c exits 1 on zero matches — that exit code is the pass), and one hit on the new Frame-the-work line in the `## Requirements` section.

### Step 3 — README: count, section removal, What's New 0.73.0 [delegate, haiku, medium]

Three edits in `README.md`.

Edit A — line 5, count claim. Old (line starts): `Twelve workflow skills plus community-contributed modes` → New: `Eleven workflow skills plus community-contributed modes` (rest of line untouched).

Edit B — delete the whole `### capturerequirements (Requirements Capture)` section, currently lines 195–204: the heading, both paragraphs ("Capturerequirements is the fast, interview-based front door…" and "Use interrogate when the cost of being wrong is high…"), the code fence containing `/kerd:capturerequirements      # interview to lock MVP must-haves`, and the trailing blank line — so exactly one blank line remains between interrogate's closing code fence and `### switch (Session Handoff)`.

Edit C — What's New. Change line 14 from `## What's New (v0.72.0)` to `## What's New (v0.73.0)`, then insert immediately after it (before `### v0.72.0`):

```

### v0.73.0

**capturerequirements is cut — a capability you had yesterday is gone.** Yesterday, saying "capture requirements" got you a fast one-question-at-a-time interview that pinned MVP must-haves into `docs/requirements/`. Today nothing answers that phrase. What replaces it: the frame flow — you declare the work's `Value` and `Release slice` sections in `docs/product/<slug>.md`, and everyday-tier work fills the `Risk ledger` in the same framing conversation (v0.72.0) — so requirements live where the entry gates read them instead of in a side note. jit's Reqs step now points there. Existing notes under `docs/requirements/` stay where they are; nothing writes new ones.
```

The existing `### v0.72.0` entry and everything below it (including the records at ~:70 and ~:86) are untouched.

Verify:

```
sed -n '5p' README.md | cut -c1-30
grep -n "What's New (v0.73.0)" README.md
grep -c '### capturerequirements' README.md
grep -n 'capturerequirements' README.md
```

Expected: `Eleven workflow skills plus co`; a hit at line 14; `0` (exit 1); remaining `capturerequirements` hits ONLY inside `### v0.x.y` What's New entries (the new v0.73.0 text plus the ~:70 and ~:86 records) — zero hits anywhere else.

### Step 4 — CLAUDE.md capability line [keep]

The conductor holds CLAUDE.md in context and edits it itself. Replace line 3 whole. Old:

```
Claude Code plugin: twelve workflow skills plus community-contributed modes for session discipline, plan readiness, requirements capture, machine handoff, knowledge management, project audits, human writing voice, structural health, skill discovery, token optimization, conversational pair mode, and workflow routing.
```

New:

```
Claude Code plugin: eleven workflow skills plus community-contributed modes for session discipline, plan readiness, machine handoff, knowledge management, project audits, human writing voice, structural health, skill discovery, token optimization, conversational pair mode, and workflow routing.
```

Verify:

```
grep -c 'requirements capture' CLAUDE.md; grep -n 'eleven workflow skills' CLAUDE.md
```

Expected: `0` (exit 1), then a hit at line 3.

### Step 5 — Manifests: capability lists + triple version bump [delegate, haiku, low]

Both capability lists lose `requirements capture, ` and stay byte-identical. The one replacement string, used verbatim in BOTH `.claude-plugin/plugin.json` → `description` AND `.claude-plugin/marketplace.json` → `plugins[0].description`:

```
Opinionated workflow toolkit with community-contributed modes: session discipline, session and machine handoff, knowledge management, project audits, human writing voice, structural health, skill discovery, token optimization, risk qualification, idea-to-launch lifecycle, conversational pair mode, and workflow routing
```

`metadata.description` in marketplace.json is intentionally a different shape — do not touch it.

Version bump `0.72.0` → `0.73.0` in all three places: `plugin.json` → `version`; `marketplace.json` → `metadata.version`; `marketplace.json` → `plugins[0].version`.

Verify:

```
python3 -c "
import json
a=json.load(open('.claude-plugin/plugin.json')); b=json.load(open('.claude-plugin/marketplace.json'))
print(a['description']==b['plugins'][0]['description'])
print(a['version'], b['metadata']['version'], b['plugins'][0]['version'])
print('requirements capture' in a['description'] or 'requirements capture' in b['plugins'][0]['description'])"
```

Expected:

```
True
0.73.0 0.73.0 0.73.0
False
```

### Step 6 — Playbook: count + roster line [delegate, haiku, low]

Two edits in `docs/playbook.md`.

Edit A — line 61. Old: `**Twelve skills, each with a single responsibility, plus four opt-in hooks:**` → New: `**Eleven skills, each with a single responsibility, plus four opt-in hooks:**`

Edit B — delete line 64 whole:

```
- **capturerequirements**: requirements capture (fast MVP-must-have interview, jit front door)
```

Verify:

```
grep -n 'Eleven skills' docs/playbook.md; grep -c 'capturerequirements' docs/playbook.md
```

Expected: a hit at line 61; `0` (exit 1).

### Step 7 — kivna: intake parenthetical [delegate, haiku, low]

In `skills/kivna/SKILL.md` (currently line 255), replace exactly. Old:

```
This is the opposite of `/kerd:capturerequirements`, which drills one question at a time — intake is *seeding*, not *deciding*, so it batches.
```

New:

```
Intake is *seeding*, not *deciding*, so it batches rather than drilling one question at a time.
```

Verify:

```
grep -c 'capturerequirements' skills/kivna/SKILL.md; grep -n 'seeding' skills/kivna/SKILL.md
```

Expected: `0` (exit 1); the rewritten sentence at ~line 255.

### Step 8 — sherpa: Build-stage repoint [delegate, sonnet, low]

Sherpa survives this build (its own rip is not yet licensed) — this is a minimal repoint of one dangling reference, nothing else. In `skills/sherpa/SKILL.md`, locate the Build-stage line (currently line 245) with:

```
grep -n 'kerd:capturerequirements' skills/sherpa/SKILL.md
```

Expected: exactly one hit, an instruction of the shape "Use `/kerd:capturerequirements` to pin …". In that line only, replace the token:

```
`/kerd:capturerequirements`
```

with:

```
the frame flow (the `Value` and `Release slice` sections of `docs/product/<slug>.md`)
```

Read the resulting sentence back and confirm it parses as correct prose (expected shape: "Use the frame flow (…) to pin …"). If the surrounding grammar breaks, adjust ONLY that sentence, minimally. If the grep shows zero or multiple hits, or the line is not that shape, STOP and hand back.

Verify:

```
grep -c 'capturerequirements' skills/sherpa/SKILL.md; grep -n 'Release slice' skills/sherpa/SKILL.md
```

Expected: `0` (exit 1); one hit on the repointed Build-stage line at ~245.

### Step 9 — Collateral diff review + trigger-phrase sweep [keep]

Deletion blast radius check. Two parts, both must pass.

Part A — the diff touches nothing outside the surface:

```
git add -A -n; git status --short
```

Expected changed paths, exactly and only: `skills/capturerequirements/SKILL.md` (D), `modes/jit.md`, `README.md`, `CLAUDE.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `docs/playbook.md`, `skills/kivna/SKILL.md`, `skills/sherpa/SKILL.md`, and this spec file (`docs/plans/2026-08-04-capturerequirements-cut-spec.md`, new). Any other path ⇒ FAIL, hand back.

Part B — no live doc still references the dead skill, by name OR by user utterance:

```
grep -rni -e 'capturerequirements' -e 'capture requirements' . --exclude-dir=.git --exclude-dir=kivna
```

PASS iff every remaining hit is a record: README What's New version entries (the new v0.73.0 text and the history entries at ~:70 and ~:86), dated `docs/plans/` files (this spec included), or the annotations log. Any hit in `skills/`, `modes/`, `docs/playbook.md`, `CLAUDE.md`, `.claude-plugin/`, `tools/`, `hooks/`, or README outside What's New ⇒ FAIL: hand the hit back to the orchestrator — do not improvise a fix. (`kivna/sessions/` records are excluded by the command itself.)

### Step 10 — Ship [keep]

1. Run the full local gate — the same checks CI enforces: R1/R2/R3, the audit, and the progress selftest. All must exit 0. Any failure ⇒ hand back, do not ship.
2. Stage by name (no `git add -A`):

```
git add skills/capturerequirements modes/jit.md README.md CLAUDE.md .claude-plugin/plugin.json .claude-plugin/marketplace.json docs/playbook.md skills/kivna/SKILL.md skills/sherpa/SKILL.md docs/plans/2026-08-04-capturerequirements-cut-spec.md
```

3. Commit with piece trailers (conductor appends its own session trailer per its conventions):

```
Cut capturerequirements: jit re-points at the frame flow (v0.73.0)

The skill is deleted whole — the repo's first true rip. Requirements now
live where the entry gates read them: the Value and Release slice
sections of docs/product/<slug>.md, with the everyday-tier Risk ledger
filled in the same framing conversation. jit's Reqs step, README,
playbook, CLAUDE.md, both capability lists, kivna and sherpa all
re-point; What's New names the cut as a loss.

Piece: capturerequirements-cut/1
Piece: capturerequirements-cut/2
Piece: capturerequirements-cut/3
Piece: capturerequirements-cut/4
Piece: capturerequirements-cut/5
Piece: capturerequirements-cut/6
Piece: capturerequirements-cut/7
Piece: capturerequirements-cut/8
Piece: capturerequirements-cut/9
```

4. Push:

```
git push
```

Verify: gate output all-pass; `git status` clean after commit; push accepted by remote. Expected: working tree clean, `main` ahead 0 after push.
