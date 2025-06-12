import os
import random
from Words.RandomWord import RandomWord

class RandomWordManager:
    def __init__(self, screen_size, lifetime=5, biome=None, player_position=None):
        self.screen_size = screen_size
        self.words = []
        self.lifetime = lifetime

        self.biome = biome
        self.word_pool = []

        self.player_position = player_position

        self.biome_name = self.get_biome_name(biome)

        if self.biome_name:
            self.load_words_from_biome(self.biome_name)

    def get_biome_name(self, biome_path):
        filename = os.path.basename(biome_path)
        name = os.path.splitext(filename)[0]
        return name

    def load_words_from_biome(self, biome):
        filename = f"{biome}.txt"
        try:
            with open(f"../assets/pre_combat_words/{filename}", "r", encoding="utf-8") as f:
                self.word_pool = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.word_pool = []

    def generate_pre_combat_words(self, quantity=5):
        if len(self.word_pool) < quantity:
            quantity = len(self.word_pool)

        selected_words = random.sample(self.word_pool, quantity)
        self.words = []
        for word in selected_words:
            x, y = self.get_valid_position(min_distance=200)
            self.words.append(RandomWord(self.screen_size, text=word, x=x, y=y, lifetime=self.lifetime))

    def update(self):
        self.words = [word for word in self.words if not word.is_expired()]

    def draw(self, screen):
        for word in self.words:
            word.draw(screen)

    def get_valid_position(self, min_distance=200):
        max_attempts = 100
        screen_width, screen_height = self.screen_size
        scenario_height = 817
        top_margin = (screen_height - scenario_height) // 2

        for _ in range(max_attempts):
            x = random.randint(0, screen_width - 100)
            y = random.randint(top_margin, top_margin + scenario_height - 50)

            if self.player_position:
                dx = x - self.player_position[0]
                dy = y - self.player_position[1]
                distance_squared = dx*dx + dy*dy
                if distance_squared >= min_distance * min_distance:
                    return x, y
            else:
                return x, y
        return 0, top_margin

    def check_word(self, typed_word):
        for word_obj in self.words:
            if word_obj.text.lower() == typed_word.lower():
                self.words.remove(word_obj)
                return word_obj
        return False

    def check_punishment_word(self, typed_word):
        if 'punir' == typed_word.lower():
            return True

    def generate_final_pre_combat_word(self, enemy):
        enemy_x, enemy_y = enemy.get_position()

        center_x = enemy_x + enemy.width // 2
        center_y = enemy_y + enemy.height // 2

        word = 'PUNIR'
        self.words.append(RandomWord(self.screen_size, text=word, x=center_x, y=center_y, lifetime=10, style='PUNIR'))