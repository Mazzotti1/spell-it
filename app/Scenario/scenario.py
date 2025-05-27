import pygame

class Scenario:
    def __init__(self):
        self.name = None
        self.objects = []
        self.music = None
        self.sound_effects = []

        self.enable_background = True
        self.enable_ground = True
        self.enable_solids = True
        self.enable_ui = True

        self.solids = []
        self.background_image = None

        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) * 1000

        self.is_start_map_animating = False
        self.map_animation_sheet = pygame.image.load('../assets/scene/map/animation/open_map_animation.png').convert_alpha()

        self.frame_width = 744    
        self.frame_height = 636  
        self.frame_cols = 5
        self.frame_rows = 4
        self.num_frames = 19
        self.current_frame = 0
        self.animation_speed = 0.1
        self.time_accumulator = 0

        self.zoom_scale = 1.0
        self.target_zoom = 1.6
        self.zoom_speed = 0.015

    def update(self):

        if self.is_start_map_animating:
            self.time_accumulator += self.dt

            if self.time_accumulator >= self.animation_speed:
                self.time_accumulator = 0
                if self.current_frame < self.num_frames - 1:
                    self.current_frame += 1
                   

        if self.current_frame == self.num_frames - 1:
            if self.zoom_scale < self.target_zoom:
                self.zoom_scale += self.zoom_speed
                if self.zoom_scale > self.target_zoom:
                    self.zoom_scale = self.target_zoom
                    self.is_start_map_animating = False



    def draw_scene(self, screen):
        if self.enable_background:
            self.draw_background(screen)

        if self.enable_ground:
            self.draw_ground(screen)

        if self.enable_solids:
            self.draw_solids(screen)

        if self.enable_ui:
            self.draw_ui(screen)

    def draw_background(self, screen):
        screen.fill((0, 0, 0))

        if self.is_start_map_animating or self.current_frame == self.num_frames - 1:
            col = self.current_frame % self.frame_cols
            row = self.current_frame // self.frame_cols

            frame_rect = pygame.Rect(
                col * self.frame_width,
                row * self.frame_height,
                self.frame_width,
                self.frame_height
            )

            frame_image = self.map_animation_sheet.subsurface(frame_rect)

            # Zoom suave
            scale_factor = self.zoom_scale if self.current_frame == self.num_frames - 1 else 1.0
            scaled_width = int(self.frame_width * scale_factor)
            scaled_height = int(self.frame_height * scale_factor)

            frame_image = pygame.transform.scale(
                frame_image,
                (scaled_width, scaled_height)
            )

            # Subida conforme zoom: sobe até 50 pixels
            max_lift = 50
            lift = int((scale_factor - 1.0) / (self.target_zoom - 1.0) * max_lift) if scale_factor > 1.0 else 0

            x = (screen.get_width() - scaled_width) // 2
            y = (screen.get_height() - scaled_height) // 2 - lift

            screen.blit(frame_image, (x, y))

        if self.background_image and not self.is_start_map_animating:
            screen_width, screen_height = screen.get_size()
            bg_width, bg_height = self.background_image.get_size()

            x = (screen_width - bg_width) // 2
            y = (screen_height - bg_height) // 2

            screen.blit(self.background_image, (x, y))




    def draw_ground(self, screen):
        ground_height = 150
        width, height = screen.get_size()
        ground_rect = pygame.Rect(0, height - ground_height, width, ground_height)
        pygame.draw.rect(screen, (139, 69, 19), ground_rect)

    def draw_solids(self, screen):
        for solid in self.solids:
            pygame.draw.rect(screen, (100, 100, 100), solid)

    def draw_ui(self, screen):
        pass

    def load_background(self, image_path):
        self.background_image = pygame.image.load(image_path).convert_alpha()