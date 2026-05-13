from app.domain.executors.get_time_executor import GetTimeExecutor
from app.domain.executors.open_youtube_executor import OpenYoutubeExecutor


class CommandRegistry:
    def __init__(self):
        self.executors = [
            OpenYoutubeExecutor(),
            GetTimeExecutor(),
        ]

    def execute(self, command: str) -> dict:
        for executor in self.executors:
            if executor.can_execute(command):
                return executor.execute()

        return {
            "success": False,
            "action": "unknown_command",
            "message": "Ainda não sei executar esse comando.",
        }
