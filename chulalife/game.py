import sys
import pygame

from .overlay import ScreenOverlay, Heart
from .levels import Level, GameOver, WelcomeScreen
from .game_state import game_state
from .setting import music_volume, background_music, FPS

pygame.init()
pygame.mixer.init()


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
        # Setting up the game
        self.setup()

        # Game loop
        while self.running:
            events = pygame.event.get()
            self.level.events = events
            for event in events:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                else:
                    action = self.level.handle_events(event)
                    if action == "exit":
                        self.running = False
            if game_state.hearts == 0:
                self.set_level(GameOver(self))

            # Draw the current level or screen
            self.level.draw()

            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def setup(self):
        pygame.mixer_music.set_volume(music_volume)
        pygame.mixer_music.load(background_music)
        pygame.mixer_music.play(-1)


if __name__ == "__main__":
    game = Game()
    game.run()
