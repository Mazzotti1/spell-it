import pygame
from Utils.menu_button import MenuButton
from Utils.confirm_dialog import ConfirmDialog
from Utils.text_button import TextButton
from Utils.utils import Utils
from Scenario.audio_manager import AudioManager
class SettingsDialog:
    def __init__(self, color, position, size, text, text_size=36, font=None, radius=15, manager=None):
        self.color = color
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.text = text
        self.text_color = 'white'
        self.font = font
        self.radius = radius
        self.position = position
        self.size = size
        self.visible = False

        self.bg_color=(50, 50, 50)
        self.border_color=(200, 200, 200)
        self.text_color=(255, 255, 255)
        self.button_size=(100, 50)
        self.button_spacing=20

        self.current_tab = 'audio'
        self.is_dirty = False
        self.manager = manager
        
        self.topbar_setting_buttons = [
            self.create_topbar_button('Áudio',  (780, 150), (120, 50), on_click= self.change_to_audio_settings),
            self.create_topbar_button('Controles',  (1000, 150), (120, 50), on_click=self.change_to_controls_settings),
        ]

        self.unsaved_changes_dialog = ConfirmDialog(
            title="Alterações não foram salvas, deseja salvar?",
            message='',
            on_confirm=self.confirm_settings,
            on_cancel=self.cancel_settings,
            confirm_text="Salvar",
            cancel_text="Fechar sem salvar",
            position= (750, 390),
            multi_line_width_cancel_button=10
        )

        self.save_confirm_dialog = ConfirmDialog(
            title="Tem certeza que deseja salvar as configurações?",
            message='',
            on_confirm=self.confirm_settings,
            on_cancel= self.hide_save_confirm_dialog,
            confirm_text="Salvar",
            cancel_text="Cancelar",
            position= (750, 390)
        )

        self.CONTROL_COMMANDS = {
            'Menu em jogo': 'ESC',
            'Enviar palavras': 'ENTER',
            'Ativar habilidade': 'MOUSE 1',
            'Ler Habilidade': 'HOVER na habilidade',
        }

        save_pos = (
            position[0] + size[0] // 4 - self.button_size[0] // 2,
            position[1] + size[1] - self.button_size[1] - self.button_spacing
        )
        cancel_pos = (
            position[0] + 3 * size[0] // 4 - self.button_size[0] // 2,
            position[1] + size[1] - self.button_size[1] - self.button_spacing
        )

        self.save_button = TextButton(
            text='Salvar',
            position=save_pos,
            size=self.button_size,
            on_click=self.confirm,
        )
        self.cancel_button = TextButton(
            text='Fechar',
            position=cancel_pos,
            size=self.button_size,
            on_click=self.cancel,
        )

        self.audio_manager = AudioManager.instance()

        self.volume = self.audio_manager.master_volume if self.audio_manager else 0.5
        self.is_muted = self.audio_manager.audio_muted if self.audio_manager else False

        self.checkbox_rect = pygame.Rect(position[0] + 100, position[1] + 190, 20, 20)
        self.checkbox_label = "Mutar som"

        self.volume_slider_rect = pygame.Rect(position[0] + 100, position[1] + 280, 300, 20)

    def confirm(self):
        if self.is_dirty:
            self.save_confirm_dialog.visible = True
        else:
            self.visible = False

    def cancel(self):
        if self.is_dirty:
            self.unsaved_changes_dialog.visible = True
        else:
            self.visible = False
            if hasattr(self, 'on_cancel') and self.on_cancel:
                self.on_cancel()


    def draw(self, screen):
        if not self.visible:
            return

        pygame.draw.rect(screen, self.border_color, self.rect, border_radius=self.radius)
        inner_rect = self.rect.inflate(-10, -10)
        
        pygame.draw.rect(screen, self.bg_color, inner_rect, border_radius=self.radius - 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        title_y = self.rect.top - text_surface.get_height() - 10  
        text_rect = text_surface.get_rect(center=(self.rect.centerx, title_y))
        screen.blit(text_surface, text_rect)

        line_padding = 10  
        line_length = 50   

        start_left = (text_rect.left - line_padding - line_length, text_rect.centery)
        end_left = (text_rect.left - line_padding, text_rect.centery)

        start_right = (text_rect.right + line_padding, text_rect.centery)
        end_right = (text_rect.right + line_padding + line_length, text_rect.centery)

        for btn in self.topbar_setting_buttons:
            btn.draw(screen)

        self.draw_tab_content(screen)

        self.save_button.draw(screen)
        self.cancel_button.draw(screen)

        if self.unsaved_changes_dialog.visible:
            self.unsaved_changes_dialog.draw(screen)
        if self.save_confirm_dialog.visible:
            self.save_confirm_dialog.draw(screen)
        
        pygame.draw.line(screen, self.text_color, start_left, end_left, 2)
        pygame.draw.line(screen, self.text_color, start_right, end_right, 2)

    def create_topbar_button(self, text, position, size, on_click):
        return  TextButton(
            text=text,
            position=position,
            size=size,
            on_click=on_click,
        )
    
    def handle_topbar_buttons_event(self, event):
        for btn in self.topbar_setting_buttons:
            btn.handle_event(event)

    def change_to_audio_settings(self):
        if self.current_tab != 'audio':
            self.current_tab = 'audio'
        #   self.is_dirty = True  quando precisar mostrar dialgo q alguma config mudou mas n foi salvo

    def change_to_controls_settings(self):
        self.current_tab = 'controls'

    def draw_tab_content(self, screen):
        content_rect = pygame.Rect(
            self.rect.left + 20,
            self.rect.top + 100,
            self.rect.width - 40,
            self.rect.height - 200
        )

        pygame.draw.rect(screen, (70, 70, 70), content_rect, border_radius=10)

        if self.current_tab == 'audio':
            content_text = "Configurações de Áudio"
        elif self.current_tab == 'controls':
            content_text = "Configurações de Controles"
        else:
            content_text = ""

        if content_text:
            content_surface = self.font.render(content_text, True, self.text_color)
            content_text_rect = content_surface.get_rect(center=(content_rect.centerx, content_rect.top + 30))
            screen.blit(content_surface, content_text_rect)

            line_y = content_text_rect.bottom + 5 
            pygame.draw.line(
                screen,
                self.text_color, 
                (content_rect.left + 40, line_y), 
                (content_rect.right - 40, line_y), 
                1  
            )

        if self.current_tab == 'audio':
            pygame.draw.rect(screen, (255, 255, 255), self.checkbox_rect, 2)
            if self.is_muted:
                pygame.draw.line(screen, (255, 255, 255), self.checkbox_rect.topleft, self.checkbox_rect.bottomright, 2)
                pygame.draw.line(screen, (255, 255, 255), self.checkbox_rect.topright, self.checkbox_rect.bottomleft, 2)

            label_surface = self.font.render(self.checkbox_label, True, self.text_color)
            screen.blit(label_surface, (self.checkbox_rect.right + 10, self.checkbox_rect.top - 4))

            pygame.draw.rect(screen, (180, 180, 180), self.volume_slider_rect)

            filled_width = int(self.volume_slider_rect.width * self.volume)
            filled_rect = pygame.Rect(
                self.volume_slider_rect.x, self.volume_slider_rect.y,
                filled_width, self.volume_slider_rect.height
            )
            pygame.draw.rect(screen, (100, 200, 100), filled_rect)

            volume_text = f"Volume: {int(self.volume * 100)}%"
            surface = self.font.render(volume_text, True, self.text_color)
            screen.blit(surface, (self.volume_slider_rect.x, self.volume_slider_rect.y - 30))

        if self.current_tab == 'controls':
            start_y = content_text_rect.bottom + 40 
            spacing = 10 
            for action, key in self.CONTROL_COMMANDS.items():
                line = f"{action}: {key}"
                line_surface = self.font.render(line, True, self.text_color)
                line_rect = line_surface.get_rect(center=(content_rect.centerx, start_y))
                screen.blit(line_surface, line_rect)
                start_y += line_surface.get_height() + spacing

    def confirm_settings(self):
        if self.is_muted:
            if not self.audio_manager.audio_muted:
                self.audio_manager.audio_muted = True
                pygame.mixer.music.pause()
        else:
            if self.audio_manager.audio_muted:
                self.audio_manager.audio_muted = False
                pygame.mixer.music.unpause()
            self.audio_manager.set_volume(self.volume)
        
        self.is_dirty = False
        self.visible = False

    def cancel_settings(self):
        self.is_dirty = False
        self.visible = False

    def hide_save_confirm_dialog(self):
        self.save_confirm_dialog.visible = False

    def handle_event(self, event):
        if not self.visible:
            return

        if self.current_tab == 'audio':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.checkbox_rect.collidepoint(event.pos):
                    self.is_muted = not self.is_muted
                    self.is_dirty = True
                elif self.volume_slider_rect.collidepoint(event.pos):
                    self.set_volume_from_mouse(event.pos[0])

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] and self.volume_slider_rect.collidepoint(event.pos):
                    self.set_volume_from_mouse(event.pos[0])

        if self.unsaved_changes_dialog.visible:
            self.unsaved_changes_dialog.handle_event(event)
            return

        if self.save_confirm_dialog.visible:
            self.save_confirm_dialog.handle_event(event)
            return

        for btn in self.topbar_setting_buttons:
            btn.handle_event(event)

        self.save_button.handle_event(event)
        self.cancel_button.handle_event(event)

    def set_volume_from_mouse(self, mouse_x):
        relative_x = mouse_x - self.volume_slider_rect.x
        self.volume = max(0.0, min(1.0, relative_x / self.volume_slider_rect.width))
        self.is_dirty = True

