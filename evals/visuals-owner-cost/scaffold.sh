#!/usr/bin/env bash
set -euo pipefail
cat > notes.md <<'EOF'
# Invoice export notes
- Today: finance can export invoices as CSV, but the export drops the VAT number column, so the accountant re-types it every month (about 2 hours).
- The export is owned by the billing team (Priya); finance cannot change it.
- Proposed fix: add the VAT column to the export. Billing estimates half a day, plus one release; the accountant's monthly import template must be updated once.
EOF
