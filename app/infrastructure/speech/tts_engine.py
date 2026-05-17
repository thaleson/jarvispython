import pyttsx3

from app.core.logger import logger


class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()

        self.engine.setProperty(
            "rate",
            180,
        )

        self.engine.setProperty(
            "volume",
            1.0,
        )

    def speak(
        self,
        text: str,
    ) -> None:

        logger.info(f"Jarvis speaking: {text}")

        self.engine.say(text)

        self.engine.runAndWait()
