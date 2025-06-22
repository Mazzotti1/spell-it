from abc import ABC, abstractmethod
import pygame

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

    def activate(self, context): pass

    def on_word_typed(self, context, word: str, correct: bool): pass

    def on_3_words_success(self, context): pass

    def on_word_error(self, context, word: str)-> bool : return False

    def on_repeat_last_word(self, context, word: str): pass

    def on_repeat_enemy_word(self, context, word: str): pass

    def on_enemy_attack(self, context, damage): return damage

    def on_turn_start(self, context): pass

    def on_turn_end(self, context): pass

