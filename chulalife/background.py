from typing import List, Optional
import pygame as pg
from pygame.typing import FileLike


class Background(pg.sprite.Sprite):
    def __init__(self, image_file: FileLike, location: List[int]):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self._image = pg.image.load(image_file)
        self._rect = self.image.get_rect()
        self._rect.left, self.rect.top = location

    @property
    def image(self) -> pg.Surface:
        return self._image

    @image.setter
    def image(self, image: pg.surface.Surface):
        if not isinstance(image, pg.Surface):
            raise ValueError("image must be a pygame.Surface")
        self._image = image

    @property
    def rect(self) -> pg.Rect:
        return self._rect

    @rect.setter
    def rect(self, rect: pg.Rect):
        if not isinstance(rect, pg.Rect):
            raise ValueError("rect must be a pygame.Rect")
        self._rect = rect
