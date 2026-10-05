---
type: regex
weight: 1
target: last_message
match: not_contains
flags: i
pattern: 'SWITCH IN COMPLETE|> 💬 \*\*[^\n]*start (?:a )?conductor'
---
The final message does not repeat Switch In's arrival screen and does not ask to start Conductor again.
