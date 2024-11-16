from typing import List
import pygame
from pygame.typing import FileLike
from pygame.surface import Surface
from pygame.image import load


class StaticBackground:
    def __init__(self, image_file_name: FileLike, *groups):
        self.bg_image = load(image_file_name)

    def draw(self, screen: Surface, offset: List[int] = [0, 0]):
        self.bg_image = pygame.transform.scale(
            self.bg_image, (screen.get_width(), screen.get_height()))
        screen.blit(self.bg_image, offset)
