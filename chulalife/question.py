from .screen import screen, WIDTH, HEIGHT
from pygame.image import load
from pygame.rect import Rect
from .ui_elements import OverlayObject


class Question(OverlayObject):
    def __init__(self, question_id: str) -> None:
        super().__init__()
        if not question_id.startswith("Q"):
            raise ValueError("Question ID must start with 'Q'")
        self.id = question_id
        self.image_file_name = f"assets/scene/text_or_die/question/{
            self.id}.png"
        self.image = load(self.image_file_name)
        self.rect = Rect(0, 0, WIDTH, HEIGHT)

    def draw(self):
        if not self.visible:
            return
        screen.blit(self.image, self.rect)
