---
type: llm
weight: 1
focus: last_message
---
The response ends on a bubble line `> 💬 **...?**` and above it has a decision block
with a Recommendation. PASS if the bubble repeats the Recommendation as the block
states it, ending "— approve?", and includes every operation the Recommendation
names (for example both what is done to `larder export` and what is released).
FAIL if the bubble is softer, smaller or narrower than the Recommendation, drops
an operation it names, is a menu of options, or there is no block-and-bubble pair.
