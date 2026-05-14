import json

from app.core.logger import logger
from app.infrastructure.llm.ollama_client import OllamaClient


class IntentService:

    @staticmethod
    def detect_intent(
        command: str,
    ) -> dict:

        prompt = f"""
Você é um sistema de detecção de intenção.

Sua função é responder SOMENTE JSON.

NUNCA explique nada.
NUNCA escreva texto fora do JSON.

Ações disponíveis:
- search_youtube
- open_youtube
- get_time
- unknown_command

Exemplos:

Comando:
"abra youtube"

Resposta:
{{"action":"open_youtube"}}

Comando:
"bota musica lofi no youtube"

Resposta:
{{"action":"search_youtube"}}

Comando:
"que horas sao"

Resposta:
{{"action":"get_time"}}

Agora responda.

Comando:
"{command}"
"""

        response = OllamaClient.generate(prompt)

        logger.info(f"LLM response: {response}")

        try:
            return json.loads(response)

        except Exception:

            logger.error("Invalid JSON returned by LLM")

            return {"action": "unknown_command"}
