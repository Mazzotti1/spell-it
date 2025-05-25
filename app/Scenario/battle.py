import pygame
from Scenario.scenario import Scenario
from Utils.button import Button

class Battle(Scenario):
    def __init__(self, manager, biome, enemy):
        super().__init__()
        self.manager = manager
        self.enemy = enemy
        self.enable_ground = False
        self.enable_solids = False
        self.enable_background = True
        self.enable_ui = False
        self.enable_enemies = True

        self.font = pygame.font.SysFont(None, 64)

        self.load_background(biome)

        self.buttons = [
            self.create_button("Encerrar", "red", (900, 410), (130, 50), manager.end_battle),
        ]

    def draw_ui(self, screen):
        for btn in self.buttons:
            btn.draw(screen)
    
    def create_button(self, text, color, position, size, on_click, text_color="white"):
        return Button(
            color=color,
            position=position,
            size=size,
            text=text,
            on_click=on_click,
            text_color=text_color
        )
    
    def handle_buttons_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw_scene(self, screen):
        super().draw_scene(screen)
        self.enemy.update_animation(self.manager.dt)
        self.enemy.draw(screen)

