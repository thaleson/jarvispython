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

        detected_intent = IntentService.detect_intent(command)

        action = detected_intent.get(
            "action",
            "unknown_command",
        )

        executor = self.executors.get(action)

        if executor:
            return executor.execute(detected_intent)

        return {
            "success": False,
            "action": ("unknown_command"),
            "message": ("Não entendi o comando."),
        }
