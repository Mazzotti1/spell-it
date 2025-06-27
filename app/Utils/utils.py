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

    @staticmethod
    def normalize_skill_name(name):
        name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
        name = name.lower()

        words = re.split(r'\s+', name.strip())
        stopwords = {"de", "do", "da", "dos", "das", "e"}
        filtered_words = [w for w in words if w not in stopwords]
        normalized = "_".join(filtered_words)
        return normalized
    
    @staticmethod
    def scaled_font(path: str, base_size: int, scale_y: float = 0, min_size: int = 16, bold: bool = False) -> pygame.font.Font:
        display_info = pygame.display.Info()
        real_height = display_info.current_h
        scale_y = real_height / 1080

        final_size = int(max(min_size, base_size * scale_y))
        return pygame.font.Font(path, final_size)

    @staticmethod
    def scaled_image(image: pygame.Surface, scale_x: float, scale_y: float) -> pygame.Surface:

        width = int(image.get_width() * scale_x)
        height = int(image.get_height() * scale_y)
        return pygame.transform.scale(image, (width, height))
