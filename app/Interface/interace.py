import pygame
from Factory.playerFactory import PlayerFactory

class Interface:
    def __init__(self, player):
        self.player = player
        self.player = PlayerFactory.create_player(0, 0, player.attributes)
        self.health_image = pygame.image.load("../assets/player/estatico/front.png").convert_alpha()
        self.health_image = pygame.transform.scale(self.health_image, (32, 32))

    def draw_health_bar(self, screen):

        health_quantity = self.player.get_health()
        icon_size = 32
        spacing = 2
        total_width = health_quantity * (icon_size + spacing) - spacing
        container_padding = 10
        container_height = icon_size + 10 
        container_width = total_width + container_padding * 2

        container_x = 40
        container_y = 40

        container_rect = pygame.Rect(container_x, container_y, container_width, container_height)
        pygame.draw.rect(screen, (212, 213, 214), container_rect, border_radius=5) 
        pygame.draw.rect(screen, (255, 255, 255), container_rect, 2, border_radius=5)

        font = pygame.font.SysFont(None, 24)
        text_surface = font.render("Vidas", True, (255, 255, 255))
        text_x = 40
        text_y = container_y - 20
        screen.blit(text_surface, (text_x, text_y))

        for i in range(health_quantity):
            x = container_x + container_padding + i * (icon_size + spacing)
            y = container_y + 5
            screen.blit(self.health_image, (x, y))
        