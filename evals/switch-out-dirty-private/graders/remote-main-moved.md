---
type: regex
weight: 1
target: {source: file, path: .remote/origin.git/refs/heads/main}
match: not_contains
pattern: '6e1224e59790b9cf2588994664ccd7a6d7caa9de'
---
The save reached the remote: origin's main no longer points at the scaffold's pushed tip.
