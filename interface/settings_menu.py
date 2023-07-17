import pygame

from button import SpriteButton
from game_settings import GameSettings


class SettingsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.bg_color = (150, 150, 150)
        self.rect_color = (50, 50, 50)

        self.UI_BUTTON_COLOR = (150, 150, 150)
        self.HOVER_BUTTON_COLOR = (200, 200, 200)
        self.BUTTON_PADDING = 20
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50

        self.menu_width = int(self.BUTTON_WIDTH + 0.2 * self.BUTTON_WIDTH) # 60% of the screen width
        self.menu_height = int(GameSettings.SCREEN_HEIGHT - GameSettings.SCREEN_HEIGHT * 0.2) # 60% of the screen height
        self.menu_x = (GameSettings.SCREEN_WIDTH - self.menu_width) // 2
        self.menu_y = 0 + (GameSettings.SCREEN_HEIGHT * 0.1)

        self.menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)

        self.resolutions = [(640, 480), (800, 600), (1024, 768), (1280, 720), (1920, 1080)]
        self.buttons = pygame.sprite.Group()

        for i, resolution in enumerate(self.resolutions):
            x = self.menu_width // 2 - self.BUTTON_WIDTH // 2
            y = self.menu_y + self.BUTTON_PADDING + i * (self.BUTTON_HEIGHT + self.BUTTON_PADDING)

            text = f"{resolution[0]}x{resolution[1]}"
            button = SpriteButton(
                x, y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, text=text, button_color=self.UI_BUTTON_COLOR, hover_color=self.HOVER_BUTTON_COLOR,
            )
            self.buttons.add(button)

        self.back_button = SpriteButton(
            x=self.menu_width // 2 - self.BUTTON_WIDTH // 2,
            y=self.menu_height - 2 * self.BUTTON_PADDING - self.BUTTON_HEIGHT,
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            text="Back",
            button_color=self.UI_BUTTON_COLOR,
            hover_color=self.HOVER_BUTTON_COLOR,
        )
        self.buttons.add(self.back_button)

        self.update_menu_positions()

    def update_menu_positions(self):
        for i, button in enumerate(self.buttons):
            button.rect.x = GameSettings.SCREEN_WIDTH // 2 - self.BUTTON_WIDTH // 2
            button.rect.y = self.menu_y + self.BUTTON_PADDING + i * (self.BUTTON_HEIGHT + self.BUTTON_PADDING)

        self.back_button.rect.x = GameSettings.SCREEN_WIDTH // 2 - self.BUTTON_WIDTH // 2
        self.back_button.rect.y = self.menu_height - 1 * self.BUTTON_PADDING

        # resize menu rect
        self.menu_rect.x = (GameSettings.SCREEN_WIDTH - self.menu_width) // 2
        self.menu_y = 0 + (GameSettings.SCREEN_HEIGHT * 0.1)

    def draw(self):
        # First fill the surface with the game visible or a black screen for the main menu
        # self.screen.fill(self.bg_color)
        # Then draw the rectangle
        pygame.draw.rect(self.screen, self.rect_color, self.menu_rect)
        # Then draw your menu elements
        self.buttons.draw(self.screen)
        # Rest of your draw code...
        pygame.display.flip()