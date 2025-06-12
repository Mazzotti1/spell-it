import random
from Attributes.attributes import Attributes
import pygame

class Entity:
    def __init__(self, x, y, name: str, attributes: Attributes, width: int = 128, height: int = 128):
        self.name = name
        self.attributes = attributes

        self.direction = 0
        self.attacking = False

        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, width, height)

        self.moving = False
        self.target_x = x
        self.target_y = y
        self.move_speed = 200
        self.move_direction = None

        self.width = width
        self.height = height

        self.idle_frames = []
        self.walk_frames = []
        self.throw_book_frames = []
        self.current_frames = []

        self.frame_index = 0
        self.animation_timer = 0
        self.frame_duration = 0.1

        self.frame_durations = {}
        self.animation_play_once = False


    def set_name(self, name: str):
        self.name = name

    def get_name(self):
        return self.name

    def set_attributes(self, attributes: Attributes):
        self.attributes = attributes

    def get_attributes(self):
        return self.attributes

    def attack(self, target: "Entity"):

        hit_chance = min(1.0, max(0.0, self.get_attack_speed()))
        did_hit = random.random() < hit_chance

        if not did_hit:
            return 0, False, target.is_alive(), False

        final_crit_chance = min(1.0, self.get_critical_chance() * self.get_lucky())
        is_critical = random.random() < final_crit_chance

        damage = self.get_strength()

        if is_critical:
            damage *= 2

        target.set_health(max(0, target.get_health() - damage))
        target_alive = target.is_alive()

        return damage, is_critical, target_alive, True

    def is_alive(self):
        return self.attributes.get_health() > 0

    def draw(self, screen):
        if hasattr(self, "visible") and not self.visible:
            return

        frame = self.current_frame
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        frame = pygame.transform.scale(frame, (self.rect.width, self.rect.height))
        screen.blit(frame, self.rect.topleft)

    def load_animations(self, animations: dict[str, tuple[str, float]]):
        for key, (path, duration) in animations.items():
            frames = Entity.load_spritesheet(path, self.width, self.height)
            setattr(self, f"{key}_frames", frames)
            self.frame_durations[key] = duration
            if not self.current_frames:
                self.current_frames = frames
                self.current_animation = key
                self.frame_duration = duration

    @staticmethod
    def load_spritesheet(path, frame_width, frame_height):
        image = pygame.image.load(path).convert_alpha()
        sprites = []
        for i in range(image.get_width() // frame_width):
            frame = image.subsurface((i * frame_width, 0, frame_width, frame_height))
            sprites.append(frame)
        return sprites

    def update_animation(self, dt):
        if not self.current_frames or len(self.current_frames) == 0:
            return False

        current_anim = getattr(self, "current_animation", None)
        frame_duration = self.frame_durations.get(current_anim, self.frame_duration)

        self.animation_timer += dt
        animation_finished = False

        if self.animation_timer >= frame_duration:
            if self.animation_play_once:
                if self.frame_index < len(self.current_frames) - 1:
                    self.frame_index += 1
                else:
                    animation_finished = True
            else:
                self.frame_index = (self.frame_index + 1) % len(self.current_frames)

            self.animation_timer = 0

        if 0 <= self.frame_index < len(self.current_frames):
            self.current_frame = self.current_frames[self.frame_index]

        if animation_finished and self.animation_play_once:
            self.current_frames = self.idle_frames
            self.current_animation = "idle"
            self.frame_index = 0
            self.animation_timer = 0
            self.animation_play_once = False

            self.y += 250
            self.rect.topleft = (self.x, self.y)

        return animation_finished


    def set_health(self, health: int):
        self.attributes.set_health(health)

    def get_health(self) -> int:
        return self.attributes.get_health()

    def set_strength(self, strength: float):
        self.attributes.set_strength(strength)

    def get_strength(self) -> float:
        return self.attributes.get_strength()

    def set_attack_speed(self, attack_speed: float):
        self.attributes.set_attack_speed(attack_speed)

    def get_attack_speed(self) -> float:
        return self.attributes.get_attack_speed()

    def set_dodge(self, dodge: float):
        self.attributes.set_dodge(dodge)

    def get_dodge(self) -> float:
        return self.attributes.get_dodge()

    def set_lucky(self, lucky: float):
        self.attributes.set_lucky(lucky)

    def get_lucky(self) -> float:
        return self.attributes.get_lucky()

    def set_critical_chance(self, critical_chance: float):
        self.attributes.set_critical_chance(critical_chance)

    def get_critical_chance(self) -> float:
        return self.attributes.get_critical_chance()
