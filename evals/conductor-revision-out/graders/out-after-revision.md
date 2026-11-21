---
type: regex
weight: 1
target: trace
pattern: '"name":"(?:Edit|Write)","input":\{"file_path":"[^"]*/launch-brief\.md"[\s\S]*"name":"Skill","input":\{(?=[^}]*"skill":"(?:kerd:)?switch")(?=[^}]*"args":"\s*out\b)'
---
Out started after the brief was changed, in the same turn: an Edit or Write on launch-brief.md comes before the Skill call that starts `/kerd:switch out`.
