import pygame
from Scenario.scenario import Scenario
from Scenario.battle import Battle
from Utils.menu_button_hover import MenuButtonHover
from Scenario.map import Map
from Utils.confirm_dialog import ConfirmDialog
from Utils.settings_dialog import SettingsDialog
from Utils.how_to_play_dialog import HowToPlayDialog
from Utils.utils import Utils
class MainMenu(Scenario):
    def __init__(self, manager, player):
        super().__init__()
        self.manager = manager
        self.allow_menu = False
        self.player = player
        self.enable_ground = False
        self.enable_solids = False
        self.font = pygame.font.SysFont(None, 64)
        

        self.buttons_font = Utils.scaled_font(
            path="../assets/fonts/VT323-Regular.ttf",
            base_size=124,
            scale_y=self.manager.scale_y
        )

        self.how_to_play_font = Utils.scaled_font(
            path="../assets/fonts/VT323-Regular.ttf",
            base_size=30,
            scale_y=self.manager.scale_y
        )

        self.background_image = pygame.image.load('../assets/scene/menu/main_menu.png').convert_alpha()
        self.background_image = Utils.scaled_image(
            self.background_image,
            self.manager.scale_x,
            self.manager.scale_y
        )
        self.player_back_idle_sheet = pygame.image.load('../assets/scene/menu/player_back_idle.png').convert_alpha() #3 frames

        self.player_frame_width = self.player_back_idle_sheet.get_width() // 3
        self.player_frame_height = self.player_back_idle_sheet.get_height()

        self.idle_frame_index = 0
        self.idle_frame_timer = 0
        self.idle_frame_delay = 200 
        
        self.menu_buttons = [
            self.create_button("Iniciar", None, (1250, 260), (300, 60), self.start_game),
            self.create_button("Como jogar", None, (1250, 360), (300, 60), self.how_to_play),
            self.create_button("Opções", None, (1250, 460), (300, 60), self.open_settings),
            self.create_button("Sair", None, (1250, 560), (300, 60), self.exit_game),
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
            font=self.how_to_play_font,
            radius=10
        )

        self.how_to_play_dialog = HowToPlayDialog(
            color='gray',
            position=(650, 120),
            size=(900, 800),
            text="Como jogar?",
            text_size=36,
            font=self.how_to_play_font,
            radius=10
        )

    def create_button(self, text, color, position, size, on_click, text_color="black"):
        return MenuButtonHover(
            color=color,
            position=position,
            size=size,
            text=text,
            on_click=on_click,
            text_color=text_color,
            font=self.buttons_font,
            hover_color=(200, 200, 200), 
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
        self.how_to_play_dialog.draw(screen)

    def handle_buttons_event(self, event):
        for btn in self.menu_buttons:
            if not self.how_to_play_dialog.visible:
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
        if not self.confirm_dialog.visible and not self.settings_dialog.visible and not self.how_to_play_dialog.visible:
            self.settings_dialog.visible = True

    def update(self):
        self.idle_frame_timer += self.manager.dt * 700
        if self.idle_frame_timer >= self.idle_frame_delay:
            self.idle_frame_index = (self.idle_frame_index + 1) % 3
            self.idle_frame_timer = 0

    def how_to_play(self):
        if not self.how_to_play_dialog.visible:
            self.how_to_play_dialog.visible = True
