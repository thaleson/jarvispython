from app.domain.executors.base_executor import BaseExecutor
from app.infrastructure.automation.browser_controller import BrowserController


class OpenYoutubeExecutor(BaseExecutor):
    def can_execute(self, command: str) -> bool:
        return "youtube" in command.lower()

    def execute(self) -> str:
        BrowserController.open_youtube()
        return "open_youtube"
