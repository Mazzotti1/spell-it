class FloatingText:
    def __init__(self, text, position, color, font, duration=1.0):
        self.text = text
        self.position = list(position)  
        self.color = color
        self.font = font
        self.duration = duration
        self.timer = 0
        self.velocity_y = -30  

        self.image = self.font.render(str(self.text), True, self.color)
        self.rect = self.image.get_rect(center=position)

    def update(self, dt):
        self.timer += dt
        self.position[1] += self.velocity_y * dt
        self.rect.center = (self.position[0], self.position[1])

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_finished(self):
        return self.timer >= self.duration
