import pygame
from typing import List, TYPE_CHECKING, TypeVar
from .elements import ImageButton, ScreenOverlay, Heart
from .background import StaticBackground, WalkableTile, Background
from .helper import scale_fit
from .color import WHITE, BLUE, GREEN, RED, PURPLE, YELLOW
from .player import Player
from .object import WarpDoor, Object, QuestCharacter, BlockerCharacter
from .screen import WIDTH, HEIGHT, screen
from .logger import get_logger
from .setting import charector_interaction, initial_hearts
from .game_state import game_state

if TYPE_CHECKING:
    from .game import Game

GameType = TypeVar("GameType", bound="Game")  # type: ignore[type-arg]

logger = get_logger(__name__)


class Level:
    def __init__(self, game):
        self.game: Game = game
        self.buttons = []
        self.current_scene: int = 0
        self.objects: List[List[Object]] = []
        self.overlay: ScreenOverlay = ScreenOverlay().add("hearts", Heart())
        self.player: Player | None = Player((0, 0))
        self.bg: list[Background] = []
        self.walkable_mask = []

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(mouse_pos):
                    return button.action()
        return None

    def draw(self):
        screen.fill(WHITE)
        # Draw background
        if len(self.bg) > 0:
            self.bg[self.current_scene].draw(screen)

        if len(self.walkable_mask) > 0:
            self.walkable_mask[self.current_scene].draw(screen)

        # Draw objects
        if len(self.objects) > 0 and len(self.objects[self.current_scene]) > 0:
            for i, obj in enumerate(self.objects[self.current_scene]):
                obj.draw()

        if len(self.walkable_mask) > 0 and self.player is not None:
            self.player.walkable_mask = self.walkable_mask[self.current_scene]

        if self.player is not None:
            self.player.draw(screen)

        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

        self.overlay.draw()

        # Handle keyboard events for player movement
        # Disabled when fullscreen overlay is open
        if (not self.overlay.is_fullscreen_open or not charector_interaction) and self.player is not None:
            self.player.handle_keys()

            # Check for interaction with objects
        self.check_interaction()

    def check_interaction(self):
        if len(self.objects) == 0 or self.player is None:
            return
        for obj in self.objects[self.current_scene]:
            if self.player.rect.colliderect(obj.rect):
                if isinstance(obj, WarpDoor):
                    if obj.action is not None:
                        obj.action()
                        return
                    self.current_scene = obj.warpTarget
                    self.player.rect.left = obj.next_pos_x
                    self.player.rect.top = obj.next_pos_y
                elif isinstance(obj, QuestCharacter):
                    logger.debug(f"Player interact with {obj.name}")

                    if self.overlay.has_element("question"):
                        if obj.question.status == "done":
                            self.overlay\
                                .set_element_visible("question", False)\
                                .remove("question")\
                                .set_fullscreen_open(False)
                            obj.clear()
                    else:
                        if obj.question.status != "done":
                            self.overlay\
                                .add("question", obj.dialog)\
                                .set_element_visible("question", True)\
                                .set_fullscreen_open(True)

    def set_scene(self, scene: int, pos=(0, 0)):
        self.current_scene = scene
        if self.player is not None:
            self.player._rect.topleft = pos


class WelcomeScreen(Level):
    def __init__(self, game):
        super().__init__(game)
        self.buttons = [
            ImageButton(
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
        ]

        self.bg = [
            StaticBackground("assets/scene/welcome/startbg.png")
        ]

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

        self.player = Player((100, 350))

        self.objects = [
            [
                WarpDoor((WIDTH - 100, int(HEIGHT/2) -
                          120), (100, 200), 1, (117, 407)),
                QuestCharacter("Q1_chick", (1650, 300)),
            ],
            [
                WarpDoor((0, 410), (100, 220), 0, (1717, 413)),
                WarpDoor((WIDTH - 100, 410),
                         (100, 210), 2, (117, 197)),
                QuestCharacter("Q2_tiger", (1650, 300)),
            ],
            [
                WarpDoor((0, 197), (100, 200), 1, (1723, 407)),
                WarpDoor((WIDTH // 2 - 350 // 2, HEIGHT - 100),
                         (350, 100), 3, (0, 0), lambda: self.game.set_level(LevelTwo(self.game))),
                QuestCharacter("Q3_yellow", (367, 72)),
                QuestCharacter("Q4_red", (917, 622), (572*0.3, 972*0.3)),
                BlockerCharacter((1617, 72))
            ],
        ]

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


class LevelTwo(Level):
    def __init__(self, game):
        super().__init__(game)
        # Define level-specific buttons
        self.bg = [
            StaticBackground("assets/scene/level_2/way2(1_3).png",
                             "assets/scene/level_2/foreground2(1_3).png"),
            StaticBackground("assets/scene/level_2/way2(2_3).png",
                             "assets/scene/level_2/foreground2(2_3).png"),
            StaticBackground("assets/scene/level_2/stage2(3_3).png"),
        ]

        self.player = Player((100, 350))
        self.objects = [
            [
                QuestCharacter("Q5_jeab", (850, 175)),
                QuestCharacter("Q6_cat", (825, 550), (340, 340)),
                WarpDoor((WIDTH // 2 - 100, HEIGHT - 100), (250, 100),
                         1, (WIDTH // 2 - self.player.rect.w // 2, 20))
            ],
            [
                QuestCharacter("Q7_panda", (848, 545), after_action=lambda: self.game.set_level(
                    LevelThree(self.game))),
            ]
        ]


class LevelThree(Level):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player((100, 350))
        self.bg = [
            StaticBackground("assets/scene/level_3/way3(1_2).png",
                             "assets/scene/level_3/foreground3(1_2).png"),
            StaticBackground("assets/scene/level_3/way3(2_2).png",
                             "assets/scene/level_3/foreground3(2_2).png"),
        ]

        self.objects = [
            [
                QuestCharacter("Q8_bus", (500, 465),
                               (650*1.4, 420*1.2), after_action=lambda: self.set_scene(1, (500, 465))),
            ],
            [
                QuestCharacter("Q9_shiba", (850, 250),
                               after_action=lambda: self.game.set_level(LevelFour(self.game))),
            ]
        ]


# Need to implement LevelFour


class LevelFour(Level):
    def __init__(self, game):
        super().__init__(game)

        self.player = Player((600, 350))

        self.bg = [
            StaticBackground("assets/scene/level_4/way4.png",
                             "assets/scene/level_4/foreground4.png"),
        ]

        self.objects = [
            [
                QuestCharacter("Q10_deer", (200, 300), after_action=lambda: self.game.set_level(
                    LevelFive(self.game)))
            ]
        ]


class LevelFive(Level):
    def __init__(self, game):
        super().__init__(game)

        self.player = Player((1300, 525))
        self.player.facing = "left"

        self.bg = [
            StaticBackground("assets/scene/level_5/way5.png",
                             "assets/scene/level_5/foreground5.png"),
        ]

        self.objects = [
            [
                QuestCharacter("Q11_fox", (825, 475), after_action=lambda: self.game.set_level(
                    EndGame(self.game)))
            ]
        ]


class GameOver(Level):
    def __init__(self, game):
        super().__init__(game)
        # Define level-specific buttons
        self.buttons = [
            ImageButton(
                x=WIDTH//2,
                y=HEIGHT//2 + HEIGHT // 4 - 50,
                w=300,
                h=300,
                image_filename="assets/scene/game_over/new_game.png",
                hover_file_name="assets/scene/game_over/new_game.png",
                active_file_name="assets/scene/game_over/new_game.png",
                hover_scale_factor=1.3,
                active_scale_factor=1.25,
                action=self.reset_game
            )
        ]

        self.bg = [
            StaticBackground("assets/scene/game_over/game_over.png")
        ]

    def reset_game(self):
        game_state.hearts = initial_hearts
        self.game.set_level(WelcomeScreen(self.game))


class EndGame(Level):
    def __init__(self, game):
        super().__init__(game)
        # Define level-specific buttons
        self.buttons = [
            ImageButton(
                x=WIDTH//2,
                y=HEIGHT//2 + HEIGHT // 4 - 50,
                w=300,
                h=300,
                image_filename="assets/scene/win/back.png",
                hover_file_name="assets/scene/win/back.png",
                active_file_name="assets/scene/win/back.png",
                hover_scale_factor=1.3,
                active_scale_factor=1.25,
                action=self.reset_game
            )
        ]

        self.bg = [
            StaticBackground("assets/scene/win/win_page.png")
        ]

        self.player = None

    def reset_game(self):
        game_state.hearts = initial_hearts
        self.game.set_level(WelcomeScreen(self.game))
