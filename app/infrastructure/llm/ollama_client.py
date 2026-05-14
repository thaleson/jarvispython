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
