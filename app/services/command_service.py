from app.infrastructure.automation.browser_controller import BrowserController


class CommandService:

    @staticmethod
    def process_command(command: str) -> str:

        normalized_command = command.lower()

        if "youtube" in normalized_command:

            BrowserController.open_youtube()

            return "open_youtube"

        if "hora" in normalized_command:
            return "get_time"

        return "unknown_command"
