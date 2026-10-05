---
type: regex
weight: 1
target: trace
pattern: '"file_path":"[^"]*[/\\](?:in-out|out)\.md"|"command":"(?:[^"\\]|\\.)*\b(?:cat|sed|head|tail|less|awk|bat|nl)\b(?:[^"\\]|\\.)*[/\\](?:in-out|out)\.md'
---
The Out guide was opened, by Read or by a cat/sed/head-style Bash read (in-out.md before the restructure, out.md after).
