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


    def set_name(self, name: str):
        self.name = name

    def get_name(self):
        return self.name

    def set_attributes(self, attributes: Attributes):
        self.attributes = attributes

    def get_attributes(self):
        return self.attributes

    def attack(self, target: "Entity"):
        damage = self.attributes.get_strength()
        target.take_damage(damage)

    def take_damage(self, damage_value: int):
        new_health = self.attributes.get_health() - damage_value
        self.attributes.set_health(max(new_health, 0))

    def is_alive(self):
        return self.attributes.get_health() > 0

    def draw(self, screen):
        frame = self.current_frame
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        frame = pygame.transform.scale(frame, (self.rect.width, self.rect.height))
        screen.blit(frame, self.rect.topleft)

    def load_animations(self, animations: dict[str, str]):
        for key, path in animations.items():
            frames = Entity.load_spritesheet(path, self.width, self.height)
            setattr(self, f"{key}_frames", frames)
            if not self.current_frames:  
                self.current_frames = frames

    @staticmethod
    def load_spritesheet(path, frame_width, frame_height):
        image = pygame.image.load(path).convert_alpha()
        sprites = []
        for i in range(image.get_width() // frame_width):
            frame = image.subsurface((i * frame_width, 0, frame_width, frame_height))
            sprites.append(frame)
        return sprites
    
    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.frame_duration and self.current_frames:
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)
            self.animation_timer = 0

        if self.current_frames:
            self.current_frame = self.current_frames[self.frame_index]