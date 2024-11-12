from dataclasses import dataclass
from typing import Literal
import sys

# PyGame imports
import pygame
from pygame.color import Color

# Internal imports
from chulalife.levels import WelcomeScreen

FPS = 60

# Colors
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
BLUE = Color(0, 0, 255)

pygame.init()


# Game Class
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = WelcomeScreen(self)  # Start with the Welcome Screen

    def set_level(self, level):
        self.level = level

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    action = self.level.handle_events(event)
                    if action == "exit":
                        self.running = False

            # Draw the current level or screen
            self.level.draw()

            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
