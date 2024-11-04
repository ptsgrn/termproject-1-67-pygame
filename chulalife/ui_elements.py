from typing import Literal
import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.color import Color

BLUE = Color(0, 0, 255)
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)

font_paths = {
    "display": "assets/fonts/2005_iannnnnCPU.ttf",
    "content": "assets/fonts/2005_iannnnnAMD.ttf",
}


def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None, font_type: Literal["display", "content"] = "content"):
    """ Returns surface with text written on """
    # font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    font = pygame.font.Font(font_paths[font_type], size=int(font_size))
    surface = font.render(text=text, antialias=True,
                          color=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
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

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
        else:
            self.mouse_over = False

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


def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (800, 600), pygame.FULLSCREEN | pygame.RESIZABLE)

    # create a ui element
    static_text_element = StaticTextElement(
        center_position=(400, 400),
        font_size=72,
        bg_rgb=None,
        text_rgb=BLUE,
        text="Hello World",
    )

    # create a ui element
    ui_element = UIElement(
        center_position=(400, 450),
        font_size=30,
        bg_rgb=None,
        text_rgb=BLUE,
        text="Hello World",
    )

    # main loop
    while True:
        screen.fill(WHITE)
        static_text_element.update()
        static_text_element.draw(screen)

        ui_element.update(pygame.mouse.get_pos())
        ui_element.draw(screen)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


# call main when the script is run
if __name__ == "__main__":
    main()
