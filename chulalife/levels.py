import pygame
from typing import List
from .ui_elements import ImageButton, Button, ScreenOverlay, Heart
from .background import StaticBackground, WalkableTile
from .helper import scale_fit
from .color import WHITE, BLUE, GREEN, RED, PURPLE, YELLOW
from .player import Player
from .object import WarpDoor, Object, QuestCharector
from .screen import WIDTH, HEIGHT, screen
from .question import Question


# Initialize Pygame
pygame.init()


class Level:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.objects: List[List[Object]] = []
        self.current_scene = 0
        self.player = Player(0, 0, 0, 0)
        self.overlay = ScreenOverlay().add("hearts", Heart())

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

    def check_interaction(self):
        for obj in self.objects[self.current_scene]:
            if self.player.rect.colliderect(obj.rect):
                if isinstance(obj, WarpDoor):
                    self.current_scene = obj.warpTarget
                    self.player.rect.left = obj.next_pos_x
                    self.player.rect.top = obj.next_pos_y


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
        StaticBackground("assets/scene/welcome/startbg.png")
        bg_image, bg_rect = scale_fit(pygame.image.load(
            "assets/scene/welcome/startbg.png"), screen.get_rect())
        screen.blit(bg_image, bg_rect)

        for button in self.buttons:
            button.draw(screen)


class LevelOne(Level):
    def __init__(self, game):
        super().__init__(game)
        # Define level-specific buttons
        self.buttons = []
        self.overlay.set_visible(True)

        # create transparent warp door
        warp_door = pygame.Surface((100, 300), pygame.SRCALPHA)

        self.player = Player(100, 350, int(WIDTH/5.5),
                             int(HEIGHT/5.5))

        self.objects = [
            [
                WarpDoor(
                    warp_door,
                    WIDTH - 100,
                    int(HEIGHT/2) - 120,
                    100,
                    200,
                    1,
                    117,
                    407
                ),
                QuestCharector("Q1_chick", 1650, 300)
            ],
            [
                WarpDoor(
                    warp_door,
                    0,
                    410,
                    100,
                    220,
                    0,
                    1717,
                    413
                ),
                WarpDoor(
                    warp_door,
                    WIDTH - 100,
                    410,
                    100,
                    210,
                    2,
                    117,
                    197
                )
            ],
            [
                WarpDoor(
                    warp_door,
                    0,
                    197,
                    100,
                    200,
                    1,
                    1723,
                    407
                ),
            ],
        ]
        self.object_colors = [YELLOW, PURPLE]
        self.current_scene = 0

        self.bg = [
            StaticBackground("assets/scene/level_1/stage1(1_3).png"),
            StaticBackground("assets/scene/level_1/stage1(2_3).png"),
            StaticBackground("assets/scene/level_1/stage1(3_3).png"),
        ]

        self.walkable_mask = [
            WalkableTile("assets/scene/level_1/way1(1_3).png"),
            WalkableTile("assets/scene/level_1/way1(2_3).png"),
            WalkableTile("assets/scene/level_1/way1(3_3).png"),
        ]

    def draw(self):
        screen.fill(WHITE)
        # Draw background
        self.bg[self.current_scene].draw(screen)

        self.walkable_mask[self.current_scene].draw(screen)

        # Draw objects
        for i, obj in enumerate(self.objects[self.current_scene]):
            obj.draw()
        self.player.walkable_mask = self.walkable_mask[self.current_scene]
        self.player.draw(screen)

        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

        self.overlay.draw()

        # Handle keyboard events for player movement
        # Disabled when fullscreen overlay is open
        if not self.overlay.is_fullscreen_open:
            self.player.handle_keys()

            # Check for interaction with objects
            self.check_interaction()

    def check_interaction(self):
        for obj in self.objects[self.current_scene]:
            if self.player.rect.colliderect(obj.rect):
                if isinstance(obj, WarpDoor):
                    self.current_scene = obj.warpTarget
                    self.player.rect.left = obj.next_pos_x
                    self.player.rect.top = obj.next_pos_y
                if isinstance(obj, QuestCharector):
                    self.overlay.set_element_visible(
                        "hearts", False)
                    if not self.overlay.has_element("question"):
                        self.overlay.add("question", obj.question)
                        self.overlay.set_element_visible("question", True)
                    self.overlay.set_fullscreen_open(True)
            else:
                self.overlay.set_element_visible(
                    "hearts", True).remove("question")


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
