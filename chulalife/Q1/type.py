import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up display for fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Text or Die")

# Load and scale background image
bg_image = pygame.image.load("assets/scene/text_or_die/textordie_time.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

# Set up fonts
font_path = "assets/fonts/2005_iannnnnAMD.ttf"
font = pygame.font.Font(font_path, 74)
small_font = pygame.font.Font(font_path, 36)

# TextObject class
class TextObject:
    def __init__(self, text, font, color, y, cursor=False):
        self.font = font
        self.color = color
        self.y = y
        self.cursor = cursor
        self.update_text(text)
        self.cursor_visible = True
        self.cursor_last_switch = time.time()

    def draw(self, screen):
        screen.blit(self.rendered_text, self.rect)
        if self.cursor and self.cursor_visible:
            cursor_rect = pygame.Rect(self.rect.topright, (3, self.rect.height))
            pygame.draw.rect(screen, self.color, cursor_rect)

    def update_text(self, new_text):
        self.text = new_text
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect = self.rendered_text.get_rect(center=(WIDTH // 2, self.y))

    def update_cursor(self):
        if self.cursor and time.time() - self.cursor_last_switch > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_last_switch = time.time()

# Game variables
correct_word = "PYTHON"
typed_word = ""
result_message = ""

# Create TextObjects
typed_word_text = TextObject(typed_word, font, (0, 0, 0), 400, cursor=True)  # Changed y position to 400
result_text = TextObject(result_message, small_font, (255, 0, 0), 300)

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(bg_image, (0, 0))
    
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                typed_word = typed_word[:-1]
            elif event.key == pygame.K_RETURN:
                if typed_word == correct_word:
                    result_message = "You win!"
                else:
                    result_message = "Incorrect word!"
                typed_word = ""
            else:
                typed_word += event.unicode.upper()
    
    # Update TextObjects
    typed_word_text.update_text(typed_word)
    result_text.update_text(result_message)
    
    # Update cursor visibility
    typed_word_text.update_cursor()
    
    # Draw TextObjects
    typed_word_text.draw(screen)
    result_text.draw(screen)
    
    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()