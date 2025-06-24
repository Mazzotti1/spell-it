import pygame
from Factory.playerFactory import PlayerFactory
from Utils.time_bar import TimerBar
import math
from Utils.hit_bar import HitBar
import time

class Interface:
    def __init__(self, player, pre_combat_time = 30, turn_time=15, punishment_time=5):
        self.player = player
        self.player = PlayerFactory.create_player(0, 0, player.attributes)
        self.health_image = pygame.image.load("../assets/player/estatico/front.png").convert_alpha()
        self.health_image = pygame.transform.scale(self.health_image, (32, 32))

        self.pre_combat_timer = TimerBar(pre_combat_time, title="Pré-combate")
        self.punishment_timer = TimerBar(punishment_time, title="Punição")
        self.turn_timer = TimerBar(turn_time, title="Turno")
        self.player_turn_timer = TimerBar(turn_time, title="Turno do jogador")

        self.hit_bar = HitBar(total_hits=15, title="Acertos")


        self.input_active = True
        self.input_text = ""
        self.input_font = pygame.font.SysFont(None, 48)

        self.popup_error_message = None
        self.popup_time_remaining = 0
        self.popup_font = pygame.font.SysFont(None, 36)
        self.popup_priority = 0

        self.skill_rects = []

        self.boss_bar_animation_time = 0.5 
        self.boss_bar_start_time = None
        self.boss_bar_height = 30
        self.boss_bar_y_target = 90 
        self.boss_bar_y_start = 170
        self.boss_bar_current_width = 0
        self.boss_bar_full_width = 600
        self.boss_bar_font = pygame.font.SysFont("arial", 26, bold=True)
        self.boss_displayed_health = None

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

    def draw_player_skills(self, screen, player):
        skills = player.skills

        if not skills:
            return

        base_icon_size = 64
        hover_icon_width = 320
        hover_icon_height = 485
        spacing = 10
        container_padding = 10

        total_width = len(skills) * (base_icon_size + spacing) - spacing
        container_height = base_icon_size + 10
        container_width = total_width + container_padding * 2

        health_container_x = 40
        health_total_width = (self.player.get_health() // 10) * (32 + 2) - 2
        health_container_width = health_total_width + container_padding * 2

        container_x = health_container_x + health_container_width + 20
        container_y = 40

        container_rect = pygame.Rect(container_x, container_y, container_width, container_height)
        pygame.draw.rect(screen, (212, 213, 214), container_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), container_rect, 2, border_radius=5)

        font = pygame.font.SysFont(None, 24)
        text_surface = font.render("Habilidades", True, (255, 255, 255))
        text_x = container_x
        text_y = container_y - 20
        screen.blit(text_surface, (text_x, text_y))

        mouse_pos = pygame.mouse.get_pos()

        self.skill_rects.clear() 
        for i, skill in enumerate(skills):
            x = container_x + container_padding + i * (base_icon_size + spacing)
            y = container_y + 5

            skill_rect = pygame.Rect(x, y, base_icon_size, base_icon_size)
            self.skill_rects.append(skill_rect)

            is_hovered = skill_rect.collidepoint(mouse_pos)

            if is_hovered:
                overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))

                center_x = screen.get_width() // 2 - hover_icon_width // 2
                center_y = screen.get_height() // 2 - hover_icon_height // 2

                skill_img = skill.get_image()
                if skill_img:
                    skill_img_scaled = pygame.transform.scale(skill_img, (hover_icon_width, hover_icon_height))
                    screen.blit(skill_img_scaled, (center_x, center_y))
                else:
                    pygame.draw.rect(screen, (255, 0, 0), (center_x, center_y, hover_icon_width, hover_icon_height))
            else:
                skill_img = skill.get_image()
                if skill_img:
                    skill_img_scaled = pygame.transform.scale(skill_img, (base_icon_size, base_icon_size))
                    screen.blit(skill_img_scaled, (x, y))
                else:
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, base_icon_size, base_icon_size))

    def draw_battle_timers(self, screen, type, playerIsMoving=True):
        if type == "pre_combat":
            self.pre_combat_timer.draw(screen, x=850, y=100, width=200, height=20, playerIsMoving=playerIsMoving)
        elif type == "turn":
            self.turn_timer.draw(screen, x=850, y=100, width=200, height=20, playerIsMoving=playerIsMoving)
        elif type == "punishment":
            self.punishment_timer.draw(screen, x=850, y=100, width=200, height=20, playerIsMoving=playerIsMoving)
        elif type == "enemy_turn":
            self.punishment_timer.is_visible = False
        elif type == "player_turn":
            self.player_turn_timer.draw(screen, x=850, y=100, width=200, height=20, playerIsMoving=playerIsMoving)
        else:
            self.pre_combat_timer.draw(screen, x=850, y=100, width=200, height=20, playerIsMoving=playerIsMoving)

    def draw_hit_bar(self, screen):
        self.hit_bar.draw(screen, x=850, y=40, width=200, height=20)

    def reset_timers(self):
        self.pre_combat_timer.reset()
        self.punishment_timer.reset()
        self.turn_timer.reset()

    def reset_plauer_turn_timer(self):
        self.player_turn_timer.reset()

    def reset_hit_bar(self):
        self.hit_bar.reset()

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
    
    def is_player_turn_over(self):
        return self.player_turn_timer.is_time_up()

    def show_popup(self, message, duration=1.5, x=None, y=None, priority=0):
        if self.popup_error_message is None or priority >= self.popup_priority:
            self.popup_error_message = message
            self.popup_time_remaining = duration
            self.popup_x = x
            self.popup_y = y
            self.popup_position = (x, y)
            self.popup_priority = priority

    def draw_popup(self, screen):
        if self.popup_error_message:
            text_surface = self.popup_font.render(self.popup_error_message, True, (255, 0, 0))
            padding = 20
            bg_width = text_surface.get_width() + padding * 2
            bg_height = text_surface.get_height() + padding * 2

            screen_width = screen.get_width()
            screen_height = screen.get_height()

            x = self.popup_x if self.popup_x is not None else ((screen_width - 800) - bg_width) // 2
            y = self.popup_y if self.popup_y is not None else 50

            bg_rect = pygame.Rect(x, y, bg_width, bg_height)
            pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=15)
            pygame.draw.rect(screen, (255, 0, 0), bg_rect, width=3, border_radius=15)

            text_x = x + (bg_width - text_surface.get_width()) // 2
            text_y = y + (bg_height - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))

    def start_boss_bar_animation(self):
        self.boss_bar_start_time = time.time()

    def draw_boss_health_bar(self, screen, enemy, dt):
        if self.boss_bar_start_time is None:
            self.start_boss_bar_animation()
            self.boss_displayed_health = enemy.get_health()

        elapsed = time.time() - self.boss_bar_start_time
        progress = min(elapsed / self.boss_bar_animation_time, 1)

        current_width = int(self.boss_bar_full_width * progress)
        bar_x = 1250  
        bar_y = self.boss_bar_y_start - int((self.boss_bar_y_start - self.boss_bar_y_target) * progress)

        pygame.draw.rect(screen, (80, 0, 0), (bar_x, bar_y, current_width, self.boss_bar_height), border_radius=10)

        if self.boss_displayed_health is None:
            self.boss_displayed_health = enemy.get_health()

        real_health = enemy.get_health()
        max_health = max(enemy.get_max_health(), 1)

        lerp_speed = 10
        diff = real_health - self.boss_displayed_health
        if abs(diff) > 0.1:
            self.boss_displayed_health += diff * min(lerp_speed * dt, 1)
        else:
            self.boss_displayed_health = real_health

        health_ratio = self.boss_displayed_health / max_health
        current_health_width = int(current_width * health_ratio)

        pygame.draw.rect(screen, (200, 0, 0), (bar_x, bar_y, current_health_width, self.boss_bar_height), border_radius=10)

        name_surf = self.boss_bar_font.render(enemy.getName(), True, (255, 255, 255))
        name_rect = name_surf.get_rect(center=(bar_x + self.boss_bar_full_width // 2, bar_y - 20))
        screen.blit(name_surf, name_rect)