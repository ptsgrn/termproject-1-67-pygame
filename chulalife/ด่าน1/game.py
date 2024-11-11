#set up file สำหรับเกมด่านแรก 
import pygame
import input

pygame.init()

#set up screen 
pygame.display.set_caption("Chula life")
screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
clear_color = (30, 150, 50)
running = True

#Gameloop 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            input.keys_down.add(event.key)
        elif event.type == pygame.KEYUP:
            input.keys_down.remove(event.key)
    #Drawcode
    screen.fill(clear_color)

    pygame.display.flip()
pygame.quit()

