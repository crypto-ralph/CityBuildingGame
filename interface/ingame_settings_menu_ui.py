import pygame

from game_settings import GameSettings
from interface.button import SpriteButton
from interface.button_builder import ButtonBuilder


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.bg_color = (150, 150, 150)
        self.rect_color = (50, 50, 50)

        self.UI_BUTTON_COLOR = (150, 150, 150)
        self.HOVER_BUTTON_COLOR = (200, 200, 200)
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50
        self.BUTTON_PADDING = 20

        self.buttons = pygame.sprite.Group()

        self.menu_width = int(self.BUTTON_WIDTH + 0.2 * self.BUTTON_WIDTH)  # 60% of the screen width
        self.menu_height = int(
            GameSettings.SCREEN_HEIGHT - GameSettings.SCREEN_HEIGHT * 0.2
        )  # 60% of the screen height
        self.menu_x = (GameSettings.SCREEN_WIDTH - self.menu_width) // 2
        self.menu_y = 0 + (GameSettings.SCREEN_HEIGHT * 0.1)

        self.menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)

    def draw(self):
        pygame.draw.rect(self.screen, self.rect_color, self.menu_rect)
        self.buttons.draw(self.screen)
        pygame.display.flip()

    def update_menu_rect(self):
        """Recalculate the size and position of the menu rectangle."""
        self.menu_width = int(self.BUTTON_WIDTH + 0.2 * self.BUTTON_WIDTH)  # 60% of the screen width
        self.menu_height = int(
            GameSettings.SCREEN_HEIGHT - GameSettings.SCREEN_HEIGHT * 0.2
        )  # 60% of the screen height
        self.menu_x = (GameSettings.SCREEN_WIDTH - self.menu_width) // 2
        self.menu_y = 0 + (GameSettings.SCREEN_HEIGHT * 0.1)
        self.menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)


class SettingsMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

        # Buttons configuration
        buttons_config = [
            {
                "text": "Resolution",
                "order": 0,
            },
            {"text": "Save Game", "order": 1},
            {"text": "Load Game", "order": 2},
            {"text": "Exit Game", "order": 3},
            {"text": "Back To Game", "order": 4, "position": "bottom"},
        ]

        for btn_config in buttons_config:
            if btn_config.get("position") == "bottom":
                y = self.menu_height - 1 * self.BUTTON_PADDING
            else:
                y = self.menu_y + self.BUTTON_PADDING + btn_config["order"] * (self.BUTTON_HEIGHT + self.BUTTON_PADDING)

            x = GameSettings.SCREEN_WIDTH // 2 - self.BUTTON_WIDTH // 2
            button = (
                ButtonBuilder()
                .position(x, y)
                .size(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
                .with_text(btn_config["text"])
                .with_colors(self.UI_BUTTON_COLOR, self.HOVER_BUTTON_COLOR)
                .build()
            )
            self.buttons.add(button)


class ResolutionMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)

        self.resolutions = {(800, 600): None, (1024, 768): None, (1280, 720): None, (1920, 1080): None}
        self.buttons = pygame.sprite.Group()

        for i, resolution in enumerate(self.resolutions.keys()):
            x = self.menu_width // 2 - self.BUTTON_WIDTH // 2
            y = self.menu_y + self.BUTTON_PADDING + i * (self.BUTTON_HEIGHT + self.BUTTON_PADDING)

            text = f"{resolution[0]}x{resolution[1]}"
            button = SpriteButton(
                x,
                y,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                text=text,
                button_color=self.UI_BUTTON_COLOR,
                hover_color=self.HOVER_BUTTON_COLOR,
            )
            self.buttons.add(button)
            self.resolutions[resolution] = button

        # create the back button
        self.back_button = (
            ButtonBuilder()
            .position(0, 0)  # We'll set the actual position in `update_menu_positions`
            .size(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
            .with_text("Back")
            .with_colors(self.UI_BUTTON_COLOR, self.HOVER_BUTTON_COLOR)
            .build()
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

    def highlight_current_resolution(self):
        current_resolution = (GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT)

        # Reset all buttons to default color
        for button in self.resolutions.values():
            button.set_color(self.UI_BUTTON_COLOR)

            # Get the button corresponding to the current resolution and highlight it
            current_resolution_button = self.resolutions.get(current_resolution)
            if current_resolution_button:
                current_resolution_button.set_color((100, 100, 100))

    def update_menu_rect(self):
        """Override to recalculate the menu rectangle and reposition buttons."""
        super().update_menu_rect()
        self.update_menu_positions()

    def draw(self):
        pygame.draw.rect(self.screen, self.rect_color, self.menu_rect)
        self.buttons.draw(self.screen)
        pygame.display.flip()
