---
route: new
stage: designed
---

# Progress HTML — the view you open, not the command you run

## Value

Born at the push-wiring goal gate (2026-08-04): the expert-user pass
found the pull surfaces "really manual and hard to consume quickly" — a
terminal table and a static SVG, with drill-down only via more terminal
commands. Tony's ask, verbatim: "cant we just have a HTML file that i
can view and interact with?"

Value, in units:

- **Actions to answer "where are we?"** — today: run a command and read
  a table, or hunt for the SVG (no detail either way); target: **open
  one file** — the board at a glance, any goal's detail one click away.
- **Detail on demand** — rungs' named have/need and each goal's piece
  list: today reachable only by per-slug terminal commands; target:
  **in the page**, expand on click, zero terminal.
- **Trust in what you're seeing** — today the viewer can't tell when
  the picture was derived; target: the page names the commit it was
  rendered at, and a stale page at a pushed tip goes red in CI like a
  stale SVG does.

## Risk ledger

| Risk | Killer? | Impact | Likelihood | Evidence | State | Countermeasure | Review trigger |
|---|---|---|---|---|---|---|---|
| A third surface that lies: the HTML drifts from the model while the canvas pair stays current — the view Tony actually reads becomes the one nothing checks | yes | the piece's whole value inverted: a trusted-looking page misstates position | certain without countermeasure | the staleness refuser shipped v0.78.0: single-serializer + byte-compare + depth-1 convergence proven on the real tree and in CI ×3 | countermeasure - permanent | The HTML is written by the same write path (`write_pair` grows to a trio) and joins the stale byte-compare — a stale page reds the tip exactly like a stale SVG | |
| Dashboard-itis: "interactive" creeps into controls, live refresh, a server, things that mutate | no | scope balloons; the read-only trust story breaks | medium (the pull is real — tonight's ask could grow) | tonight's conversation already reached for "interact" | countermeasure - permanent | Slice 1 is READ-ONLY by name: no server, no live refresh, nothing that writes; each excluded thing returns only through its own frame | |
| Self-contained constraint fails: interactivity needs something a bare `file://` page can't do | no | page needs serving or external deps — friction returns | low | the model is already JSON (`--json` seams on both tools); embed + vanilla JS is standard, no fetch needed when data is inlined | countermeasure - permanent | All data inlined at generation; zero external requests; acceptance includes opening via `file://` cold | |

## Goal verdict — slice 1 (2026-08-05)

Machine keys passed (contract met 4/4 pieces, fixtures 14/14, CI trio
compare green ×2, Mac↔Linux byte-identity proven). **Expert-user key
REFUSED:** the page renders the machine's model faithfully and answers a
machine's question — "it looks like a system level CI page, it means
nothing to me as a human reader" (Tony, the cold open). The route
truthfully shows this goal open; the gate schema has no refusal-record
shape (backlogged). The finding seeded the journey-view frame, which
owns this page's fate — leading option: keep the trio plumbing, replace
the page content with the human telling.

## Release slice

Smallest valuable slice: **one committed self-contained page** —
`docs/plans/progress.html`, generated from the same derived model (+ the
gate kit's named have/need), showing the board grid, every goal strip,
click-to-expand per goal (pieces + per-rung have/need), and the commit
it was rendered at. It joins the staleness byte-compare, so a lying page
cannot sit at a pushed tip unnoticed. Deliberately excluded, named: live
refresh or watch mode · any server · any control that mutates anything ·
replacing the SVG/terminal surfaces (they stay).
The slice's win: "where are we?" becomes opening a file.
