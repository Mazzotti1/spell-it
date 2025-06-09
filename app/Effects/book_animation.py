import time

import pygame


class BookAnimation:
    def __init__(self, start_pos, end_pos, duration=1):
        self.start_x, self.start_y = start_pos
        self.end_x, self.end_y = end_pos
        self.duration = duration
        self.start_time = time.time()

        self.total_frames = 10
        self.sprite_sheet = pygame.image.load("../assets/objects/Book_scaled.png").convert_alpha()
        self.frame_width = self.sprite_sheet.get_width() // self.total_frames
        self.frame_height = 256

    def is_finished(self):
        return (time.time() - self.start_time) >= self.duration

    def draw(self, screen):
            elapsed = time.time() - self.start_time
            t = min(elapsed / self.duration, 1.0)

            x = self.start_x + (self.end_x - self.start_x) * t
            y = self.start_y + (self.end_y - self.start_y) * t

            current_frame = int(t * self.total_frames)
            current_frame = min(current_frame, self.total_frames - 1)

            frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame_surface.blit(
                self.sprite_sheet,
                (0, 0),
                (current_frame * self.frame_width, 0, self.frame_width, self.frame_height)
            )

            screen.blit(frame_surface, (x, y))