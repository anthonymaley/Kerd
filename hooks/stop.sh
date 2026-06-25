#!/bin/bash
# Kerd Stop Hook
# Reminds about uncommitted changes and active modes when a session ends.
# Silent when there's nothing to report.
set -euo pipefail

# Stay silent if the project dir didn't resolve (env var unset or empty).
# Guard before the deref: under `set -u`, cd "$UNSET" aborts the script with an
# unbound-variable error *before* `|| exit 0` can fire. This is the path-
# resolution failure class (v0.29.1) — a hook must go quiet, never crash.
[ -n "${CLAUDE_PROJECT_DIR:-}" ] || exit 0
cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || exit 0

messages=()

# Check for uncommitted changes
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  messages+=("uncommitted changes detected")
fi

# Check for active mode
if [ -f "kivna/.active-modes" ]; then
  mode_line=$(grep '^mode:' "kivna/.active-modes" 2>/dev/null || true)
  if [ -n "$mode_line" ]; then
    mode_state="${mode_line#mode: }"
    messages+=("mode active: $mode_state")
  fi

  # Check for active dian
  dian_line=$(grep '^dian:' "kivna/.active-modes" 2>/dev/null || true)
  if [ -n "$dian_line" ]; then
    dian_state="${dian_line#dian: }"
    messages+=("dian: $dian_state")
  fi
fi

# If nothing to report, stay silent
if [ ${#messages[@]} -eq 0 ]; then
  exit 0
fi

# Build output
output="⚠ "
output+=$(printf '%s. ' "${messages[@]}" | sed 's/\. $//')
output+=". Run /switch out to wrap up."

echo "$output"
