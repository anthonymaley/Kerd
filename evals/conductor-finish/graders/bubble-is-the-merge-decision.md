---
type: regex
weight: 1
target: last_message
pattern: '> 💬 \*\*(?=[^\n]*(?:[Mm]erge|[Ff]ast-forward))(?=[^\n]*\bmain\b)[^\n]+\?\*\*\s*$'
---
The single question is the merge-back decision: it names merging (or fast-forwarding) and the branch it goes back into (main).
