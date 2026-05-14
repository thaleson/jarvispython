from app.domain.executors.get_time_executor import GetTimeExecutor
from app.domain.executors.open_youtube_executor import OpenYoutubeExecutor
from app.domain.executors.search_youtube_executor import SearchYoutubeExecutor
from app.services.intent_service import IntentService


class CommandRegistry:

    def __init__(self):

        self.executors = {
            "search_youtube": (SearchYoutubeExecutor()),
            "open_youtube": (OpenYoutubeExecutor()),
            "get_time": (GetTimeExecutor()),
        }

    def execute(
        self,
        command: str,
    ) -> dict:

        normalized_command = command.lower()

        youtube_search_terms = [
            "musica",
            "música",
            "bota",
            "toque",
            "coloque",
            "pesquise",
        ]

        if "youtube" in normalized_command and any(
            term in normalized_command for term in youtube_search_terms
        ):

            return self.executors["search_youtube"].execute(command)

        detected_intent = IntentService.detect_intent(command)

        action = detected_intent.get(
            "action",
            "unknown_command",
        )

        executor = self.executors.get(action)

        if executor:
            return executor.execute(command)

        return {
            "success": False,
            "action": ("unknown_command"),
            "message": ("Não entendi o comando."),
        }
