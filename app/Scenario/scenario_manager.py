import pygame
from Scenario.battle import Battle
from Attributes.attributes import Attributes
from Factory.enemyFactory import EnemyFactory
from Factory.playerFactory import PlayerFactory
from Scenario.main_menu import MainMenu
from Scenario.audio_manager import AudioManager
class ScenarioManager:
    def __init__(self, player, scale_x, scale_y):
        self.current_scenario = None
        self.battle_scenario = None
        self.in_battle = False
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000
        self.player = player
        self.player_final_x = 420
        self.player_final_y = 750
        self.need_to_expand_map = False

        self.scale_x = scale_x
        self.scale_y = scale_y


        self.audio_manager = AudioManager.instance()
        
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

    def start_boss_battle(self, scenario, boss, index):
        scene_enemy, biome_path = self.getBossBattleScene(boss, index)

        if index in [6, 7]:
            isLastBattle = True
        else:
            isLastBattle = False

        self.boss_battle_scenario = Battle(self, biome_path, scene_enemy, self.player_final_x, self.player_final_y, isBossBattle=True, isLastBattle=isLastBattle)

        self.player.x = -100
        self.player.y = 750
        self.player.rect.topleft = (self.player.x, self.player.y)
        self.player.moving = False
        self.player.battle_initial_movement_done = False
        self.in_battle = True
        self.current_scenario = self.boss_battle_scenario

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

    def getBossBattleScene(self, enemy, index):
        attributes = self.boss_scale_attributes(index)

        match enemy:
            case "tupinaje":
                tupinaje = EnemyFactory.create_enemy('Tupinajé', attributes, 1200, 550)
                return tupinaje, "../assets/scene/battle/amazonic_scenario.png"
            case "vermaçu":
                vermaçu = EnemyFactory.create_enemy('Vermaçu', attributes, 1200, 580)
                return vermaçu, "../assets/scene/battle/caatinga_scenario.png"
            case "donJacarone":
                donJacarone = EnemyFactory.create_enemy('Don Jacarone', attributes, 1280, 520)
                return donJacarone,  "../assets/scene/battle/pantanal_scenario.png"
            case "drPestis":
                drPestis = EnemyFactory.create_enemy('Dr. Pestis', attributes, 1100, 420)
                return drPestis, "../assets/scene/battle/pampa_scenario.png"
            case "froguelhao":
                froguelhao = EnemyFactory.create_enemy('Froguelhão', attributes, 1100, 560)
                return froguelhao, "../assets/scene/battle/mata_atlantica_scenario.png"

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
            dodge=10.0,
            attack_speed=71.0,
            strength=7.0,
            health=70,
            lucky=1.2,
            critical_chance=20.0,
            max_health=70
        )
        self.player.set_attributes(new_attributes)
        self.player.skills = []
        self.player.all_acquired_skills = []
        self.change_scenario(MainMenu(self, self.player))

    def scale_attributes(self, index: int) -> Attributes:
        idx = index + 1
        return Attributes(
            dodge=min(10 + 2 * idx, 50),
            attack_speed=65 + idx * 2,
            strength=2 + idx * 2,
            health=5 + idx * 20,
            lucky=1.2,
            critical_chance=min(5 + 2 * idx, 50),
            max_health=5 + idx * 20,
        )

    def boss_scale_attributes(self, index: int) -> Attributes:
        idx = index + 1
        return Attributes(
            dodge=min(10 + 2 * idx, 50),
            attack_speed=65 + idx * 2,
            strength=4 + idx * 2,
            health=65 + idx * 10,
            lucky=1.2,
            critical_chance=min(10 + 2 * idx, 50),
            max_health=65 + idx * 10,
        )
