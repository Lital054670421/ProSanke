"""
sound_manager.py

This module implements the SoundManager for the Snake game.
It manages background music and sound effects using the Singleton pattern,
ensuring that only one instance of the SoundManager exists.
It provides functions to load, play, stop, and toggle audio.
"""

import pygame
import config.settings as settings

class SoundManager:
    """
    A Singleton class to manage background music and sound effects.
    
    This class initializes pygame's mixer, loads sound effect files and background music,
    and provides methods to play and stop sounds. It ensures only one instance exists.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Initialize the mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Flag indicating whether background music is enabled (default from settings)
        self.music_enabled = getattr(settings, "BACKGROUND_MUSIC", True)
        
        # Dictionary to hold loaded sound effects
        self.sounds = {}
        self.load_sounds()

        # Load background music file path from settings (if provided)
        self.music_file = getattr(settings, "MUSIC_BACKGROUND", None)

    def load_sounds(self) -> None:
        """
        Loads sound effect files defined in settings into the sounds dictionary.
        """
        try:
            self.sounds["SOUND_FOOD"] = pygame.mixer.Sound(settings.SOUND_FOOD)
        except Exception as e:
            print("Error loading SOUND_FOOD:", e)
        try:
            self.sounds["SOUND_GAMEOVER"] = pygame.mixer.Sound(settings.SOUND_GAMEOVER)
        except Exception as e:
            print("Error loading SOUND_GAMEOVER:", e)
        try:
            self.sounds["SOUND_MOVE"] = pygame.mixer.Sound(settings.SOUND_MOVE)
        except Exception as e:
            print("Error loading SOUND_MOVE:", e)

    def play_music(self, loops: int = -1) -> None:
        """
        Plays the background music in a loop if music is enabled.
        
        :param loops: Number of times to loop; -1 means infinite.
        """
        if self.music_enabled and self.music_file:
            try:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.play(loops=loops)
            except Exception as e:
                print("Error playing background music:", e)

    def stop_music(self) -> None:
        """
        Stops the background music.
        """
        pygame.mixer.music.stop()

    def toggle_music(self) -> None:
        """
        Toggles the background music on or off.
        """
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.play_music()
        else:
            self.stop_music()

    def set_volume(self, volume: float) -> None:
        """
        Sets the volume for both background music and all sound effects.
        
        :param volume: A float between 0.0 (mute) and 1.0 (max volume).
        """
        try:
            pygame.mixer.music.set_volume(volume)
            for key, sound in self.sounds.items():
                sound.set_volume(volume)
        except Exception as e:
            print(f"Error setting volume: {e}")

    def play_sound(self, sound_key: str) -> None:
        """
        Plays a sound effect corresponding to the given sound key.
        
        :param sound_key: The key of the sound effect (e.g. "SOUND_FOOD").
        """
        sound = self.sounds.get(sound_key)
        if sound:
            try:
                sound.play()
            except Exception as e:
                print(f"Error playing sound {sound_key}:", e)
        else:
            print(f"Sound {sound_key} not found.")


# For testing purposes, you can run this module independently.
if __name__ == "__main__":
    pygame.init()
    # Create an instance of SoundManager (Singleton)
    sm = SoundManager()
    print("Playing background music...")
    sm.play_music()
    pygame.time.delay(2000)  # 2-second delay
    print("Playing SOUND_FOOD effect...")
    sm.play_sound("SOUND_FOOD")
    pygame.time.delay(2000)
    print("Toggling music (should stop)...")
    sm.toggle_music()
    pygame.time.delay(2000)
    print("Setting volume to 0.3 (Low)...")
    sm.set_volume(0.3)
    pygame.time.delay(2000)
    print("Setting volume to 1.0 (High)...")
    sm.set_volume(1.0)
    pygame.time.delay(3000)
    pygame.quit()
