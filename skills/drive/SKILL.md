---
name: drive
description: "Use when the user says 'drive', 'drive <slug>', 'start a work item', 'frame this idea', 'where is <slug> on the ladder', 'take this from idea to release', or wants one thing walked through the whole funnel — frame → viability → scope → design → work handoff → loop → acceptance — across many sessions. Drive owns the WORK ITEM: it reads the item's rung from disk, runs the frame gate's question set at intake (work type declared, never inferred), shows now / next / after, and hands each sitting's work to /kerd:conductor without changing it. Not for running a session (that is conductor) and not for the session boundary (that is switch)."
---

# Drive (Work Item Umbrella)

**Name.** Drive — `/kerd:drive`.
**Purpose.** Walk one work item from idea to acceptance, one rung at a time, across as many sittings as it takes — so nothing that entered through a frame can stall unseen.
**Outcomes.** (a) The item has a work record on disk, at the position the gates derive from it. (b) At the frame gate: a declared work type, and a question set the person edited and answered. (c) Each sitting's work is handed to `/kerd:conductor` framed from the record, and the position is read again when it returns.

The three lines above are ISO/IEC/IEEE 24774 §5.3's required elements — name, purpose, outcomes — adopted as the header for Kerd skills on 2026-08-22. Drive is the first skill written with it.

## What Drive owns, and what it does not

```
/kerd:drive       owns the WORK ITEM   frame → viability → scope → design → handoff → loop → acceptance
                  spans many sessions · state lives on disk, in the work record

/kerd:conductor   owns the SESSION     orient → plan → execute → close
                  spans one sitting
```

**The rule this skill is built under: Drive may CALL conductor, but must never REQUIRE conductor to change.** Any Drive change that needs `skills/conductor/SKILL.md` to behave differently stops there — the frame's retired killer risk comes back the moment that line is crossed.

Vocabulary. The thing Drive moves is a **work item**; its living file is the **work record**, stored today at `docs/product/<slug>.md` (the canonical home `docs/work/<slug>.md` is a later migration). The rung named `handoff` is the **work handoff** — the contract handed to a build. The **session handoff** is switch's, and the two are never called by the bare word.

## Usage

```
/kerd:drive <slug>      pick the item up where disk says it is
/kerd:drive             no slug: list docs/product/*.md slugs with their position, then ask for one — or a new slug
```

## The protocol

### 1. Position — read it, never remember it

Run `python3 tools/gates/gate.py route <slug>`. It is read-only. Never use `tools/diagram/progress.py` for this — it rewrites the committed board on every invocation, `--json` included. From the `enters at:` and `missing for` lines, print one line in plain words:

```
<slug> — now > <rung>, next <rung>, after <rung>
```

`after` is the rung following `next` on the ladder `frame → viability → scope → design → handoff → loop → acceptance → ready-to-release`. At the top, say `now > ready-to-release — the ladder is climbed`. Then print the `need:` lines verbatim; they are the gate's own words for what is still missing, and rewording them is how vocabulary drifts.

Where the repo has no `tools/gates/` (a consuming project without the machinery), say so, and say that position is then the person's word rather than the disk's.

### 2. Intake — only when the work record does not exist

Runs once per item, when `route` reports `docs/product/<slug>.md — file exists` under `need:`.

1. **Declare the work type. Never infer it.** List the seeds on disk — `ls docs/work/question-sets/` — each `<work-type>.md` is one. Ask the person which one this is. If none fits, stop: say the set for that type has not been written yet, and do not pick the nearest. A system that guesses is wrong about a third of the time and fails silently.
2. **Create the work record** `docs/product/<slug>.md`:

   ```
   ---
   route: new
   stage: framed
   work-type: <declared>
   ---

   # <one-line title, in the person's words>

   ## Question set

   <the seed's entries, copied verbatim>
   ```

   `work-type` sits ABOVE any `concerns:` block; the front-matter parser stops reading keys at the first `key: value` line after `concerns:`. `route` is `new` unless the person says this is a `problem` or a licensed `spike`.
3. **Hand the list to the person before asking anything.** They may add, remove or reword entries now. The seed is never read again — what they edited is the set. Editable before starting, never skippable during.

### 3. The frame gate — ask · check · show, from one list

- **Ask.** One entry at a time. Write each answer under its `A:` line in the person's words and read it back. A comment on the read-back is a correction, not a rejection; reshape and read it back again.
- **Check.** `python3 tools/gates/gate.py check <slug> viability` — the command names the rung being entered, but it is the FRAME gate refusing: leaving frame is what is being checked. The frame gate counts answered against declared — `Question set (frame gate): k of n answered — still open: …` — and refuses until every entry has an answer. It counts presence, never quality: whether an answer is true is the person's call, and nothing on disk refuses on it.
- **Show.** Step 1's line, after every check.

When the set is complete, its answers become the first sections — drafted by Drive from the answers, approved by the person: `## Value` (the problem, who has it, the change in units), `## Risk ledger` with at least one `Killer? = yes` row (what would make this not worth doing), `## Grounding` (what exists that this touches). Run `route` again; the item now enters at viability.

### 4. A sitting's work — call conductor, never re-describe it

When a rung needs building, invoke `/kerd:conductor` via the Skill tool with a task framed from the work record and the gate's words:

```
<slug> is at <rung>; the gate still needs: <the need: lines>. This sitting's task: <one item from that list>.
```

Conductor runs orient → plan → execute → close exactly as its own SKILL.md defines, and does not know the task came from Drive. Do not restate its steps here or anywhere. When it returns, go back to step 1 and print the position line.

### 5. Rungs beyond frame

Viability, scope, design, work handoff, loop and acceptance have no question set yet. Say so plainly — "no question set for <rung> yet; the gate's `need:` lines are what is asked" — show the position, hand the sitting to conductor, repeat. The other sets are following slices, one gate at a time.

## The limit, stated

Drive forces the stages and counts the answers. It cannot tell whether an answer is true, whether a drawing means anything, or whether the item was worth starting — those are the person's keys, and this skill adds no machinery that pretends otherwise. Nothing in the gates observes whether Drive or a hand wrote a section; ownership is prompt-layer. Presence is checkable, comprehension is not.

## Principles

- **Call conductor, never change it.** One definition of a session, two callers.
- **Declared, never inferred.** The work type is the producer's word.
- **One list drives ask, check and show.** What is asked, what counts as finished, and what is shown cannot drift apart when they are the same section.
- **Position is read from disk, every time.** Never remembered, never computed by a tool that writes.
