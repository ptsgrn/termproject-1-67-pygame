import pygame
import time
from typing import Literal
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.typing import FileLike
from pygame.transform import scale_by
from pygame.image import load

# Internal imports
from .helper import scale_fit
from .color import BLACK
from .screen import WIDTH
from .logger import get_logger

logger = get_logger(__name__)

font_paths = {
    "display": "assets/fonts/2005_iannnnnCPU.ttf",
    "content": "assets/fonts/2005_iannnnnAMD.ttf",
}


def get_font_pathname(font_type: Literal["display", "content"]) -> str:
    """
    Get the font file pathname based on the specified font type.

    Args:
        font_type (Literal["display", "content"]): The type of font to retrieve.
            Must be either "display" or "content".

    Returns:
        str: The file path to the requested font.

    Raises:
        ValueError: If the specified font_type is not found in font_paths.
    """
    if font_type not in font_paths:
        raise ValueError("Invalid font")
    return font_paths[font_type]


def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None, font_type: Literal["display", "content"] = "content"):
    """Create a new pygame Surface with rendered text.

    This function creates a new Surface with the specified text rendered using the chosen font.

    Args:
        text (str): The text to render
        font_size (int): Size of the font in pixels
        text_rgb (tuple): RGB color tuple for the text (e.g. (255, 255, 255) for white)
        bg_rgb (tuple, optional): RGB color tuple for the background. Defaults to None for transparent.
        font_type (Literal["display", "content"], optional): Type of font to use - either "display" or "content". 
            Defaults to "content".

    Returns:
        pygame.Surface: A new Surface with the rendered text, converted to include alpha channel

    Example:
        >>> text_surface = create_surface_with_text("Hello", 32, (255, 255, 255))
    """
    """ Returns surface with text written on """
    font = pygame.font.Font(font_paths[font_type], size=int(font_size))
    surface = font.render(text=text, antialias=True,
                          color=text_rgb, background=bg_rgb)
    return surface.convert_alpha()


class BaseButton(Sprite):
    """A base class for clickable button sprites in Pygame.

    This class provides basic button functionality including click detection and action execution.

    Attributes:
        rect (pygame.Rect): The rectangular area defining the button's position and size
        action (callable): Function to be called when button is clicked
        clicked (bool): Current button state - True if being clicked, False otherwise

    Args:
        x (int): X-coordinate of button's top-left corner
        y (int): Y-coordinate of button's top-left corner
        w (int): Width of the button in pixels
        h (int): Height of the button in pixels 
        action (callable): Function to execute when button is clicked

    Methods:
        update(events): Updates button state based on mouse events
        is_clicked(mouse_pos): Checks if given position collides with button
    """

    def __init__(self, x, y, w, h, action):
        self.rect = Rect(x, y, w, h)
        self.action = action
        self.clicked = False

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.clicked:
                        self.action()
                    self.clicked = False
        else:
            self.clicked = False

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class ImageButton(BaseButton):
    """
    A button class that displays different images based on mouse interaction.

    This button class inherits from _BaseButton and displays three different image states:
    - Default state: Shows the default image
    - Hover state: Shows hover image with optional scaling when mouse hovers over
    - Active state: Shows active image with optional scaling when mouse clicks

    Args:
        x (int): X-coordinate position of the button
        y (int): Y-coordinate position of the button
        w (int): Width of the button
        h (int): Height of the button
        image_filename (str): Filepath to the default state image
        hover_file_name (str): Filepath to the hover state image  
        active_file_name (str): Filepath to the active/clicked state image
        hover_scale_factor (float): Scale factor to apply to hover image (e.g. 1.1 for 10% larger)
        active_scale_factor (float): Scale factor to apply to active image
        action (callable): Function to call when button is clicked

    Methods:
        draw(screen): Draws the appropriate button state image based on mouse interaction
    """

    def __init__(self, x: int, y: int, w: float, h: float, image_filename: str, hover_file_name: str, active_file_name: str, hover_scale_factor: float, active_scale_factor: float, action):
        self._default_image = load(image_filename).convert_alpha()

        super().__init__(x, y, w, h, action)

        w = w or self._default_image.get_width()
        h = h or self._default_image.get_height()
        default_rect = Rect(x, y, w, h)
        default_rect.center = (x, y)

        self._default_image, self._rect = scale_fit(
            self._default_image, default_rect)
        self._hover_image = self.scalable_surface(
            hover_file_name, hover_scale_factor, default_rect)
        self._active_image = self.scalable_surface(
            active_file_name, active_scale_factor, default_rect)
        self.hover_scale_factor = hover_scale_factor
        self.active_scale_factor = active_scale_factor

        self.mouse_over = False
        self.mouse_down = False

        self._image = self._default_image

    @property
    def image(self):
        if self.mouse_over and self.mouse_down and self._active_image:
            return self._active_image
        if self.mouse_over and self._hover_image:
            return self._hover_image
        return self._default_image

    @image.setter
    def image(self, image):
        self._image = image

    @property
    def rect(self):
        if self.mouse_over and self._hover_image:
            return self._hover_image.get_rect(center=self._rect.center)
        if self.mouse_over and self.mouse_down and self._active_image:
            return self._active_image.get_rect(center=self._rect.center)
        return self._default_image.get_rect(center=self._rect.center)

    @rect.setter
    def rect(self, rect):
        self._rect = rect

    def draw(self, screen: pygame.Surface):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mouse_over = True
            if pygame.mouse.get_pressed()[0]:
                self.mouse_down = True
            else:
                self.mouse_down = False
        else:
            self.mouse_over = False
            self.mouse_down = False

        if self.mouse_down and self._active_image:
            self.image = scale_by(self._active_image, self.active_scale_factor)
        elif self.mouse_over and self._hover_image:
            self.image = scale_by(self._hover_image, self.hover_scale_factor)
        else:
            self.image = self._default_image
        screen.blit(self.image, self.rect)

    def scalable_surface(self, filename: FileLike | None, scale_factor: float, rect: Rect):
        return scale_fit(
            load(
                filename).convert_alpha(),
            Rect(rect.x, rect.y, int(rect.h*scale_factor),
                 int(rect.w*scale_factor))
        )[0] if filename else scale_by(self._default_image, scale_factor)


class TextObject:
    def __init__(self, text: str,  pos: tuple[int, int] = (0, 0), color=BLACK, font: Literal["content", "display"] = "content", font_size: int = 36, cursor: bool = False):
        self.font = pygame.font.Font(get_font_pathname(font), font_size)
        self.color = color
        self.x = pos[0]
        self.y = pos[1]
        self.cursor = cursor
        self.update_text(text)
        self.cursor_visible = True
        self.cursor_last_switch = time.time()

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.rendered_text, self.rect)
        if self.cursor and self.cursor_visible:
            cursor_rect = pygame.Rect(
                self.rect.topright, (5, self.rect.height))
            pygame.draw.rect(screen, self.color, cursor_rect)

    def update_text(self, new_text):
        self.text = new_text
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = self.rendered_text.get_rect(center=(WIDTH // 2, self.y))

    def update_cursor(self):
        if self.cursor and time.time() - self.cursor_last_switch > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_last_switch = time.time()
