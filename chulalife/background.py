from typing import List, Tuple
import pygame
from pygame.typing import FileLike
from pygame.surface import Surface
from pygame.image import load
from .color import PURPLE
from .setting import background_debug, walkable_debug
from .logger import get_logger
from .screen import screen

logger = get_logger(__name__)


class Background:
    def __init__(self, image_file_name: FileLike, screen=screen) -> None:
        self.bg_image = load(image_file_name)
        self.debug = background_debug
        self.screen = screen

    def draw(self, screen: Surface, offset: List[int] = [0, 0]):
        logger.error("draw method not implemented")

    def add(self, image_file_name: FileLike) -> None:
        # load and merge the image
        self.bg_image = pygame.transform.scale(
            self.bg_image, (self.screen.get_width(), self.screen.get_height()))
        new_image = load(image_file_name)
        new_image = pygame.transform.scale(
            new_image, (self.screen.get_width(), self.screen.get_height()))
        self.bg_image.blit(new_image, (0, 0))


class StaticBackground(Background):
    def __init__(self, image_file_name: FileLike, *image_file_names: FileLike) -> None:
        super().__init__(image_file_name)
        for file_name in image_file_names:
            self.add(file_name)

    def draw(self, screen: Surface, offset: List[int] = [0, 0]):
        self.bg_image = pygame.transform.scale(
            self.bg_image, (screen.get_width(), screen.get_height()))
        screen.blit(self.bg_image, offset)


class WalkableTile:
    def __init__(self, file_name: str) -> None:
        self.debug = walkable_debug
        self.image = load(file_name)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def draw(self, screen: Surface, offset: List[int] = [0, 0]):
        if self.debug:
            mask_surface = self.mask.to_surface(
                setcolor=PURPLE, unsetcolor=(0, 0, 0, 0))
            screen.blit(mask_surface, (self.rect.x +
                                       offset[0], self.rect.y + offset[1]))

    def is_walkable(self, player_mask: pygame.mask.Mask, player_rect: pygame.Rect, offset: Tuple[int, int] = (0, 0)) -> bool:
        # Calculate the offset between the player and tile positions
        mask_offset = (player_rect.x - (self.rect.x + offset[0]),
                       player_rect.y - (self.rect.y + offset[1]))
        return player_mask.overlap(self.mask, mask_offset) is None
