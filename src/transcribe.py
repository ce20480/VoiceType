"""
Transcription module using faster-whisper for local speech-to-text.
"""

import os
from typing import Optional


class Transcriber:
    """
    Lazy-loading transcriber using faster-whisper.

    The model is loaded once on first use and reused for subsequent calls.
    Uses int8 quantization for faster inference on CPU.
    """

    _model = None
    _current_model_name = None

    @classmethod
    def get_model(cls, model_name: str = "base.en"):
        """
        Get or create the Whisper model.

        Args:
            model_name: Model to use. Options:
                - tiny.en: Fastest, least accurate (~75MB)
                - base.en: Fast, good accuracy (~150MB) [DEFAULT]
                - small.en: Balanced (~244MB)
                - medium.en: More accurate, slower (~769MB)
                - large-v3: Most accurate, slowest (~1.5GB)

        Returns:
            WhisperModel instance
        """
        if cls._model is None or cls._current_model_name != model_name:
            from faster_whisper import WhisperModel

            cls._model = WhisperModel(
                model_name,
                device="cpu",
                compute_type="int8"  # Faster inference with quantization
            )
            cls._current_model_name = model_name

        return cls._model

    @classmethod
    def transcribe(
        cls,
        audio_path: str,
        model_name: str = "base.en",
        language: Optional[str] = "en"
    ) -> str:
        """
        Transcribe an audio file to text.

        Args:
            audio_path: Path to the audio file (WAV recommended)
            model_name: Whisper model to use
            language: Language code (default: "en" for English)

        Returns:
            Transcribed text as a string

        Raises:
            FileNotFoundError: If audio file doesn't exist
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        model = cls.get_model(model_name)

        # Transcribe with VAD filtering to skip silence
        segments, info = model.transcribe(
            audio_path,
            beam_size=5,
            language=language,
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=500,  # Minimum silence to split on
                speech_pad_ms=200             # Padding around speech segments
            )
        )

        # Combine all segments into a single string
        text = " ".join(segment.text.strip() for segment in segments)

        return text.strip()

    @classmethod
    def transcribe_with_timestamps(
        cls,
        audio_path: str,
        model_name: str = "base.en"
    ) -> list:
        """
        Transcribe audio and return segments with timestamps.

        Returns:
            List of dicts with 'start', 'end', and 'text' keys
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        model = cls.get_model(model_name)

        segments, info = model.transcribe(
            audio_path,
            beam_size=5,
            language="en",
            vad_filter=True
        )

        return [
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            }
            for segment in segments
        ]
