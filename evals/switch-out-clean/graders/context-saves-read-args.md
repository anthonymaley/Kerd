---
type: regex
weight: 1
target: {source: file, path: CONTEXT.md}
pattern: '##\s+For Kerd.s next pickup[^\n]*\n(?:(?!\n##\s)[\s\S])*?(?:read_args|"--(?:record|file|section)")(?:(?!\n##\s)[\s\S])*$'
---
CONTEXT.md saves the measured read_args selection under its "## For Kerd's next pickup" heading, the last section of the file.
