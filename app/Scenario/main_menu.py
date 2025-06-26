import pygame
from Scenario.scenario import Scenario
from Scenario.battle import Battle
from Utils.button import Button
from Scenario.map import Map
from Utils.confirm_dialog import ConfirmDialog
from Utils.settings_dialog import SettingsDialog

class MainMenu(Scenario):
    def __init__(self, manager, player):
        super().__init__()
        self.manager = manager
        self.allow_menu = False
        self.player = player
        self.enable_ground = False
        self.enable_solids = False
        self.font = pygame.font.SysFont(None, 64)

        self.buttons_font = pygame.font.Font("../assets/fonts/VT323-Regular.ttf", 64)

        self.background_image = pygame.image.load('../assets/scene/menu/main_menu.png').convert_alpha()
        self.player_back_idle_sheet = pygame.image.load('../assets/scene/menu/player_back_idle.png').convert_alpha() #3 frames

        self.player_frame_width = self.player_back_idle_sheet.get_width() // 3
        self.player_frame_height = self.player_back_idle_sheet.get_height()

        self.idle_frame_index = 0
        self.idle_frame_timer = 0
        self.idle_frame_delay = 200 
        
        self.menu_buttons = [
            self.create_button("Iniciar", None, (1250, 260), (150, 50), self.start_game),
            self.create_button("Como jogar", None, (1250, 360), (150, 50), self.how_to_play),
            self.create_button("Opções", None, (1250, 460), (150, 50), self.open_settings),
            self.create_button("Sair", None, (1250, 560), (150, 50), self.exit_game),
        ]

        self.confirm_dialog = ConfirmDialog(
            title="Deseja Fechar o jogo?",
            message="Ao confirmar o jogo será fechado.",
            on_confirm=self.confirm_exit,
            on_cancel=self.cancel_exit,
            confirm_text="Fechar",
            cancel_text="Cancelar"
        )

        self.settings_dialog = SettingsDialog(
            color='gray',
            position=(650, 120),
            size=(600, 800),
            text="Configurações",
            text_size=36,
            font=None,
            radius=10
        )

    def create_button(self, text, color, position, size, on_click, text_color="black"):
        return Button(
            color=color,
            position=position,
            size=size,
            text=text,
            on_click=on_click,
            text_color=text_color,
            font=self.buttons_font
        )

    def draw_background(self, screen):
        screen.blit(self.background_image, (0, 0))

        frame_rect = pygame.Rect(
            self.idle_frame_index * self.player_frame_width,
            0,
            self.player_frame_width,
            self.player_frame_height
        )
        frame = self.player_back_idle_sheet.subsurface(frame_rect)

        scaled_frame = pygame.transform.scale(
            frame,
            (self.player_frame_width // 2, self.player_frame_height // 2)
        )

        screen.blit(scaled_frame, (100, screen.get_height() - scaled_frame.get_height() - 50))

    def draw_ui(self, screen):
        for btn in self.menu_buttons:
            btn.draw(screen)
        self.confirm_dialog.draw(screen)
        self.settings_dialog.draw(screen)

    def handle_buttons_event(self, event):
        for btn in self.menu_buttons:
            btn.handle_event(event)

    def exit_game(self):
        if not self.confirm_dialog.visible and not self.settings_dialog.visible:
            self.confirm_dialog.visible = True

    def confirm_exit(self):
        self.confirm_dialog.visible = False
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def cancel_exit(self):
        self.confirm_dialog.visible = False

    def start_game(self):
        if not self.confirm_dialog.visible and not self.settings_dialog.visible:
            self.manager.change_scenario(Map(self.manager, "../assets/scene/map/hd_m/map_1.png", self.player))
         
    def open_settings(self):
        if not self.confirm_dialog.visible and not self.settings_dialog.visible:
            self.settings_dialog.visible = True

    def update(self):
        self.idle_frame_timer += self.manager.dt
        if self.idle_frame_timer >= self.idle_frame_delay:
            self.idle_frame_index = (self.idle_frame_index + 1) % 3
            self.idle_frame_timer = 0

    def how_to_play(self):
        pass