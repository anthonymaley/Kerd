# Switch In: a plain-English open-work view with one recommendation

## Where this stands

**Built and reviewed, not yet released (0.135.0).** Direction agreed by Anthony
2026-09-18 10:11. Suite green at 738 tests; `gate.py release` clean. The commit and
push wait for Anthony's yes.

**Review, 2026-09-18 10:29.** A fresh Claude reviewer (requested Opus 5 through
`kerd:effort-high`; observed model not read) took the place of Codex, which had no
tokens until 2026-09-19. It found **no authority holes**. Fixed:

- **Medium-high:** a nothing-open arrival written as `null`/`null`, as the guide
  instructs, fell back to the old grid with NOW and THIS SESSION. The layout is now
  chosen by key presence. The new test fails on the old condition (negative
  control run) and passes on the fix.
- **Medium:** "the Switch In approval line" survived in `execution.md` and twice in
  `journey.md`, the reading this change forbids. Now "arrival question".
- **Low-medium:** stale grid/NOW wording in `journey.md`'s entry paragraph (it now
  links the answer mapping), `session-succession.md`, README's Day-to-day line, and
  the old ruling's index line in `decisions.md` (now marked superseded in part).
- **Low:** the terminal Team line and a long project name overflowed the width (now
  wrapped, never cut); a `why` with no recommendation printed an orphan reason (now
  suppressed). Tests added for each.

Left as recorded gaps, not defects: the new authority sentences in `in-out.md` have no
text guard, and "weigh every open item" is model judgment with no mechanical check.
**Not yet observed on a real arrival**; the first real Switch In on 0.135.0 is the test.

## Why

At the 2026-09-18 09:58 Switch In, NOW carried "take the assistant-side byte-identity
reading", because the previous Out had saved it as the proposed continuation. It
carried no reason that mattered to Anthony, and the product work (the launch sequence
at 0 of 5) sat behind the *Open work* link. His words:

- 10:07 — "i dont care about the screen being unchnaged or not - that makes no sense.
  switch in need to tell me what happens next and why, not just put up text from last
  session byte identical"
- 10:08, after a plain list of open work with one recommendation — "yes this is
  better. plain english open work view with recommendation"
- 10:11 — "yes" to the direction below, including the new closing question.

The byte-identity item was dropped the same morning:
`docs/work/question-pickers/work.md`.

## Agreement

- In weighs every open item, the saved next step included: does it move the product,
  and why would it come first? A saved step is a candidate, never repeated because it
  was saved. Work that only proves Kerd's own mechanics does not lead unless it blocks
  product work or the person chose it.
- The screen says, in plain English: where things stand, last session, the open work
  one line each, one recommendation and why, a compact team line, attention and links.
  No status grid, no NOW list.
- The closing question becomes **"What do you want this session to move forward?"**,
  with the recommendation as its proposed answer. It replaces "Start a Conductor
  session?" (2026-09-14 ruling, superseded in part).
- Kept from that ruling: every answer that chooses work enters Conductor, so guidance
  has one way in; choosing work, a plain yes included, opens Shape for it and never
  approves its operations; "not now" starts nothing.
- Before → after view: `before-after.html` beside this record.

## What changed

- `skills/switch/references/in-out.md` — *Compose the arrival* (weighing), *Enter
  Conductor from the answer* (replaces *after the ordinary offer*), *Welcome back*
  (new layout, example, keys), and Out saving the selection's reason.
- `skills/switch/scripts/where_we_are.py` — a second arrival layout chosen when the
  summary carries `open_work` or `recommendation`; `OPEN_WORK_KEYS`. The grid layout
  stays for record-driven views and older callers.
- `skills/switch/SKILL.md`, `skills/conductor/SKILL.md`,
  `skills/conductor/references/journey.md` — the new question and its entry mapping.
- Tests: `test_where_we_are.py` (documented-example tests moved to the new layout,
  new layout cases, legacy grid still guarded), `test_question_form.py` (exemption and
  picker wording).
- `README.md`, `docs/decisions.md`, version 0.135.0.

## 0.136.0: the first real arrival, and what it corrected

**Observed 2026-09-18 10:40**, the first arrival produced by 0.135.0 (the plugin
cache had updated). The weighing held: the recommendation led with product work and
a reason, not the saved self-check. Anthony's verdict at 10:48 named five defects:

1. "nothing is being built" was agent state, not product language he could use;
2. the grid was gone, and the loose text made the page long and hard to scan;
3. the closing question has to be "Start a Conductor session?", or an answer can
   skip Conductor;
4. drop the `updated … · rendered …` footer and the END OF PICKUP marker;
5. the question can carry a picker: "yes" and "something else".

**Agreed 10:51**, "yes this is it", against `arrival-grid.html` (today beside
proposed), with one change: the grid's second column is the phase, "design, build,
loop etc". It was built as the recommended item's rung on the project's ladder
(frame … acceptance). Stated to him as the default, to push back on if he meant
Conductor's own stages.

**Built:** the renderer's arrival opens with `PROJECT | PHASE | NEXT | TEAM`, drops
the Team line (now in the grid), shows documents on one line, and ends on the question
with no footer or end marker; the older record-driven grid keeps its footer. The guide
asks for product English and names work by what it changes. The picker is exactly
"Yes — <the recommended work>" and "Something else"; both open Conductor. `source`
and `updated` left the arrival's keys. Tests moved to the new layout: the question
ends the screen, no footer, grid first with phase and next. 738 tests before the
test edits: 8 failed, all pinning the old screen.

## Open

- Observe the first real 0.136.0 arrival: is the grid readable in chat, is "where
  things stand" product language, and does "Something else" still reach Conductor?
- The weighing is model judgment against a stated test ("does it move the product?"),
  with no mechanical check. It can fail: an arrival that leads with a self-check
  nobody asked for fails it.
