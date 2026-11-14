---
type: regex
weight: 1
target: trace
match: not_contains
flags: m
pattern: '^\{"type":"assistant"[^\n]*?\|\s*Task\s*\|\s*Who\s*\|\s*Model[^|]*\|\s*Effort\s*\|'
---
No assistant message shows a task / who / model / effort grid. Entering Shape dispatches no contributor, so the entry is one plain line (Conductor's inline single-task entry, 0.196.0).
