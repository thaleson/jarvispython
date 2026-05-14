from faster_whisper import WhisperModel

from app.core.logger import logger


class AudioTranscriber:
    def __init__(self):
        logger.info("Loading Whisper model...")

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
        )

    def transcribe(
        self,
        audio_path: str,
    ) -> str:
        logger.info(f"Transcribing audio: {audio_path}")

        segments, _ = self.model.transcribe(
            audio_path,
            language="pt",
        )

        full_text = ""

        for segment in segments:
            full_text += segment.text + " "

        transcription = full_text.strip()

        logger.info(f"Transcription: {transcription}")

        return transcription
