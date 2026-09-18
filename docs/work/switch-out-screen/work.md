# Switch Out: a plain-English closing screen

## Where this stands

**Built 2026-09-18, awaiting review and Anthony's yes to commit** as Kerd 0.138.0.

## Why

After 0.136.0 tightened Switch In, Anthony (15:35): "lets take a quick look at
switch out display - we tightened up switch in lets do the same for OUT". The
closing box had eleven labelled parts, all save mechanics, and never said what the
session achieved or why the next step mattered.

## Agreement

- 15:37, Anthony: "yes like it", against `closing-grid.html` (today beside
  proposed), with one change: the closing line becomes "Exit and restart or /clear
  and /switch in to pick up from here".
- Written as "/kerd:switch in" (the release gate requires the prefix on Kerd's
  commands). Under Codex the line names no Claude command ("Exit and restart, then
  switch in to pick up from here"), because an existing test kept the closing
  line host-neutral and Switch runs under both.

## What changed

- `skills/switch/scripts/where_we_are.py` `render_closing`: grid (PROJECT, SAVED,
  PHASE, NEXT), This session, Next time with Why, Attention only for a real
  problem (save not on the remote, memory not ready or unrecorded, a dirty tree,
  warnings), one closing line, no render time. New keys `phase`, `this_session`,
  `why`, `warnings`, `host`; `commit`, `files`, `remote`, `local_only`, `closed`,
  `reading_set`, `measured`, `log` left the box and stay in the records.
- Guide `in-out.md` closing section and example; `SKILL.md`; the Agent succession
  guide (a failed designation goes to `warnings`); README.
- Tests: the closing box tests rewritten. Every save-failure guard kept: restart
  offered only after a confirmed save with memory ready, unknown never read as
  "nothing committed". Negative control: the new closing tests against the
  0.137.1 renderer, 113 failures.

## Open

- Observe the first real closing box, this sitting's own Switch Out.
