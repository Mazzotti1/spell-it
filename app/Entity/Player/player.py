from Entity.entity import Entity
from Skills.skill import Skill 

class Player(Entity):
    def __init__(self, name, attributes, x=0, y=0):
        super().__init__(x, y, name, attributes)

        self.load_animations({
            "idle": "../assets/player/idle_sprite.png",
        })

        self.skills: list[Skill] = []


    def add_skill(self, skill: Skill):
        self.skills.append(skill)

    def use_skill(self, skill_name: str, target: "Entity"):
        skill = next((s for s in self.skills if s.name == skill_name), None)
        skill.use(self, target)