from abc import ABC, abstractmethod
from Entity.entity import Entity

class Skill(ABC):
    def __init__(self, name: str):
        self._name = name

    def set_name(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name