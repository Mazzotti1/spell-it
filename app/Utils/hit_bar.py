
import pygame


class HitBar:
    def __init__(self, total_hits, title="Acertos"):
        self.total_hits = total_hits
        self.current_hits = 0
        self.title = title
        self.is_visible = True

        self.red_threshold = total_hits // 3
        self.yellow_threshold = (total_hits * 2) // 3

    def add_hit(self):
        self.current_hits = min(self.total_hits, self.current_hits + 1)

    def reset(self):
        self.current_hits = 0

    def get_color(self):
        if self.current_hits <= self.red_threshold:
            return (200, 50, 50)   
        elif self.current_hits <= self.yellow_threshold:
            return (255, 200, 50)  
        else:
            return (50, 200, 50)  

    def draw(self, screen, x, y, width, height):
        if not self.is_visible:
            return

        pygame.draw.rect(screen, (80, 80, 80), (x, y, width, height), border_radius=5)

        percent = self.current_hits / self.total_hits if self.total_hits > 0 else 0
        bar_width = int(width * percent)
        color = self.get_color()

        pygame.draw.rect(screen, color, (x, y, bar_width, height), border_radius=5)

        pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2, border_radius=5)

        title_font = pygame.font.SysFont(None, 24)
        title_surface = title_font.render(self.title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(x + width // 2, y - 20))
        screen.blit(title_surface, title_rect)
