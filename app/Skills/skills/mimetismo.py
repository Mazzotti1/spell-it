
from Skills.skill import Skill


class Mimetismo(Skill):
    def __init__(self):
        super().__init__("Mimetismo")
        self.streak = 0

    def activate(self, context):
        context.interface.reset_plauer_turn_timer()
        context.interface.show_popup("Mimetismo ativado!", duration=2.0)
        context.manager.player.remove_skill(self.get_name())
        context.manager.player.is_mime_hit = True
        context.manager.player.mime_damage = context.enemy.get_strength() * 2
        context.active_skills.append(self) 
