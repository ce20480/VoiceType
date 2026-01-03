"""
Audio recording module using sox with silence detection.
"""

import subprocess
import os
import tempfile
from pathlib import Path


def get_recording_path():
    """Get the path for temporary recording storage."""
    config_dir = Path.home() / ".voice-cli"
    config_dir.mkdir(exist_ok=True)
    return str(config_dir / "recording.wav")


def record_with_silence_detection(
    output_path=None,
    silence_duration=2.0,
    threshold="1%",
    sample_rate=16000,
    max_duration=30,
    start_immediately=True
):
    """
    Record audio from the default microphone until silence is detected.

    Args:
        output_path: Where to save the audio. Defaults to ~/.voice-cli/recording.wav
        silence_duration: Seconds of silence before stopping (default: 2.0)
        threshold: Silence threshold percentage (default: "1%" - very sensitive)
        sample_rate: Audio sample rate in Hz (default: 16000, optimal for Whisper)
        max_duration: Maximum recording time in seconds (default: 30)
        start_immediately: If True, start recording immediately without waiting for speech

    Returns:
        Path to the recorded audio file

    Raises:
        subprocess.CalledProcessError: If sox fails
        FileNotFoundError: If sox is not installed
    """
    if output_path is None:
        output_path = get_recording_path()

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Remove existing file if present
    if os.path.exists(output_path):
        os.remove(output_path)

    # sox command for macOS with silence detection
    # -d: Use default audio input device
    # -c 1: Mono channel
    # -r 16000: 16kHz sample rate (optimal for Whisper)
    cmd = [
        "sox",
        "-d",                              # Default audio device (microphone)
        "-c", "1",                         # Mono
        "-r", str(sample_rate),            # Sample rate
        output_path,                       # Output file
        "trim", "0", str(max_duration),    # Max recording duration
    ]

    # Add silence detection to stop after silence
    # This records immediately but stops after silence_duration of quiet
    cmd.extend([
        "silence",
        "1", "0.1", threshold,             # Start: need 0.1s above threshold (captures speech start)
        "1", str(silence_duration), threshold  # Stop after silence_duration below threshold
    ])

    try:
        # Use timeout to prevent hanging forever
        subprocess.run(cmd, check=True, capture_output=True, timeout=max_duration + 5)
    except subprocess.TimeoutExpired:
        # Recording timed out - file should still exist
        pass
    except FileNotFoundError:
        raise FileNotFoundError(
            "sox is not installed. Run: brew install sox"
        )
    except subprocess.CalledProcessError as e:
        # sox returns non-zero if interrupted, which is fine
        if not os.path.exists(output_path):
            raise

    return output_path


def record_fixed_duration(output_path=None, duration=5.0, sample_rate=16000):
    """
    Record audio for a fixed duration.

    Args:
        output_path: Where to save the audio
        duration: Recording duration in seconds
        sample_rate: Audio sample rate in Hz

    Returns:
        Path to the recorded audio file
    """
    if output_path is None:
        output_path = get_recording_path()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if os.path.exists(output_path):
        os.remove(output_path)

    cmd = [
        "sox",
        "-d",
        "-c", "1",
        "-r", str(sample_rate),
        output_path,
        "trim", "0", str(duration)
    ]

    subprocess.run(cmd, check=True, capture_output=True)
    return output_path
