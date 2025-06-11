import pygame
from Scenario.scenario import Scenario
from Utils.button import Button
from Interface.interace import Interface
from Words.RandomWordManager import RandomWordManager
from Effects.book_animation import BookAnimation
from Effects.puff_animation import PuffAnimation
class Battle(Scenario):
    def __init__(self, manager, biome, enemy, player_final_x, player_final_y):
        super().__init__(manager),
        self.manager = manager
        self.enemy = enemy
        self.enable_ground = False
        self.enable_solids = False
        self.enable_background = True
        self.enable_ui = True
        self.enable_enemies = True
        self.player_final_x = player_final_x
        self.player_final_y = player_final_y

        self.quantity_pre_combat_words = 5

        self.pre_combat_ended = False

        self.font = pygame.font.SysFont(None, 64)

        self.load_background(biome)

        self.buttons = [
            self.create_button("Encerrar", "red", (0, 0), (130, 50), manager.end_battle),
        ]
        self.pre_combat_time = 15

        self.interface = Interface(manager.player, pre_combat_time=self.pre_combat_time)

        screen_size = (1920, 1080)
        self.word_manager = RandomWordManager(screen_size, self.pre_combat_time, biome, player_position=(self.player_final_x, self.player_final_y))

        self.alreadyGeneratedWords = False
        self.turn_started = False
        self.pre_combat_word_count = 0

        self.pre_combat_result = None
        self.result_finalization_animation_progress = 0
        self.result_finalization_animation_active = False
        self.result_finalization_animation_timer = 0

        self.book_animations = []

        self.explosion_animations = []

        self.start_punishin_animation = False

    def draw_ui(self, screen):
        if not self.manager.player.moving:
            for btn in self.buttons:
                btn.draw(screen)
            self.draw_menu(screen)
            self.interface.draw_input_box(screen)
            self.interface.draw_popup(screen)


            if self.result_finalization_animation_active:
                self.draw_result_pre_combat_animation(screen)
            else:
                if not self.pre_combat_ended:
                    self.interface.draw_battle_timers(screen, "pre_combat", self.manager.player.moving)


    def create_button(self, text, color, position, size, on_click, text_color="white"):
        return Button(
            color=color,
            position=position,
            size=size,
            text=text,
            on_click=on_click,
            text_color=text_color
        )

    def handle_buttons_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)
        typed_word = self.interface.handle_input_event(event)
        if typed_word:
            word_obj = self.word_manager.check_word(typed_word)
            self.interface.input_text = ""

            if self.pre_combat_ended:
                self.manager.player.play_skill_animation()
                self.start_punishin_animation = True
                damage, is_critical, enemy_alive = self.manager.player.attack(self.enemy)
                print(f"Dano causado: {damage}")
                if is_critical:
                    print("⚡ Dano crítico!")
                if not enemy_alive:
                    print("☠️ Inimigo derrotado!")
                return

            if word_obj and not self.pre_combat_ended:
                self.pre_combat_word_count += 1

                word_x, word_y = word_obj.x, word_obj.y
                player_x, player_y = self.manager.player.get_position()

                animation = BookAnimation((player_x, player_y), (word_x, word_y))
                self.book_animations.append(animation)

                if self.pre_combat_word_count >= self.quantity_pre_combat_words:
                    self.pre_combat_ended = True
                    self.start_result_animation("success")
            else:
                self.interface.pre_combat_timer.decrease_time(3)
                self.interface.show_popup("Palavra errada: -3 segundos", duration=1.5)


    def draw_scene(self, screen, player):
        super().draw_scene(screen)
        self.enemy.update_animation(self.manager.dt)
        self.enemy.draw(screen)

        if not player.moving and not self.alreadyGeneratedWords:
            self.word_manager.generate_pre_combat_words(quantity=self.quantity_pre_combat_words)
            self.alreadyGeneratedWords = True

        if not player.moving:
            self.word_manager.draw(screen)
            if not self.result_finalization_animation_active and not self.pre_combat_ended:
                self.interface.draw_battle_timers(screen, "pre_combat",  self.manager.player.moving)

        self.draw_ui(screen)

        for anim in self.book_animations[:]:
            if anim.is_finished():
                self.book_animations.remove(anim)

                explosion = PuffAnimation(position=(anim.end_x, anim.end_y))
                self.explosion_animations.append(explosion)
            else:
                anim.draw(screen)

        for explosion in self.explosion_animations[:]:
            if explosion.is_finished():
                self.explosion_animations.remove(explosion)
            else:
                explosion.draw(screen)

        if self.start_punishin_animation:
            self.enemy.punish()
            self.start_punishin_animation = False

        for effect in self.enemy.punish_effects[:]:
            if effect.is_finished():
                self.enemy.punish_effects.remove(effect)
            else:
                effect.draw(screen)


    def draw_background(self, screen):
        screen.fill((0, 0, 0))

        if self.background_image and not self.is_start_map_animating:
            screen_width, screen_height = screen.get_size()
            bg_width, bg_height = self.background_image.get_size()

            x = (screen_width - bg_width) // 2
            y = (screen_height - bg_height) // 2

            rounded_bg = self.utils.round_image(surface=self.background_image, radius=0)

            screen.blit(rounded_bg, (x, y))

    def update(self):
        self.word_manager.update()

        if self.interface.is_pre_combat_over() and not self.pre_combat_ended:
            self.pre_combat_ended = True
            self.word_manager.words.clear()
            self.start_result_animation("failure")
            self.interface.input_active = False

        if self.interface.popup_time_remaining > 0:
            self.interface.popup_time_remaining -= self.manager.dt

        if self.interface.popup_time_remaining <= 0:
            self.interface.popup_error_message = None

        if self.result_finalization_animation_active:
            self.result_finalization_animation_timer += self.manager.dt
            total_duration = 3
            self.result_finalization_animation_progress = min(self.result_finalization_animation_timer / total_duration, 1)

            if self.result_finalization_animation_progress >= 1:
                self.result_finalization_animation_active = False
                if self.pre_combat_result == "success":
                    self.word_manager.generate_final_pre_combat_word(self.enemy)
                # Ativar o combate real aqui

        for effect in self.enemy.punish_effects:
            effect.update(self.manager.dt)


    def draw_result_pre_combat_animation(self, screen):
        if not self.result_finalization_animation_active:
            return

        width, height = screen.get_size()
        center_y = height // 2

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((50, 50, 50, 185))
        screen.blit(overlay, (0, 0))

        line_duration = 0.3
        line_progress = min(self.result_finalization_animation_timer / line_duration, 1)
        max_line_length = int(width * 0.8)
        line_length = int(max_line_length * line_progress)
        start_x = (width - max_line_length) // 2
        pygame.draw.line(screen, (255, 255, 255), (start_x, center_y), (start_x + line_length, center_y), 5)

        text_duration = 0.3
        text_progress = min(self.result_finalization_animation_timer / text_duration, 0.5)

        result_text = "Pré combate bem sucedido!" if self.pre_combat_result == "success" else "Pré combate foi um fracasso!"
        color = (0, 200, 0) if self.pre_combat_result == "success" else (200, 0, 0)

        text_surface = self.font.render(result_text, True, color)
        text_x = (width - text_surface.get_width()) // 2
        text_final_y = center_y - 100
        text_start_y = center_y
        text_y = text_start_y - int((text_start_y - text_final_y) * text_progress)

        screen.blit(text_surface, (text_x, text_y))

    def start_result_animation(self, result):
        self.result_finalization_animation_active = True
        self.result_finalization_animation_timer = 0
        self.result_finalization_animation_progress = 0
        self.pre_combat_result = result
