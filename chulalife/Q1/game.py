import pygame 
import input 
from player import Player 
from sprite import sprites 

pygame.init()

pygame.display.set_caption("Chula life")
screen = pygame.display.set_mode((800,600))
clear_color = (30, 150, 50)
running = True
player = Player('chulalife/Q1/images/Rabbit_front.png', 0,0)

#Game Loop 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            input.key_down.add(event.key)
        elif event.type == pygame.KEYUP:
            input.key_down.remove(event.key)
            
    #update code 
    player.update()
    #draw code 
    screen.fill(clear_color)
    for s in sprites:
        s.draw(screen)
    pygame.display.flip()

pygame.quit()