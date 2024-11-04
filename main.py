import pygame
from pygame.locals import *  # noqa
from pygame.color import Color
from dataclasses import dataclass
from typing import Literal

from chulalife.ui_elements import StaticTextElement, create_surface_with_text

RESOLUTION = (800, 600)
FPS = 60

# Colors
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
BLUE = Color(0, 0, 255)

pygame.init()
# pygame.display.set_caption('')


@dataclass
class Ball:
    x: float = RESOLUTION[0] / 2
    y: float = RESOLUTION[1] / 2
    dx: float = 1
    dy: float = 1
    radius: int = 15
    element_type: Literal["ball"] = "ball"

    def draw(self, screen):
        pygame.draw.circle(
            screen, BLUE, (int(self.x), int(self.y)), self.radius)

    def update(self, game_objects):
        self.x += self.dx
        self.y += self.dy
        if (self.x - self.radius <= 0 or self.x + self.radius >= RESOLUTION[0]):
            self.dx *= -1
        if (self.y - self.radius <= 0 or self.y + self.radius >= RESOLUTION[1]):
            self.dy *= -1


@dataclass
class Player:
    x: float = 0
    y: float = 0
    radius: float = 15
    element_type: Literal["player"] = "player"
    is_game_over: bool = False

    def draw(self, screen):
        pygame.draw.circle(
            screen, BLACK, (self.x, self.y), self.radius)

    def update(self, game_objects):
        mouse = pygame.mouse.get_pos()
        self.x = mouse[0]
        self.y = mouse[1]
        for go in game_objects:
            if go.element_type == "ball":
                if (go.x - self.x) ** 2 + (go.y - self.y) ** 2 <= (go.radius + self.radius) ** 2:
                    self.is_game_over = True


@dataclass
class GameController:
    interval: int = 1
    next: float = pygame.time.get_ticks() + (2 * 1000)
    element_type: str = "controller"
    score: int = 0
    score_text = pygame.font.Font(None, 28)

    def update(self, game_objects):
        if self.next < pygame.time.get_ticks():
            self.next = pygame.time.get_ticks() + (self.interval * 1000)
            game_objects.append(
                Ball(dx=random.random() * 2, dy=random.random()*2))
            self.score += 1

    def draw(self, screen):
        screen.blit(self.score_text.render(
            str(self.score), True, BLACK), (5, 5))


class Game:
    def __init__(self) -> None:
        # Init screen
        self.screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.game_objects: list = [Ball(), Ball(100), Ball(y=200)]
        self.game_objects.append(GameController())
        self.game_objects.append(Player())

        self.state: Literal["welcome", "running",
                            "game_over", "game_end"] = "welcome"
        self.level: int = 1

    def run(self):
        while True:
            self.handleEvents()

            self.screen.fill(WHITE)

            if self.state == "welcome":
                self.screen.fill(WHITE)
                # text_rect = text.get_rect(
                #     center=pygame.display.get_surface().get_rect().center)
                screen_center = pygame.display.get_surface().get_rect().center
                create_surface_with_text(
                    "Welcome to the game", 50, WHITE, BLACK).blit(self.screen, screen_center)
                welcomeText = create_surface_with_text(
                    "ยินดีต้อนรับสู่ Chula life", 50, BLUE, font_type="display")
                self.screen.blit(welcomeText, (screen_center[0], screen_center[1] + 50))
                pygame.display.flip()

            self.clock.tick(FPS)
            pygame.display.flip()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
