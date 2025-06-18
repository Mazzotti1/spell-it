import random
import pygame

from Effects.custom_sprite_animation import CustomSpriteAnimation
from Skills.skill import Skill

class SkillCardAnimation:
    def __init__(self, start_pos, target_pos=None, player=None, manager=None):
        self.pos = list(start_pos)
        self.target_pos = list(target_pos) if target_pos is not None else list(start_pos)
        self.player = player
        self.manager = manager

        self.skill_names = [
            "colapso_ortografico",
            "corrente_combos",
            "disruptor_semantico",
            "ditador_palavras",
            "eco_palavras",
            "explosao_verbo",
            "mimetismo",
            "palavra_proibida",
            "ritual_palavras",
            "roubo_vocabulario"
        ]

        self.front_images = {
            name: pygame.image.load(f"../assets/skill/skills/{name}.png").convert_alpha()
            for name in self.skill_names
        }

        self.skill_name, self.front_image = self.get_unique_skill()

        self.dice_animation = CustomSpriteAnimation(
                "../assets/objects/dice_sheet.png",
                (self.target_pos[0] - 70, self.target_pos[1] - 300),
                num_frames=28,
                loop=True,
                frame_duration=0.01,
                total_duration=1.5,
                frame_height= 128,
                frame_width= 128
        )

        self.back_image = pygame.image.load("../assets/skill/skills/skill_back.png").convert_alpha()
        self.current_image = self.back_image

        self.rect = self.back_image.get_rect(center=self.pos)

        self.state = "back"
        self.hovered = False
        self.clicked = False

        self.scale = 1.0
        self.hover_scale = 1.1
        self.dice_playing = False

        self.reveal_time = None
        self.end_battle_called = False

    def update(self, mouse_pos, dt):
        target_scale = self.hover_scale if self.rect.collidepoint(mouse_pos) else 1.0
        self.scale += (target_scale - self.scale) * 0.1

        self.pos[0] += (self.target_pos[0] - self.pos[0]) * 0.1
        self.pos[1] += (self.target_pos[1] - self.pos[1]) * 0.1

        self.rect.center = self.pos
        self.hovered = self.rect.collidepoint(mouse_pos)

        if self.dice_playing:
            self.dice_animation.update(dt)
            if self.dice_animation.is_finished():
                self.dice_playing = False
                self.state = "front"
                self.current_image = self.front_image

                if not any(skill.get_name() == self.skill_name for skill in self.player.skills):
                    new_skill = Skill(self.skill_name, self.front_images[self.skill_name])
                    self.player.add_skill(new_skill)

                self.reveal_time = pygame.time.get_ticks()

        if self.reveal_time and not self.end_battle_called:
            current_time = pygame.time.get_ticks()
            if current_time - self.reveal_time >= 2500:
                self.manager.end_battle()
                self.end_battle_called = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if event.button == 1 and self.state == "back" and not self.dice_playing:
                self.dice_playing = True
                self.dice_animation.total_elapsed = 0
                self.dice_animation.current_frame_index = 0
                self.dice_animation.finished = False

    def draw(self, surface):
        image = self.current_image
        width = int(image.get_width() * self.scale)
        height = int(image.get_height() * self.scale)
        scaled_image = pygame.transform.scale(image, (width, height))
        self.rect = scaled_image.get_rect(center=self.pos)
        surface.blit(scaled_image, self.rect)

        if self.dice_playing:
            self.dice_animation.draw(surface)

    def get_unique_skill(self):
        owned_names = {skill.get_name() for skill in self.player.skills}
        available = [name for name in self.skill_names if name not in owned_names]

        if not available:
            name = self.skill_names[0]
        else:
            name = random.choice(available)

        return name, self.front_images[name]
