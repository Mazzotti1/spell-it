class PunishAnimation:
    def __init__(self, animation, delay=0.0, position_offset=(0, 0)):
        self.animation = animation  
        self.delay = delay  
        self.elapsed = 0
        self.started = False
        self.position_offset = position_offset

    def update(self, dt):
        self.elapsed += dt
        if not self.started and self.elapsed >= self.delay:
            self.started = True
        if self.started:
            self.animation.update(dt)

    def draw(self, screen):
        if self.started:
            self.animation.draw(screen)

    def is_finished(self):
        return self.started and self.animation.is_finished()