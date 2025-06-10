import pygame

class CustomSpriteAnimation:
    def __init__(
        self,
        sprite_sheet_path,
        position,
        num_frames=None,
        frame_duration=0.1,
        loop=False,
        total_duration=None
    ):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.position = list(position)
        self.frame_duration = frame_duration
        self.loop = loop
        self.total_duration = total_duration
        self.num_frames = num_frames

        self.frames = []
        self.current_frame_index = 0
        self.elapsed_time = 0
        self.total_elapsed = 0
        self.finished = False

        self._load_frames()

    def _load_frames(self):
        sheet_width, sheet_height = self.sprite_sheet.get_size()

        self.frame_width = sheet_width // self.num_frames
        self.frame_height = sheet_height

        for i in range(self.num_frames):
            x = i * self.frame_width
            frame = self.sprite_sheet.subsurface((x, 0, self.frame_width, self.frame_height))
            self.frames.append(frame)


    def update(self, dt):
        if self.finished:
            return

        self.elapsed_time += dt
        self.total_elapsed += dt

        if self.total_duration and self.total_elapsed >= self.total_duration:
            self.finished = True
            return

        if self.elapsed_time >= self.frame_duration:
            self.elapsed_time = 0
            self.current_frame_index += 1

            if self.current_frame_index >= len(self.frames):
                if self.loop:
                    self.current_frame_index = 0
                else:
                    self.finished = True

    def draw(self, screen):
        if not self.finished and self.current_frame_index < len(self.frames):
            frame = self.frames[self.current_frame_index]
            screen.blit(frame, self.position)

    def is_finished(self):
        return self.finished
