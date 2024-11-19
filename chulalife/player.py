import pygame
from pygame.surface import Surface
from typing import Literal
from .color import BLUE, WHITE, PURPLE, GREEN
from .helper import scale_fit
from .screen import WIDTH, HEIGHT, screen
from .setting import player_debug, show_player_position, player_speed
from .background import WalkableTile
from .logger import get_logger

logger = get_logger(__name__)


class Player(pygame.sprite.Sprite):
    def __init__(self, init_pos: tuple[int, int], width_height: tuple[int, int] = (225, 225)):
        super().__init__()
        self._image = pygame.Surface((40, 40))
        self.speed = player_speed
        self.facing: Literal['down', 'up', 'left', 'right'] = "down"
        self._rect = pygame.Rect(init_pos, width_height)
        self.__facing_image = {
            "up": self.load_image_fit_rect("assets/characters/bunny/face-up.png"),
            "down": self.load_image_fit_rect("assets/characters/bunny/face-down.png"),
            "left": self.load_image_fit_rect("assets/characters/bunny/face-left.png"),
            "right": self.load_image_fit_rect("assets/characters/bunny/face-right.png"),
        }
        self.walkable_mask: WalkableTile | None = None
        self.debug = player_debug

    def load_image_fit_rect(self, filename):
        image = pygame.image.load(filename).convert_alpha()
        return scale_fit(image, self._rect)[0]

    def draw(self, screen):
        if show_player_position:
            logger.debug(f"Player position: {self.rect.topleft}")
        screen.blit(self.image, self.rect)
        if self.debug:
            pygame.draw.rect(screen, BLUE, self.rect, 2)

    def move(self, dx, dy):
        # Calculate new potential position for feet and upper body
        new_rect = self.rect.move(dx, dy)
        if not self.is_within_walkable_mask():
            return

        if self.is_within_screen(screen, new_rect):
            self.rect = new_rect
        else:
            self.rect.left = max(
                0, min(screen.get_width() - self.rect.width, self.rect.left))
            self.rect.top = max(
                0, min(screen.get_height() - self.rect.height, self.rect.top))

    def is_within_screen(self, screen: pygame.surface.Surface, new_rect: pygame.rect.Rect) -> bool:
        return new_rect.left >= 0 and new_rect.right <= screen.get_width() and new_rect.top >= 0 and new_rect.bottom <= screen.get_height()

    def is_within_walkable_mask(self):
        if self.walkable_mask is None:
            return True
        return self.walkable_mask.is_walkable(pygame.mask.Mask((self.rect.w, 10)), self.rect)

    @property
    def foot_rect(self):
        foot_rect = pygame.rect.Rect(
            self.rect.left, self.rect.bottom - 10, self.rect.width, 10)

        if self.debug:
            pygame.draw.rect(screen, GREEN, foot_rect, 2)

        return foot_rect

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.facing = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.facing = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.facing = "down"
        self.move(dx, dy)

    @property
    def image(self):
        self._rect.width = self.__facing_image[self.facing].get_width()
        self._rect.height = self.__facing_image[self.facing].get_height()
        return self.__facing_image[self.facing]

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value: pygame.rect.Rect):
        self._rect = value


if __name__ == "__main__":
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player((100, 100))
    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        player.handle_keys()
        player.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
