import pygame
import random
from Entity.entity import Entity
from Skills.skill import Skill 

class Player(Entity):
    def __init__(self, name, attributes, x=0, y=0):
        super().__init__(x, y, name, attributes)

        #pra carregar os outros sprites lembrar de botar em 128x128
        self.load_animations({
            "idle": "../assets/player/idle_sprite.png",
            # "idle_back": "../assets/player/player_idle_back.png",
            # "walking_left": "../assets/player/player_walking_left.png",
            "walking_right": "../assets/player/player_walking_right.png",
            "walking_node_right": "../assets/player/player_diagonal_right.png",
            # "walking_node_left": "../assets/player/player_diagonal_right.png",
            "walking_top": "../assets/player/player_walking_top.png",
            # "walking_bottom": "../assets/player/player_walking_bottom.png",
        })

        self.skills: list[Skill] = []


    def add_skill(self, skill: Skill):
        self.skills.append(skill)

    def use_skill(self, skill_name: str, target: "Entity"):
        skill = next((s for s in self.skills if s.name == skill_name), None)
        skill.use(self, target)

    def start_moving_to(self, target_x, target_y, direction="walking_right"):
        self.target_x = target_x
        self.target_y = target_y
        self.moving = True
        self.move_direction = direction
        self.current_frames = getattr(self, f"{direction}_frames")
        self.frame_index = 0
        self.animation_timer = 0


    def update_movement(self, dt):
        if not self.moving:
            return

        dx = self.target_x - self.x
        dy = self.target_y - self.y

        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < self.move_speed * dt:
            self.x = self.target_x
            self.y = self.target_y
            self.moving = False
            self.current_frames = self.idle_frames  
            self.frame_index = 0 
        else:
            direction_x = dx / distance
            direction_y = dy / distance

            self.x += direction_x * self.move_speed * dt
            self.y += direction_y * self.move_speed * dt

        self.rect.topleft = (self.x, self.y)

    def calculate_attributes(self, attribute, lucky):
        if lucky <= 0:
            return

        getter = getattr(self.attributes, f"get_{attribute}")
        setter = getattr(self.attributes, f"set_{attribute}")
        current_value = getter()

        if attribute in ['health']:
            setter(current_value + 1)
            return

        bonus = random.uniform(0, lucky * 0.5)
        setter(current_value + bonus) 

    def trade_health_for_attribute(self, attribute):
        if self.get_health() <= 1:
            return
             
        self.set_health(self.get_health() - 1) 
        self.calculate_attributes(attribute, self.get_lucky())

    def trade_lucky_for_attribute(self, attribute):
        if self.get_lucky() <= 0.5:
            return
             
        self.set_lucky(self.get_lucky() - 0.5) 
        self.calculate_attributes(attribute, self.get_lucky())

    def trade_dodge_for_attribute(self, attribute):
        if self.get_dodge() <= 0.5:
            return
             
        self.set_dodge(self.get_dodge() - 0.5) 
        self.calculate_attributes(attribute, self.get_lucky())

    def trade_critical_chance_for_attribute(self, attribute):
        if self.get_critical_chance() <= 0.5:
            return
             
        self.set_critical_chance(self.get_critical_chance() - 0.5) 
        self.calculate_attributes(attribute, self.get_lucky())

    def trade_strength_for_attribute(self, attribute):
        if self.get_strength() <= 0.5:
            return

        self.set_strength(self.get_strength() - 0.5) 
        self.calculate_attributes(attribute, self.get_lucky())
