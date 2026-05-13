from app.core.logger import logger
from app.services.command_registry import CommandRegistry


class CommandService:
    @staticmethod
    def process_command(command: str) -> dict:

        logger.info(f"Command received: {command}")

        registry = CommandRegistry()

        result = registry.execute(command)

        logger.info(f"Action executed: {result['action']}")

        return result
