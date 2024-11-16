import sys
import pygame

# Internal imports
from .levels import WelcomeScreen, Level, LevelOne

FPS = 60

pygame.init()


# Game Class
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        # Start with the Welcome Screen
        self.level: Level = WelcomeScreen(self)
        # self.level: Level = LevelOne(self)

    def set_level(self, level: Level):
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
