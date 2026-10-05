---
type: regex
weight: 1
target: {source: file, path: .git/HEAD}
pattern: '^ref: refs/heads/main\s*$'
---
The checked-out branch is still main: no concert branch was started.
