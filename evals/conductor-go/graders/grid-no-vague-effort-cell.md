---
type: regex
weight: 1
target: trace
match: not_contains
flags: m
pattern: '^\{"type":"assistant"[^\n]*?\|\s*Task\s*\|\s*Who\s*\|[^\n]*?\\n\|(?! *Task)(?! *-)[^|\\]*\|(?![^|\\]*(?:[Tt]his session|[Ii]nline|[Cc]ontroller))[^|\\]*\|[^|\\]*\|(?! *(?:low|medium|high|xhigh|max|[Nn]ot supported|[Uu]nset)\b)[^|\\]*\|'
---
No dispatch row has an effort cell that is not a concrete level (or `not supported` / `unset and unverified`). Rows for this session itself are exempt.
