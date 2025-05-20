from abc import ABC, abstractmethod
from Entity.entity import Entity

class Skill(ABC):
    def __init__(self, name: str, description: str, cooldown: float):
        self._name = name
        self._description = description
        self._cooldown = cooldown

    def set_name(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def set_description(self, description: str):
        self._description = description

    def get_description(self) -> str:
        return self._description

    @abstractmethod
    def can_use(self, caster: Entity) -> bool:
        pass

    @abstractmethod
    def activate(self, caster: Entity, target: Entity):
        pass
