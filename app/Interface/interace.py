import pygame
from Factory.playerFactory import PlayerFactory
from Utils.time_bar import TimerBar
import math

class Interface:
    def __init__(self, player, pre_combat_time = 30, turn_time=15, punishment_time=10):
        self.player = player
        self.player = PlayerFactory.create_player(0, 0, player.attributes)
        self.health_image = pygame.image.load("../assets/player/estatico/front.png").convert_alpha()
        self.health_image = pygame.transform.scale(self.health_image, (32, 32))

        self.pre_combat_timer = TimerBar(pre_combat_time, title="Pré-combate")
        self.punishment_timer = TimerBar(punishment_time, title="Punição")
        self.turn_timer = TimerBar(turn_time, title="Turno")

        self.input_active = True
        self.input_text = ""
        self.input_font = pygame.font.SysFont(None, 48)

        self.popup_error_message = None
        self.popup_time_remaining = 0
        self.popup_font = pygame.font.SysFont(None, 36)

    def draw_health_bar(self, screen):
        health_quantity = self.player.get_health() // 10

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


    def draw_battle_timers(self, screen, type, playerIsMoving=True):
        if type == "pre_combat":
            self.pre_combat_timer.draw(screen, x=850, y=100, width=200, height=20, playerIsMoving=playerIsMoving)
        elif type == "turn":
            self.turn_timer.draw(screen, x=850, y=100, width=200, height=20, playerIsMoving=playerIsMoving)
        elif type == "punishment":
            self.punishment_timer.draw(screen, x=850, y=100, width=200, height=20, playerIsMoving=playerIsMoving)
        elif type == "enemy_turn":
            self.punishment_timer.is_visible = False
        else:
            self.pre_combat_timer.draw(screen, x=850, y=100, width=200, height=20, playerIsMoving=playerIsMoving)

    def reset_timers(self):
        self.pre_combat_timer.reset()
        self.punishment_timer.reset()
        self.turn_timer.reset()

    def draw_input_box(self, screen):
        box_width, box_height = 400, 60
        x, y = (screen.get_width() - box_width) // 2, screen.get_height() - 133

        input_rect = pygame.Rect(x, y, box_width, box_height)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), input_rect, 3, border_radius=10)

        if self.input_text:
            if not self.input_active:
                self.input_text = ""
            text_surface = self.input_font.render(self.input_text, True, (0, 0, 0))
        else:
            placeholder = "Bloqueado" if not self.input_active else "Apenas digite..."
            text_surface = self.input_font.render(placeholder, True, (150, 150, 150))

        screen.blit(text_surface, (x + 10, y + (box_height - text_surface.get_height()) // 2))

    def handle_input_event(self, event):
        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                return self.input_text.strip()
            else:
                self.input_text += event.unicode

    def is_pre_combat_over(self):
        return self.pre_combat_timer.is_time_up()

    def is_punishment_over(self):
        return self.punishment_timer.is_time_up()

    def show_popup(self, message, duration=1.5):
        self.popup_error_message = message
        self.popup_time_remaining = duration

    def draw_popup(self, screen):
        if self.popup_error_message:
            text_surface = self.popup_font.render(self.popup_error_message, True, (255, 0, 0))
            padding = 20
            bg_width = text_surface.get_width() + padding * 2
            bg_height = text_surface.get_height() + padding * 2

            screen_width = screen.get_width()
            screen_height = screen.get_height()

            x = ((screen_width - 800) - bg_width) // 2
            y = 50

            bg_rect = pygame.Rect(x, y, bg_width, bg_height)
            pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=15)
            pygame.draw.rect(screen, (255, 0, 0), bg_rect, width=3, border_radius=15)

            text_x = x + (bg_width - text_surface.get_width()) // 2
            text_y = y + (bg_height - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))
