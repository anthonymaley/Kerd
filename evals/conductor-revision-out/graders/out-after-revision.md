---
type: tool_order
weight: 1
before:
  tool: Edit
  input_match: 'launch-brief\.md'
after:
  tool: Skill
  input_match: '^(?=[\s\S]*"skill"\s*:\s*"(?:kerd:)?switch")(?=[\s\S]*"args"\s*:\s*"\s*out\b)'
---
Out started after the brief was revised, in the same turn, not before the change was made.
