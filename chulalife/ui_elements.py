from typing import Literal
import pygame
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.color import Color
from pygame.typing import FileLike
from pygame.transform import scale_by
from pygame.image import load
from pygame.surface import Surface

# Internal imports
if __name__ == "__main__":
    from helper import scale_fit
else:
    from .helper import scale_fit

BLUE = Color(0, 0, 255)
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)

font_paths = {
    "display": "assets/fonts/2005_iannnnnCPU.ttf",
    "content": "assets/fonts/2005_iannnnnAMD.ttf",
}


def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None, font_type: Literal["display", "content"] = "content"):
    """ Returns surface with text written on """
    font = pygame.font.Font(font_paths[font_type], size=int(font_size))
    surface = font.render(text=text, antialias=True,
                          color=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class TextButton(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
        """
        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        # calls the init method of the parent sprite class
        super().__init__()

        # properties that vary the image and its rect when the mouse is over the element

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self):
        self.mouse_over = self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)


class StaticTextElement(Sprite):
    """ An user interface element that can be added to a surface
    source: https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
    """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb):
        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # add both images and their rects to lists
        self.images = [default_image]
        self.rects = [
            default_image.get_rect(center=center_position),
        ]

        # calls the init method of the parent sprite class
        super().__init__()

   # properties that vary the image and its rect when the mouse is over the element

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self):
        pass

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)


class ImageButton(Sprite):
    """
    A class representing an image button with different states (default, hover, active).

    Attributes:
        mouse_over (bool): Indicates if the mouse is over the button.
        mouse_down (bool): Indicates if the mouse button is pressed down on the button.
        default_image (Surface): The default image of the button.
        _rect (Rect): The rectangle defining the button's position and size.
        _active_image (Surface): The image of the button when it is active.
        _hover_image (Surface): The image of the button when it is hovered over.
        images (list): A list of images used for different button states.
        action (callable): The action to be performed when the button is clicked.

    Methods:
        scalable_surface(filename, scale_factor, rect):
            Scales the surface of the image based on the provided scale factor and rectangle.

        image():
            Returns the current image of the button based on its state.

        rect():
            Returns the current rectangle of the button based on its state.

        update():
            Updates the state of the button based on mouse interactions.

        draw(surface):
            Draws the button on the provided surface.
    """

    def __init__(self, image_filename: FileLike, x: int = 0, y: int = 0, h: int | None = None, w: int | None = None, hover_file_name=None, active_file_name=None,
                 action=None, hover_scale_factor: float = 1.1, active_scale_factor: float = 0.05):

        self.mouse_over = False
        self.mouse_down = False

        self.default_image = load(image_filename).convert_alpha()
        w = w or self.default_image.get_width()
        h = h or self.default_image.get_height()
        default_rect = Rect(x, y, w, h)
        default_rect.center = (x, y)
        self.default_image, self._rect = scale_fit(
            self.default_image, default_rect)

        self._active_image = self.scalable_surface(
            active_file_name, active_scale_factor, rect=default_rect)
        self._hover_image = self.scalable_surface(
            hover_file_name, hover_scale_factor, rect=default_rect)
        self.images = [self.default_image,
                       self._hover_image, self._active_image]
        self.images = [image for image in self.images if image]

        self.action = action

        super().__init__()

    def scalable_surface(self, filename: FileLike | None, scale_factor: float, rect: Rect):
        return scale_fit(
            load(
                filename).convert_alpha(),
            Rect(rect.x, rect.y, int(rect.h*scale_factor),
                 int(rect.w*scale_factor))
        )[0] if filename else scale_by(self.default_image, scale_factor)

    @property
    def image(self):
        if self.mouse_over and self.mouse_down and self._active_image:
            return self._active_image
        if self.mouse_over and self._hover_image:
            return self._hover_image
        return self.default_image

    @property
    def rect(self):
        if self.mouse_over and self._hover_image:
            return self._hover_image.get_rect(center=self._rect.center)
        if self.mouse_over and self.mouse_down and self._active_image:
            return self._active_image.get_rect(center=self._rect.center)
        return self.default_image.get_rect(center=self._rect.center)

    def update(self):
        self.mouse_over = self.rect.collidepoint(pygame.mouse.get_pos())
        self.mouse_down = pygame.mouse.get_pressed()[0]
        if self.mouse_over and self.mouse_down and self.action:
            return self.action

    def draw(self, surface: Surface):
        surface.blit(self.image, self.rect)


def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (800, 600), pygame.RESIZABLE)

    image_button = ImageButton(
        x=400,
        y=300,
        h=100,
        w=100,
        image_filename="assets/level/welcome/Button_normal.png",
        hover_file_name="assets/level/welcome/Button_big.png",
        active_file_name="assets/level/welcome/Button_click.png",
        hover_scale_factor=1.3,
        active_scale_factor=1.2,
    )

    # create a ui element
    ui_element = TextButton(
        center_position=(400, 450),
        font_size=30,
        bg_rgb=None,
        text_rgb=BLUE,
        text="Hello World",
    )

    # main loop
    while True:
        screen.fill(WHITE)
        elements = pygame.sprite.Group()
        elements.add(image_button)
        # elements.add(ui_element)
        elements.update()
        elements.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


# call main when the script is run
if __name__ == "__main__":
    main()
