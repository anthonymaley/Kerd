---
type: tool_used
weight: 1
tool: Bash
input_match: '"command":"(?:[^"\\]|\\.)*(?:\bsave\b|\bgit\b(?:[^"\\]|\\.)*\b(?:add|commit)\b)(?:[^"\\]|\\.)*launch-brief\.md'
min: 0
max: 0
---
Out does not save the brief before the person answers: no helper save or git add/commit names launch-brief.md. Out keeps its own save authority, and the person's own files are asked about first.
