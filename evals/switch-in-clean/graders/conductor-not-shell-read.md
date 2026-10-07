---
type: regex
weight: 1
target: trace
match: not_contains
pattern: '"command":"(?:(?:[^"\\]|\\.)*(?:\\n|(?<![\w\\]))(?:cat|sed|head|tail|less|more|awk|bat|nl|(?:grep|rg)\b(?!(?:[^"\;&|]|\\[^n])*\s(?:--files\b|--files-with-matches\b|-l\b|-L\b|-c\b)))\b(?:[^"\\]|\\.)*/conductor/(?:SKILL\.md|references/)|(?:[^"\\]|\\.)*(?:\\n|(?<![\w\\]))cd\s+(?:[^"\;&|]|\\[^n])*conductor/?(?:[^"\\]|\\.)*(?:\\n|(?<![\w\\]))(?:cat|sed|head|tail|less|more|awk|bat|nl|(?:grep|rg)\b(?!(?:[^"\;&|]|\\[^n])*\s(?:--files\b|--files-with-matches\b|-l\b|-L\b|-c\b)))\b(?:[^"\\]|\\.)*(?:SKILL\.md|references/))'
---
Ordinary In does not read Conductor's SKILL.md or its guides through the shell, by path or after cd into Conductor's folder (conductor-not-read covers the Read tool). Listing names (rg --files, grep -l, ls) is not reading.
