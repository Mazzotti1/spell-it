import pygame

class Scenario:
    def __init__(self):
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

    def update(self):
        pass

    def draw_scene(self, screen):
        if self.enable_background:
            self.draw_background(screen)

        if self.enable_ground:
            self.draw_ground(screen)

        if self.enable_solids:
            self.draw_solids(screen)

        if self.enable_ui:
            self.draw_ui(screen)

    def draw_background(self, screen):
        screen.fill((0,0,0)) 

        if self.background_image:
            screen_width, screen_height = screen.get_size()
            bg_width, bg_height = self.background_image.get_size()

            x = (screen_width - bg_width) // 2
            y = (screen_height - bg_height) // 2

            screen.blit(self.background_image, (x, y))



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