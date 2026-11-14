#!/bin/bash
# Kerd PostToolUse Hook (Skill matcher)
# Read-only: reminds about mode progress when a skill completes.
# Does NOT mutate .active-modes. A mode block found there is legacy state.
# Silent when no mode is active or the skill doesn't match the current step.
# No external dependencies (no jq — pure bash/sed).
set -euo pipefail

# Stay silent if the project dir didn't resolve (env var unset or empty).
# Guard before the deref: under `set -u`, cd "$UNSET" aborts the script with an
# unbound-variable error *before* `|| exit 0` can fire. This is the path-
# resolution failure class (v0.29.1) — a hook must go quiet, never crash.
[ -n "${CLAUDE_PROJECT_DIR:-}" ] || exit 0
cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || exit 0

# Only proceed if a mode is active
[ -f "kivna/.active-modes" ] || exit 0

mode_line=$(grep '^mode:' "kivna/.active-modes" 2>/dev/null || true)
[ -n "$mode_line" ] || exit 0

# Read the completed skill invocation from stdin (PostToolUse provides tool_input)
# Payload is a full envelope: {session_id, tool_name, tool_input: {skill, args}, tool_response: {success}, ...}
# Parse without jq: extract fields with sed
input=$(cat)

# Only report progress on successful skill runs
echo "$input" | grep -q '"success"[[:space:]]*:[[:space:]]*true' || exit 0

# Extract skill name from tool_input.skill
skill_name=$(echo "$input" | sed -n 's/.*"skill"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
[ -n "$skill_name" ] || exit 0

# Extract args if present: find "args":"value" or "args": "value"
skill_args=$(echo "$input" | sed -n 's/.*"args"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

# Build the concrete invocation to match against the step
# e.g., "kerd:switch in" or "gsd:discuss-phase 1"
if [ -n "$skill_args" ]; then
  completed_invocation="$skill_name $skill_args"
else
  completed_invocation="$skill_name"
fi

# Find the [current] step
current_step=$(grep '\[current\]' "kivna/.active-modes" 2>/dev/null || true)
[ -n "$current_step" ] || exit 0

# Extract concrete command from current step
# Format: "N: /plugin:skill [args] | label [current]"
# Extract everything between "N: " and " | " then strip leading /
current_command=$(echo "$current_step" | sed -E 's/^[[:space:]]*[0-9]+:[[:space:]]*//' | sed -E 's/[[:space:]]*\|.*$//' | sed 's|^/||' | xargs)

# Exact match: completed invocation must equal the current step's concrete command
if [ "$completed_invocation" != "$current_command" ]; then
  exit 0
fi

# Extract mode state
mode_state="${mode_line#mode: }"
instruction=$(grep '^  instruction:' "kivna/.active-modes" 2>/dev/null | sed 's/^  instruction: //' || true)

# Find next pending step
next_step=$(grep '\[pending\]' "kivna/.active-modes" 2>/dev/null | head -1 || true)

if [ -n "$next_step" ]; then
  next_id=$(echo "$next_step" | sed -E 's/^[[:space:]]*([0-9]+):.*/\1/')
  next_label=$(echo "$next_step" | sed -E 's/^[^|]*\|[[:space:]]*//' | sed -E 's/[[:space:]]*\[pending\]//')
  next_skill=$(echo "$next_step" | sed -E 's/^[[:space:]]*[0-9]+:[[:space:]]*//' | sed -E 's/[[:space:]]*\|.*$//' | xargs)

  output="✓ Step complete: /$current_command"
  if [ -n "$instruction" ]; then
    output+="\n  Instruction: $instruction"
  fi
  output+="\n  Next: step $next_id — $next_skill ($next_label)"
else
  output="✓ Final step complete: /$current_command"
  output+="\n  Mode finishing: $mode_state"
fi

echo -e "$output"
