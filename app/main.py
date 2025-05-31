import pygame
import sys
from Scenario.scenario_manager import ScenarioManager
from Scenario.main_menu import MainMenu
from Scenario.battle import Battle
from Factory.playerFactory import PlayerFactory
from Scenario.map import Map
from Attributes.attributes import Attributes
class App:
    def __init__(self):
      
        pygame.init()
        pygame.display.set_caption("Menu")

        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True 
        

        attributes = Attributes(
            dodge=1.0, 
            attack_speed=1.0, 
            strength=1.0, 
            health=5, 
            lucky=1.0, 
            critical_chance=1.0
        )
        self.player = PlayerFactory.create_player(-100, 750, attributes)

        self.manager = ScenarioManager(self.player)
        self.manager.change_scenario(MainMenu(self.manager, self.player))
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.manager.current_scenario.open_menu()

                if hasattr(self.manager.current_scenario, "handle_buttons_event"):
                    self.manager.current_scenario.handle_buttons_event(event)

                if isinstance(self.manager.current_scenario, Map):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        for node in self.manager.current_scenario.nodes:
                            if node['rect'].collidepoint(mouse_pos):
                                self.manager.current_scenario.handle_node_click(node)
                                
                        self.manager.current_scenario.handle_perk_click(mouse_pos)
                    
            self.manager.update()
            self.manager.draw(self.screen)

            if isinstance(self.manager.current_scenario, Battle):
                self.player.update_movement(dt)
                self.player.update_animation(dt)
                self.player.draw(self.screen)
                if not hasattr(self.player, "battle_initial_movement_done") or not self.player.battle_initial_movement_done:
                    self.player.start_moving_to(420, 750, direction="walking_right") 
                    self.player.battle_initial_movement_done = True

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()
