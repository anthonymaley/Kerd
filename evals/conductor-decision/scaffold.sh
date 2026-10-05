#!/usr/bin/env bash
set -euo pipefail
cat > notes.md <<'EOT'
# Larder 0.5.0 notes
- `larder export` (writes pantry.csv) has no tests and, from reading the code on 2026-10-01, breaks on item names that contain a comma. Nobody has run it on real data since 0.2.0.
- Idea (Claude, 2026-10-02): delete `larder export` and ship 0.5.0 with only `list` and `shop`. Saves about half a day of fixing it.
- Ruling (Anthony, 2026-09-14): a released command is never removed without a deprecation release first (the command still works and prints a warning for one release).
- One forum message (2026-09-29, a single user): "I use export to feed my spreadsheet every Sunday." It is the only feedback on export so far. Larder has no telemetry, so nobody knows how many people use it.
EOT
