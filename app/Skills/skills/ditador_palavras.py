
from Skills.skill import Skill


class DitadorDePalavras(Skill):
    def __init__(self):
        super().__init__("Ditador de Palavras")
        self.streak = 0
        self.activated_once = False
    def on_word_typed(self, context, word: str, correct: bool):
        if correct:
            self.streak += 1
        else:
            self.streak = 0

    def activate(self, context):
        context.interface.reset_plauer_turn_timer()
        context.interface.show_popup("Ditador de Palavras ativado!", duration=2.0, y=880)
        context.manager.player.remove_skill(self.get_name())
        context.active_skills.append(self) 

    def on_3_words_success(self, context):
        if self.streak >= 3 and not self.activated_once:
            context.interface.show_popup("O inimigo foi cegado por 2 turnos!", duration=2.0, y=880)
            context.enemy.forced_miss_turns += 2
            self.activated_once = True
            self.streak = 0