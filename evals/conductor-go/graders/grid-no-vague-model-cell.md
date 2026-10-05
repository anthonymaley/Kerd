---
type: regex
weight: 1
target: trace
match: not_contains
flags: m
pattern: '^\{"type":"assistant"[^\n]*?\|\s*Task\s*\|\s*Who\s*\|[^\n]*?\\n\|(?! *Task)(?! *-)[^|\\]*\|(?![^|\\]*(?:[Tt]his session|[Ii]nline|[Cc]ontroller))[^|\\]*\|(?! *(?:Haiku|Sonnet|Opus|Fable)\b)[^|\\]*\|'
---
No dispatch row has a model cell that is not a concrete model (inherited, default, unknown, per definition, empty). Rows for this session itself are exempt.
