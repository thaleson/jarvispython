from app.services.command_registry import CommandRegistry


class CommandService:
    @staticmethod
    def process_command(command: str) -> dict:
        registry = CommandRegistry()
        return registry.execute(command)
