from datetime import datetime

from app.domain.executors.base_executor import BaseExecutor


class GetTimeExecutor(BaseExecutor):
    def can_execute(self, command: str) -> bool:
        return "hora" in command.lower()

    def execute(self) -> dict:
        current_time = datetime.now().strftime("%H:%M")

        return {
            "success": True,
            "action": "get_time",
            "message": f"Agora são {current_time}.",
        }
