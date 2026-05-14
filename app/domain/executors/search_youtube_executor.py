from app.domain.executors.base_executor import BaseExecutor
from app.infrastructure.automation.youtube_controller import YoutubeController


class SearchYoutubeExecutor(BaseExecutor):
    def can_execute(
        self,
        command: dict,
    ) -> bool:
        return True

    def execute(
        self,
        command: dict,
    ) -> dict:
        query = command.get("query")

        if not query:
            parameters = command.get(
                "parameters",
                {},
            )

            query = parameters.get(
                "query",
                "",
            )

        if not query:
            return {
                "success": False,
                "action": "search_youtube",
                "message": "Não encontrei o termo para pesquisar no YouTube.",
            }

        YoutubeController.search_and_play(query)

        return {
            "success": True,
            "action": "search_youtube",
            "message": (f"Tocando '{query}' " "no YouTube."),
        }
