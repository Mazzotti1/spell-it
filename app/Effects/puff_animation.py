import time
import pygame

class PuffAnimation:
    def __init__(self, position, duration=0.5):
        self.x, self.y = position
        self.duration = duration
        self.start_time = time.time()

        self.total_frames = 4
        self.sprite_sheet = pygame.image.load("../assets/effects/Puff.png").convert_alpha()
        self.frame_width = self.sprite_sheet.get_width() // self.total_frames
        self.frame_height = self.sprite_sheet.get_height()

    def is_finished(self):
        return (time.time() - self.start_time) >= self.duration

    def draw(self, screen):
        elapsed = time.time() - self.start_time
        t = min(elapsed / self.duration, 1.0)

        current_frame = int(t * self.total_frames)
        current_frame = min(current_frame, self.total_frames - 1)

        frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        frame_surface.blit(
            self.sprite_sheet,
            (0, 0),
            (current_frame * self.frame_width, 0, self.frame_width, self.frame_height)
        )

        screen.blit(frame_surface, (self.x, self.y))
