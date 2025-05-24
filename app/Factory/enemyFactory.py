import pygame
from Attributes.attributes import Attributes
from Entity.Enemy.enemy import Enemy

class EnemyFactory:
    @staticmethod
    def create_enemy(type, attributes, x, y, idle_sprite):
        enemy = Enemy(type, attributes, x, y, idle_sprite)
        enemy.rect = pygame.Rect(x, y, enemy.width, enemy.height)

        enemy.current_frames = enemy.idle_frames
        enemy.frame_index = 0
        enemy.animation_timer = 0
        enemy.current_frame = enemy.current_frames[0] if enemy.current_frames else None

        return enemy