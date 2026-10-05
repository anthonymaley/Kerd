---
type: regex
weight: 1
target: {source: file, path: CONTEXT.md}
flags: i
pattern: '\d[\d,]*\s*(?:bytes|tokens)'
---
CONTEXT.md records the measurement (bytes or estimated tokens).
