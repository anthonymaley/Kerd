#!/usr/bin/env bash
set -euo pipefail
mkdir -p acme-billing
cd acme-billing
cat > notes.md <<'EOF'
# Invoice export notes
- Finance exports invoices as CSV every month. The export drops the VAT number column; the accountant re-types VAT numbers each month (about 2 hours).
- The export code lives in the billing service. Finance has no access to that repository.
- Billing ships on a two-week release train; their current sprint is full.
- Idea: add the VAT column to the export. The accountant's monthly import template would need its columns updated.
EOF
cat > README.md <<'EOF'
# Acme Billing

Internal notes for the billing service's invoice export.
EOF
git init -q
git add notes.md README.md
git -c user.email="eval@example.com" -c user.name="Eval Scaffold" commit -q -m "Initial notes for VAT export fix"
