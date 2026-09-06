from abc import ABC, abstractmethod

class SkillAgent(ABC):
    name: str

    @abstractmethod
    def run(self, context: dict) -> dict:
        raise NotImplementedError
