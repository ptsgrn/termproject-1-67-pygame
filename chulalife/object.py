import pygame
from .color import MAGENTA, GREEN


class Object(pygame.sprite.Sprite):
    def __init__(self, image_filename, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load(image_filename).convert_alpha(
        ) if isinstance(image_filename, str) else image_filename
        self._mask = pygame.mask.from_surface(self.image)
        self.debug = False
        self.__debug_color = MAGENTA

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, pygame.Rect(self.x, self.y,
                    self.w or self.image.get_width(), self.h or self.image.get_height()))
        if self.debug:
            pygame.draw.rect(screen, self.__debug_color, self.rect, 2)

    def update(self):
        pass

    @property
    def rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))

    @property
    def mask(self):
        return self._mask


class ForegroundWalkable(Object):
    def __init__(self, image_filename, x, y, w, h):
        super().__init__(image_filename, x, y, w, h)
        self._mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


class WarpDoor(Object):
    def __init__(self, image_filename, x, y, w, h, warpToScene=0, next_pos_x=0, next_pos_y=0):
        super().__init__(image_filename, x, y, w, h)
        self._rect = pygame.rect.Rect(x, y, w, h)
        self.warpTarget = warpToScene
        self.next_pos_x = next_pos_x
        self.next_pos_y = next_pos_y

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(
            self.image,
            self._rect
        )
        if self.debug:
            pygame.draw.rect(screen, GREEN, self._rect, 2)
