import pygame

from button import SpriteButton
from game_settings import GameSettings


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.UI_BUTTON_COLOR = (150, 150, 150)
        self.HOVER_BUTTON_COLOR = (200, 200, 200)
        self.BUTTON_PADDING = 20
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50

        self.BUTTON_X = GameSettings.SCREEN_WIDTH / 2 - self.BUTTON_WIDTH /2
        self.BUTTON_Y_INIT = 120
        self.BUTTON_PADDING = self.BUTTON_HEIGHT + 20

        self.start_button = SpriteButton(
            x=self.BUTTON_X,
            y=self.BUTTON_Y_INIT,
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            text="Start Game",
            button_color=self.UI_BUTTON_COLOR,
            hover_color=self.HOVER_BUTTON_COLOR,
        )
        self.settings_button = SpriteButton(
            x=self.BUTTON_X,
            y=self.BUTTON_Y_INIT + self.BUTTON_PADDING,
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            text="Settings",
            button_color=self.UI_BUTTON_COLOR,
            hover_color=self.HOVER_BUTTON_COLOR,
        )
        self.exit_button = SpriteButton(
            x=self.BUTTON_X,
            y=self.BUTTON_Y_INIT + 2 * self.BUTTON_PADDING,
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            text="Exit Game",
            button_color=self.UI_BUTTON_COLOR,
            hover_color=self.HOVER_BUTTON_COLOR,
        )
        self.credits_button = SpriteButton(
            x=self.BUTTON_X,
            y=self.BUTTON_Y_INIT + 3 * self.BUTTON_PADDING,
            width=200,
            height=50,
            text="Credits",
            button_color=self.UI_BUTTON_COLOR,
            hover_color=self.HOVER_BUTTON_COLOR,
        )
        self.menu_buttons = pygame.sprite.Group()
        self.menu_buttons.add(self.start_button)
        self.menu_buttons.add(self.settings_button)
        self.menu_buttons.add(self.exit_button)
        self.menu_buttons.add(self.credits_button)

    def draw(self):
        # Draw the screen
        self.screen.fill((0, 0, 0))
        self.menu_buttons.draw(self.screen)
        pygame.display.flip()