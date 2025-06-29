import pygame
import random
import string
import time
from Utils.utils import Utils

class RandomWord:
    def __init__(self, screen_size, text=None, x=None, y=None, lifetime=5, style=None):
        self.text = text if text else self.generate_random_word()
        self.x = x if x is not None else random.randint(0, screen_size[0] - 100)
        self.y = y if y is not None else random.randint(0, screen_size[1] - 50)
        self.creation_time = time.time()
        self.lifetime = lifetime

        self.style = style if style is not None else random.choice([0, 1, 2])

        display_info = pygame.display.Info()
        real_width = display_info.current_w
        real_height = display_info.current_h

        self.scale_x = real_width / 1920
        self.scale_y = real_height / 1080

        if self.style == 0:
            self.color = (255, 255, 255)
            self.font = Utils.scaled_font(
                path=None,
                base_size=40,
                scale_y=self.scale_y
            )
            self.use_outline = True
            self.use_shadow = True
        elif self.style == 1: 
            self.color = (200, 200, 200)
            self.font = Utils.scaled_font(
                path=None,
                base_size=32,
                scale_y=self.scale_y
            )
            self.use_outline = True
            self.use_shadow = False
        elif self.style == 'PUNIR':
            self.color = (255, 0, 0)
            self.font = Utils.scaled_font(
                path=None,
                base_size=48,
                scale_y=self.scale_y
            )
            self.use_outline = True
            self.use_shadow = True
        else:  
            self.color = (180, 180, 180)
            self.font = Utils.scaled_font(
                path=None,
                base_size=24,
                scale_y=self.scale_y
            )
            self.use_outline = False
            self.use_shadow = False

    def generate_random_word(self, length=5):
        return ''.join(random.choices(string.ascii_uppercase, k=length))

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(topleft=(self.x, self.y))

        if self.use_shadow:
            shadow = pygame.Surface((text_rect.width + 10, text_rect.height + 4))
            shadow.set_alpha(120)
            shadow.fill((0, 0, 0))
            screen.blit(shadow, (self.x - 5, self.y - 2))

        if self.use_outline:
            border_color = (0, 0, 0)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        border = self.font.render(self.text, True, border_color)
                        screen.blit(border, (self.x + dx, self.y + dy))

        screen.blit(text_surface, (self.x, self.y))

    def is_expired(self):
        return time.time() - self.creation_time > self.lifetime
