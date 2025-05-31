import pygame

class MenuButton:
    def __init__(self, icon, position, size, on_click=None):
        self.icon = pygame.image.load(icon).convert_alpha()
        self.icon = pygame.transform.scale(self.icon, size)

        self.position = position
        self.size = size
        self.on_click = on_click
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])

        self.color = (50, 50, 50)
        self.radius = 10  

    def draw(self, screen):
        border_color = (192, 192, 192)
        border_thickness = 3

        is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())

        if is_hovered:
            draw_rect = self.rect.inflate(15, 15) 
            border_color = (255, 215, 0) 
        else:
            draw_rect = self.rect

        pygame.draw.rect(screen, border_color, draw_rect, border_radius=self.radius)

        inner_rect = draw_rect.inflate(-2 * border_thickness, -2 * border_thickness)
        pygame.draw.rect(screen, self.color, inner_rect, border_radius=self.radius - 2)

        icon_rect = self.icon.get_rect(center=inner_rect.center)
        screen.blit(self.icon, icon_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    return self.on_click()