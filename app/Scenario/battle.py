import pygame
from Scenario.scenario import Scenario
from Utils.button import Button
from Interface.interace import Interface
from Words.RandomWordManager import RandomWordManager

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
        self.word_manager.generate_pre_combat_words(quantity=self.quantity_pre_combat_words)

        self.turn_started = False
        self.pre_combat_word_count = 0

    def draw_ui(self, screen):
        for btn in self.buttons:
            btn.draw(screen)
        self.draw_menu(screen)
        self.interface.draw_input_box(screen)

        if not self.pre_combat_ended:
            self.interface.draw_battle_timers(screen, "pre_combat")

        if self.turn_started:
            self.interface.draw_battle_timers(screen, "turn")

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
            isValidWord = self.word_manager.check_word(typed_word)
            self.interface.input_text = "" 
            
            if isValidWord:
                self.pre_combat_word_count += 1
                if self.pre_combat_word_count >= self.quantity_pre_combat_words:
                    self.pre_combat_ended = True
        
    def draw_scene(self, screen, player):
        super().draw_scene(screen)
        self.enemy.update_animation(self.manager.dt)
        self.enemy.draw(screen)
        self.word_manager.draw(screen)

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
        if self.interface.is_pre_combat_over():
            self.pre_combat_ended = True
            self.turn_started = True