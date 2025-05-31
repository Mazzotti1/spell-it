import pygame
from Utils.text_button import TextButton
from Utils.utils import Utils

class ConfirmDialog:
    def __init__(
        self,
        title,
        message,
        on_confirm=None,
        on_cancel=None,
        confirm_text="Sim",
        cancel_text="Não",
        font=None,
        font_size=28,
        position=(780, 300),
        size=(400, 220),
        radius=15,
        bg_color=(50, 50, 50),
        border_color=(200, 200, 200),
        text_color=(255, 255, 255),
        button_size=(100, 50),
        button_spacing=20,
        multiLineWidth = 50,
        multi_line_width_cancel_button = 50
    ):
        self.title = title
        self.message = message
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.rect = pygame.Rect(position, size)
        self.radius = radius
        self.font = pygame.font.Font(font, font_size)
        self.visible = False
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        self.utils = Utils()
        self.font_message = pygame.font.SysFont('Arial', 16)
        self.multiLineWidth = multiLineWidth
        self.multi_line_width_cancel_button = multi_line_width_cancel_button  

        confirm_pos = (
            position[0] + size[0] // 4 - button_size[0] // 2,
            position[1] + size[1] - button_size[1] - button_spacing
        )
        cancel_pos = (
            position[0] + 3 * size[0] // 4 - button_size[0] // 2,
            position[1] + size[1] - button_size[1] - button_spacing
        )

        self.confirm_button = TextButton(
            text=confirm_text,
            position=confirm_pos,
            size=button_size,
            on_click=self.confirm
        )
        self.cancel_button = TextButton(
            text=cancel_text,
            position=cancel_pos,
            size=button_size,
            on_click=self.cancel,
            multiLineWidth=self.multi_line_width_cancel_button
        )

    def confirm(self):
        self.visible = False
        if self.on_confirm:
            self.on_confirm()

    def cancel(self):
        self.visible = False
        if self.on_cancel:
            self.on_cancel()

    def draw(self, screen):
        if not self.visible:
            return

        pygame.draw.rect(screen, self.border_color, self.rect, border_radius=self.radius)
        inner_rect = self.rect.inflate(-10, -10)
        pygame.draw.rect(screen, self.bg_color, inner_rect, border_radius=self.radius - 2)

        y_inner_offset = inner_rect.top + 20

        title_surfaces = self.utils.render_multiline_text(self.title, self.font, self.text_color, 20)
        
        for surface in title_surfaces:
            title_rect = surface.get_rect(center=(self.rect.centerx, y_inner_offset + surface.get_height() // 2))
            screen.blit(surface, title_rect)
            y_inner_offset += surface.get_height() + 5 

        y_message_offset = y_inner_offset + 20  

        message_surfaces = self.utils.render_multiline_text(self.message, self.font_message, self.text_color, self.multiLineWidth)

        for surface in message_surfaces:
            message_rect = surface.get_rect(center=(self.rect.centerx, y_message_offset + surface.get_height() // 2))
            screen.blit(surface, message_rect)
            y_message_offset += surface.get_height() + 5 
            
        self.confirm_button.draw(screen)
        self.cancel_button.draw(screen)


    def handle_event(self, event):
        if not self.visible:
            return
        self.confirm_button.handle_event(event)
        self.cancel_button.handle_event(event)
