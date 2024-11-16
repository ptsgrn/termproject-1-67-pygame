import pygame
from typing import Literal
from .color import BLUE, WHITE
from .helper import scale_fit
from .screen import WIDTH, HEIGHT, screen


class PlayerFactory:
    def __init__(self):
        self.players = []

    def create(self, x, y):
        player = Player(x, y)
        self.players.append(player)
        return player

    def draw(self, screen):
        for player in self.players:
            player.draw(screen)

    def handle_keys(self):
        for player in self.players:
            player.handle_keys()

    def update(self):
        for player in self.players:
            player.update()

    def remove(self, player):
        self.players.remove(player)


class Player:
    def __init__(self, init_x: int, init_y: int, w: int = 40, h: int = 40, speed=10):
        self._image = pygame.Surface((40, 40))
        self.speed = speed
        self.facing: Literal['down', 'up', 'left', 'right'] = "down"
        self._rect = pygame.Rect(init_x, init_y, w, h)
        self.__facing_image = {
            "up": self.load_image_fit_rect("assets/characters/bunny/face-up.png"),
            "down": self.load_image_fit_rect("assets/characters/bunny/face-down.png"),
            "left": self.load_image_fit_rect("assets/characters/bunny/face-left.png"),
            "right": self.load_image_fit_rect("assets/characters/bunny/face-right.png"),
        }
        image_ratio = self.image.get_width() / self.image.get_height()
        self.walkable_mask: pygame.mask.Mask | None = None
        self.debug = False

    def load_image_fit_rect(self, filename):
        image = pygame.image.load(filename).convert_alpha()
        return scale_fit(image, self._rect)[0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.debug:
            pygame.draw.rect(screen, BLUE, self.rect, 2)

    def move(self, dx, dy, walkable_mask: pygame.mask.Mask | None):
        # Calculate new potential position for feet and upper body
        new_rect = self.rect.move(dx, dy)

        # upper_body_rect = pygame.Rect(
        #     new_rect.left, new_rect.top, new_rect.width, int(
        #         new_rect.height * 0.7)
        # )  # Upper body collision area

        # if walkable_mask is None or (walkable_mask.get_at(feet_pos) and not self._upper_body_collision(upper_body_rect, walkable_mask)):
        #     self.rect = new_rect
        # if walkable_mask.overlap_area(pygame.mask.Mask((player.width, player.height), True), (new_x, new_y)) == player.width * player.height:
        #     player.x, player.y = new_x, new_y
        # if walkable_mask is None or walkable_mask.overlap_area(self.mask, (new_rect.x, new_rect.y)) == self.rect.width * self.rect.height:
        #     self.rect = new_rect
        # if walkable_mask is None or walkable_mask.get_at(feet_pos):

        # เดี๋ยวค่อยมาแก้เรื่องการชนขอบ
        if self.is_within_screen(screen, new_rect):
            self.rect = new_rect
        else:
            self.rect.left = max(
                0, min(screen.get_width() - self.rect.width, self.rect.left))
            self.rect.top = max(
                0, min(screen.get_height() - self.rect.height, self.rect.top))

    def is_within_screen(self, screen: pygame.surface.Surface, new_rect: pygame.rect.Rect) -> bool:
        return new_rect.left >= 0 and new_rect.right <= screen.get_width() and new_rect.top >= 0 and new_rect.bottom <= screen.get_height()

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
        self.move(dx, dy, self.walkable_mask)

    @property
    def image(self):
        self._rect.width = self.__facing_image[self.facing].get_width()
        self._rect.height = self.__facing_image[self.facing].get_height()
        return self.__facing_image[self.facing]

    @property
    def mask(self):
        # create a mask from the image with cropped feet

        return pygame.mask.Mask((40, 40))

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
    player = Player(100, 100)
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
