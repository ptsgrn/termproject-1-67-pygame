import pygame

# Initialize Pygame mixer
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("assets/song/RealMan_bg_music.mp3")
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

while True:
    pass
