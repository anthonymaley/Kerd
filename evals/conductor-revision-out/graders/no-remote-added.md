---
type: regex
weight: 1
target: {source: file, path: .git/config}
match: not_contains
pattern: '\[remote '
---
No remote was added to make a push possible: the project still has none, as the scaffold left it.
