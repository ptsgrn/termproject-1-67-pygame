#set up file สำหรับเกมด่านแรก 
import pygame
import input
from player import Player 
from sprite import sprites 



pygame.init()

#set up screen 
pygame.display.set_caption("Chula life")
screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
clear_color = (30, 150, 50)
running = True
player = Player("images/player.png", 400, 300)

#Gameloop 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            input.keys_down.add(event.key)
        elif event.type == pygame.KEYUP:
            input.keys_down.remove(event.key)

    #update Code
    player.update()

    #Drawcode
    screen.fill(clear_color)
    for s in sprites:
        s.draw(screen)

    pygame.display.flip()
pygame.quit()

