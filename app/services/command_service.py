from app.core.logger import logger
from app.core.security import SecurityValidator
from app.services.command_registry import CommandRegistry


class CommandService:
    @staticmethod
    def process_command(command: str) -> dict:
        logger.info(f"Command received: {command}")

        is_safe = SecurityValidator.is_safe(command)

        if not is_safe:
            logger.warning(f"Blocked unsafe command: {command}")

            return {
                "success": False,
                "action": "blocked_command",
                "message": "Comando bloqueado por segurança.",
            }

        registry = CommandRegistry()
        result = registry.execute(command)

        logger.info(f"Action executed: {result['action']}")

        return result
