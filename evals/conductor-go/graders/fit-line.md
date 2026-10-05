---
type: regex
weight: 1
target: trace
flags: m
pattern: '^\{"type":"assistant"[^\n]*?Fit ·'
---
An assistant message has a `Fit ·` line for the dispatched jobs.
