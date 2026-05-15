from pathlib import Path

import sounddevice as sd
from scipy.io.wavfile import write

from app.core.config import settings
from app.core.logger import logger


class MicrophoneRecorder:
    SAMPLE_RATE = 16000

    @classmethod
    def record(
        cls,
        duration=None,
        output_path=None,
    ) -> str:

        duration = duration or settings.VOICE_RECORD_DURATION

        output_path = output_path or "temp_audio/input.wav"

        Path(settings.TEMP_AUDIO_DIR).mkdir(
            exist_ok=True,
        )

        logger.info(f"Recording audio for " f"{duration} seconds...")

        audio = sd.rec(
            int(duration * cls.SAMPLE_RATE),
            samplerate=16000,
            channels=1,
            dtype="int16",
        )

        sd.wait()

        write(
            output_path,
            cls.SAMPLE_RATE,
            audio,
        )

        logger.info(f"Audio saved at: " f"{output_path}")

        return output_path
