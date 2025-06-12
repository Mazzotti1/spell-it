import pygame
from Attributes.attributes import Attributes
from Entity.Player.player import Player

class PlayerFactory:
    @staticmethod
    def create_player(x, y, attributes = None):

        if attributes is None:
            attributes = Attributes(
                dodge=1,
                attack_speed=1.0,
                strength=10,
                health=50,
                lucky=1,
                critical_chance=1
            )

        player = Player("Aurélio", attributes, x, y)
        player.rect = pygame.Rect(x, y, player.width, player.width)

        player.current_frames = player.idle_frames
        player.frame_index = 0
        player.animation_timer = 0
        player.current_frame = player.current_frames[0] if player.current_frames else None

        return player