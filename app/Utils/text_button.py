import pygame
from Utils.utils import Utils
from Scenario.audio_manager import AudioManager

class TextButton:
    def __init__(self, text, position, size, on_click=None, font=None, font_size=24, text_color=(255,255,255), bg_color=(100,100,100), hover_color=(150,150,150), radius=10, multiLineWidth=50
                 ):
        self.text = text
        self.position = position
        self.size = size
        self.on_click = on_click
        self.rect = pygame.Rect(position, size)
        self.font = pygame.font.Font(font, font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.radius = radius
        self.hovered = False
        self.multiLineWidth = multiLineWidth

        display_info = pygame.display.Info()
        real_width = display_info.current_w
        real_height = display_info.current_h

        self.scale_x = real_width / 1920
        self.scale_y = real_height / 1080
        self.font_text = Utils.scaled_font(
            path=None,
            base_size=24,
            scale_y=self.scale_y
        )
        
        self.audio_manager = AudioManager.instance()
        self.utils = Utils()

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=self.radius)

        text_surfaces = self.utils.render_multiline_text(self.text, self.font_text, self.text_color, self.multiLineWidth)
        total_height = sum(surface.get_height() for surface in text_surfaces) + (len(text_surfaces) - 1) * 5 
        y_offset = self.rect.centery - total_height // 2 

        for surface in text_surfaces:
            text_rect = surface.get_rect(center=(self.rect.centerx, y_offset + surface.get_height() // 2))
            screen.blit(surface, text_rect)
            y_offset += surface.get_height() + 5

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                    if not self.audio_manager.audio_muted:
                        self.audio_manager.play_sound_effect("../assets/soundfx/button_click.ogg", self.audio_manager.master_volume)

