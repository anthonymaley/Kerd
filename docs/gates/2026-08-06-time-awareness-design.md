---
route: new
stage: designed
---

# Design GO — time-awareness slice 1 (honest actuals), 2026-08-06

**Clock:** 2026-08-06 15:17 EDT

Zero-correction GO. The canvas round ran on the shared Excalidraw
scene (one clobber recovered — the two-tab last-writer-wins gotcha
fired once and the single-tab rule fixed it); Tony's verdict: "good to
go", and the scene diff confirmed it — 47/47 elements, type census
identical to the generator's output, zero foreign elements.

The Clock line above is this record dogfooding its own design: the
schema addition ships in the build, but the shape is exercised here
first, written in the same turn as a `date` run per the rule it
records.

Package: `docs/design/time-awareness.md` +
`docs/design/time-awareness.excalidraw` (generator:
`tools/diagram/gen_time_awareness.py`). Every stage-1 measurement has
a named answer (design doc, Measurements section — six, each with the
command and expected shape).

Design facts that bound the build:

- The same-turn rule is defined ONCE in `docs/state-contract.md`;
  skills carry pointers (single-definition law).
- All four `.active-modes` readers are prefix-greps — the marker
  stamp is proven safe against the live hook scripts, and stop.sh
  echoes the stamp to the human for free.
- The statusline slot on this machine is occupied (scorched-earth's
  wrapper) — the script composes via an optional chained-command
  argument, never claims the slot.
- No retrofits: `docs/gates/*` untouched by the build; Clock lines
  appear in new records only.

Hands to CONTRACT.
