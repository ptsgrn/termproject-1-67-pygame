from typing import List
import pygame
from pygame.typing import FileLike
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from .helper import scale_fit


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file: FileLike, location: List[int]):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self._image = pygame.image.load(image_file)
        self._rect = self.image.get_rect()
        self._rect.left, self.rect.top = location

    @property
    def image(self) -> pygame.Surface:
        return self._image

    @image.setter
    def image(self, image: pygame.surface.Surface):
        if not isinstance(image, pygame.Surface):
            raise ValueError("image must be a pygame.Surface")
        self._image = image

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @rect.setter
    def rect(self, rect: pygame.Rect):
        if not isinstance(rect, pygame.Rect):
            raise ValueError("rect must be a pygame.Rect")
        self._rect = rect
