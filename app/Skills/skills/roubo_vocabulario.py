
from Skills.skill import Skill


class RouboDeVocabulario(Skill):
    def __init__(self):
        super().__init__("Roubo de Vocabulário")
        self.streak = 0
        self.streak_enemy_words = 0 
        self.activated_once = False

    def on_word_typed(self, context, word: str, correct: bool):
        if correct:
            self.streak += 1
        else:
            self.streak = 0

    def activate(self, context):
        context.interface.reset_plauer_turn_timer()
        context.interface.show_popup("Roubo de Vocabulário ativado!", duration=2.0, y=880)
        context.manager.player.remove_skill(self.get_name())
        context.active_skills.append(self) 

    def on_repeat_enemy_word(self, context, word: str):

        for enemy_word in context.word_manager.enemy_words:
            if word == enemy_word.text:
                self.streak_enemy_words += 1

        if self.streak_enemy_words >= 2 and not self.activated_once:
            context.interface.show_popup("Roubo de vocabulário foi atingido!", duration=2.0, priority=1, y=880)
            context.manager.player.set_health(context.manager.player.get_health() + 20)
            self.activated_once = True