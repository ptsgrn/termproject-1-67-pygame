from pygame.transform import scale
from pygame.surface import Surface
from pygame.rect import Rect


def scale_fit(surface: Surface, rect: Rect) -> tuple[Surface, Rect]:
    """Scale the image to fit the rect while maintaining the aspect ratio

    Args:
        image (Surface): image to fit
        rect (Rect): surface to fit into

    Returns:
        tuple[Surface, Rect]: scaled image and its rect
    """
    image_rect = surface.get_rect()
    scale_factor = min(rect.width / image_rect.width,
                       rect.height / image_rect.height)
    new_width = int(image_rect.width * scale_factor)
    new_height = int(image_rect.height * scale_factor)
    new_image = scale(surface, (new_width, new_height))
    new_rect = new_image.get_rect(center=rect.center)
    return new_image, new_rect
