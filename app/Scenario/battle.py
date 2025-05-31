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
        self.enable_ui = True
        self.enable_enemies = True

        self.font = pygame.font.SysFont(None, 64)

        self.load_background(biome)

        self.buttons = [
            self.create_button("Encerrar", "red", (0, 0), (130, 50), manager.end_battle),
        ]

    def draw_ui(self, screen):
        for btn in self.buttons:
            btn.draw(screen)
        self.draw_menu(screen)

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


    def draw_background(self, screen):
        screen.fill((0, 0, 0))

        if self.background_image and not self.is_start_map_animating:
            screen_width, screen_height = screen.get_size()
            bg_width, bg_height = self.background_image.get_size()

            x = (screen_width - bg_width) // 2
            y = (screen_height - bg_height) // 2

            rounded_bg = self.utils.round_image(surface=self.background_image, radius=0)

            screen.blit(rounded_bg, (x, y))