import pygame

from button import SpriteButton


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.UI_BUTTON_COLOR = (150, 150, 150)
        self.HOVER_BUTTON_COLOR = (200, 200, 200)
        self.BUTTON_PADDING = 20
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50

        self.start_button = SpriteButton(
            x=50,
            y=50,
            width=200,
            height=50,
            text="Start Game",
            button_color=self.UI_BUTTON_COLOR,
            hover_color=self.HOVER_BUTTON_COLOR,
        )
        self.settings_button = SpriteButton(
            x=50, y=120, width=200, height=50, text="Settings", button_color=self.UI_BUTTON_COLOR, hover_color=self.HOVER_BUTTON_COLOR,
        )
        self.exit_button = SpriteButton(
            x=50,
            y=190,
            width=200,
            height=50,
            text="Exit Game",
            button_color=self.UI_BUTTON_COLOR,
            hover_color=self.HOVER_BUTTON_COLOR,
        )
        self.credits_button = SpriteButton(
            x=50, y=260, width=200, height=50, text="Credits", button_color=self.UI_BUTTON_COLOR, hover_color=self.HOVER_BUTTON_COLOR,
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