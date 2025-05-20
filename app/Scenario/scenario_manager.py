

class ScenarioManager:
    def __init__(self):
        self.current_scenario = None

    def change_scenario(self, new_scenario):
        self.current_scenario = new_scenario

    def update(self):
        if self.current_scenario:
            self.current_scenario.update()

    def draw(self, screen):
        if self.current_scenario:
            self.current_scenario.draw_scene(screen)
