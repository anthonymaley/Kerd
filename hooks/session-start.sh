#!/bin/bash
# Kerd SessionStart Hook
# Surfaces stale state on same-machine resume: remote drift, last session date,
# and interrupted mode. Silent when there's nothing to report.
set -euo pipefail

# Stay silent if the project dir didn't resolve (env var unset or empty).
# Guard before the deref: under `set -u`, cd "$UNSET" aborts the script with an
# unbound-variable error *before* `|| exit 0` can fire. This is the path-
# resolution failure class (v0.29.1) — a hook must go quiet, never crash.
[ -n "${CLAUDE_PROJECT_DIR:-}" ] || exit 0
cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || exit 0

# Must be a git repo with Kerd structure
[ -d ".git" ] || exit 0
[ -d "kivna" ] || exit 0

messages=()

# Check if local is behind remote
fetch_output=$(git fetch --dry-run 2>&1 || true)
if echo "$fetch_output" | grep -q '\->'; then
  behind_count=$(git rev-list --count 'HEAD..@{u}' 2>/dev/null || echo "0")
  if [ "$behind_count" -gt 0 ]; then
    messages+=("local is behind remote ($behind_count commits)")
  fi
fi

# Read last session date from TODO.md
if [ -f "TODO.md" ]; then
  session_line=$(grep -m1 '## Current Session' "TODO.md" 2>/dev/null || true)
  if [ -n "$session_line" ]; then
    # Look for date on the next line (e.g., "(completed 2026-04-04)")
    date_line=$(grep -A1 '## Current Session' "TODO.md" | tail -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' || true)
    if [ -n "$date_line" ]; then
      messages+=("last session: $date_line")
    fi
  fi
fi

# Check for interrupted mode (same-machine only)
if [ -f "kivna/.active-modes" ]; then
  mode_line=$(grep '^mode:' "kivna/.active-modes" 2>/dev/null || true)
  if [ -n "$mode_line" ]; then
    mode_state="${mode_line#mode: }"
    messages+=("mode interrupted: $mode_state")
  fi
fi

# If nothing to report, stay silent
if [ ${#messages[@]} -eq 0 ]; then
  exit 0
fi

# Build output
output="📋 "
first=true
for msg in "${messages[@]}"; do
  if [ "$first" = true ]; then
    # Capitalize first message
    output+="$(echo "${msg:0:1}" | tr '[:lower:]' '[:upper:]')${msg:1}"
    first=false
  else
    output+=". $(echo "${msg:0:1}" | tr '[:upper:]' '[:lower:]')${msg:1}"
  fi
done

# Add suggestion if behind remote or mode interrupted
if echo "${messages[*]}" | grep -qE 'behind remote|mode interrupted'; then
  output+=". Run /switch in to sync and pick up."
fi

echo "$output"
