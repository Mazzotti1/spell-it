import pygame

class MenuButtonHover:
    def __init__(self, color, position, size, text, on_click=None,
                 text_color="black", text_size=36, font=None, radius=15, hover_color=None):
        self.color = color
        self.base_color = color
        if isinstance(color, tuple) and len(color) == 3:
            self.hover_color = tuple(min(c + 40, 255) for c in color)
        else:
            self.hover_color = hover_color
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.text = text
        self.text_color = text_color
        self.font = font
        self.radius = radius
        self.on_click = on_click
        self.position = position
        self.size = size
        self.is_hovered = False

    def draw(self, screen):
        current_color = self.hover_color if self.is_hovered and self.hover_color else self.base_color
        if current_color is not None:
            pygame.draw.rect(screen, current_color, self.rect, border_radius=self.radius)

        surface_text = self.font.render(self.text, True, self.text_color)
        rect_text = surface_text.get_rect(center=(self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] // 2))
        screen.blit(surface_text, rect_text)


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    return self.on_click()
