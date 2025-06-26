import pygame
from Utils.utils import Utils
class Button:
    def __init__(self, color, position, size, text, on_click=None,
                 text_color="black", text_size=36, font=None, radius=15):
        self.color = color
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.text = text
        self.text_color = text_color

        display_info = pygame.display.Info()
        real_width = display_info.current_w
        real_height = display_info.current_h

        self.scale_x = real_width / 1920
        self.scale_y = real_height / 1080

        if font is None:
            self.font = Utils.scaled_font(
                path=None,
                base_size=text_size,
                scale_y=self.scale_y
            )
        else:
            self.font = font
        self.radius = radius
        self.on_click = on_click
        self.position = position
        self.size = size

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.radius)
        surface_text = self.font.render(self.text, True, self.text_color)
        rect_text = surface_text.get_rect(center=(self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] // 2))
        screen.blit(surface_text, rect_text)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    return self.on_click()