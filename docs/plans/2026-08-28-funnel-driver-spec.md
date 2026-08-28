# funnel-driver — slice 2: Drive exists, one question set, used once for real

Contract for `docs/product/funnel-driver.md`, release slice 2 (rigor: mvp).
Frame: `docs/product/funnel-driver.md` (Scope → Slice 2). Design:
`docs/design/funnel-driver.md`. GO record:
`docs/gates/2026-08-23-funnel-driver-design.md`.

**Base commit: `94f4304`** (`funnel-driver: write down that slice 2 builds
skills/drive/SKILL.md`). Every diff assertion below is against it.

**What lands.** `skills/drive/SKILL.md` — `/kerd:drive`, the umbrella that owns
a WORK ITEM across frame → viability → scope → design → work handoff → loop →
acceptance, and CALLS `/kerd:conductor` for a sitting's work without changing
it. One hand-written question set for the FRAME gate, seeded at
`docs/work/question-sets/software-change.md` and copied into the work record as
`## Question set` at intake. The completeness check in `tools/gates/kit.py`
reads that same section — one list drives ask · check · show — counting
answered against declared entries, presence only. The check is exercised once
end to end on a real work item, and what it produces is committed. The two
stale sealed views of this item are corrected and resealed through
`gate.py seal`. Version `0.103.0 → 0.104.0`, one bump.

**What does not land.**
- No hunk in `skills/conductor/SKILL.md`. Step 13 asserts the diff is empty;
  a non-empty diff is a refusal, not a review comment (GO record, call 1).
- No `docs/product → docs/work` migration for existing records (slice 3). The
  seed file lives under `docs/work/question-sets/` because the design put it
  there; nothing else moves.
- No split of the fifteen project types (slice 4), no template system, no
  browser opening, no question sets for the other six gates.
- No new drawing. The three sealed views exist; two are corrected, none added.
- The frame's and design doc's own "5 of 8 → 8 of 8" measurement rows are
  NOT rewritten here. They are stale vocabulary in living prose (the same
  class the 2026-08-25 ruling left to its own gate), and the frame is the
  producer's text. Named at the approval gate; not fixed by this slice.
- `docs/design/kerd-map.svg` names nine skills and will be one short. Not
  redrawn here — the release close-out pass (tend, then slainte) that the
  version bump fires is where that drift gets reported.

## Decisions the steps depend on

- **D1 — Where the check lives.** `RUNGS` starts at `frame`, which "requires
  nothing — always enterable" (`check_rung`: the first block is
  `idx >= RUNGS.index("viability")`). So the CODE for the frame gate's exit
  sits in that block — that is a fact about `check_rung`'s shape, not about
  the lifecycle. **Every reader-facing surface calls this a frame-gate
  input** (producer, 2026-08-28: "if the README's viability row carries it,
  the code may be right while the reader learns the wrong lifecycle
  position"): the README's `frame` row, the `need:`/`have:` strings the code
  emits, the skill text, the README prose. An item with an open set is held
  at `frame`. Nothing is added to `route()`; the new rows ride the existing
  have/need lists and print through the existing CLI unchanged.
- **D2 — Opt-in by presence.** `## Question set` absent → no rows at all
  (same shape as AU5's grounding and the design gate's concerns block). No
  existing slug carries the section, so Step 3 proves that every one of the
  21 routes is byte-identical before and after.
- **D3 — The grammar.** One entry is a line `- Q: <question>`; it is answered
  when a following line `A: <text>` (any indentation) before the next entry
  carries non-empty text. Continuation lines belong to the answer above them
  and are not parsed. Lines inside ``` fences are invisible (`_fence_mask`).
  Counted, never judged.
- **D4 — Work type is a front-matter key on the work record**, the design's
  candidate, settled here: `work-type: <slug>` where the value matches
  `^[a-z][a-z0-9-]*$` and names the seed `docs/work/question-sets/<slug>.md`.
  The gate checks the value's SHAPE only, not that the seed exists — the seed
  is the person's, in their repo, and a consuming project owns its own set.
  The key must sit ABOVE any `concerns:` block, because `parse_concerns`
  stops reading at the first `key: value` line after `concerns:`. Required
  only when `## Question set` is present.
- **D5 — The words the gate prints are plain** (the currency rule): `Question
  set: 2 of 6 answered — still open: "Who has it?"; …`. No new vocabulary; a
  newcomer can act on the sentence.
- **D6 — Drive's position oracle is `gate.py route`, never `progress.py`.**
  Gap 6 in the frame: `progress.py` writes the committed trio on every
  invocation including `--json`. Drive reads position read-only.
- **D7 — The reseal follows the 2026-08-25 procedure exactly**
  (`docs/plans/2026-08-25-rung-vocabulary-spec.md` Step 14, ruled in
  CONTEXT.md): downgrade the approval line to its hand-written form, correct
  the text, let `gate.py seal` compute the fingerprint FROM CONTENT, re-render
  the PNG, compare `shasum` (not byte count), and a human eye on the render
  before the key goes back on. The re-approval date is the day the eye lands:
  `2026-08-28`.
- **D8 — Push once, at assembly.** Every `Piece:` trailer moves the board, so
  each work commit makes `progress.py stale` red until a render commit
  follows. Commit per piece (conductor's rule), push at Step 13 behind one
  render commit — the rung-vocabulary assembly precedent. If the sitting
  must cross a session boundary before Step 13, render and push first.
- **D9 — The skill carries the 24774 §5.3 header** (name, purpose, outcomes),
  the adaptation decided 2026-08-22 (CONTEXT.md, "Every layer stands on a
  standard") and queued in TODO as "24774 §5.3 header on every SKILL.md". No
  skill has it yet; Drive is the first written with it. That queued item is
  NOT discharged by this — one of ten.
- **D10 — The real item is `measurement`** (TODO `## Now` item 3: "Frame the
  measurement item — Tony's value statement is captured verbatim in
  CONTEXT.md and nothing is framed yet"), work type `software-change`. A new
  slug, so intake runs for real. The producer has to be at the keyboard for
  Step 12 — the set is his to edit and answer; a run with model-written
  answers proves nothing.

## Pieces

- [ ] 1. `tools/gates/kit.py` + `tools/gates/README.md` — the question-set check at the frame gate, T50/T51, the canonical write-down (Steps 1–3)
- [ ] 2. `docs/work/question-sets/software-change.md` — the first seed, hand-written (Step 4)
- [ ] 3. `skills/drive/SKILL.md` + the release checklist to 0.104.0 — README, CLAUDE.md, both capability lists (Steps 5–8)
- [ ] 4. `docs/design/funnel-driver/why-an-umbrella.html` + `span-vs-slice.html` resealed, PNGs re-rendered, the producer's eye (Steps 9–11)
- [ ] 5. `docs/product/measurement.md` — the real run, its answered set committed (Step 12)
- [ ] 6. Assembly — boxes checked, conductor diff empty, board rendered, pushed (Step 13)

Commit order: this spec first, with no trailer (it moves `funnel-driver`
handoff → loop, so the render in Step 13 covers it). Then one commit per
piece carrying `Piece: funnel-driver/<n>` as the last line. Pieces 3's commit
is the one that bumps the version — the release checklist runs before it,
not after.

---

### Step 1 — kit.py: the question-set check at the frame gate, with its fixtures  [delegate, model: sonnet, effort: high]

**What:** Three edits to `tools/gates/kit.py`, then the selftest count.

1. **Constants**, directly under `RIGOR_SECTION_HEADING_RE` (line ~133):

   ```python
   # ── the question set (frame gate; funnel-driver slice 2) ──────────────────
   # One list drives ask · check · show. An entry is '- Q: <question>'; it is
   # answered when a following 'A: <text>' line (any indentation) before the
   # next entry carries text. Counted, never judged — the human key judges.
   QUESTION_SET_TITLE = "Question set"
   QS_Q_RE = re.compile(r'^- Q:\s*(.*)$')
   QS_A_RE = re.compile(r'^\s*A:\s*(.*)$')
   # work-type names a seed file, docs/work/question-sets/<work-type>.md, so
   # it is shaped like a filename stem. Declared by the producer, never
   # inferred; the gate checks the shape, never that the seed exists.
   WORK_TYPE_RE = re.compile(r'^[a-z][a-z0-9-]*$')
   ```

2. **The parser**, a new function placed directly after `rigor_problems`
   (before the `# ── the risk ledger` banner):

   ```python
   # ── the question set (frame gate) ───────────────────────────────────────────

   def question_set_status(text):
       """Count answered against declared entries in '## Question set' —
       presence only, never quality. None when the section is absent (opt-in
       by presence: a work record with no set is not refused, so nothing
       already on a board moves). Otherwise {"declared": int, "answered":
       int, "unanswered": [question], "problems": [str]}. Grammar: QS_Q_RE
       opens an entry; the first QS_A_RE line before the next entry answers
       it when it carries text; other lines are content (continuations).
       Lines inside ``` fences are invisible — a quoted example is content,
       not an entry. Problem strings carry no 'docs/product/<S>.md — '
       prefix; callers prepend it."""
       body = find_section(text, QUESTION_SET_TITLE)
       if body is None:
           return None
       lines = body.splitlines()
       mask = _fence_mask(lines)
       entries = []      # [question, answered]
       problems = []
       for n, (line, fenced) in enumerate(zip(lines, mask), start=1):
           if fenced:
               continue
           mq = QS_Q_RE.match(line)
           if mq:
               q = mq.group(1).strip()
               if not q:
                   problems.append(f"Question set: entry {len(entries) + 1} has no question text")
               entries.append([q, False])
               continue
           ma = QS_A_RE.match(line)
           if ma:
               if not entries:
                   problems.append(f"Question set: line {n} answer before any question")
                   continue
               if ma.group(1).strip():
                   entries[-1][1] = True
       if not entries:
           problems.append("Question set: declared with no entries (want '- Q: <question>' lines)")
       return {
           "declared": len(entries),
           "answered": sum(1 for _, a in entries if a),
           "unanswered": [q for q, a in entries if not a],
           "problems": problems,
       }
   ```

3. **The wiring**, in `check_rung`, inside the `idx >= RUNGS.index("viability")`
   block's `else:` branch, appended AFTER the killer-risk floor (after the
   `need.append(... "Risk ledger names no killer risk" ...)` line's block
   closes, still inside the `else:`):

   ```python
           # The FRAME gate's completeness check (funnel-driver slice 2) — it
           # lives in the viability block only because `frame` requires
           # nothing to enter; every string it emits says "frame gate", so
           # the reader learns the right lifecycle position. One list drives
           # ask · check · show. Opt-in by presence — a record with no
           # '## Question set' is not refused here. Presence only:
           # an answer is counted, never judged, and nothing in this file can
           # tell whether Drive or a hand wrote it.
           qs = question_set_status(product_text)
           if qs is not None:
               wt = (fm or {}).get("work-type", "") or ""
               if WORK_TYPE_RE.match(wt):
                   have.append(f"{rel_product} — front matter work-type={wt}")
               else:
                   need.append(
                       f"{rel_product} — front matter work-type "
                       "(declared by the producer, never inferred)"
                   )
               for p in qs["problems"]:
                   need.append(f"{rel_product} — {p}")
               if qs["declared"] and not qs["unanswered"] and not qs["problems"]:
                   have.append(
                       f'{rel_product} — Question set (frame gate): {qs["answered"]} of {qs["declared"]} answered'
                   )
               elif qs["declared"]:
                   listed = "; ".join(f'"{q}"' for q in qs["unanswered"][:3])
                   more = qs["unanswered"][3:]
                   tail = f" (+{len(more)} more)" if more else ""
                   need.append(
                       f'{rel_product} — Question set (frame gate): {qs["answered"]} of {qs["declared"]} '
                       f"answered — still open: {listed}{tail}"
                   )
   ```

4. **Fixtures T50 and T51**, appended in `_selftest_body()` directly BEFORE
   the `# T45 — purity` block (T45 sits last by design; keep it last):

   ```python
       # T50 — the frame gate's completeness check (funnel-driver slice 2). A
       # '## Question set' is opt-in by presence; once present, every entry
       # needs an answer and the front matter needs a declared work-type. The
       # refusal names the count and the open questions in plain words.
       with tempfile.TemporaryDirectory() as root_t50:
           p50 = os.path.join(root_t50, "docs", "product", f"{slug}.md")
           qs_open = (
               "## Question set\n\n"
               "- Q: What is the problem?\n  A: Nothing walks an item to launch.\n"
               "- Q: Who has it?\n  A:\n"
               "- Q: What would be different?\n"
           )
           _sw(p50, ledger_named_only + "\n" + qs_open)
           assert route(root_t50, slug)["enters_at"] == "frame", \
               "T50: an open question set must hold the item at frame"
           cr = check_rung(root_t50, slug, "viability")
           assert (
               f"docs/product/{slug}.md — front matter work-type (declared by the producer, never inferred)"
           ) in cr["need"], f"T50: expected the work-type need row, got {cr['need']}"
           assert (
               f'docs/product/{slug}.md — Question set (frame gate): 1 of 3 answered — still open: '
               '"Who has it?"; "What would be different?"'
           ) in cr["need"], f"T50: expected the plain-words count row, got {cr['need']}"

           qs_done = (
               "## Question set\n\n"
               "- Q: What is the problem?\n  A: Nothing walks an item to launch.\n"
               "- Q: Who has it?\n  A: Tony, on every item.\n"
               "- Q: What would be different?\n  A: Three unowned rungs get an owner.\n"
               "  A continuation line belongs to the answer above it.\n"
           )
           _sw(p50, ledger_named_only.replace("route: new\n", "route: new\nwork-type: software-change\n")
               + "\n" + qs_done)
           cr = check_rung(root_t50, slug, "viability")
           assert cr["need"] == [], f"T50: expected the frame gate to release, got {cr['need']}"
           assert f"docs/product/{slug}.md — front matter work-type=software-change" in cr["have"], \
               f"T50: expected the work-type have row, got {cr['have']}"
           assert f"docs/product/{slug}.md — Question set (frame gate): 3 of 3 answered" in cr["have"], \
               f"T50: expected the answered have row, got {cr['have']}"
           assert route(root_t50, slug)["enters_at"] == "viability", \
               "T50: a complete set must release the item to viability"

           # no section at all is not a refusal — nothing already on a board moves
           _sw(p50, ledger_named_only)
           cr = check_rung(root_t50, slug, "viability")
           assert not any("Question set" in x or "work-type" in x for x in cr["need"] + cr["have"]), \
               f"T50: an absent section must add no rows, got {cr['need'] + cr['have']}"
           assert route(root_t50, slug)["enters_at"] == "viability", \
               "T50: an item with no question set routes exactly as before"

       # T51 — the grammar's edges: a quoted example inside ``` is content,
       # not an entry; a work-type that is not a filename stem is refused; an
       # answer before any question and a section with no entries are named
       # problems, never a vacuous pass.
       with tempfile.TemporaryDirectory() as root_t51:
           p51 = os.path.join(root_t51, "docs", "product", f"{slug}.md")
           _sw(p51, ledger_named_only.replace("route: new\n", "route: new\nwork-type: Software Change\n")
               + "\n## Question set\n\n"
               "```\n- Q: quoted example, invisible\n  A:\n```\n"
               "- Q: Real question?\n  A: Real answer.\n")
           cr = check_rung(root_t51, slug, "viability")
           assert f"docs/product/{slug}.md — Question set (frame gate): 1 of 1 answered" in cr["have"], \
               f"T51: the fenced example must be invisible, got {cr['have']}"
           assert (
               f"docs/product/{slug}.md — front matter work-type (declared by the producer, never inferred)"
           ) in cr["need"], f"T51: 'Software Change' is not a seed filename stem, got {cr['need']}"
           assert route(root_t51, slug)["enters_at"] == "frame", \
               "T51: an illegal work-type holds the item at frame"

           st = question_set_status("# X\n\n## Question set\n\nA: orphan answer\n\nprose only\n")
           assert st["declared"] == 0 and st["answered"] == 0, f"T51: expected nothing declared, got {st}"
           assert st["problems"] == [
               "Question set: line 1 answer before any question",
               "Question set: declared with no entries (want '- Q: <question>' lines)",
           ], f"T51: expected the two named problems in order, got {st['problems']}"
           assert question_set_status("# X\n\n## Value\n\nno set here\n") is None, \
               "T51: an absent section is None, not a problem"
   ```

   `ledger_named_only` is the T4 fixture string, defined at function scope
   inside `_selftest_body` and still bound after its `with` block closes —
   T47–T49 already use `ledger_good` and `spec_checked` the same way.

5. **The count.** In `selftest()`, both the docstring ("Run the 49
   fixture-built cases" → "Run the 51 fixture-built cases") and the print
   (`"selftest: 49 cases passed"` → `"selftest: 51 cases passed"`).

**Why:** This is the FRAME gate's check. Its code sits in `check_rung`'s
viability block only because `frame` requires nothing to enter and the
exit of one rung is evaluated as the entry of the next (D1); putting it
anywhere else would need a new rung or a change to `route()`, and neither is
owed. The emitted strings say `(frame gate)` so that the one line a newcomer
reads names the lifecycle position correctly even though the command that
printed it was `check <slug> viability`. Opt-in by presence (D2) is what
lets this land without moving a single existing item — the board is derived,
and a check that turned 21 rows red on landing would be a regression dressed
as a feature. `QS_A_RE` accepts any indentation because `find_section` strips
the body, which removes the leading spaces of a first-line answer. The problem
strings are prefixed by the caller like `rigor_problems`' are — one
convention. `WORK_TYPE_RE` checks a filename stem's shape and nothing more:
the seed is the person's file in the person's repo, and a gate that demanded
Kerd's seed exist would be Kerd deciding what work types there are.

**Verify:** `python3 tools/gates/gate.py selftest` → last two lines
`root resolution: 7 cases passed` then `selftest: 51 cases passed`, exit 0.
Then `python3 tools/gates/gate.py audit` → `audit: clean` (with any
pre-existing `finding:` lines unchanged), and
`python3 tools/gates/gate.py route funnel-driver | grep '^enters at:'` →
`enters at: loop` (this spec is on disk by now; if it prints `handoff` the
spec was not committed/placed first).

---

### Step 2 — the gates README: the canonical write-down of the new check  [delegate, model: sonnet, effort: low]

**What:** Two edits to `tools/gates/README.md`.

1. In the rung table, the `frame` row (line 40, today exactly
   `| \`frame\` | nothing — always enterable |`) becomes the frame gate's
   entry AND exit condition. Replace the whole row with:

   > | `frame` | to enter: nothing — always enterable. To LEAVE: when section `Question set` exists (opt-in by presence — an absent section adds no rows): front matter `work-type` matching `^[a-z][a-z0-9-]*$` (declared by the producer at intake, never inferred; names the seed `docs/work/question-sets/<work-type>.md`, placed ABOVE any `concerns:` block) · every `- Q: <question>` entry answered — a following `A: <text>` line before the next entry carrying text; fenced lines invisible. Counted, never judged: `Question set (frame gate): k of n answered — still open: "…"` names what is open. Evaluated by `check <S> viability` because a rung's exit is the next rung's entry; it is the frame gate's input, not viability's. |

   The `viability` row (line 41) is NOT touched.

2. A new subsection, placed directly BEFORE the `## Views` (or the first
   `## ` heading after the rung table that describes the design gate's
   concerns block — read the file and pick the heading that opens the views
   section):

   ```markdown
   ## Question set (frame gate)

   One list drives three things at the frame gate: what `/kerd:drive` asks
   the person, what this gate counts as finished, and what Drive shows as
   `now > frame, next viability, after scope`. The list lives IN the work
   record as `## Question set`, copied at intake from a seed
   `docs/work/question-sets/<work-type>.md` that is never read again — what
   the person edited is the set.

   Grammar (`kit.question_set_status`): an entry is `- Q: <question>`; it is
   answered when the first `A: <text>` line before the next entry carries
   text; other lines are content (continuations). Fenced code is invisible.

       - Q: What is the problem, in the words of the person who has it?
         A: Nothing walks an item from idea to launch.

   The gate counts presence and refuses while any entry is open. It never
   judges an answer — that is the producer's key — and nothing here can tell
   whether Drive or a hand wrote the section. Opt-in by presence: a work
   record without the section is checked exactly as before.
   ```

**Why:** The README is "the canonical home" of the ladder's write-down
(rung-vocabulary Step 6); a check that exists only in code is the drift the
2026-08-25 sweep spent a step removing. The example is indented four spaces
rather than fenced so the `- Q:` line reads as an example in the README
without teaching a reader that fences are the format.

**Verify:** `sed -n 40p tools/gates/README.md | grep -c 'Question set (frame gate)'` → `1`;
`sed -n 41p tools/gates/README.md | grep -c 'Question set'` → `0` (the viability row is untouched);
`grep -n '^## Question set (frame gate)' tools/gates/README.md` → one line;
`python3 tools/gates/gate.py audit` → `audit: clean`.

---

### Step 3 — diff review: no existing item moved, no existing row changed  [keep]

**What:** Read the Step 1 and Step 2 diffs (`git diff 94f4304 -- tools/gates/`)
for collateral, then prove the board did not move:

```
for s in $(ls docs/product | sed 's/\.md$//'); do printf "%-40s %s\n" $s "$(python3 tools/gates/gate.py route $s | grep '^enters at')"; done
```

Expected, exactly (measured at `94f4304` on 2026-08-28, with only
`funnel-driver` changed — by this spec's existence, not by the check):

```
conductor-boundary                       enters at: ready-to-release
diagram-toolkit                          enters at: frame
funnel-driver                            enters at: loop
gate-visuals                             enters at: acceptance
grounding-was-read                       enters at: ready-to-release
hooks-autoload                           enters at: viability
inline-composer                          enters at: design
model-effort-advisory                    enters at: design
progress-html                            enters at: acceptance
push-wiring                              enters at: ready-to-release
release-closeout                         enters at: ready-to-release
requirements-project-type-templates      enters at: frame
requirements-traceability                enters at: design
requirements-view                        enters at: frame
rigor-level                              enters at: ready-to-release
rung-vocabulary                          enters at: ready-to-release
shared-memory                            enters at: design
standards-grounding                      enters at: frame
switch-fidelity                          enters at: design
time-awareness                           enters at: ready-to-release
vault-unhook                             enters at: ready-to-release
```

What the review must catch: any change outside the three insertion points
named in Step 1 (constants, the new function, the viability `else:` branch)
and the two-line count edit; any existing `have`/`need` string reworded; T45
no longer last. Then commit Pieces 1: `git add tools/gates/kit.py
tools/gates/README.md`, message ending `Piece: funnel-driver/1`.

**Why:** A check that lands by "adding rows" can still reword an existing row
by accident, and the router's strings are read by people who were not in the
room (CONTEXT.md, 2026-08-27). Reading a diff for edits that pass every verify
command yet leave the stated scope is judgment; it cannot be a command.

**Verify:** `git log -1 --format=%B | tail -1` → `Piece: funnel-driver/1`;
`git diff --stat 94f4304..HEAD -- skills/conductor/SKILL.md` → empty output.

---

### Step 4 — the seed: `docs/work/question-sets/software-change.md`  [delegate, model: haiku, effort: low]

**What:** Create the file with exactly this content:

```markdown
# Question set — software change

Seed for a work item whose declared work type is `software-change`. Drive
copies the entries below into the work record's `## Question set` at intake;
the person edits them there, and this seed is never read again. Six entries,
doing two jobs: enough to judge whether the idea is worth pursuing, and
enough to become the first requirements.

What the gate reads: an entry is a `- Q:` line followed by an `A:` line. It
counts as answered when the `A:` line carries text. Indented lines after it
belong to the answer. The gate counts; it never judges.

- Q: What is the problem, in the words of the person who has it?
  A:
- Q: Who has it, and how often does it bite?
  A:
- Q: What would be different if this worked — in units someone could measure?
  A:
- Q: What is the smallest thing that would prove it, and what is deliberately left out?
  A:
- Q: What could make this not worth doing at all?
  A:
- Q: What already exists that this touches or replaces?
  A:
```

Commit as Piece 2: `git add docs/work/question-sets/software-change.md`,
message ending `Piece: funnel-driver/2`.

**Why:** Six, not twenty — the frame killed a 20-item checklist that
measured at zero. Each entry maps to a section the ladder will demand next:
1–3 become `## Value` (the value in the person's words, in units), 4 seeds
`## Scope`, 5 is the killer-risk floor the viability gate requires, 6 is
`## Grounding`. The seed carries no `## Question set` heading, so the gate
never mistakes the seed for a record. It sits under `docs/work/` because the
design named that as the home for reusable sets; no other path moves.

**Verify:** `grep -c '^- Q: ' docs/work/question-sets/software-change.md` →
`6`; `grep -c '^## ' docs/work/question-sets/software-change.md` → `0`;
`python3 tools/gates/gate.py audit` → `audit: clean`.

---

### Step 5 — `skills/drive/SKILL.md`, the caller  [delegate, model: haiku, effort: low]

**What:** Create `skills/drive/SKILL.md` with exactly this content (verbatim;
the text is the deliverable, and it is deliberately short):

````markdown
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
````

**Why:** Short and procedural, as the design's "What Drive is" asks; every
sentence either tells the model what to run or states a limit. Conductor is
named as a call and its steps are never restated — the same idiom
conductor's own close-out uses for `/kerd:switch out`. The 24774 header is D9.
The description names the phrases a person would actually say and draws the
boundary against conductor and switch in the same breath, because the three
are the words most likely to be confused at invocation time.

**Verify:** `python3 tools/gates/gate.py release` → `release: clean`
(`_skill_names` now includes `drive`, so R3 sweeps for bare `/drive` too);
`grep -c 'kerd:conductor' skills/drive/SKILL.md` → `4` or more;
`grep -nE '(^|[^a-z-])handoff([^a-z-]|$)' skills/drive/SKILL.md | grep -v 'work handoff\|session handoff\|→ handoff\|named .handoff.' ` → empty
(bare `handoff` appears only as the rung name in ladder lines or as a
qualified phrase).

---

### Step 6 — review the skill against the umbrella rule  [keep]

**What:** Read `skills/drive/SKILL.md` once, cold, as the model that will run
it, and check four things by eye that no grep can:

1. Nothing in it asks conductor to behave differently — every conductor
   mention is an invoke or a boundary, never an instruction to conductor.
2. Every machine-emitted string it tells the model to print is plain
   (the position line, the intake prompt, the "no question set yet" line).
3. `handoff` never stands bare in prose; the ladder lines are the only bare
   uses and they are rung names.
4. The frontmatter `name:` is `drive` with no prefix; every slash reference is
   `/kerd:…`.

Then: `git diff --stat 94f4304..HEAD -- skills/conductor/SKILL.md` → empty.

**Why:** The umbrella rule is a prompt-layer promise, and the frame's own
risk ledger says prompt-layer instruction is advice the model can skip. The
one place that promise can be checked is a human reading the text before it
ships. This step does not commit; Piece 3's commit follows Step 8 so the
version bump lands in the same commit as the skill (CLAUDE.md: the release
checklist runs before the commit, not after).

**Verify:** `git diff --stat 94f4304..HEAD -- skills/conductor/SKILL.md` →
empty output; `git status --porcelain skills/` → exactly `?? skills/drive/`.

---

### Step 7 — the release checklist: 0.104.0, README, CLAUDE.md, both capability lists  [delegate, model: sonnet, effort: medium]

**What:** Exact edits, five files. One bump for this release — no other step
touches a version.

1. **`.claude-plugin/plugin.json`** — `"version": "0.103.0"` → `"0.104.0"`;
   `"description"` becomes exactly:

   ```
   Opinionated workflow toolkit: driving a work item from idea to acceptance, session discipline, session and machine handoff, knowledge management, project audits, human writing voice, structural health, skill discovery, risk qualification, and conversational pair mode
   ```

2. **`.claude-plugin/marketplace.json`** — `metadata.version` and
   `plugins[0].version` both `"0.103.0"` → `"0.104.0"`;
   `plugins[0].description` becomes the byte-identical string from item 1.
   `metadata.description` ("Kerd: opinionated workflow skills for Claude
   Code") is NOT touched.

3. **`CLAUDE.md`** — line 3: `nine workflow skills for session discipline,`
   → `ten workflow skills for driving a work item from idea to acceptance, session discipline,`.
   In the `## Project Structure` block, add directly after the
   `docs/product/` line:

   ```
   docs/work/question-sets/ # seed question sets, one <work-type>.md, copied into a work record at intake
   ```

4. **`README.md`** — three edits:
   - Line 7: `**What is Kerd?** Nine workflow skills` → `**What is Kerd?** Ten workflow skills`.
   - Under `## What's New (v0.99.0)`, directly above `### v0.103.0`, insert:

     ```markdown
     ### v0.104.0

     **The funnel has a driver.** `/kerd:drive <slug>` is a new skill that owns one work item across the whole ladder — frame → viability → scope → design → work handoff → loop → acceptance — over as many sessions as it takes, and hands each sitting's work to `/kerd:conductor` without changing a line of it. At the frame gate it asks a short question set: you declare the work type (never guessed), the set is copied from a seed into the work record, you edit it before anything is asked, and the frame gate counts answered against declared until every entry has an answer — the item stays at `frame` until then. One list drives what is asked, what counts as finished, and the `now > frame, next viability, after scope` line you see. **What it means:** an idea can enter the funnel by being asked six questions rather than by someone remembering the sections, and nothing already on the board moves — the check applies only to a record that carries the section. **The limit, stated:** the gate counts presence, never quality; it cannot tell whether an answer is true, and it cannot tell whether Drive or a hand wrote the section. One seed exists (`software-change`); the other gates' sets are following slices.
     ```

   - Under `## Skills`, directly ABOVE `### conductor (Session Discipline)`,
     insert:

     ```markdown
     ### drive (Work Item Umbrella)

     Drive walks one work item from idea to acceptance, across as many sessions as it takes, and calls conductor for each sitting's work without changing it. It reads the item's rung from disk (`gate.py route`, never the board renderer), shows `now > X, next Y, after Z`, and at the frame gate runs a question set: you declare the work type from the seeds in `docs/work/question-sets/`, the set is copied into the work record's `## Question set`, you edit it first, and the frame gate holds the item at `frame` until every entry carries an answer. Counted, never judged — the answers are yours. Conductor owns the session; switch owns the session boundary; Drive owns the item.

     ```
     /drive <slug>        # pick the item up where disk says it is, or start it
     /drive               # list every item and where it sits
     ```
     ```

5. **`skills/drive/SKILL.md`** — nothing; its frontmatter `description` is
   the trigger and was written in Step 5.

**Why:** A new skill is MINOR (CLAUDE.md Version Strategy). The two capability
lists must be byte-identical because `_release_capability` refuses drift;
`metadata.description` is a different shape by design and is left alone. The
README section follows the pair/slainte pattern — one paragraph, one code
block of shorthand — and the shorthand omits `kerd:` because README examples
are the one place the namespace rule allows it. "Session and machine handoff"
is an existing qualified phrase and stays; "work handoff" is the Drive rung.

**Verify:** `python3 tools/gates/gate.py release` → `release: clean`;
`python3 -c "import json;p=json.load(open('.claude-plugin/plugin.json'));m=json.load(open('.claude-plugin/marketplace.json'));print(p['version'],m['metadata']['version'],m['plugins'][0]['version'],p['description']==m['plugins'][0]['description'])"`
→ `0.104.0 0.104.0 0.104.0 True`; `grep -c '^### drive (Work Item Umbrella)' README.md` → `1`;
`grep -c 'Ten workflow skills' README.md` → `1`; `grep -c 'ten workflow skills' CLAUDE.md` → `1`.

---

### Step 8 — review the release seam, then commit Piece 3  [keep]

**What:** `git diff 94f4304 -- README.md CLAUDE.md .claude-plugin/` read in
full. What the review must catch: any line changed outside the five named
edits (a formatter re-wrapping JSON, a stray README paragraph), the What's New
entry landing under the wrong heading, the skills section landing after
conductor instead of before it, and `metadata.description` touched. Then
commit: `git add skills/drive/SKILL.md README.md CLAUDE.md .claude-plugin/plugin.json .claude-plugin/marketplace.json`,
message ending `Piece: funnel-driver/3`. Do not stage `CONTEXT.md`, `TODO.md`
or anything under `kivna/`.

**Why:** The skill and its release checklist land in one commit so no push
ever carries a skill without its bump (CLAUDE.md commit rules). Reading a
JSON diff for a re-serialised file is judgment: `release` passes on a
reformatted manifest that has doubled in line count.

**Verify:** `git log -1 --format=%B | tail -1` → `Piece: funnel-driver/3`;
`git show --stat HEAD | grep -c 'skills/conductor'` → `0`;
`python3 tools/gates/gate.py release` → `release: clean`.

---

### Step 9 — correct the two views, downgrade their seals, let `seal` retake the fingerprints  [delegate, model: sonnet, effort: medium]

**What:** In this exact order.

1. **`docs/product/funnel-driver.md`** — two approval lines downgraded to
   the hand-written form with the re-approval date. Line 9
   `    approval: Tony, 2026-08-23 · fp:54f84887b8b8` →
   `    approval: Tony, 2026-08-28`. Line 17
   `    approval: Tony, 2026-08-23 · fp:5adeb340c7ee` →
   `    approval: Tony, 2026-08-28`. Line 13 (`gate-loop.html`,
   `fp:47883502cf4b`) is NOT touched — that view carries no retired name
   (checked 2026-08-28: `grep -nw 'slice\|contract\|build\|goal\|eight'`
   finds only the phrase "I want to build X"). Change nothing else in the
   file. **Do not compute a hash by hand.**

2. **`docs/design/funnel-driver/why-an-umbrella.html`** — text only, no
   layout changes except deleting the eighth box. Line numbers are as at
   `94f4304`; match on the strings.
   - Line 25, inside `<desc id="cl-d">`: `of the funnel's eight stages, five have an owner in some skill and three — frame, slice and design — have none.` → `of the funnel's seven rungs, four have an owner in some skill and three — frame, scope and design — have none.`
   - Line 100: `Of the funnel's eight stages, five have something that owns them. Three have nobody:` → `Of the funnel's seven rungs, four have something that owns them. Three have nobody:`
   - Line 101: `nothing anywhere writes the idea, the cut, or the design.` → `nothing anywhere writes the idea, the scope, or the design.`
   - Line 110: `>slice</text>` → `>scope</text>`; the `the cut` caption two lines below it (`x="278" y="754"`) → `the scope`.
   - Line 118: `>contract</text>` → `>handoff</text>`.
   - Line 121: `>build</text>` → `>loop</text>`.
   - Line 124: `>goal</text>` → `>acceptance</text>`.
   - Lines 126–128 — the eighth box (`<rect class="box" x="814" …`, `<text … x="828" y="716" …>loop</text>`, `<text class="e" x="828" y="736">owned</text>`) — delete all three lines.
   - Line 129: `5 of 8 owned. The three with nobody are the three at the front — where a person starts.` → `4 of 7 owned. The three with nobody are the three at the front — where a person starts.`
   - Every other line stays byte-identical, including the `<title>` and `<h1>`.

3. **`docs/design/funnel-driver/span-vs-slice.html`** — five text nodes; the
   `<title>`, `<h1>` and the SVG `<title id="sv-t">` keep the word `slice`
   (it is the time-slice sense and is correct).
   - Line 70: `frame → viability → slice → design` → `frame → viability → scope → design`
   - Line 76: `frame → design → contract → build → goal` → `frame → design → handoff → loop → acceptance`
   - Line 80: `frame → … → done` → `frame … ready-to-release` (the arrows are dropped because this label sits inside a 192px bar; the longer rung name needs the width)
   - Line 110: `>slice</text>` → `>scope</text>`
   - Line 112: `>contract</text>` → `>handoff</text>`

4. **Seal.** `python3 tools/gates/gate.py seal funnel-driver`. `seal_views`
   reads each view's CONTENT, computes the fingerprint, and writes it into
   the two downgraded lines; `gate-loop` reports `already`.

Do not stage or commit — Step 11 commits Piece 4 after the producer's eye.

**Why:** D7. The seal IS the approval: a changed drawing loses its key by
design, so the route is downgrade → correct → recompute from content, never
a hand-typed hash (`view_fingerprint` handed a path returns a plausible
wrong value — measured 2026-08-25). Ownership is restated for the seven-rung
ladder as it stood before Drive: viability (interrogate), handoff, loop and
acceptance (conductor's spec and build, the acceptance record) owned; frame,
scope and design unowned — the same three the design doc names as Drive's.
The eighth box is deleted rather than relabelled because the fold
(`build`+`goal` → `loop`+`acceptance`) has one fewer position.

**Verify:**

```
grep -c 'eight stages\|>slice<\|>contract<\|>build<\|>goal<\|5 of 8\|the cut' docs/design/funnel-driver/why-an-umbrella.html
grep -c 'slice → design\|contract → build\|→ done\|>slice<\|>contract<' docs/design/funnel-driver/span-vs-slice.html
grep -c '<title>A work item is a span. A session is a slice.</title>' docs/design/funnel-driver/span-vs-slice.html
grep -n 'approval: Tony' docs/product/funnel-driver.md
python3 tools/gates/gate.py audit
python3 tools/gates/gate.py check funnel-driver design | tail -1
```

→ `0`, `0`, `1`; then three approval lines where lines 9 and 17 read
`approval: Tony, 2026-08-28 · fp:<12 hex>` with values that are neither
`54f84887b8b8` nor `5adeb340c7ee`, and line 13 still `Tony, 2026-08-23 · fp:47883502cf4b`;
then `audit: clean` (a mismatched seal is an AU9 problem — a clean audit is
the proof the reseal took); then `PASS design — funnel-driver: …`.

---

### Step 10 — re-render the two PNGs at their committed dimensions  [delegate, model: haiku, effort: low]

**What:** From the repo root. The dimensions were read off the PNG headers on
2026-08-28 (`why-an-umbrella.png` 1100×1300, `span-vs-slice.png` 1100×950);
do not guess them.

```
cd /Users/anthonymaley/development/product/Kerd
shasum docs/design/funnel-driver/why-an-umbrella.png docs/design/funnel-driver/span-vs-slice.png
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars \
  --screenshot="$PWD/docs/design/funnel-driver/why-an-umbrella.png" --window-size=1100,1300 \
  "file://$PWD/docs/design/funnel-driver/why-an-umbrella.html"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars \
  --screenshot="$PWD/docs/design/funnel-driver/span-vs-slice.png" --window-size=1100,950 \
  "file://$PWD/docs/design/funnel-driver/span-vs-slice.html"
shasum docs/design/funnel-driver/why-an-umbrella.png docs/design/funnel-driver/span-vs-slice.png
python3 -c "import struct;[print(p,struct.unpack('>II',open(p,'rb').read(24)[16:24])) for p in ['docs/design/funnel-driver/why-an-umbrella.png','docs/design/funnel-driver/span-vs-slice.png']]"
```

Report both `shasum` pairs verbatim.

**Why:** A re-read PNG can come back CACHED at an identical byte count
(measured 2026-08-25); the hash pair is the only evidence the render
happened. System Chrome, not Playwright, per the playbook.

**Verify:** both `shasum` values differ between the first and second run;
the dimensions line prints `(1100, 1300)` and `(1100, 950)`;
`git status --porcelain docs/design/funnel-driver/ docs/product/funnel-driver.md`
→ exactly five modified paths (two `.html`, two `.png`, the product doc).

---

### Step 11 — the producer's eye on the renders, then Piece 4  [keep]

**What:** Open both re-rendered PNGs and look. On `why-an-umbrella.png`: the
bottom band shows SEVEN boxes, labelled frame · viability · scope · design ·
handoff · loop · acceptance, with frame/scope/design marked `nobody`, the
caption reads `4 of 7 owned…`, nothing is clipped and no box overlaps the
band's right edge. On `span-vs-slice.png`: the three bars read
`frame → viability → scope → design`, `frame → design → handoff → loop → acceptance`
and `frame … ready-to-release` — the last inside its 192px bar without
spilling; the lower-left panel reads scope · design · handoff. Everything
else is unchanged in content from what was approved on 2026-08-23. If
anything else moved, stop and hand back — do not commit a drawing the
producer has not seen.

Put the two PNGs in front of the producer. His word is the approval the
`2026-08-28` date on the seal lines now claims. On it, commit Piece 4:
`git add docs/design/funnel-driver/why-an-umbrella.html docs/design/funnel-driver/why-an-umbrella.png docs/design/funnel-driver/span-vs-slice.html docs/design/funnel-driver/span-vs-slice.png docs/product/funnel-driver.md`,
message ending `Piece: funnel-driver/4`.

**Why:** Step 9 wrote a line saying Tony approved this content, and the
machine cannot tell a vocabulary correction under a standing ruling from a
redrawn diagram. His ruling authorises the reseal of THIS correction and
nothing the render might otherwise show. This is the producer's key and the
one step in the reseal that cannot be a command.

**Verify:** `git log -1 --format=%B | tail -1` → `Piece: funnel-driver/4`;
`python3 tools/gates/gate.py audit` → `audit: clean`;
`python3 tools/gates/gate.py route funnel-driver | grep '^enters at:'` → `enters at: loop`.

---

### Step 12 — the real run: `/kerd:drive measurement`, end to end at the frame gate  [keep]

**What:** With the producer at the keyboard, in this session, invoke the new
skill on a NEW slug and let it run its own steps — do not shortcut them by
hand. Expected shape of the run, each beat observable:

1. `python3 tools/gates/gate.py route measurement` → `enters at: frame` with
   `need: docs/product/measurement.md — file exists` among the four viability
   rows. Drive prints `measurement — now > frame, next viability, after scope`.
2. Intake: `ls docs/work/question-sets/` → `software-change.md`. Drive asks;
   the producer DECLARES `software-change` (if he declares something else,
   Drive must stop and say that set does not exist yet — that refusal is
   also a valid observation). Drive creates `docs/product/measurement.md`
   with `route: new`, `stage: framed`, `work-type: software-change`, a title
   in his words, and `## Question set` holding the six seed entries. Drive
   hands him the list to edit BEFORE asking anything.
3. Ask · check · show: entries asked one at a time, answers written under
   `A:` in his words and read back; after each check,
   `python3 tools/gates/gate.py check measurement viability` prints the
   `Question set (frame gate): k of 6 answered — still open: …` row until every entry is
   answered, then the `have:` row `Question set (frame gate): 6 of 6 answered` and
   `front matter work-type=software-change`.
4. Drive drafts `## Value`, `## Risk ledger` (≥1 `Killer? = yes` row) and
   `## Grounding` from the answers for his approval. Whether he approves
   them in this sitting is his call; the run is complete at the counted set.
5. The conductor call (Drive step 4) is exercised only if the sitting
   continues into a build. It is not required for this piece — say so at
   the gate rather than stage a call to tick it.

Commit Piece 5: `git add docs/product/measurement.md`, message body carrying
Drive's final position line verbatim, ending `Piece: funnel-driver/5`.
Keep what the run produced — the work record — exactly as it ended, open
questions and all.

**Why:** "Run it once on a real item, end to end, and keep what it produces"
is the frame's fourth bullet and the only one that proves the loop rather
than declares it. A model-answered set would pass the counter and prove
nothing (the set is the person's; the counter counts presence). The item is
one the producer already wants framed (D10), so the run is work, not a
rehearsal. Anything the run reveals about the skill text is a spec problem,
not a reason to edit the skill mid-run — hand it back.

**Verify:** `python3 tools/gates/gate.py check measurement viability | grep 'Question set'`
→ `have: docs/product/measurement.md — Question set (frame gate): 6 of 6 answered`;
`grep -c '^work-type: software-change$' docs/product/measurement.md` → `1`;
`git log -1 --format=%B | tail -1` → `Piece: funnel-driver/5`;
`python3 tools/gates/gate.py audit` → `audit: clean`.

---

### Step 13 — assembly: boxes, the conductor assertion, one render, push  [keep]

**What:** In order.

1. `git diff --stat 94f4304..HEAD -- skills/conductor/SKILL.md` → empty. If
   it is not, stop: the slice has broken the umbrella rule and nothing is
   pushed until the hunk is gone.
2. `git log 94f4304..HEAD --format=%B | grep '^Piece:' | sort` →
   `Piece: funnel-driver/1` … `/5`, one each.
3. Check boxes 1–6 in this file's `## Pieces` and commit with
   `git add docs/plans/2026-08-28-funnel-driver-spec.md`, message ending
   `Piece: funnel-driver/6`. Boxes ride a work commit, never the render
   commit (playbook, stale refuser's fifth catch).
4. `python3 tools/diagram/progress.py` (bare — this is the one place it is
   meant to write), then commit the trio with NO trailer:
   `git add docs/plans/progress.excalidraw docs/plans/progress.svg docs/plans/progress.html`,
   message `Refresh the progress render — funnel-driver reaches acceptance, measurement enters at frame`.
5. The CI suite locally, every step green:
   `python3 tools/gates/gate.py selftest && python3 tools/gates/gate.py audit && python3 tools/gates/gate.py release && python3 tools/diagram/progress.py selftest && python3 tools/design/matrix.py selftest && python3 tools/design/matrix.py audit && python3 tools/diagram/gen_journey.py check && python3 tools/diagram/progress.py stale && python3 tools/gates/fidelity.py`
6. `git push`. Then, because the version changed, conductor's close-out fires
   the release close-out pass (`/kerd:tend`, then `/kerd:slainte`) — that pass,
   not this spec, is where `kerd-map.svg`'s nine-skill count gets reported.

**Why:** D8 — every trailer moved the board, so one render at the end is the
converging commit and the push is one batch behind it. The conductor
assertion is repeated here because it is the slice's acceptance condition,
not a courtesy check. `funnel-driver` reaches `acceptance` (zero unchecked
boxes) and stops there: the acceptance record is the producer's gate, not
this spec's.

**Verify:** `python3 tools/diagram/progress.py stale` → clean, exit 0;
`python3 tools/gates/gate.py route funnel-driver | grep '^enters at:'` →
`enters at: acceptance`; `python3 tools/gates/gate.py route measurement | grep '^enters at:'`
→ `enters at: frame` or `viability` (whichever Step 12 ended at);
`git status --porcelain` → empty; `git log origin/main..HEAD` → empty after the push.
