
class Attributes:
    def __init__(self, 
                 dodge: float, 
                 attack_speed: float, 
                 strength: float, 
                 health: int, 
                 lucky: float, 
                 critical_chance: float):
        self.dodge = dodge
        self.attack_speed = attack_speed
        self.strength = strength
        self.health = health
        self.lucky = lucky
        self.critical_chance = critical_chance

    def set_dodge(self, dodge: float):
        self.dodge = dodge

    def get_dodge(self):
        return self.dodge
    
    def set_attack_speed(self, attack_speed: float):
        self.attack_speed = attack_speed

    def get_attack_speed(self):
        return self.attack_speed
    
    def set_strength(self, strength: float):
        self.strength = strength

    def get_strength(self):
        return self.strength
    
    def set_health(self, health: int):
        self.health = health

    def get_health(self):
        return self.health
    
    def set_lucky(self, lucky: float):
        self.lucky = lucky

    def get_lucky(self):
        return self.lucky
    
    def set_critical_chance(self, critical_chance: float):
        self.critical_chance = critical_chance

    def get_critical_chance(self):
        return self.critical_chance