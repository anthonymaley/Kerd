---
type: tool_used
weight: 1
tool: Bash
input_match: '"command":"(?:[^"\\]|\\.)*(?:git\s+(?:-C\s+\S+\s+)?add\s+(?:-A|--all|-u|\.(?=\s|$|\\|"))|git\s+(?:-C\s+\S+\s+)?add\s[^;&|\\]*scratch\.patch|--file[\s=]+\S*scratch\.patch)'
max: 0
min: 0
arm: both
---
scratch.patch is never staged or named in a save, and nothing is blanket-staged (git add -A/./-u).
