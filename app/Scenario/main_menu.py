import pygame
from Scenario.scenario import Scenario
from Scenario.battle import Battle
from Utils.button import Button
from Scenario.map import Map

class MainMenu(Scenario):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.enable_ground = False
        self.enable_solids = False
        self.font = pygame.font.SysFont(None, 64)

        self.menu_buttons = [
            self.create_button("Iniciar", "green", (900, 410), (130, 50), self.start_game),
            self.create_button("Opções", "orange", (900, 510), (130, 50), self.start_game),
            self.create_button("Sair", "red", (900, 610), (130, 50), self.exit_game, text_color="white"),
        ]

    def create_button(self, text, color, position, size, on_click, text_color="black"):
        return Button(
            color=color,
            position=position,
            size=size,
            text=text,
            on_click=on_click,
            text_color=text_color
        )

    def draw_background(self, screen):
        screen.fill((0, 0, 0))

    def draw_ui(self, screen):
        for btn in self.menu_buttons:
            btn.draw(screen)

    def handle_buttons_event(self, event):
        for btn in self.menu_buttons:
            btn.handle_event(event)

    def exit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def start_game(self):
        self.manager.change_scenario(Map(self.manager, "../assets/scene/map/map_1.png"))
         