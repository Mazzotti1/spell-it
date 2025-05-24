from Entity.entity import Entity

class Enemy(Entity):
    def __init__(self, type, attributes, x=0, y=0, idle_sprite="../assets/enemys/anaconda/enemy_anaconda_idle_sprite.png"):
        super().__init__(x, y, type, attributes, width=384, height=384)
    
        self.load_animations({
            "idle": idle_sprite
        })

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type