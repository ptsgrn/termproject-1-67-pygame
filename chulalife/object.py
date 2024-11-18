import pygame
from pygame.transform import scale
from .color import MAGENTA, ORANGE, GREEN
from .setting import object_debug, warpdoor_debug, character_show_outline
from .screen import screen


class Object(pygame.sprite.Sprite):
    def __init__(self, image_filename, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load(
            image_filename).convert_alpha() if image_filename else None
        self.debug = object_debug
        self.debug_color = MAGENTA

    def draw(self):
        if self.debug:
            pygame.draw.rect(screen, self.debug_color, self.rect, 2)

    @property
    def rect(self):
        if self.image is None:
            return pygame.rect.Rect(self.x, self.y, self.w, self.h)
        return self.image.get_rect(topleft=(self.x, self.y))


class WarpDoor(Object):
    def __init__(self, image, x, y, w, h, warpToScene=0, next_pos_x=0, next_pos_y=0):
        super().__init__(None, x, y, w, h)
        self.image = image
        self._rect = pygame.rect.Rect(x, y, w, h)
        self.warpTarget = warpToScene
        self.next_pos_x = next_pos_x
        self.next_pos_y = next_pos_y
        self.debug = warpdoor_debug

    def draw(self):
        screen.blit(
            self.image,
            self._rect
        )
        if self.debug:
            pygame.draw.rect(screen, GREEN, self._rect, 2)


class QuestCharector(Object):
    def __init__(self, charector_name: str, x: int = 0, y: int = 0, w: int = 120, h: int = 120, quest_file_name: str | None = None):
        self.debug_color = ORANGE
        self.name = charector_name
        super().__init__(
            f"assets/scene/text_or_die/Character_Q/{charector_name}.png", x, y, w, h)
        self.debug = character_show_outline
        self.quest_file_name = quest_file_name
        self.image = scale(self.image, (w, h))

    def draw(self):
        super(QuestCharector, self).draw()
        if self.image is None:
            raise ValueError(
                f"Character image not found: {self.name}")
        screen.blit(self.image, self.rect)
