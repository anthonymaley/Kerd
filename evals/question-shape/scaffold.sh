#!/usr/bin/env bash
set -euo pipefail
cat > notes.md <<'EOF'
# Shop notes
- Catalogue sync took 9 s once, 2026-09-24 14:02, while a full disk backup was running. Normal runs have not been timed.
- Idea (Claude, 2026-09-24): keep a local copy of the catalogue so the page shows the last copy at once and refreshes in the background. About two days of work.
- Ruling (Anthony, 2026-09-10): the catalogue is always read fresh; never show a stale copy.
EOF
