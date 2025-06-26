import random
from Entity.entity import Entity
from Effects.custom_sprite_animation import CustomSpriteAnimation
from Effects.punish_animation import PunishAnimation
from Effects.falling_anvil_animation import FallingAnvilAnimation
class Enemy(Entity):
    def __init__(self, type, attributes, x=0, y=0):
        super().__init__(x, y, type, attributes, width=384, height=384)

        self.load_enemy_assets()

        self.punish_effects = []
        self.dying_animations = []
        self.visible = True
        self.forced_miss_turns = 0
        self.player_recieve_lucky = 0

    def load_enemy_assets(self):
        base_path = "../assets/enemys"
        name = self.name.replace("-", "").replace(" ", "").lower()
        idle_sprite = f"{base_path}/{self.name}/enemy_{name}_idle.png"
        attacking_sprite = f"{base_path}/{self.name}/attacking/{name}_attacking_sheet.png"
        hitted_sprite = f"{base_path}/{self.name}/hited/{name}_hited.png"
        dying_sprite = f"{base_path}/Dying/{name}_dying.png"

        self.load_animations({
            "idle": (idle_sprite, 0.15),
            "attacking": (attacking_sprite, 0.1),
            "hited": (hitted_sprite, 0.1),
            "dying": (dying_sprite, 0.1),
        })

        if self.name == "Anaconda":
            self.anaconda_hited = CustomSpriteAnimation(
                hitted_sprite,
                (self.x, self.y),
                num_frames=5,
                loop=False,
                frame_duration=0.1,
                total_duration=0.5,
                frame_height=384,
                frame_width=384
            )
            self.anaconda_dying = CustomSpriteAnimation(
                dying_sprite,
                (self.x, self.y),
                num_frames=7,
                loop=False,
                frame_duration=0.1,
                total_duration=4.0,
                frame_height=384,
                frame_width=384
            )
        elif self.name == "Calango":
            self.calango_hited = CustomSpriteAnimation(
                hitted_sprite,
                (self.x, self.y),
                num_frames=5,
                loop=False,
                frame_duration=0.1,
                total_duration=0.5,
                frame_height=384,
                frame_width=384
            )
            self.calango_dying = CustomSpriteAnimation(
                dying_sprite,
                (self.x, self.y),
                num_frames=8,
                loop=False,
                frame_duration=0.1,
                total_duration=3.5,
                frame_height=384,
                frame_width=384
            )
        elif self.name == "Jacare":
            self.jacare_hited = CustomSpriteAnimation(
                hitted_sprite,
                (self.x, self.y),
                num_frames=6,
                loop=False,
                frame_duration=0.1,
                total_duration=0.5,
                frame_height=384,
                frame_width=384
            )
            self.jacare_dying = CustomSpriteAnimation(
                dying_sprite,
                (self.x, self.y),
                num_frames=8,
                loop=False,
                frame_duration=0.1,
                total_duration=3.5,
                frame_height=384,
                frame_width=384
            )
        elif self.name == "Mico":
            self.mico_hited = CustomSpriteAnimation(
                hitted_sprite,
                (self.x, self.y),
                num_frames=8,
                loop=False,
                frame_duration=0.1,
                total_duration=0.5,
                frame_height=384,
                frame_width=384
            )
            self.mico_dying = CustomSpriteAnimation(
                dying_sprite,
                (self.x, self.y),
                num_frames=12,
                loop=False,
                frame_duration=0.1,
                total_duration=4.5,
                frame_height=384,
                frame_width=384
            )
        elif self.name == "Quero-Quero":
            self.quero_quero_hited = CustomSpriteAnimation(
                hitted_sprite,
                (self.x, self.y),
                num_frames=5,
                loop=False,
                frame_duration=0.01,
                total_duration=0.5,
                frame_height=384,
                frame_width=384
            )
            self.quero_quero_dying = CustomSpriteAnimation(
                dying_sprite,
                (self.x, self.y),
                num_frames=8,
                loop=False,
                frame_duration=0.1,
                total_duration=3.5,
                frame_height=384,
                frame_width=384
            )
        elif self.name == "Tupinajé":
            self.tupinaje_hited = CustomSpriteAnimation(
                hitted_sprite,
                (self.x, self.y),
                num_frames=12,
                loop=False,
                frame_duration=0.01,
                total_duration=0.5,
                frame_height=384,
                frame_width=384
            )
            self.tupinaje_dying = CustomSpriteAnimation(
                dying_sprite,
                (self.x, self.y),
                num_frames=12,
                loop=False,
                frame_duration=0.1,
                total_duration=3.5,
                frame_height=384,
                frame_width=384
            )
        elif self.name == "Don Jacarone":
            self.don_jacarone_hited = CustomSpriteAnimation(
                hitted_sprite,
                (self.x, self.y),
                num_frames=10,
                loop=False,
                frame_duration=0.01,
                total_duration=0.5,
                frame_height=384,
                frame_width=384
            )
            self.don_jacarone_dying = CustomSpriteAnimation(
                dying_sprite,
                (self.x, self.y),
                num_frames=12,
                loop=False,
                frame_duration=0.1,
                total_duration=3.5,
                frame_height=384,
                frame_width=384
            )
        elif self.name == "Dr. Pestis":
            self.dr_pestis_hited = CustomSpriteAnimation(
                hitted_sprite,
                (self.x, self.y),
                num_frames=10,
                loop=False,
                frame_duration=0.01,
                total_duration=0.5,
                frame_height=384,
                frame_width=384
            )
            self.dr_pestis_dying = CustomSpriteAnimation(
                dying_sprite,
                (self.x, self.y),
                num_frames=11,
                loop=False,
                frame_duration=0.1,
                total_duration=3.5,
                frame_height=384,
                frame_width=384
            )
        elif self.name == "Vermaçu":
            self.vermaçu_hited = CustomSpriteAnimation(
                hitted_sprite,
                (self.x, self.y),
                num_frames=10,
                loop=False,
                frame_duration=0.01,
                total_duration=0.5,
                frame_height=384,
                frame_width=384
            )
            self.vermaçu_dying = CustomSpriteAnimation(
                dying_sprite,
                (self.x, self.y),
                num_frames=12,
                loop=False,
                frame_duration=0.1,
                total_duration=3.5,
                frame_height=384,
                frame_width=384
            )
        elif self.name == "Froguelhão":
            self.froguelhao_hited = CustomSpriteAnimation(
                hitted_sprite,
                (self.x, self.y),
                num_frames=7,
                loop=False,
                frame_duration=0.01,
                total_duration=0.5,
                frame_height=384,
                frame_width=384
            )
            self.froguelhao_dying = CustomSpriteAnimation(
                dying_sprite,
                (self.x, self.y),
                num_frames=10,
                loop=False,
                frame_duration=0.1,
                total_duration=3.5,
                frame_height=384,
                frame_width=384
            )

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def get_position(self):
        return (self.x, self.y)

    def attack(self, target: "Entity"):
        final_crit_chance = min(1.0, (self.get_critical_chance() / 100.0) * self.get_lucky())
        is_critical = random.random() < final_crit_chance

        damage = self.get_strength()

        if is_critical:
            damage *= 2

        if self.player_recieve_lucky > 0:
            dodge = target.get_dodge() * 4
            self.player_recieve_lucky -= 1
        else:
            dodge = (target.get_dodge() / 100.0)

        base_hit_chance = self.get_attack_speed() / 100.0
        hit_chance = base_hit_chance * self.get_lucky()

        final_hit_chance = min(1.0, max(0.0, hit_chance - dodge))

        if self.forced_miss_turns > 0:
            did_hit = False
            self.forced_miss_turns -= 1
        else:
            did_hit = random.random() < final_hit_chance

        if not did_hit:
            return {
                "damage": 0,
                "is_critical": is_critical,
                "did_dodge": True,
                "target_alive": target.is_alive()
            }
          
        target.set_health(max(0, target.get_health() - damage))
        
        return {
            "damage": damage,
            "is_critical": is_critical,
            "did_dodge": False,
            "target_alive": target.is_alive()
        }


    def punish(self):
        self.punish_effects.clear()

        if self.name in ["Anaconda", "Tupinajé"]:
                animation_hit = self.anaconda_hited if self.name == "Anaconda" else self.tupinaje_hited
                animation_dying = self.anaconda_dying if self.name == "Anaconda" else self.tupinaje_dying

                anvil_start_y = self.y - 400
                anvil_anim = FallingAnvilAnimation(
                    "../assets/effects/anvil/anvil_sheet.png",
                    (self.x, anvil_start_y),
                    (self.x, self.y),
                    duration=0.2,
                    num_frames=1,
                    frame_duration=0.6,
                    frame_height=320,
                    frame_width=320
                )
                self.punish_effects.append(PunishAnimation(anvil_anim))

                stars_anim = CustomSpriteAnimation(
                    "../assets/effects/anvil/shining_sheet.png",
                    (self.x, self.y),
                    frame_duration=0.2,
                    num_frames=7,
                    loop=True,
                    total_duration=2.5,
                    frame_height=320,
                    frame_width=320
                )

                self.punish_effects.append(PunishAnimation(stars_anim, delay=0.6))
                self.punish_effects.append(PunishAnimation(animation_hit, delay=0.7))

                if not self.is_alive():
                    self.dying_animations.append(PunishAnimation(animation_dying, delay=0.0))

        elif self.name in ["Calango", "Vermaçu"]:
            animation_hit = self.calango_hited if self.name == "Calango" else self.vermaçu_hited
            animation_dying = self.calango_dying if self.name == "Calango" else self.vermaçu_dying

            flame = CustomSpriteAnimation(
                "../assets/effects/flame/fire_sheet.png",
                (self.x, self.y),
                frame_duration=0.05,
                num_frames=7,
                loop=True,
                total_duration=3.0,
                frame_height=320,
                frame_width=320
            )
            self.punish_effects.append(PunishAnimation(flame))
            self.punish_effects.append(PunishAnimation(animation_hit, delay=0.6))

            if not self.is_alive():
                self.dying_animations.append(PunishAnimation(animation_dying, delay=0.0))

        elif self.name in ["Jacare", "Don Jacarone"]:
            animation_hit = self.jacare_hited if self.name == "Jacare" else self.don_jacarone_hited
            animation_dying = self.jacare_dying if self.name == "Jacare" else self.don_jacarone_dying

            firefly = CustomSpriteAnimation(
                "../assets/effects/tornado/big_tornado_sheet.png",
                (self.x, self.y - 70),
                frame_duration=0.05,
                num_frames=20,
                loop=True,
                total_duration=2.5,
                frame_height=512,
                frame_width=512
            )
            self.punish_effects.append(PunishAnimation(firefly))
            self.punish_effects.append(PunishAnimation(animation_hit, delay=0.2))

            if not self.is_alive():
                self.dying_animations.append(PunishAnimation(animation_dying, delay=0.5))

        elif self.name in ["Quero-Quero", "Dr. Pestis"]:
            animation_hit = self.quero_quero_hited if self.name == "Quero-Quero" else self.dr_pestis_hited
            animation_dying = self.quero_quero_dying if self.name == "Quero-Quero" else self.dr_pestis_dying

            tornado = CustomSpriteAnimation(
                "../assets/effects/tornado/tornado_sheet.png",
                (self.x, self.y),
                frame_duration=0.05,
                num_frames=7,
                loop=True,
                total_duration=3.0,
                frame_height=320,
                frame_width=320
            )
            self.punish_effects.append(PunishAnimation(tornado))
            self.punish_effects.append(PunishAnimation(animation_hit, delay=0.2))

            if not self.is_alive():
                self.dying_animations.append(PunishAnimation(animation_dying, delay=0.5))

        elif self.name in ["Mico", "Froguelhão"]:
            animation_hit = self.mico_hited if self.name == "Mico" else self.froguelhao_hited
            animation_dying = self.mico_dying if self.name == "Mico" else self.froguelhao_dying

            storm = CustomSpriteAnimation(
                "../assets/effects/storm/storm_sheet.png",
                (self.x, self.y - 180),
                num_frames=12,
                loop=True,
                frame_duration=0.1,
                total_duration=2.0,
                frame_height=320,
                frame_width=512
            )
            self.punish_effects.append(PunishAnimation(storm))
            self.punish_effects.append(PunishAnimation(animation_hit, delay=0.2))

            if not self.is_alive():
                self.dying_animations.append(PunishAnimation(animation_dying, delay=0.5))

    def set_animation(self, name: str, play_once: bool = False):
        self.current_frames = getattr(self, f"{name}_frames")
        self.current_animation = name
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_play_once = play_once

        enemy_key = self.name.lower().replace('-', '_').replace(' ', '_')

        if name == "hited":
            hited_anim = getattr(self, f"{enemy_key}_hited", None)
            if hited_anim:
                hited_anim.reset()
                self.punish_effects.append(PunishAnimation(hited_anim, delay=0))

            self._play_extra_effect(enemy_key)

        elif name == "dying":
            dying_anim = getattr(self, f"{enemy_key}_dying", None)
            if dying_anim:
                self.dying_animations.append(PunishAnimation(dying_anim, delay=0))

            self._play_extra_effect(enemy_key)

    def _play_extra_effect(self, enemy_key: str):
        if enemy_key in ["anaconda", "tupinajé"]:
            anvil_start_y = self.y - 400
            anvil = FallingAnvilAnimation(
                "../assets/effects/anvil/anvil_sheet.png",
                (self.x, anvil_start_y),
                (self.x, self.y),
                duration=0.2,
                num_frames=1,
                frame_duration=0.6,
                frame_height=320,
                frame_width=320
            )
            stars = CustomSpriteAnimation(
                "../assets/effects/anvil/shining_sheet.png",
                (self.x, self.y),
                frame_duration=0.2,
                num_frames=7,
                loop=True,
                total_duration=2.5,
                frame_height=320,
                frame_width=320
            )
            self.punish_effects.append(PunishAnimation(anvil))
            self.punish_effects.append(PunishAnimation(stars, delay=0.6))

        elif enemy_key in ["calango", "vermaçu"]:
            flame = CustomSpriteAnimation(
                "../assets/effects/flame/fire_sheet.png",
                (self.x, self.y),
                frame_duration=0.05,
                num_frames=7,
                loop=True,
                total_duration=3.0,
                frame_height=320,
                frame_width=320
            )
            self.punish_effects.append(PunishAnimation(flame))

        elif enemy_key in ["jacare", "don_jacarone"]:
            tornado = CustomSpriteAnimation(
                "../assets/effects/tornado/big_tornado_sheet.png",
                (self.x, self.y - 70),
                frame_duration=0.05,
                num_frames=20,
                loop=True,
                total_duration=2.5,
                frame_height=512,
                frame_width=512
            )
            self.punish_effects.append(PunishAnimation(tornado))

        elif enemy_key in ["quero_quero", "dr._pestis"]:
            tornado = CustomSpriteAnimation(
                "../assets/effects/tornado/tornado_sheet.png",
                (self.x, self.y),
                frame_duration=0.05,
                num_frames=7,
                loop=True,
                total_duration=3.0,
                frame_height=320,
                frame_width=320
            )
            self.punish_effects.append(PunishAnimation(tornado))

        elif enemy_key in ["mico", "froguelhão"]:
            storm = CustomSpriteAnimation(
                "../assets/effects/storm/storm_sheet.png",
                (self.x, self.y - 180),
                frame_duration=0.1,
                num_frames=12,
                loop=True,
                total_duration=2.0,
                frame_height=320,
                frame_width=512
            )
            self.punish_effects.append(PunishAnimation(storm))