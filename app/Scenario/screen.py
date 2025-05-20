import pygame
from Scenario.scenario import Scenario

class Screen(Scenario):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.enable_ground = True
        self.enable_solids = True
        self.enable_background = True
        self.enable_ui = False
        self.font = pygame.font.SysFont(None, 64)
