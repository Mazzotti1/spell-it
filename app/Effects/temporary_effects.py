class TemporaryEffect:
    def __init__(self, image, position, duration= 1.0):
        self.image = image
        self.duration = duration 
        self.timer = 0
        self.position = list(position)  
        self.velocity_y = -120  

        self.rect = self.image.get_rect(center=position)

    def update(self, dt):
        self.timer += dt
        self.position[1] += self.velocity_y * dt 
        self.rect.center = (self.position[0], self.position[1])

    def is_finished(self):
        return self.timer >= self.duration

    def draw(self, screen):
        screen.blit(self.image, self.position)
