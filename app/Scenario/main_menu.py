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

        self.menu_buttons = [
            self.create_button("Iniciar", "green", (900, 410), (130, 50), self.start_game),
            self.create_button("Opções", "orange", (900, 510), (130, 50), self.open_settings),
            self.create_button("Sair", "red", (900, 610), (130, 50), self.exit_game, text_color="white"),
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
            text_color=text_color
        )

    def draw_background(self, screen):
        screen.fill((15, 15, 15))

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