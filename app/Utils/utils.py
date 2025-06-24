import pygame
import textwrap
import unicodedata
import re
class Utils:
    def __init__(self):
        pass

    @staticmethod
    def round_image(surface, radius):
        size = surface.get_size()

        rounded_surface = pygame.Surface(size, pygame.SRCALPHA)

        rect = pygame.Rect(0, 0, *size)
        shape_surf = pygame.Surface(size, pygame.SRCALPHA)

        pygame.draw.rect(shape_surf, (255, 255, 255, 255), rect, border_radius=radius)

        rounded_surface.blit(surface, (0, 0))
        rounded_surface.blit(shape_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        return rounded_surface

    @staticmethod
    def render_multiline_text(text, font, color, width = 20):
        wrapped_lines = []
        for paragraph in text.split('\n'):
            wrapped = textwrap.wrap(paragraph, width)
            wrapped_lines.extend(wrapped)
        return [font.render(line, True, color) for line in wrapped_lines]
    
    def normalize_skill_name(name):
        name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
        name = re.sub(r'\s+', '_', name.lower())
        return name