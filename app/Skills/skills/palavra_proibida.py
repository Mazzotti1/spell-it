
from Skills.skill import Skill


class PalavraProibida(Skill):
    def __init__(self):
        super().__init__("Palavra Proibida")
        self.streak = 0

    def activate(self, context):
        context.interface.reset_plauer_turn_timer()
        context.interface.show_popup("Palavra Proibida ativada!", duration=2.0)
        context.manager.player.remove_skill(self.get_name())
        context.manager.player.recieve_lucky += 2
        context.enemy.player_recieve_lucky += 2
        context.active_skills.append(self) 
