---
type: regex
weight: 1
target: last_message
flags: m
pattern: '^[ \t]*\|[^|\n]*\|[^|\n]*\|\s*(?:(?:Sonnet|Opus|Fable)\b[^|\n]*\|\s*(?:low|medium|high|xhigh|max|unset and unverified)\b|Haiku\b[^|\n]*\|\s*[Nn]ot supported\b)'
---
At least one grid row in the Ready reply names a concrete model and a valid effort for it: Sonnet, Opus or Fable with low to max (or "unset and unverified"), or Haiku with "not supported".
