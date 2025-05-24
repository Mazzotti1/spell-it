import pygame
import sys
from Scenario.scenario_manager import ScenarioManager
from Scenario.main_menu import MainMenu
from Scenario.battle import Battle
from Attributes.attributes import Attributes
from Entity.Player.player import Player
from Factory.enemyFactory import EnemyFactory
from Factory.playerFactory import PlayerFactory
class App:
    def __init__(self):
      
        pygame.init()
        pygame.display.set_caption("Menu")

        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True 
        
        self.manager = ScenarioManager()
        self.manager.change_scenario(MainMenu(self.manager))

        
        self.player = PlayerFactory.create_player(520, 750)

        anacaonda_attributes = Attributes(
            dodge=0.0, 
            attack_speed=0.0, 
            strength=0, 
            health=0, 
            lucky=0.0, 
            critical_chance=0.0
        )
        self.anaconda = EnemyFactory.create_enemy('Anaconda', anacaonda_attributes, 1200, 550, "../assets/enemys/Anaconda/enemy_anaconda_idle.png")

        quero_quero_attributes = Attributes(
            dodge=0.0, 
            attack_speed=0.0, 
            strength=0, 
            health=0, 
            lucky=0.0, 
            critical_chance=0.0
        )
        self.quero_quero = EnemyFactory.create_enemy('Quero-Quero', quero_quero_attributes, 1100, 420, "../assets/enemys/QueroQuero/enemy_quero_quero_idle.png")

        calango_attributes = Attributes(
            dodge=0.0, 
            attack_speed=0.0, 
            strength=0, 
            health=0, 
            lucky=0.0, 
            critical_chance=0.0
        )
        self.calango = EnemyFactory.create_enemy('Calango', calango_attributes, 1200, 620, "../assets/enemys/Calango/enemy_calango_idle.png")

        jacare_attributes = Attributes(
            dodge=0.0, 
            attack_speed=0.0, 
            strength=0, 
            health=0, 
            lucky=0.0, 
            critical_chance=0.0
        )
        self.jacare = EnemyFactory.create_enemy('Jacaré', jacare_attributes, 1280, 520, "../assets/enemys/Jacare/enemy_jacare_idle.png")

        mico_attributes = Attributes(
            dodge=0.0, 
            attack_speed=0.0, 
            strength=0, 
            health=0, 
            lucky=0.0, 
            critical_chance=0.0
        )
        self.mico = EnemyFactory.create_enemy('Mico', mico_attributes, 1000, 300, "../assets/enemys/Mico/enemy_mico_idle.png")

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

            if isinstance(self.manager.current_scenario, Battle):
                self.player.update_animation(dt)
                self.player.draw(self.screen)

                self.quero_quero.update_animation(dt)
                self.quero_quero.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()
