---
type: regex
weight: 1
target: trace
pattern: '"tool_result","content":"(?:[^"\\]|\\.)*# Out: clean boundaries(?:(?:[^"\\]|\\.)*Without `--sync` it is local-only\.|[\s\S]*"tool_result","content":"(?:[^"\\]|\\.)*Without `--sync` it is local-only\.)'
---
The whole Out guide was read: its first heading and, later, its last sentence both came back in tool output, so a head slice fails. A separate head and tail read would still pass. The anchor sentence is checked against the guide by skills/switch/scripts/tests/test_eval_graders.py.
