from datetime import datetime

from app.domain.executors.base_executor import BaseExecutor


class GetTimeExecutor(BaseExecutor):
    def can_execute(self, command: str) -> bool:
        return "hora" in command.lower()

    def execute(self) -> str:
        return datetime.now().strftime("%H:%M")
