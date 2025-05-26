import pygame
import random
import textwrap
from Scenario.scenario import Scenario
import random
from Factory.playerFactory import PlayerFactory

class Map(Scenario):
    def __init__(self, manager, background, player):
        super().__init__()
        self.manager = manager
        self.player = player
        self.enable_ground = False
        self.enable_solids = False
        self.enable_background = True
        self.enable_ui = True
        self.in_battle = False
        self.is_choosing_perk = False
        self.font_title = pygame.font.Font('../assets/fonts/CrimsonPro-VariableFont_wght.ttf', 24)
        self.font_desc = pygame.font.Font('../assets/fonts/CrimsonPro-VariableFont_wght.ttf', 20)

        self.load_background(background)

        self.enemies = [
            {'image': pygame.image.load('../assets/scene/map/enemy_anaconda_map.png'), 'type': 'anaconda'},
            {'image': pygame.image.load('../assets/scene/map/enemy_calango_map.png'), 'type': 'calango'},
            {'image': pygame.image.load('../assets/scene/map/enemy_jacare_map.png'), 'type': 'jacare'},
            {'image': pygame.image.load('../assets/scene/map/enemy_quero_quero_map.png'), 'type': 'quero_quero'},
            {'image': pygame.image.load('../assets/scene/map/enemy_mico_map.png'), 'type': 'mico'}
        ]

        self.perks = [
            {'title': 'Receber Vida', 'description': 'Recebe um ponto de vida', 'effect': lambda player: player.set_health(player.get_health() + 1), 'icon': '../assets/objects/recieve_attributes.png'},
            {'title': 'Receber Força', 'description': 'Suas palavras ficam mais fortes', 'effect': lambda player: player.set_strength(player.get_strength() + 1), 'icon': '../assets/objects/recieve_attributes.png'},
            {'title': 'Receber Velocidade', 'description': 'Você esquiva com mais frequência de palavras', 'effect': lambda player: player.set_dodge(player.get_dodge() + 1), 'icon': '../assets/objects/recieve_attributes.png'},
            {'title': 'Receber Sorte', 'description': 'Você fica mais sortudo', 'effect': lambda player: player.set_lucky(player.get_lucky() + 1), 'icon': '../assets/objects/recieve_attributes.png'},
            {'title': 'Receber Velocidade de ataque', 'description': 'Você ataca mais rápido', 'effect': lambda player: player.set_attack_speed(player.get_attack_speed() + 1), 'icon': '../assets/objects/recieve_attributes.png'},
            {'title': 'Receber Crítico', 'description': 'Seus críticos vão ser mais frequente', 'effect': lambda player: player.set_critical_chance(player.get_critical_chance() + 1), 'icon': '../assets/objects/recieve_attributes.png'},
            {'title': 'Trocar vida por força', 'description': 'Troca dois pontos de vida por mais força que o normal', 'effect': lambda player: player.trade_health_for_attribute('strength'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar vida por esquiva', 'description': 'Troca dois pontos de vida por mais chance de esquiva que o normal', 'effect': lambda player: player.trade_health_for_attribute('dodge'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar vida por sorte', 'description': 'Troca dois pontos de vida por mais sorte que o normal', 'effect': lambda player: player.trade_health_for_attribute('lucky'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar vida por velocidade de ataque', 'description': 'Troca dois pontos de vida por mais velocidade de ataque que o normal', 'effect': lambda player: player.trade_health_for_attribute('attack_speed'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar vida por crítico', 'description': 'Troca dois pontos de vida por mais crítico que o normal', 'effect': lambda player: player.trade_health_for_attribute('critical_chance'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar Sorte por vida', 'description': 'Trocar sorte por um ponto de vida', 'effect': lambda player: player.trade_lucky_for_attribute('health'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar Sorte por força', 'description': 'Trocar sorte por um pouco de força', 'effect': lambda player: player.trade_lucky_for_attribute('strength'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar esquiva por vida', 'description': 'Trocar esquiva por um ponto de vida', 'effect': lambda player: player.trade_dodge_for_attribute('health'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar esquiva por força', 'description': 'Trocar esquiva por um pouco de força', 'effect': lambda player: player.trade_dodge_for_attribute('strength'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar esquiva por sorte', 'description': 'Trocar esquiva por um pouco de sorte', 'effect': lambda player: player.trade_dodge_for_attribute('lucky'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar crítico por vida', 'description': 'Trocar crítico por um ponto de vida', 'effect': lambda player: player.trade_critical_chance_for_attribute('health'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar crítico por força', 'description': 'Trocar crítico por um pouco de força', 'effect': lambda player: player.trade_critical_chance_for_attribute('strength'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar crítico por esquiva', 'description': 'Trocar crítico por um pouco de esquiva', 'effect': lambda player: player.trade_critical_chance_for_attribute('dodge'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar Força por crítico', 'description': 'Trocar força por um pouco de crítico', 'effect': lambda player: player.trade_strength_for_attribute('critical_chance'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar Força por esquiva', 'description': 'Trocar força por um pouco de esquiva', 'effect': lambda player: player.trade_strength_for_attribute('dodge'), 'icon': '../assets/objects/trade_attributes.png'},
            {'title': 'Trocar Força por sorte', 'description': 'Trocar força por um pouco de sorte', 'effect': lambda player: player.trade_strength_for_attribute('lucky'), 'icon': '../assets/objects/trade_attributes.png'}
        ]

        self.selected_perks = []
        self.perk_cards = [] 
        self.is_node_perk = False
        self.is_first_node = True
        self.card_image = pygame.image.load('../assets/objects/skill_scroll.png').convert_alpha()
        self.boss_image = pygame.image.load('../assets/scene/map/boss_map.png')
        self.bonus_image = pygame.image.load('../assets/scene/map/attributes_bonus_map.png')

        self.nodes = [] 
        self.player = PlayerFactory.create_player(0, 0, self.player.attributes)
        self.generate_branches()
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1150 

        self.moving_entity = None  
        self.move_target_node = None 
        self.move_speed = 300 
        
    def generate_branches(self, steps=3):
        start_x = 930
        start_y = 830
        branch_width = 90
        branch_height = 90
        offset_x = 110
        offset_y = 110

        current_x = start_x
        current_y = start_y

        first = {
            'rect': pygame.Rect(current_x, current_y, branch_width, branch_height),
            'parent': None,
            'type': 'start',
            'entity': self.player
        }
        self.nodes.append(first)

        self.player.rect = first['rect']
        self.player.current_frames = self.player.idle_frames
        self.player.frame_index = 0
        self.player.animation_timer = 0
        self.player.current_frame = self.player.current_frames[0]

        for _ in range(steps):
            middle_node = self.nodes[-1]

            branch_x_left = current_x - offset_x
            branch_y_left = current_y - offset_y
            left_branch = {
                'rect': pygame.Rect(branch_x_left, branch_y_left, branch_width, branch_height),
                'parent': middle_node['rect'],
                'type': 'branch'
            }

            branch_x_right = current_x + offset_x
            branch_y_right = current_y - offset_y
            right_branch = {
                'rect': pygame.Rect(branch_x_right, branch_y_right, branch_width, branch_height),
                'parent': middle_node['rect'],
                'type': 'branch'
            }

            put_enemy_in_left = random.choice([True, False])

            if self.enemies:
                enemy = self.enemies.pop(random.randrange(len(self.enemies)))
                enemy_image = enemy['image']
                enemy_type = enemy['type']

                if put_enemy_in_left:
                    left_branch['enemy_image'] = enemy_image
                    left_branch['enemy_type'] = enemy_type
                    right_branch['type'] = 'perk'
                else:
                    right_branch['enemy_image'] = enemy_image
                    right_branch['enemy_type'] = enemy_type
                    left_branch['type'] = 'perk'

            self.nodes.append(left_branch)
            self.nodes.append(right_branch)

            return_x = current_x
            return_y = branch_y_left - offset_y
            return_left = {
                'rect': pygame.Rect(return_x, return_y, branch_width, branch_height),
                'parent': left_branch['rect'],
                'type': 'middle'
            }
            return_right = {
                'rect': pygame.Rect(return_x, return_y, branch_width, branch_height),
                'parent': right_branch['rect'],
                'type': 'middle'
            }

            self.nodes.append(return_left)
            self.nodes.append(return_right)

            current_y = return_y


    def draw_branches(self, screen):
        if self.in_battle:
            return
        
        for node in self.nodes:
            if node['parent']:
                start = node['parent'].center
                end = node['rect'].center
                pygame.draw.line(screen, 'gray', start, end, 5)

        for node in self.nodes:
            if 'enemy_image' in node:
                img = node['enemy_image']
                scale_factor = 1
                new_width = int(node['rect'].width * scale_factor)
                new_height = int(node['rect'].height * scale_factor)

                scaled_img = pygame.transform.scale(img, (new_width, new_height))
                rounded_img = self.round_image(scaled_img, radius=min(new_width, new_height)//2) 

                rect = rounded_img.get_rect(center=node['rect'].center)
                screen.blit(rounded_img, rect)

            elif node['type'] == 'middle':
                if node.get('entity') != self.player and 'enemy_image' not in node:
                    scale_factor = 1.7
                    new_width = int(node['rect'].width * scale_factor)
                    new_height = int(node['rect'].height * scale_factor)

                    scaled_img = pygame.transform.scale(self.boss_image, (new_width, new_height))
                    rounded_img = self.round_image(scaled_img, radius=min(new_width, new_height)//2)
                    rect = rounded_img.get_rect(center=node['rect'].center)

                    screen.blit(rounded_img, rect)

            elif 'entity' not in node:
                scale_factor = 0.7
                new_width = int(node['rect'].width * scale_factor)
                new_height = int(node['rect'].height * scale_factor)

                scaled_img = pygame.transform.scale(self.bonus_image, (new_width, new_height))
                rounded_img = self.round_image(scaled_img, radius=min(new_width, new_height)//2)
                rect = rounded_img.get_rect(center=node['rect'].center)

                border_radius = max(new_width, new_height) // 2 
                pygame.draw.circle(screen, 'black', rect.center, border_radius + 2) 

                screen.blit(rounded_img, rect)

        if self.moving_entity:
            self.moving_entity.update_animation(self.dt)
            self.moving_entity.draw(screen)

        for node in self.nodes:
            if 'entity' in node and node['entity'] == self.player:
                entity = node['entity']
                entity.update_animation(self.dt) 
                entity.draw(screen)

    def draw_ui(self, screen):
        self.update_movement()
        self.draw_branches(screen)
        self.draw_attributes(screen)
        if self.is_node_perk or self.is_first_node:
            self.draw_perks(screen)


    def round_image(self, surface, radius):
        size = surface.get_size()

        rounded_surface = pygame.Surface(size, pygame.SRCALPHA)
        
        rect = pygame.Rect(0, 0, *size)
        shape_surf = pygame.Surface(size, pygame.SRCALPHA)
        
        pygame.draw.rect(shape_surf, (255, 255, 255, 255), rect, border_radius=radius)

        rounded_surface.blit(surface, (0, 0))
        rounded_surface.blit(shape_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        return rounded_surface

    def handle_node_click(self, clicked_node):
        current_node = None
        for node in self.nodes:
            if 'entity' in node and node['entity'] == self.player:
                current_node = node
                break

        if not current_node:
            return  

        if clicked_node['rect'] == current_node.get('parent'):
            pass
        else:
            if self.is_choosing_perk:
                return 
            
            for node in self.nodes:
                if node.get('parent') == current_node['rect'] and node['rect'] == clicked_node['rect']:
                    self.move_player_to_node(clicked_node)
                    break

    def move_player_to_node(self, node):
        self.moving_entity = PlayerFactory.create_player(self.player.rect.x, self.player.rect.y)
        self.move_target_node = node

        self.moving_entity.current_frames = self.moving_entity.walking_top_frames
        self.moving_entity.frame_index = 0
        self.moving_entity.animation_timer = 0
        self.moving_entity.current_frame = self.moving_entity.current_frames[0]

        for n in self.nodes:
            if 'entity' in n and n['entity'] == self.player:
                del n['entity']
                break

    def update_movement(self):
        if self.moving_entity and self.move_target_node:
            target_pos = pygame.math.Vector2(self.move_target_node['rect'].center)
            current_pos = pygame.math.Vector2(self.moving_entity.rect.center)
            
            direction = (target_pos - current_pos)
            distance = direction.length()

            if distance < 5: 
                self.moving_entity = None
                self.player.rect = self.move_target_node['rect']
                self.move_target_node['entity'] = self.player

                if 'enemy_image' in self.move_target_node:

                    self.manager.map_scenario = self
                    self.manager.start_battle(self, self.move_target_node['enemy_type'])
                elif self.move_target_node['type'] == 'perk':
                    self.is_node_perk = True

                self.move_target_node = None

                self.player.current_frames = self.player.idle_frames
                self.player.frame_index = 0
                self.player.animation_timer = 0
                self.player.current_frame = self.player.current_frames[0]

            else:
                direction = direction.normalize()
                move_step = direction * self.move_speed * self.dt
                new_pos = current_pos + move_step

                self.moving_entity.rect.center = (round(new_pos.x), round(new_pos.y))
                self.moving_entity.update_animation(self.dt)

    def draw_perks(self, screen):
        if self.in_battle:
            return

        self.is_choosing_perk = True

        if not self.selected_perks:
            self.selected_perks = random.sample(self.perks, 3)
            self.perk_cards = []

        def render_multiline_text(text, font, color, max_width):
            wrapped_lines = []
            for paragraph in text.split('\n'):
                wrapped = textwrap.wrap(paragraph, width=30)
                wrapped_lines.extend(wrapped)
            return [font.render(line, True, color) for line in wrapped_lines]

        card_width = 500
        card_height = 390

        for i, perk in enumerate(self.selected_perks):
            card_x = 200 + i * (card_width + 20)
            card_y = 560 - card_height // 2

            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            self.perk_cards.append((card_rect, perk))

            card_img_scaled = pygame.transform.smoothscale(self.card_image, (card_width, card_height))
            screen.blit(card_img_scaled, (card_x, card_y))

            padding_x = 15
            max_text_width = card_width - padding_x * 2

            title_surfaces = render_multiline_text(perk['title'], self.font_title, (0, 0, 0), max_text_width)

            title_y_offset = card_y + 90  
            y_offset = title_y_offset

            area_center_x = card_x + padding_x + (max_text_width // 2)

            for surf in title_surfaces:
                title_rect = surf.get_rect()
                title_rect.centerx = area_center_x
                title_rect.top = y_offset
                screen.blit(surf, title_rect)
                y_offset += surf.get_height()

            space_between_title_and_icon = 30  
            y_offset += space_between_title_and_icon

            icon_image = pygame.image.load(perk['icon']).convert_alpha()
            icon_rect = icon_image.get_rect()
            icon_rect.centerx = card_x + card_width // 2
            icon_rect.top = y_offset
            screen.blit(icon_image, icon_rect)
            y_offset += icon_rect.height

            description_surfaces = render_multiline_text(perk['description'], self.font_desc, (0, 0, 0), max_text_width)

            max_desc_height = card_y + card_height - 20
        
            for surf in description_surfaces:
                if y_offset + surf.get_height() > max_desc_height:
                    break
                desc_rect = surf.get_rect()
                desc_rect.centerx = area_center_x
                desc_rect.top = y_offset
                screen.blit(surf, desc_rect)
                y_offset += surf.get_height() + 3

    def handle_perk_click(self, mouse_pos):
        if not self.is_choosing_perk:
            return

        for rect, perk in self.perk_cards:
            if rect.collidepoint(mouse_pos):
                print(f"Perk escolhido: {perk['title']}")
                perk['effect'](self.player)
                self.is_choosing_perk = False
                self.is_node_perk = False 
                self.is_first_node = False
                self.selected_perks = [] 
                self.perk_cards = []
                break

    def draw_attributes(self, screen):
        if self.in_battle:
            return

        font = pygame.font.Font(None, 24) 
        color = (255, 255, 255)  

        x = 10
        y = 10
        spacing = 25 

        attributes = [
            f"Vida: {self.player.get_health()}",
            f"Força: {self.player.get_strength()}",
            f"Esquiva: {self.player.get_dodge()}",
            f"Sorte: {self.player.get_lucky()}",
            f"Velocidade de Ataque: {self.player.get_attack_speed()}",
            f"Chance de crítico: {self.player.get_critical_chance()}",
        ]

        for attr in attributes:
            text_surface = font.render(attr, True, color)
            screen.blit(text_surface, (x, y))
            y += spacing

