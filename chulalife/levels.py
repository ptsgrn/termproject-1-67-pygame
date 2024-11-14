import pygame
import sys
from .ui_elements import ImageButton, Button
from .background import StaticBackground
from .helper import scale_fit
from .color import WHITE, BLUE, GREEN, RED, PURPLE, YELLOW
from .player import Player

# Initialize Pygame
pygame.init()

screen_info = pygame.display.Info()

WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Chula Life")


class Level:
    def __init__(self, game):
        self.game = game
        self.buttons = []

    def draw(self):
        raise NotImplementedError(
            "This method should be implemented by subclasses.")

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(mouse_pos):
                    return button.action()
        return None


class WelcomeScreen(Level):
    def __init__(self, game):
        super().__init__(game)
        # Background image
        start_button = ImageButton(
            x=WIDTH // 2,
            y=HEIGHT // 2 + HEIGHT // 4,
            w=300,
            h=300,
            image_filename="assets/scene/welcome/Button_normal.png",
            hover_file_name="assets/scene/welcome/Button_big.png",
            active_file_name="assets/scene/welcome/Button_click.png",
            hover_scale_factor=1.3,
            active_scale_factor=1.25,
            action=lambda: self.game.set_level(LevelOne(self.game))
        )
        self.buttons.append(start_button)

    def draw(self):
        StaticBackground("assets/scene/welcome/startbg.png",
                         screen)
        bg_image, bg_rect = scale_fit(pygame.image.load(
            "assets/scene/welcome/startbg.png"), screen.get_rect())
        screen.blit(bg_image, bg_rect)

        for button in self.buttons:
            button.draw(screen)


class LevelOne(Level):
    def __init__(self, game):
        super().__init__(game)
        # Define level-specific buttons
        self.buttons = [
            Button(50, 500, 200, 50, "Go to Level 2", GREEN,
                   lambda: self.game.set_level(LevelTwo(self.game))),
            Button(300, 500, 200, 50, "Exit", RED, lambda: "exit"),
        ]
        self.buttons = [
            Button(300, 500, 200, 50, "Go to Level 2", GREEN,
                   lambda: self.game.set_level(LevelTwo(self.game))),
            Button(550, 500, 200, 50, "Exit", RED, lambda: "exit")
        ]

        # Define interactable objects as rectangles
        self.objects = [
            pygame.Rect(300, 200, 60, 60),  # Yellow object
            pygame.Rect(500, 300, 60, 60)   # Purple object
        ]
        self.object_colors = [YELLOW, PURPLE]
        self.player = Player(100, 100)

    def draw(self):
        screen.fill(WHITE)
        title_font = pygame.font.Font(None, 50)
        title_text = title_font.render("Level 1", True, BLUE)
        screen.blit(title_text, (WIDTH // 2 -
                    title_text.get_width() // 2, 100))

        # Draw objects
        for i, obj in enumerate(self.objects):
            pygame.draw.rect(screen, self.object_colors[i], obj)

        # Draw player
        self.player.draw(screen)

        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
        # Handle keyboard events for player movement
        self.player.handle_keys()

        # Check for interaction with objects
        self.check_interaction()

    def check_interaction(self):
        # Check if player collides with any object
        for obj in self.objects:
            if self.player.rect.colliderect(obj):
                print(f"Player collided with object at {obj}")
            else:
                print(f"Player did not collide with object at {obj}")

class LevelTwo(Level):
    def __init__(self, game):
        super().__init__(game)
        # Define level-specific buttons
        self.buttons = [
            Button(50, 500, 200, 50, "Back to Level 1", BLUE,
                   lambda: self.game.set_level(LevelOne(self.game))),
            Button(300, 500, 200, 50, "Exit", RED, lambda: "exit"),
            Button(550, 500, 200, 50, "Secret Action",
                   (128, 0, 128), lambda: self.secret_action())
        ]

    def draw(self):
        screen.fill(WHITE)
        title_font = pygame.font.Font(None, 50)
        title_text = title_font.render("Level 2", True, GREEN)
        screen.blit(title_text, (WIDTH // 2 -
                    title_text.get_width() // 2, 100))
        for button in self.buttons:
            button.draw(screen)

    def secret_action(self):
        print("Secret Action Activated!")
        # Implement other actions as desired.
