import pygame
import sys
from Scenario.scenario_manager import ScenarioManager
from Scenario.main_menu import MainMenu
from Attributes.attributes import Attributes
from Entity.Player.player import Player

class App:
    def __init__(self):
      
        pygame.init()
        pygame.display.set_caption("Menu")

        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True 
        
        self.manager = ScenarioManager()
        self.manager.change_scenario(MainMenu(self.manager))

        player_attributes = Attributes(
            dodge=0.1, 
            attack_speed=1.0, 
            strength=10, 
            health=100, 
            lucky=0.05, 
            critical_chance=0.1
        )

        self.player = Player("Aurélio", player_attributes, 368, 268)
        self.player.rect = pygame.Rect(368, 268, self.player.width, self.player.height)

        self.player.current_frames = self.player.idle_frames
        self.player.frame_index = 0
        self.player.animation_timer = 0
        self.player.current_frame = self.player.current_frames[0] if self.player.current_frames else None
        
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if hasattr(self.manager.current_scenario, "handle_buttons_event"):
                    self.manager.current_scenario.handle_buttons_event(event)

            self.manager.update()
            self.manager.draw(self.screen)

            self.player.animation_timer += dt
            if self.player.animation_timer >= self.player.frame_duration:
                self.player.frame_index = (self.player.frame_index + 1) % len(self.player.current_frames)
                self.player.animation_timer = 0

            self.player.current_frame = self.player.current_frames[self.player.frame_index]

            if self.player.current_frame:
                self.player.draw(self.screen)
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()
