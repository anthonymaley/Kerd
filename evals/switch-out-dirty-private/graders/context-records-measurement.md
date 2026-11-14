---
type: regex
weight: 1
target: {source: file, path: CONTEXT.md}
flags: i
pattern: '##\s+For Kerd.s next pickup[^\n]*\n(?:(?!\n##\s)[\s\S])*?\d[\d,.]*\s*k?\s*(?:bytes|tokens)(?:(?!\n##\s)[\s\S])*$'
---
CONTEXT.md records the measurement (bytes or estimated tokens, "7,993 tokens" or "0.7k tokens") under its "## For Kerd's next pickup" heading, where the person can skip it; that section is the file's last.
