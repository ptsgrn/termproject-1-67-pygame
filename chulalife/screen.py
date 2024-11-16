import pygame

pygame.init()

screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Chula Life")

WIDTH, HEIGHT = pygame.display.get_surface().get_size()
