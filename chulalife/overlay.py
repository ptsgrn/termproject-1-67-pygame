from typing import Dict
from pygame.rect import Rect
from pygame.transform import scale
from pygame.image import load
from .logger import get_logger
from .game_state import game_state
from .screen import screen

logger = get_logger(__name__)


class OverlayObject:
    def __init__(self) -> None:
        self.visible = False
        self.z_index = 0

    def draw(self):
        pass

    def set_visible(self, visible: bool):
        self.visible = visible
        return self


class Heart(OverlayObject):
    def __init__(self, h: int = 100, w: int = 100) -> None:
        super().__init__()
        self.rect = Rect(10, 10, w, h)
        self.visible = True
        self.surface = scale(load("assets/common/heart.png"), self.rect.size)
        self.z_index = 10

    def draw(self):
        if not self.visible:
            return
        if game_state.hearts < 0:
            game_state.hearts = 0
        elif game_state.hearts > 0:
            for i in range(game_state.hearts):
                screen.blit(self.surface, Rect(self.rect.x + i *
                            self.rect.w, self.rect.y, self.rect.w, self.rect.h))

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True


class ScreenOverlay:
    def __init__(self) -> None:
        self.overlay_objects: Dict[str, OverlayObject] = dict()
        self.visible = False
        self.is_fullscreen_open = False

    def draw(self):
        # sort overlay objects by z-index, more z-index means latter draw
        for key in sorted(self.overlay_objects.keys(), key=lambda x: self.overlay_objects[x].z_index):
            self.overlay_objects[key].draw()

    def add(self, key, obj: OverlayObject):
        self.overlay_objects[key] = obj
        return self

    def remove(self, key):
        self.overlay_objects.pop(key, None)
        return self

    def set_visible(self, visible: bool):
        self.visible = visible
        # Set visibility for all overlay objects
        for key in self.overlay_objects:
            self.overlay_objects[key].set_visible(visible)
        return self

    def set_element_visible(self, key, visible):
        if key not in self.overlay_objects:
            logger.error(f"Element {key} not found in overlay")
            return self
        self.overlay_objects[key].set_visible(visible)
        return self

    def set_fullscreen_open(self, open: bool):
        self.is_fullscreen_open = open
        return self

    def has_element(self, key):
        return key in self.overlay_objects

    def set_element(self, key, obj: OverlayObject):
        self.overlay_objects[key] = obj
        return self
