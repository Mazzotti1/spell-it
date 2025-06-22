
from Skills.skill import Skill


class EcoDePalavras(Skill):
    def __init__(self):
        super().__init__("Eco de Palavras")
        self.streak = 0
        self.count_words = 0
        self.last_correct_word = None

    def on_word_typed(self, context, word: str, correct: bool):
        if correct:
            self.last_correct_word = word
            self.streak += 1
            self.count_words += 1
        else:
            self.streak = 0


    def activate(self, context):
        context.interface.reset_plauer_turn_timer()
        context.interface.show_popup("Eco de palavras ativado!", duration=2.0)
        context.manager.player.remove_skill(self.get_name())
        context.active_skills.append(self) 

    def on_repeat_last_word(self, context, word: str):
        if self.last_correct_word == word and self.count_words >= 1:
            context.interface.show_popup("Eco de palavras foi atingido!", duration=2.0, priority=1)
            context.manager.player.double_damage = True
            self.last_correct_word = None

