---
type: regex
weight: 1
target: trace
flags: m
pattern: '^\{"type":"assistant"[^\n]*?Conductor · Shape [—–-][^\\]*(?:[Ss]hopping|larder shop|`shop`)'
---
Some assistant message carries the entry line `Conductor · Shape — <activity>` and the activity names the chosen work (the shopping list). The stage is Shape: choosing work in answer to Switch In's question is not approval of its operations.
