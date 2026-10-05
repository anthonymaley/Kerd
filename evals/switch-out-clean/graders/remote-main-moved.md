---
type: regex
weight: 1
target: {source: file, path: .remote/origin.git/refs/heads/main}
match: not_contains
pattern: 'a0dd36e9f1c5e9164039fb99d05db703342a0bdb'
---
The save reached the remote: origin's main no longer points at the scaffold's pushed tip.
