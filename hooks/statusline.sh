#!/bin/bash
# Kerd statusline segment — the wall clock, composed not claimed.
# Prints HH:MM. Given an existing statusline command as $1, prints
# "HH:MM · <that command's output>", forwarding the context JSON that Claude
# Code puts on stdin, so an occupied statusLine slot keeps working.
# Machine-local, opt-in wiring — see README (Hooks). Not a hook event: it is
# registered under `statusLine`, never under `hooks`.
set -euo pipefail

# A statusline runs on every update. It must go quiet, never crash — the
# path-resolution failure class (v0.29.1) governs here exactly as in hooks.
now=$(date '+%H:%M' 2>/dev/null || true)
[ -n "$now" ] || exit 0

inner="${1:-}"
if [ -z "$inner" ]; then
  printf '%s\n' "$now"
  exit 0
fi

# Claude Code feeds statusline commands a context JSON envelope on stdin.
# Read it once, hand it to the wrapped command unchanged.
payload=$(cat 2>/dev/null || true)
rest=$(printf '%s' "$payload" | /bin/sh -c "$inner" 2>/dev/null || true)

if [ -n "$rest" ]; then
  printf '%s · %s\n' "$now" "$rest"
else
  printf '%s\n' "$now"
fi
