---
type: regex
weight: 1
target: trace
flags: m
pattern: '^\{"type":"assistant"[^\n]*?\\n\|[^|\\]*\|[^|\\]*\|\s*(?:Haiku|Sonnet|Opus|Fable)\b[^|\\]*\|\s*(?:low|medium|high|xhigh|max|[Nn]ot supported|[Uu]nset)\b'
---
At least one grid row names a concrete model (Haiku, Sonnet, Opus or Fable) and a concrete effort (low to max, or not supported for Haiku).
