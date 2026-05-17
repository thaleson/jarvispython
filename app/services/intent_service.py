import re

from app.core.logger import logger


class IntentService:
    @staticmethod
    def _clean_query(query: str) -> str:
        cleaned = query.lower()

        remove_terms = [
            "jarvis",
            "javis",
            "javes",
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
            "abrir",
            "abri",
            "abre",
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

        cleaned = re.sub(
            r"\s+",
            " ",
            cleaned,
        )

        return cleaned.strip()

    @staticmethod
    def _detect_time_intent(
        command: str,
    ) -> dict | None:
        normalized_command = command.lower()

        time_terms = [
            "hora",
            "horas",
            "horário",
            "horario",
        ]

        if any(term in normalized_command for term in time_terms):
            return {
                "action": "get_time",
            }

        return None

    @staticmethod
    def _detect_youtube_intent(
        command: str,
    ) -> dict | None:
        normalized_command = command.lower()

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

        if has_play:
            query = IntentService._clean_query(
                command,
            )

            if query:
                return {
                    "action": "search_youtube",
                    "query": query,
                }

        return None

    @staticmethod
    def detect_intent(
        command: str,
    ) -> dict:
        time_intent = IntentService._detect_time_intent(
            command,
        )

        if time_intent:
            logger.info(f"Local intent detected: {time_intent}")

            return time_intent

        youtube_intent = IntentService._detect_youtube_intent(
            command,
        )

        if youtube_intent:
            logger.info(f"Local intent detected: {youtube_intent}")

            return youtube_intent

        conversation_intent = {
            "action": "conversation",
            "query": command,
        }

        logger.info(f"Local intent detected: {conversation_intent}")

        return conversation_intent
