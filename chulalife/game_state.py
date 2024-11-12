from enum import Enum


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    LEVEL1 = 1

    @classmethod
    def _missing_(cls, value):
        print(f"ERROR: GameState({value}) does not exist, returning TITLE")
        return cls.TITLE
