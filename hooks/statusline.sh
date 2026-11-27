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

# Claude Code feeds statusline commands a context JSON envelope on stdin. It goes to a
# private temp file, so every byte (NUL included) reaches the wrapped command and needs.py.
tmp=$(mktemp 2>/dev/null || true)
[ -n "$tmp" ] || { printf '%s\n' "$now"; exit 0; }
trap 'rm -f "$tmp"' EXIT
[ -t 0 ] || cat > "$tmp" 2>/dev/null || true

# "Needs you" segment: what waits for the person in this session's folder.
# Quiet on any error; local files only, no network.
needs=""
if [ -s "$tmp" ]; then
  here=$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd -P || true)
  helper="$here/../skills/conductor/scripts/needs.py"
  if [ -f "$helper" ] && command -v python3 >/dev/null 2>&1; then
    needs=$(python3 "$helper" show --line --status-json "$tmp" 2>/dev/null || true)
  fi
fi

head="$now"
[ -z "$needs" ] || head="$now · $needs"

rest=""
if [ -n "$inner" ]; then
  rest=$(/bin/sh -c "$inner" < "$tmp" 2>/dev/null || true)
fi

if [ -n "$rest" ]; then
  printf '%s · %s\n' "$head" "$rest"
else
  printf '%s\n' "$head"
fi
