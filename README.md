# VoiceType

Voice-to-text for terminal sessions. Speak and text appears at your cursor.

## Features

- **Auto-stop recording** - Silero VAD neural network detects when you stop speaking
- **Local transcription** - Uses faster-whisper, no API keys needed
- **Enter trigger** - Say "send" or "enter" at the end to auto-submit
- **Number conversion** - "one" → "1" for easy option selection

## Requirements

- macOS (uses osascript for typing)
- Python 3.10+
- Homebrew

## Install

```bash
git clone https://github.com/ce20480/VoiceType.git
cd VoiceType
./setup.sh
```

## Setup Raycast Hotkey

1. Open Raycast → Settings → Extensions → Script Commands
2. Add script directory: `/path/to/VoiceType/raycast`
3. Assign hotkey to "Voice Toggle" (recommended: `Ctrl+Opt+V`)

### Permissions

Grant Raycast these permissions in System Settings → Privacy & Security:
- **Microphone** - for recording
- **Accessibility** - for typing keystrokes

## Usage

1. Press hotkey → hear "Ping"
2. Speak your text
3. Stop speaking → hear "Pop" → text appears
4. Say "send" at the end to also press Enter

## Configuration

Edit `~/.voice-cli/config.yaml`:

```yaml
model: base.en          # tiny.en, base.en, small.en, medium.en, large-v3
silence_duration: 2.0   # seconds of silence before stopping
vad_threshold: 0.5      # speech detection sensitivity (0-1)
auto_enter: true        # enable "send"/"enter" trigger words
sound_feedback: true    # play Ping/Pop sounds
```

## CLI Options

```bash
voice-cli --debug       # print output instead of typing
voice-cli --no-vad      # fixed 5s recording instead of auto-stop
voice-cli --no-enter    # disable enter trigger words
voice-cli --model small.en  # use different model
```

## Troubleshooting

**No text appears after speaking:**
- Check Raycast has Microphone + Accessibility permissions
- Run `voice-cli --debug` from terminal to see errors

**First words cut off:**
- VAD model loads before recording starts, should not happen
- Check `~/.voice-cli/raycast.log` for errors

## License

MIT
