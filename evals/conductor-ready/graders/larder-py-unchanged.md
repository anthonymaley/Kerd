---
type: regex
weight: 1
target: {source: file, path: larder.py}
match: not_contains
pattern: 'shop'
---
larder.py still has no shop command (nothing built through Bash either).
