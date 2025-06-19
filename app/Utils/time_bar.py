import time
import pygame

class TimerBar:
    def __init__(self, total_time, title, color=(200, 50, 50)):
        self.total_time = total_time
        self.current_time = total_time
        self.last_update = None
        self.title = title
        self.color = color
        self.is_visible = True

    def update(self, playerIsMoving=True):
        if not playerIsMoving:
            if self.last_update is None:
                self.last_update = time.time()
                return
            now = time.time()
            elapsed = now - self.last_update
            self.current_time = max(0, self.current_time - elapsed)
            self.last_update = now

    def reset(self):
        self.current_time = self.total_time
        self.last_update = time.time()

    def draw(self, screen, x, y, width, height, show_time=True, playerIsMoving=True):
        if not self.is_visible:
            return 
           
        self.update(playerIsMoving)
    
        pygame.draw.rect(screen, (80, 80, 80), (x, y, width, height), border_radius=5)

        percent = self.current_time / self.total_time if self.total_time > 0 else 0
        bar_width = int(width * percent)
        pygame.draw.rect(screen, self.color, (x, y, bar_width, height), border_radius=5)

        pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2, border_radius=5)

        font = pygame.font.SysFont(None, 22)
        if show_time:
            time_surface = font.render(f"{int(self.current_time)} Segundos", True, (255, 255, 255))
            screen.blit(time_surface, (x + width + 10, y + 3))

        title_font = pygame.font.SysFont(None, 24)
        title_surface = title_font.render(self.title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(x + width // 2, y - 20))
        screen.blit(title_surface, title_rect)

    def is_time_up(self):
        return self.current_time == 0

    def decrease_time(self, seconds):
        self.current_time -= seconds

    def clear(self):
        self.current_time = 0
        self.last_update = time.time()
