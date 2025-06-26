import pygame
from Utils.menu_button import MenuButton
from Utils.confirm_dialog import ConfirmDialog

class MenuDialog:
    def __init__(self, manager, color, position, size, text, text_size=36, font=None, radius=15, settings_dialog=None):
        self.color = color
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.text = text
        self.text_color = 'white'
        self.font = font
        self.radius = radius
        self.position = position
        self.size = size
        self.manager = manager

        self.menu_buttons = [
            self.create_menu_button('../assets/objects/logout_icon.png',  (820, 320), (150, 150), on_click= self.logout),
            self.create_menu_button('../assets/objects/option_gear_icon.png',  (990, 320), (150, 150), on_click=self.open_options),
        ]

        self.confirm_dialog = ConfirmDialog(
            title="Deseja voltar para o menu?",
            message="Ao voltar para o menu, você perderá o progresso atual.",
            on_confirm=self.perform_logout,
            on_cancel=self.cancel_logout,
            confirm_text="Sim",
            cancel_text="Não"
        )

        self.settings_dialog = settings_dialog

    def draw(self, screen):
        border_color = (192, 192, 192)
        border_thickness = 4

        pygame.draw.rect(screen, border_color, self.rect, border_radius=self.radius)

        inner_rect = self.rect.inflate(-2*border_thickness, -2*border_thickness)

        pygame.draw.rect(screen, (17, 18, 17), inner_rect, border_radius=self.radius - 2)

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

        for btn in self.menu_buttons:
            btn.draw(screen)
        
        pygame.draw.line(screen, self.text_color, start_left, end_left, 2)
        pygame.draw.line(screen, self.text_color, start_right, end_right, 2)

        self.confirm_dialog.draw(screen)
        self.settings_dialog.draw(screen)

    def create_menu_button(self, icon, position, size, on_click):
        return MenuButton(
            icon=icon,
            position=position,
            size=size,
            on_click=on_click,
        )
    
    def handle_menu_buttons_event(self, event):
        if self.confirm_dialog.visible:
            self.confirm_dialog.handle_event(event)
            return  

        if self.settings_dialog.visible:
            self.settings_dialog.handle_event(event)
            return
    
        for btn in self.menu_buttons:
            btn.handle_event(event)

    def logout(self):
        self.confirm_dialog.visible = True
    
    def perform_logout(self):
        self.confirm_dialog.visible = False
        self.manager.back_to_main()

    def cancel_logout(self):
        self.confirm_dialog.visible = False

    def open_options(self):
        self.settings_dialog.visible = True

    
