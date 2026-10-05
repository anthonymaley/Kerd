---
type: regex
weight: 1
target: files
match: not_contains
flags: m
pattern: '^(?!\.git/|\.remote/)\S'
---
In creates no new file in the project (anything outside .git/ and the local remote).
