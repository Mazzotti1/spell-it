from Entity.entity import Entity
from Skills.skill import Skill 

class Player(Entity):
    def __init__(self, name, attributes, x=0, y=0):
        super().__init__(x, y, name, attributes)

        #pra carregar os outros sprites lembrar de botar em 128x128
        self.load_animations({
            "idle": "../assets/player/idle_sprite.png",
            # "idle_back": "../assets/player/player_idle_back.png",
            # "walking_left": "../assets/player/player_walking_left.png",
            # "walking_right": "../assets/player/player_walking_right.png",
            "walking_node_right": "../assets/player/player_diagonal_right.png",
            # "walking_node_left": "../assets/player/player_diagonal_right.png",
            "walking_top": "../assets/player/player_walking_top.png",
            # "walking_bottom": "../assets/player/player_walking_bottom.png",
        })

        self.skills: list[Skill] = []


    def add_skill(self, skill: Skill):
        self.skills.append(skill)

    def use_skill(self, skill_name: str, target: "Entity"):
        skill = next((s for s in self.skills if s.name == skill_name), None)
        skill.use(self, target)