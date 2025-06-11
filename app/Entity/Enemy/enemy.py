from Entity.entity import Entity
from Effects.custom_sprite_animation import CustomSpriteAnimation
from Effects.punish_animation import PunishAnimation
from Effects.falling_anvil_animation import FallingAnvilAnimation
class Enemy(Entity):
    def __init__(self, type, attributes, x=0, y=0, idle_sprite="../assets/enemys/anaconda/enemy_anaconda_idle_sprite.png"):
        super().__init__(x, y, type, attributes, width=384, height=384)

        self.load_animations({
            "idle": (idle_sprite, 0.15),
        })

        self.punish_effects = []

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def get_position(self):
        return (self.x, self.y)

    def punish(self):
        self.punish_effects.clear()

        if self.name == "Anaconda":
            anvil_start_y = self.y - 700
            anvil_anim = FallingAnvilAnimation(
                "../assets/effects/anvil/anvil_sheet.png",
                (self.x, anvil_start_y),
                (self.x, self.y),
                duration=0.6,
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

        elif self.name == "Jacaré":
            firefly = CustomSpriteAnimation(
                "../assets/effects/tornado/big_tornado_sheet.png",
                (self.x, self.y - 70),
                frame_duration=0.05,
                num_frames=20,
                loop=True,
                total_duration=3.0,
                frame_height= 512,
                frame_width= 512
            )
            self.punish_effects.append(PunishAnimation(firefly))

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

        elif self.name == "Mico":
            storm = CustomSpriteAnimation(
                "../assets/effects/storm/storm_sheet.png",
                (self.x, self.y - 180),
                num_frames=12,
                loop=True,
                frame_duration=0.1,
                total_duration=3.0,
                frame_height= 320,
                frame_width= 512
            )
            self.punish_effects.append(PunishAnimation(storm))
