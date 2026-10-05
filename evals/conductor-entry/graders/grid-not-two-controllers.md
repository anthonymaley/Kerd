---
type: regex
weight: 1
target: trace
match: not_contains
flags: m
pattern: '^\{"type":"assistant"[^\n]*?\\n\|[^\\]*?(?:Controller|This session)[^\\]*(?:\\n\|[^\\]*)*?\\n\|[^\\]*?(?:Controller|This session)'
---
The grid does not carry two controller rows (rows for work this session does itself).
