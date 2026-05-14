from pathlib import Path

import sounddevice as sd
from scipy.io.wavfile import write

from app.core.logger import logger


class MicrophoneRecorder:
    SAMPLE_RATE = 16000

    @classmethod
    def record(
        cls,
        duration: int = 5,
        output_path: str = "temp_audio/input.wav",
    ) -> str:
        Path("temp_audio").mkdir(
            exist_ok=True,
        )

        logger.info(f"Recording audio for {duration} seconds...")

        audio = sd.rec(
            int(duration * cls.SAMPLE_RATE),
            samplerate=cls.SAMPLE_RATE,
            channels=1,
            dtype="int16",
        )

        sd.wait()

        write(
            output_path,
            cls.SAMPLE_RATE,
            audio,
        )

        logger.info(f"Audio saved at: {output_path}")

        return output_path
