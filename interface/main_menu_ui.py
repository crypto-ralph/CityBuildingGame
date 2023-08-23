import pygame
from game_settings import GameSettings
from interface.button_builder import ButtonBuilder


class MainMenu:
    """
    Represents the main menu of the game.

    .. attribute:: UI_BUTTON_COLOR
        The color of the button when not hovered.
    .. attribute:: HOVER_BUTTON_COLOR
        The color of the button when hovered over.
    .. attribute:: BUTTON_PADDING
        The spacing between buttons.
    .. attribute:: BUTTON_WIDTH
        Width of each button.
    .. attribute:: BUTTON_HEIGHT
        Height of each button.
    """

    UI_BUTTON_COLOR = (150, 150, 150)
    HOVER_BUTTON_COLOR = (200, 200, 200)
    BUTTON_PADDING = 20
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50

    def __init__(self, screen: pygame.Surface):
        """
        Initialize a MainMenu instance.

        :param pygame.Surface screen: The game screen on which the menu will be displayed.
        """
        self.screen = screen
        self.button_x = GameSettings.SCREEN_WIDTH / 2 - self.BUTTON_WIDTH / 2
        self.first_button_y = GameSettings.SCREEN_HEIGHT * 0.2

        self.start_button = self.create_button(0, "Start Game")
        self.settings_button = self.create_button(1, "Settings")
        self.exit_button = self.create_button(2, "Exit Game")
        self.credits_button = self.create_button(3, "Credits")

        self.menu_buttons = pygame.sprite.Group(
            self.start_button, self.settings_button, self.exit_button, self.credits_button
        )

    def create_button(self, position: int, text: str) -> pygame.sprite.Sprite:
        """
        Create a button with a specific position and text.

        :param int position: Vertical position index of the button.
        :param str text: Display text for the button.
        :return: A button ready for rendering.
        :rtype: pygame.sprite.Sprite
        """
        button_spacing = self.BUTTON_HEIGHT + self.BUTTON_PADDING
        button_builder = ButtonBuilder()
        return (
            button_builder.position(self.button_x, self.first_button_y + position * button_spacing)
            .size(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
            .with_text(text)
            .with_colors(self.UI_BUTTON_COLOR, self.HOVER_BUTTON_COLOR)
            .build()
        )

    def draw(self):
        """
        Draw the main menu on the screen.
        """
        self.screen.fill((0, 0, 0))
        self.menu_buttons.draw(self.screen)
        pygame.display.flip()
