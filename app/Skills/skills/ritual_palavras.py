
from Skills.skill import Skill


class RitualDasPalavras(Skill):
    def __init__(self):
        super().__init__("Ritual das Palavras")
        self.streak = 0
        self.activated_once = False
    def on_word_typed(self, context, word: str, correct: bool):
        if correct:
            self.streak += 1
        else:
            self.streak = 0

    def activate(self, context):
        context.interface.reset_plauer_turn_timer()
        context.interface.show_popup("Ritual das palaras ativado!", duration=2.0, y=880)
        context.manager.player.remove_skill(self.get_name())
        context.active_skills.append(self) 

    def on_3_words_success(self, context):
        if self.streak >= 6 and not self.activated_once:
            context.interface.show_popup("Você está mais forte por 2 turnos!", duration=2.0, y=880)
            
            context.manager.player.buff_atack_speed += 2
            context.manager.player.buff_atack_damage += 2

            self.activated_once = True
            self.streak = 0