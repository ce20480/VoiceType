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

# Run voice-cli and capture output
"$VENV_PYTHON" "$VOICE_CLI" 2>&1 | tee -a "$LOG_FILE"

# Log completion
echo "Completed with exit code: $?" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
