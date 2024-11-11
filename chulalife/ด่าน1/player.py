import pygame 
from sprite import Sprite
from input import is_key_pressed

class Player(image):
    def _init_(self, image, x, y):
        super()._init_(image, x, y)
        self.movement_speed = 2
    
    def updete(self):
        if is_key_pressed(pygame.K_w):
            self.y -= self.movement_speed
        if is_key_pressed(pygame.K_a):
            self.x -= self.movement_speed
        if is_key_pressed(pygame.k_s):
            self.y += self.movement_speed
        if is_key_pressed(pygame.K_d):
            self.x += self.movement_speed
            super().updete()


