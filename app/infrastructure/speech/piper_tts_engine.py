import os
import subprocess
from pathlib import Path
from uuid import uuid4

from app.core.logger import logger


class PiperTTSEngine:
    PIPER_BINARY = "/home/thaleson/piper/piper/piper"

    PIPER_MODEL = "/home/thaleson/piper/piper/" "pt_BR-faber-medium.onnx"

    OUTPUT_DIR = "temp_audio"

    def synthesize_to_file(
        self,
        text: str,
    ) -> str:
        output_dir = Path(
            self.OUTPUT_DIR,
        )

        output_dir.mkdir(
            exist_ok=True,
        )

        raw_output_path = str(
            output_dir / f"jarvis_raw_{uuid4()}.wav",
        )

        final_output_path = str(
            output_dir / f"jarvis_response_{uuid4()}.wav",
        )

        logger.info(
            "Piper synthesizing: %s",
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
        finally:
            if os.path.exists(raw_output_path):
                os.remove(raw_output_path)

        return final_output_path

    def play_file(
        self,
        audio_path: str,
    ) -> None:
        subprocess.run(
            [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet",
                audio_path,
            ],
            check=True,
        )

    def speak(
        self,
        text: str,
    ) -> None:
        audio_path = self.synthesize_to_file(text)

        try:
            self.play_file(audio_path)
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)
