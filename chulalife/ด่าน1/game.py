import os
import pygame
from player import Player
from sprite import sprites

pygame.init()

# Set up screen
pygame.display.set_caption("Chula life")
screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
clear_color = (30, 150, 50)
running = True

# Verify the image path
image_path = os.path.join(os.getcwd(), "chulalife/ด่าน1/image/player.png")
if not os.path.exists(image_path):
    print(f"Image file not found: {image_path}")
    running = False  # Exit if the image is not found

# Initialize player
if running:  # Only initialize if the game is set to run
    player = Player(image_path, 400, 300)

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Exit fullscreen with ESC
                running = False

    # Clear screen
    screen.fill(clear_color)

    # Draw and update player and sprites
    if running:
        player.draw(screen)
        player.update()  # Update the player if it has an update method

    for sprite in sprites:
        sprite.draw(screen)

    # Update display
    pygame.display.flip()

pygame.quit()
