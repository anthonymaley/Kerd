---
type: regex
weight: 1
target: trace
pattern: '"file_path":"[^"]*[/\\](?:in-out|in)\.md"|"command":"(?:[^"\\]|\\.)*\b(?:cat|sed|head|tail|less|awk|bat|nl)\b(?:[^"\\]|\\.)*[/\\](?:in-out|in)\.md'
---
The In guide was opened, by Read or by a cat/sed/head-style Bash read (in-out.md before the restructure, in.md after).
