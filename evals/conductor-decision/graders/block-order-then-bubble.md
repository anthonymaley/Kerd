---
type: regex
weight: 1
target: last_message
pattern: '\*\*Problem[:.]?\*\*[:.]?[\s\S]*\*\*Facts(?:[ :.,(][^*\n]{0,70})?\*\*[:.]?[\s\S]*\*\*Known options[:.]?\*\*[:.]?[\s\S]*\*\*Recommendation[:.]?\*\*[:.]?[\s\S]*\*\*Why[:.]?\*\*[:.]?[\s\S]*\*\*Cost[:.]?\*\*[:.]?[\s\S]*\*\*What we lose[:.]?\*\*[:.]?[\s\S]*\*\*Input[:.]?\*\*[:.]?[\s\S]*> 💬 \*\*'
---
The decision block comes first, in order (Problem, Facts, Known options, Recommendation, Why, Cost, What we lose, Input), and the bubble follows it.
