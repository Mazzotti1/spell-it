import pygame
from Utils.menu_button import MenuButton
from Utils.confirm_dialog import ConfirmDialog
from Utils.text_button import TextButton
import textwrap

class HowToPlayDialog:
    def __init__(self, color, position, size, text, text_size=36, font=None, radius=15):
        self.color = color
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.text = text
        self.text_color = 'white'
        self.font = font
        self.radius = radius
        self.position = position
        self.size = size
        self.visible = False
        self.scroll_offset = 0
        self.scroll_speed = 20

        self.bg_color=(50, 50, 50)
        self.border_color=(200, 200, 200)
        self.text_color=(255, 255, 255)
        self.button_size=(100, 50)
        self.button_spacing=20

        close_pos = (
            position[0] + 3 * size[0] // 4 - self.button_size[0] // 2,
            position[1] + size[1] - self.button_size[1] - self.button_spacing
        )

        self.images = {
            "pre_combat": pygame.image.load("../assets/menu/pre_combat_timer.png"),
            "player_turn": pygame.image.load("../assets/menu/player_turn_timer.png"),
            "skills": pygame.image.load("../assets/menu/skills.png"),
            "skills_hover": pygame.image.load("../assets/menu/skills_hover.png"),
        }

        self.save_button = TextButton(
            text='Fechar',
            position=close_pos,
            size=self.button_size,
            on_click=self.confirm
        )

        self.content_blocks = self.create_content_blocks()


    def confirm(self):
        self.visible = False
        self.scroll_offset = 0

    def draw(self, screen):
        if not self.visible:
            return

        pygame.draw.rect(screen, self.border_color, self.rect, border_radius=self.radius)
        inner_rect = self.rect.inflate(-10, -10)
        pygame.draw.rect(screen, self.bg_color, inner_rect, border_radius=self.radius - 2)

        title_surface = self.font.render("Como Jogar", True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.rect.centerx, self.rect.top + 30))
        screen.blit(title_surface, title_rect)

        self.draw_tab_content(screen)

        self.save_button.draw(screen)

    def draw_tab_content(self, screen):
        content_rect = pygame.Rect(
            self.rect.left + 20,
            self.rect.top + 80,
            self.rect.width - 40,
            self.rect.height - 120
        )
        screen.set_clip(content_rect)
        y_offset = content_rect.top - self.scroll_offset
        spacing = 10
        padding = 20

        final_y = y_offset

        for block_type, content in self.content_blocks:
            if block_type == "text":
                wrapped_lines = textwrap.wrap(content, width=70)
                for line in wrapped_lines:
                    line_surface = self.font.render(line, True, self.text_color)
                    line_rect = line_surface.get_rect(topleft=(content_rect.left + padding, final_y))
                    screen.blit(line_surface, line_rect)
                    final_y += line_surface.get_height() + spacing
                final_y += spacing

            elif block_type == "image":
                image = self.images[content]
                image_rect = image.get_rect()
                image_rect.topleft = (content_rect.left + padding, final_y)
                screen.blit(image, image_rect)
                final_y += image_rect.height + spacing

        self.content_height = final_y - (content_rect.top - self.scroll_offset)
        screen.set_clip(None)


    def handle_event(self, event):
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.save_button.rect.collidepoint(event.pos):
                self.save_button.handle_event(event)

            if event.button == 4:
                self.scroll_offset = max(self.scroll_offset - self.scroll_speed, 0)
            elif event.button == 5:
                content_rect_height = self.rect.height - 120  
                max_scroll = max(0, self.content_height - content_rect_height)
                self.scroll_offset = min(self.scroll_offset + self.scroll_speed, max_scroll)



    def create_content_blocks(self):
        raw_blocks = [
            ("text", "Os combates são constituídos por um Pré-combate, Turno do Jogador e Turno do Adversário."),

            ("text", "Pré-combate:\n"
            "Sempre inicia com um tempo limitado para o jogador procurar e acertar 5 palavras. "
            "Assim que acertar todas, ele tem direito de punir o adversário. Caso não consiga atingir as 5 palavras a tempo, "
            "o turno iniciará com o inimigo. MAS CUIDADO! Ao errar uma palavra, mesmo que por uma letra, você perde 3 segundos no timer!\n\n"),
           
            ("image", "pre_combat"),

            ("text", "Turno do Jogador:\n"
            "O turno tem um temporizador e uma barra de acertos. Muitas palavras aparecem e o jogador deve acertar o máximo possível. "
            "A barra indica o multiplicador de dano com base nas cores: verde, amarela ou vermelha. Cada erro reduz 1 segundo do tempo.\n\n"),
            
            ("image", "player_turn"),

            ("text", "Habilidades do Jogador:\n"
            "Ao vencer inimigos, o jogador recebe habilidades ativas e únicas. Uma vez usadas, elas não retornam. São poderosas, "
            "ativadas com o mouse no canto superior esquerdo, ao deixar o mouse em cima e apresentado a descrição dela para poder ler!"
            "Elas também resetam o tempo do turno. Entenda os efeitos e combine "
            "habilidades para formar combos fortes!\n\n"),

            ("image", "skills"),
            ("image", "skills_hover"),

            ("text", "Turno do Inimigo:\n"
            "Os inimigos atacam e deixam palavras na tela. Decore essas palavras: algumas habilidades dependem delas. "
            "E torça para o inimigo errar o ataque!"),
        ]
        return raw_blocks

            

            
            