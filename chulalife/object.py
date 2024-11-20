import pygame
from pygame.transform import scale
from .color import MAGENTA, ORANGE, GREEN, RED
from .setting import object_debug, warpdoor_debug, character_show_outline
from .screen import screen
from .question import Question
from .logger import get_logger

logger = get_logger(__name__)


class Object(pygame.sprite.Sprite):
    def __init__(self, image_filename, pos, width_height):
        super().__init__()
        self.image = pygame.image.load(
            image_filename).convert_alpha() if image_filename else None
        self.debug = object_debug
        self.debug_color = MAGENTA
        self.pos = pos
        self.width_height = width_height

    def draw(self):
        if self.debug:
            pygame.draw.rect(screen, self.debug_color, self.rect, 2)

    @property
    def rect(self):
        if self.image is None:
            return pygame.rect.Rect(self.pos, self.width_height)
        return self.image.get_rect(topleft=self.pos)


class WarpDoor(Object):
    def __init__(self, pos: tuple[int, int] = (0, 0), width_height: tuple[int, int] = (200, 200), warp_to_scene=0, next_pos=(0, 0), action=None):
        super().__init__(None, pos, width_height)
        self._rect = pygame.rect.Rect(pos, width_height)
        self.warpTarget = warp_to_scene
        self.next_pos_x = next_pos[0]
        self.next_pos_y = next_pos[1]
        self.debug = warpdoor_debug
        self.action = action
        self.surface = pygame.Surface(self._rect.size, pygame.SRCALPHA)

    def draw(self):
        screen.blit(
            self.surface,
            self._rect
        )
        if self.debug:
            pygame.draw.rect(screen, GREEN, self._rect, 2)


class QuestCharacter(Object):
    def __init__(self, charector_name: str, pos: tuple[int, int] = (0, 0), width_height=(250, 250), after_action=None):
        self.debug_color = ORANGE
        self.name = charector_name
        super().__init__(
            f"assets/scene/text_or_die/Character_Q/{charector_name}.png", pos, width_height)
        self.debug = character_show_outline
        self.image = scale(self.image, width_height)
        self.question_id = charector_name.split("_")[0]
        self.question = Question(self.question_id)
        self.done = False
        self.after_action = after_action

    def draw(self):
        super(QuestCharacter, self).draw()
        if self.image is None:
            raise ValueError(
                f"Character image not found: {self.name}")
        if not self.done:
            screen.blit(self.image, self.rect)

    def clear(self):
        self.done = True
        if self.after_action:
            self.after_action()

    @property
    def dialog(self):
        return self.question


class BlockerCharacter(Object):
    def __init__(self, pos: tuple[int, int] = (0, 0), width_height=(250, 250)):
        self.debug_color = RED
        super().__init__(f"assets/scene/text_or_die/Character_Q/blockway.png", pos, width_height)
        self.debug = character_show_outline
        self.image = scale(self.image, width_height)

    def draw(self):
        super(BlockerCharacter, self).draw()
        screen.blit(self.image, self.rect)
