---
type: regex
weight: 1
target: {source: file, path: TODO.md}
match: not_contains
pattern: '- \[ \] Colour the expiry warnings'
---
TODO.md no longer lists the finished item "Colour the expiry warnings" as an open `- [ ]` row.
