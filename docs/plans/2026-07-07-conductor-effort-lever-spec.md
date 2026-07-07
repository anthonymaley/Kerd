# Spec: conductor per-step reasoning-effort lever (v0.63.0)

**Session:** 2026-07-07 delegated conductor (fable on) — this spec is itself the first live run of the v0.62.0 delegated flow.

**Goal:** a `[delegate]` step in a conductor spec may carry a reasoning-effort hint; dispatch passes it to the subagent via the Agent tool `effort` param. Effort × model tier, not tier alone. Provenance: a friend's Fable-delegation workflow (the compaction/checkpoint parts were rejected — switch owns boundaries).

**Acceptance criteria (whole task):**
- SKILL.md: `[delegate]` steps may carry `effort: low|medium|high`; dispatch passes it; guidance maps effort to work type; spec-authoring named as high-effort work.
- README: v0.63.0 What's New entry + conductor section mentions the lever.
- Versions synced at 0.63.0 in all three locations; both JSON files parse.
- Hook test 26/26.
- No change to inline execution, switch, focus. No trigger-description change (the lever doesn't change *when* conductor is invoked).

---

## Step 1 `[fable]` — SKILL.md effort-lever design + edits

Design the hint format and wire it into `skills/conductor/SKILL.md` (Plan § Delegated execution, Execute § Dispatch mode). Format decided: tag stays `[fable]`/`[delegate]`; a `[delegate]` step may append an effort hint — `[delegate, effort: low]`. Model still chosen at dispatch (the v0.62.0 "two tags" decision stands).

Verify: grep `effort` in SKILL.md shows the hint in both Plan and Execute sections.

## Step 2 `[delegate, effort: medium]` — README edits

Three exact edits to `README.md`. Why: docs travel with code; these mirror the SKILL.md change for readers. Do not touch any other text.

**2a.** Replace the line:

```
## What's New (v0.62.0)
```

with:

```
## What's New (v0.63.0)

### v0.63.0

**Delegated steps carry a reasoning-effort hint.** A `[delegate]` step in a conductor spec may now append an effort level — `[delegate, effort: low]` — which dispatch passes to the subagent via the Agent tool's `effort` param. Effort and model tier are two independent levers: mechanical edits run low-effort on a small model, standard implementation medium, and core-but-delegatable work high-effort on a bigger model — while spec-authoring itself is the high-effort work the expensive planning model does inline. Omit the hint and the subagent runs at its default effort, exactly as in v0.62.0.
```

**2b.** In the `### v0.62.0` section, leave all text unchanged.

**2c.** In the conductor section's "**Delegated execution (optional, off by default).**" paragraph, replace the sentence fragment:

```
each step tagged `[fable]` (done inline) or `[delegate]` (handed off), approved at the plan gate.
```

with:

```
each step tagged `[fable]` (done inline) or `[delegate]` (handed off, optionally with a reasoning-effort hint like `[delegate, effort: low]` that dispatch passes to the subagent), approved at the plan gate.
```

Verify (run both, expect a match each):
- `grep -n "effort: low" README.md` — hits in both the v0.63.0 note and the conductor section.
- `grep -n "What's New (v0.63.0)" README.md` — one hit.

Return: the verify command outputs.

## Step 3 `[delegate, effort: low]` — version bump 0.62.0 → 0.63.0

Three exact replacements, nothing else:
- `.claude-plugin/plugin.json`: `"version": "0.62.0"` → `"version": "0.63.0"`
- `.claude-plugin/marketplace.json`: both occurrences of `"version": "0.62.0"` → `"version": "0.63.0"` (metadata.version and plugins[0].version)

Verify (run, expect exactly three 0.63.0 lines and `json ok`):

```
grep -h '"version"' .claude-plugin/plugin.json .claude-plugin/marketplace.json
python3 -c "import json;json.load(open('.claude-plugin/plugin.json'));json.load(open('.claude-plugin/marketplace.json'));print('json ok')"
```

Return: the verify command outputs.

## Step 4 `[fable]` — close backlog item, full verification, evidence review

Remove the effort-lever backlog item from TODO.md (recording closure), run `bash tests/hooks_test.sh` (expect 26/26), re-run steps 2–3 greps, review subagent evidence against acceptance criteria.
