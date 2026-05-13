from abc import ABC, abstractmethod


class BaseExecutor(ABC):
    @abstractmethod
    def can_execute(self, command: str) -> bool:
        pass

    @abstractmethod
    def execute(self) -> str:
        pass
