---
type: regex
weight: 1
target: {source: file, path: CONTEXT.md}
flags: i
pattern: '\d[\d,.]*\s*k?\s*(?:bytes|tokens)'
---
CONTEXT.md records the measurement (bytes or estimated tokens, "7,993 tokens" or "0.7k tokens").
