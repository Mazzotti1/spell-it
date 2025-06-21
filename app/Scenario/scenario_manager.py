import pygame
from Scenario.battle import Battle
from Attributes.attributes import Attributes
from Factory.enemyFactory import EnemyFactory
from Factory.playerFactory import PlayerFactory
from Scenario.main_menu import MainMenu
class ScenarioManager:
    def __init__(self, player):
        self.current_scenario = None
        self.battle_scenario = None
        self.in_battle = False
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000
        self.player = player
        self.player_final_x = 420
        self.player_final_y = 750
        self.need_to_expand_map = False

    def change_scenario(self, new_scenario):
        self.current_scenario = new_scenario

    def start_battle(self, scenario, enemy, index):
        scene_enemy, biome_path = self.getBattleScene(enemy, index)
        self.battle_scenario = Battle(self, biome_path, scene_enemy, self.player_final_x, self.player_final_y)

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

        self.player.x = self.player_final_x
        self.player.y = self.player_final_y
        self.player.rect.topleft = (self.player.x, self.player.y)
        self.player.moving = False
        self.player.current_frames = self.player.idle_frames

    def update(self):
        if self.current_scenario:
            self.current_scenario.update()

    def draw(self, screen):
        if self.current_scenario:
            self.current_scenario.draw_scene(screen , self.player)

    def getBattleScene(self, enemy, index):
        attributes = self.scale_attributes(index)

        match enemy:
            case "anaconda":
                anaconda = EnemyFactory.create_enemy('Anaconda', attributes, 1200, 550)
                return anaconda, "../assets/scene/battle/amazonic_scenario.png"
            case "calango":
                calango = EnemyFactory.create_enemy('Calango', attributes, 1200, 620)
                return calango, "../assets/scene/battle/caatinga_scenario.png"
            case "jacare":
                jacare = EnemyFactory.create_enemy('Jacare', attributes, 1280, 520)
                return jacare,  "../assets/scene/battle/pantanal_scenario.png"
            case "quero_quero":
                quero_quero = EnemyFactory.create_enemy('Quero-Quero', attributes, 1100, 420)
                return quero_quero, "../assets/scene/battle/pampa_scenario.png"
            case "mico":
                mico = EnemyFactory.create_enemy('Mico', attributes, 1000, 300)
                return mico, "../assets/scene/battle/mata_atlantica_scenario.png"

    def back_to_main(self):
        self.in_battle = False

        if hasattr(self.player, "battle_initial_movement_done"):
            self.player.battle_initial_movement_done = False

        self.player.x = 420
        self.player.y = 750
        self.player.rect.topleft = (self.player.x, self.player.y)
        self.player.moving = False
        self.player.current_frames = self.player.idle_frames

        new_attributes = Attributes(
            dodge=1.0,
            attack_speed=1.0,
            strength=1.0,
            health=50,
            lucky=1.0,
            critical_chance=1.0
        )
        self.player.set_attributes(new_attributes)
        self.player.skills = []
        self.change_scenario(MainMenu(self, self.player))

    def scale_attributes(self, index: int) -> Attributes:
        idx = index + 1
        return Attributes(
            dodge=min(0.1 + 0.02 * idx, 0.5),
            attack_speed=0.5 + 0.05 * idx,
            strength=1 + idx * 2,
            health=5 + idx * 10,
            lucky=0.05 + 0.01 * idx,
            critical_chance=min(0.05 + 0.02 * idx, 0.5)
        )

