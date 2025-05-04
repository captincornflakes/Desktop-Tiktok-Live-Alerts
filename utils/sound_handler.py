import os
import pygame

def play_sound(sound_file):
    """
    Play a sound file using pygame.
    :param sound_file: Path to the sound file to play.
    """
    if not os.path.exists(sound_file):
        print(f"SoundHandler: Sound file '{sound_file}' not found.")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"SoundHandler: Error playing sound '{sound_file}': {str(e)}")

def play_alert_sound():
    """
    Play the alert sound using the file 'alert_sound.mp3'.
    """
    alert_file = "sounds/alert_sound.mp3"
    play_sound(alert_file)