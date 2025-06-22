from Skills.skill import Skill

class ColapsoOrtografico(Skill):
    def __init__(self):
        super().__init__("Colapso Ortográfico")

    def activate(self, context):
        context.interface.reset_plauer_turn_timer()
        context.interface.show_popup("Colapso Ortográfico ativado!", duration=2.0)
        context.manager.player.remove_skill(self.get_name())
        context.active_skills.append(self) 

    def on_word_error(self, context, word):
        context.interface.show_popup(f"{word} foi desconsiderada automaticamente!", 1.5)
        return True