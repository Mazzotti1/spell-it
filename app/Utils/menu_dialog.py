import pygame
from Utils.button import Button

class MenuDialog:
    def __init__(self, color, position, size, text, text_size=36, font=None, radius=15):
        self.color = color
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.text = text
        self.text_color = 'white'
        self.font = pygame.font.Font(font, text_size)
        self.radius = radius
        self.position = position
        self.size = size

        # self.buttons = [
        #     self.create_button("Logout", "red", (0, 0), (130, 50), ),
        # ]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.radius)

        surface_text = self.font.render(self.text, True, self.text_color)
        rect_text = surface_text.get_rect()
        
        text_x = self.rect.centerx
        text_y = self.rect.top - rect_text.height - 10 
        
        rect_text.center = (text_x, text_y)
        screen.blit(surface_text, rect_text)

        line_padding = 10  
        line_length = 50   

        start_left = (rect_text.left - line_padding - line_length, rect_text.centery)
        end_left = (rect_text.left - line_padding, rect_text.centery)

        start_right = (rect_text.right + line_padding, rect_text.centery)
        end_right = (rect_text.right + line_padding + line_length, rect_text.centery)

        pygame.draw.line(screen, self.text_color, start_left, end_left, 2)
        pygame.draw.line(screen, self.text_color, start_right, end_right, 2)

    def create_button(self, text, color, position, size, on_click, text_color="white"):
        return Button(
            color=color,
            position=position,
            size=size,
            text=text,
            on_click=on_click,
            text_color=text_color
        )