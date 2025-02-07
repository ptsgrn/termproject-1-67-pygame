import pygame
import pygame.event
from typing import Literal
from pygame.image import load
from pygame.rect import Rect
from .screen import screen, WIDTH, HEIGHT
from .elements import TextObject
from .overlay import OverlayObject
from .setting import charector_interaction
from .logger import get_logger
from .color import BLACK, RED
from .game_state import game_state

logger = get_logger(__name__)

answers = {
    "Q1": "UNIVERSITY",
    "Q2": "SCIENCE",
    "Q3": "COMPUTER",
    "Q4": "MATHEMATICS",
    "Q5": "PROFESSOR",
    "Q6": "CALCULUS",
    "Q7": "LABORATORY",
    "Q8": "BUS-STOP",
    "Q9": "LIBRARY",
    "Q10": "EXAMINATION",
    "Q11": "WITHDRAW",
}


class Question(OverlayObject):
    def __init__(self, question_id: str) -> None:
        super().__init__()
        self.z_index = 5
        if not question_id.startswith("Q"):
            raise ValueError("Question ID must start with 'Q'")
        self.id = question_id
        self.image_file_name = f"assets/scene/text_or_die/question/{
            self.id}.png"
        self.image = load(self.image_file_name)
        self.rect = Rect(0, 0, WIDTH, HEIGHT)
        self.is_disabled = not charector_interaction
        self.typed_word = ""
        self.correct_word = answers[self.id]
        self.text_input = TextObject(
            self.typed_word, (0, HEIGHT // 2 + HEIGHT // 4 - 28), BLACK, "content", 100, True)
        self.notify_text = ""
        self.notify = TextObject(
            "", (0, HEIGHT // 2 + HEIGHT // 4 + 50), RED, "display", 52)
        self.status: Literal["active", "done"] = "active"

    def draw(self):
        if not self.visible:
            return
        if self.is_disabled:
            logger.warning(
                "Question is disabled by charector_no_interaction setting")
            return
        self.handle_events()
        self.text_input.update_text(self.typed_word)
        self.text_input.update_cursor()
        screen.blit(self.image, self.rect)
        self.notify.update_text(self.notify_text)
        if self.notify_text and self.typed_word == "":
            self.notify.draw(screen)
        self.text_input.draw(screen)
        if self.status == "done":
            self.notify_text = ""
            pygame.time.wait(500)

    def check_answer(self):
        if self.typed_word == self.correct_word:
            return True
        return False

    def handle_events(self):
        logger.info(f"Event: {self.events}")
        for event in self.events:
            if not self.visible or self.is_disabled:
                return
            if event.type == pygame.KEYDOWN:
                logger.info(f"Event: {event}")
                if event.key == pygame.K_BACKSPACE:
                    self.typed_word = self.typed_word[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.typed_word == "":
                        return
                    if not self.check_answer():
                        game_state.hearts -= 1
                        self.typed_word = ""
                        self.notify_text = f"Incorrect word! {
                            game_state.hearts} hearts left"
                    else:
                        self.notify_text = "Yes Correct!!!"
                        self.status = "done"
                        self.typed_word = ""
                elif event.unicode.isalpha() or event.unicode == "-":
                    self.typed_word += event.unicode.upper()
