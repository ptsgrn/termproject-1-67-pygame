import pygame 
import input 

pygame.init()

pygame.display.set_caption("Chula life")
screen = pygame.display.set_mode((800,600))
clear_color = (30, 150, 50)
running = True

#Game Loop 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pyagme.KEYDOWN:
            input.key_down.add(event.key)
        elif event.type == pyagme.KEYUP:
            input.key_down.remove(event.key)
            
    
    #draw code 
    screen.fill(clear_color)

    pygame.display.flip()

pygame.quit()