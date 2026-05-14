from app.domain.executors.base_executor import BaseExecutor
from app.infrastructure.automation.youtube_controller import YoutubeController


class SearchYoutubeExecutor(BaseExecutor):
    def can_execute(
        self,
        command: str,
    ) -> bool:
        normalized_command = command.lower()

        return "youtube" in normalized_command

    def execute(
        self,
        command: str,
    ) -> dict:
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

        YoutubeController.search_and_play(search_query)

        return {
            "success": True,
            "action": "search_youtube",
            "message": (f"Tocando '{search_query}' " "no YouTube."),
        }
