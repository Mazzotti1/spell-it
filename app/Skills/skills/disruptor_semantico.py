
from Skills.skill import Skill


class DisruptorSemantico(Skill):
    def __init__(self):
        super().__init__("Disruptor Semântico")
        self.streak = 0

    def activate(self, context):
        context.interface.reset_plauer_turn_timer()
        context.interface.show_popup("Disruptor Semântico ativado!", duration=2.0)
        context.manager.player.remove_skill(self.get_name())
        context.enemy.forced_miss_turns += 1
        context.active_skills.append(self) 
