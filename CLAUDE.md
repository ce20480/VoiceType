# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VoiceType is a macOS voice-to-text tool for terminal sessions. Press a hotkey, speak, and text appears at your cursor. Uses Silero VAD for intelligent speech detection and faster-whisper for local transcription.

## Commands

```bash
# Install/setup
./setup.sh

# Run directly (uses venv)
~/.voice-cli-venv/bin/python bin/voice-cli

# Debug mode (prints instead of typing)
~/.voice-cli-venv/bin/python bin/voice-cli --debug

# Test with fixed duration (bypass VAD)
~/.voice-cli-venv/bin/python bin/voice-cli --no-vad --duration 3
```

No test suite exists yet.

## Architecture

```
Raycast hotkey → voice-toggle.sh → bin/voice-cli
                                        ↓
                              vad_record.py (Silero VAD)
                                        ↓
                              transcribe.py (faster-whisper)
                                        ↓
                              number_words.py (optional)
                                        ↓
                              output.py (clipboard + osascript paste)
```

### Key Data Flow

1. **Recording**: `vad_record.py` uses PyAudio + Silero VAD to record until silence (32ms chunks, 512 samples at 16kHz)
2. **Transcription**: `transcribe.py` uses faster-whisper with lazy-loaded model (int8 quantization on CPU)
3. **Output**: `output.py` copies to clipboard, activates original app, pastes via Cmd+V (required because Raycast becomes frontmost)

### Critical Implementation Details

- **VAD chunk size**: Silero VAD requires exactly 512 samples at 16kHz (32ms). Other sizes will error.
- **Model pre-loading**: VAD model must load BEFORE the Ping sound plays, otherwise first words get missed
- **Async sound**: `play_sound()` uses `subprocess.Popen` (not `.run`) to avoid blocking recording start
- **Enter triggers**: `check_enter_trigger()` strips punctuation (`.!?,;:`) before checking for "send"/"enter" because Whisper adds trailing punctuation

### Configuration

User config: `~/.voice-cli/config.yaml`
Logs: `~/.voice-cli/raycast.log`
Temp audio: `~/.voice-cli/recording.wav`

## macOS Permissions

Raycast needs both Microphone and Accessibility permissions (not the terminal) because Raycast spawns the subprocess.
