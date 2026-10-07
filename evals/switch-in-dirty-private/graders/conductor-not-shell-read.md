---
type: regex
weight: 1
target: trace
match: not_contains
pattern: '"command":"(?:[^"\\]|\\.)*\b(?:cat|sed|head|tail|less|more|awk|bat|nl|grep|rg)\b(?:[^"\\]|\\.)*/conductor/(?:SKILL\.md|references/)'
---
Ordinary In does not read Conductor's SKILL.md or its guides through the shell either (conductor-not-read covers the Read tool).
