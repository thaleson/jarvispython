import json
import re

from app.core.logger import logger
from app.infrastructure.llm.ollama_client import OllamaClient


class IntentService:
    @staticmethod
    def _clean_query(query: str) -> str:
        cleaned = query.lower()

        remove_terms = [
            "jarvis",
            "javis",
            "jávis",
            "jáaves",
            "já vejo",
            "tocar",
            "toque",
            "bota",
            "coloque",
            "coloca",
            "pesquise",
            "pesquisa",
            "para mim",
            "pra mim",
            "por favor",
            "no youtube",
            "youtube",
        ]

        for term in remove_terms:
            cleaned = cleaned.replace(term, "")

        cleaned = cleaned.replace(",", " ")
        cleaned = cleaned.replace(".", " ")
        cleaned = re.sub(r"\s+", " ", cleaned)

        return cleaned.strip()

    @staticmethod
    def _detect_youtube_intent(command: str) -> dict | None:
        normalized_command = command.lower()

        has_youtube = (
            "youtube" in normalized_command or "you tube" in normalized_command
        )

        play_terms = [
            "tocar",
            "toque",
            "bota",
            "coloque",
            "coloca",
            "pesquise",
            "pesquisa",
        ]

        has_play = any(term in normalized_command for term in play_terms)

        if has_youtube and has_play:
            query = IntentService._clean_query(command)

            return {
                "action": "search_youtube",
                "query": query,
            }

        return None

    @staticmethod
    def detect_intent(command: str) -> dict:
        local_intent = IntentService._detect_youtube_intent(command)

        if local_intent:
            logger.info(f"Local intent detected: {local_intent}")
            return local_intent

        prompt = f"""
Você é um classificador de intenção para um assistente local.

Responda SOMENTE JSON válido.

Ações disponíveis:
- search_youtube
- open_youtube
- get_time
- unknown_command

Regras:
- Se pedir para tocar, colocar, pesquisar ou buscar algo no YouTube:
  {{"action":"search_youtube","query":"termo principal"}}
- Se pedir apenas abrir YouTube:
  {{"action":"open_youtube"}}
- Se perguntar horário:
  {{"action":"get_time"}}

Comando:
"{command}"

JSON:
"""

        response = OllamaClient.generate(prompt)

        logger.info(f"LLM response: {response}")

        json_match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL,
        )

        if not json_match:
            logger.error("No JSON found in LLM response")
            return {"action": "unknown_command"}

        try:
            data = json.loads(json_match.group())

            if "result" in data and isinstance(data["result"], dict):
                data = data["result"]

            if "parameters" in data and isinstance(data["parameters"], dict):
                data["query"] = data["parameters"].get("query", "")

            if data.get("action") == "search_youtube":

                query_value = data.get(
                    "query",
                    command,
                )

            data["query"] = IntentService._clean_query(query_value)

            return data

        except Exception:
            logger.error("Invalid JSON returned by LLM")
            return {"action": "unknown_command"}
