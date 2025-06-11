import pygame
import random
from Scenario.scenario import Scenario
import random
from Factory.playerFactory import PlayerFactory
from Interface.interace import Interface
from Utils.utils import Utils

class Map(Scenario):
    def __init__(self, manager, background, player):
        super().__init__(manager)
        self.manager = manager
        self.player = player
        self.enable_ground = False
        self.enable_solids = False
        self.enable_background = True
        self.enable_ui = True
        self.in_battle = False
        self.is_choosing_perk = False
        self.font_title = pygame.font.Font('../assets/fonts/CrimsonPro-VariableFont_wght.ttf', 24)
        self.font_desc = pygame.font.Font('../assets/fonts/CrimsonPro-VariableFont_wght.ttf', 18)

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

        self.is_animating_perk = True
        self.perk_image_sheet = pygame.image.load('../assets/objects/perks_cards.png').convert_alpha()
        self.frame_perk_width = 510
        self.frame_perk_height = 899
        self.num_perk_cols = 5
        self.num_perk_rows = 3
        self.perk_frames = self.load_perk_frames()
        self.current_perk_frame = 0
        self.num_perk_frames = len(self.perk_frames)
        self.time_perk_accumulator = 0
        self.perk_animation_speed = 0.4

        self.time_passed = 0

        self.frame_player_index = 0

        self.boss_image = pygame.image.load('../assets/scene/map/boss_map.png')
        self.bonus_image = pygame.image.load('../assets/scene/map/attributes_bonus_map.png')

        self.nodes = []
        self.player = PlayerFactory.create_player(0, 0, self.player.attributes)
        self.generate_branches()
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1200

        self.moving_entity = None
        self.move_target_node = None
        self.move_speed = 300

        self.utils = Utils()

        self.is_start_map_animating = True
        self.map_animation_sheet = pygame.image.load('../assets/scene/map/animation/open_map_animation.png').convert_alpha()

        self.frame_book_map_width = 744
        self.frame_book_map_height = 636
        self.frame_book_map_cols = 5
        self.num_book_map_frames = 19
        self.current_book_map_frame = 0
        self.animation_book_map_speed = 0.1
        self.time_book_map_accumulator = 0

        self.zoom_scale_book_map = 1.0
        self.target_zoom_book_map = 1.95
        self.zoom_speed_book_map = 0.015

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
        self.player.frame_player_index = 0
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
                rounded_img = self.utils.round_image(surface=scaled_img, radius=min(new_width, new_height)//2)

                rect = rounded_img.get_rect(center=node['rect'].center)
                screen.blit(rounded_img, rect)

            elif node['type'] == 'middle':
                if node.get('entity') != self.player and 'enemy_image' not in node:
                    scale_factor = 1.7
                    new_width = int(node['rect'].width * scale_factor)
                    new_height = int(node['rect'].height * scale_factor)

                    scaled_img = pygame.transform.scale(self.boss_image, (new_width, new_height))
                    rounded_img = self.utils.round_image(surface=scaled_img, radius=min(new_width, new_height)//2)
                    rect = rounded_img.get_rect(center=node['rect'].center)

                    screen.blit(rounded_img, rect)

            elif 'entity' not in node:
                scale_factor = 0.7
                new_width = int(node['rect'].width * scale_factor)
                new_height = int(node['rect'].height * scale_factor)

                scaled_img = pygame.transform.scale(self.bonus_image, (new_width, new_height))
                rounded_img = self.utils.round_image(surface=scaled_img, radius=min(new_width, new_height)//2)
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
        interface = Interface(self.player)

        if not self.is_start_map_animating:
            self.update_movement()
            self.draw_branches(screen)
            interface.draw_health_bar(screen)

            if self.is_node_perk or self.is_first_node:
                self.draw_perks(screen)
        self.draw_menu(screen)

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
        self.moving_entity.frame_player_index = 0
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
                    enemy_nodes = [node for node in self.nodes if 'enemy_image' in node]
                    enemy_index = enemy_nodes.index(self.move_target_node)

                    self.manager.map_scenario = self
                    self.manager.start_battle(self, self.move_target_node['enemy_type'], enemy_index)
                elif self.move_target_node['type'] == 'perk':
                    self.is_node_perk = True

                self.move_target_node = None

                self.player.current_frames = self.player.idle_frames
                self.player.frame_player_index = 0
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

            self.current_perk_frame = 0
            self.time_perk_accumulator = 0
            self.is_animating_perk = True

        card_width = 400
        card_height = 500
        spacing = 30
        total_width = (card_width * 3) + (spacing * 2)
        start_x = (screen.get_width() - total_width) // 2
        y = (screen.get_height() - card_height) // 2

        mouse_pos = pygame.mouse.get_pos()

        for i, perk in enumerate(self.selected_perks):
            x = start_x + i * (card_width + spacing)
            is_hovered = False

            card_rect = pygame.Rect(x, y, card_width, card_height)
            if card_rect.collidepoint(mouse_pos) and not self.is_menu_open:
                is_hovered = True

            draw_width = card_width + 35 if is_hovered else card_width
            draw_height = card_height + 35 if is_hovered else card_height
            draw_x = x - 10 if is_hovered else x
            draw_y = y - 10 if is_hovered else y

            if self.perk_frames:
                frame = self.perk_frames[self.current_perk_frame]
                frame_scaled = pygame.transform.smoothscale(frame, (draw_width, draw_height))
                rounded_frame = self.utils.round_image(frame_scaled, 20)
                screen.blit(rounded_frame, (draw_x, draw_y))

            if not self.is_animating_perk:
                center_x = draw_x + draw_width // 2
                title_y = draw_y + 160

                title_surfs = self.utils.render_multiline_text(perk["title"], self.font_title, (0,0,0))
                for surf in title_surfs:
                    rect = surf.get_rect(centerx=center_x, top=title_y)
                    screen.blit(surf, rect)
                    title_y += surf.get_height()

                try:
                    icon = pygame.image.load(perk["icon"]).convert_alpha()
                    icon = pygame.transform.scale(icon, (64, 64))
                    icon_rect = icon.get_rect(centerx=center_x, top=title_y + 10)
                    screen.blit(icon, icon_rect)
                    icon_bottom = icon_rect.bottom
                except:
                    icon_bottom = title_y + 64 + 10

                desc_y = icon_bottom + 10
                desc_surfs = self.utils.render_multiline_text(perk["description"], self.font_desc, (0,0,0))
                for surf in desc_surfs:
                    rect = surf.get_rect(centerx=center_x, top=desc_y)
                    screen.blit(surf, rect)
                    desc_y += surf.get_height() + 3

            self.perk_cards.append((pygame.Rect(draw_x, draw_y, draw_width, draw_height), perk))


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


    def draw_background(self, screen):
        screen.fill((0, 0, 0))

        if self.is_start_map_animating or self.current_book_map_frame == self.num_book_map_frames - 1:
            col = self.current_book_map_frame % self.frame_book_map_cols
            row = self.current_book_map_frame // self.frame_book_map_cols

            frame_rect = pygame.Rect(
                col * self.frame_book_map_width,
                row * self.frame_book_map_height,
                self.frame_book_map_width,
                self.frame_book_map_height
            )

            frame_image = self.map_animation_sheet.subsurface(frame_rect)

            scale_factor = self.zoom_scale_book_map if self.current_book_map_frame == self.num_book_map_frames - 1 else 1.0
            scaled_width = int(self.frame_book_map_width * scale_factor)
            scaled_height = int(self.frame_book_map_height * scale_factor)

            frame_image = pygame.transform.scale(
                frame_image,
                (scaled_width, scaled_height)
            )

            max_lift = 120
            lift = int((scale_factor - 1.0) / (self.target_zoom_book_map - 1.0) * max_lift) if scale_factor > 1.0 else 0

            x = (screen.get_width() - scaled_width) // 2
            y = (screen.get_height() - scaled_height) // 2 - lift

            screen.blit(frame_image, (x, y))

        if self.background_image and not self.is_start_map_animating:
            screen_width, screen_height = screen.get_size()
            bg_width, bg_height = self.background_image.get_size()

            x = (screen_width - bg_width) // 2
            y = (screen_height - bg_height) // 2

            rounded_bg = self.utils.round_image(surface=self.background_image, radius=90)

            screen.blit(rounded_bg, (x, y))

    def update(self):
        if self.is_start_map_animating:
            self.time_book_map_accumulator += self.dt

            if self.time_book_map_accumulator >= self.animation_book_map_speed:
                self.time_book_map_accumulator = 0
                if self.current_book_map_frame < self.num_book_map_frames - 1:
                    self.current_book_map_frame += 1

        if self.current_book_map_frame == self.num_book_map_frames - 1:
            if self.zoom_scale_book_map < self.target_zoom_book_map:
                self.zoom_scale_book_map += self.zoom_speed_book_map
                if self.zoom_scale_book_map > self.target_zoom_book_map:
                    self.zoom_scale_book_map = self.target_zoom_book_map
                    self.is_start_map_animating = False

        if (self.is_choosing_perk or self.is_first_node) and not self.is_start_map_animating:
            self.time_perk_accumulator += self.dt * 1000

            if self.time_perk_accumulator >= self.perk_animation_speed:
                self.time_perk_accumulator = 0
                if self.current_perk_frame < self.num_perk_frames - 1:
                    self.current_perk_frame += 1
                else:
                    self.is_animating_perk = False


    def load_perk_frames(self):
        perk_frames = []
        for row in range(self.num_perk_rows):
            for col in range(self.num_perk_cols):
                x = col * self.frame_perk_width
                y = row * self.frame_perk_height
                frame = self.perk_image_sheet.subsurface(
                    pygame.Rect(x, y, self.frame_perk_width, self.frame_perk_height)
                )
                perk_frames.append(frame)
        return perk_frames
