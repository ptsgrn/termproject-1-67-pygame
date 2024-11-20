from typing import List, Tuple
import pygame
from pygame.typing import FileLike
from pygame.surface import Surface
from pygame.image import load
from .color import PURPLE, GREEN
from .setting import background_debug, walkable_debug, walkable_tile_interactions
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
    def __init__(self, blocked_way_rects: List[pygame.rect.RectType] = [], walkable_way_rects: List[pygame.rect.RectType] = []) -> None:
        self.debug = walkable_debug
        self.blocked_way_rects: list[pygame.rect.Rect] = blocked_way_rects
        self.walkable_way_rects: list[pygame.rect.Rect] = walkable_way_rects

    def draw(self):
        if self.debug:
            for rect in self.blocked_way_rects:
                pygame.draw.rect(screen, PURPLE, rect, 5)
            for rect in self.walkable_way_rects:
                pygame.draw.rect(screen, GREEN, rect, 5)

    def is_walkable(self, player_rect: pygame.Rect) -> bool:
        if not walkable_tile_interactions:
            return True
        is_collided = False
        for rect in self.blocked_way_rects:
            if player_rect.colliderect(rect):
                is_collided = True
                break
        for rect in self.walkable_way_rects:
            if player_rect.colliderect(rect):
                is_collided = False
                break
        return not is_collided

    def add_blocked_way(self, *rect: pygame.rect.Rect):
        self.blocked_way_rects.extend(rect)
        return self
    
    def add_walkable_way(self, *rect: pygame.rect.Rect):
        self.walkable_way_rects.extend(rect)
        return self
