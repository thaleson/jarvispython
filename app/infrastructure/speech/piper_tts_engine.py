import os
import subprocess
from pathlib import Path
from uuid import uuid4

from app.core.logger import logger


class PiperTTSEngine:
    PIPER_BINARY = "/home/thaleson/piper/piper/piper"

    PIPER_MODEL = "/home/thaleson/piper/piper/" "pt_BR-faber-medium.onnx"

    OUTPUT_DIR = "temp_audio"

    def speak(
        self,
        text: str,
    ) -> None:
        output_dir = Path(
            self.OUTPUT_DIR,
        )

        output_dir.mkdir(
            exist_ok=True,
        )

        raw_output_path = str(output_dir / f"jarvis_raw_{uuid4()}.wav")

        final_output_path = str(output_dir / f"jarvis_response_{uuid4()}.wav")

        logger.info(
            "Piper speaking: %s",
            text,
        )

        subprocess.run(
            [
                self.PIPER_BINARY,
                "--model",
                self.PIPER_MODEL,
                "--output_file",
                raw_output_path,
                "--length_scale",
                "1.08",
                "--noise_scale",
                "0.45",
                "--noise_w",
                "0.65",
            ],
            input=text,
            text=True,
            check=True,
        )

        ffmpeg_filter = (
            "asetrate=22050*0.86,"
            "aresample=22050,"
            "atempo=1.04,"
            "aecho=0.82:0.88:55:0.10,"
            "equalizer=f=90:t=q:w=1:g=5,"
            "equalizer=f=180:t=q:w=1:g=3,"
            "equalizer=f=3200:t=q:w=1:g=-2,"
            "acompressor="
            "threshold=-18dB:ratio=3,"
            "volume=1.4"
        )

        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    raw_output_path,
                    "-af",
                    ffmpeg_filter,
                    final_output_path,
                ],
                check=True,
            )

            subprocess.run(
                [
                    "ffplay",
                    "-nodisp",
                    "-autoexit",
                    "-loglevel",
                    "quiet",
                    final_output_path,
                ],
                check=True,
            )
        finally:
            for file_path in [
                raw_output_path,
                final_output_path,
            ]:
                if os.path.exists(file_path):
                    os.remove(file_path)
