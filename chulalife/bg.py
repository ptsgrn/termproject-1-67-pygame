import pygame

pygame.init()

pygame.display.set_caption("Chula life")
screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
clear_color = (30, 150, 50)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #draw code
    screen.fill(clear_color)

    pygame.display.flip
pygame.quit()
