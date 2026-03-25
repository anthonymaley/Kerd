#!/bin/bash
# Kerd Mode Demo — Recording Cheat Sheet
#
# This script is a helper, not the demo itself. It starts asciinema
# and drops you into a shell where you run Claude Code manually.
#
# The recording captures everything in your terminal including
# Claude Code's interactive UI.
#
# HOW TO USE:
#   1. Run: ./scripts/demo-mode.sh
#   2. Follow the steps below inside the recording
#   3. Type 'exit' when done — asciinema saves automatically
#
# RECORDING STEPS:
#
#   A. Intro (type these lines so they appear in the recording):
#      echo ""
#      echo "  ╔═════════════════════════════════════════════════╗"
#      echo "  ║  Kerd: /mode strategy — interactive walkthrough ║"
#      echo "  ╚═════════════════════════════════════════════════╝"
#      echo ""
#
#   B. Start Claude Code:
#      claude
#
#   C. In Claude Code, type:
#      /kerd:mode strategy
#
#   D. Claude will:
#      - Show core skills (all ✓)
#      - Show discovered extras
#      - Present phase selection (Setup, Define, Analyze, Decide, Capture)
#      - Each phase is a checkbox question — select/deselect steps
#      - Ask for session instructions — pick one or type custom
#      - Show final summary and ask to confirm
#
#   E. Walk through each prompt naturally. Take your time.
#      The recording is more useful slow than fast.
#
#   F. After confirming the flow, type /exit to leave Claude Code
#
#   G. Type 'exit' to stop the recording
#
# The .cast file can be played back with:
#   asciinema play docs/demo-mode.cast
#
# Or uploaded to asciinema.org for embedding.

CAST_FILE="docs/demo-mode.cast"

echo ""
echo "  Starting asciinema recording..."
echo "  Output: $CAST_FILE"
echo "  Type 'exit' when done to stop recording."
echo ""

# idle_time_limit caps gaps between keystrokes in playback
# so pauses don't drag on forever
asciinema rec \
    --idle-time-limit 3 \
    --title "Kerd /mode strategy — interactive workflow routing" \
    "$CAST_FILE"

echo ""
echo "  Recording saved to $CAST_FILE"
echo "  Play:   asciinema play $CAST_FILE"
echo "  Upload: asciinema upload $CAST_FILE"
echo ""
