import json
from collections.abc import Generator

import requests

from app.core.logger import logger


class OllamaClient:
    BASE_URL = "http://localhost:11434"
    MODEL = "llama3.2:1b"

    @classmethod
    def generate(cls, prompt: str) -> str:
        payload = {
            "model": cls.MODEL,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(
                f"{cls.BASE_URL}/api/generate",
                json=payload,
                timeout=60,
            )
            response.raise_for_status()

            data = response.json()
            return data.get("response", "").strip()

        except requests.RequestException as error:
            logger.error(f"Ollama request failed: {error}")
            return "Erro ao consultar IA local."

    @classmethod
    def generate_stream(
        cls,
        prompt: str,
    ) -> Generator[str]:
        payload = {
            "model": cls.MODEL,
            "prompt": prompt,
            "stream": True,
        }

        try:
            response = requests.post(
                f"{cls.BASE_URL}/api/generate",
                json=payload,
                stream=True,
                timeout=60,
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue

                data = json.loads(line)
                token = data.get("response", "")

                if token:
                    yield token

                if data.get("done", False):
                    break

        except requests.RequestException as error:
            logger.error(f"Ollama stream failed: {error}")
            yield "Erro ao consultar IA local."
