#!/bin/bash
# Kerd UserPromptSubmit Hook — focus mode
# When focus is ON for this repo (kivna/.focus contains "on"), inject the
# partner-mode working agreement so it rides every prompt. Silent otherwise.
# Per-repo toggle, default off — flip with /kerd:focus on|off.
set -euo pipefail

# Guard before the deref (v0.29.1 path-resolution class): a hook must go quiet,
# never crash, when CLAUDE_PROJECT_DIR is unset or empty.
[ -n "${CLAUDE_PROJECT_DIR:-}" ] || exit 0

focus_file="$CLAUDE_PROJECT_DIR/kivna/.focus"
[ -f "$focus_file" ] || exit 0
grep -qi '^on' "$focus_file" || exit 0

echo "Partner mode: rapid back-and-forth; keep reasoning to yourself unless it changes the user's decision or you're stuck; ask ONE question — open by default, multiple choice only when it clarifies a real choice that's the user's to make (2-4 crisp, distinct options; never a lazy binary you should just decide yourself, never vague or verbose); interrupt early to ask or flag - do not work alone then dump."
