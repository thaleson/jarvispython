from faster_whisper import WhisperModel

from app.core.config import settings
from app.core.logger import logger


class AudioTranscriber:
    _model = None

    def __init__(self):
        if AudioTranscriber._model is None:
            logger.info("Loading Whisper model...")

            AudioTranscriber._model = WhisperModel(
                settings.WHISPER_MODEL,
                device=settings.WHISPER_DEVICE,
                compute_type=settings.WHISPER_COMPUTE_TYPE,
            )

        self.model = AudioTranscriber._model

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
