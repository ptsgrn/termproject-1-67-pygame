from dataclasses import dataclass
from typing import Literal

# PyGame imports
import pygame as pg
from pygame.color import Color

# Internal imports
from chulalife.ui_elements import ImageButton
from chulalife.game_state import GameState
from chulalife.background import Background

RESOLUTION = (1200, 900)
FPS = 60

# Colors
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
BLUE = Color(0, 0, 255)

pg.init()


@dataclass
class Player:
    x: float = 0
    y: float = 0
    radius: float = 15
    element_type: Literal["player"] = "player"
    is_game_over: bool = False

    def draw(self, screen):
        pg.draw.circle(
            screen, BLACK, (self.x, self.y), self.radius)

    def update(self, game_objects):
        mouse = pg.mouse.get_pos()
        self.x = mouse[0]
        self.y = mouse[1]
        for go in game_objects:
            if go.element_type == "ball":
                if (go.x - self.x) ** 2 + (go.y - self.y) ** 2 <= (go.radius + self.radius) ** 2:
                    self.is_game_over = True


@dataclass
class GameController:
    interval: int = 1
    next: float = pg.time.get_ticks() + (2 * 1000)
    element_type: str = "controller"
    score: int = 0
    score_text = pg.font.Font(None, 28)

    def update(self):
        pass

    def draw(self, screen):
        pass


class Game:
    def __init__(self) -> None:
        # Init screen
        self.screen = pg.display.set_mode(RESOLUTION, pg.FULLSCREEN)
        self.clock = pg.time.Clock()

        self.state: GameState = GameState.TITLE
        self.level: int = 1

    def run(self):
        while True:
            self.handleEvents()

            screen = self.screen
            if self.state == GameState.QUIT:
                pg.quit()
            elif self.state == GameState.TITLE:
                screen_center = pg.display.get_surface().get_rect().center
                bg = Background(
                    'assets/level/welcome/Start_BG.png', [0, 0])
                screen.blit(bg.image, bg.rect)
                elements = pg.sprite.Group()
                start_button = ImageButton(
                    image_filename="assets/level/welcome/Button_normal.png",
                    hover_file_name="assets/level/welcome/Button_big.png",
                    active_file_name="assets/level/welcome/Button_click.png",
                    hover_scale_factor=1.3,
                    active_scale_factor=1.25,
                    h=200,
                    w=200,
                    x=screen_center[0],
                    # Roughly 2/3 down the screen
                    y=screen_center[1] + screen_center[1] // 2
                )
                elements.add(start_button)
                elements.update()
                elements.draw(screen)

            self.clock.tick(FPS)
            pg.display.flip()

    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
