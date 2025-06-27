import pygame

class AudioManager:
    _instance = None

    @staticmethod
    def instance():
        if AudioManager._instance is None:
            AudioManager()
        return AudioManager._instance

    def __init__(self):
        if AudioManager._instance is not None:
            raise Exception("AudioManager já foi instanciado!")
        AudioManager._instance = self

        self.audio_muted = False
        self.master_volume = 0.5
        self.sound_cache = {}

        pygame.mixer.music.set_volume(self.master_volume)
        self.current_music_path = None 
        self.previous_music_path = None

        self.pending_music = None
        self.fade_start_time = 0
        self.fade_duration = 0


        pygame.mixer.music.set_volume(self.master_volume)

    def toggle_mute(self):
        self.audio_muted = not self.audio_muted
        if self.audio_muted:
            pygame.mixer.music.set_volume(0)
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.set_volume(self.master_volume)
            pygame.mixer.music.unpause()

    def set_volume(self, volume):
        self.master_volume = max(0.0, min(1.0, volume))
        if not self.audio_muted:
            pygame.mixer.music.set_volume(self.master_volume)


    def play_music(self, path: str, loop: bool = True, fadein_ms: int = 0):
        if self.current_music_path == path:
            return

        self.current_music_path = path
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0 if self.audio_muted else self.master_volume)
        pygame.mixer.music.play(loops=-1 if loop else 0, fade_ms=fadein_ms)


    def play_battle_music(self, path: str, loop: bool = True):
        self.previous_music_path = self.current_music_path
        self.play_music(path, loop=loop, fadein_ms=2000)

    def restore_previous_music(self, fade_ms=2000):
        if self.previous_music_path:
            pygame.mixer.music.fadeout(fade_ms)
            
            self.pending_music = self.previous_music_path
            self.fade_start_time = pygame.time.get_ticks()
            self.fade_duration = fade_ms
            
            self.previous_music_path = None

    def play_sound_effect(self, path: str, volume: float = 1.0):
        try:
            if path not in self.sound_cache:
                self.sound_cache[path] = pygame.mixer.Sound(path)
            sound = self.sound_cache[path]
            sound.set_volume(volume)
            sound.play()
        except pygame.error as e:
            print(f"[Erro] Não foi possível carregar o som '{path}': {e}")

    def update(self):
        if hasattr(self, "pending_music") and self.pending_music:
            elapsed = pygame.time.get_ticks() - self.fade_start_time
            if elapsed >= self.fade_duration:
                self.play_music(self.pending_music)
                self.pending_music = None