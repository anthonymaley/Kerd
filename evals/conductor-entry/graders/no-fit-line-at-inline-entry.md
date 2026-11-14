---
type: regex
weight: 1
target: trace
match: not_contains
flags: m
pattern: '^\{"type":"assistant"[^\n]*?Fit ·'
---
No assistant message carries a `Fit ·` line: Fit lines go with dispatched contributors, and entering Shape dispatches none.
