---
type: llm
weight: 1
focus: trace
---
Switch Out has a guide, references/out.md in the switch skill, whose first line is the
heading "# Out: clean boundaries" and whose last sentence is "Without `--sync` it is
local-only." PASS if the trace shows that guide read in full after Out started: tool
output containing its first heading and, in the same or later reads, its last sentence.
FAIL if the guide was never read, was read only in part (a slice such as a head or a
range that leaves out its end), or was only named in a command without its text coming
back.
