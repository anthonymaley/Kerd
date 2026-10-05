---
type: regex
weight: 1
target: {source: file, path: .remote/origin.git/refs/heads/main}
match: not_contains
pattern: 'e08ff4d52ec03758209184660b6ed91b6c9f7d0c'
---
The save reached the remote: origin's main no longer points at the scaffold's pushed tip.
