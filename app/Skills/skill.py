from abc import ABC, abstractmethod
import pygame
from Entity.entity import Entity

class Skill(ABC):
    def __init__(self, name: str, image: pygame.Surface = None):
        self._name = name
        self.image = image

    def set_name(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def get_image(self):
        return self.image

    def create_skill(name: str, front_images_dict):
        image = front_images_dict.get(name)
        return Skill(name, image)
