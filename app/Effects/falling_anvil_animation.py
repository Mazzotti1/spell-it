
from Effects.custom_sprite_animation import CustomSpriteAnimation


class FallingAnvilAnimation(CustomSpriteAnimation):
    def __init__(self, sprite_sheet_path, start_pos, end_pos, duration, **kwargs):
        super().__init__(sprite_sheet_path, start_pos, **kwargs)
        self.start_y = start_pos[1]
        self.end_y = end_pos[1]
        self.fall_duration = duration
        self.fall_elapsed = 0

    def update(self, dt):
        super().update(dt)

        if self.fall_elapsed < self.fall_duration:
            self.fall_elapsed += dt 
            progress = min(1.0, self.fall_elapsed / self.fall_duration)
            self.position[1] = self.start_y + (self.end_y - self.start_y) * progress
