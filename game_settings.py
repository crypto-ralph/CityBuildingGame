from enum import Enum, auto


class GameState(Enum):
    MAIN_MENU = auto()
    INGAME_SETTINGS = auto()
    SETTINGS = auto()
    GAME = auto()
    EXIT_PLAY = auto()
    EXIT_GAME = auto()


class GameSettings:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    GAME_WORLD_WIDTH = int(SCREEN_WIDTH * 0.75)
    GAME_WORLD_HEIGHT = SCREEN_HEIGHT
    UI_AREA_WIDTH = int(SCREEN_WIDTH * 0.25)
    UI_AREA_HEIGHT = SCREEN_HEIGHT
    GAME_STATE = GameState.MAIN_MENU

    @classmethod
    def set_screen_dimensions(cls, width, height):
        cls.SCREEN_WIDTH = width
        cls.SCREEN_HEIGHT = height
        cls.GAME_WORLD_WIDTH = int(width * 0.75)
        cls.GAME_WORLD_HEIGHT = height
        cls.UI_AREA_WIDTH = int(width * 0.25)
        cls.UI_AREA_HEIGHT = height
