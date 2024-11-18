import pygame
from pygame.color import Color


BLUE = Color(0, 0, 255)
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
GREEN = Color(0, 255, 0)
RED = Color(255, 0, 0)
YELLOW = Color(255, 255, 0)
PURPLE = Color(128, 0, 128)
MAGENTA = Color(255, 0, 255)
ORANGE = Color(255, 165, 0)

colors = [BLUE, WHITE, BLACK, GREEN, RED, YELLOW, PURPLE, MAGENTA, ORANGE]

if __name__ == "__main__":
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    colors = sorted(colors, key=lambda c: c.hsva)
    block_size = 100

    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        title_font = pygame.font.Font("assets/fonts/2005_iannnnnCPU.ttf", 40)
        screen.blit(title_font.render("Color Sample", True, BLACK), (20, 15))
        for r, top in enumerate(range(80, HEIGHT, block_size + 20)):
            for c, left in enumerate(range(0, WIDTH, block_size + 10)):
                if r * (WIDTH // (block_size + 10)) + c >= len(colors):
                    break
                color = colors[r * (WIDTH // (block_size + 10)) + c]
                pygame.draw.rect(
                    screen, color, (left, top + 20, block_size, block_size))
                font = pygame.font.Font("assets/fonts/2005_iannnnnAMD.ttf", 22)
                text = font.render(str(color), True, BLACK)
                screen.blit(text, (left + 5, top + block_size + 20))

        pygame.display.flip()
        pygame.time.Clock().tick(1)
