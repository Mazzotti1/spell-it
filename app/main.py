import pygame
import sys
from Scenario.scenario_manager import ScenarioManager
from Scenario.main_menu import MainMenu
from Scenario.battle import Battle
from Factory.playerFactory import PlayerFactory
from Scenario.map import Map
from Attributes.attributes import Attributes
from Scenario.audio_manager import AudioManager
class App:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("Menu")

        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.running = True
        self.audio_manager = AudioManager.instance()
        
        attributes = Attributes(
            dodge=10.0,
            attack_speed=71.0,
            strength=7.0,
            health=70,
            lucky=1.2,
            critical_chance=20.0,
            max_health=70
        )
        self.player = PlayerFactory.create_player(-100, 750, attributes)

        display_info = pygame.display.Info()
        real_width = display_info.current_w
        real_height = display_info.current_h

        scale_x = real_width / 1920
        scale_y = real_height / 1080

        self.manager = ScenarioManager(self.player, scale_x, scale_y)
        self.manager.change_scenario(MainMenu(self.manager, self.player))

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue

                if hasattr(self.manager.current_scenario, 'confirm_dialog'):
                    if self.manager.current_scenario.confirm_dialog.visible:
                        self.manager.current_scenario.confirm_dialog.handle_event(event)
                        continue

                if hasattr(self.manager.current_scenario, 'settings_dialog'):
                    if self.manager.current_scenario.settings_dialog.visible:
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            self.manager.current_scenario.settings_dialog.cancel()
                            continue

                if hasattr(self.manager.current_scenario, 'how_to_play_dialog'):
                    if self.manager.current_scenario.how_to_play_dialog.visible:
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            self.manager.current_scenario.how_to_play_dialog.visible = False
                            continue

                if getattr(self.manager.current_scenario, 'is_menu_open', False):
                        if getattr(self.manager.current_scenario, 'allow_pause_menu', True):
                            menu = self.manager.current_scenario.menu
                            if menu.confirm_dialog.visible:
                                menu.confirm_dialog.handle_event(event)
                            else:
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                    self.manager.current_scenario.open_menu()
                                else:
                                    menu.handle_menu_buttons_event(event)
                            continue
                        else:
                            continue

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if getattr(self.manager.current_scenario, 'allow_pause_menu', True):
                                self.manager.current_scenario.open_menu()
                            continue

                if hasattr(self.manager.current_scenario, "handle_buttons_event"):
                    self.manager.current_scenario.handle_buttons_event(event)

                if isinstance(self.manager.current_scenario, Map):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        for node in self.manager.current_scenario.nodes:
                            if node['rect'].collidepoint(mouse_pos):
                                self.manager.current_scenario.handle_node_click(node)

                        self.manager.current_scenario.handle_perk_click(mouse_pos)

                if hasattr(self.manager.current_scenario, 'settings_dialog'):
                    settings_dialog = self.manager.current_scenario.settings_dialog
                    if settings_dialog.visible:
                        settings_dialog.handle_event(event)

                        if settings_dialog.unsaved_changes_dialog.visible:
                            settings_dialog.unsaved_changes_dialog.handle_event(event)
                        elif settings_dialog.save_confirm_dialog.visible:
                            settings_dialog.save_confirm_dialog.handle_event(event)
                        continue

                if hasattr(self.manager.current_scenario, 'how_to_play_dialog'):
                    how_to_play_dialog = self.manager.current_scenario.how_to_play_dialog
                    if how_to_play_dialog.visible:
                        how_to_play_dialog.handle_event(event)
                        continue

            self.manager.update()
            self.manager.draw(self.screen)
            self.audio_manager.update()

            if isinstance(self.manager.current_scenario, Battle):
                battle = self.manager.current_scenario
                self.player.update_movement(dt)
                self.player.update_animation(dt)
                if not hasattr(self.player, "battle_initial_movement_done") or not self.player.battle_initial_movement_done:
                    self.player.start_moving_to(420, 750, direction="walking_right")
                    self.player.battle_initial_movement_done = True

                for card in battle.reward_cards:
                    card.handle_event(event)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()
