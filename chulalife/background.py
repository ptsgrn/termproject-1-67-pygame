from typing import List
import pygame
from pygame.typing import FileLike
from pygame.surface import Surface
from pygame.image import load

from .helper import scale_fit


class StaticBackground:
    def __init__(self, image_file_name: FileLike, screen: Surface, *groups):
        self.bg_image, self.bg_rect = scale_fit(
            load(image_file_name), screen.get_rect())
        screen.blit(self.bg_image, self.bg_rect)
