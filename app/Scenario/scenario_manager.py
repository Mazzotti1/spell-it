import pygame
from Scenario.battle import Battle
from Attributes.attributes import Attributes
from Factory.enemyFactory import EnemyFactory
class ScenarioManager:
    def __init__(self, player):
        self.current_scenario = None
        self.battle_scenario = None
        self.in_battle = False
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000 
        self.player = player
    def change_scenario(self, new_scenario):
        self.current_scenario = new_scenario

    def start_battle(self, map_scenario, enemy):
        scene_enemy, biome_path = self.getBattleScene(enemy)
        self.battle_scenario = Battle(self, biome_path, scene_enemy)

        self.player.x = -100
        self.player.y = 750
        self.player.rect.topleft = (self.player.x, self.player.y)
        self.player.moving = False
        self.player.battle_initial_movement_done = False 
        self.in_battle = True
        self.current_scenario = self.battle_scenario
        
    def end_battle(self):
        self.in_battle = False
        self.current_scenario = self.map_scenario
        
        if hasattr(self.player, "battle_initial_movement_done"):
            self.player.battle_initial_movement_done = False 

        self.player.x = 420
        self.player.y = 750
        self.player.rect.topleft = (self.player.x, self.player.y)
        self.player.moving = False
        self.player.current_frames = self.player.idle_frames

    def update(self):
        if self.current_scenario:
            self.current_scenario.update()

    def draw(self, screen):
        if self.current_scenario:
            self.current_scenario.draw_scene(screen)
        
    def getBattleScene(self, enemy):
        match enemy:
            case "anaconda":

                anacaonda_attributes = Attributes(
                    dodge=0.0, 
                    attack_speed=0.0, 
                    strength=0, 
                    health=0, 
                    lucky=0.0, 
                    critical_chance=0.0
                )
                anaconda = EnemyFactory.create_enemy('Anaconda', anacaonda_attributes, 1200, 550, "../assets/enemys/Anaconda/enemy_anaconda_idle.png")
                return anaconda, "../assets/scene/battle/amazonic_scenario.png"
            case "calango":

                calango_attributes = Attributes(
                    dodge=0.0, 
                    attack_speed=0.0, 
                    strength=0, 
                    health=0, 
                    lucky=0.0, 
                    critical_chance=0.0
                )
                calango = EnemyFactory.create_enemy('Calango', calango_attributes, 1200, 620, "../assets/enemys/Calango/enemy_calango_idle.png")
                return calango, "../assets/scene/battle/caatinga_scenario.png"
            case "jacare":

                jacare_attributes = Attributes(
                    dodge=0.0, 
                    attack_speed=0.0, 
                    strength=0, 
                    health=0, 
                    lucky=0.0, 
                    critical_chance=0.0
                )
                jacare = EnemyFactory.create_enemy('Jacaré', jacare_attributes, 1280, 520, "../assets/enemys/Jacare/enemy_jacare_idle.png")
                return jacare,  "../assets/scene/battle/pantanal_scenario.png"
            case "quero_quero":

                quero_quero_attributes = Attributes(
                    dodge=0.0, 
                    attack_speed=0.0, 
                    strength=0, 
                    health=0, 
                    lucky=0.0, 
                    critical_chance=0.0
                )
                quero_quero = EnemyFactory.create_enemy('Quero-Quero', quero_quero_attributes, 1100, 420, "../assets/enemys/QueroQuero/enemy_quero_quero_idle.png")
                return quero_quero, "../assets/scene/battle/pampa_scenario.png"
            case "mico":

                mico_attributes = Attributes(
                    dodge=0.0, 
                    attack_speed=0.0, 
                    strength=0, 
                    health=0, 
                    lucky=0.0, 
                    critical_chance=0.0
                )
                mico = EnemyFactory.create_enemy('Mico', mico_attributes, 1000, 300, "../assets/enemys/Mico/enemy_mico_idle.png")
                return mico, "../assets/scene/battle/mata_atlantica_scenario.png"
