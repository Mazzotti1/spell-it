import pygame
import random
from Entity.entity import Entity
from Skills.skill import Skill
from Skills.skill_factory import create_skill

class Player(Entity):
    def __init__(self, name, attributes, x=0, y=0):
        super().__init__(x, y, name, attributes)

        #pra carregar os outros sprites lembrar de botar em 128x128
        self.load_animations({
            "idle": ("../assets/player/idle_sprite.png", 0.1),
            "idle_back": ("../assets/player/player_idle_back.png", 0.15),
            # "walking_left": ("../assets/player/player_walking_left.png", 0.1),
            "walking_right": ("../assets/player/player_walking_right.png", 0.05),
            "walking_node_right": ("../assets/player/player_diagonal_right.png", 0.05),
            # "walking_node_left": ("../assets/player/player_diagonal_right.png", 0.12),
            "walking_top": ("../assets/player/player_walking_top.png", 0.05),
            # "walking_bottom": ("../assets/player/player_walking_bottom.png", 0.1),
            "skill": ("../assets/skill/player_skill_sheet.png", 0.05),
            "hited": ("../assets/player/player_hited_sheet.png", 0.1),
            "dying": ("../assets/player/Dying/player_dying.png", 0.1),
        })

        self.visible = True
        
        self.skills = []
        self.all_acquired_skills = []

        self.force_critical_hit = False
        self.double_damage = False

        self.is_mime_hit = False
        self.mime_damage = None
        self.recieve_lucky = 0

        self.buff_atack_speed = 0
        self.buff_atack_damage = 0

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
        bonus_int = max(1, int(bonus))

        setter(current_value + bonus_int)

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

    def get_position(self):
        return (self.x, self.y)

    def play_skill_animation(self):
        self.current_frames = self.skill_frames
        self.current_animation = "skill"
        self.frame_index = 0
        self.animation_timer = 0
        self.moving = False
        self.animation_play_once = True

        self.y -= 250
        self.rect.topleft = (self.x, self.y)

    def set_animation(self, name: str, play_once: bool = False):
        self.current_frames = getattr(self, f"{name}_frames")
        self.current_animation = name
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_play_once = play_once

    def add_skill(self, skill: Skill):
        self.skills.append(create_skill(skill._name, skill.get_image()))
        self.all_acquired_skills.append(create_skill(skill._name, skill.get_image()))

    def remove_skill(self, skill_name: str):
        self.skills = [skill for skill in self.skills if skill.get_name() != skill_name]


    def use_skill(self, skill_name: str):
        pass

    def attack(self, target: "Entity", hit_bonus = 1):

        if self.recieve_lucky > 0:
            lucky = self.get_lucky() * 4
            self.recieve_lucky -= 1
        else:
            lucky = self.get_lucky()

        if self.buff_atack_damage > 0:
            print("bonus")
            random_bonus = random.randint(1, 3) * lucky
            strength = self.get_strength() + random_bonus
            self.buff_atack_damage -= 1
        else:
            strength = self.get_strength()

        if self.buff_atack_speed > 0:
            print("bonus")
            random_bonus = random.randint(1, 3) * lucky
            atack_speed = self.get_attack_speed() + random_bonus
            self.buff_atack_speed -= 1
        else:
            atack_speed = self.get_attack_speed()

        hit_chance = min(1.0, max(0.0, atack_speed))
        did_hit = random.random() < hit_chance

        if not did_hit:
            return 0, False, target.is_alive(), False

        final_crit_chance = min(1.0, self.get_critical_chance() * lucky)

        if self.force_critical_hit:
            is_critical = True
            self.force_critical_hit = False 
        else:
            is_critical = random.random() < final_crit_chance

        if self.double_damage:
            double_strength = strength * 2
            damage = double_strength * hit_bonus
            self.double_damage = False
        elif self.is_mime_hit:
            print("mimetismo")
            damage = self.mime_damage * hit_bonus
            self.is_mime_hit = False
            self.mime_damage = None
        else:
            damage = strength * hit_bonus

        if is_critical:
            damage *= 2

        target.set_health(max(0, target.get_health() - damage))
        target_alive = target.is_alive()

        return damage, is_critical, target_alive, True
    
    def recieveBossReward(self):
        bonus_health = random.randint(5, 10)
        bonus_strength = round(random.uniform(0.2, 0.5), 2)
        bonus_attack_speed = round(random.uniform(0.05, 0.1), 2)
        bonus_dodge = round(random.uniform(0.01, 0.03), 2)
        bonus_critical = round(random.uniform(0.01, 0.03), 2)
        bonus_lucky = round(random.uniform(0.01, 0.03), 2)

        self.set_health(self.get_health() + bonus_health)
        self.attributes.strength += bonus_strength
        self.attributes.attack_speed += bonus_attack_speed
        self.attributes.dodge = min(self.attributes.dodge + bonus_dodge, 0.5)
        self.attributes.critical_chance = min(self.attributes.critical_chance + bonus_critical, 0.5)
        self.attributes.lucky += bonus_lucky