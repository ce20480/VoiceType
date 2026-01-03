#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Voice Toggle
# @raycast.mode silent
# @raycast.packageName Voice CLI

# Optional parameters:
# @raycast.icon 🎤
# @raycast.description Voice-to-text for terminal sessions. Speak and text appears in your terminal.

# Documentation:
# @raycast.author avini
# @raycast.authorURL https://github.com/avini

# Use absolute paths (~ might not expand correctly in all contexts)
VENV_PYTHON="/Users/avini/.voice-cli-venv/bin/python"
VOICE_CLI="/Users/avini/Documents/GitHub/voice-cli/bin/voice-cli"
LOG_FILE="/Users/avini/.voice-cli/raycast.log"

# Log start time
echo "=== $(date) ===" >> "$LOG_FILE"
echo "Starting voice-cli from Raycast" >> "$LOG_FILE"

# Run voice-cli (stderr goes to log, stdout is silent in normal mode)
"$VENV_PYTHON" "$VOICE_CLI" 2>> "$LOG_FILE"
EXIT_CODE=$?

# Log completion
echo "Exit code: $EXIT_CODE" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
