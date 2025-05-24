import pygame
from Scenario.scenario import Scenario

class Map(Scenario):
    def __init__(self, manager, background):
        super().__init__()
        self.manager = manager
        self.enable_ground = False
        self.enable_solids = False
        self.enable_background = True
        self.enable_ui = False
        self.font = pygame.font.SysFont(None, 64)

        self.load_background(background)
