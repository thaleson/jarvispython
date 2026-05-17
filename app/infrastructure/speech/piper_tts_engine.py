import subprocess
from pathlib import Path
from uuid import uuid4

from app.core.logger import logger


class PiperTTSEngine:
    PIPER_BINARY = "/home/thaleson/piper/piper/piper"
    PIPER_MODEL = "/home/thaleson/piper/piper/pt_BR-faber-medium.onnx"
    OUTPUT_DIR = "temp_audio"

    def speak(
        self,
        text: str,
    ) -> None:
        Path(self.OUTPUT_DIR).mkdir(
            exist_ok=True,
        )

        output_path = f"{self.OUTPUT_DIR}/" f"jarvis_response_{uuid4()}.wav"

        logger.info(f"Piper speaking: {text}")

        subprocess.run(
            [
                self.PIPER_BINARY,
                "--model",
                self.PIPER_MODEL,
                "--output_file",
                output_path,
            ],
            input=text,
            text=True,
            check=True,
        )

        subprocess.run(
            [
                "ffplay",
                "-nodisp",
                "-autoexit",
                output_path,
            ],
            check=True,
        )
