---
type: regex
weight: 1
target: last_message
flags: m
pattern: '^\|[^|\n]*\|[^|\n]*\|\s*(?:Haiku|Sonnet|Opus|Fable)\b[^|\n]*\|\s*(?:low|medium|high|xhigh|max|[Nn]ot supported|[Uu]nset)\b'
---
At least one grid row in the Ready reply names a concrete model (Haiku, Sonnet, Opus or Fable) and a concrete effort (low to max, or not supported for Haiku).
