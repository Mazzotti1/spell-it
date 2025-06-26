import pygame
from Utils.utils import Utils
from Utils.menu_dialog import MenuDialog
from Utils.settings_dialog import SettingsDialog

class Scenario:
    def __init__(self, manager=None):
        self.name = None
        self.objects = []
        self.music = None
        self.sound_effects = []

        self.enable_background = True
        self.enable_ground = True
        self.enable_solids = True
        self.enable_ui = True

        self.solids = []
        self.background_image = None
        self.is_start_map_animating = False
        self.utils = Utils()
        self.allow_menu = True
        self.manager = manager
        
        self.is_menu_open = False

        self.font = Utils.scaled_font(
            path="../assets/fonts/VT323-Regular.ttf",
            base_size=30,
        )

        self.settings_dialog = SettingsDialog(
            color='gray',
            position=(650, 120),
            size=(600, 800),
            text="Configurações",
            text_size=36,
            font=self.font,
            radius=10
        )

        self.menu = MenuDialog(
            self.manager,
            color='gray',
            position=(780, 300),
            size=(400, 200),
            text="Opções",
            text_size=36,
            font=self.font,
            radius=10,
            settings_dialog=self.settings_dialog,
        )

    def update(self):
        pass

    def draw_scene(self, screen, player=None):
        if self.enable_background:
            self.draw_background(screen)

        if self.enable_ground:
            self.draw_ground(screen)

        if self.enable_solids:
            self.draw_solids(screen)

        if self.enable_ui:
            self.draw_ui(screen)

    def draw_background(self, screen):
        screen.fill((0, 0, 0))

    def draw_ground(self, screen):
        ground_height = 150
        width, height = screen.get_size()
        ground_rect = pygame.Rect(0, height - ground_height, width, ground_height)
        pygame.draw.rect(screen, (139, 69, 19), ground_rect)

    def draw_solids(self, screen):
        for solid in self.solids:
            pygame.draw.rect(screen, (100, 100, 100), solid)

    def draw_ui(self, screen):
        pass

    def load_background(self, image_path):
        self.background_image = pygame.image.load(image_path).convert_alpha()

    def open_menu(self):
        if self.allow_menu:
            self.is_menu_open = not self.is_menu_open  

    def draw_menu(self, screen):
        if self.is_menu_open:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  
            overlay.fill((38, 35, 35, 225)) 

            screen.blit(overlay, (0, 0))
            self.menu.draw(screen)
        