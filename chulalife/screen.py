import pygame

pygame.init()

WIDTH = 1920
HEIGHT = 1080

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Chula Life")

WIDTH, HEIGHT = pygame.display.get_surface().get_size()
print(f"Screen size: {WIDTH}x{HEIGHT}")
