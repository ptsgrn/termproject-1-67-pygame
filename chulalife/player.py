import pygame
from typing import Literal
from .color import BLUE, WHITE


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
    def __init__(self, init_x: int, init_y: int, w: int = 40, h: int = 40, speed=5):
        self.rect = pygame.Rect(init_x, init_y, w, h)
        self._image = pygame.Surface((40, 40))
        self.speed = 5
        self.facing: Literal['down', 'up', 'left', 'right'] = "down"
        self.__facing_image = {
            "up": self.load_image_fit_rect("assets/characters/bunny/face-up.png"),
            "down": self.load_image_fit_rect("assets/characters/bunny/face-down.png"),
            "left": self.load_image_fit_rect("assets/characters/bunny/face-left.png"),
            "right": self.load_image_fit_rect("assets/characters/bunny/face-right.png"),
        }

    def load_image_fit_rect(self, filename):
        image = pygame.image.load(filename).convert_alpha()
        return pygame.transform.scale(image, self.rect.size)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

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
        return self.__facing_image[self.facing]


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
