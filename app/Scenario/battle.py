import pygame
from Scenario.scenario import Scenario
from Utils.button import Button
from Interface.interace import Interface
from Words.RandomWordManager import RandomWordManager
from Effects.book_animation import BookAnimation
from Effects.puff_animation import PuffAnimation
from Effects.temporary_effects import TemporaryEffect
from Effects.floating_text import FloatingText
from Effects.custom_sprite_animation import CustomSpriteAnimation
from Effects.punish_animation import PunishAnimation
from Skills.SkillCardAnimation import SkillCardAnimation

##Turno do player enche com muita palavra na tela
##Barra de tempo, 15 segundos
##Barra com 3 niveis de acerto, verde amarelo e vermelho
##Acabou o tempo tentativa de ataque do player com o dano base sendo multiplicado pelo nivel de acerto da barra
##Se acertar verificar o critico sobre o dano base + multiplcador por nivel de acerto

##Se skill for usada timer reseta pra 15 segundos e armazena a açao dela pra verificar o que deve acontecer baseado nela

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
        self.punishment_ended = False
        self.player_turn_ended = False
        self.enemy_turn_ended = False

        self.font = pygame.font.SysFont(None, 64)
        self.critical_img = pygame.image.load("../assets/effects/hits/critical.png").convert_alpha()
        self.dodge_img = pygame.image.load("../assets/effects/hits/dodge.png").convert_alpha()

        self.hurricane = CustomSpriteAnimation(
            "../assets/effects/enemys/furacao_sheet.png",
            (350, 580),
            num_frames=3,
            loop=True,
            frame_duration=0.1,
            total_duration=5.0,
            frame_height= 320,
            frame_width= 320
        )

        self.diagonal_claw = CustomSpriteAnimation(
            "../assets/effects/enemys/garra_diagonal_sheet.png",
            (350 - 50, 750 - 70),
            num_frames=5,
            loop=True,
            frame_duration=0.1,
            total_duration=5.0,
            frame_height= 320,
            frame_width= 320
        )

        self.claw = CustomSpriteAnimation(
            "../assets/effects/enemys/garra_sheet.png",
            (350, 750 - 70),
            num_frames=5,
            loop=True,
            frame_duration=0.1,
            total_duration=5.0,
            frame_height= 320,
            frame_width= 320
        )

        self.lion = CustomSpriteAnimation(
            "../assets/effects/enemys/leao_sheet.png",
            (420, 510),
            num_frames=11,
            loop=True,
            frame_duration=0.05,
            total_duration=5.0,
            frame_height= 320,
            frame_width= 320
        )

        self.bite = CustomSpriteAnimation(
            "../assets/effects/enemys/mordida_sheet.png",
            (350, 620),
            num_frames=5,
            loop=True,
            frame_duration=0.1,
            total_duration=5.0,
            frame_height= 320,
            frame_width= 320
        )

        self.thunder = CustomSpriteAnimation(
            "../assets/effects/enemys/raio_sheet.png",
            (300, 560),
            num_frames=29,
            loop=True,
            frame_duration=0.1,
            total_duration=5.0,
            frame_height= 320,
            frame_width= 320
        )

        self.load_background(biome)

        self.buttons = [
            self.create_button("Encerrar", "red", (1440, 0), (130, 50), manager.end_battle),
        ]
        self.restart_button =   self.create_button("Recomeçar", "orange", (860, 540), (180, 50), self.restart)

        self.pre_combat_time = 15

        self.interface = Interface(manager.player, pre_combat_time=self.pre_combat_time)

        screen_size = (1920, 1080)
        self.word_manager = RandomWordManager(screen_size, self.pre_combat_time, biome, player_position=(self.player_final_x, self.player_final_y))

        self.alreadyGeneratedWords = False
        self.alreadyGeneratedEnemyWords = False

        self.pre_combat_word_count = 0

        self.pre_combat_result = None
        self.result_finalization_animation_progress = 0
        self.result_finalization_animation_active = False
        self.result_finalization_animation_timer = 0

        self.book_animations = []

        self.explosion_animations = []

        self.start_punishin_animation = False
        self.enemy_alive = True
        self.player_turn = False

        self.flash_timer = 0
        self.flash_interval = 120
        self.flash_on = False

        self.temporary_effects = []
        self.floating_texts = []

        self.pending_enemy_attack = False
        self.enemy_attack_animation_active = False
        self.enemy_attack_animation_timer = 0
        self.enemy_attack_animation_duration = 0.7
        self.turn_transition_delay = 0
        self.pending_damage_result = False

        self.enemy_attacks = []
        self.enemy_animation_attacking_started = False

        self.player_hited_animation_active = False
        self.player_hited = []

        self.enemy_hited_animation_active = False
        self.enemy_hited = []

        self.enemy_dying_animation_active = False
        self.enemy_dying = []

        self.player_dying_animation_active = False
        self.defeat_animation_started = False

        self.draw_restart_button = False

        self.victory_animation_started = False
        self.victory_animation_timer = 0

        self.reward_cards = []
        self.showing_reward_cards = False

    def draw_ui(self, screen):
        if not self.manager.player.moving:
            for btn in self.buttons:
                btn.draw(screen)
            self.draw_menu(screen)
            self.interface.draw_input_box(screen)
            self.interface.draw_popup(screen)
            self.interface.draw_health_bar(screen)

            if len(self.manager.player.skills) > 0:
                self.interface.draw_player_skills(screen, self.manager.player)

            if self.draw_restart_button:
                self.restart_button.draw(screen)

            if self.result_finalization_animation_active:
                self.draw_result_pre_combat_animation(screen)
            else:
                if not self.pre_combat_ended:
                    self.interface.draw_battle_timers(screen, "pre_combat", self.manager.player.moving)
                elif not self.punishment_ended and self.pre_combat_ended:
                    self.interface.draw_battle_timers(screen, "punishment", self.manager.player.moving)

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

        if self.draw_restart_button:
            self.restart_button.handle_event(event)

        typed_word = self.interface.handle_input_event(event)
        if typed_word:
            word_obj = self.word_manager.check_word(typed_word)
            self.interface.input_text = ""

            if self.pre_combat_ended and not self.punishment_ended:
                punishment_word = self.word_manager.check_punishment_word(typed_word)
                if punishment_word:
                    self.manager.player.play_skill_animation()
                    self.start_punishin_animation = True
                    damage, is_critical, enemy_alive, did_hit = self.manager.player.attack(self.enemy)

                    if not did_hit:
                        image = self.dodge_img
                        pos = (self.enemy.x, self.enemy.y - 100)
                        self.temporary_effects.append(TemporaryEffect(image, pos, duration=0.5))
                        self.turn_transition_delay = 0.8
                    else:
                        damage = damage
                        pos = (self.enemy.x + 100, self.enemy.y - 80)

                        color = (255, 215, 0) if is_critical else (255, 0, 0)
                        self.floating_texts.append(FloatingText(str(damage), pos, color, self.font, duration=1.0))

                        if is_critical:
                            image = self.critical_img
                            self.temporary_effects.append(TemporaryEffect(image, pos, duration=0.5))

                        self.turn_transition_delay = 0.8

                    self.interface.input_active = False
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
                self.interface.punishment_timer.decrease_time(3)
                self.interface.show_popup("Palavra errada: -3 segundos", duration=1.5)

    def draw_scene(self, screen, player):
        super().draw_scene(screen)
        self.enemy.update_animation(self.manager.dt)
        self.enemy.draw(screen)

        self.manager.player.draw(screen)

        if not player.moving and not self.alreadyGeneratedWords:
            self.word_manager.generate_pre_combat_words(quantity=self.quantity_pre_combat_words)
            self.alreadyGeneratedWords = True

        if not player.moving and not self.alreadyGeneratedEnemyWords and self.enemy_attack_animation_active and len(self.enemy_attacks) > 0:
            self.word_manager.generate_pre_combat_words(quantity=self.quantity_pre_combat_words)
            self.alreadyGeneratedEnemyWords = True

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

        for dying_effect in self.enemy.dying_animations[:]:
            self.enemy.visible = False
            if dying_effect.is_finished():
                self.enemy.dying_animations.remove(dying_effect)
                self.interface.input_active = False
            else:
                dying_effect.draw(screen)

        for effect in self.temporary_effects:
            effect.draw(screen)

        for text in self.floating_texts:
            text.draw(screen)

        if self.enemy_attack_animation_active:
            if not self.enemy_animation_attacking_started:
                self.enemy.set_animation("attacking")
                self.enemy_animation_attacking_started = True

            self.interface.draw_battle_timers(screen, "enemy_turn", self.manager.player.moving)

            match self.enemy.getName():
                case "Anaconda":
                    animation = self.thunder
                case "Calango":
                    animation = self.bite
                case "Jacaré":
                    animation = self.diagonal_claw
                case "Quero-Quero":
                    animation = self.hurricane
                case "Mico":
                    animation = self.lion

            self.enemy_attacks.append(PunishAnimation(animation, delay = 0.0))

        for enemy_attack_animation in self.enemy_attacks[:]:
            if enemy_attack_animation.is_finished():
                self.enemy_attacks.remove(enemy_attack_animation)
                self.enemy.set_animation("idle")
            else:
                enemy_attack_animation.draw(screen)

        if self.player_hited_animation_active:
            self.manager.player.set_animation("hited")
            self.player_hited_animation_active = False

            player_hited_animation = CustomSpriteAnimation(
                "../assets/player/player_hited_sheet.png",
                (self.manager.player.x, self.manager.player.y),
                num_frames=5,
                loop=False,
                frame_duration=0.1,
                total_duration=0.5,
                frame_height= 128,
                frame_width= 128
            )
            self.player_hited.append(player_hited_animation)

        for player_hited_animation in self.player_hited[:]:
            if player_hited_animation.is_finished():
                self.player_hited.remove(player_hited_animation)
                self.manager.player.set_animation("idle")
            else:
                player_hited_animation.draw(screen)

        if self.enemy_hited_animation_active: ## aqui é pra batalha do turno do player
            self.enemy.set_animation("hited")
            self.enemy_hited_animation_active = False

            match self.enemy.getName():
                case "Anaconda":
                    animation = self.enemy.anaconda_hited
                case "Calango":
                    animation = self.enemy.calango_hited
                case "Jacaré":
                    animation = self.enemy.jacare_hited
                case "Quero-Quero":
                    animation = self.enemy.quero_quero_hited
                case "Mico":
                    animation = self.enemy.mico_hited

            self.enemy_hited.append(PunishAnimation(animation, delay = 0))

        for enemy_hited_animation in self.enemy_hited[:]:
            if enemy_hited_animation.is_finished():
                self.enemy_hited.remove(enemy_hited_animation)
                self.enemy.set_animation("idle")
            else:
                enemy_hited_animation.draw(screen)

        if self.enemy_dying_animation_active: ## aqui é pra batalha do turno do player
            self.enemy.set_animation("dying")
            self.enemy_dying_animation_active = False

            match self.enemy.getName():
                case "Anaconda":
                    animation = self.enemy.anaconda_dying
                case "Calango":
                    animation = self.enemy.calango_dying
                case "Jacaré":
                    animation = self.enemy.jacare_dying
                case "Quero-Quero":
                    animation = self.enemy.quero_quero_dying
                case "Mico":
                    animation = self.enemy.mico_dying

            self.enemy_dying.append(PunishAnimation(animation, delay=0))

        for enemy_dying_animation in self.enemy_dying[:]:
            if enemy_dying_animation.is_finished():
                self.enemy_dying.remove(enemy_dying_animation)
                self.enemy.visible = False
            else:
                enemy_dying_animation.draw(screen)

        if self.player_dying_animation_active:
            self.manager.player.set_animation("dying", True)
            self.player_dying_animation_active = False

        if self.victory_animation_started:
            self.victory_animation_timer += self.manager.dt
            total_duration = 3.0
            if self.victory_animation_timer >= total_duration:
                self.victory_animation_started = False
                self.victory_animation_timer = 0.0
                self.start_reward_animation(screen)

        if self.showing_reward_cards:
            for card in self.reward_cards:
                card.draw(screen)


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

        if self.turn_transition_delay > 0:
            self.turn_transition_delay -= self.manager.dt
            return

        if not self.manager.player.is_alive() and not self.defeat_animation_started:
            self.manager.player.visible = False

        if (
            not self.manager.player.is_alive()
            and not self.enemy_attack_animation_active
            and not self.defeat_animation_started
            and len(self.floating_texts) <= 0
            and len(self.temporary_effects) <= 0
        ):
            self.word_manager.words.clear()
            self.start_result_animation("defeat")
            self.defeat_animation_started = True
            self.draw_restart_button = True

        if self.interface.is_pre_combat_over() and not self.pre_combat_ended:
            self.pre_combat_ended = True
            self.word_manager.words.clear()
            self.start_result_animation("failure")
            self.interface.input_active = False
            self.pending_enemy_attack = True

        if (
            self.interface.is_punishment_over()
            and not self.punishment_ended
            and self.enemy.is_alive()
            and self.manager.player.is_alive()
            and self.pre_combat_ended
            and not self.enemy_attack_animation_active
            and len(self.floating_texts) <= 0
            and len(self.temporary_effects) <= 0
        ):
            self.punishment_ended = True
            self.word_manager.words.clear()
            self.alreadyGeneratedEnemyWords = False
            self.start_result_animation("player_turn_started")

        if (
            self.interface.is_punishment_over()
            and not self.punishment_ended
            and not self.enemy.is_alive()
            and self.manager.player.is_alive()
            and self.pre_combat_ended
            and not self.enemy_attack_animation_active
            and len(self.floating_texts) <= 0
            and len(self.temporary_effects) <= 0
        ):
            self.punishment_ended = True
            self.word_manager.words.clear()
            self.start_result_animation("victory")
            self.enemy.visible = False
            self.victory_animation_started = True

        if self.interface.popup_time_remaining > 0:
            self.interface.popup_time_remaining -= self.manager.dt

        if self.interface.popup_time_remaining <= 0:
            self.interface.popup_error_message = None

        if self.result_finalization_animation_active:
            self.result_finalization_animation_timer += self.manager.dt
            total_duration = 3
            self.result_finalization_animation_progress = min(self.result_finalization_animation_timer / total_duration, 1)
            self.interface.input_active = False
            if self.result_finalization_animation_progress >= 1:
                self.result_finalization_animation_active = False
                if self.pre_combat_result == "success":
                    self.word_manager.generate_final_pre_combat_word(self.enemy)
                    self.interface.input_active = True

        for effect in self.enemy.punish_effects:
            effect.update(self.manager.dt)

        for effect_dying in self.enemy.dying_animations:
            self.enemy.visible = False
            effect_dying.update(self.manager.dt)

        for text in self.floating_texts[:]:
            text.update(self.manager.dt)
            if text.is_finished():
                self.floating_texts.remove(text)

        for temp_effect in self.temporary_effects[:]:
            temp_effect.update(self.manager.dt)
            if temp_effect.is_finished():
                self.temporary_effects.remove(temp_effect)

        if not self.result_finalization_animation_active and self.pending_enemy_attack:
            self.pending_enemy_attack = False
            self.enemy_attack_animation_active = True
            self.enemy_attack_animation_timer = 0
            self.player_hited_animation_active = True

        if self.enemy_attack_animation_active:
            self.enemy_attack_animation_timer += self.manager.dt
            if self.enemy_attack_animation_timer >= self.enemy_attack_animation_duration:
                self.enemy_attack_animation_active = False
                self.pending_damage_result = True

        if self.pending_damage_result:
            self.pending_damage_result = False
            result = self.enemy.attack(self.manager.player)

            if result["did_dodge"]:
                image = self.dodge_img
                pos = (self.manager.player.x, self.manager.player.y - 100)
                self.temporary_effects.append(TemporaryEffect(image, pos, duration=0.5))
                self.turn_transition_delay = 0.8
            else:
                damage = result["damage"]
                pos = (self.manager.player.x + 100, self.manager.player.y - 80)

                color = (255, 215, 0) if result["is_critical"] else (255, 0, 0)
                self.floating_texts.append(FloatingText(str(damage), pos, color, self.font, duration=1.0))

                if result["is_critical"]:
                    image = self.critical_img
                    self.temporary_effects.append(TemporaryEffect(image, pos, duration=0.5))

                self.turn_transition_delay = 0.8

            if not result["target_alive"]:
                self.player_dying_animation_active = True
                self.player_hited_animation_active = False

        for enemy_attack_animation in self.enemy_attacks:
            enemy_attack_animation.update(self.manager.dt)

        for player_hited_animation in self.player_hited:
            player_hited_animation.update(self.manager.dt)

        for enemy_hited_animation in self.enemy_hited:
            enemy_hited_animation.update(self.manager.dt)

        for enemy_dying_animation in self.enemy_dying:
            enemy_dying_animation.update(self.manager.dt)

        if self.showing_reward_cards:
            mouse_pos = pygame.mouse.get_pos()
            for card in self.reward_cards:
                card.update(mouse_pos, self.manager.dt)

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

        if self.pre_combat_result == "success":
            result_text = "Pré combate bem sucedido!"
            color = (0, 200, 0)
        elif self.pre_combat_result == "failure":
            result_text = "Pré combate foi um fracasso! Turno do inimigo iniciado!"
            color = (200, 0, 0)
        elif self.pre_combat_result == "victory":
            result_text = "Você venceu!"
            color = (0, 200, 0)
        elif self.pre_combat_result == "player_turn_started":
            result_text = "Seu turno começou!"
            color = (50, 168, 123)
        elif self.pre_combat_result == "defeat":
            result_text = "Você foi derrotado!"
            color = (200, 0, 0)
        else:
            result_text = "Resultado desconhecido."
            color = (200, 0, 0)

        text_surface = self.font.render(result_text, True, color)

        stroke_color = (255, 255, 255)
        stroke_surface = self.font.render(result_text, True, stroke_color)

        text_x = (width - text_surface.get_width()) // 2
        text_final_y = center_y - 100
        text_start_y = center_y
        text_y = text_start_y - int((text_start_y - text_final_y) * text_progress)

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    screen.blit(stroke_surface, (text_x + dx, text_y + dy))

        screen.blit(text_surface, (text_x, text_y))

    def start_result_animation(self, result):
        self.result_finalization_animation_active = True
        self.result_finalization_animation_timer = 0
        self.result_finalization_animation_progress = 0
        self.pre_combat_result = result

    def restart(self):
        self.manager.player.visible = True
        self.manager.back_to_main()

    def start_reward_animation(self, screen):
        self.showing_reward_cards = True
        self.reward_cards.clear()

        screen_center_x = screen.get_width() // 2
        screen_center_y = screen.get_height() // 2

        start_pos = (screen_center_x, screen_center_y + 400)
        target_pos = (screen_center_x, screen_center_y)

        card = SkillCardAnimation(start_pos=start_pos, target_pos=target_pos, player= self.manager.player, manager=self.manager)
        self.reward_cards.append(card)
