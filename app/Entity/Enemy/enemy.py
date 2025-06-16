import random
from Entity.entity import Entity
from Effects.custom_sprite_animation import CustomSpriteAnimation
from Effects.punish_animation import PunishAnimation
from Effects.falling_anvil_animation import FallingAnvilAnimation
class Enemy(Entity):
    def __init__(self, type, attributes, x=0, y=0, 
                 idle_sprite="../assets/enemys/Anaconda/enemy_anaconda_idle_sprite.png", 
                 attacking_sprite="../assets/enemys/Anaconda/attacking/anaconda_attacking_sheet.png",
                 hitted_sprite = "../assets/enemys/Anaconda/hited/anaconda_hited.png",
                 dying_sprite = "../assets/enemys/Dying/anaconda_dying.png",):
        super().__init__(x, y, type, attributes, width=384, height=384)

        self.load_animations({
            "idle": (idle_sprite, 0.15),
            "attacking":(attacking_sprite, 0.1),
            "hited": (hitted_sprite, 0.1),
            "dying": (dying_sprite, 0.1),
        })

        self.punish_effects = []
        self.dying_animations = []
        self.visible = True

        self.anaconda_hited = CustomSpriteAnimation(
            "../assets/enemys/Anaconda/hited/anaconda_hited.png",
            (self.x, self.y),
            num_frames=5,
            loop=True,
            frame_duration=0.1,
            total_duration=0.5,
            frame_height= 384,
            frame_width= 384
        )

        self.mico_hited = CustomSpriteAnimation(
            "../assets/enemys/Mico/hited/mico_hited.png",
            (self.x, self.y),
            num_frames=8,
            loop=True,
            frame_duration=0.07,
            total_duration=0.5,
            frame_height= 384,
            frame_width= 384
        )

        self.calango_hited = CustomSpriteAnimation(
            "../assets/enemys/Calango/hited/calango_hited.png",
            (self.x, self.y),
            num_frames=5,
            loop=True,
            frame_duration=0.01,
            total_duration=0.5,
            frame_height= 384,
            frame_width= 384
        )

        self.jacare_hited = CustomSpriteAnimation(
            "../assets/enemys/Jacare/hited/jacare_hited.png",
            (self.x, self.y),
            num_frames=6,
            loop=True,
            frame_duration=0.01,
            total_duration=0.5,
            frame_height= 384,
            frame_width= 384
        )

        self.quero_quero_hited = CustomSpriteAnimation(
            "../assets/enemys/QueroQuero/hited/quero_quero_hited.png",
            (self.x, self.y),
            num_frames=5,
            loop=True,
            frame_duration=0.01,
            total_duration=0.5,
            frame_height= 384,
            frame_width= 384
        )

        self.anaconda_dying = CustomSpriteAnimation(
            "../assets/enemys/Dying/anaconda_dying.png",
            (self.x, self.y),
            num_frames=7,
            loop=False,
            frame_duration=0.1,
            total_duration=3.5,
            frame_height= 384,
            frame_width= 384
        )

        self.calango_dying = CustomSpriteAnimation(
            "../assets/enemys/Dying/calango_dying.png",
            (self.x, self.y),
            num_frames=8,
            loop=False,
            frame_duration=0.1,
            total_duration=3.5,
            frame_height= 384,
            frame_width= 384
        )

        self.jacare_dying = CustomSpriteAnimation(
            "../assets/enemys/Dying/jacare_dying.png",
            (self.x, self.y),
            num_frames=9,
            loop=False,
            frame_duration=0.1,
            total_duration=3.5,
            frame_height= 384,
            frame_width= 384
        )

        self.mico_dying = CustomSpriteAnimation(
            "../assets/enemys/Dying/mico_dying.png",
            (self.x, self.y),
            num_frames=12,
            loop=False,
            frame_duration=0.1,
            total_duration=3.5,
            frame_height= 384,
            frame_width= 384
        )

        self.quero_quero_dying = CustomSpriteAnimation(
            "../assets/enemys/Dying/quero_quero_dying.png",
            (self.x, self.y),
            num_frames=8,
            loop=False,
            frame_duration=0.1,
            total_duration=3.5,
            frame_height= 384,
            frame_width= 384
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
        final_crit_chance = min(1.0, self.get_critical_chance() * self.get_lucky())
        is_critical = random.random() < final_crit_chance

        damage = self.get_strength()

        if is_critical:
            damage *= 2

        dodge_chance = min(1.0, self.get_lucky() * target.get_dodge())
        did_dodge = random.random() < dodge_chance

        if not did_dodge:
            target.set_health(max(0, target.get_health() - damage))

        target_alive = target.is_alive()

        return {
            "damage": 0 if did_dodge else damage,
            "is_critical": is_critical,
            "did_dodge": did_dodge,
            "target_alive": target_alive
        }

    def punish(self):
        self.punish_effects.clear()

        if self.name == "Anaconda":
            anvil_start_y = self.y - 400
            anvil_anim = FallingAnvilAnimation(
                "../assets/effects/anvil/anvil_sheet.png",
                (self.x, anvil_start_y),
                (self.x, self.y),
                duration=0.2,
                num_frames=1,
                frame_duration=0.6,
                frame_height= 320,
                frame_width= 320
            )
            self.punish_effects.append(PunishAnimation(anvil_anim))

            stars_anim = CustomSpriteAnimation(
                "../assets/effects/anvil/shining_sheet.png",
                (self.x, self.y),
                frame_duration=0.2,
                num_frames=7,
                loop=True,
                total_duration=2.5,
                frame_height= 320,
                frame_width= 320
            )

            self.punish_effects.append(PunishAnimation(stars_anim, delay = 0.6))
            self.punish_effects.append(PunishAnimation(self.anaconda_hited, delay = 0.7))
            self.dying_animations.append(PunishAnimation(self.anaconda_dying, delay = 0.0))

        elif self.name == "Calango":
            flame = CustomSpriteAnimation(
                "../assets/effects/flame/fire_sheet.png",
                (self.x, self.y),
                frame_duration=0.05,
                num_frames=7,
                loop=True,
                total_duration=3.0,
                frame_height= 320,
                frame_width= 320
            )
            self.punish_effects.append(PunishAnimation(flame))
            self.punish_effects.append(PunishAnimation(self.calango_hited, delay = 0.6))
            self.dying_animations.append(PunishAnimation(self.calango_dying, delay = 0.0))

        elif self.name == "Jacaré":
            firefly = CustomSpriteAnimation(
                "../assets/effects/tornado/big_tornado_sheet.png",
                (self.x, self.y - 70),
                frame_duration=0.05,
                num_frames=20,
                loop=True,
                total_duration=2.5,
                frame_height= 512,
                frame_width= 512
            )
            self.punish_effects.append(PunishAnimation(firefly))
            self.punish_effects.append(PunishAnimation(self.jacare_hited, delay = 0.2))
            self.dying_animations.append(PunishAnimation(self.jacare_dying, delay = 0.5))


        elif self.name == "Quero-Quero":
            tornado = CustomSpriteAnimation(
                "../assets/effects/tornado/tornado_sheet.png",
                (self.x, self.y),
                frame_duration=0.05,
                num_frames=7,
                loop=True,
                total_duration=3.0,
                frame_height= 320,
                frame_width= 320
            )
            self.punish_effects.append(PunishAnimation(tornado))
            self.punish_effects.append(PunishAnimation(self.quero_quero_hited, delay = 0.2))
            self.dying_animations.append(PunishAnimation(self.quero_quero_dying, delay = 0.5))

        elif self.name == "Mico":
            storm = CustomSpriteAnimation(
                "../assets/effects/storm/storm_sheet.png",
                (self.x, self.y - 180),
                num_frames=12,
                loop=True,
                frame_duration=0.1,
                total_duration=2.0,
                frame_height= 320,
                frame_width= 512
            )
            self.punish_effects.append(PunishAnimation(storm))
            self.punish_effects.append(PunishAnimation(self.mico_hited, delay = 0.2))
            self.dying_animations.append(PunishAnimation(self.mico_dying, delay = 0.5))

    def set_animation(self, name: str, play_once: bool = False):
        self.current_frames = getattr(self, f"{name}_frames")
        self.current_animation = name
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_play_once = play_once
