BLOCKED_TERMS = [
    "rm -rf",
    "shutdown",
    "reboot",
    "format",
    "mkfs",
    "passwd",
    "sudo",
]


class SecurityValidator:

    @staticmethod
    def is_safe(command: str) -> bool:

        normalized_command = command.lower()

        for term in BLOCKED_TERMS:

            if term in normalized_command:
                return False

        return True
