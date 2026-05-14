from urllib.parse import quote_plus

from app.domain.executors.base_executor import BaseExecutor
from app.infrastructure.automation.browser_controller import BrowserController


class SearchYoutubeExecutor(BaseExecutor):
    def can_execute(self, command: str) -> bool:

        normalized_command = command.lower()

        return "youtube" in normalized_command and (
            "musica" in normalized_command
            or "música" in normalized_command
            or "toque" in normalized_command
            or "coloque" in normalized_command
            or "bota" in normalized_command
        )

    def execute(self, command: str) -> dict:

        search_query = (
            command.lower()
            .replace("youtube", "")
            .replace("música", "")
            .replace("musica", "")
            .replace("toque", "")
            .replace("coloque", "")
            .replace("bota", "")
            .strip()
        )

        encoded_query = quote_plus(search_query)

        youtube_url = "https://www.youtube.com/results?"
        f"search_query={encoded_query}"

        BrowserController.open_url(youtube_url)

        return {
            "success": True,
            "action": "search_youtube",
            "message": (f"Pesquisando '{search_query}' " "no YouTube."),
        }
