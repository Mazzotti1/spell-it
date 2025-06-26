
from Skills.skill import Skill


class CorrenteDeCombos(Skill):
    def __init__(self):
        super().__init__("Corrente de Combos")
        self.streak = 0
        self.activated_once = False
    def on_word_typed(self, context, word: str, correct: bool):
        if correct:
            self.streak += 1
        else:
            self.streak = 0

    def activate(self, context):
        context.interface.reset_plauer_turn_timer()
        context.interface.show_popup("Corrente de Combos ativado!", duration=2.0, y=880)
        context.manager.player.remove_skill(self.get_name())
        context.active_skills.append(self) 

    def on_3_words_success(self, context):
        if self.streak >= 3 and not self.activated_once:
            context.interface.show_popup("O ataque será crítico!", duration=2.0, y=880)
            context.manager.player.force_critical_hit = True
            self.activated_once = True
            self.streak = 0