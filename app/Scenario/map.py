import pygame
from Scenario.scenario import Scenario
import random
from Factory.playerFactory import PlayerFactory

class Map(Scenario):
    def __init__(self, manager, background):
        super().__init__()
        self.manager = manager
        self.enable_ground = False
        self.enable_solids = False
        self.enable_background = True
        self.enable_ui = True
        self.font = pygame.font.SysFont(None, 64)

        self.load_background(background)

        self.enemy_images = [
            pygame.image.load('../assets/scene/map/enemy_anaconda_map.png'),
            pygame.image.load('../assets/scene/map/enemy_calango_map.png'),
            pygame.image.load('../assets/scene/map/enemy_jacare_map.png'),
            pygame.image.load('../assets/scene/map/enemy_quero_quero_map.png'),
            pygame.image.load('../assets/scene/map/enemy_mico_map.png')
        ]

        self.boss_image = pygame.image.load('../assets/scene/map/boss_map.png')
        self.bonus_image = pygame.image.load('../assets/scene/map/attributes_bonus_map.png')

        self.nodes = [] 
        self.player = PlayerFactory.create_player(0, 0)
        self.generate_branches()
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1150 

        self.moving_entity = None  
        self.move_target_node = None 
        self.move_speed = 300 


        
    def generate_branches(self, steps=3):
        start_x = 930
        start_y = 870
        branch_width = 60
        branch_height = 60
        offset_x = 120
        offset_y = 120

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

            if self.enemy_images: 
                enemy_image = self.enemy_images.pop(random.randrange(len(self.enemy_images)))

                if put_enemy_in_left:
                    left_branch['enemy_image'] = enemy_image
                else:
                    right_branch['enemy_image'] = enemy_image

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