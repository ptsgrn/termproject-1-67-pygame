import sys
import pygame
from .elements import ScreenOverlay, Heart
from .levels import WelcomeScreen, Level, EndScreen
from .game_state import game_state

FPS = 60

pygame.init()


# Game Class
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        # Start with the Welcome Screen
        self.level: Level = WelcomeScreen(self)
        self.overlay: ScreenOverlay = ScreenOverlay()
        self.overlay.add("hearts", Heart())

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
            if game_state.hearts == 0:
                self.set_level(EndScreen(self))

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
